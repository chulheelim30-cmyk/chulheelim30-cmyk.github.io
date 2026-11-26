"""풍년이의 모험 1화 쇼츠 (30초 시험본) — 게임 그림만으로 조립."""
import math, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

A = sys.argv[1]          # 그림 폴더
FONT = sys.argv[2]       # Jua 글꼴
OUT = sys.argv[3]        # 결과 mp4
W, H, FPS, DUR = 1080, 1920, 30, 30.0
N = int(FPS * DUR)

import os
X4 = "/home/claude/assets_x4"
def img(n):
    p = f"{X4}/{n}.png"
    if os.path.exists(p):
        return Image.open(p).convert("RGBA")
    return Image.open(f"{A}/{n}.webp").convert("RGBA")

def grade(sp, tint=(255, 214, 170), amt=0.18, rim=(255, 170, 90), rim_a=0.75, side=1):
    """캐릭터를 배경 빛에 맞추기: 따뜻한 색 입히기 + 해 쪽 테두리 빛"""
    rgb = np.array(sp.convert("RGB")).astype(np.float32)
    a = np.array(sp.getchannel("A")).astype(np.float32) / 255
    t = np.array(tint, np.float32)
    rgb = rgb * (1 - amt) + (rgb * t / 255) * amt * 2.2
    sh = int(max(4, sp.width * 0.025))
    shifted = np.roll(a, -side * sh, axis=1)
    edge = np.clip(a - shifted, 0, 1)
    edge = np.array(Image.fromarray((edge * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sh * 0.6))).astype(np.float32) / 255 * a
    rgb = rgb + edge[..., None] * np.array(rim, np.float32) * rim_a
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    out.putalpha(sp.getchannel("A"))
    return out

def fit_h(im, h):
    return im.resize((max(1, int(im.width * h / im.height)), int(h)), Image.LANCZOS)

def fit_w(im, w):
    return im.resize((int(w), max(1, int(im.height * w / im.width))), Image.LANCZOS)

def font(sz):
    return ImageFont.truetype(FONT, sz)

F_HOOK, F_CAP, F_SM, F_BIG = font(88), font(70), font(46), font(96)

def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)

def lerp(a, b, x):
    return a + (b - a) * x

def make_bg(name, dark=0.0, sat=1.0, blur=0):
    im = img(name).convert("RGB")
    im = im.resize((int(im.width * H / im.height), H), Image.LANCZOS)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    if sat != 1.0:
        im = ImageEnhance.Color(im).enhance(sat)
    if dark:
        im = ImageEnhance.Brightness(im).enhance(1 - dark)
    return im
def breathe(sp, t, amt=0.025, sp_hz=2.2):
    k = amt * math.sin(t * sp_hz * 2)
    return sp.resize((sp.width, max(1, int(sp.height * (1 + k)))), Image.BILINEAR)

def stand(c, sp, x, t, amt=0.025):
    b = sway(breathe(sp, t, amt), t, 0.014, 0.55, ph=x * 0.01)
    put(c, b, x, GROUND - b.height / 2 + 15)


def squash(sp, k):
    return sp.resize((max(1, int(sp.width * (1 + k))), max(1, int(sp.height * (1 - k)))), Image.BILINEAR)

def put(canvas, sp, cx, cy, scale=1.0, alpha=1.0, flip=False, rot=0):
    if flip:
        sp = sp.transpose(Image.FLIP_LEFT_RIGHT)
    if scale != 1.0:
        sp = sp.resize((max(1, int(sp.width * scale)), max(1, int(sp.height * scale))), Image.BILINEAR)
    if rot:
        sp = sp.rotate(rot, expand=True, resample=Image.BICUBIC)
    if alpha < 1.0:
        sp = sp.copy()
        sp.putalpha(sp.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)))

def shadow(canvas, cx, cy, w, a=90):
    sh = Image.new("RGBA", (int(w), int(w * 0.22)), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((0, 0, sh.width - 1, sh.height - 1), fill=(40, 20, 40, a))
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    canvas.alpha_composite(sh, (int(cx - sh.width / 2), int(cy - sh.height / 2)))

def text(canvas, s, cy, f, alpha=1.0, fill=(255, 255, 255), stroke=(58, 34, 70), sw=9):
    if alpha <= 0:
        return
    lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    lines = s.split("\n")
    lh = f.size * 1.25
    y0 = cy - lh * len(lines) / 2
    for i, ln in enumerate(lines):
        w = d.textlength(ln, font=f)
        d.text((W / 2 - w / 2, y0 + i * lh), ln, font=f, fill=fill + (255,), stroke_width=sw, stroke_fill=stroke + (255,))
    if alpha < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(lay)

def bubble(canvas, s, cx, cy, tail_x, tail_y, alpha=1.0, f=None):
    f = f or F_CAP
    lay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    tw = d.textlength(s, font=f)
    pw, ph = tw + 70, f.size + 56
    x0, y0 = cx - pw / 2, cy - ph / 2
    d.polygon([(cx - 30, cy + ph / 2 - 8), (cx + 30, cy + ph / 2 - 8), (tail_x, tail_y)], fill=(255, 255, 255, 240), outline=(58, 34, 70, 255))
    d.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), radius=40, fill=(255, 255, 255, 240), outline=(58, 34, 70, 255), width=6)
    d.text((cx - tw / 2, cy - f.size * 0.62), s, font=f, fill=(58, 34, 70, 255))
    if alpha < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * alpha)))
    canvas.alpha_composite(lay)

def fade(t, a, b, d=0.3):  # a~b 사이 보이고 앞뒤로 부드럽게
    return ease((t - a) / d) * ease((b - t) / d)

def sparkles(canvas, t, cx, cy, n=8, r=260, size=60, seed=1):
    rng = np.random.default_rng(seed)
    for i in range(n):
        ang, dist, ph = rng.uniform(0, 6.28), rng.uniform(0.3, 1) * r, rng.uniform(0, 6.28)
        tw = 0.5 + 0.5 * math.sin(t * 5 + ph)
        sp = SPARK.resize((int(size * (0.5 + tw * 0.7)),) * 2)
        put(canvas, sp, cx + math.cos(ang) * dist, cy + math.sin(ang) * dist * 0.7, alpha=0.3 + 0.7 * tw)

