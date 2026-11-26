import cv2, numpy as np, sys, glob, os
from PIL import Image
for p in sorted(glob.glob('/tmp/w/x4w/*.png')):
    im = np.array(Image.open(p).convert('RGBA'))
    rgb = im[..., :3].astype(np.int16); a = im[..., 3]
    m = (a > 100).astype(np.uint8)
    mn = rgb.min(2); mx = rgb.max(2)
    bright = ((mn > 222) & (mx - mn < 28)).astype(np.uint8)
    k = np.ones((3, 3), np.uint8)
    for _ in range(30):
        er = cv2.erode(m, k)
        edge = (m == 1) & (er == 0) & (bright == 1)
        if not edge.any(): break
        m[edge] = 0
    # 작은 구멍·가시 정리
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, k)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    big = 1 + np.argmax(st[1:, 4]); keep = np.zeros_like(m)
    for i in range(1, n):
        if st[i, 4] > st[big, 4] * 0.01: keep[lab == i] = 1
    # 가장자리 1px 안쪽으로 + 부드럽게
    keep = cv2.erode(keep, k)
    af = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 1.3)
    af = np.clip((af - 0.15) / 0.7, 0, 1)
    out = im.copy(); out[..., 3] = (af * 255).astype(np.uint8)
    ys, xs = np.where(out[..., 3] > 0)
    out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    Image.fromarray(out).save('/tmp/w/x4w2/' + os.path.basename(p))
    print(os.path.basename(p), out.shape)
