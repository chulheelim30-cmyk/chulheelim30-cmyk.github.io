# ---------- 10화: 달빛 구름길 · 달토끼 (시즌 1 마지막) ----------
EG = dict(tint=(215, 200, 255), amt=0.12, rim=(255, 230, 170), rim_a=0.5)
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
RAB = SP("b_rabbit", 420, side=-1, **EG)
RAB2 = SP("b_rabbit2", 420, side=-1, **EG)
CROW10 = SP("b_crow", 300, side=-1, **EG)
FRIENDS = [SP(n, h, side=-1, **EG) for n, h in [("b_crow2", 230), ("b_goose", 260), ("b_robot", 240), ("b_owl2", 250), ("b_rac", 250),
                                              ("b_frog", 250), ("b_squirrel", 220), ("b_hedgehog", 240), ("b_snowman", 280)]]

def s1(t):
    lt = t
    c = bg_at("main", 0.1 + 0.04 * lt)
    run_pair(c, lt, lerp(-200, 640, ease(lt / 1.8)), ground=GROUND)
    title(c, lt, 10, "꿈길 열째 동네,\n달빛 구름길")
    return c

def s2(t):  # 4~8.4 친구들 응원
    lt = t - 4
    c = bg_at("main", 0.4)
    rows = [(FRIENDS[:5], GROUND - 330, [130, 340, 540, 740, 950]), (FRIENDS[5:], GROUND - 170, [200, 420, 660, 880])]
    k0 = 0
    for sps, y, xs in rows:
        for sp, x in zip(sps, xs):
            k = ease((lt - 0.2 - k0 * 0.18) / 0.4); k0 += 1
            if k <= 0: continue
            put(c, sp, x, y - sp.height / 2 - bounce(lt + k0, 4, 22) * (lt > 2.0), alpha=k)
    shadow(c, 330, GROUND + 10, 360); stand(c, LOVE, 330, lt)
    shadow(c, 750, GROUND + 10, 300); stand(c, W_SIT_M, 750, lt, 0.03)
    if lt > 2.0: hearts(c, lt - 2.0, base=GROUND - 500)
    text(c, "그동안 만난 친구들이\n모두 응원하러 왔어요!", 330, F_CAP, alpha=fade(lt, 0.3, 4.2), fill=(255, 236, 150))
    return c

def s3(t):  # 8.4~12.6 달토끼
    lt = t - 8.4
    c = bg_at("main", 0.5)
    duo(c, lt, 250, 520, WAVE2, W_SIT_M)
    rx = lerp(1300, 850, ease(lt / 1.4))
    shadow(c, rx, GROUND + 10, 260); put(c, RAB, rx, GROUND - RAB.height / 2 + 15 - bounce(lt, 6, 14) * (lt < 1.4))
    text(c, "구름길 끝에서\n달토끼가 기다리고 있었어요", 330, F_CAP, alpha=fade(lt, 0.3, 4.2))
    if lt > 1.6:
        bubble(c, "어서 와, 용감한 형제들아", 620, 1150, 850, GROUND - 480, alpha=fade(lt, 1.6, 9, 0.15), f=F_SM)
    return c

def s4(t):  # 12.6~17 황금 방울
    lt = t - 12.6
    c = bg_at("main", 0.5)
    duo(c, lt, 300, 560, LOVE if lt > 2.4 else WAVE2, W_SIT_M)
    shadow(c, 850, GROUND + 10, 260); stand(c, RAB, 850, lt, 0.02)
    p = ease((lt - 0.8) / 1.6)
    bx, by = lerp(800, 330, p), lerp(GROUND - 360, GROUND - 560, p) - math.sin(p * math.pi) * 200
    put(c, BELL, bx, by + 10 * math.sin(lt * 5), scale=1 + 0.08 * math.sin(lt * 6))
    sparkles(c, lt, bx, by, n=8, r=150, size=44, seed=23)
    bubble(c, "용감한 형제에게!", 640, 1130, 850, GROUND - 480, alpha=fade(lt, 0.3, 2.2, 0.15), f=F_SM)
    text(c, "황금 방울을\n돌려받았어요!", 330, F_CAP, alpha=fade(lt, 2.2, 9), fill=(255, 236, 150))
    return c

