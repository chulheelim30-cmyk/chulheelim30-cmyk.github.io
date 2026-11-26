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
