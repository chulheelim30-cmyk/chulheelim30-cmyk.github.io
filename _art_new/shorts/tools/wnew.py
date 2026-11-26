
# ---------- 새 왕년이 그림(11-26 12포즈 시트) ----------
from PIL import ImageOps as _IO
_WN = "/tmp/w/x4w"
def _w(n, flip=False):
    p = f"{_WN}/{n}.png"
    if not os.path.exists(p): p = f"/tmp/w/wnew/{n}.png"
    im = Image.open(p).convert("RGBA")
    return _IO.mirror(im) if flip else im
_G = dict(globals().get("MK", {}) or dict(tint=(255, 214, 170), amt=0.12))
_G["rim_a"] = 0.12
_D = dict(globals().get("DAY", _G)); _D["rim_a"] = 0.1
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
