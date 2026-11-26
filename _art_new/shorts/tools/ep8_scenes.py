# ---------- 8화: 꽃 골목 우체통 · 따끔이 우체부 ----------
EG = dict(tint=(255, 230, 205), amt=0.10, rim=(255, 220, 170), rim_a=0.45)
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
HOG = SP("b_hedgehog", 380, side=-1, **EG)
HOG2 = SP("b_hedgehog2", 380, side=-1, **EG)
_lr = np.random.default_rng(21)
LET = [(_lr.uniform(-1, 1), _lr.uniform(0.5, 1.0), _lr.uniform(0, 6.28)) for _ in range(5)]
def flying_letters(c, lt, x0, y0, k=1.0):
    for i, (vx, vy, ph) in enumerate(LET):
        x = x0 + vx * 520 * lt + 60 * math.sin(lt * 2 + ph)
        y = y0 - vy * 700 * min(lt, 1.2) + 120 * max(0, lt - 1.2) + 40 * math.sin(lt * 3 + ph)
        envelope(c, x, y, 0.9, rot=25 * math.sin(lt * 3 + ph), alpha=k)

def s1(t):
    lt = t
    c = bg_at("main", 0.1 + 0.04 * lt)
    run_pair(c, lt, lerp(-200, 640, ease(lt / 1.8)), ground=GROUND)
    title(c, lt, 8, "꿈길 여덟째 동네,\n꽃 골목")
    return c

def s2(t):  # 4~8.4 우체부 넘어지고 편지 훨훨
    lt = t - 4
    c = bg_at("main", 0.3)
    duo(c, lt, 260, 540, DAZE if lt > 1.4 else WAVE, W_SCARE if lt > 1.4 else W_SIT_M)
    hx = lerp(1300, 850, ease(lt / 1.2))
    shadow(c, hx, GROUND + 10, 260)
    if lt < 1.4:
        put(c, HOG, hx, GROUND - HOG.height / 2 + 15 - bounce(lt, 8, 16))
    else:
        put(c, HOG2, hx, GROUND - HOG2.height / 2 + 15, rot=lerp(-25, 0, ease((lt - 1.4) / 0.6)))
        flying_letters(c, lt - 1.4, hx - 50, GROUND - 300)
    pow_txt(c, "휘잉~", 700, 800, fade(lt, 1.4, 2.6, 0.15))
    text(c, "앗! 따끔이 우체부의\n편지가 훨훨", 330, F_CAP, alpha=fade(lt, 1.2, 9))
    return c
SHAKE.append((4 + 1.4, 0.2, 8))

def s3(t):  # 8.4~12.6 풀 죽은 우체부
    lt = t - 8.4
    c = bg_at("main", 0.45)
    flying_letters(c, lt + 3, 300, GROUND - 300, k=0.8)
    duo(c, lt, 260, 540, DAZE, W_SIT_M)
    shadow(c, 860, GROUND + 10, 260); stand(c, HOG2, 860, lt, 0.02)
    bubble(c, "오늘 배달할 편지인데... 어쩌지", 600, 1150, 860, GROUND - 420, alpha=fade(lt, 0.4, 2.4, 0.15), f=F_SM)
    if lt > 2.4:
        bubble(c, "우리가 잡아 줄게요!", 400, 1150, 260, GROUND - 420, alpha=fade(lt, 2.4, 9, 0.15), f=F_SM)
    text(c, "편지를 다 잃어버린\n따끔이 우체부", 330, F_CAP, alpha=fade(lt, 0.3, 4.2), fill=(255, 236, 150))
    return c

def s4(t):  # 12.6~17 폴짝, 쭉! 잡기
    lt = t - 12.6
    c = bg_at("main", 0.5 + 0.03 * lt)
    caught = 0
    for i, (lx, ly) in enumerate([(300, 820), (760, 700), (450, 600), (820, 950), (560, 880)]):
        tc = 0.6 + i * 0.7
        if lt < tc:
            envelope(c, lx + 40 * math.sin(lt * 2 + i), ly + 30 * math.sin(lt * 3 + i), 0.9, rot=20 * math.sin(lt * 3 + i))
        else:
            caught += 1
            q = (lt - tc) / 0.3
            if q < 1: sparkles(c, q, lx, ly, n=6, r=90, size=36, seed=30 + i)
    # 풍년이 폴짝
    jp = (lt % 1.4) / 1.4
    px = 300 + 160 * math.sin(lt * 1.3)
    shadow(c, px, GROUND + 10, 300)
    put(c, JUMP, px, GROUND - 220 - math.sin(jp * math.pi) * 520)
    wx = 760 - 120 * math.sin(lt * 1.1)
    shadow(c, wx, GROUND + 10, 280)
    put(c, W_LEAP, wx, GROUND - W_LEAP.height / 2 - math.sin(((lt + 0.7) % 1.4) / 1.4 * math.pi) * 380, flip=True)
    pow_txt(c, f"{caught}/5", 540, 1450, 1.0 if caught else 0)
    text(c, "풍년이는 폴짝,\n왕년이는 쭉!", 330, F_CAP, alpha=fade(lt, 0.3, 4.2))
    return c

