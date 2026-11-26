"""배경을 GIF처럼 살리기: 물결·버드나무 흔들림·풀·구름 흐름·해/달빛·별 반짝임 + 빛 알갱이·낙엽·반딧불.
노을/밤 호수공원 그림(같은 구도) 전용 좌표. 좌표는 세로 600px 미리보기 기준 × S."""
import math
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter

H = 1920
S = H / 600.0


def _smooth(m, k):
    k = int(k) | 1
    return cv2.GaussianBlur(m.astype(np.float32), (k, k), 0)


def _box(Wb, x0, y0, x1, y1, feather=40, ramp=True, pw=1.3):
    """나무처럼 위(뿌리 쪽이 아니라 가지 붙은 곳)는 덜, 아래로 늘어진 끝은 많이 흔들리는 무게"""
    m = np.zeros((H, Wb), np.float32)
    X0, Y0, X1, Y1 = [int(v * S) for v in (x0, y0, x1, y1)]
    X1 = min(X1, Wb); Y1 = min(Y1, H)
    if ramp:
        r = np.linspace(0, 1, Y1 - Y0, dtype=np.float32)[:, None] ** pw
        m[Y0:Y1, X0:X1] = r
    else:
        m[Y0:Y1, X0:X1] = 1
    return _smooth(m, feather * 2 + 1)


