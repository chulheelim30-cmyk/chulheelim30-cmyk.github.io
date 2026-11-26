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
# ---------- 5화: 노을 다리 · 너굴 대장 ----------
SS = dict(tint=(255, 210, 160), amt=0.16, rim=(255, 175, 95), rim_a=0.7)
_b = cover_h(img2("bg_bridge"))
add_bg("bridge", _b, RegionBG(_b, 418, [
    ("water", 0, 195, 235, 300, 5), ("water", 395, 195, 746, 345, 6),
    ("sway", 0, 88, 150, 418, 16), ("sway", 428, 195, 746, 418, 14),
    ("cloud", 0, 0, 746, 128, "pink"), ("sun", 548, 138, 70),
    ("lamp", 240, 190, 30), ("lamp", 298, 185, 20), ("lamp", 323, 183, 14)]),
    kind="sunset", leaves=True, strength=0.8)
_sb = img2("s_bridge").convert("RGB")
_sb = _sb.resize((W, int(_sb.height * W / _sb.width)), Image.LANCZOS)
if _sb.height < H:
    _sb = _sb.resize((int(_sb.width * H / _sb.height), H), Image.LANCZOS)
add_bg("pic", _sb, None, kind="sunset", leaves=True, strength=0.7)
GROUND = 1800
SHAKE = []
BX = 0.36
RUN = [grade(fit_h(img(f"g_r{i}"), 380), **SS) for i in range(8)]
YAY = grade(fit_h(img("c_yay"), 430), **SS)
WAVE = grade(fit_h(img("c_wave"), 420), **SS)
WAVE2 = grade(fit_h(img("c_wave2"), 440), **SS)
LOVE = grade(fit_h(img("c_love"), 420), **SS)
DAZE = grade(fit_h(img("c_daze"), 420), **SS)
RAC = SP("b_rac", 470, side=-1, **SS)
RAC_CAN = SP("b_rac2", 440, side=-1, **SS)
W_SIT5 = SP("w_sit", 475, **SS)
W_RUN = [SP("w_run0", 322, **SS), SP("w_run1", 420, **SS)]

def s1(t):  # 0~4
    lt = t
    c = bg_at("bridge", BX - 0.05 + 0.02 * lt)
    run_pair(c, lt, lerp(-200, 640, ease(lt / 1.8)), ground=GROUND)
    text(c, "풍년이의 모험 5화", 250, F_SM, alpha=fade(lt, 0.1, 9))
    text(c, "꿈길 다섯째 동네,\n노을 다리", 440, F_HOOK, alpha=fade(lt, 0.2, 9), fill=(255, 236, 150))
    return c

def s2(t):  # 4~8.4 친구들이 모두 모인 그림
    lt = t - 4
    c = bg_at("pic", 0.5)
    z = 1 + 0.06 * (lt / 4.4)
    w2, h2 = int(W / z), int(H / z)
    c = c.crop(((W - w2) // 2, (H - h2) // 3, (W - w2) // 2 + w2, (H - h2) // 3 + h2)).resize((W, H), Image.BILINEAR)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle((0, 0, W, 330), fill=(30, 15, 40, 120))
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(30)))
    text(c, "다리 위 노을,\n친구들이 모두 모였어요", 190, F_CAP, alpha=fade(lt, 0.3, 4.2), fill=(255, 236, 150))
    return c

def s3(t):  # 8.4~12.4 절반이나 왔어!
    lt = t - 8.4
    c = bg_at("bridge", BX)
    shadow(c, 360, GROUND + 10, 360); stand(c, LOVE, 360, lt)
    shadow(c, 720, GROUND + 10, 280)
    put(c, W_SIT5, 720, GROUND - W_SIT5.height / 2 + 15 - bounce(lt, 5, 30), scale=1 + 0.04 * ease(lt / 1.5))
    bubble(c, "형, 우리 절반이나 왔어!", 640, 1180, 720, GROUND - 380, alpha=fade(lt, 0.3, 9, 0.2), f=F_SM)
    text(c, "왕년이가 처음으로\n가슴을 활짝 폈어요", 440, F_CAP, alpha=fade(lt, 0.5, 4.0))
    return c

def s4(t):  # 12.4~16.8 너굴 대장 등장
    lt = t - 12.4
    c = bg_at("bridge", BX)
    shadow(c, 300, GROUND + 10, 360); stand(c, DAZE if lt < 2.4 else WAVE2, 300, lt)
    shadow(c, 90, GROUND + 10, 260); stand(c, W_SIT5, 90, lt, 0.03)
    rx = lerp(1350, 790, ease(lt / 1.0))
    shadow(c, rx, GROUND + 10, 340)
    swag = math.sin(lt * 6) * 6 if lt > 1.0 else 0
    put(c, RAC, rx, GROUND - RAC.height / 2 + 15 - bounce(lt, 6, 10) * (lt < 1.0), rot=swag)
    text(c, "다리 지킴이,\n너굴 대장 등장!", 440, F_CAP, alpha=fade(lt, 0.3, 2.2), fill=(255, 236, 150))
    if lt > 1.0:
        bubble(c, "츄르 또 있어? 없으면 못 건너!", 560, 1090, 790, GROUND - 480, alpha=fade(lt, 1.0, 3.0, 0.15), f=F_SM)
    if lt > 3.0:
        bubble(c, "우리 츄르는 다 나눠 줬는걸...", 420, 1190, 300, GROUND - 450, alpha=fade(lt, 3.0, 9, 0.15), f=F_SM)
    return c