# ---------- 2화 배경 ----------
X4B = os.environ.get("X4B", "/tmp/w/x4ep2")
def img2(n):
    p = f"{X4B}/{n}.png"
    if os.path.exists(p):
        return Image.open(p).convert("RGBA")
    return img(n)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alive import LivingBG, Particles, MarketBG, petal_particles, sway

def cover_h(im):
    return im.convert("RGB").resize((int(im.width * H / im.height), H), Image.LANCZOS)

from alive import RegionBG
BG, LBG, PCONF = {}, {}, {}
PT = Particles(3)
PETAL = petal_particles(8)
CUR_T = [0.0]
def add_bg(key, im, living=None, **pconf):
    BG[key] = im
    if living is not None:
        LBG[key] = living
    PCONF[key] = pconf

def bg_at(key, x, dim=0.0):
    im = BG[key]
    off = int((im.width - W) * x)
    t = CUR_T[0]
    if key in LBG:
        c = Image.fromarray(LBG[key].frame(off, t)).convert("RGBA")
    else:
        c = im.crop((off, 0, off + W, H)).convert("RGBA")
    if dim:
        c.alpha_composite(Image.new("RGBA", c.size, (10, 6, 30, int(255 * dim))))
    pc = PCONF.get(key, {})
    P = PETAL if pc.get("petals") else PT
    P.draw(c, t, pc.get("kind", "sunset"), cam=off, leaves=pc.get("leaves", False) or pc.get("petals", False),
           motes=pc.get("motes", True), flies=pc.get("flies", False), strength=pc.get("strength", 1.0))
    return c

add_bg("end", make_bg("bgp", dark=0.35, blur=6), None, kind="night", flies=True)
# ---------- 2화 그림 ----------
MK = dict(tint=(255, 240, 225), amt=0.08, rim=(255, 235, 200), rim_a=0.35)  # 시장은 낮 햇살이라 약하게
RUN = [grade(fit_h(img(f"g_r{i}"), 380), **MK) for i in range(8)]
JUMP = grade(fit_h(img("g_jump"), 400), **MK)
EAT = grade(fit_h(img("c_eat"), 420), **MK)
WAVE = grade(fit_h(img("c_wave"), 420), **MK)
WAVE2 = grade(fit_h(img("c_wave2"), 440), **MK)
YAY = grade(fit_h(img("c_yay"), 430), **MK)
LOVE = grade(fit_h(img("c_love"), 420), **MK)
DAZE = grade(fit_h(img("c_daze"), 420), **MK)
TILT = grade(fit_h(img("n_cat_tilt"), 440))
HAPPY_S = grade(fit_h(img("n_cat_happy"), 420))
HAPPY_M = grade(fit_h(img("n_cat_happy"), 420), **MK)
WAVE_END = fit_h(img("c_wave"), 430)

W_BOX = grade(fit_w(img2("w_box"), 360))
W_JUMP = grade(fit_h(img2("w_jump"), 588))
W_SIT = grade(fit_h(img2("w_sit"), 560))
W_SIT_M = grade(fit_h(img2("w_sit"), 461), **MK)
W_RUN = [grade(fit_h(img2("w_run0"), 322), **MK), grade(fit_h(img2("w_run1"), 420), **MK)]
W_SCARE = grade(fit_h(img2("w_scare"), 461), **MK)
W_NUZZLE = grade(fit_h(img2("w_nuzzle"), 392), **MK)
GOOSE = grade(fit_h(img2("b_goose"), 520), side=-1, **MK)
GOOSE_C = grade(fit_h(img2("b_goose2"), 470), side=-1, **MK)
GOOSE_F = grade(fit_h(img2("o_goose"), 420), side=-1, **MK)
FISH = fit_h(img2("i_fish"), 150)
HEART = fit_h(img("o_heart"), 80)
SPARK = img("fx_s0")
F_HUGE = font(150)

def bounce(t, a, b):
    return abs(math.sin(t * a)) * b

def steam(c, t, x, y, n=4):
    """생선 굽는 김(모락모락)"""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for i in range(n):
        p = (t * 0.45 + i / n) % 1
        cx = x + 30 * math.sin(p * 6 + i) + (i - n / 2) * 22
        cy = y - p * 260
        r = 18 + p * 40
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, int(120 * (1 - p) * min(1, p * 4))))
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(8)))

def stars_round(c, t, cx, cy, r=110, n=5):
    for i in range(n):
        a = t * 4 + i * 6.28 / n
        put(c, SPARK.resize((54, 54)), cx + math.cos(a) * r, cy + math.sin(a) * r * 0.35)

def pow_txt(c, s, x, y, k):
    if k <= 0:
        return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = font(int(110 + 50 * (1 - k)))
    ImageDraw.Draw(lay).text((x, y), s, font=f, fill=(255, 232, 110, int(255 * k)), stroke_width=10, stroke_fill=(58, 34, 70, int(255 * k)), anchor="mm")
    c.alpha_composite(lay)

def text_z(c, s, x, y, sz, a):
    a = max(0, min(1, a))
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((x, y), s, font=font(sz), fill=(255, 245, 200, int(255 * a)), stroke_width=4, stroke_fill=(58, 34, 70, int(255 * a)))
    c.alpha_composite(lay)

_SC = {}
def SP(name, h, gr=True, side=1, **kw):
    """그림 불러와 높이 맞추고 빛 입히기(캐시)"""
    k = (name, h, gr, side)
    if k not in _SC:
        im = fit_h(img2(name), h)
        _SC[k] = grade(im, side=side, **(kw or MK)) if gr else im
    return _SC[k]

def end_card(t, t0, n, nxt):
    lt = t - t0
    c = bg_at("end", 0.5)
    put(c, sway(WAVE_END, lt, 0.015, 0.6), 540, 540, scale=1 + 0.03 * math.sin(lt * 4))
    sparkles(c, lt, 540, 560, n=8, r=220, size=50, seed=41)
    text(c, f"{n}단계, 직접 달려 볼래요?", 860, F_CAP, alpha=fade(lt, 0.1, 9, 0.25))
    text(c, "게임 '풍년이의 모험'", 990, F_SM, alpha=fade(lt, 0.3, 9, 0.25), fill=(255, 236, 150))
    text(c, f"다음 화: {nxt}", 1400, F_SM, alpha=fade(lt, 0.6, 9, 0.25))
    return c

