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

BG = {"sunset": cover_h(img("bg_sunset")), "night": cover_h(img("bg_night")), "market": cover_h(img2("bg_market")),
      "end": make_bg("bgp", dark=0.35, blur=6)}
LBG = {"sunset": LivingBG(BG["sunset"], "sunset", BG["night"]), "market": MarketBG(BG["market"])}
PT = Particles(3)
PETAL = petal_particles(8)
CUR_T = [0.0]

def bg_at(key, x):
    im = BG[key]
    off = int((im.width - W) * x)
    t = CUR_T[0]
    if key in LBG:
        c = Image.fromarray(LBG[key].frame(off, t)).convert("RGBA")
    else:
        c = im.crop((off, 0, off + W, H)).convert("RGBA")
    if key == "market":
        PETAL.draw(c, t, "sunset", cam=off, leaves=True, motes=True, strength=0.9)
    else:
        PT.draw(c, t, "night" if key == "end" else "sunset", cam=off, leaves=key == "sunset", motes=True, flies=key == "end")
    return c

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
W_JUMP = grade(fit_h(img2("w_jump"), 420))
W_SIT = grade(fit_h(img2("w_sit"), 400))
W_SIT_M = grade(fit_h(img2("w_sit"), 330), **MK)
W_RUN = [grade(fit_h(img2("w_run0"), 230), **MK), grade(fit_h(img2("w_run1"), 300), **MK)]
W_SCARE = grade(fit_h(img2("w_scare"), 330), **MK)
W_NUZZLE = grade(fit_h(img2("w_nuzzle"), 280), **MK)
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

# ---------- 장면 ----------
GROUND = 1700
SHAKE = []  # (시작, 길이, 세기)

def s1(t):  # 0~4.2 지난 화의 상자 → 왕년이
    lt = t
    c = bg_at("sunset", 0.38)
    gy = 1660
    shadow(c, 300, gy + 10, 340)
    stand(c, TILT if lt < 2.4 else HAPPY_S, 300, lt)
    bx = 760
    shadow(c, bx, gy + 20, 330)
    if lt < 1.8:
        sh = 10 * math.sin(lt * 24) if 0.7 < lt < 1.4 else 0
        put(c, W_BOX, bx + sh, gy - 110)
    else:
        p = (lt - 1.8) / 0.6
        if p < 1:
            put(c, W_BOX, bx, gy - 110)
            put(c, W_JUMP, bx, gy - 260 - math.sin(min(1, p) * math.pi) * 200)
        else:
            stand(c, W_SIT, bx, lt, 0.03)
    text(c, "풍년이의 모험 2화", 250, F_SM, alpha=fade(lt, 0.1, 9))
    text(c, "상자 속에 숨어 있던 건...", 430, F_CAP, alpha=fade(lt, 0.2, 1.9))
    if lt > 1.9:
        text(c, "꼬마 고양이 왕년이!", 430, F_HOOK, alpha=fade(lt, 2.0, 9), fill=(255, 236, 150))
    if lt > 2.7:
        bubble(c, "형... 혼자 있으면 무섭단 말이야", 600, 1120, 720, 1260, alpha=fade(lt, 2.7, 9, 0.2), f=F_SM)
    return c

def s2(t):  # 4.2~8.6 시장 골목을 둘이 달리기
    lt = t - 4.2
    c = bg_at("market", 0.05 + 0.1 * lt)
    cx = lerp(-260, 560, ease(lt / 1.6))
    wx = cx - 330
    shadow(c, cx, GROUND + 10, 360)
    put(c, RUN[int(lt * 14) % 8], cx, GROUND - 180 - bounce(lt, 7, 14))
    shadow(c, wx, GROUND + 10, 260)
    wr = W_RUN[int(lt * 9) % 2]
    put(c, wr, wx, GROUND - wr.height / 2 - 10 - bounce(lt, 9, 26))
    text(c, "둘이 같이 가기로 했어요", 430, F_CAP, alpha=fade(lt, 0.2, 2.1))
    text(c, "꿈길 둘째 동네,\n고소한 시장 골목", 430, F_CAP, alpha=fade(lt, 2.2, 4.4), fill=(255, 236, 150))
    return c

