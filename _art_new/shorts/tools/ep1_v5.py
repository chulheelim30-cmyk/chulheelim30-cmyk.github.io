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

# ---------- 배경 (세로로 꽉 채우고 옆으로 흐르기) ----------
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

BG = {
    "night": make_bg("bg_night", dark=0.35),
    "sunset": make_bg("bg_sunset"),
    "sunset_sad": make_bg("bg_sunset", dark=0.4, sat=0.55),
    "end": make_bg("bgp", dark=0.35, blur=6),
}

CUR_T = [0.0]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from alive import LivingBG, Particles, sway
_NIGHT_REF = BG["night"]
LBG = {"sunset": LivingBG(BG["sunset"], "sunset", _NIGHT_REF),
       "sunset_sad": LivingBG(BG["sunset_sad"], "sunset", _NIGHT_REF),
       "night": LivingBG(BG["night"], "night", _NIGHT_REF)}
PT = Particles(3)
def bg_at(key, x):  # x: 0(왼쪽)~1(오른쪽)
    im = BG[key]
    off = int((im.width - W) * x)
    t = CUR_T[0]
    if key in LBG:
        c = Image.fromarray(LBG[key].frame(off, t, wind=0.7 if key == "sunset_sad" else 1.0)).convert("RGBA")
    else:
        c = im.crop((off, 0, off + W, H)).convert("RGBA")
    kind = "night" if key in ("night", "end") else "sunset"
    PT.draw(c, t, kind, cam=off, leaves=key in ("sunset", "sunset_sad"), motes=True, flies=key in ("night", "end"),
            strength=0.6 if key == "sunset_sad" else 1.0)
    return c

# ---------- 그림 ----------
RUN = [grade(fit_h(img(f"g_r{i}"), 400)) for i in range(8)]
SLEEP = grade(fit_w(img("c_sleep"), 640), tint=(170, 180, 255), amt=0.15, rim=(255, 220, 150), rim_a=0.5)
DAZE = grade(fit_h(img("c_daze"), 430))
WAVE = grade(fit_h(img("c_wave"), 430))
WAVE_END = fit_h(img("c_wave"), 430)
LOVE = grade(fit_h(img("c_love"), 430))
YAY = grade(fit_h(img("c_yay"), 430))
CROW = grade(fit_h(img("b_crow"), 380), side=-1)
CROW_SM = grade(fit_h(img("b_crow"), 300), side=-1)
BELL = fit_h(img("i_bell"), 120)
CHURU = fit_h(img("i_churu"), 150)
HEART = fit_h(img("o_heart"), 80)
SPARK = img("fx_s0")
BOX = grade(fit_w(img("w_box"), 330))
CROW_F = grade(fit_h(img("o_crow"), 380), side=-1)
JUMP = grade(fit_h(img("g_jump"), 400))
HURT = grade(fit_h(img("hurt"), 400))
EAT = grade(fit_h(img("c_eat"), 430))
WAVE2 = grade(fit_h(img("c_wave2"), 450))

N_CROW_BELL = grade(fit_h(img("n_crow_bell"), 400), side=-1)
N_CROW_SAD = grade(fit_h(img("n_crow_sad"), 330), side=-1)
N_CROW_SAD_L = grade(fit_h(img("n_crow_sad"), 430), side=-1)
N_CROW_EAT = grade(fit_h(img("n_crow_eat"), 320), side=-1)
N_CROW_HEART = grade(fit_h(img("n_crow_heart"), 340), side=-1)
N_CAT_JUMP = grade(fit_h(img("n_cat_jump"), 440))
N_CAT_GIVE = grade(fit_h(img("n_cat_give"), 430))
N_CAT_TILT = grade(fit_h(img("n_cat_tilt"), 450))
N_CAT_HAPPY = grade(fit_h(img("n_cat_happy"), 430))

def breathe(sp, t, amt=0.025, sp_hz=2.2):
    k = amt * math.sin(t * sp_hz * 2)
    return sp.resize((sp.width, max(1, int(sp.height * (1 + k)))), Image.BILINEAR)

