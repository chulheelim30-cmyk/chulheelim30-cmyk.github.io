#!/usr/bin/env python3
"""방울풍: 고유 아이템 '풍년 방울' — 3연속 펑마다 받음. 닿은 곳 둘레 2칸의 방울을 가장 많은 색 하나로 바꾼 뒤 터뜨림 (2026-11-24 차별화)"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/bangulpung/index.html'; s = P.read_text(encoding='utf-8')
if 'PAINT_V1' in s: print('already'); sys.exit(0)
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:70]); s = s.replace(a, b)
rep("  if (col === 'bomb') {\n    JE.jelly(c, m, m, s * 0.9, s * 0.9, '#3b3f3d', { radius: 0.5 });",
    """  if (col === 'paint') { // PAINT_V1 풍년 방울: 무지개 젤리
    const gr = c.createLinearGradient(m - s * 0.45, m - s * 0.45, m + s * 0.45, m + s * 0.45); ['#ff7a9a', '#ffcf3f', '#a9ec6c', '#7ee0ff', '#b58cff'].forEach((k, i) => gr.addColorStop(i / 4, k));
    c.beginPath(); c.arc(m, m, s * 0.45, 0, 7); c.fillStyle = gr; c.fill(); c.lineWidth = 2.2; c.strokeStyle = '#2b2b2b'; c.stroke();
    c.fillStyle = 'rgba(255,255,255,.55)'; c.beginPath(); c.ellipse(m - s * 0.16, m - s * 0.2, s * 0.12, s * 0.07, -0.5, 0, 7); c.fill();
    c.font = B.font(s * 0.36); c.textAlign = 'center'; c.textBaseline = 'middle'; c.lineWidth = 3; c.strokeStyle = '#2b2b2b'; c.strokeText('풍', m, m + 2); c.fillStyle = '#fff'; c.fillText('풍', m, m + 2);
    SPR[key] = cv; return cv;
  }
  if (col === 'bomb') {
    JE.jelly(c, m, m, s * 0.9, s * 0.9, '#3b3f3d', { radius: 0.5 });""")
rep("  const ak = col === 'bomb' ? 'bub_bomb' : 'bub_' + COLORS.indexOf(col);", "  const ak = col === 'bomb' ? 'bub_bomb' : col === 'paint' ? 'bub_paint_none' : 'bub_' + COLORS.indexOf(col);")
rep("  if (G.pops >= G.bombAt) { G.next = 'bomb'; G.bombAt += 20; }", "  if (G.paintNext) { G.next = 'paint'; G.paintNext = false; }\n  else if (G.pops >= G.bombAt) { G.next = 'bomb'; G.bombAt += 20; }")
rep("  if (G.cur !== 'bomb' && !colorsLeft().includes(G.cur) && colorsLeft().length)", "  if (G.cur !== 'bomb' && G.cur !== 'paint' && !colorsLeft().includes(G.cur) && colorsLeft().length)")
rep("function land(r, c, col) {\n  JE.sfx.land();\n  let popped = [];",
    """function land(r, c, col) {
  JE.sfx.land();
  let popped = [];
  if (col === 'paint') { // 둘레 2칸을 가장 많은 색으로 칠함
    const seen = new Set([r + ',' + c]), q = [[r, c, 0]], area = [], cnt = {};
    while (q.length) { const [a, b, k] = q.shift(); area.push([a, b]); if (k >= 2) continue; for (const [x, y] of neighbors(a, b)) if (!seen.has(x + ',' + y) && get(x, y) != null && get(x, y) !== 'bomb') { seen.add(x + ',' + y); q.push([x, y, k + 1]); } }
    area.forEach(([a, b]) => { const v = get(a, b); if (v && v !== 'paint') cnt[v] = (cnt[v] || 0) + 1; });
    const best = Object.keys(cnt).sort((x, y) => cnt[y] - cnt[x])[0] || randCol(colorsLeft());
    area.forEach(([a, b]) => { G.rows[a][b] = best; JE.fx.burst(px(a, b), py(a), best, 4, 120); });
    col = best; JE.sfx.select(6); K.flash(0.25, '255,230,140');
    K.pop('풍년 방울! 한 색으로', px(r, c), py(r) - 30, { size: 24, c1: '#fff3c8', c2: '#ff9ad5' });
  }""")
rep("    G.combo++; G.maxCombo = Math.max(G.maxCombo, G.combo);\n    popped.forEach(",
    "    G.combo++; G.maxCombo = Math.max(G.maxCombo, G.combo);\n    if (G.combo % 3 === 0 && G.next !== 'paint') { G.paintNext = true; K.pop('풍년 방울 준비!', L.W / 2, L.deadY - 150, { size: 22, c1: '#fff3c8', c2: '#ff9ad5' }); }\n    popped.forEach(")
rep("      if (!colorsLeft().includes(G.cur)) G.cur = randCol(colorsLeft());\n    }\n  } else {", "      if (G.cur !== 'paint' && !colorsLeft().includes(G.cur)) G.cur = randCol(colorsLeft());\n    }\n  } else {")
rep("{ t: G.next === 'bomb' ? '다음: 폭탄!' :", "{ t: G.next === 'paint' ? '다음: 풍년 방울!' : G.next === 'bomb' ? '다음: 폭탄!' :")
rep("매달린 방울은 우르르 떨어져 보너스.<br>", "매달린 방울은 우르르 떨어져 보너스.<br>3연속 펑이면 <b style=\"color:#ff9ad5\">풍년 방울</b>: 둘레를 한 색으로!<br>")
P.write_text(s, encoding='utf-8'); print('ok')