def s3(t):  # 8.6~12.4 생선 냄새에 멈춘 풍년이, 꼬리 끄는 왕년이
    lt = t - 8.6
    c = bg_at("market", 0.66)
    cx, wx = 470, 180
    fx, fy = 820, 1290
    steam(c, lt, fx, fy - 60)
    put(c, FISH, fx, fy + 8 * math.sin(lt * 2), rot=8 * math.sin(lt * 1.6))
    sparkles(c, lt, fx, fy, n=5, r=120, size=40, seed=12)
    shadow(c, cx, GROUND + 10, 360)
    if lt < 0.6:
        put(c, RUN[int(lt * 14) % 8], cx, GROUND - 180 - bounce(lt, 7, 14))
    else:
        b = sway(breathe(EAT, lt, 0.03, 3.0), lt, 0.02, 0.9)
        put(c, b, cx, GROUND - b.height / 2 + 15)
        # 냄새 줄기
        for i in range(3):
            p = (lt * 0.8 + i / 3) % 1
            x = lerp(fx - 60, cx + 120, p)
            y = lerp(fy, GROUND - 330, p) + 30 * math.sin(p * 9 + i)
            text_z(c, "~", x, y, 70, 1 - abs(p - 0.5) * 2)
    shadow(c, wx, GROUND + 10, 240)
    if lt < 1.6:
        put(c, W_RUN[int(lt * 9) % 2], wx, GROUND - 140 - bounce(lt, 9, 20))
    else:
        tug = math.sin(lt * 10) * 14
        put(c, W_NUZZLE, wx + tug, GROUND - W_NUZZLE.height / 2 + 12)
    text(c, "생선 냄새에\n풍년이 발이 멈췄어요", 430, F_CAP, alpha=fade(lt, 0.3, 1.9))
    if lt > 1.8:
        bubble(c, "형! 우리 호수공원 가야 돼!", 470, 1060, 260, GROUND - 290, alpha=fade(lt, 1.8, 9, 0.2), f=F_SM)
    return c

def s4(t):  # 12.4~16.8 꽥장군 등장
    lt = t - 12.4
    c = bg_at("market", 0.42 + 0.01 * lt)
    cx, wx = 330, 120
    shadow(c, cx, GROUND + 10, 360)
    if lt < 1.3:
        stand(c, DAZE, cx, lt)
    else:
        stand(c, WAVE, cx, lt)
    shadow(c, wx, GROUND + 10, 240)
    put(c, W_SCARE, wx + 4 * math.sin(lt * 40), GROUND - W_SCARE.height / 2 + 10)
    gx = lerp(1350, 800, ease(lt / 0.9))
    shadow(c, gx, GROUND + 10, 360)
    if lt < 0.9:
        put(c, GOOSE_C, gx, GROUND - GOOSE_C.height / 2 + 10 - bounce(lt, 12, 25))
    elif lt < 2.6:
        sp = GOOSE_C if int(lt * 6) % 2 else squash(GOOSE_C, 0.04)
        put(c, sp, gx, GROUND - sp.height / 2 + 10)
    else:
        b = sway(breathe(GOOSE, lt, 0.02, 1.6), lt, 0.012, 0.7)
        put(c, b, gx, GROUND - b.height / 2 + 15)
    if 0.8 < lt < 2.6:
        bubble(c, "꽥! 통행증 없인 못 지나간다!", 560, 820, 760, GROUND - 480, alpha=fade(lt, 0.9, 2.6, 0.15), f=F_SM)
    text(c, "시장 골목 문지기,\n꽥장군 등장!", 430, F_CAP, alpha=fade(lt, 0.4, 2.6), fill=(255, 236, 150))
    if lt > 2.6:
        text(c, "겁쟁이 왕년이는\n덜덜 떨고 있어요", 430, F_CAP, alpha=fade(lt, 2.7, 9))
        bubble(c, "형... 무서워...", 260, 1180, 140, GROUND - 330, alpha=fade(lt, 2.8, 9, 0.2), f=F_SM)
    return c

SHAKE.append((12.4 + 0.85, 0.45, 16))