class LivingBG:
    def __init__(self, img_rgb, kind, night_ref=None):
        """img_rgb: H 높이로 맞춘 PIL RGB. kind: 'sunset' | 'night'. night_ref: 물 찾기용 밤 그림(같은 구도)"""
        self.kind = kind
        self.src = np.ascontiguousarray(np.array(img_rgb.convert("RGB")))
        Wb = self.src.shape[1]
        self.Wb = Wb
        ref = np.array((night_ref or img_rgb).convert("RGB").resize((Wb, H))).astype(np.int32)
        R, G, B = ref[..., 0], ref[..., 1], ref[..., 2]
        yy = np.arange(H)[:, None]
        water = (B > 70) & (B > R + 20) & (yy > 385 * S) & (yy < 552 * S)
        self.water = _smooth(water, 9)
        self.water_hard = water
        # 기둥(가로등)은 안 흔들리게
        lamp = np.zeros((H, Wb), np.float32)
        for (a, b) in [(92, 138), (698, 748)]:
            lamp[int(270 * S):, int(a * S):int(b * S)] = 1
        lamp = _smooth(lamp, 25)
        self.lamp = lamp
        keep = 1 - lamp
        # 버드나무(크게), 섬 버드나무(중간), 먼 나무줄(살짝)
        self.tree = (_box(Wb, 0, 100, 240, 480, 30) * 1.0 + _box(Wb, 660, 195, 800, 480, 30) * 1.0
                     + _box(Wb, 505, 280, 622, 425, 22) * 0.7 + _box(Wb, 228, 312, 515, 388, 14) * 0.25
                     + _box(Wb, 600, 260, 700, 420, 20) * 0.45)
        self.tree = np.clip(self.tree, 0, 1) * keep * (1 - self.water * 0.9)
        # 풀·덤불: 아래가 고정, 위 끝이 흔들림
        g = np.zeros((H, Wb), np.float32)
        y0, y1 = int(470 * S), int(600 * S)
        g[y0:y1] = np.linspace(1, 0.15, y1 - y0, dtype=np.float32)[:, None]
        self.grass = _smooth(g, 31) * keep * (1 - self.water)
        # 구름 띠(하늘 위쪽), 나무 꼭대기는 빼기
        c = np.zeros((H, Wb), np.float32)
        c[: int(205 * S)] = 1
        c[int(150 * S):, int(470 * S):] = 0   # 오른쪽 아파트 꼭대기는 그대로
        c[int(200 * S):, int(220 * S):int(320 * S)] = 0
        c = _smooth(c, 41) * (1 - np.clip(self.tree * 3, 0, 1))
        self.cloud = c
        # 해·달 위치
        self.sun = (390 * S, 255 * S) if kind == "sunset" else (612 * S, 78 * S)
        # 반짝이(별·창문·달) 덩어리마다 다른 박자
        self.stars = None
        if kind == "night":
            sr = np.array(img_rgb.convert("RGB")).astype(np.int32)
            st = ((sr[..., 0] > 170) & (sr[..., 1] > 150) & (yy < 300 * S)).astype(np.uint8)
            st = cv2.dilate(st, np.ones((5, 5), np.uint8))
            n, lab, stats, cen = cv2.connectedComponentsWithStats(st)
            rng = np.random.default_rng(5)
            ph = rng.uniform(0, 6.28, n).astype(np.float32)
            spd = rng.uniform(1.5, 4.0, n).astype(np.float32)
            big = stats[:, cv2.CC_STAT_AREA] > 3000  # 달
            win = cen[:, 1] > 150 * S                # 건물 창문: 아주 천천히
            spd[win] = rng.uniform(0.3, 0.8, win.sum())
            amp = np.where(win, 0.18, 0.55).astype(np.float32)
            amp[big] = 0.0
            amp[0] = 0
            self.stars = (lab, ph, spd, amp)
        self.glints = self._make_glints()
        self.grid_x, self.grid_y = None, None

    def _make_glints(self):
        rng = np.random.default_rng(11)
        ys, xs = np.nonzero(self.water_hard[::4, ::4])
        pts = []
        sx = self.sun[0]
        for _ in range(140):
            i = rng.integers(0, len(ys))
            x, y = xs[i] * 4, ys[i] * 4
            # 해(달) 그림자 기둥 근처에 더 많이
            if self.kind == "sunset" and abs(x - sx) > 340 * (1 + (y - 1230) / 500) and rng.random() < 0.7:
                continue
            if self.kind == "night" and rng.random() < 0.3:
                continue
            pts.append((x, y, rng.integers(14, 60), rng.uniform(0, 6.28), rng.uniform(1.5, 3.5)))
        return pts

    def frame(self, off, t, wind=1.0):
        """off: 가로 자를 위치(px), t: 초. 자른 W×H RGB 배열을 돌려줌"""
        Wc = 1080
        if self.grid_x is None:
            gx, gy = np.meshgrid(np.arange(Wc, dtype=np.float32), np.arange(H, dtype=np.float32))
            self.grid_x, self.grid_y = gx, gy
        X = self.grid_x + off
        Y = self.grid_y
        sl = np.s_[:, off:off + Wc]
        tree, grass, water, cloud = self.tree[sl], self.grass[sl], self.water[sl], self.cloud[sl]
        # 바람: 느린 큰 흔들림 + 가끔 돌풍
        gust = 1 + 0.6 * max(0.0, math.sin(t * 0.7 + 1.0)) ** 3
        dx = tree * wind * gust * (13 * np.sin(t * 1.5 + Y * 0.0042 + X * 0.0013) + 4 * np.sin(t * 3.7 + Y * 0.02))
        dy = tree * wind * 2.5 * np.sin(t * 1.9 + X * 0.004)
        dx += grass * wind * gust * 6 * np.sin(t * 2.4 + X * 0.018 + Y * 0.004)
        # 물결: 가로로 일렁 + 아래로 갈수록 크게
        k = np.clip((Y - 1230) / 520, 0, 1)
        dx += water * (2.5 + 6 * k) * np.sin(Y * 0.085 - t * 2.4 + X * 0.003)
        dy += water * (1.2 + 2.0 * k) * np.sin(Y * 0.05 + X * 0.01 - t * 1.7)
        # 구름: 천천히 흐르고 살짝 부풀었다 줄었다
        dx += cloud * (-9 * t + 6 * np.sin(t * 0.6 + Y * 0.01))
        dy += cloud * 2 * np.sin(t * 0.8 + X * 0.004)
        out = cv2.remap(self.src, (X - dx).astype(np.float32), (Y - dy).astype(np.float32),
                        cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        out = out.astype(np.float32)
        # 해/달빛 숨쉬기
        sx, sy = self.sun[0] - off, self.sun[1]
        r = np.sqrt((self.grid_x - sx) ** 2 + (Y - sy) ** 2)
        if self.kind == "sunset":
            pulse = 0.5 + 0.5 * math.sin(t * 1.3)
            glow = np.exp(-(r / (430 + 40 * pulse)) ** 2) * (26 + 16 * pulse)
            ang = np.arctan2(Y - sy, self.grid_x - sx)
            rays = (0.5 + 0.5 * np.sin(ang * 11 + t * 0.35)) ** 3 * np.exp(-(r / 1100)) * np.clip((r - 200) / 200, 0, 1) * 14 * (Y < 1300)
            out += (glow + rays)[..., None] * np.array([1.0, 0.72, 0.45], np.float32)
        else:
            pulse = 0.5 + 0.5 * math.sin(t * 1.1)
            glow = np.exp(-(r / (300 + 30 * pulse)) ** 2) * (16 + 10 * pulse)
            out += glow[..., None] * np.array([1.0, 0.95, 0.75], np.float32)
            lab, ph, spd, amp = self.stars
            L = lab[sl]
            fac = (amp * np.sin(t * spd + ph)).astype(np.float32)[L]
            out *= (1 + fac)[..., None]
            out += (np.clip(fac, 0, 1) * 60)[..., None] * np.array([1, 0.95, 0.7], np.float32)
            # 가로등 빛 흔들림
            for (lx, ly) in [(117 * S, 315 * S), (707 * S, 315 * S)]:
                rr = np.sqrt((self.grid_x - (lx - off)) ** 2 + (Y - ly) ** 2)
                fl = 0.85 + 0.15 * math.sin(t * 9 + lx) * math.sin(t * 2.3)
                out += (np.exp(-(rr / 230) ** 2) * 38 * fl)[..., None] * np.array([1.0, 0.85, 0.5], np.float32)
        # 물 위 반짝임
        lay = np.zeros((H, Wc), np.float32)
        for (x, y, ln, p, s) in self.glints:
            xx = int(x - off)
            if xx < -ln or xx > Wc:
                continue
            b = max(0.0, math.sin(t * s + p)) ** 3
            if b < 0.05:
                continue
            x0, x1 = max(0, xx), min(Wc, xx + ln)
            lay[y:y + 4, x0:x1] = np.maximum(lay[y:y + 4, x0:x1], b)
        lay = cv2.GaussianBlur(lay, (0, 0), 2.2)
        col = np.array([255, 235, 190], np.float32) if self.kind == "sunset" else np.array([200, 215, 255], np.float32)
        out += lay[..., None] * col * 0.85
        return np.clip(out, 0, 255).astype(np.uint8)


# ---------- 화면 앞 입자: 빛 알갱이·낙엽·반딧불 ----------
def _leaf_sprite(sz, col):
    im = Image.new("RGBA", (sz * 3, sz * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w, h = sz * 3, sz * 3
    d.ellipse((w * 0.12, h * 0.36, w * 0.88, h * 0.64), fill=col + (255,), outline=(90, 40, 30, 255), width=max(2, sz // 6))
    d.line((w * 0.16, h * 0.5, w * 0.84, h * 0.5), fill=(120, 55, 30, 200), width=max(1, sz // 8))
    return im.resize((sz * 2, sz * 2), Image.LANCZOS)


def _glow_sprite(r, col, core=0.35):
    s = int(r * 4)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    a = np.zeros((s, s), np.float32)
    yy, xx = np.mgrid[0:s, 0:s]
    d = np.sqrt((xx - s / 2) ** 2 + (yy - s / 2) ** 2) / (s / 2)
    a = np.clip(np.exp(-(d / 0.45) ** 2) + (d < core * 0.5) * 0.6, 0, 1)
    arr = np.zeros((s, s, 4), np.uint8)
    arr[..., :3] = col
    arr[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


class Particles:
    def __init__(self, seed=3):
        rng = np.random.default_rng(seed)
        self.rng = rng
        cols = [(236, 132, 58), (214, 96, 46), (246, 178, 72), (196, 82, 52)]
        self.leaf_sp = [[_leaf_sprite(int(s), c) for c in cols] for s in (16, 22, 28)]
        self.mote_sp = [_glow_sprite(r, (255, 226, 160)) for r in (6, 10, 16)]
        self.fly_sp = _glow_sprite(12, (210, 255, 120), 0.5)
        self.leaves = [dict(x=rng.uniform(0, 1080), y=rng.uniform(-200, 1920), v=rng.uniform(70, 130), sw=rng.uniform(40, 110),
                            f=rng.uniform(0.8, 1.8), p=rng.uniform(0, 6.28), sz=rng.integers(0, 3), c=rng.integers(0, 4),
                            rs=rng.uniform(-160, 160), par=rng.uniform(0.6, 1.4)) for _ in range(14)]
        self.motes = [dict(x=rng.uniform(0, 1080), y=rng.uniform(0, 1920), v=rng.uniform(12, 40), p=rng.uniform(0, 6.28),
                           s=rng.integers(0, 3), tw=rng.uniform(1, 3)) for _ in range(34)]
        self.flies = [dict(x=rng.uniform(0, 1080), y=rng.uniform(900, 1800), p=rng.uniform(0, 6.28), q=rng.uniform(0, 6.28),
                           f=rng.uniform(0.3, 0.7), tw=rng.uniform(1.5, 3.5)) for _ in range(16)]

    def draw(self, canvas, t, kind, cam=0.0, leaves=True, motes=True, flies=False, strength=1.0):
        """canvas: PIL RGBA. cam: 배경이 흐른 양(px) → 입자도 조금 같이 흐름"""
        W, Hh = canvas.size
        if motes:
            for m in self.motes:
                y = (m["y"] - m["v"] * t) % (Hh + 100) - 50
                x = (m["x"] + 30 * math.sin(t * 0.7 + m["p"]) - cam * 0.3) % (W + 60) - 30
                a = (0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * m["tw"] + m["p"]))) * strength
                if kind == "night":
                    a *= 0.6
                sp = self.mote_sp[m["s"]]
                if a < 1:
                    sp = sp.copy(); sp.putalpha(sp.getchannel("A").point(lambda v, a=a: int(v * a)))
                canvas.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height / 2)))
        if leaves:
            for L in self.leaves:
                y = (L["y"] + L["v"] * t) % (Hh + 300) - 150
                x = (L["x"] + L["sw"] * math.sin(t * L["f"] + L["p"]) - cam * 0.5 * L["par"] + 25 * t) % (W + 200) - 100
                sp = self.leaf_sp[L["sz"]][L["c"]]
                flip = abs(math.cos(t * L["f"] * 1.3 + L["p"]))  # 뒤집히며 팔랑
                sp = sp.resize((sp.width, max(2, int(sp.height * (0.25 + 0.75 * flip)))), Image.BILINEAR)
                sp = sp.rotate(L["rs"] * t + L["p"] * 57, expand=True, resample=Image.BICUBIC)
                if strength < 1:
                    sp.putalpha(sp.getchannel("A").point(lambda v: int(v * strength)))
                canvas.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height / 2)))
        if flies:
            for F in self.flies:
                x = (F["x"] + 140 * math.sin(t * F["f"] + F["p"]) - cam * 0.4) % (W + 60) - 30
                y = F["y"] + 90 * math.sin(t * F["f"] * 1.3 + F["q"])
                a = max(0.0, math.sin(t * F["tw"] + F["p"])) ** 2 * strength
                if a < 0.04:
                    continue
                sp = self.fly_sp.copy(); sp.putalpha(sp.getchannel("A").point(lambda v, a=a: int(v * a)))
                canvas.alpha_composite(sp, (int(x - sp.width / 2), int(y - sp.height / 2)))


