#!/usr/bin/env python3
"""블락풍 v72: 톡 = 돌리기 ↔ 원래대로 (대표 11-25 23:25)
- 톡 누르면 90도 돌아가고, 다시 톡 누르면 원래 모양으로 돌아와요(두 모양만 왔다 갔다)
- 막힘 판정·↻ 표시는 '지금 모양 또는 반대쪽 모양'까지 봐요
- 원래 모양은 이어하기 저장에도 남아요(t 배열 5번째 칸)
v64·v70·v71이 먼저 들어가 있어야 해요. 파일 경로를 인자로 주면 그 파일에 적용(앱 www 복사본용).
"""
import pathlib, sys
P = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'play/blockpung/index.html'
s = P.read_text(encoding='utf-8')
if 'ROTTG_V72' in s: print('already'); sys.exit(0)
assert 'ROT1_V71' in s, 'v71 먼저'
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)
rep("function canPlaceRot(b, sh, used) { if (canPlaceAnywhere(b, sh)) return true; if (used) return false; const n = rotOf(sh); return n !== sh && canPlaceAnywhere(b, n); }",
    "/* ROTTG_V72 돌리기↔원래대로 */ function altOf(pc) { return pc.rot && pc.sh0 ? pc.sh0 : rotOf(pc.sh); }\n"
    "function canPlaceRot(b, sh, pc) { if (canPlaceAnywhere(b, sh)) return true; const n = pc ? altOf(pc) : rotOf(sh); return n !== sh && canPlaceAnywhere(b, n); }")
rep("canPlaceRot(G.board, x.sh, x.rot)", "canPlaceRot(G.board, x.sh, x)", 2)
rep("canPlaceRot(G.board, pc.sh, pc.rot)", "canPlaceRot(G.board, pc.sh, pc)")
rep("if (pc.rot) { SND.bad(); JE.haptic('tap'); G.trayPop[d.i] = 0.3; return; } if (n !== pc.sh) { pc.rot = 1; pc.sh = n;",
    "if (pc.rot && pc.sh0) { pc.sh = pc.sh0; pc.sh0 = null; pc.rot = 0; pc.face = Math.min(pc.face, pc.sh.cells.length - 1); G.trayPop[d.i] = 0.55; SND.pick(); JE.haptic('tap'); save(); return; } if (n !== pc.sh) { pc.rot = 1; pc.sh0 = pc.sh; pc.sh = n;")
rep("x.face, x.rot ? 1 : 0] : 0)", "x.face, x.rot ? 1 : 0, x.rot && x.sh0 ? SHAPES.indexOf(x.sh0) : -1] : 0)")
rep("face: x[2], rot: x[3] || 0 } : null);", "face: x[2], rot: x[3] && x[4] >= 0 ? 1 : 0, sh0: x[3] && x[4] >= 0 ? SHAPES[x[4]] : null } : null);")
rep("'끌어서 놓고, 톡 누르면 한 번 돌아가요'", "'끌어서 놓고, 톡 누르면 돌아가요(다시 톡: 원래대로)'")
P.write_text(s, encoding='utf-8'); print('OK', P)