def stand(c, sp, x, t, amt=0.025):
    b = sway(breathe(sp, t, amt), t, 0.014, 0.55, ph=x * 0.01)
    put(c, b, x, GROUND - b.height / 2 + 15)

def flap(t, hz=7):
    return CROW if int(t * hz) % 2 else CROW_F

def squash(sp, k):
    return sp.resize((max(1, int(sp.width * (1 + k))), max(1, int(sp.height * (1 - k)))), Image.BILINEAR)
FACE = fit_w(img("face"), 230)

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

# ---------- 장면 ----------
GROUND = 1660

def s1(t):  # 0~3.6 잠드는 풍년이
    c = bg_at("night", 0.5 + 0.02 * t)
    sparkles(c, t, 540, 500, n=10, r=480, size=46, seed=3)
    br = 1 + 0.035 * math.sin(t * 2.6)
    sp = SLEEP.resize((SLEEP.width, int(SLEEP.height * br)))
    shadow(c, 540, 1180, 560)
    put(c, sp, 540, 1130 - sp.height / 2 + 60)
    for i in range(3):  # Z z z
        p = (t * 0.6 + i / 3) % 1
        lay_y = 900 - p * 220
        text_z(c, "Z" if i == 0 else "z", 760 + p * 90 + i * 30, lay_y - i * 40, 60 - i * 12, (1 - p))
    text(c, "풍년이의 모험 1화", 250, F_SM, alpha=fade(t, 0.1, 9))
    text(c, "풍년이는\n자면 꼭 같은 꿈을 꿔요", 430, F_HOOK, alpha=fade(t, 0.15, 9))
    return c

def text_z(c, s, x, y, sz, a):
    lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((x, y), s, font=font(sz), fill=(255, 245, 200, int(255 * max(0, min(1, a)))), stroke_width=4, stroke_fill=(58, 34, 70, int(255 * max(0, min(1, a)))))
    c.alpha_composite(lay)

def run_frame(t):
    return RUN[int(t * 14) % 8]

def s2(t):  # 3.6~8.6 노을 공원 달리기 + 황금 방울
    lt = t - 3.6
    c = bg_at("sunset", 0.1 + 0.08 * lt)
    cx = lerp(-260, 470, ease(lt / 1.6))
    bob = abs(math.sin(lt * 7)) * 14
    shadow(c, cx, GROUND + 10, 380)
    if 1.6 < lt < 2.3:
        p = (lt - 1.6) / 0.7
        put(c, JUMP, cx, GROUND - 200 - math.sin(p * math.pi) * 170)
    elif 2.3 <= lt < 2.5:
        sq = squash(run_frame(lt), 0.12 * (1 - (lt - 2.3) / 0.2))
        put(c, sq, cx, GROUND - sq.height / 2 + 10)
    else:
        put(c, run_frame(lt), cx, GROUND - 190 - bob)
    sparkles(c, lt, cx - 220, GROUND - 120, n=6, r=120, size=44, seed=int(lt * 4) % 5 + 7)
    text(c, "꿈길 첫 동네, 노을 공원", 430, F_CAP, alpha=fade(lt, 0.3, 3.0))
    return c

def s3(t):  # 8.6~13.4 까마귀 등장, 방울 뺏기
    lt = t - 8.6
    c = bg_at("sunset", 0.5 + 0.03 * lt)
    cat_x = 470
    grab = 0.9
    shadow(c, cat_x, GROUND + 10, 380)
    if lt < grab:
        put(c, run_frame(lt), cat_x, GROUND - 190 - abs(math.sin(lt * 7)) * 14)
    elif lt < grab + 0.55:
        p = (lt - grab) / 0.55
        put(c, HURT, cat_x - 60 * p, GROUND - 200 - math.sin(p * math.pi) * 150)
    elif lt < grab + 0.75:
        sq = squash(DAZE, 0.14 * (1 - (lt - grab - 0.55) / 0.2))
        put(c, sq, cat_x - 80, GROUND - sq.height / 2 + 10)
    else:
        put(c, DAZE, cat_x - 80, GROUND - 205)
    # 까마귀 경로: 오른쪽 위 → 방울 → 오른쪽 위
    bell_home = (cat_x + 210, GROUND - 400)
    if lt < grab:
        p = ease(lt / grab)
        crx, cry = lerp(1250, bell_home[0] + 60, p), lerp(250, bell_home[1] - 120, p)
        put(c, BELL, *bell_home)
    else:
        p = ease((lt - grab) / 1.1)
        crx, cry = lerp(bell_home[0] + 60, 800, p), lerp(bell_home[1] - 120, 760, p)
        cry += 15 * math.sin(lt * 6)
        put(c, BELL, crx - 70, cry + 150, rot=10 * math.sin(lt * 8))
    put(c, flap(lt, 9 if lt < grab else 7), crx, cry, flip=True, rot=-8 if lt < grab else 6 * math.sin(lt * 5))
    if lt > 2.1:
        bubble(c, "까악! 이건 내 거야!", 640, 420, 760, 560, alpha=fade(lt, 2.1, 4.8, 0.2))
    if lt > 2.9:
        bubble(c, "어어, 내 방울!", 330, GROUND - 600, 430, GROUND - 470, alpha=fade(lt, 2.9, 4.8, 0.2), f=F_SM)
    return c