def s5(t):  # 17~21.4 마지막 편지 받는 사람은
    lt = t - 17
    c = bg_at("main", 0.55)
    duo(c, lt, 230, 860, DAZE, W_SIT_M)
    s = 1.0 + 1.6 * ease(lt / 1.0)
    envelope(c, 540, lerp(1300, 1000, ease(lt / 1.0)), s, rot=lerp(20, 0, ease(lt / 1.0)), label="풍년이와 왕년이에게" if lt > 1.4 else None)
    text(c, "마지막 편지 받는 사람은...", 330, F_CAP, alpha=fade(lt, 0.3, 1.9))
    if lt > 1.8:
        text(c, "바로 우리?!", 330, F_HOOK, alpha=fade(lt, 1.8, 9), fill=(255, 236, 150))
        pow_txt(c, "!", 900, 640, fade(lt, 1.8, 3.0, 0.1))
    return c

def s6(t):  # 21.4~26 친구
    lt = t - 21.4
    c = bg_at("main", 0.55)
    shadow(c, 260, GROUND + 10, 360); stand(c, LOVE, 260, lt)
    shadow(c, 540, GROUND + 10, 300); put(c, W_SIT_M, 540, GROUND - W_SIT_M.height / 2 + 15 - bounce(lt, 5, 24))
    shadow(c, 860, GROUND + 10, 260); put(c, HOG, 860, GROUND - HOG.height / 2 + 15 - bounce(lt, 6, 30))
    hearts(c, lt, base=GROUND - 300)
    bubble(c, "\"다음 동네에서 기다릴게\" 라고 써 있어!", 540, 900, 860, GROUND - 460, alpha=fade(lt, 0.4, 2.6, 0.15), f=F_SM)
    if lt > 2.6:
        bubble(c, "고마워! 덕분에 배달 완료!", 620, 1150, 860, GROUND - 460, alpha=fade(lt, 2.6, 9, 0.15), f=F_SM)
    text(c, "따끔이 우체부랑 친구!", 330, F_CAP, alpha=fade(lt, 0.3, 9), fill=(255, 236, 150))
    return c

def s7(t):
    lt = t - 26
    c = bg_at("main", 0.7 + 0.08 * lt)
    cx = lerp(380, 1250, ease(lt / 2))
    shadow(c, cx - 680, GROUND + 10, 200); put(c, HOG, cx - 680, GROUND - HOG.height / 2 + 15 - bounce(lt, 8, 30), scale=0.8, flip=True)
    run_pair(c, lt, cx, ground=GROUND)
    text(c, "다음 동네로 출발!", 330, F_CAP, alpha=fade(lt, 0.2, 2.0))
    return c

def s8(t):
    return end_card(t, 28, 8, "눈 오는 언덕, 눈뭉치 아저씨")

SCENES = [(0, 4, s1), (4, 8.4, s2), (8.4, 12.6, s3), (12.6, 17, s4), (17, 21.4, s5), (21.4, 26, s6), (26, 28, s7), (28, 30.01, s8)]
XF = 0.35
TENSE = [(4.0, 12.6)]
PROG = [(523, 659, 784), (440, 554, 659), (466, 587, 698), (392, 494, 587)]
BEAT = 0.36
FX = [("whoosh", 4.4, 0.6, 0.2), ("boing", 5.4, 0.3), ("wind", 5.5, 2.0, 0.1), ("pop", 13.2, 0.2, 700, 1300), ("pop", 13.9, 0.2, 700, 1300),
      ("pop", 14.6, 0.2, 700, 1300), ("pop", 15.3, 0.2, 700, 1300), ("pop", 16.0, 0.2, 700, 1300), ("chime", 18.9, 1568, 0.12),
      ("chime", 21.6, 1047, 0.13), ("chime", 22.1, 1319, 0.1)]
