#!/usr/bin/env python3
"""블락풍 v37: 보관 칸 빼고 '톡 = 돌리기'(블록을 누르면 90도 회전) + 올 클리어가 실제로 나오게(블록 고를 때 판을 싹 비울 수 있는 세트 우대, 보상 +1000)"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/blockpung/index.html'; s = P.read_text(encoding='utf-8')
if 'ROT_V1' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
# 회전 짝 찾기
rep("function fits(b, sh, gr, gc) {", """/* ROT_V1 톡 = 돌리기: 같은 블록(id)의 90도 돌린 모양 */
function rotOf(sh) { const rc = norm(sh.cells.map(([r, c]) => [c, -r])), key = JSON.stringify(rc); return SHAPES.find(x => x.id === sh.id && JSON.stringify(x.cells) === key) || sh; }
function canPlaceRot(b, sh) { let v = sh; for (let k = 0; k < 4; k++) { if (canPlaceAnywhere(b, v)) return true; v = rotOf(v); } return false; }
function fits(b, sh, gr, gc) {""")
rep("      G.drag = { i, x: p.x, y: p.y, k: 0, snap: null };", "      G.drag = { i, x: p.x, y: p.y, sx: p.x, sy: p.y, t0: performance.now(), k: 0, snap: null };")
rep("    d.x = p.x; d.y = p.y; const s = snapOf(d);\n    if (s) place(d.i, s.gr, s.gc); else { SND.bad(); G.trayPop[d.i] = 0; }",
    """    if (Math.hypot(p.x - d.sx, p.y - d.sy) < 12 && performance.now() - d.t0 < 350) { // 톡 → 돌리기
      const pc = G.tray[d.i], nx = rotOf(pc.sh);
      if (nx === pc.sh) { fxPop('돌려도 같아요', p.x, p.y - 30, { size: 18, life: 0.6 }); SND.bad(); }
      else { pc.sh = nx; pc.face = Math.min(pc.face, nx.cells.length - 1); G.trayPop[d.i] = 0.4; JE.tweens.to(G.trayPop, { [d.i]: 1 }, 0.18, 'outBack'); SND.pick(); JE.haptic('tap'); G.rots = (G.rots || 0) + 1; save(); }
      return;
    }
    d.x = p.x; d.y = p.y; const s = snapOf(d);
    if (s) place(d.i, s.gr, s.gc); else { SND.bad(); G.trayPop[d.i] = 0; }""")
# 막힘 판정: 돌려서라도 놓을 수 있으면 안 막힘
rep("  checkBest();\n  if (!G.tray.some(x => x && canPlaceAnywhere(G.board, x.sh))) stuck();", "  checkBest();\n  if (!G.tray.some(x => x && canPlaceRot(G.board, x.sh))) stuck();")
rep("  if (!G.tray.some(x => x && canPlaceAnywhere(G.board, x.sh))) stuck();\n}\nasync function again()", "  if (!G.tray.some(x => x && canPlaceRot(G.board, x.sh))) stuck();\n}\nasync function again()")
rep("const sr = slotRect(i), ok = canPlaceAnywhere(G.board, pc.sh);", "const sr = slotRect(i), ok = canPlaceRot(G.board, pc.sh);")
rep("const hint = G.placed < 2 ? '블록을 끌어서 판에 놓아요' : anyDim ? '흐린 블록은 지금 놓을 자리가 없어요' : '';",
    "const hint = G.placed < 2 ? '끌어서 놓기 · 톡 누르면 돌려요' : anyDim ? '흐린 블록은 돌려도 놓을 자리가 없어요' : (G.rots || 0) < 1 && G.placed < 12 ? '블록을 톡 누르면 돌릴 수 있어요' : '';")
# 올 클리어: 블록 고를 때 판을 싹 비울 수 있는 세트 우대 + 보상 크게
rep("if (ok) { let f = 0; for (const r of nb) for (const x of r) if (x) f++; best = Math.max(best, lines * 40 - holesOf(nb) * 25 - f * 8); }",
    "if (ok) { let f = 0; for (const r of nb) for (const x of r) if (x) f++; best = Math.max(best, lines * 40 - holesOf(nb) * 25 - f * 8 + (f === 0 && lines ? 900 : 0)); }")
rep("""      G.score += 300; SND.sweep(); fxConfetti(80); fxFlash(0.5, '255,220,90'); JE.shake.add(12);
      fxPop('판 싹쓸이! +300', L.W / 2, L.by + L.bs * 0.35, { size: 42, rainbow: true, life: 1.6, delay: 0.25 });""",
    """      G.score += 1000; G.allClear = (G.allClear || 0) + 1; SND.sweep(); JE.sfx.fanfare(); fxConfetti(140); fxFlash(0.6, '255,220,90'); JE.shake.add(14); JE.haptic('success');
      fxPop('올 클리어!', L.W / 2, L.by + L.bs * 0.32, { size: 52, rainbow: true, life: 1.8, delay: 0.2, wobble: true });
      fxPop('+1000', L.W / 2, L.by + L.bs * 0.32 + 56, { size: 34, c1: '#fff', c2: '#ffd23f', life: 1.6, delay: 0.35 });
      if (JE.sketch) FX.pungi = { t: 0, say: '싹 비웠다!', mood: 'love' };""")
rep("desc: '젤리 블록을 끌어다 놓고<br>", "desc: '젤리 블록을 끌어다 놓고 <b>톡 누르면 돌려요</b><br>")
rep('  let set = null; const good = [];', '  let set = null; const good = [];\n  let acSet = null; if (fill > 0 && fill <= 24) acSet = findAllClear(b); // 올 클리어 기회 만들기')
rep('function newTray() {', 'function findAllClear(b) { // 판을 싹 비울 수 있는 블록 3개 찾기 (순서 6가지 × 상위 5개 판을 이어 보는 빔 탐색)\n  const b0 = b.map(r => r.map(x => !!x)), t0 = performance.now();\n  const conc = nb => { let s = 0; for (let r = 0; r < N; r++) { let k = 0; for (let c = 0; c < N; c++) if (nb[r][c]) k++; s += k * k; } for (let c = 0; c < N; c++) { let k = 0; for (let r = 0; r < N; r++) if (nb[r][c]) k++; s += k * k; } return s; };\n  const pool = SHAPES.filter(x => x.cells.length <= 6);\n  for (let t = 0; t < 70 && performance.now() - t0 < 120; t++) {\n    const cand = [pool[Math.floor(Math.random() * pool.length)], pool[Math.floor(Math.random() * pool.length)], pool[Math.floor(Math.random() * pool.length)]];\n    if (new Set(cand.map(x => x.id)).size < 3) continue;\n    for (const ord of PERMS3) {\n      let beam = [b0];\n      for (const i of ord) { const sh = cand[i], next = [];\n        for (const nb of beam) for (let r = 0; r <= N - sh.h; r++) for (let c = 0; c <= N - sh.wd; c++) { if (!fits(nb, sh, r, c)) continue; const a = boardAfter(nb, sh, r, c); let f = 0; for (const rr of a.nb) for (const x of rr) if (x) f++; next.push({ nb: a.nb, v: (f === 0 ? 1e6 : 0) + a.lines * 200 - f * 6 + conc(a.nb) }); }\n        if (!next.length) { beam = null; break; }\n        next.sort((x, y) => y.v - x.v); beam = next.slice(0, 5).map(x => x.nb);\n      }\n      if (beam && beam.some(nb => nb.every(r => r.every(x => !x)))) return cand;\n    }\n  }\n  return null;\n}\nfunction newTray() {')
rep('for (let tries = 0; tries < 40 && good.length < 8; tries++) {', 'for (let tries = 0; tries < 40 && good.length < 8 && !acSet; tries++) {')
rep('  if (good.length) { // 판에 잘 맞는 세트 우선', '  if (acSet) { set = acSet; G.acFound = (G.acFound || 0) + 1; }\n  else if (good.length) { // 판에 잘 맞는 세트 우선')
P.write_text(s, encoding='utf-8'); print('ok')
