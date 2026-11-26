
# ---------- 6~10화 소품(직접 그림) ----------
def rain(c, t, k=1.0, n=140):
    if k <= 0: return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    rng = np.random.default_rng(5)
    xs, ys, sp = rng.uniform(0, W + 200, n), rng.uniform(0, H, n), rng.uniform(1800, 2600, n)
    for x, y, s in zip(xs, ys, sp):
        yy = (y + t * s) % (H + 100) - 50; xx = (x - t * s * 0.18) % (W + 200) - 100
        d.line((xx, yy, xx - 10, yy + 46), fill=(220, 235, 255, int(150 * k)), width=3)
    c.alpha_composite(lay)
    c.alpha_composite(Image.new("RGBA", (W, H), (40, 50, 80, int(50 * k))))

def snow(c, t, k=1.0, n=160):
    if k <= 0: return
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    rng = np.random.default_rng(7)
    xs, ys, sz, sp = rng.uniform(0, W, n), rng.uniform(0, H, n), rng.uniform(3, 10, n), rng.uniform(60, 180, n)
    for i, (x, y, s, v) in enumerate(zip(xs, ys, sz, sp)):
        yy = (y + t * v) % H; xx = (x + 30 * math.sin(t * 0.8 + i)) % W
        d.ellipse((xx - s, yy - s, xx + s, yy + s), fill=(255, 255, 255, int(220 * k)))
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1)))

def acorn(c, x, y, s=1.0, rot=0, alpha=1.0):
    w = int(70 * s); h = int(86 * s)
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, int(h * 0.3), w + 4, h + 4), fill=(196, 120, 52), outline=(90, 50, 30), width=max(2, int(4 * s)))
    d.ellipse((2, 4, w + 6, int(h * 0.48)), fill=(120, 78, 40), outline=(80, 45, 25), width=max(2, int(4 * s)))
    d.rectangle((w // 2 - 3, 0, w // 2 + 5, 10), fill=(90, 55, 30))
    d.ellipse((int(w * 0.25), int(h * 0.5), int(w * 0.45), int(h * 0.68)), fill=(235, 170, 100))
    put(c, im, x, y, rot=rot, alpha=alpha)

def envelope(c, x, y, s=1.0, rot=0, alpha=1.0, label=None):
    w, h = int(150 * s), int(100 * s)
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w + 4, h + 4), radius=int(8 * s), fill=(255, 248, 230), outline=(110, 70, 50), width=max(2, int(4 * s)))
    d.line((4, 4, w // 2 + 4, h // 2 + 8, w + 4, 4), fill=(110, 70, 50), width=max(2, int(4 * s)))
    d.ellipse((w // 2 - 10 * s + 4, h // 2 - 2, w // 2 + 10 * s + 4, h // 2 + 18 * s), fill=(220, 60, 70))
    if label:
        f = font(max(14, int(15 * s)))
        d.text((w // 2 + 4, int(h * 0.82)), label, font=f, fill=(90, 50, 40), anchor="mm")
    put(c, im, x, y, rot=rot, alpha=alpha)

def paper_boat(c, x, y, s=1.0, rot=0):
    w, h = int(760 * s), int(300 * s)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(0, int(h * 0.45)), (w, int(h * 0.45)), (int(w * 0.82), h - 4), (int(w * 0.18), h - 4)], fill=(250, 250, 245), outline=(110, 90, 80))
    d.polygon([(int(w * 0.2), int(h * 0.45)), (int(w * 0.5), 0), (int(w * 0.8), int(h * 0.45))], fill=(235, 238, 245), outline=(110, 90, 80))
    d.line((int(w * 0.5), 0, int(w * 0.5), int(h * 0.45)), fill=(170, 170, 180), width=3)
    put(c, im, x, y, rot=rot)

def sled(c, x, y, s=1.0, rot=0):
    w, h = int(640 * s), int(120 * s)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 10, w - 60, int(h * 0.55)), radius=18, fill=(214, 60, 60), outline=(110, 30, 30), width=5)
    d.arc((w - 120, -40, w - 10, int(h * 0.9)), 270, 90, fill=(150, 110, 70), width=10)
    d.line((30, h - 14, w - 70, h - 14), fill=(150, 110, 70), width=10)
    put(c, im, x, y, rot=rot)

def snowball(c, x, y, r, rot, face=None):
    im = Image.new("RGBA", (2 * r + 8, 2 * r + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((4, 4, 2 * r + 4, 2 * r + 4), fill=(250, 252, 255), outline=(150, 170, 200), width=6)
    for i in range(7):
        a = i * 0.9 + rot * 0.05
        d.arc((4 + r * 0.3, 4 + r * 0.3, 2 * r - r * 0.3, 2 * r - r * 0.3), math.degrees(a), math.degrees(a) + 30, fill=(205, 220, 240), width=5)
    if face is not None:
        f = fit_w(face, int(r * 1.1)); im.alpha_composite(f, (int(r + 4 - f.width / 2), int(r + 4 - f.height / 2)))
    put(c, im, x, y, rot=rot)

def star_map(c, t, k):
    if k <= 0: return
    nodes = [(140, 300), (300, 220), (460, 330), (620, 210), (780, 320), (930, 230), (860, 470), (640, 520), (420, 560), (200, 500)]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    m = k * len(nodes)
    for i in range(len(nodes) - 1):
        if i + 1 > m: break
        (x0, y0), (x1, y1) = nodes[i], nodes[i + 1]
        q = min(1, m - i - 1 + 1e-3) if i + 1 < m else 0
        for j in range(12):
            p = j / 12
            if p > q: break
            xx, yy = lerp(x0, x1, p), lerp(y0, y1, p)
            d.ellipse((xx - 4, yy - 4, xx + 4, yy + 4), fill=(255, 240, 170, 230))
    for i, (x, y) in enumerate(nodes):
        if i < m:
            r = 16 + 5 * math.sin(t * 4 + i)
            d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 230, 140, 220), outline=(255, 255, 255, 255), width=3)
    c.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.5)))
    gl = lay.filter(ImageFilter.GaussianBlur(14)); c.alpha_composite(gl)
