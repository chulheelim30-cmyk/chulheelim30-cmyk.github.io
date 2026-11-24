#!/usr/bin/env python3
"""풍년이의 모험 v29: 점프 = 슈퍼맨 대시 포즈(g_boost), 피버 = 빠른 달리기, 꿀잠 깨우는 왕년이가 풍년이를 가리지 않게. 맨 마지막에 적용"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'POSE_V29' in s: print('already'); sys.exit(0)
R = [
 ("else if (!PL.ground) f = PL.jumps >= 2 && PL.vy < 300 ? 'g_roll' : PL.vy < 120 ? 'g_jump' : 'g_leap';",
  "else if (!PL.ground) f = PL.jumps >= 2 && PL.vy < -250 ? 'g_roll' : PL.vy < 420 ? 'g_boost' : 'g_leap'; // POSE_V29 점프 = 슈퍼맨 대시"),
 ("else if (G.fever > 0 && G.state === 'play') f = 'g_boost'; else f = IMG.g_r0 && IMG.g_r0.complete ? 'g_r' + (Math.floor(PL.anim * 1.5) % 8)",
  "else f = IMG.g_r0 && IMG.g_r0.complete ? 'g_r' + (Math.floor(PL.anim * (G.fever > 0 ? 2.2 : 1.5)) % 8)"),
]
for a, b in R:
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
i = s.index("  if (G.nap > 0) { // 꿀잠: 동생이 달려와 톡톡"); j = s.index("    return;\n  }\n  G.napSaid = false;", i)
s = s[:i] + "  if (G.nap > 0) { // 꿀잠: 동생이 앞쪽에서 달려와 톡톡 (JUMP 버튼·풍년이에 안 가리게 오른쪽에서, 왼쪽을 보고)\n    const e = (G.napT0 || 1.8) - G.nap, arrive = Math.min(1, e / 0.6), x = SX() + 330 - arrive * 200, key = arrive < 1 ? 'w_run' + (Math.floor(G.t * 10) % 2) : 'w_wake', h = arrive < 1 ? 78 : 66;\n    if (arrive >= 1 && !G.napSaid) { G.napSaid = true; pop(PX() + 130, GY - 110, '형, 일어나…', '#ffffff', 16); }\n    const im = IMG[key]; if (im && im.complete && im.naturalWidth) { const w = im.naturalWidth * h / im.naturalHeight; ctx.save(); ctx.translate(x, GY + 4 - (arrive >= 1 ? Math.abs(Math.sin(G.t * 9)) * 3 : 0)); ctx.scale(-1, 1); ctx.drawImage(im, -w / 2, -h, w, h); ctx.restore(); }\n" + s[j:]
P.write_text(s, encoding='utf-8'); print('ok')