def run_pair(c, lt, cx, gap=420, ground=1700, scale=1.0):
    wx = cx - gap
    shadow(c, cx, ground + 10, 360)
    put(c, RUN[int(lt * 14) % 8], cx, ground - 180 - bounce(lt, 7, 14), scale=scale)
    shadow(c, wx, ground + 10, 260)
    wr = W_RUN[int(lt * 9) % 2]
    put(c, wr, wx, ground - wr.height / 2 - 10 - bounce(lt, 9, 26), scale=scale)

def hearts(c, lt, n=7, cx=540, base=1400):
    for i in range(n):
        hp = (lt * 0.55 + i / n) % 1
        put(c, HEART, cx + math.sin(i * 2.3) * 320, base - hp * 650, scale=0.6 + 0.5 * hp, alpha=1 - hp)

# ---------- 6~10화 소품(직접 그림) ----------
def rain(c, t, k=1.0, n=140):
    if k <= 0: return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    rng = np.random.default_rng(5)
    xs, ys, sp = rng.uniform(0, W + 200, n), rng.uniform(0, H, n), rng.uniform(1800, 2600, n)
    for x, y, s in zip(xs, ys, sp):
        yy = (y + t * s) % (H + 100) - 50; xx = (x - t * s * 0.18) % (W + 200) - 100
        d.line((xx, yy, xx - 10, yy + 46), fill=(220, 235, 255, int(150 * k)), width=3)
    c.alpha_composite(lay)
    c.alpha_composite(Image.new("RGBA", (W, H), (40, 50, 80, int(50 * k))))

def snow(c, t, k=1.0, n=160):
    if k <= 0: return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    rng = np.random.default_rng(7)
    xs, ys, sz, sp = rng.uniform(0, W, n), rng.uniform(0, H, n), rng.uniform(3, 10, n), rng.uniform(60, 180, n)
    for i, (x, y, s, v) in enumerate(zip(xs, ys, sz, sp)):
        yy = (y + t * v) % H; xx = (x + 30 * math.sin(t * 0.8 + i)) % W
        d.ellipse((xx - s, yy - s, xx + s, yy + s), fill=(255, 255, 255, int(220 * k)))
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1)))

def acorn(c, x, y, s=1.0, rot=0, alpha=1.0):
    w = int(70 * s); h = int(86 * s)
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, int(h * 0.3), w + 4, h + 4), fill=(196, 120, 52), outline=(90, 50, 30), width=max(2, int(4 * s)))
    d.ellipse((2, 4, w + 6, int(h * 0.48)), fill=(120, 78, 40), outline=(80, 45, 25), width=max(2, int(4 * s)))
    d.rectangle((w // 2 - 3, 0, w // 2 + 5, 10), fill=(90, 55, 30))
    d.ellipse((int(w * 0.25), int(h * 0.5), int(w * 0.45), int(h * 0.68)), fill=(235, 170, 100))
    put(c, im, x, y, rot=rot, alpha=alpha)

def envelope(c, x, y, s=1.0, rot=0, alpha=1.0, label=None):
    w, h = int(150 * s), int(100 * s)
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w + 4, h + 4), radius=int(8 * s), fill=(255, 248, 230), outline=(110, 70, 50), width=max(2, int(4 * s)))
    d.line((4, 4, w // 2 + 4, h // 2 + 8, w + 4, 4), fill=(110, 70, 50), width=max(2, int(4 * s)))
    d.ellipse((w // 2 - 10 * s + 4, h // 2 - 2, w // 2 + 10 * s + 4, h // 2 + 18 * s), fill=(220, 60, 70))
    if label:
        f = font(max(14, int(15 * s)))
        d.text((w // 2 + 4, int(h * 0.82)), label, font=f, fill=(90, 50, 40), anchor="mm")
    put(c, im, x, y, rot=rot, alpha=alpha)

def paper_boat(c, x, y, s=1.0, rot=0):
    w, h = int(760 * s), int(300 * s)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(0, int(h * 0.45)), (w, int(h * 0.45)), (int(w * 0.82), h - 4), (int(w * 0.18), h - 4)], fill=(250, 250, 245), outline=(110, 90, 80))
    d.polygon([(int(w * 0.2), int(h * 0.45)), (int(w * 0.5), 0), (int(w * 0.8), int(h * 0.45))], fill=(235, 238, 245), outline=(110, 90, 80))
    d.line((int(w * 0.5), 0, int(w * 0.5), int(h * 0.45)), fill=(170, 170, 180), width=3)
    put(c, im, x, y, rot=rot)

def sled(c, x, y, s=1.0, rot=0):
    w, h = int(640 * s), int(120 * s)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 10, w - 60, int(h * 0.55)), radius=18, fill=(214, 60, 60), outline=(110, 30, 30), width=5)
    d.arc((w - 120, -40, w - 10, int(h * 0.9)), 270, 90, fill=(150, 110, 70), width=10)
    d.line((30, h - 14, w - 70, h - 14), fill=(150, 110, 70), width=10)
    put(c, im, x, y, rot=rot)

def snowball(c, x, y, r, rot, face=None):
    im = Image.new("RGBA", (2 * r + 8, 2 * r + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, 4, 2 * r + 4, 2 * r + 4), fill=(250, 252, 255), outline=(150, 170, 200), width=6)
    for i in range(7):
        a = i * 0.9 + rot * 0.05
        d.arc((4 + r * 0.3, 4 + r * 0.3, 2 * r - r * 0.3, 2 * r - r * 0.3), math.degrees(a), math.degrees(a) + 30, fill=(205, 220, 240), width=5)
    if face is not None:
        f = fit_w(face, int(r * 1.1)); im.alpha_composite(f, (int(r + 4 - f.width / 2), int(r + 4 - f.height / 2)))
    put(c, im, x, y, rot=rot)

def star_map(c, t, k):
    if k <= 0: return
    nodes = [(140, 300), (300, 220), (460, 330), (620, 210), (780, 320), (930, 230), (860, 470), (640, 520), (420, 560), (200, 500)]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    m = k * len(nodes)
    for i in range(len(nodes) - 1):
        if i + 1 > m: break
        (x0, y0), (x1, y1) = nodes[i], nodes[i + 1]
        q = min(1, m - i - 1 + 1e-3) if i + 1 < m else 0
        for j in range(12):
            p = j / 12
            if p > q: break
            xx, yy = lerp(x0, x1, p), lerp(y0, y1, p)
            d.ellipse((xx - 4, yy - 4, xx + 4, yy + 4), fill=(255, 240, 170, 230))
    for i, (x, y) in enumerate(nodes):
        if i < m:
            r = 16 + 5 * math.sin(t * 4 + i)
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 230, 140, 220), outline=(255, 255, 255, 255), width=3)
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.5)))
    gl = lay.filter(ImageFilter.GaussianBlur(14)); c.alpha_composite(gl)