def s5(t):  # 16.8~20.6 점프해서 머리 콩!
    lt = t - 16.8
    c = bg_at("market", 0.46)
    cx0, gx = 330, lerp(820, 700, ease(lt / 0.8))
    hit = 1.25
    shadow(c, gx, GROUND + 10, 360)
    if lt < hit:
        put(c, GOOSE_C, gx, GROUND - GOOSE_C.height / 2 + 10 - bounce(lt, 10, 18))
    else:
        q = lt - hit
        sq = squash(GOOSE, 0.12 * max(0, 1 - q / 0.25))
        put(c, sq, gx, GROUND - sq.height / 2 + 15, rot=4 * math.sin(q * 5))
        stars_round(c, q, gx - 20, GROUND - 520)
    # 풍년이 점프: 0.4~1.25 올라갔다가 머리 위로
    if lt < 0.4:
        stand(c, WAVE, cx0, lt)
        shadow(c, cx0, GROUND + 10, 360)
    elif lt < hit + 0.55:
        p = min(1, (lt - 0.4) / (hit + 0.55 - 0.4))
        x = lerp(cx0, gx - 260, p)
        y = GROUND - 200 - math.sin(p * math.pi) * 560
        shadow(c, x, GROUND + 10, 300)
        put(c, JUMP, x, y, rot=-10 * math.sin(p * math.pi))
    else:
        shadow(c, gx - 280, GROUND + 10, 360)
        stand(c, YAY, gx - 280, lt)
    pow_txt(c, "콩!", gx - 10, GROUND - 640, fade(lt, hit, hit + 1.0, 0.1))
    text(c, "풍년이가 점프해서\n머리 콩!", 430, F_CAP, alpha=fade(lt, 0.3, 3.6))
    return c

SHAKE.append((16.8 + 1.25, 0.3, 12))

def s6(t):  # 20.6~25.8 다정한 인사 → 경례, 친구
    lt = t - 20.6
    c = bg_at("market", 0.5)
    cx, gx, wx = 330, 760, 120
    shadow(c, cx, GROUND + 10, 360)
    stand(c, WAVE2 if lt < 2.6 else LOVE, cx, lt)
    shadow(c, wx, GROUND + 10, 240)
    if lt < 2.6:
        stand(c, W_SIT_M, wx, lt, 0.03)
    else:
        put(c, W_SIT_M, wx, GROUND - W_SIT_M.height / 2 + 15 - bounce(lt, 5, 26))
    shadow(c, gx, GROUND + 10, 360)
    if lt < 2.6:
        stand(c, GOOSE, gx, lt, 0.02)
    else:
        q = lt - 2.6
        # 경례: 가슴 펴고 몸을 살짝 젖힘 + 깃털 반짝
        sp = GOOSE.resize((int(GOOSE.width * 1.04), int(GOOSE.height * 1.04)))
        put(c, sp, gx, GROUND - sp.height / 2 + 15, rot=-6 * ease(q / 0.3))
        sparkles(c, q, gx, GROUND - 520, n=6, r=150, size=48, seed=44)
    if 0.4 < lt < 2.6:
        bubble(c, "수고 많으세요~", 360, 1110, 360, GROUND - 440, alpha=fade(lt, 0.4, 2.6, 0.15), f=F_SM)
    if lt > 2.7:
        bubble(c, "꽥! 통행증 발급 완료!", 640, 940, 760, GROUND - 540, alpha=fade(lt, 2.7, 9, 0.15), f=F_SM)
        for i in range(7):
            hp = ((lt - 2.7) * 0.55 + i / 7) % 1
            put(c, HEART, 540 + math.sin(i * 2.3) * 320, GROUND - 300 - hp * 650, scale=0.6 + 0.5 * hp, alpha=1 - hp)
    text(c, "풍년이의 다정한 인사 한마디", 430, F_CAP, alpha=fade(lt, 0.3, 2.6))
    text(c, "꽥장군 마음이 사르르~\n또 친구가 됐어요!", 430, F_CAP, alpha=fade(lt, 2.7, 5.2), fill=(255, 236, 150))
    return c

