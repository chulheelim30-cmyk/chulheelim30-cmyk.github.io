#!/usr/bin/env python3
"""풍년이의 모험 v40: 꾸미기 아이템을 풍년이와 같은 그림체 그림으로 (그림이 없으면 예전 코드 그림)"""
import sys, json, pathlib
D = pathlib.Path(__file__).resolve().parent
P = D.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'DECOIMG_V40' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
art = json.load(open(D / 'pung_deco_v40.json'))
i = s.index('const IMG = {};')
s = s[:i] + '/* DECOIMG_V40 */ Object.assign(SPR,' + json.dumps(art, separators=(',', ':')) + ');\n' + s[i:]
rep("  if (k === 'band') { const bw",
"""  const di = DIMG[k], im = IMG['d_' + k]; // DECOIMG_V40: [가로 위치, 세로 위치, 폭, 기울기] (머리 폭 기준)
  if (di && im && im.complete && im.naturalWidth) {
    const sp = SPR['d_' + k], w = hw * di[2], h = w * sp.h / sp.w; c.shadowBlur = hw * 0.05; c.shadowOffsetY = hw * 0.03; c.shadowColor = 'rgba(30,18,40,.3)';
    c.translate(x + hw * di[0], y + hw * di[1]); c.rotate(di[3] + (k === 'cape' ? Math.sin(G.t * 10) * 0.05 : 0)); c.drawImage(im, -w / 2, -h / 2, w, h);
    if (k === 'band') { c.shadowBlur = 0; c.fillStyle = '#fff'; c.font = `${Math.round(h * 0.42)}px Jua, sans-serif`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('투쟁결의단결', 0, -h * 0.05); }
    c.restore(); return;
  }
  if (k === 'band') { const bw""")
rep("function drawDeco(k, x, y, hw) { // DECO_V30",
"""const DIMG = { beanie: [0.02, 0.06, 1.05, 0.08], santa: [-0.12, 0.06, 1.5, 0.1], flower: [0, 0.12, 1.15, 0.06], bow: [-0.3, 0.06, 0.55, -0.3], crown: [0.02, -0.06, 0.6, 0.06],
  glasses: [0.12, 0.52, 1.0, 0.04], band: [0.03, 0.26, 1.1, 0.06], raincoat: [0.02, 0.52, 1.45, 0], scarf: [-0.08, 1.12, 1.15, 0.1], bowtie: [0.04, 1.08, 0.85, 0.05],
  cape: [-0.85, 1.0, 1.8, 0], backpack: [-1.25, 0.6, 0.85, -0.15] };
function drawDeco(k, x, y, hw) { // DECO_V30""")
P.write_text(s, encoding='utf-8'); print('ok')
# 투쟁 머리띠 글자는 띠 곡선을 따라 한 글자씩 (본문 참고, 수동 반영)
