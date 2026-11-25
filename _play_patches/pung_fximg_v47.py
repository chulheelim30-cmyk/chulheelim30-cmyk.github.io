#!/usr/bin/env python3
"""풍년이의 모험 v47: 달리기 효과를 그림으로 (꽃잎 6·별 4·비눗방울 4·하트 발자국 4·무지개 띠)"""
import sys, json, pathlib
D = pathlib.Path(__file__).resolve().parent
P = D.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'FXIMG_V47' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
art = json.load(open(D / 'pung_fx_v47.json'))
i = s.index('const IMG = {};')
s = s[:i] + '/* FXIMG_V47 */ Object.assign(SPR,' + json.dumps(art, separators=(',', ':')) + ');\n' + s[i:]
rep("t: 'petal' });", "t: 'petal', v: Math.floor(Math.random() * 6) });")
rep("t: 'star' });", "t: 'star', v: [0, 1, 3, 4][Math.floor(Math.random() * 4)] });")
rep("s: rnd(8, 14), t: 'bub' });", "s: rnd(8, 14), t: 'bub', v: Math.floor(Math.random() * 4) });")
rep("s: 10, t: 'heart' }); }", "s: 10, t: 'heart', v: Math.floor(Math.random() * 4), r: rnd(-0.25, 0.25), y: GY - 12 + (TR.alt = !TR.alt) * 7 }); }")
rep("  const c = ctx; c.save();\n  if (k === 'cape' && TR.rb.length > 2) {",
"""  const c = ctx; c.save();
  const fi = n => { const im = IMG[n]; return im && im.complete && im.naturalWidth ? im : null; };
  const rbI = k === 'cape' && fi('fx_rb');
  if (rbI && TR.rb.length > 2) { // 무지개 띠 그림을 세로 조각으로 나눠 지나온 길을 따라 휘게
    const n = Math.min(TR.rb.length, 24), W = 190, sw = W / n, ih = 30, sp = SPR.fx_rb;
    for (let j = 0; j < n; j++) { const p = TR.rb[j], x = TR.rb[0].x - G.cam - (j + 1) * sw, y = p.y + Math.sin(G.t * 8 - j * 0.45) * 2.5;
      c.globalAlpha = Math.min(1, (n - j) / 5); c.drawImage(rbI, sp.w * (1 - (j + 1) / n), 0, sp.w / n + 1, sp.h, x, y - ih / 2, sw + 1, ih); }
    c.globalAlpha = 1;
  } else if (k === 'cape' && TR.rb.length > 2) {""")
rep("    if (p.t === 'petal') { c.fillStyle = p.c;",
"""    const pim = p.t === 'petal' ? fi('fx_p' + p.v) : p.t === 'star' ? fi('fx_s' + p.v) : p.t === 'bub' ? fi('fx_b' + p.v) : p.t === 'heart' ? fi('fx_w' + p.v) : null;
    if (pim) { const sz = p.t === 'petal' ? p.s * 2.8 : p.t === 'star' ? p.s * 2.6 * (0.75 + 0.25 * Math.sin(G.t * 18 + p.x)) : p.t === 'bub' ? p.s * 2 : 20, sp = SPR[pim === IMG['fx_rb'] ? 'fx_rb' : (p.t === 'petal' ? 'fx_p' : p.t === 'star' ? 'fx_s' : p.t === 'bub' ? 'fx_b' : 'fx_w') + p.v];
      if (p.t === 'bub') c.globalAlpha = a * 0.85; if (p.t === 'heart') c.translate(0, p.y - (GY - 12));
      const w = sp.w >= sp.h ? sz : sz * sp.w / sp.h, h = sp.w >= sp.h ? sz * sp.h / sp.w : sz; c.drawImage(pim, -w / 2, -h / 2, w, h); c.restore(); continue; }
    if (p.t === 'petal') { c.fillStyle = p.c;""")
P.write_text(s, encoding='utf-8'); print('ok')
# (수동 반영) 하트 발자국 위치 이중 이동 제거
# (수동 반영) 하트 발자국: 발 디딜 때 살짝 떠오르며 사라짐, 24px