# ---------- 9화: 눈 오는 언덕 · 눈뭉치 아저씨 ----------
EG = dict(tint=(225, 230, 255), amt=0.10, rim=(255, 225, 210), rim_a=0.4)
# ---------- 6~10화 공통 앞부분 (EG 는 각 화에서 먼저 정함) ----------
GROUND = 1720
SHAKE = []
RUN = [grade(fit_h(img(f"g_r{i}"), 380), **EG) for i in range(8)]
YAY = grade(fit_h(img("c_yay"), 430), **EG)
WAVE = grade(fit_h(img("c_wave"), 420), **EG)
WAVE2 = grade(fit_h(img("c_wave2"), 440), **EG)
LOVE = grade(fit_h(img("c_love"), 420), **EG)
DAZE = grade(fit_h(img("c_daze"), 420), **EG)
EAT = grade(fit_h(img("c_eat"), 420), **EG)
JUMP = grade(fit_h(img("g_jump"), 400), **EG)
SLEEP = grade(fit_w(img("c_sleep"), 560), **EG)
FACE = fit_w(img("face"), 230)
BELL = fit_h(img("i_bell"), 150)
def title(c, lt, n, place):
    text(c, f"풍년이의 모험 {n}화", 250, F_SM, alpha=fade(lt, 0.1, 9))
    text(c, place, 440, F_HOOK, alpha=fade(lt, 0.2, 9), fill=(255, 236, 150))
def duo(c, lt, px, wx, psp=None, wsp=None):
    psp = psp or LOVE; wsp = wsp or W_SIT_M
    shadow(c, px, GROUND + 10, 360); stand(c, psp, px, lt)
    shadow(c, wx, GROUND + 10, 300); stand(c, wsp, wx, lt, 0.03)
SNOW = SP("b_snowman", 460, side=-1, **EG)
PHEAD = DAZE.crop((0, 0, DAZE.width, int(DAZE.height * 0.52)))
SNOW2 = SP("b_snowman2", 460, side=-1, **EG)


def s1(t):
    lt = t
    c = bg_at("main", 0.1 + 0.04 * lt)
    run_pair(c, lt, lerp(-200, 640, ease(lt / 1.8)), ground=GROUND)
    snow(c, t)
    title(c, lt, 9, "꿈길 아홉째 동네,\n눈 오는 언덕")
    return c

def s2(t):  # 4~8.4 미끄러져 데굴데굴 눈뭉치
    lt = t - 4
    c = bg_at("main", 0.3 + 0.03 * lt)
    if lt < 0.8:
        shadow(c, 300, GROUND + 10, 360); put(c, DAZE, 300, GROUND - DAZE.height / 2 + 15, rot=-15 * ease(lt / 0.8))
    else:
        q = lt - 0.8
        r = int(140 + 60 * min(1, q / 2.5))
        x = lerp(300, 760, ease(q / 3.0))
        shadow(c, x, GROUND + 10, r * 2)
        snowball(c, x, GROUND - r + 10, r, rot=-q * 260, face=PHEAD)
        pow_txt(c, "데굴데굴~", 540, 1150, fade(lt, 1.0, 4.4, 0.2))
    if lt > 1.8:
        wx = lerp(-200, 260, ease((lt - 1.8) / 1.2))
        shadow(c, wx, GROUND + 10, 280)
        put(c, W_RUN[int(lt * 9) % 2], wx, GROUND - W_RUN[0].height / 2 - 10 - bounce(lt, 9, 20))
        bubble(c, "형! 기다려~!", 360, 1250, wx + 60, GROUND - 330, alpha=fade(lt, 2.2, 9, 0.15), f=F_SM)
    snow(c, t)
    text(c, "미끄러운 언덕에서\n풍년이가 눈뭉치가 됐어요!", 330, F_CAP, alpha=fade(lt, 0.4, 9))
    return c

def s3(t):  # 8.4~12.6 쿵! 눈사람과 부딪힘
    lt = t - 8.4
    c = bg_at("main", 0.45)
    sx = 860
    if lt < 1.0:
        x = lerp(500, sx - 250, ease(lt / 1.0))
        shadow(c, x, GROUND + 10, 400); snowball(c, x, GROUND - 190, 200, rot=-lt * 300, face=PHEAD)
        shadow(c, sx, GROUND + 10, 300); put(c, SNOW, sx, GROUND - SNOW.height / 2 + 15)
    else:
        q = lt - 1.0
        pow_txt(c, "펑!", sx - 220, GROUND - 600, fade(lt, 1.0, 2.0, 0.1))
        for i in range(10):
            a = i / 10 * 6.28; d = 260 * ease(min(1, q / 0.6))
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); rr = 30 - i % 3 * 6
            cx, cy = sx - 250 + math.cos(a) * d, GROUND - 200 + math.sin(a) * d * 0.6
            ImageDraw.Draw(lay).ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(255, 255, 255, int(230 * max(0, 1 - q / 1.5))))
            c.alpha_composite(lay)
        shadow(c, 300, GROUND + 10, 360); stand(c, DAZE, 300, lt)
        shadow(c, sx, GROUND + 10, 300); stand(c, SNOW2, sx, lt, 0.02)
        if q > 0.6:
            bubble(c, "아이고, 내 당근 코!", 640, 1100, sx, GROUND - 500, alpha=fade(lt, 1.6, 9, 0.15), f=F_SM)
    snow(c, t)
    text(c, "쿵! 눈사람이랑 부딪혔어요", 330, F_CAP, alpha=fade(lt, 1.1, 9), fill=(255, 236, 150))
    return c
