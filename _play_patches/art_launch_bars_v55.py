# v55: 미끌풍 막대 그림 7종, 방울풍 젤리 대포, 탱탱풍 젤리 발사판 (그림은 _art_new/)
# 사용: python3 _play_patches/art_launch_bars_v55.py  (저장소 맨 위에서)
import base64, re
A = '_art_new/'
def uri(f): return 'data:image/webp;base64,' + base64.b64encode(open(A + f, 'rb').read()).decode()
def load(g): return open(f'play/{g}/index.html', encoding='utf8').read()
def save(g, s): open(f'play/{g}/index.html', 'w', encoding='utf8').write(s)
def rep(s, old, new):
    assert s.count(old) == 1, ('못 찾음/여러 개', old[:70]); return s.replace(old, new)
def setart(s, k, f):
    s2, n = re.subn(r"JE\.art\.add\('" + k + r"','data:[^']*'\);", lambda m: f"JE.art.add('{k}','{uri(f)}');", s)
    assert n == 1, k; return s2

# --- 미끌풍 ---
s = load('miklpung')
if 'ART_V55' not in s:
    adds = ''.join(f"JE.art.add('mk_bar{i}','{uri(f'bar{i}.webp')}');\n" for i in range(7))
    s = rep(s, "JE.art.add('pungi_run7',", adds + "JE.art.add('pungi_run7',")
    s = rep(s, "function drawBlock(c, b, x, y, o = {}) {", """function mkBar(c, k, x, y, w, h) { /* ART_V55: 양 끝은 그대로, 가운데만 늘림 */
  const A = JE.art; if (!A || !A.has(k)) return false;
  const im = A.img[k], [iw, ih] = A.size[k], cap = Math.min(iw / 2 - 1, ih * 0.55), dc = Math.min(w / 2, cap * h / ih);
  c.drawImage(im, 0, 0, cap, ih, x, y, dc + 0.5, h);
  c.drawImage(im, iw - cap, 0, cap, ih, x + w - dc - 0.5, y, dc + 0.5, h);
  if (w - dc * 2 > 0) c.drawImage(im, cap, 0, iw - cap * 2, ih, x + dc - 0.5, y, w - dc * 2 + 1, h);
  return true;
}
function drawBlock(c, b, x, y, o = {}) {""")
    s = rep(s, "  JE.jelly(c, x + w / 2 + 2, y + h / 2 + 2, w, h, b.gold ? '#ffd23f' : b.col, { radius: 0.3, sx: 1 + (1 - v) * 0.3, sy: v, glow: b.gold ? 0.6 + 0.3 * Math.sin(G.t * 5) : 0 });\n  c.lineWidth = 2.5; c.strokeStyle = BC.ink; JE.roundRect(c, x + 2, y + 2 + h * (1 - v), w, h * v, h * 0.3); c.stroke();",
        "  const bi = b.gold ? 6 : COLORS.indexOf(b.col), sw = w * (1 + (1 - v) * 0.3);\n  if (bi < 0 || !mkBar(c, 'mk_bar' + bi, x + 2 + (w - sw) / 2, y + 2 + h * (1 - v), sw, h * v)) {\n  JE.jelly(c, x + w / 2 + 2, y + h / 2 + 2, w, h, b.gold ? '#ffd23f' : b.col, { radius: 0.3, sx: 1 + (1 - v) * 0.3, sy: v, glow: b.gold ? 0.6 + 0.3 * Math.sin(G.t * 5) : 0 });\n  c.lineWidth = 2.5; c.strokeStyle = BC.ink; JE.roundRect(c, x + 2, y + 2 + h * (1 - v), w, h * v, h * 0.3); c.stroke(); }")
    save('miklpung', s); print('미끌풍 OK')

# --- 방울풍 ---
s = load('bangulpung')
if 'ART_V55' not in s:
    s = setart(s, 'bub_cannon', 'bangulpung_cannon.webp')
    s = rep(s, "  c.fillStyle = BC.metal2; c.beginPath(); c.arc(L.gunX, L.gunY + L.d * 0.4, L.d * 0.95, Math.PI, 0); c.fill(); c.lineWidth = 3; c.strokeStyle = BC.deep; c.stroke();",
        "  /* ART_V55 젤리 대포 */ if (!(JE.art && JE.art.draw(c, 'bub_cannon', L.gunX, L.gunY - L.d * 0.35, L.d * 1.9, L.d * 1.9, { ay: 0, sy: 1 - G.swapT * 0.08 }))) { c.fillStyle = BC.metal2; c.beginPath(); c.arc(L.gunX, L.gunY + L.d * 0.4, L.d * 0.95, Math.PI, 0); c.fill(); c.lineWidth = 3; c.strokeStyle = BC.deep; c.stroke(); }")
    save('bangulpung', s); print('방울풍 OK')

# --- 탱탱풍 ---
s = load('taengtaengpung')
if 'ART_V55' not in s:
    s = setart(s, 'tt_launcher', 'taengtaengpung_pad.webp')
    s = rep(s, "    K.jellyFace(c, lx, ly - L.r * 0.4, L.r * 3.4, L.r * 2.8, B.JELLY[4], { radius: 0.5, mood: G.phase === 'fly' ? 'happy' : 'normal' });",
        "    /* ART_V55 젤리 발사판 */ if (!(JE.art && JE.art.draw(c, 'tt_launcher', lx, L.floor + 8, 74, 56, { ay: 1 }))) K.jellyFace(c, lx, ly - L.r * 0.4, L.r * 3.4, L.r * 2.8, B.JELLY[4], { radius: 0.5, mood: G.phase === 'fly' ? 'happy' : 'normal' });\n    if (G.phase !== 'fly' && JE.art && JE.art.has('tt_ball')) JE.art.draw(c, 'tt_ball', lx, L.floor - 38, L.r * 2.6, L.r * 2.6);")
    save('taengtaengpung', s); print('탱탱풍 OK')
