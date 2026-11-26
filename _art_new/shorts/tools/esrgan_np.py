"""Real-ESRGAN (x4plus_anime_6B) 추론을 torch 없이 numpy로. 사용: python esrgan_np.py weights.pth in.png out.png"""
import sys, zipfile, pickle, collections, numpy as np
from PIL import Image

def load_pth(path):
    zf = zipfile.ZipFile(path)
    root = zf.namelist()[0].split('/')[0]
    class Storage:
        def __init__(self, dtype): self.dtype = dtype
    class FloatStorage(Storage): pass
    def rebuild(storage, offset, size, stride, *a):
        key, dtype = storage
        buf = np.frombuffer(zf.read(f'{root}/data/{key}'), dtype=dtype)
        n = int(np.prod(size)) if size else 1
        arr = np.lib.stride_tricks.as_strided(buf[offset:], shape=tuple(size), strides=tuple(s * buf.itemsize for s in stride)) if size else buf[offset:offset+1]
        return np.array(arr, dtype=np.float32)
    class U(pickle.Unpickler):
        def find_class(self, mod, name):
            if name == '_rebuild_tensor_v2': return rebuild
            if name == 'OrderedDict': return collections.OrderedDict
            if name.endswith('Storage'): return {'FloatStorage': np.float32, 'HalfStorage': np.float16}.get(name, np.float32)
            return super().find_class(mod, name)
        def persistent_load(self, pid):
            _, dtype, key, loc, n = pid
            return (key, dtype)
    sd = U(zf.open(f'{root}/data.pkl')).load()
    if 'params_ema' in sd: sd = sd['params_ema']
    elif 'params' in sd: sd = sd['params']
    return sd

def conv(x, w, b):  # x: (C,H,W) w: (O,C,3,3)
    C, H, W = x.shape
    xp = np.pad(x, ((0, 0), (1, 1), (1, 1)))
    cols = np.empty((C * 9, H * W), np.float32)
    i = 0
    for c0 in range(C):
        pass
    # im2col 순서: (C, ky, kx)
    s = np.lib.stride_tricks.sliding_window_view(xp, (3, 3), axis=(1, 2))  # C,H,W,3,3
    cols = s.transpose(0, 3, 4, 1, 2).reshape(C * 9, H * W)
    out = w.reshape(w.shape[0], -1) @ cols
    out += b[:, None]
    return out.reshape(w.shape[0], H, W)

def lrelu(x):
    return np.where(x > 0, x, 0.2 * x)

def net(x, P):
    def c(name, t): return conv(t, P[name + '.weight'], P[name + '.bias'])
    feat = c('conv_first', x)
    body = feat
    for i in range(6):
        rrdb_in = body
        for r in (1, 2, 3):
            pre = f'body.{i}.rdb{r}.'
            x0 = body
            x1 = lrelu(c(pre + 'conv1', x0))
            x2 = lrelu(c(pre + 'conv2', np.concatenate([x0, x1])))
            x3 = lrelu(c(pre + 'conv3', np.concatenate([x0, x1, x2])))
            x4 = lrelu(c(pre + 'conv4', np.concatenate([x0, x1, x2, x3])))
            x5 = c(pre + 'conv5', np.concatenate([x0, x1, x2, x3, x4]))
            body = x5 * 0.2 + x0
        body = body * 0.2 + rrdb_in
    feat = feat + c('conv_body', body)
    feat = lrelu(c('conv_up1', feat.repeat(2, 1).repeat(2, 2)))
    feat = lrelu(c('conv_up2', feat.repeat(2, 1).repeat(2, 2)))
    return c('conv_last', lrelu(c('conv_hr', feat)))

def upscale_rgb(arr, P, tile=96, pad=10):
    H, W, _ = arr.shape
    x = arr.transpose(2, 0, 1).astype(np.float32) / 255.0
    out = np.zeros((3, H * 4, W * 4), np.float32)
    for y0 in range(0, H, tile):
        for x0 in range(0, W, tile):
            y1, x1 = min(H, y0 + tile), min(W, x0 + tile)
            ya, xa = max(0, y0 - pad), max(0, x0 - pad)
            yb, xb = min(H, y1 + pad), min(W, x1 + pad)
            o = net(x[:, ya:yb, xa:xb], P)
            out[:, y0 * 4:y1 * 4, x0 * 4:x1 * 4] = o[:, (y0 - ya) * 4:(y0 - ya + y1 - y0) * 4, (x0 - xa) * 4:(x0 - xa + x1 - x0) * 4]
    return (np.clip(out, 0, 1).transpose(1, 2, 0) * 255).round().astype(np.uint8)

def upscale_file(P, src, dst):
    im = Image.open(src)
    rgba = im.convert('RGBA')
    rgb = np.array(rgba.convert('RGB'))
    up = upscale_rgb(rgb, P)
    res = Image.fromarray(up)
    if im.mode in ('RGBA', 'LA', 'P'):
        a = rgba.getchannel('A').resize(res.size, Image.LANCZOS)
        res.putalpha(a)
    res.save(dst)

if __name__ == '__main__':
    P = load_pth(sys.argv[1])
    for i in range(2, len(sys.argv), 2):
        upscale_file(P, sys.argv[i], sys.argv[i + 1])
        print('ok', sys.argv[i + 1], flush=True)