def s5(t):  # 16.8~21 츄르 자랑하다 쓰레기통에 쏙
    lt = t - 16.8
    c = bg_at("bridge", BX)
    shadow(c, 300, GROUND + 10, 360); stand(c, DAZE, 300, lt)
    shadow(c, 90, GROUND + 10, 260); stand(c, W_SIT5, 90, lt, 0.03)
    rx = 790
    shadow(c, rx, GROUND + 10, 340)
    if lt < 1.4:  # 츄르 흔들며 춤
        put(c, RAC, rx + 30 * math.sin(lt * 8), GROUND - RAC.height / 2 + 15 - bounce(lt, 8, 30), rot=12 * math.sin(lt * 8))
    elif lt < 1.8:
        p = (lt - 1.4) / 0.4
        put(c, RAC, rx + 60 * p, GROUND - RAC.height / 2 + 15 - math.sin(p * math.pi) * 120, rot=lerp(0, -90, p))
    else:
        q = lt - 1.8
        put(c, RAC_CAN, rx + 40, GROUND - RAC_CAN.height / 2 + 15 + 6 * math.sin(q * 25) * (q < 0.5), rot=4 * math.sin(q * 6))
        bubble(c, "으읍! 꺼내 줘~", 760, 1180, 830, GROUND - 420, alpha=fade(lt, 2.0, 9, 0.15), f=F_SM)
    pow_txt(c, "쏙!", 600, GROUND - 330, fade(lt, 1.8, 2.8, 0.1))
    text(c, "앗! 츄르 자랑하다가\n쓰레기통에 쏙!", 440, F_CAP, alpha=fade(lt, 1.6, 9))
    return c
SHAKE.append((16.8 + 1.8, 0.3, 12))

def s6(t):  # 21~26 영차 꺼내 주고 친구
    lt = t - 21
    c = bg_at("bridge", BX)
    rx = 820
    if lt < 2.2:
        tug = math.sin(lt * 12) * 12
        shadow(c, rx, GROUND + 10, 340); put(c, RAC_CAN, rx + tug * 0.5, GROUND - RAC_CAN.height / 2 + 15, rot=tug * 0.3)
        shadow(c, 520, GROUND + 10, 360); put(c, WAVE2, 520 - tug, GROUND - WAVE2.height / 2 + 15)
        shadow(c, 260, GROUND + 10, 260); put(c, W_SIT5, 260 - tug, GROUND - W_SIT5.height / 2 + 15)
        text(c, "영차! 영차!", 440, F_HOOK, alpha=fade(lt, 0.2, 2.2), fill=(255, 236, 150))
    else:
        q = lt - 2.2
        shadow(c, rx, GROUND + 10, 340)
        put(c, RAC, rx, GROUND - RAC.height / 2 + 15 - bounce(q, 5, 30) * (q > 0.3))
        shadow(c, 460, GROUND + 10, 360); stand(c, LOVE, 460, q)
        shadow(c, 200, GROUND + 10, 260); put(c, W_SIT5, 200, GROUND - W_SIT5.height / 2 + 15 - bounce(q, 5, 26))
        hearts(c, q, base=GROUND - 300)
        sparkles(c, q, rx, GROUND - 300, n=6, r=200, size=46, seed=15)
        bubble(c, "고마워! 이 츄르, 같이 먹자!", 600, 1110, rx, GROUND - 480, alpha=fade(q, 0.3, 9, 0.15), f=F_SM)
        text(c, "꺼내 주고, 나눠 먹고\n너굴 대장이랑 친구!", 440, F_CAP, alpha=fade(q, 0.2, 9), fill=(255, 236, 150))
    pow_txt(c, "뽁!", 820, GROUND - 600, fade(lt, 2.2, 3.0, 0.1))
    return c

def s7(t):  # 26~28
    lt = t - 26
    c = bg_at("bridge", BX + 0.03 * lt)
    cx = lerp(380, 1250, ease(lt / 2))
    shadow(c, cx - 650, GROUND + 10, 300); put(c, RAC, cx - 650, GROUND - RAC.height / 2 + 15 - bounce(lt, 8, 20), flip=True, scale=0.85)
    run_pair(c, lt, cx, ground=GROUND)
    text(c, "이제 강 건너 절반!", 440, F_CAP, alpha=fade(lt, 0.2, 2.0))
    return c

def s8(t):
    return end_card(t, 28, 5, "비 오는 날, 개굴 선장")

SCENES = [(0, 4, s1), (4, 8.4, s2), (8.4, 12.4, s3), (12.4, 16.8, s4), (16.8, 21, s5), (21, 26, s6), (26, 28, s7), (28, 30.01, s8)]
XF = 0.35
TENSE = [(12.4, 23.0)]
PROG = [(523, 659, 784), (440, 523, 659), (349, 440, 523), (392, 494, 587)]
BEAT = 0.36
FX = [("chime", 4.3, 1047, 0.1), ("chime", 9.0, 1319, 0.1), ("whoosh", 12.5, 0.8, 0.22), ("pop", 13.3, 0.25),
      ("whoosh", 18.2, 0.5, 0.25), ("boing", 18.6, 0.35), ("pop", 21.3, 0.15), ("pop", 21.8, 0.15), ("pop", 22.3, 0.15),
      ("pop", 23.2, 0.45, 900, 200), ("chime", 23.4, 1047, 0.14), ("chime", 23.9, 1319, 0.1)]
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
