# v63 풍년이의 모험
# 1) 렉 줄이기: 장애물 빨간 빛(v60)과 풍년이 흰 테두리를 매 장면마다 흐림 필터로 그리던 걸
#    그림마다 한 번만 미리 만들어 두고 재사용. 피버 때 풍년이 그림자 흐림(shadowBlur)도 뺌
# 2) 망토: 코드로 그린 망토 대신 Bing으로 그린 망토 3장(펄럭이는 순서대로)
# 그림: _art_new/items/cape0~2.webp
import base64
P = 'play/pungnyeon/index.html'
A = '_art_new/items/'
s = open(P, encoding='utf8').read()
def rep(o, n):
    global s
    assert s.count(o) == 1, ('못 찾음/여러 개', s.count(o), o[:90]); s = s.replace(o, n)
def spr(k, f):
    from PIL import Image
    im = Image.open(A + f); return f'"{k}": {{"src": "data:image/webp;base64,{base64.b64encode(open(A + f, "rb").read()).decode()}", "w": {im.width}, "h": {im.height}}}'
if 'PERF_V63' not in s:
    # --- 1) 장애물 빛: 미리 만들어 둔 그림 사용
    rep("function put(e, x, y, o) {\n  const W = e.ww + 16, H = e.hh + 16;",
        "let HZG = false; /* PERF_V63 */\n"
        "function glowSpr(e) { if (e.gl) return e.gl; const k = e.cv.width / (e.ww + 16), c = document.createElement('canvas'); c.width = e.cv.width; c.height = e.cv.height; const g = c.getContext('2d');\n"
        "  g.filter = `drop-shadow(0 0 ${1.6 * k}px #fff) drop-shadow(0 0 ${1.2 * k}px #fff) drop-shadow(0 0 ${3.5 * k}px rgba(255,60,50,.95))`; g.drawImage(e.cv, 0, 0); e.gl = { cv: c, ax: e.ax, ay: e.ay, ww: e.ww, hh: e.hh }; return e.gl; }\n"
        "function put(e, x, y, o) {\n  if (HZG && e && e.cv) e = glowSpr(e);\n  const W = e.ww + 16, H = e.hh + 16;")
    rep("if (hz) { ctx.save(); ctx.filter = OUTF; }", "if (hz) { ctx.save(); HZG = true; }")
    # 장애물 그리기 끝(if (hz) ctx.restore();)은 한 군데만 있어요
    rep("    if (hz) ctx.restore();", "    if (hz) { HZG = false; ctx.restore(); }")
    # --- 풍년이 흰 테두리: 그림·크기별로 한 번만
    rep("drawBoss(); drawWang(); drawPals(); runLines(); ctx.save(); ctx.filter = CATF; drawCat(); ctx.restore();",
        "drawBoss(); drawWang(); drawPals(); runLines(); ctx.save(); drawCat(); ctx.restore();")
    rep("  ctx.drawImage(im, -w * 0.55, -h, w, h); ctx.shadowBlur = 0;",
        "  { const cg = catGlow(im, f, w, h); ctx.shadowBlur = 0; ctx.drawImage(cg, -w * 0.55 - 4, -h - 4, w + 8, h + 8); } ctx.shadowBlur = 0;")
    rep("function drawCat() {", """const CGL = new Map();
function catGlow(im, f, w, h) { const key = f + '|' + Math.round(w) + '|' + Math.round(h); let c = CGL.get(key); if (c) return c;
  const k = Math.min(2, DPR || 1); c = document.createElement('canvas'); c.width = Math.ceil((w + 8) * k); c.height = Math.ceil((h + 8) * k); const g = c.getContext('2d');
  g.filter = `drop-shadow(0 0 ${2 * k}px rgba(255,255,255,.95))`; g.drawImage(im, 4 * k, 4 * k, w * k, h * k); if (CGL.size > 160) CGL.clear(); CGL.set(key, c); return c; }
function drawCat() {""")
    # --- 2) 망토 그림
    rep("/* DECOIMG_V40 */ Object.assign(SPR,{",
        "/* CAPE_V63 */ Object.assign(SPR,{" + ', '.join(spr(f'cape{i}', f'cape{i}.webp') for i in range(3)) + "});\n/* DECOIMG_V40 */ Object.assign(SPR,{")
    i0 = s.index("function drawCape() {"); i1 = s.index("function drawCat() {", i0)
    # catGlow 정의가 drawCape 뒤·drawCat 앞에 들어갔으므로 drawCape 본문만 바꿔요
    i1 = s.index("const CGL = new Map();", i0)
    s = s[:i0] + """function drawCape() { // 피버 비행 망토(그림 3장을 번갈아): 걸쇠가 풍년이 목에 오게
  if (!(G.fever > 0) || !G.flying || G.state !== 'play') return;
  const k = 'cape' + (Math.floor(G.t * 10) % 3), im = IMG[k], sp = SPR[k]; if (!im || !im.complete || !im.naturalWidth) return;
  const W = 140, H = W * sp.h / sp.w, cx = SX() + 22, cy = PL.y - 60;
  ctx.drawImage(im, cx - W * 0.955, cy - H * 0.45, W, H);
  if (!LOW && Math.random() < 0.35) parts.push({ x: G.cam + cx - W + rnd(-4, 4), y: cy + rnd(-6, 14), vx: -G.speed * 0.2, vy: rnd(-20, 20), life: 0.45, max: 0.45, kind: 'spark', col: ['#fff3b0', '#ff9ad0', '#fff'][Math.floor(Math.random() * 3)], size: 0.45, rot: 0, vr: 0, g: 0 });
}
""" + s[i1:]
    open(P, 'w', encoding='utf8').write(s); print('OK')
