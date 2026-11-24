#!/usr/bin/env python3
"""풍년이의 모험 v39: 꾸미기가 몸에 붙어 보이게 — 머리 위치 흔들림 줄이기(부드럽게 따라가기), 털 위 그림자, 얇은 선, 가방 모양 정리"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'DECO_V39' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("if (sp.hd && DECO.cur) drawDeco(DECO.cur, -w * 0.55 + sp.hd[0] * s, -h + sp.hd[1] * s, sp.hd[2] * s);",
    "if (sp.hd && DECO.cur) decoAt(-w * 0.55 + sp.hd[0] * s, -h + sp.hd[1] * s, sp.hd[2] * s);")
rep("function drawDeco(k, x, y, hw) { // DECO_V30\n  const c = ctx; c.save(); c.lineJoin = 'round'; c.lineWidth = Math.max(1, hw * 0.05); c.strokeStyle = 'rgba(60,30,50,.85)';",
"""const DS = { x: 0, y: 0, w: 0, t: -1 }; // DECO_V39: 프레임마다 튀는 머리 위치를 부드럽게
function decoAt(x, y, w) {
  const fresh = G.t - DS.t > 0.3; DS.t = G.t; const a = fresh ? 1 : 0.4;
  DS.x += (x - DS.x) * a; DS.y += (y - DS.y) * a; DS.w += (Math.min(w, 46) - DS.w) * (fresh ? 1 : 0.15);
  drawDeco(DECO.cur, DS.x, DS.y, DS.w);
}
function drawDeco(k, x, y, hw) { // DECO_V30
  const c = ctx; c.save(); c.lineJoin = 'round'; c.lineCap = 'round'; c.lineWidth = Math.max(0.8, hw * 0.035); c.strokeStyle = 'rgba(38,28,44,.9)';
  c.shadowColor = 'rgba(30,18,40,.38)'; c.shadowBlur = hw * 0.07; c.shadowOffsetY = hw * 0.04; // 털 위에 얹힌 그림자""")
rep("c.strokeStyle = 'rgba(60,30,50,.85)'; c.lineWidth = Math.max(1, hw * 0.05);\n    rr(c, x - rw * 1.04",
    "c.strokeStyle = 'rgba(38,28,44,.9)'; c.lineWidth = Math.max(0.8, hw * 0.035);\n    rr(c, x - rw * 1.04")
# 가방: 등 위 작은 가방 + 어깨끈 하나로 단순하게
rep("const bx = x - hw * 1.0, by = y + hw * 0.5,", "const bx = x - hw * 0.82, by = y + hw * 0.62,")
rep("c.strokeStyle = 'rgba(60,30,50,.85)'; c.lineWidth = Math.max(1, hw * 0.05);\n    c.save(); c.translate(bx, by + bob); c.rotate(-0.18);",
    "c.strokeStyle = 'rgba(38,28,44,.9)'; c.lineWidth = Math.max(0.8, hw * 0.035);\n    c.save(); c.translate(bx, by + bob); c.rotate(-0.18); c.scale(0.85, 0.85);")
P.write_text(s, encoding='utf-8'); print('ok')
# (수동 적용) 털모자 by 0.2→0.32, 산타 모자 by 0.2→0.3 : 머리에 눌러쓴 느낌
