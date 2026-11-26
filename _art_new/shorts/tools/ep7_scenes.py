# ---------- 7화: 도토리 숲 · 도토리 쌍둥이 ----------
EG = dict(tint=(255, 215, 160), amt=0.14, rim=(255, 190, 110), rim_a=0.55)
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
SQ = SP("b_squirrel", 330, side=-1, **EG)
SQ2 = SP("b_squirrel2", 330, side=-1, **EG)
_ar = np.random.default_rng(11)
ACORNS = [(_ar.uniform(80, 1000), _ar.uniform(0, 1.2), _ar.uniform(0.7, 1.2)) for _ in range(14)]
def falling(c, lt, t0, dur=1.6, n=14, land=None):
    land = land or GROUND + 30
    for i, (x, d0, s) in enumerate(ACORNS[:n]):
        p = (lt - t0 - d0 * 0.6) / dur
        if p < 0: continue
        y = lerp(-80, land, min(1, p) ** 2)
        acorn(c, x, y, s, rot=(p * 400 + i * 30) if p < 1 else 15)

def s1(t):
    lt = t
    c = bg_at("main", 0.1 + 0.04 * lt)
    run_pair(c, lt, lerp(-200, 640, ease(lt / 1.8)), ground=GROUND)
    title(c, lt, 7, "꿈길 일곱째 동네,\n도토리 숲")
    return c

def s2(t):  # 4~8.4 도토리 우수수
    lt = t - 4
    c = bg_at("main", 0.35)
    duo(c, lt, 360, 720, DAZE if lt > 1.2 else LOVE, W_SCARE if lt > 1.2 else W_SIT_M)
    falling(c, lt, 0.4)
    pow_txt(c, "콩!", 380, GROUND - 520, fade(lt, 1.2, 2.0, 0.1))
    text(c, "도토리가 우수수!", 330, F_CAP, alpha=fade(lt, 0.2, 9))
    return c
SHAKE.append((4 + 1.2, 0.25, 8))

def s3(t):  # 8.4~12.6 우는 쌍둥이
    lt = t - 8.4
    c = bg_at("main", 0.5)
    for x, y, s in [(200, GROUND + 30, 1), (460, GROUND + 40, 0.9), (930, GROUND + 25, 1.1), (680, GROUND + 45, 0.8)]:
        acorn(c, x, y, s, rot=20)
    duo(c, lt, 230, 470, DAZE, W_SIT_M)
    for k, x in enumerate([760, 940]):
        shadow(c, x, GROUND + 10, 220)
        put(c, SQ2, x + 3 * math.sin(lt * 20 + k), GROUND - SQ2.height / 2 + 15, flip=k == 1)
    text(c, "울고 있는\n도토리 쌍둥이", 330, F_CAP, alpha=fade(lt, 0.3, 4.2), fill=(255, 236, 150))
    if lt > 1.0:
        bubble(c, "겨울 도토리가 다 흩어졌어...", 600, 1150, 850, GROUND - 380, alpha=fade(lt, 1.0, 9, 0.15), f=F_SM)
    return c

def s4(t):  # 12.6~17 풍년이 날쌔게 줍기
    lt = t - 12.6
    c = bg_at("main", 0.5 + 0.03 * lt)
    xs = [200, 380, 560, 740, 920]
    px = lerp(-150, 1150, ease(lt / 3.6))
    got = 0
    for x in xs:
        if px < x - 30:
            acorn(c, x, GROUND + 30 - 6 * math.sin(lt * 6 + x), 1.0, rot=15)
        else:
            got += 1
            q = (px - x) / 300
            if q < 1: acorn(c, x, GROUND - 100 - q * 300, 1.0 - 0.4 * q, alpha=1 - q)
    shadow(c, px, GROUND + 10, 360)
    put(c, RUN[int(lt * 16) % 8], px, GROUND - 180 - bounce(lt, 8, 14))
    if got:
        pow_txt(c, f"{got}개!", min(900, max(180, px)), GROUND - 520, 1.0)
    text(c, "풍년이는 날쌔게\n하나, 둘, 셋!", 330, F_CAP, alpha=fade(lt, 0.3, 4.2))
    return c

