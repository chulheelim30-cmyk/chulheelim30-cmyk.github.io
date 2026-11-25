#!/usr/bin/env python3
"""블락풍 v64: '톡 = 블록 돌리기'를 크레용 새 화면에 다시 넣기
(v37 blockpung_rotate.py는 이후 크레용 화면으로 새로 만들면서 빠졌어요)
- 아래 대기 블록을 짧게 톡 누르면 90도 돌아가요. 끌면 지금처럼 놓기
- 돌려서라도 놓을 자리가 있으면 막힌 걸로 치지 않아요
- 지금 모양으론 못 놓지만 돌리면 놓을 수 있는 블록은 반쯤 흐리게 + ↻ 표시
"""
import pathlib, sys
P = pathlib.Path(__file__).resolve().parent.parent / 'play/blockpung/index.html'; s = P.read_text(encoding='utf-8')
if 'ROT_V64' in s: print('already'); sys.exit(0)
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)
rep("function fits(b, sh, gr, gc) {", """/* ROT_V64 톡 = 돌리기 */
function rotOf(sh) { const key = JSON.stringify(norm(sh.cells.map(([r, c]) => [c, -r]))); return SHAPES.find(x => x.id === sh.id && JSON.stringify(x.cells) === key) || sh; }
function canPlaceRot(b, sh) { let v = sh; for (let k = 0; k < 4; k++) { if (canPlaceAnywhere(b, v)) return true; const n = rotOf(v); if (n === v) break; v = n; } return false; }
function fits(b, sh, gr, gc) {""")
rep("      G.drag = { i, x: p.x, y: p.y, k: 0, snap: null };", "      G.drag = { i, x: p.x, y: p.y, sx: p.x, sy: p.y, t0: performance.now(), k: 0, snap: null };")
rep("    d.x = p.x; d.y = p.y; const s = snapOf(d);\n    if (s) place(d.i, s.gr, s.gc); else { SND.bad(); G.trayPop[d.i] = 0; }",
    "    d.x = p.x; d.y = p.y;\n"
    "    if (Math.hypot(p.x - d.sx, p.y - d.sy) < 14 && performance.now() - d.t0 < 350) { const pc = G.tray[d.i], n = rotOf(pc.sh); if (n !== pc.sh) { pc.sh = n; pc.face = Math.min(pc.face, n.cells.length - 1); G.trayPop[d.i] = 0.55; SND.pick(); JE.haptic('tap'); save(); } return; }\n"
    "    const s = snapOf(d);\n    if (s) place(d.i, s.gr, s.gc); else { SND.bad(); G.trayPop[d.i] = 0; }")
rep("if (!G.tray.some(x => x && canPlaceAnywhere(G.board, x.sh))) stuck();", "if (!G.tray.some(x => x && canPlaceRot(G.board, x.sh))) stuck();", 2)
rep("const sr = slotRect(i), ok = canPlaceAnywhere(G.board, pc.sh); if (!ok) anyDim = true;",
    "const sr = slotRect(i), ok0 = canPlaceAnywhere(G.board, pc.sh), rotOk = !ok0 && canPlaceRot(G.board, pc.sh), ok = ok0; if (!ok0 && !rotOk) anyDim = true;")
rep("{ face: k === pc.face, scale: Math.max(0, e), alpha: ok ? 1 : 0.32 }));",
    "{ face: k === pc.face, scale: Math.max(0, e), alpha: ok ? 1 : rotOk ? 0.6 : 0.32 }));\n"
    "      if (rotOk) { c.font = `700 18px ${JE.FONT}`; c.textAlign = 'center'; c.fillStyle = '#ff8a3d'; c.fillText('↻', sr.x + sr.w - 12, sr.y + 18); }")
rep("const hint = G.placed < 2 ? '블록을 끌어서 판에 놓아요' : anyDim ? '흐린 블록은 지금 놓을 자리가 없어요' : '';",
    "const hint = G.placed < 2 ? '끌어서 놓고, 톡 누르면 돌아가요' : anyDim ? '흐린 블록은 돌려도 놓을 자리가 없어요' : '';")
P.write_text(s, encoding='utf-8'); print('OK')
