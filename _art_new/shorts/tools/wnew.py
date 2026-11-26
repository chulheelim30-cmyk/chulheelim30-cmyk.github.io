
# ---------- 새 왕년이 그림(11-26 12포즈 시트) ----------
from PIL import ImageOps as _IO
_WN = "/tmp/w/x4w2"
def _w(n, flip=False):
    p = f"{_WN}/{n}.png"
    if not os.path.exists(p): p = f"/tmp/w/wnew/{n}.png"
    im = Image.open(p).convert("RGBA")
    return _IO.mirror(im) if flip else im
_G = dict(globals().get("MK", {}) or dict(tint=(255, 214, 170), amt=0.12))
_G["rim_a"] = 0.12
_D = dict(globals().get("DAY") or globals().get("NT") or globals().get("SS") or globals().get("EG") or _G); _D["rim_a"] = 0.1
W_BOX = grade(fit_w(_w("w_box"), 400), **_G)
BOX = grade(fit_w(_w("w_box"), 380), **_G)
W_JUMP = grade(fit_h(_w("w_run1"), 430), **_G)
W_SIT = grade(fit_h(_w("w_sit"), 540), **_G)
W_SIT_M = grade(fit_h(_w("w_sit"), 470), **_G)
W_RUN = [grade(fit_h(_w("w_run0"), 350), **_G), grade(fit_h(_w("w_run1"), 370), **_G)]
W_SCARE = grade(fit_h(_w("w_scare"), 470), **_D)
W_NUZZLE = grade(fit_h(_w("w_walk", True), 430), **_G)
W_JUMP3 = grade(fit_h(_w("w_run1"), 420), **_D)
W_SIT3 = grade(fit_h(_w("w_sit"), 470), **_D)
W_SIT4 = W_SIT5 = grade(fit_h(_w("w_sit"), 470), **_D)
W_SCARE4 = grade(fit_h(_w("w_scare"), 470), **_D)
W_NUZ = grade(fit_h(_w("w_walk"), 400), **_D)
if any(k in globals() for k in ("NT", "SS", "EG")):
    W_RUN = [grade(fit_h(_w("w_run0"), 350), **_D), grade(fit_h(_w("w_run1"), 370), **_D)]
W_CHURU = grade(fit_h(_w("w_churu"), 470), **_D)
W_GROOM = grade(fit_h(_w("w_groom"), 450), **_D)
W_WALK = grade(fit_h(_w("w_walk"), 430), **_D)
W_BELLY = grade(fit_w(_w("w_sleep"), 520), **_D)
W_LIE = grade(fit_w(_w("w_lie"), 520), **_D)
W_SCRATCH = grade(fit_h(_w("w_scratch"), 480), **_D)
W_LEAP = grade(fit_h(_w("w_run1"), 400), **_D)
