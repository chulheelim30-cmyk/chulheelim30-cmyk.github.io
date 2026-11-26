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