CLIP_T0 = 6.4
CLIP_N = len(os.listdir("/home/claude/canva/frames"))
def sclip(t):  # 6.4~14.4 Canva로 만든 장면
    lt = t - CLIP_T0
    i = min(CLIP_N, max(1, int(lt * 30) + 1))
    c = Image.open(f"/home/claude/canva/frames/{i:04d}.jpg").convert("RGBA")
    PT.draw(c, t, "sunset", cam=0, leaves=True, motes=True, strength=0.8)
    text(c, "풍년이의 보물, 황금 방울!", 430, F_CAP, alpha=fade(lt, 0.3, 2.8))
    if lt > 4.0:
        bubble(c, "까악! 이건 내 거야!", 470, 215, 600, 330, alpha=fade(lt, 4.0, 5.9, 0.2))
    if lt > 6.1:
        text(c, "어어... 내 방울!", 1500, F_CAP, alpha=fade(lt, 6.1, 8.2, 0.2))
    return c

def s4(t):  # 14.4~18.8 혼자인 까마귀
    lt = t - 14.4
    c = bg_at("sunset_sad", 0.75)
    z = 1 + 0.06 * ease(lt / 5)
    vign = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(vign).ellipse((-300, 300, W + 300, H - 200), fill=(0, 0, 0, 0))
    shadow(c, 560, 1180, 330)
    put(c, CROW, 560, 1050, scale=z, rot=2 * math.sin(lt * 1.5))
    put(c, BELL, 700, 1130, scale=z)
    sparkles(c, lt, 560, 1060, n=9, r=300, size=54, seed=21)
    text(c, "반짝이는 걸 잔뜩 모았지만...", 430, F_CAP, alpha=fade(lt, 0.3, 2.1))
    text(c, "보여 줄 친구가\n하나도 없었대요", 450, F_CAP, alpha=fade(lt, 2.2, 4.6))
    return c

