# ---------- 소리(화마다 TENSE·FX만 바꿈) ----------
SR = 44100
def synth_audio(path):
    n = int(SR * DUR); out = np.zeros(n); tt = np.arange(n) / SR
    rng = np.random.default_rng(0)
    def note(f, start, dur, vol, dec=4.5):
        i0, i1 = int(start * SR), min(n, int((start + dur) * SR))
        if i0 >= n: return
        x = tt[: i1 - i0]
        env = np.exp(-x * dec) * np.minimum(1, x * 200)
        out[i0:i1] += vol * env * (np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * 2 * f * x) * np.exp(-x * 8))
    prog = PROG
    tense = [(440, 523, 622), (415, 494, 587)]
    beat = BEAT; t = 0.0; k = 0
    while t < DUR - 1.0:
        ten = any(a <= t < b for a, b in TENSE)
        if ten:
            ch = tense[(k // 4) % 2]; vol = 0.09; pat = [0, 2, 0, 2]
        else:
            ch = prog[(k // 8) % len(prog)]; vol = 0.11; pat = [0, 1, 2, 1, 2, 1, 0, 2]
        note(ch[pat[k % len(pat)]], t, 0.9, vol)
        if k % 4 == 0:
            note(ch[0] / 2, t, 1.6, 0.07)
        t += beat; k += 1
    def chime(start, base=1047, vol=0.12):
        for j, mult in enumerate([1, 1.25, 1.5, 2]):
            note(base * mult, start + j * 0.07, 0.9, vol)
    def pop(start, vol=0.35, f0=300, f1=900):
        i0 = int(start * SR); m = int(0.14 * SR); x = np.arange(m) / SR
        out[i0:i0 + m] += vol * np.sin(2 * np.pi * (f0 + (f1 - f0) * x / 0.14) * x) * np.exp(-x * 25)
    def whoosh(start, dur=0.5, vol=0.2):
        i0 = int(start * SR); m = int(dur * SR)
        nz = np.convolve(rng.normal(0, 1, m), np.ones(30) / 30, mode="same")
        out[i0:i0 + m] += vol * nz * np.sin(np.linspace(0, np.pi, m)) ** 2
    def beep(start, vol=0.15):
        for j, f in enumerate([1320, 990, 1320]):
            i0 = int((start + j * 0.11) * SR); m = int(0.08 * SR); x = np.arange(m) / SR
            out[i0:i0 + m] += vol * np.sign(np.sin(2 * np.pi * f * x)) * np.exp(-x * 20)
    def hoot(start, vol=0.25):
        for j in range(2):
            i0 = int((start + j * 0.45) * SR); m = int(0.35 * SR); x = np.arange(m) / SR
            f = 380 - 40 * x / 0.35
            out[i0:i0 + m] += vol * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * x / 0.35)
    def boing(start, vol=0.3):
        i0 = int(start * SR); m = int(0.4 * SR); x = np.arange(m) / SR
        out[i0:i0 + m] += vol * np.sin(2 * np.pi * (200 + 150 * np.sin(x * 40)) * x) * np.exp(-x * 7)
    def wind(start, dur=2.0, vol=0.12):
        i0 = int(start * SR); m = min(int(dur * SR), n - i0)
        nz = np.convolve(rng.normal(0, 1, m), np.ones(80) / 80, mode="same")
        out[i0:i0 + m] += vol * nz * 6 * np.sin(np.linspace(0, np.pi, m)) * (0.6 + 0.4 * np.sin(np.linspace(0, 9, m)))
    F = dict(chime=chime, pop=pop, whoosh=whoosh, beep=beep, hoot=hoot, boing=boing, wind=wind)
    for fx in FX:
        F[fx[0]](*fx[1:])
    out[: int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))
    out[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))
    out = np.clip(out / max(1e-6, np.abs(out).max()) * 0.8, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