SHAKE.append((8.4 + 1.0, 0.3, 14))

def s4(t):  # 12.6~17 외로운 눈뭉치 아저씨
    lt = t - 12.6
    c = bg_at("main", 0.5)
    duo(c, lt, 260, 560, DAZE, W_SIT_M)
    shadow(c, 880, GROUND + 10, 300); stand(c, SNOW2, 880, lt, 0.02)
    bubble(c, "추워서 아무도 놀러 안 와...", 620, 1100, 880, GROUND - 500, alpha=fade(lt, 0.4, 9, 0.15), f=F_SM)
    snow(c, t, 0.7)
    text(c, "눈뭉치 아저씨는\n혼자 외로웠대요", 330, F_CAP, alpha=fade(lt, 0.3, 4.2))
    return c

def s5(t):  # 17~21.4 코 붙여 주기
    lt = t - 17
    c = bg_at("main", 0.55)
    shadow(c, 260, GROUND + 10, 360); stand(c, WAVE, 260, lt)
    wx = lerp(540, 700, ease(lt / 1.0))
    sx = 880
    shadow(c, sx, GROUND + 10, 300)
    put(c, SNOW2 if lt < 1.6 else SNOW, sx, GROUND - SNOW.height / 2 + 15)
    shadow(c, wx, GROUND + 10, 300)
    push = max(0, math.sin((lt - 0.9) * 8)) * 14 if 0.9 < lt < 1.6 else 0
    put(c, W_SIT_M, wx + push, GROUND - W_SIT_M.height / 2 + 15)
    if lt > 1.6:
        sparkles(c, lt - 1.6, sx, GROUND - 330, n=8, r=200, size=46, seed=19)
        pow_txt(c, "꾹!", sx - 80, GROUND - 560, fade(lt, 1.5, 2.4, 0.1))
    snow(c, t, 0.7)
    text(c, "왕년이가 당근 코를\n꾹 붙여 줬어요", 330, F_CAP, alpha=fade(lt, 0.3, 4.2), fill=(255, 236, 150))
    return c

def s6(t):  # 21.4~24.4 친구
    lt = t - 21.4
    c = bg_at("main", 0.55)
    shadow(c, 260, GROUND + 10, 360); stand(c, YAY, 260, lt)
    shadow(c, 560, GROUND + 10, 300); put(c, W_SIT_M, 560, GROUND - W_SIT_M.height / 2 + 15 - bounce(lt, 5, 24))
    shadow(c, 880, GROUND + 10, 300); stand(c, SNOW, 880, lt, 0.03)
    hearts(c, lt, base=GROUND - 300)
    bubble(c, "고마워! 같이 눈썰매 타자!", 620, 1100, 880, GROUND - 500, alpha=fade(lt, 0.4, 9, 0.15), f=F_SM)
    snow(c, t, 0.7)
    text(c, "눈뭉치 아저씨랑 친구!", 330, F_CAP, alpha=fade(lt, 0.3, 9), fill=(255, 236, 150))
    return c

def s7(t):  # 24.4~28 눈썰매 쌩
    lt = t - 24.4
    c = bg_at("main", 0.5 + 0.12 * lt)
    p = ease(lt / 3.4)
    x = lerp(-300, 1350, p); y = lerp(GROUND - 260, GROUND - 40, p)
    put(c, W_SIT_M, x - 170, y - 150, scale=0.62, rot=-8)
    put(c, YAY, x + 110, y - 165, scale=0.62, rot=-8)
    sled(c, x, y, 1.0, rot=-8)
    for i in range(6):
        q = (lt * 2 + i / 6) % 1
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); rr = 18 + q * 30
        cx, cy = x - 320 - q * 160, y + 40 - q * 40
        ImageDraw.Draw(lay).ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(255, 255, 255, int(200 * (1 - q))))
        c.alpha_composite(lay)
    shadow(c, 880, GROUND + 10, 300); put(c, SNOW, 880, GROUND - SNOW.height / 2 + 15, scale=0.8)
    snow(c, t)
    text(c, "눈썰매 타고 쌩~\n다음 동네로!", 330, F_CAP, alpha=fade(lt, 0.3, 3.6))
    return c

def s8(t):
    return end_card(t, 28, 9, "달빛 구름길, 달토끼")

SCENES = [(0, 4, s1), (4, 8.4, s2), (8.4, 12.6, s3), (12.6, 17, s4), (17, 21.4, s5), (21.4, 24.4, s6), (24.4, 28, s7), (28, 30.01, s8)]
XF = 0.35
TENSE = [(4.0, 10.0)]
PROG = [(392, 494, 587), (330, 415, 494), (349, 440, 523), (392, 494, 587)]
BEAT = 0.40
FX = [("whoosh", 4.8, 1.2, 0.18), ("boing", 9.4, 0.4), ("pop", 9.5, 0.35), ("pop", 18.5, 0.3), ("chime", 18.6, 1568, 0.12),
      ("chime", 21.6, 1047, 0.13), ("chime", 22.1, 1319, 0.1), ("whoosh", 24.6, 2.4, 0.22)]

# ---------- 새 배경(11-26 사용자 그림 13장)으로 바꾸기: 장면 파일 뒤에 붙임 ----------
import os as _os
from PIL import ImageFilter as _IF, ImageEnhance as _IE
from alive import RegionBG as _RBG, Particles as _Pt, petal_particles as _pp
NB_DIR = "/tmp/w/nbg"
NB_EP = int(_os.environ.get("NB_EP", "1"))

def _cover(im):
    im = im.convert("RGB")
    im = im.resize((int(im.width * H / im.height), H), Image.LANCZOS)
    return im.filter(_IF.UnsharpMask(radius=2, percent=70, threshold=2))