def s5(t):  # 18.8~24.6 츄르 나눠 주고 친구
    lt = t - 18.8
    c = bg_at("sunset", 0.62)
    cat_x, crow_x = 330, 780
    shadow(c, cat_x, GROUND + 10, 340)
    shadow(c, crow_x, GROUND - 20, 260)
    friend = lt > 2.9
    if lt < 1.0:
        put(c, EAT, cat_x, GROUND - 205 + 4 * math.sin(lt * 14))
    elif lt < 2.9:
        put(c, WAVE2, cat_x, GROUND - 215)
    else:
        put(c, LOVE, cat_x, GROUND - 205 - abs(math.sin(lt * 4)) * 10)
    if friend:
        hop = abs(math.sin(lt * 6))
        sp = fit_h(flap(lt, 8), 300) if hop > 0.4 else squash(CROW_SM, 0.08)
        put(c, sp, crow_x, GROUND - 170 - hop * 60)
    else:
        put(c, CROW_SM, crow_x, GROUND - 170 + 3 * math.sin(lt * 3))
    # 츄르가 풍년이 → 까마귀
    if lt < 1.0:
        pass
    elif lt < 2.9:
        p = ease((lt - 1.3) / 1.2)
        put(c, CHURU, lerp(cat_x + 150, crow_x - 90, p), GROUND - 330 - math.sin(p * 3.14) * 160, rot=lerp(0, -30, p))
    else:
        put(c, CHURU, crow_x - 70, GROUND - 230, rot=-30)
        # 방울은 다시 풍년이에게
        p = ease((lt - 3.1) / 0.9)
        put(c, BELL, lerp(crow_x + 40, cat_x + 170, p), GROUND - 420 - math.sin(p * 3.14) * 120)
        for i in range(7):  # 하트
            hp = ((lt - 2.9) * 0.55 + i / 7) % 1
            put(c, HEART, 540 + math.sin(i * 2.3) * 300, GROUND - 300 - hp * 650, scale=0.6 + 0.5 * hp, alpha=1 - hp)
        sparkles(c, lt, 560, 900, n=10, r=420, size=56, seed=31)
    text(c, "풍년이가 제일 아끼는 츄르를...\n나눠 줬어요", 430, F_CAP, alpha=fade(lt, 0.3, 2.8))
    text(c, "심술쟁이 까마귀랑\n친구가 됐어요!", 430, F_CAP, alpha=fade(lt, 3.0, 5.8), fill=(255, 236, 150))
    return c

def s6(t):  # 24.6~27.4 상자 속 누군가
    lt = t - 24.6
    c = bg_at("sunset", 0.35)
    shadow(c, 320, GROUND + 10, 340)
    put(c, YAY, 320, GROUND - 205 - abs(math.sin(lt * 5)) * 20)
    put(c, BELL, 470, GROUND - 400)
    bx = lerp(1250, 800, ease((lt - 0.6) / 0.6))
    shadow(c, bx, GROUND + 20, 300)
    put(c, BOX, bx, GROUND - 90 + (8 * math.sin(lt * 20) if 1.3 < lt < 1.7 else 0))
    if lt > 1.6:
        lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((bx - 30, GROUND - 380 - 10 * math.sin(lt * 6)), "?", font=F_BIG, fill=(255, 236, 150, 255), stroke_width=8, stroke_fill=(58, 34, 70, 255))
        c.alpha_composite(lay)
    text(c, "...근데 누가\n따라오는 것 같아요", 430, F_CAP, alpha=fade(lt, 0.3, 3.2))
    return c

def s7(t):  # 27.4~30 끝 화면
    lt = t - 27.4
    c = bg_at("end", 0.5)
    put(c, WAVE_END, 540, 540, scale=1 + 0.03 * math.sin(lt * 4))
    sparkles(c, lt, 540, 560, n=8, r=220, size=50, seed=41)
    text(c, "1단계, 직접 달려 볼래요?", 860, F_CAP, alpha=fade(lt, 0.1, 9, 0.25))
    text(c, "게임 '풍년이의 모험'", 990, F_SM, alpha=fade(lt, 0.3, 9, 0.25), fill=(255, 236, 150))
    text(c, "다음 화: 시장 골목 꽥장군", 1400, F_SM, alpha=fade(lt, 0.6, 9, 0.25))
    return c

def s4(t):  # 14.4~18.8 방울 들고 날아가 혼자 앉은 까마귀
    lt = t - 14.4
    c = bg_at("sunset_sad", 0.75)
    if lt < 1.4:
        p = ease(lt / 1.4)
        put(c, N_CROW_BELL, lerp(1250, 560, p), lerp(500, GROUND - 260, p) + 25 * math.sin(lt * 9) * (1 - p), rot=6 * math.sin(lt * 9) * (1 - p))
    else:
        q = lt - 1.4
        if q < 0.2:
            sq = squash(N_CROW_SAD_L, 0.12 * (1 - q / 0.2))
            put(c, sq, 560, GROUND + 15 - sq.height / 2)
        else:
            b = breathe(N_CROW_SAD_L, q, 0.02, 1.2)
            shadow(c, 560, GROUND + 15, 340)
            put(c, b, 560, GROUND + 15 - b.height / 2, rot=1.5 * math.sin(q * 1.4))
        put(c, BELL, 790, GROUND - 70 + 4 * math.sin(lt * 3))
        sparkles(c, lt, 790, GROUND - 80, n=6, r=110, size=46, seed=21)
    text(c, "반짝이는 걸 잔뜩 모았지만...", 430, F_CAP, alpha=fade(lt, 0.3, 2.1))
    text(c, "보여 줄 친구가\n하나도 없었대요", 450, F_CAP, alpha=fade(lt, 2.2, 4.6))
    return c

