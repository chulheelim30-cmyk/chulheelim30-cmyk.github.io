# ---------- 6화: 비 오는 날 · 개굴 선장 ----------
EG = dict(tint=(215, 230, 255), amt=0.10, rim=(255, 240, 210), rim_a=0.35)
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
FROG = SP("b_frog", 400, side=-1, **EG)
FROG2 = SP("b_frog2", 400, side=-1, **EG)
PUDDLE = fit_w(img("o_puddle"), 700)
RK = lambda t: max(0, min(1, (t - 2.5) / 0.8)) * (1 - max(0, min(1, (t - 17.4) / 1.2)))

def s1(t):
    lt = t
    c = bg_at("main", 0.1 + 0.04 * lt)
    run_pair(c, lt, lerp(-200, 640, ease(lt / 1.8)), ground=GROUND)
    rain(c, t, RK(t))
    title(c, lt, 6, "꿈길 여섯째 동네,\n연꽃 연못")
    return c

def s2(t):  # 4~8.4 비, 웅덩이
    lt = t - 4
    c = bg_at("main", 0.3)
    put(c, PUDDLE, 640, GROUND + 70)
    shadow(c, 330, GROUND + 10, 360); stand(c, DAZE, 330, lt)
    shadow(c, 800, GROUND + 10, 300)
    put(c, W_SCARE, 800 + 5 * math.sin(lt * 40), GROUND - W_SCARE.height / 2 + 12)
    rain(c, t, RK(t))
    text(c, "갑자기 비가 쏴아!", 330, F_CAP, alpha=fade(lt, 0.2, 2.2))
    if lt > 1.8:
        bubble(c, "형... 웅덩이 무서워", 600, 1180, 800, GROUND - 470, alpha=fade(lt, 1.8, 9, 0.2), f=F_SM)
        text(c, "앞에는 커다란 물웅덩이", 330, F_CAP, alpha=fade(lt, 2.2, 9), fill=(255, 236, 150))
    return c

def s3(t):  # 8.4~12.6 개굴 선장 등장
    lt = t - 8.4
    c = bg_at("main", 0.35)
    put(c, PUDDLE, 640, GROUND + 70)
    duo(c, lt, 260, 560, WAVE2 if lt > 2 else DAZE, W_SIT_M)
    fx = lerp(1350, 860, ease(lt / 0.9))
    shadow(c, fx, GROUND + 10, 260)
    put(c, FROG, fx, GROUND - FROG.height / 2 + 15 - bounce(lt, 7, 40) * (lt < 1.0))
    rain(c, t, RK(t))
    text(c, "종이배를 든\n개굴 선장 등장!", 330, F_CAP, alpha=fade(lt, 0.3, 4.2), fill=(255, 236, 150))
    if lt > 1.2:
        bubble(c, "내 배에 타라, 개굴!", 640, 1140, 860, GROUND - 440, alpha=fade(lt, 1.2, 9, 0.15), f=F_SM)
    return c

def s4(t):  # 12.6~17 종이배로 건너기
    lt = t - 12.6
    c = bg_at("main", 0.4 + 0.04 * lt)
    put(c, PUDDLE, 540, GROUND + 70, scale=1.3)
    bx = lerp(-150, 1250, ease(lt / 4.2)); by = GROUND - 90 + 14 * math.sin(lt * 3)
    rot = 4 * math.sin(lt * 2.4)
    put(c, W_SIT_M, bx - 250, by - 80, scale=0.62, rot=rot)
    put(c, YAY, bx + 230, by - 90, scale=0.62, rot=rot)
    paper_boat(c, bx, by, 0.85, rot)
    put(c, FROG, bx + 10, by - 250, scale=0.55, rot=rot)
    for i in range(3):
        r = (lt * 0.8 + i / 3) % 1
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse((bx - 420 - r * 200, by + 120 - r * 20, bx - 260 + r * 60, by + 150 + r * 20), outline=(255, 255, 255, int(160 * (1 - r))), width=4)
        c.alpha_composite(lay)
    rain(c, t, RK(t))
    text(c, "셋이 종이배를 타고\n웅덩이를 건너요", 330, F_CAP, alpha=fade(lt, 0.3, 4.2))
    return c

