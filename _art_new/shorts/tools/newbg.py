
# ---------- 새 배경(11-26 사용자 그림 13장)으로 바꾸기: 장면 파일 뒤에 붙임 ----------
import os as _os
from PIL import ImageFilter as _IF, ImageEnhance as _IE
from alive import RegionBG as _RBG, Particles as _Pt, petal_particles as _pp
NB_DIR = "/tmp/w/nbg"
NB_EP = int(_os.environ.get("NB_EP", "1"))

def _cover(im):
    im = im.convert("RGB")
    im = im.resize((int(im.width * H / im.height), H), Image.LANCZOS)
    return im.filter(_IF.UnsharpMask(radius=2, percent=70, threshold=2))

_PARK_C = [("cloud", 0, 0, 832, 470, "pink")]
_MK_C = [("cloud", 0, 0, 832, 260, "pink")]
_RF_C = [("cloud", 0, 0, 832, 360, "pink")]
NB_REG = {
    "park_0": _PARK_C + [("hang", 0, 0, 320, 680, 9), ("hang", 560, 0, 832, 520, 9), ("water", 150, 560, 832, 800, 6),
                         ("sun", 590, 520, 50), ("lamp", 150, 370, 26)],
    "park_1": _PARK_C + [("hang", 0, 0, 320, 680, 9), ("hang", 560, 0, 832, 520, 9), ("water", 150, 570, 832, 800, 6),
                         ("sun", 615, 540, 50), ("lamp", 140, 380, 26)],
    "park_2": _PARK_C + [("hang", 0, 0, 300, 720, 9), ("hang", 560, 150, 832, 660, 9), ("water", 100, 650, 832, 900, 6),
                         ("sun", 343, 632, 55), ("lamp", 160, 370, 28)],
    "park_3": _PARK_C + [("hang", 0, 0, 260, 700, 9), ("water", 200, 600, 832, 860, 6),
                         ("sun", 335, 572, 50), ("lamp", 700, 477, 22)],
    "park_4": _PARK_C + [("hang", 0, 0, 300, 700, 9), ("hang", 600, 200, 832, 650, 8), ("water", 200, 545, 832, 800, 6),
                         ("sun", 307, 509, 45), ("lamp", 95, 498, 22)],
    "market_1": _MK_C + [("hang", 0, 420, 280, 560, 4), ("hang", 540, 410, 832, 560, 4), ("water", 0, 930, 832, 1248, 3),
                         ("lamp", 770, 195, 26), ("lamp", 595, 283, 18), ("lamp", 165, 300, 18)],
    "market_2": _MK_C + [("hang", 0, 490, 330, 640, 4), ("hang", 500, 520, 832, 680, 4), ("water", 0, 960, 832, 1248, 3),
                         ("lamp", 37, 683, 22), ("lamp", 765, 722, 22), ("lamp", 535, 673, 16)],
    "market_3": _MK_C + [("hang", 0, 420, 300, 560, 4), ("hang", 520, 400, 832, 560, 4), ("water", 0, 900, 832, 1248, 3),
                         ("lamp", 25, 576, 22), ("lamp", 787, 576, 22), ("lamp", 600, 273, 16)],
    "market_4": _MK_C + [("hang", 0, 470, 300, 620, 4), ("hang", 520, 460, 832, 620, 4), ("water", 0, 950, 832, 1248, 3),
                         ("lamp", 648, 293, 18)],
    "roof_1": _RF_C + [("hang", 470, 420, 720, 570, 10), ("sun", 322, 420, 40), ("sway", 580, 760, 800, 980, 7), ("sway", 0, 480, 140, 820, 7)],
    "roof_2": _RF_C + [("hang", 500, 390, 790, 490, 10), ("sun", 135, 470, 40), ("sway", 0, 850, 280, 1010, 6), ("sway", 720, 450, 832, 800, 7)],
    "roof_3": _RF_C + [("hang", 55, 450, 290, 570, 10), ("sun", 172, 420, 35), ("sway", 580, 780, 760, 990, 6)],
    "roof_4": _RF_C + [("hang", 510, 410, 765, 570, 10), ("sun", 453, 498, 35), ("sway", 0, 620, 160, 780, 6), ("sway", 540, 950, 700, 1060, 6)],
    "ep4": [("hang", 0, 0, 200, 700, 8), ("hang", 650, 0, 832, 500, 7), ("water", 150, 600, 832, 880, 5), ("sun", 640, 215, 40)],
    "ep5": [("hang", 0, 0, 330, 350, 6), ("water", 0, 450, 832, 760, 5), ("sun", 420, 330, 50), ("lamp", 340, 620, 18), ("lamp", 660, 640, 20),
            ("cloud", 0, 0, 832, 330, "pink")],
    "ep6": [("cloud", 0, 0, 832, 450, "white"), ("sway", 0, 250, 250, 800, 8), ("water", 150, 650, 832, 950, 5)],
    "ep7": [("hang", 0, 0, 832, 480, 5), ("sun", 420, 450, 60)],
    "ep8": [("sway", 580, 250, 832, 800, 5), ("sway", 0, 300, 250, 700, 5), ("lamp", 690, 420, 18), ("cloud", 0, 0, 832, 250, "white")],
    "ep9": [("cloud", 0, 0, 832, 400, "pink"), ("sun", 650, 450, 35), ("lamp", 60, 700, 18), ("lamp", 560, 720, 14)],
    "ep10": [("cloud", 0, 0, 832, 520, "pink"), ("sun", 620, 300, 70), ("water", 300, 620, 700, 1000, 2)],
}
NB_NIGHT = {"ep4", "ep10"}
NB_PK = {"ep4": ("night", False, True, 0.8), "ep5": ("sunset", True, False, 0.8), "ep6": ("sunset", False, False, 0.6),
         "ep7": ("sunset", True, False, 1.1), "ep8": ("petal", True, False, 0.7), "ep9": ("night", False, False, 0.5),
         "ep10": ("night", False, True, 0.9)}