def sway(sp, t, amp=0.018, hz=1.3, ph=0.0, anchor_bottom=True):
    """캐릭터 몸을 살짝 기울였다 돌아오기(머리 쪽이 더 움직이고 발은 고정) — 숨쉬듯 살아 있는 느낌"""
    a = np.array(sp)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    k = (1 - yy / h) if anchor_bottom else (yy / h)
    k = k ** 1.6
    dx = amp * w * k * math.sin(t * hz * 2 * math.pi + ph)
    dy = -0.012 * h * k * (0.5 + 0.5 * math.sin(t * hz * 4 * math.pi + ph))  # 숨 들이쉴 때 살짝 위로
    out = cv2.remap(a, xx - dx, yy - dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return Image.fromarray(out, "RGBA")


# ---------- 2화: 시장 골목 ----------
class MarketBG:
    """시장 골목 그림(1100x614 구도) 전용: 천막·파라솔 펄럭, 벚나무 흔들림, 구름 숨쉬기, 젖은 바닥 일렁임·반짝임"""
    def __init__(self, img_rgb):
        self.src = np.ascontiguousarray(np.array(img_rgb.convert("RGB")))
        Hh, Wb = self.src.shape[:2]
        self.Wb = Wb
        s = Hh / 614.0
        self.s = s
        def box(x0, y0, x1, y1, f=25, pw=1.2, ramp=True):
            m = np.zeros((Hh, Wb), np.float32)
            X0, Y0, X1, Y1 = int(x0 * s), int(y0 * s), min(Wb, int(x1 * s)), min(Hh, int(y1 * s))
            m[Y0:Y1, X0:X1] = (np.linspace(0, 1, Y1 - Y0, dtype=np.float32)[:, None] ** pw) if ramp else 1
            return _smooth(m, f * 2 + 1)
        self.flag = np.clip(box(775, 150, 1100, 390, 25, 1.0) * 1.0 + box(232, 280, 478, 335, 14) * 0.7
                            + box(25, 168, 432, 292, 18, 1.6) * 0.45 + box(638, 268, 792, 322, 12) * 0.6
                            + box(430, 312, 545, 352, 8) * 0.4, 0, 1)
        self.tree = np.clip(box(0, 15, 125, 280, 20) + box(955, 55, 1100, 205, 20), 0, 1) * (1 - _smooth(box(120, 0, 165, 614, 4, ramp=False) > 0.5, 15))
        a = self.src.astype(np.int32)
        R, G, B = a[..., 0], a[..., 1], a[..., 2]
        yy = np.arange(Hh)[:, None]; xx = np.arange(Wb)[None, :]
        cl = ((R > 215) & (G > 200) & (B > 200) | ((R > 210) & (R > B + 15) & (G < 200))) & (yy > 60 * s) & (yy < 235 * s) & (xx > 395 * s) & (xx < 870 * s)
        self.cloud = _smooth(cv2.dilate(cl.astype(np.uint8), np.ones((15, 15), np.uint8)), 31)
        fl = np.zeros((Hh, Wb), np.float32)
        fl[int(395 * s):, int(330 * s):int(760 * s)] = 1
        self.floor = _smooth(fl, 61)
        rng = np.random.default_rng(4)
        self.glints = [(rng.uniform(380, 740) * s, rng.uniform(400, 610) * s, int(rng.integers(10, 40)), rng.uniform(0, 6.28), rng.uniform(1.2, 3.0)) for _ in range(70)]
        self.grid = None

    def frame(self, off, t, wind=1.0):
        Wc, Hh = 1080, self.src.shape[0]
        if self.grid is None:
            self.grid = np.meshgrid(np.arange(Wc, dtype=np.float32), np.arange(Hh, dtype=np.float32))
        gx, Y = self.grid
        X = gx + off
        sl = np.s_[:, off:off + Wc]
        fg, tr, cl, fl = self.flag[sl], self.tree[sl], self.cloud[sl], self.floor[sl]
        gust = 1 + 0.7 * max(0.0, math.sin(t * 0.9)) ** 3
        dx = fg * wind * gust * (7 * np.sin(t * 3.1 + X * 0.006 + Y * 0.01))
        dy = fg * wind * gust * (6 * np.sin(t * 4.3 + X * 0.012))
        dx += tr * wind * gust * (9 * np.sin(t * 1.6 + Y * 0.005) + 3 * np.sin(t * 4.1 + Y * 0.03))
        dx += cl * (8 * np.sin(t * 0.5 + Y * 0.01) - 3 * t)
        dx += fl * 2.2 * np.sin(Y * 0.11 - t * 2.0)
        out = cv2.remap(self.src, (X - dx).astype(np.float32), (Y - dy).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).astype(np.float32)
        lay = np.zeros((Hh, Wc), np.float32)
        for (x, y, ln, p, sp) in self.glints:
            xx = int(x - off)
            if xx < -ln or xx > Wc:
                continue
            b = max(0.0, math.sin(t * sp + p)) ** 4
            if b > 0.05:
                y = int(y); lay[y:y + 4, max(0, xx):min(Wc, xx + ln)] = b
        out += cv2.GaussianBlur(lay, (0, 0), 2.0)[..., None] * np.array([255, 250, 230], np.float32) * 0.7
        # 천막 사이로 들어오는 햇살 띠
        band = (0.5 + 0.5 * math.sin(t * 0.8)) * 10
        rays = np.clip(np.sin((gx + off) * 0.004 - Y * 0.0025 + t * 0.15), 0, 1) ** 8 * band * (Y < 1500)
        out += rays[..., None] * np.array([1, 0.92, 0.7], np.float32)
        return np.clip(out, 0, 255).astype(np.uint8)


def petal_particles(seed=8):
    P = Particles(seed)
    cols = [(255, 196, 214), (255, 172, 200), (255, 222, 232), (246, 150, 186)]
    def petal(sz, col):
        im = Image.new("RGBA", (sz * 3, sz * 3), (0, 0, 0, 0))
        d = ImageDraw.Draw(im); w = sz * 3
        d.ellipse((w * 0.2, w * 0.3, w * 0.8, w * 0.7), fill=col + (255,), outline=(200, 110, 140, 255), width=max(2, sz // 7))
        return im.resize((sz * 2, sz * 2), Image.LANCZOS)
    P.leaf_sp = [[petal(int(s), c) for c in cols] for s in (12, 16, 20)]
    return P
