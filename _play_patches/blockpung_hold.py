#!/usr/bin/env python3
"""블락풍: 보관 칸 1개 (블록 하나를 맡겨 두었다가 나중에 꺼내 쓰기) — 장르 대표작과 차별화 (2026-11-24)"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/blockpung/index.html'; s = P.read_text(encoding='utf-8')
if 'HOLD_V1' in s: print('already'); sys.exit(0)
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:70]); s = s.replace(a, b)
rep("const slotRect = i => ({ x: L.bx + i * L.bs / 3, y: L.trayY - 6, w: L.bs / 3, h: L.trayH + 12 });",
    """/* HOLD_V1 보관 칸: 트레이 3칸(각 bs/3.6) + 오른쪽 보관 칸 */
const SW = () => L.bs / 3.6;
const slotRect = i => i === 3 ? { x: L.bx + 3 * SW() + 8, y: L.trayY - 2, w: L.bs - 3 * SW() - 8, h: L.trayH + 4 } : { x: L.bx + i * SW(), y: L.trayY - 6, w: SW(), h: L.trayH + 12 };
const PC = i => i === 3 ? G.hold : G.tray[i];""")
rep("const TRAY_K = sh => Math.min(0.68, (L.bs / 3 - 12) / (sh.wd * L.p), (L.trayH - 14) / (sh.h * L.p));",
    "const TRAY_K = sh => Math.min(0.68, (SW() - 12) / (sh.wd * L.p), (L.trayH - 14) / (sh.h * L.p));\nconst HOLD_K = sh => { const r = slotRect(3); return Math.min(0.5, (r.w - 14) / (sh.wd * L.p), (r.h - 26) / (sh.h * L.p)); };")
rep("const sh = G.tray[d.i].sh, k = d.k, tk = TRAY_K(sh),", "const sh = PC(d.i).sh, k = d.k, tk = d.i === 3 ? HOLD_K(sh) : TRAY_K(sh),")
rep("const o = dragOrigin(d), sh = G.tray[d.i].sh;", "const o = dragOrigin(d), sh = PC(d.i).sh;")
rep("    for (let i = 0; i < 3; i++) if (G.tray[i] && inRect(p, slotRect(i))) {", "    for (let i = 0; i < 4; i++) if (PC(i) && inRect(p, slotRect(i))) {")
rep("d.preview = s ? previewClear(G.tray[d.i], s) : null; },", "d.preview = s ? previewClear(PC(d.i), s) : null; },")
rep("    if (s) place(d.i, s.gr, s.gc); else { SND.bad(); G.trayPop[d.i] = 0; }",
    """    const hr = slotRect(3), inHold = inRect(p, { x: hr.x - 6, y: hr.y - 10, w: hr.w + 12, h: hr.h + 20 });
    if (!s && inHold && d.i !== 3) { holdSwap(d.i); return; }
    if (s) place(d.i, s.gr, s.gc); else { SND.bad(); if (d.i < 3) G.trayPop[d.i] = 0; }""")
rep("function place(i, gr, gc) {\n  const pc = G.tray[i]; G.tray[i] = null;",
    """function holdSwap(i) { // 트레이 블록 ↔ 보관 칸
  const pc = G.tray[i]; G.tray[i] = G.hold || null; G.hold = pc; G.trayPop[i] = 0; G.holdPop = 0;
  JE.tweens.to(G, { holdPop: 1 }, 0.25, 'outBack'); SND.pick(); JE.haptic('tap');
  if (G.tray.every(x => !x)) newTray();
  if (!G.tray.some(x => x && canPlaceAnywhere(G.board, x.sh)) && !(G.hold && canPlaceAnywhere(G.board, G.hold.sh))) stuck(); else save();
}
function place(i, gr, gc) {
  const pc = PC(i); if (i === 3) G.hold = null; else G.tray[i] = null;""")
rep("  if (G.tray.every(x => !x)) newTray();\n  checkBest();\n  if (!G.tray.some(x => x && canPlaceAnywhere(G.board, x.sh))) stuck();",
    "  if (G.tray.every(x => !x)) newTray();\n  checkBest();\n  if (!G.tray.some(x => x && canPlaceAnywhere(G.board, x.sh)) && !(G.hold && canPlaceAnywhere(G.board, G.hold.sh))) stuck();")
rep("  if (!G.tray.some(x => x && canPlaceAnywhere(G.board, x.sh))) stuck();\n}\nasync function again()",
    "  if (!G.tray.some(x => x && canPlaceAnywhere(G.board, x.sh)) && !(G.hold && canPlaceAnywhere(G.board, G.hold.sh))) stuck();\n}\nasync function again()")
rep("t: G.tray.map(x => x ? [SHAPES.indexOf(x.sh), COLORS.indexOf(x.col), x.face] : 0),", "t: G.tray.map(x => x ? [SHAPES.indexOf(x.sh), COLORS.indexOf(x.col), x.face] : 0), h: G.hold ? [SHAPES.indexOf(G.hold.sh), COLORS.indexOf(G.hold.col), G.hold.face] : 0,")
rep("  G.tray = sv.t.map(x => x ? { sh: SHAPES[x[0]], col: COLORS[x[1]], face: x[2] } : null);", "  G.tray = sv.t.map(x => x ? { sh: SHAPES[x[0]], col: COLORS[x[1]], face: x[2] } : null);\n  G.hold = sv.h ? { sh: SHAPES[sv.h[0]], col: COLORS[sv.h[1]], face: sv.h[2] } : null;")
rep("drag: null, continued: 0, glowLines: [],", "drag: null, hold: null, holdPop: 1, continued: 0, glowLines: [],")
# 그리기: 보관 칸
rep("    c.font = `700 12px ${JE.FONT}`; c.textAlign = 'center'; c.fillStyle = BC.sub;\n    const hint = G.placed < 2 ?",
    """    { const hr = slotRect(3), hl = G.hold && !(d && d.i === 3), over = d && d.i !== 3 && inRect({ x: d.x, y: d.y }, { x: hr.x - 6, y: hr.y - 10, w: hr.w + 12, h: hr.h + 20 });
      c.save(); c.setLineDash([5, 4]); c.lineWidth = over ? 2.6 : 1.8; c.strokeStyle = over ? BC.pink : (JE.sketch ? BC.ink : 'rgba(255,255,255,.5)'); c.fillStyle = over ? 'rgba(255,140,190,.12)' : 'rgba(255,255,255,.06)';
      rr(c, hr.x, hr.y, hr.w, hr.h, 12); c.fill(); c.stroke(); c.restore();
      c.font = `800 11px ${JE.FONT}`; c.textAlign = 'center'; c.textBaseline = 'top'; c.fillStyle = JE.sketch ? BC.ink : BC.sub; c.fillText('보관', hr.x + hr.w / 2, hr.y + 5);
      if (hl) { const pc = G.hold, tp = L.p * HOLD_K(pc.sh), e = Math.max(0, Math.min(1.2, G.holdPop == null ? 1 : G.holdPop)), ok = canPlaceAnywhere(G.board, pc.sh);
        const ox = hr.x + hr.w / 2 - pc.sh.wd * tp / 2, oy = hr.y + 12 + (hr.h - 12) / 2 - pc.sh.h * tp / 2;
        pc.sh.cells.forEach(([r, col], k) => drawCube(c, ox + col * tp + tp * 0.04, oy + r * tp, tp * 0.92, pc.col, { face: k === pc.face, scale: e, alpha: ok ? 1 : 0.32 })); }
      else if (!G.hold && G.placed < 6) { c.font = `700 10px ${JE.FONT}`; c.fillStyle = BC.sub; c.textBaseline = 'middle'; c.fillText('끌어서', hr.x + hr.w / 2, hr.y + hr.h / 2 + 2); c.fillText('맡기기', hr.x + hr.w / 2, hr.y + hr.h / 2 + 15); } }
    c.font = `700 12px ${JE.FONT}`; c.textAlign = 'center'; c.fillStyle = BC.sub;
    const hint = G.placed < 2 ?""")
rep("    const pc = G.tray[d.i], o = dragOrigin(d), ps = o.p - L.gap * d.k;", "    const pc = PC(d.i), o = dragOrigin(d), ps = o.p - L.gap * d.k;")
rep("if (d && d.snap) { const pc = G.tray[d.i];", "if (d && d.snap) { const pc = PC(d.i);")
rep('desc: \'젤리 블록을 끌어다 놓고<br>가로·세로 한 줄을 채우면 펑!<br><b style="color:#ff9ad5">같은 색 6칸 이상</b> 줄은 <b style="color:#ff9ad5">점수 2배</b><br>연달아 지우면 <b style="color:#7ee0ff">콤보</b>!\'', 'desc: \'젤리 블록을 끌어다 놓고<br>가로·세로 한 줄을 채우면 펑!<br><b style="color:#ff9ad5">같은 색 6칸 이상</b> 줄은 <b style="color:#ff9ad5">점수 2배</b><br>연달아 지우면 <b style="color:#7ee0ff">콤보</b>!<br>남는 블록은 <b>보관 칸</b>에 맡겨요\'')
P.write_text(s, encoding='utf-8'); print('ok')