def s7(t):  # 25.8~27.8 셋이 같이 달려 나가기
    lt = t - 25.8
    c = bg_at("market", 0.72 + 0.1 * lt)
    cx = lerp(420, 1300, ease(lt / 2.0))
    for x, sp, b in [(cx - 600, GOOSE_C.transpose(Image.FLIP_LEFT_RIGHT), 12), (cx - 290, W_RUN[int(lt * 9) % 2], 22), (cx, RUN[int(lt * 14) % 8], 14)]:
        shadow(c, x, GROUND + 10, 300)
        put(c, sp, x, GROUND - sp.height / 2 - bounce(lt, 8, b))
    text(c, "다음 동네로 출발!", 430, F_CAP, alpha=fade(lt, 0.2, 2.0))
    return c

def s8(t):  # 27.8~30 끝 화면
    lt = t - 27.8
    c = bg_at("end", 0.5)
    put(c, sway(WAVE_END, lt, 0.015, 0.6), 540, 540, scale=1 + 0.03 * math.sin(lt * 4))
    sparkles(c, lt, 540, 560, n=8, r=220, size=50, seed=41)
    text(c, "2단계, 직접 달려 볼래요?", 860, F_CAP, alpha=fade(lt, 0.1, 9, 0.25))
    text(c, "게임 '풍년이의 모험'", 990, F_SM, alpha=fade(lt, 0.3, 9, 0.25), fill=(255, 236, 150))
    text(c, "다음 화: 지붕 위 바람, 빙글이 로봇", 1400, F_SM, alpha=fade(lt, 0.6, 9, 0.25))
    return c

def text_z(c, s, x, y, sz, a):
    a = max(0, min(1, a))
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((x, y), s, font=font(sz), fill=(255, 245, 200, int(255 * a)), stroke_width=4, stroke_fill=(58, 34, 70, int(255 * a)))
    c.alpha_composite(lay)

SCENES = [(0, 4.2, s1), (4.2, 8.6, s2), (8.6, 12.4, s3), (12.4, 16.8, s4), (16.8, 20.6, s5), (20.6, 25.8, s6), (25.8, 27.8, s7), (27.8, 30.01, s8)]
XF = 0.35
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

# ---------- 소리 ----------
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
    # 경쾌한 시장 오르골(박자 0.3초), 꽥장군 등장 때 낮은 화음, 친구 되면 밝게
    happy = [(523, 659, 784), (587, 698, 880), (523, 659, 784), (392, 494, 587)]
    tense = [(440, 523, 622), (415, 494, 587)]
    beat = 0.3; t = 0.0; k = 0
    while t < DUR - 1.0:
        if 12.4 <= t < 20.6:
            ch = tense[(k // 4) % 2]; vol = 0.09; pat = [0, 2, 0, 2]
        else:
            ch = happy[(k // 8) % 4]; vol = 0.12 if t >= 4.2 else 0.09; pat = [0, 1, 2, 1, 2, 1, 0, 2]
        note(ch[pat[k % len(pat)]], t, 0.9, vol)
        if k % 4 == 0:
            note(ch[0] / 2, t, 1.6, 0.07)
        if t >= 4.2 and not (12.4 <= t < 20.6) and k % 2 == 0:  # 통통 발소리 박자
            i0 = int(t * SR); m = int(0.06 * SR); x = np.arange(m) / SR
            out[i0:i0 + m] += 0.12 * np.sin(2 * np.pi * 140 * x) * np.exp(-x * 60)
        t += beat; k += 1
    def honk(start, vol=0.3):
        for j in range(2):
            i0 = int((start + j * 0.3) * SR); m = int(0.25 * SR); x = np.arange(m) / SR
            f = 330 + 60 * np.sin(x * 30)
            ph = 2 * np.pi * np.cumsum(f) / SR
            sq = np.sign(np.sin(ph)) * 0.6 + np.sin(ph * 2) * 0.4
            out[i0:i0 + m] += vol * sq * np.minimum(1, x * 50) * np.exp(-x * 5)
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
    pop(1.0, 0.2); pop(1.2, 0.2); pop(1.85, 0.3, 400, 1200)   # 상자 들썩 → 폴짝
    chime(2.0, 1319, 0.1)
    whoosh(12.5, 0.8, 0.25); honk(13.3); honk(15.0, 0.22)
    whoosh(17.2, 0.6, 0.22); pop(18.05, 0.5, 900, 200); chime(18.1, 1568, 0.08)  # 콩!
    chime(21.0, 784, 0.08)
    chime(23.3, 1047, 0.14); chime(23.8, 1319, 0.1); honk(23.4, 0.12)
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