def s5(t):  # 17~21.4 별빛 지도
    lt = t - 17
    c = bg_at("main", 0.5)
    star_map(c, lt, ease(lt / 2.6))
    duo(c, lt, 300, 640, WAVE2, W_SIT_M)
    put(c, BELL, 330, GROUND - 560 + 8 * math.sin(lt * 5), scale=1.1)
    sparkles(c, lt, 330, GROUND - 560, n=10, r=200, size=50, seed=25)
    text(c, "방울이 반짝!\n하늘에 별빛 지도가 펼쳐져요", 1000, F_CAP, alpha=fade(lt, 0.4, 9))
    return c

def s6(t):  # 21.4~26 까마귀의 편지
    lt = t - 21.4
    c = bg_at("main", 0.55)
    star_map(c, lt + 5, 1.0)
    duo(c, lt, 300, 640, DAZE if lt > 1.4 else WAVE2, W_SCARE if lt > 1.4 else W_SIT_M)
    p = ease(lt / 1.4)
    cx, cy = lerp(1300, 820, p), lerp(500, GROUND - 520, p)
    put(c, CROW10, cx, cy + 20 * math.sin(lt * 8), rot=-8 * (1 - p))
    envelope(c, cx - 70, cy + 140 + 20 * math.sin(lt * 8), 0.8, rot=-10)
    pow_txt(c, "!", 980, 640, fade(lt, 1.3, 2.4, 0.1))
    text(c, "...그런데 그때!", 330, F_CAP, alpha=fade(lt, 0.2, 1.8))
    if lt > 1.5:
        bubble(c, "큰일 났어! 꿈길 저편 동네를 도와줘!", 540, 1180, cx, cy - 120, alpha=fade(lt, 1.5, 9, 0.15), f=F_SM)
    return c
SHAKE.append((21.4 + 1.3, 0.25, 10))

def s7(t):  # 26~28 시즌 1 끝
    lt = t - 26
    c = bg_at("main", 0.6)
    star_map(c, lt + 8, 1.0)
    shadow(c, 360, GROUND + 10, 360); stand(c, WAVE2, 360, lt)
    shadow(c, 720, GROUND + 10, 300); stand(c, W_SIT_M, 720, lt, 0.03)
    text(c, "형, 우리 또 가는 거지?", 1180, F_SM, alpha=fade(lt, 0.1, 9))
    text(c, "시즌 1 끝!\n시즌 2에서 만나요", 330, F_HOOK, alpha=fade(lt, 0.3, 9), fill=(255, 236, 150))
    return c

def s8(t):
    return end_card(t, 28, 10, "시즌 2, 꿈길 저편 동네")

SCENES = [(0, 4, s1), (4, 8.4, s2), (8.4, 12.6, s3), (12.6, 17, s4), (17, 21.4, s5), (21.4, 26, s6), (26, 28, s7), (28, 30.01, s8)]
XF = 0.35
TENSE = [(21.4, 26.0)]
PROG = [(523, 659, 784), (440, 554, 659), (349, 440, 523), (392, 494, 587)]
BEAT = 0.44
FX = [("chime", 4.4, 1047, 0.1), ("chime", 4.9, 1319, 0.1), ("chime", 5.4, 1568, 0.1), ("chime", 13.4, 2093, 0.14), ("chime", 13.9, 1568, 0.12),
      ("chime", 17.3, 1319, 0.1), ("chime", 17.8, 1568, 0.1), ("chime", 18.3, 2093, 0.1), ("whoosh", 21.5, 1.2, 0.22), ("pop", 22.7, 0.35),
      ("chime", 26.2, 1047, 0.13), ("chime", 26.7, 1319, 0.12)]