_PARK_C = [("cloud", 0, 0, 832, 470, "pink")]
_MK_C = [("cloud", 0, 0, 832, 260, "pink")]
_RF_C = [("cloud", 0, 0, 832, 360, "pink")]
NB_REG = {
    "park_0": _PARK_C + [("hang", 0, 0, 320, 680, 9), ("hang", 560, 0, 832, 520, 9), ("water", 150, 560, 832, 800, 6),
                         ("sun", 590, 520, 50), ("lamp", 150, 370, 26)],
    "park_1": _PARK_C + [("hang", 0, 0, 320, 680, 9), ("hang", 560, 0, 832, 520, 9), ("water", 150, 570, 832, 800, 6),
                         ("sun", 615, 540, 50), ("lamp", 140, 380, 26)],
    "park_2": _PARK_C + [("hang", 0, 0, 300, 720, 9), ("hang", 560, 150, 832, 660, 9), ("water", 100, 650, 832, 900, 6),
                         ("sun", 343, 632, 55), ("lamp", 160, 370, 28)],
    "park_3": _PARK_C + [("hang", 0, 0, 260, 700, 9), ("water", 200, 600, 832, 860, 6),
                         ("sun", 335, 572, 50), ("lamp", 700, 477, 22)],
    "park_4": _PARK_C + [("hang", 0, 0, 300, 700, 9), ("hang", 600, 200, 832, 650, 8), ("water", 200, 545, 832, 800, 6),
                         ("sun", 307, 509, 45), ("lamp", 95, 498, 22)],
    "market_1": _MK_C + [("hang", 0, 420, 280, 560, 4), ("hang", 540, 410, 832, 560, 4), ("water", 0, 930, 832, 1248, 3),
                         ("lamp", 770, 195, 26), ("lamp", 595, 283, 18), ("lamp", 165, 300, 18)],
    "market_2": _MK_C + [("hang", 0, 490, 330, 640, 4), ("hang", 500, 520, 832, 680, 4), ("water", 0, 960, 832, 1248, 3),
                         ("lamp", 37, 683, 22), ("lamp", 765, 722, 22), ("lamp", 535, 673, 16)],
    "market_3": _MK_C + [("hang", 0, 420, 300, 560, 4), ("hang", 520, 400, 832, 560, 4), ("water", 0, 900, 832, 1248, 3),
                         ("lamp", 25, 576, 22), ("lamp", 787, 576, 22), ("lamp", 600, 273, 16)],
    "market_4": _MK_C + [("hang", 0, 470, 300, 620, 4), ("hang", 520, 460, 832, 620, 4), ("water", 0, 950, 832, 1248, 3),
                         ("lamp", 648, 293, 18)],
    "roof_1": _RF_C + [("hang", 470, 420, 720, 570, 10), ("sun", 322, 420, 40), ("sway", 580, 760, 800, 980, 7), ("sway", 0, 480, 140, 820, 7)],
    "roof_2": _RF_C + [("hang", 500, 390, 790, 490, 10), ("sun", 135, 470, 40), ("sway", 0, 850, 280, 1010, 6), ("sway", 720, 450, 832, 800, 7)],
    "roof_3": _RF_C + [("hang", 55, 450, 290, 570, 10), ("sun", 172, 420, 35), ("sway", 580, 780, 760, 990, 6)],
    "roof_4": _RF_C + [("hang", 510, 410, 765, 570, 10), ("sun", 453, 498, 35), ("sway", 0, 620, 160, 780, 6), ("sway", 540, 950, 700, 1060, 6)],
    "ep4": [("hang", 0, 0, 200, 700, 8), ("hang", 650, 0, 832, 500, 7), ("water", 150, 600, 832, 880, 5), ("sun", 640, 215, 40)],
    "ep5": [("hang", 0, 0, 330, 350, 6), ("water", 0, 450, 832, 760, 5), ("sun", 420, 330, 50), ("lamp", 340, 620, 18), ("lamp", 660, 640, 20),
            ("cloud", 0, 0, 832, 330, "pink")],
    "ep6": [("cloud", 0, 0, 832, 450, "white"), ("sway", 0, 250, 250, 800, 8), ("water", 150, 650, 832, 950, 5)],
    "ep7": [("hang", 0, 0, 832, 480, 5), ("sun", 420, 450, 60)],
    "ep8": [("sway", 580, 250, 832, 800, 5), ("sway", 0, 300, 250, 700, 5), ("lamp", 690, 420, 18), ("cloud", 0, 0, 832, 250, "white")],
    "ep9": [("cloud", 0, 0, 832, 400, "pink"), ("sun", 650, 450, 35), ("lamp", 60, 700, 18), ("lamp", 560, 720, 14)],
    "ep10": [("cloud", 0, 0, 832, 520, "pink"), ("sun", 620, 300, 70), ("water", 300, 620, 700, 1000, 2)],
}
NB_NIGHT = {"ep4", "ep10"}
NB_PK = {"ep4": ("night", False, True, 0.8), "ep5": ("sunset", True, False, 0.8), "ep6": ("sunset", False, False, 0.6),
         "ep7": ("sunset", True, False, 1.1), "ep8": ("petal", True, False, 0.7), "ep9": ("night", False, False, 0.5),
         "ep10": ("night", False, True, 0.9)}
_NB_IM, _NB_L = {}, {}
def _nb_get(name):
    if name not in _NB_L:
        base, _, mod = name.partition(":")
        im = _cover(Image.open(f"{NB_DIR}/bg_{base}.jpg"))
        night = base in NB_NIGHT
        if mod == "night":
            a = np.array(im).astype(np.float32)
            a = a * 0.42 + np.array([10, 14, 45], np.float32)
            a[..., 2] *= 1.25
            im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); night = True
        elif mod == "sad":
            im = _IE.Brightness(_IE.Color(im).enhance(0.6)).enhance(0.68)
        elif mod == "end":
            im = _IE.Brightness(im.filter(_IF.GaussianBlur(8))).enhance(0.62)
        _NB_IM[name] = im
        _NB_L[name] = None if mod == "end" else _RBG(im, 1248, NB_REG[base], night=night)
    return _NB_IM[name], _NB_L[name]