def s5(t):  # 17~21.4 왕년이 큰 덩치로 쿵
    lt = t - 17
    c = bg_at("main", 0.62)
    wx = 560
    if lt < 1.2:
        p = ease(lt / 1.2)
        shadow(c, lerp(300, wx, p), GROUND + 10, 300)
        put(c, W_RUN[int(lt * 9) % 2], lerp(300, wx, p), GROUND - W_RUN[0].height / 2 - 10 - bounce(lt, 9, 20))
    else:
        q = lt - 1.2
        sq = squash(W_SIT_M, 0.1 * max(0, 1 - q / 0.3))
        shadow(c, wx, GROUND + 10, 300); put(c, sq, wx, GROUND - sq.height / 2 + 15)
        falling(c, lt, 1.25, dur=1.2, n=10)
        pow_txt(c, "쿵!", wx, GROUND - 600, fade(lt, 1.2, 2.0, 0.1))
    shadow(c, 880, GROUND + 10, 220); put(c, SQ2 if lt < 2.4 else SQ, 880, GROUND - SQ.height / 2 + 15 - bounce(lt, 7, 30) * (lt > 2.4))
    text(c, "왕년이는 큰 덩치로 쿵!\n높은 도토리까지 우수수", 330, F_CAP, alpha=fade(lt, 0.3, 4.2), fill=(255, 236, 150))
    return c
SHAKE.append((17 + 1.2, 0.35, 16))

def s6(t):  # 21.4~26 친구
    lt = t - 21.4
    c = bg_at("main", 0.62)
    shadow(c, 260, GROUND + 10, 360); stand(c, YAY, 260, lt)
    shadow(c, 540, GROUND + 10, 300); put(c, W_SIT_M, 540, GROUND - W_SIT_M.height / 2 + 15 - bounce(lt, 5, 24))
    for k, x in enumerate([790, 960]):
        shadow(c, x, GROUND + 10, 220)
        put(c, SQ, x, GROUND - SQ.height / 2 + 15 - bounce(lt + k * 0.4, 7, 40), flip=k == 1)
    hearts(c, lt, base=GROUND - 300)
    text(c, "도토리 쌍둥이랑 친구!\n지름길도 알려 줬어요", 330, F_CAP, alpha=fade(lt, 0.3, 9), fill=(255, 236, 150))
    if lt > 1.2:
        bubble(c, "형들 최고! 이쪽이 지름길이야!", 620, 1150, 870, GROUND - 380, alpha=fade(lt, 1.2, 9, 0.15), f=F_SM)
    return c

def s7(t):
    lt = t - 26
    c = bg_at("main", 0.7 + 0.08 * lt)
    cx = lerp(380, 1250, ease(lt / 2))
    for k in range(2):
        x = cx - 650 - k * 170
        shadow(c, x, GROUND + 10, 180); put(c, SQ, x, GROUND - SQ.height / 2 + 15 - bounce(lt + k * 0.3, 9, 50), scale=0.75, flip=True)
    run_pair(c, lt, cx, ground=GROUND)
    text(c, "다음 동네로 출발!", 330, F_CAP, alpha=fade(lt, 0.2, 2.0))
    return c

def s8(t):
    return end_card(t, 28, 7, "꽃 골목 우체통, 따끔이 우체부")

SCENES = [(0, 4, s1), (4, 8.4, s2), (8.4, 12.6, s3), (12.6, 17, s4), (17, 21.4, s5), (21.4, 26, s6), (26, 28, s7), (28, 30.01, s8)]
XF = 0.35
TENSE = [(4.0, 12.6)]
PROG = [(440, 554, 659), (392, 494, 587), (349, 440, 523), (392, 494, 587)]
BEAT = 0.36
FX = [("pop", 4.6, 0.2), ("pop", 4.9, 0.2), ("boing", 5.2, 0.35), ("pop", 5.5, 0.2), ("pop", 13.4, 0.2, 700, 1200), ("pop", 14.0, 0.2, 700, 1200),
      ("pop", 14.6, 0.2, 700, 1200), ("pop", 15.2, 0.2, 700, 1200), ("pop", 15.8, 0.2, 700, 1200), ("boing", 18.2, 0.45), ("pop", 18.6, 0.2),
      ("chime", 21.6, 1047, 0.13), ("chime", 22.1, 1319, 0.1)]
