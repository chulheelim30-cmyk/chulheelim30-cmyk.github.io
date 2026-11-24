#!/usr/bin/env python3
"""풍년이의 모험 v30: 꾸미기 자연스럽게(머리 장식이 달릴 때 살랑, 점프 땐 뒤로 젖힘, 조금 크게 · 가방은 등 위로) + 피버 더 빠르게. 맨 마지막에 적용"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'DECO_V30' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("(fv ? 1.25 : 1) * G.restK;", "(fv ? 1.5 : 1) * G.restK;")
rep("Math.floor(PL.anim * (G.fever > 0 ? 2.2 : 1.5)) % 8)", "Math.floor(PL.anim * (G.fever > 0 ? 2.6 : 1.5)) % 8)")
rep("function drawDeco(k, x, y, hw) {\n  const c = ctx; c.save(); c.lineJoin = 'round'; c.lineWidth = Math.max(1, hw * 0.05); c.strokeStyle = 'rgba(60,30,50,.85)';\n",
    """function drawDeco(k, x, y, hw) { // DECO_V30
  const c = ctx; c.save(); c.lineJoin = 'round'; c.lineWidth = Math.max(1, hw * 0.05); c.strokeStyle = 'rgba(60,30,50,.85)';
  if (['bow', 'beanie', 'flower', 'crown', 'santa', 'raincoat', 'band', 'glasses'].includes(k)) { // 머리 장식: 달릴 때 살랑, 점프 땐 바람에 살짝 뒤로, 조금 크게
    const sw = G.state === 'play' ? (PL.ground ? Math.sin(PL.anim * 3.1) * 0.05 : -0.1 - Math.min(0.08, Math.max(-0.08, PL.vy / 9000))) : Math.sin(G.t * 2) * 0.03, px = x, py = y + hw * 0.55;
    c.translate(px, py); c.rotate(sw); c.scale(1.15, 1.15); c.translate(-px, -py);
  }
""")
rep("const cw = hw * 0.5, cy = y + hw * 0.06, ch = hw * 0.34;", "const cw = hw * 0.66, cy = y + hw * 0.08, ch = hw * 0.44;")
i = s.index("  } else if (k === 'backpack') {"); j = s.index("  } else if (k === 'crown') {", i)
s = s[:i] + """  } else if (k === 'backpack') { // 등 위에 얹은 소풍 가방 + 가슴 끈
    const bx = x - hw * 1.0, by = y + hw * 0.5, bob = PL.ground ? Math.sin(PL.anim * 3.1) * hw * 0.03 : -hw * 0.04;
    c.strokeStyle = '#2f7a44'; c.lineWidth = hw * 0.07; c.beginPath(); c.moveTo(bx + hw * 0.25, by + hw * 0.15 + bob); c.quadraticCurveTo(x - hw * 0.35, y + hw * 0.95, x - hw * 0.1, y + hw * 1.0); c.stroke();
    c.strokeStyle = 'rgba(60,30,50,.85)'; c.lineWidth = Math.max(1, hw * 0.05);
    c.save(); c.translate(bx, by + bob); c.rotate(-0.18);
    rr(c, -hw * 0.3, -hw * 0.28, hw * 0.6, hw * 0.46, hw * 0.16); c.fillStyle = '#4fb36a'; c.fill(); c.stroke();
    c.beginPath(); c.moveTo(-hw * 0.3, -hw * 0.1); c.quadraticCurveTo(0, hw * 0.06, hw * 0.3, -hw * 0.1); c.lineTo(hw * 0.3, -hw * 0.16); c.quadraticCurveTo(0, -hw * 0.38, -hw * 0.3, -hw * 0.16); c.closePath(); c.fillStyle = '#7fd48f'; c.fill(); c.stroke();
    c.fillStyle = '#ffd23f'; c.beginPath(); c.arc(0, -hw * 0.02, hw * 0.05, 0, 7); c.fill();
    c.fillStyle = 'rgba(255,255,255,.4)'; c.beginPath(); c.ellipse(-hw * 0.14, -hw * 0.2, hw * 0.08, hw * 0.03, -0.3, 0, 7); c.fill();
    c.restore();
""" + s[j:]
P.write_text(s, encoding='utf-8'); print('ok')