# (시작, 끝, 원래 key, 새 그림) — 위에서부터 먼저 맞는 것
NB_MAP = {
    1: [(0, 99, "night", "park_4:night"), (0, 99, "sunset_sad", "park_3:sad"), (0, 99, "end", "park_2:end"),
        (0, 8.6, "sunset", "park_1"), (8.6, 14.4, "sunset", "park_0"), (14.4, 24.6, "sunset", "park_4"), (24.6, 99, "sunset", "park_2")],
    2: [(0, 99, "sunset", "park_2"), (0, 99, "end", "market_2:end"), (0, 99, "night", "park_4:night"),
        (0, 8.6, "market", "market_2"), (8.6, 12.4, "market", "market_1"), (12.4, 20.6, "market", "market_3"),
        (20.6, 25.8, "market", "market_4"), (25.8, 99, "market", "market_2")],
    4: [(0, 99, "night", "ep4"), (0, 99, "end", "ep4:end")],
    5: [(0, 99, "bridge", "ep5"), (0, 99, "pic", "ep5"), (0, 99, "end", "ep5:end")],
    6: [(0, 99, "main", "ep6"), (0, 99, "end", "ep6:end")],
    7: [(0, 99, "main", "ep7"), (0, 99, "end", "ep7:end")],
    8: [(0, 99, "main", "ep8"), (0, 99, "end", "ep8:end")],
    9: [(0, 99, "main", "ep9"), (0, 99, "end", "ep9:end")],
    10: [(0, 99, "main", "ep10"), (0, 99, "end", "ep10:end")],
    3: [(0, 99, "end", "roof_2:end"), (0, 4, "roof", "roof_2"), (4, 12.6, "roof", "roof_1"), (12.6, 17, "roof", "roof_4"),
        (17, 21, "roof", "roof_3"), (21, 26, "roof", "roof_4"), (26, 99, "roof", "roof_2")],
}
_NB_PT = _Pt(3); _NB_PETAL = _pp(8)
_old_bg_at = bg_at
def bg_at(key, x, dim=0.0, *a, **k):
    t = CUR_T[0]
    nm = None
    for (t0, t1, kk, nn) in NB_MAP[NB_EP]:
        if kk == key and t0 <= t < t1:
            nm = nn; break
    if nm is None:
        return _old_bg_at(key, x, *([dim] if dim else []))
    im, L = _nb_get(nm)
    x = max(0.0, min(1.0, x))
    off = int((im.width - W) * x)
    if L is not None:
        c = Image.fromarray(L.frame(off, t, wind=0.7 if nm.endswith(":sad") else 1.0)).convert("RGBA")
    else:
        c = im.crop((off, 0, off + W, H)).convert("RGBA")
    if dim:
        c.alpha_composite(Image.new("RGBA", c.size, (10, 6, 30, int(255 * dim))))
    base = nm.split(":")[0]
    if nm.endswith(":night") or nm.endswith(":end"):
        _NB_PT.draw(c, t, "night", cam=off, leaves=False, motes=True, flies=True, strength=0.8)
    elif base in NB_PK:
        kd, lv, fl, st = NB_PK[base]
        if kd == "petal":
            _NB_PETAL.draw(c, t, "sunset", cam=off, leaves=True, motes=True, strength=st)
        else:
            _NB_PT.draw(c, t, kd, cam=off, leaves=lv, motes=True, flies=fl, strength=st)
    elif base.startswith("park"):
        _NB_PT.draw(c, t, "sunset", cam=off, leaves=True, motes=True, strength=0.6 if nm.endswith(":sad") else 0.9)
    elif base.startswith("market"):
        _NB_PT.draw(c, t, "sunset", cam=off, leaves=False, motes=True, strength=0.8)
    else:
        _NB_PETAL.draw(c, t, "sunset", cam=off, leaves=True, motes=True, strength=0.5)
    return c

GROUND = {3: 1600, 4: 1740, 5: 1720}.get(NB_EP, GROUND)

# ---------- 새 왕년이 그림(11-26 12포즈 시트) ----------
from PIL import ImageOps as _IO
_WN = "/tmp/w/x4w"
def _w(n, flip=False):
    p = f"{_WN}/{n}.png"
    if not os.path.exists(p): p = f"/tmp/w/wnew/{n}.png"
    im = Image.open(p).convert("RGBA")
    return _IO.mirror(im) if flip else im
_G = dict(globals().get("MK", {}) or dict(tint=(255, 214, 170), amt=0.12))
_G["rim_a"] = 0.12
_D = dict(globals().get("DAY") or globals().get("NT") or globals().get("SS") or globals().get("EG") or _G); _D["rim_a"] = 0.1
W_BOX = grade(fit_w(_w("w_box"), 400), **_G)
BOX = grade(fit_w(_w("w_box"), 380), **_G)
W_JUMP = grade(fit_h(_w("w_run1"), 430), **_G)
W_SIT = grade(fit_h(_w("w_sit"), 540), **_G)
W_SIT_M = grade(fit_h(_w("w_sit"), 470), **_G)
W_RUN = [grade(fit_h(_w("w_run0"), 350), **_G), grade(fit_h(_w("w_run1"), 370), **_G)]
W_SCARE = grade(fit_h(_w("w_scare"), 470), **_D)
W_NUZZLE = grade(fit_h(_w("w_walk", True), 430), **_G)
W_JUMP3 = grade(fit_h(_w("w_run1"), 420), **_D)
W_SIT3 = grade(fit_h(_w("w_sit"), 470), **_D)
W_SIT4 = W_SIT5 = grade(fit_h(_w("w_sit"), 470), **_D)
W_SCARE4 = grade(fit_h(_w("w_scare"), 470), **_D)
W_NUZ = grade(fit_h(_w("w_walk"), 400), **_D)
if any(k in globals() for k in ("NT", "SS", "EG")):
    W_RUN = [grade(fit_h(_w("w_run0"), 350), **_D), grade(fit_h(_w("w_run1"), 370), **_D)]
