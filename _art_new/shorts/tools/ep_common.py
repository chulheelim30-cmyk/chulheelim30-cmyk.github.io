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
