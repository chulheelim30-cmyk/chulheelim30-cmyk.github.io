#!/usr/bin/env python3
"""블락풍 v70: '톡 = 돌리기'가 폰에서 잘 안 먹던 문제
- 예전: 0.35초 안에, 14px 안에서 떼야만 돌아감 → 엄지로 누르면 자주 놓침
- 지금: 누르는 동안 손가락이 22px 넘게 안 움직였으면(1초까지) 돌림
- 누르자마자 블록이 위로 들리던 것 → 손가락이 움직이기 시작할 때 들림(톡이 '집기'로 안 느껴지게)
v64(ROT_V64)가 먼저 들어가 있어야 해요. 파일 경로를 인자로 주면 그 파일에 적용(앱 www 복사본용).
"""
import pathlib, sys
P = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'play/blockpung/index.html'
s = P.read_text(encoding='utf-8')
if 'TAP_V70' in s: print('already'); sys.exit(0)
assert 'ROT_V64' in s, 'v64 먼저'
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)
rep("      G.drag = { i, x: p.x, y: p.y, sx: p.x, sy: p.y, t0: performance.now(), k: 0, snap: null };\n      JE.tweens.to(G.drag, { k: 1 }, 0.12, 'outCubic');",
    "      G.drag = { i, x: p.x, y: p.y, sx: p.x, sy: p.y, t0: performance.now(), k: 0, snap: null, mv: 0, lifted: false }; /* TAP_V70 */")
rep("  move(p) { const d = G.drag; if (!d) return; d.x = p.x; d.y = p.y;",
    "  move(p) { const d = G.drag; if (!d) return; d.x = p.x; d.y = p.y; d.mv = Math.max(d.mv, Math.hypot(p.x - d.sx, p.y - d.sy)); if (!d.lifted && d.mv >= 10) { d.lifted = true; JE.tweens.to(d, { k: 1 }, 0.12, 'outCubic'); }")
rep("if (Math.hypot(p.x - d.sx, p.y - d.sy) < 14 && performance.now() - d.t0 < 350) {",
    "if (Math.max(d.mv || 0, Math.hypot(p.x - d.sx, p.y - d.sy)) < 22 && performance.now() - d.t0 < 1000) {")
P.write_text(s, encoding='utf-8'); print('OK', P)