W_CHURU = grade(fit_h(_w("w_churu"), 470), **_D)
W_GROOM = grade(fit_h(_w("w_groom"), 450), **_D)
W_WALK = grade(fit_h(_w("w_walk"), 430), **_D)
W_BELLY = grade(fit_w(_w("w_sleep"), 520), **_D)
W_LIE = grade(fit_w(_w("w_lie"), 520), **_D)
W_SCRATCH = grade(fit_h(_w("w_scratch"), 480), **_D)
W_LEAP = grade(fit_h(_w("w_run1"), 400), **_D)
VIG = None
def post(im, t):
    global VIG
    if VIG is None:
        yy, xx = np.mgrid[0:H, 0:W]
        d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2)
        VIG = np.clip(1 - (d - 0.55) * 0.9, 0.55, 1)[..., None].astype(np.float32)
    # 카메라: 장면마다 천천히 다가가기 + 까마귀 순간 흔들림
    z = 1.0
    for a, b, fn in SCENES:
        if a <= t < b:
            z = 1.0 + 0.05 * ((t - a) / (b - a))
    sx = sy = 0
    for (a0, d0, amp) in SHAKE:
        if a0 <= t < a0 + d0:
            k = 1 - (t - a0) / d0
            sx, sy = int(amp * k * math.sin(t * 90)), int(amp * 0.7 * k * math.cos(t * 70))
    if z != 1.0 or sx or sy:
        w2, h2 = int(W / z), int(H / z)
        x0, y0 = (W - w2) // 2 + sx, (H - h2) // 2 + sy
        im = im.crop((x0, y0, x0 + w2, y0 + h2)).resize((W, H), Image.BILINEAR)
    rgb = im.convert("RGB")
    # 빛 번짐
    small = rgb.resize((W // 4, H // 4), Image.BILINEAR)
    br = np.array(small).astype(np.float32)
    br = np.clip(br - 170, 0, 255) * 1.4
    glow = Image.fromarray(br.astype(np.uint8)).filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR)
    arr = np.array(rgb).astype(np.float32) + np.array(glow).astype(np.float32) * 0.45
    arr *= VIG
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

def frame(t):
    CUR_T[0] = t
    return post(frame_raw(t), t)

def frame_raw(t):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= t < b:
            cur = fn(t)
            if i > 0 and t - a < XF:
                prev = SCENES[i - 1][2](t)
                cur = Image.blend(prev, cur, ease((t - a) / XF))
            return cur
    return SCENES[-1][2](t)

# ---------- 소리(화마다 TENSE·FX만 바꿈) ----------
SR = 44100
def synth_audio(path):
    n = int(SR * DUR); out = np.zeros(n); tt = np.arange(n) / SR
    rng = np.random.default_rng(0)
    def note(f, start, dur, vol, dec=4.5):
        i0, i1 = int(start * SR), min(n, int((start + dur) * SR))
        if i0 >= n: return
        x = tt[: i1 - i0]
        env = np.exp(-x * dec) * np.minimum(1, x * 200)
        out[i0:i1] += vol * env * (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * 2 * f * x) * np.exp(-x * 8))
    prog = PROG
    tense = [(440, 523, 622), (415, 494, 587)]
    beat = BEAT; t = 0.0; k = 0
    while t < DUR - 1.0:
        ten = any(a <= t < b for a, b in TENSE)
        if ten:
            ch = tense[(k // 4) % 2]; vol = 0.09; pat = [0, 2, 0, 2]
        else:
            ch = prog[(k // 8) % len(prog)]; vol = 0.11; pat = [0, 1, 2, 1, 2, 1, 0, 2]
        note(ch[pat[k % len(pat)]], t, 0.9, vol)
        if k % 4 == 0:
            note(ch[0] / 2, t, 1.6, 0.07)
        t += beat; k += 1
    def chime(start, base=1047, vol=0.12):
        for j, mult in enumerate([1, 1.25, 1.5, 2]):
            note(base * mult, start + j * 0.07, 0.9, vol)
    def pop(start, vol=0.35, f0=300, f1=900):
        i0 = int(start * SR); m = int(0.14 * SR); x = np.arange(m) / SR
        out[i0:i0 + m] += vol * np.sin(2 * np.pi * (f0 + (f1 - f0) * x / 0.14) * x) * np.exp(-x * 25)
    def whoosh(start, dur=0.5, vol=0.2):
        i0 = int(start * SR); m = int(dur * SR)
        nz = np.convolve(rng.normal(0, 1, m), np.ones(30) / 30, mode="same")
        out[i0:i0 + m] += vol * nz * np.sin(np.linspace(0, np.pi, m)) ** 2
    def beep(start, vol=0.15):
        for j, f in enumerate([1320, 990, 1320]):
            i0 = int((start + j * 0.11) * SR); m = int(0.08 * SR); x = np.arange(m) / SR
            out[i0:i0 + m] += vol * np.sign(np.sin(2 * np.pi * f * x)) * np.exp(-x * 20)
    def hoot(start, vol=0.25):
        for j in range(2):
            i0 = int((start + j * 0.45) * SR); m = int(0.35 * SR); x = np.arange(m) / SR
            f = 380 - 40 * x / 0.35
            out[i0:i0 + m] += vol * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * x / 0.35)
    def boing(start, vol=0.3):
        i0 = int(start * SR); m = int(0.4 * SR); x = np.arange(m) / SR
        out[i0:i0 + m] += vol * np.sin(2 * np.pi * (200 + 150 * np.sin(x * 40)) * x) * np.exp(-x * 7)
    def wind(start, dur=2.0, vol=0.12):
        i0 = int(start * SR); m = min(int(dur * SR), n - i0)
        nz = np.convolve(rng.normal(0, 1, m), np.ones(80) / 80, mode="same")
        out[i0:i0 + m] += vol * nz * 6 * np.sin(np.linspace(0, np.pi, m)) * (0.6 + 0.4 * np.sin(np.linspace(0, 9, m)))
    F = dict(chime=chime, pop=pop, whoosh=whoosh, beep=beep, hoot=hoot, boing=boing, wind=wind)
    for fx in FX:
        F[fx[0]](*fx[1:])
    out[: int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    out[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))
    out = np.clip(out / max(1e-6, np.abs(out).max()) * 0.8, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
if __name__ == "__main__":
    wav = OUT.replace(".mp4", ".wav")
    synth_audio(wav)
    if len(sys.argv) > 4:  # 미리보기 프레임만
        for ts in sys.argv[4].split(","):
            frame(float(ts)).convert("RGB").save(OUT.replace(".mp4", f"_{ts}.jpg"), quality=85)
        sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    for i in range(N):
        p.stdin.write(frame(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    print("done", OUT)
