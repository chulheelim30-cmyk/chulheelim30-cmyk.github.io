#!/usr/bin/env python3
"""블락풍 v71: 블록마다 돌리기는 한 번만 (대표 11-25 23:18 "무한은 좀 그래")
- 대기 블록 하나당 톡으로 90도 한 번만 돌아가요. 이미 돌린 블록을 또 누르면 '삑' 소리만
- 막힘 판정·↻ 표시도 '지금 모양 또는 한 번 돌린 모양'까지만 봐요
- 돌렸는지 여부는 이어하기 저장에도 남아요
v64·v70이 먼저 들어가 있어야 해요. 파일 경로를 인자로 주면 그 파일에 적용(앱 www 복사본용).
"""
import pathlib, sys
P = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'play/blockpung/index.html'
s = P.read_text(encoding='utf-8')
if 'ROT1_V71' in s: print('already'); sys.exit(0)
assert 'ROT_V64' in s and 'TAP_V70' in s, 'v64·v70 먼저'
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)
rep("function canPlaceRot(b, sh) { let v = sh; for (let k = 0; k < 4; k++) { if (canPlaceAnywhere(b, v)) return true; const n = rotOf(v); if (n === v) break; v = n; } return false; }",
    "/* ROT1_V71 한 번만 */ function canPlaceRot(b, sh, used) { if (canPlaceAnywhere(b, sh)) return true; if (used) return false; const n = rotOf(sh); return n !== sh && canPlaceAnywhere(b, n); }")
rep("canPlaceRot(G.board, x.sh)", "canPlaceRot(G.board, x.sh, x.rot)", 2)
rep("rotOk = !ok0 && canPlaceRot(G.board, pc.sh)", "rotOk = !ok0 && canPlaceRot(G.board, pc.sh, pc.rot)")
rep("const pc = G.tray[d.i], n = rotOf(pc.sh); if (n !== pc.sh) { pc.sh = n;",
    "const pc = G.tray[d.i], n = rotOf(pc.sh); if (pc.rot) { SND.bad(); JE.haptic('tap'); G.trayPop[d.i] = 0.3; return; } if (n !== pc.sh) { pc.rot = 1; pc.sh = n;")
rep("t: G.tray.map(x => x ? [SHAPES.indexOf(x.sh), COLORS.indexOf(x.col), x.face] : 0)",
    "t: G.tray.map(x => x ? [SHAPES.indexOf(x.sh), COLORS.indexOf(x.col), x.face, x.rot ? 1 : 0] : 0)")
rep("G.tray = sv.t.map(x => x ? { sh: SHAPES[x[0]], col: COLORS[x[1]], face: x[2] } : null);",
    "G.tray = sv.t.map(x => x ? { sh: SHAPES[x[0]], col: COLORS[x[1]], face: x[2], rot: x[3] || 0 } : null);")
rep("'끌어서 놓고, 톡 누르면 돌아가요'", "'끌어서 놓고, 톡 누르면 한 번 돌아가요'")
P.write_text(s, encoding='utf-8'); print('OK', P)