def s5(t):  # 18.8~24.6 츄르 나눠 주고 친구
    lt = t - 18.8
    c = bg_at("sunset", 0.62)
    cat_x, crow_x = 330, 790
    shadow(c, cat_x, GROUND + 10, 340)
    shadow(c, crow_x, GROUND + 5, 260)
    # 풍년이
    if lt < 1.0:
        put(c, EAT, cat_x, GROUND - 205 + 4 * math.sin(lt * 14))
    elif lt < 2.0:
        stand(c, N_CAT_GIVE, cat_x, lt)
    elif lt < 3.6:
        stand(c, N_CAT_HAPPY, cat_x, lt)
    else:
        put(c, LOVE, cat_x, GROUND - 205 - abs(math.sin(lt * 4)) * 12)
    # 츄르 날아가기
    if 2.0 <= lt < 2.8:
        p = ease((lt - 2.0) / 0.8)
        put(c, CHURU, lerp(cat_x + 120, crow_x - 80, p), GROUND - 300 - math.sin(p * math.pi) * 180, rot=lerp(0, -200, p))
    # 까마귀
    if lt < 2.8:
        stand(c, N_CROW_SAD, crow_x, lt, 0.02)
    elif lt < 4.0:
        stand(c, N_CROW_EAT, crow_x, lt * 3, 0.03)
    else:
        hop = abs(math.sin((lt - 4.0) * 6))
        b = N_CROW_HEART if hop > 0.25 else squash(N_CROW_HEART, 0.08)
        put(c, b, crow_x, GROUND - b.height / 2 + 15 - hop * 60)
    if lt > 3.9:
        p = ease((lt - 3.9) / 0.9)
        put(c, BELL, lerp(crow_x, cat_x + 170, p), GROUND - 470 - math.sin(p * math.pi) * 120)
        for i in range(7):
            hp = ((lt - 3.9) * 0.55 + i / 7) % 1
            put(c, HEART, 540 + math.sin(i * 2.3) * 300, GROUND - 300 - hp * 650, scale=0.6 + 0.5 * hp, alpha=1 - hp)
        sparkles(c, lt, 560, 900, n=10, r=420, size=56, seed=31)
    text(c, "풍년이가 제일 아끼는 츄르를...\n나눠 줬어요", 430, F_CAP, alpha=fade(lt, 0.3, 3.7))
    text(c, "심술쟁이 까마귀랑\n친구가 됐어요!", 430, F_CAP, alpha=fade(lt, 3.9, 5.8), fill=(255, 236, 150))
    return c