_NB_IM, _NB_L = {}, {}
def _nb_get(name):
    if name not in _NB_L:
        base, _, mod = name.partition(":")
        im = _cover(Image.open(f"{NB_DIR}/bg_{base}.jpg"))
        night = base in NB_NIGHT
        if mod == "night":
            a = np.array(im).astype(np.float32)
            a = a * 0.42 + np.array([10, 14, 45], np.float32)
            a[..., 2] *= 1.25
            im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); night = True
        elif mod == "sad":
            im = _IE.Brightness(_IE.Color(im).enhance(0.6)).enhance(0.68)
        elif mod == "end":
            im = _IE.Brightness(im.filter(_IF.GaussianBlur(8))).enhance(0.62)
        _NB_IM[name] = im
        _NB_L[name] = None if mod == "end" else _RBG(im, 1248, NB_REG[base], night=night)
    return _NB_IM[name], _NB_L[name]

# (시작, 끝, 원래 key, 새 그림) — 위에서부터 먼저 맞는 것
NB_MAP = {
    1: [(0, 99, "night", "park_4:night"), (0, 99, "sunset_sad", "park_3:sad"), (0, 99, "end", "park_2:end"),
        (0, 8.6, "sunset", "park_1"), (8.6, 14.4, "sunset", "park_0"), (14.4, 24.6, "sunset", "park_4"), (24.6, 99, "sunset", "park_2")],
    2: [(0, 99, "sunset", "park_2"), (0, 99, "end", "market_2:end"), (0, 99, "night", "park_4:night"),
        (0, 8.6, "market", "market_2"), (8.6, 12.4, "market", "market_1"), (12.4, 20.6, "market", "market_3"),
        (20.6, 25.8, "market", "market_4"), (25.8, 99, "market", "market_2")],
    4: [(0, 99, "night", "ep4"), (0, 99, "end", "ep4:end")],
    5: [(0, 99, "bridge", "ep5"), (0, 99, "pic", "ep5"), (0, 99, "end", "ep5:end")],
    6: [(0, 99, "main", "ep6"), (0, 99, "end", "ep6:end")],
    7: [(0, 99, "main", "ep7"), (0, 99, "end", "ep7:end")],
    8: [(0, 99, "main", "ep8"), (0, 99, "end", "ep8:end")],
    9: [(0, 99, "main", "ep9"), (0, 99, "end", "ep9:end")],
    10: [(0, 99, "main", "ep10"), (0, 99, "end", "ep10:end")],
    3: [(0, 99, "end", "roof_2:end"), (0, 4, "roof", "roof_2"), (4, 12.6, "roof", "roof_1"), (12.6, 17, "roof", "roof_4"),
        (17, 21, "roof", "roof_3"), (21, 26, "roof", "roof_4"), (26, 99, "roof", "roof_2")],
}
_NB_PT = _Pt(3); _NB_PETAL = _pp(8)
_old_bg_at = bg_at
def bg_at(key, x, dim=0.0, *a, **k):
    t = CUR_T[0]
    nm = None
    for (t0, t1, kk, nn) in NB_MAP[NB_EP]:
        if kk == key and t0 <= t < t1:
            nm = nn; break
    if nm is None:
        return _old_bg_at(key, x, *([dim] if dim else []))
    im, L = _nb_get(nm)
    x = max(0.0, min(1.0, x))
    off = int((im.width - W) * x)
    if L is not None:
        c = Image.fromarray(L.frame(off, t, wind=0.7 if nm.endswith(":sad") else 1.0)).convert("RGBA")
    else:
        c = im.crop((off, 0, off + W, H)).convert("RGBA")
    if dim:
        c.alpha_composite(Image.new("RGBA", c.size, (10, 6, 30, int(255 * dim))))
    base = nm.split(":")[0]
    if nm.endswith(":night") or nm.endswith(":end"):
        _NB_PT.draw(c, t, "night", cam=off, leaves=False, motes=True, flies=True, strength=0.8)
    elif base in NB_PK:
        kd, lv, fl, st = NB_PK[base]
        if kd == "petal":
            _NB_PETAL.draw(c, t, "sunset", cam=off, leaves=True, motes=True, strength=st)
        else:
            _NB_PT.draw(c, t, kd, cam=off, leaves=lv, motes=True, flies=fl, strength=st)
    elif base.startswith("park"):
        _NB_PT.draw(c, t, "sunset", cam=off, leaves=True, motes=True, strength=0.6 if nm.endswith(":sad") else 0.9)
    elif base.startswith("market"):
        _NB_PT.draw(c, t, "sunset", cam=off, leaves=False, motes=True, strength=0.8)
    else:
        _NB_PETAL.draw(c, t, "sunset", cam=off, leaves=True, motes=True, strength=0.5)
    return c

GROUND = {3: 1600, 4: 1740, 5: 1720}.get(NB_EP, GROUND)