def s5(t):  # 17~21.4 비 그침, 선장의 고백
    lt = t - 17
    c = bg_at("main", 0.6)
    duo(c, lt, 300, 600, LOVE, W_SIT_M)
    shadow(c, 880, GROUND + 10, 260)
    stand(c, FROG2 if lt < 2.4 else FROG, 880, lt, 0.03)
    rain(c, t, RK(t))
    if lt > 1.0:
        sparkles(c, lt, 540, 700, n=10, r=420, size=50, seed=6)
    text(c, "비가 그치고\n무지개가 떴어요", 330, F_CAP, alpha=fade(lt, 0.4, 2.4), fill=(255, 236, 150))
    if lt > 0.8:
        bubble(c, "사실 나도 혼자 무서웠어, 개굴...", 560, 1140, 880, GROUND - 440, alpha=fade(lt, 0.8, 2.6, 0.15), f=F_SM)
    if lt > 2.6:
        bubble(c, "이젠 셋이니까 괜찮아요!", 420, 1180, 300, GROUND - 440, alpha=fade(lt, 2.6, 9, 0.15), f=F_SM)
    return c

def s6(t):  # 21.4~26 친구
    lt = t - 21.4
    c = bg_at("main", 0.6)
    shadow(c, 300, GROUND + 10, 360); stand(c, YAY, 300, lt)
    shadow(c, 600, GROUND + 10, 300); put(c, W_SIT_M, 600, GROUND - W_SIT_M.height / 2 + 15 - bounce(lt, 5, 26))
    shadow(c, 880, GROUND + 10, 260); put(c, FROG, 880, GROUND - FROG.height / 2 + 15 - bounce(lt + 0.3, 6, 40))
    hearts(c, lt, base=GROUND - 300)
    sparkles(c, lt, 880, GROUND - 300, n=6, r=180, size=44, seed=16)
    text(c, "개굴 선장이랑 친구!", 330, F_CAP, alpha=fade(lt, 0.3, 9), fill=(255, 236, 150))
    if lt > 1.4:
        bubble(c, "다음에 또 배 태워 줄게, 개굴!", 600, 1140, 880, GROUND - 440, alpha=fade(lt, 1.4, 9, 0.15), f=F_SM)
    return c

def s7(t):  # 26~28
    lt = t - 26
    c = bg_at("main", 0.7 + 0.08 * lt)
    cx = lerp(380, 1250, ease(lt / 2))
    shadow(c, cx - 680, GROUND + 10, 220); put(c, FROG, cx - 680, GROUND - FROG.height / 2 + 15 - bounce(lt, 8, 50), scale=0.8, flip=True)
    run_pair(c, lt, cx, ground=GROUND)
    text(c, "다음 동네로 출발!", 330, F_CAP, alpha=fade(lt, 0.2, 2.0))
    return c

def s8(t):
    return end_card(t, 28, 6, "도토리 숲, 도토리 쌍둥이")

SCENES = [(0, 4, s1), (4, 8.4, s2), (8.4, 12.6, s3), (12.6, 17, s4), (17, 21.4, s5), (21.4, 26, s6), (26, 28, s7), (28, 30.01, s8)]
XF = 0.35
TENSE = [(4.0, 9.6)]
PROG = [(392, 494, 587), (440, 523, 659), (349, 440, 523), (392, 494, 587)]
BEAT = 0.38
FX = [("wind", 2.5, 3.0, 0.08), ("pop", 9.0, 0.3), ("pop", 9.3, 0.25), ("boing", 9.6, 0.3), ("whoosh", 12.8, 1.0, 0.18),
      ("chime", 17.6, 1319, 0.1), ("chime", 18.0, 1568, 0.1), ("chime", 21.6, 1047, 0.13), ("chime", 22.1, 1319, 0.1), ("pop", 22.4, 0.2)]