def s6(t):  # 24.6~27.4 상자 속 누군가
    lt = t - 24.6
    c = bg_at("sunset", 0.35)
    shadow(c, 320, GROUND + 10, 340)
    if lt < 1.3:
        stand(c, N_CAT_HAPPY, 320, lt)
        put(c, BELL, 470, GROUND - 420)
    elif lt < 1.9:
        p = (lt - 1.3) / 0.6
        put(c, N_CAT_JUMP, 300, GROUND - 230 - math.sin(p * math.pi) * 130)
    else:
        stand(c, N_CAT_TILT, 300, lt)
    bx = lerp(1250, 800, ease((lt - 0.4) / 0.6))
    shadow(c, bx, GROUND + 20, 300)
    put(c, BOX, bx, GROUND - 90 + (10 * math.sin(lt * 22) if 1.1 < lt < 1.6 else 0))
    if lt > 1.6:
        lay = Image.new("RGBA", c.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((bx - 30, GROUND - 380 - 10 * math.sin(lt * 6)), "?", font=F_BIG, fill=(255, 236, 150, 255), stroke_width=8, stroke_fill=(58, 34, 70, 255))
        c.alpha_composite(lay)
    text(c, "...근데 누가\n따라오는 것 같아요", 430, F_CAP, alpha=fade(lt, 0.3, 3.2))
    return c

SCENES = [(0, 3.6, s1), (3.6, 6.4, s2), (6.4, 14.4, sclip), (14.4, 18.8, s4), (18.8, 24.6, s5), (24.6, 27.4, s6), (27.4, 30.01, s7)]
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
    if False:
        k = (9.9 - t) / 0.5
        sx, sy = int(14 * k * math.sin(t * 90)), int(10 * k * math.cos(t * 70))
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
    n = int(SR * DUR)
    out = np.zeros(n)
    tt = np.arange(n) / SR
    def note(f, start, dur, vol, shape="sine"):
        i0, i1 = int(start * SR), min(n, int((start + dur) * SR))
        if i0 >= n: return
        x = tt[: i1 - i0]
        env = np.exp(-x * 4.5) * np.minimum(1, x * 200)
        w = np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * 2 * f * x) * np.exp(-x * 8)
        out[i0:i1] += vol * env * w
    # 오르골: 박자 0.4초
    happy = [(523, 659, 784), (440, 523, 659), (349, 440, 523), (392, 494, 587)]
    sad = [(440, 523, 659), (349, 440, 523), (330, 392, 494), (349, 440, 523)]
    beat = 0.4
    t = 0.0; k = 0
    while t < DUR - 1.2:
        prog = sad if 14.4 <= t < 18.8 else happy
        ch = prog[(k // 8) % 4]
        pat = [0, 1, 2, 1, 2, 1, 0, 2]
        vol = 0.0 if 6.2 <= t < 14.4 else (0.10 if 14.4 <= t < 18.8 else 0.13)
        note(ch[pat[k % 8]] * (1 if k % 8 else 1), t, 1.2, vol)
        if k % 8 == 0:
            note(ch[0] / 2, t, 2.5, 0.0 if 4.0 <= t < 14.4 else 0.08)
        t += beat; k += 1
    # 효과음
    rng = np.random.default_rng(0)
    def whoosh(start, dur=0.6, vol=0.25):
        i0 = int(start * SR); m = int(dur * SR)
        noise = rng.normal(0, 1, m)
        k = np.ones(30) / 30
        noise = np.convolve(noise, k, mode="same")
        env = np.sin(np.linspace(0, np.pi, m)) ** 2
        out[i0:i0 + m] += vol * noise * env
    def caw(start, vol=0.22):
        for j in range(2):
            i0 = int((start + j * 0.28) * SR); m = int(0.22 * SR)
            x = np.arange(m) / SR
            f = 520 - 180 * x / 0.22
            ph = 2 * np.pi * np.cumsum(f) / SR
            saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
            env = np.minimum(1, x * 60) * np.exp(-x * 6)
            out[i0:i0 + m] += vol * env * (0.7 * saw + 0.3 * rng.normal(0, 1, m))
    def chime(start, base=1047, vol=0.12):
        for j, mult in enumerate([1, 1.25, 1.5, 2]):
            note(base * mult, start + j * 0.07, 0.9, vol)
    def pop(start, vol=0.3):
        i0 = int(start * SR); m = int(0.12 * SR); x = np.arange(m) / SR
        out[i0:i0 + m] += vol * np.sin(2 * np.pi * (300 + 900 * x / 0.12) * x) * np.exp(-x * 30)
    chime(21.7, 1047, 0.14)     # 친구
    chime(22.2, 1319, 0.1)
    pop(25.9); pop(26.2)        # 상자 들썩
    chime(27.5, 784, 0.12)
    # 부드럽게 시작·끝
    out[: int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    out[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))
    out = np.clip(out / max(1e-6, np.abs(out).max()) * 0.8, -1, 1)
    with wave.open("/home/claude/canva/clip.wav") as cw:
        ca = np.frombuffer(cw.readframes(cw.getnframes()), np.int16).astype(np.float32) / 32767
    i0 = int(CLIP_T0 * SR); m = min(len(ca), n - i0)
    seg = ca[:m].copy()
    f = int(0.25 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    out[i0:i0 + m] += seg * 0.9
    out = np.clip(out, -1, 1)
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
