#!/usr/bin/env python3
"""풍년이의 모험 v31: 보스 5종 그림 교체(제미나이 10칸, 평소/약해진 모습) + 오프닝·장면에도 사용. 맨 마지막에 적용"""
import sys, pathlib
D = pathlib.Path(__file__).resolve().parent
P = D.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'drawBossImg' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
i = s.index('Object.assign(SPR,{"w_wake"'); j = s.index('</script>', i) + 9
s = s[:j] + '\n<script>Object.assign(SPR,' + (D / 'pung_boss_spr.json').read_text() + ');</script>' + s[j:]
rep("""  if (B.kind === 'crow') {
    if (B.hp > 0) put(ART.sack(), x + 6, y + 70, { rot: Math.sin(G.t * 3) * 0.25, s: 1.1 });""", """  const okImg = drawBossImg(x, y, B, a);
  if (okImg) {} else if (B.kind === 'crow') {
    if (B.hp > 0) put(ART.sack(), x + 6, y + 70, { rot: Math.sin(G.t * 3) * 0.25, s: 1.1 });""")
rep("  if (B.hp > 0 && B.kind === 'crow') { // 심술 표시", "  if (!okImg && B.hp > 0 && B.kind === 'crow') { // 심술 표시")
rep("function drawGooseB(x, y, B, a) {", r"""function bimg(key, x, y, h, o = {}) { const im = IMG[key]; if (!im || !im.complete || !im.naturalWidth) return false; const w = im.naturalWidth * h / im.naturalHeight; ctx.save(); ctx.translate(x, y); if (o.rot) ctx.rotate(o.rot); if (o.a != null) ctx.globalAlpha = o.a; ctx.drawImage(im, -w / 2, o.bottom ? -h : -h / 2, w, h); ctx.restore(); return true; }
function drawBossImg(x, y, B, a) { // 11-24 제미나이 보스 그림 (윗줄 평소 · 아랫줄 약해진 모습). 그림이 없으면 예전 코드 그림
  const k = B.kind, ph = B.ph, low = B.hp > 0 && B.hp < B.max * 0.3;
  const shadow = (w) => { ctx.fillStyle = 'rgba(30,20,50,.28)'; ctx.beginPath(); ctx.ellipse(x, GY + 3, w, 8, 0, 0, 7); ctx.fill(); };
  if (k === 'crow') return bimg(low ? 'b_crow2' : 'b_crow', x, y, 150, { rot: B.throw > 0 ? -0.18 : Math.sin(G.t * 2) * 0.05, a });
  if (k === 'goose') { const run = ph === 'atk'; shadow(52); if (ph === 'warn' && Math.floor(G.t * 10) % 2) text('!', x, y - 150, 40, 'center', '#ff4a5a'); return bimg(run ? 'b_goose2' : 'b_goose', x, y + 4 - (run ? Math.abs(Math.sin(G.t * 18)) * 4 : 0), run ? 118 : 135, { bottom: true, a, rot: run ? -0.05 : Math.sin(G.t * 3) * 0.03 }); }
  if (k === 'robot') { const hot = ph === 'fall' || ph === 'roll' || ph === 'retreat'; if (ph === 'roll') shadow(40); return bimg(hot ? 'b_robot2' : 'b_robot', x, y - 46, 108, { a, rot: ph === 'roll' ? -G.t * 14 : B.throw > 0 ? -0.12 : Math.sin(G.t * 2) * 0.06 }); }
  if (k === 'owl') { const sit = ph === 'walk' || ph === 'land'; if (sit) shadow(40); return bimg(sit ? 'b_owl2' : 'b_owl', x, sit ? y + 36 : y, sit ? 88 : 100, { bottom: sit, a, rot: ph === 'atk' ? -0.3 : Math.sin(G.t * 2) * 0.05 }); }
  if (k === 'raccoon') { const st = ph === 'stuck' || ph === 'slide' || ph === 'retreat'; shadow(44); return bimg(st ? 'b_rac2' : 'b_rac', x, y + 4, st ? 104 : 116, { bottom: true, a, rot: ph === 'slide' ? Math.sin(G.t * 20) * 0.06 : 0 }); }
  return false;
}
function drawGooseB(x, y, B, a) {""")
# 오프닝·장면: 친구들도 새 그림으로
rep("opImg(g, 'o_crow', W * 0.62 + Math.sin(OP.t * 2) * 20, H * 0.32, H * 0.14, true);", "opImg(g, 'b_crow', W * 0.62 + Math.sin(OP.t * 2) * 20, H * 0.36, H * 0.16, true);")
rep("opImg(g, 'o_goose', W * 0.18, gy - bob * 0.5, H * 0.16, true);", "opImg(g, 'b_goose2', W * 0.2, gy - bob * 0.5, H * 0.2, true);")
rep("['o_goose', 0.18, 0.22, true], ['c_wave', 0.42, 0.36], ['w_run0', 0.68, 0.24]]", "['b_goose', 0.12, 0.26, true], ['b_rac', 0.26, 0.24, true], ['c_wave', 0.46, 0.36], ['w_run0', 0.7, 0.24], ['b_robot', 0.88, 0.2]]")
rep("opImg(g, 'c_love', W * 0.38, H * 0.92, H * 0.42); opImg(g, 'w_nuzzle', W * 0.64, H * 0.92, H * 0.34);",
    "[['b_crow', 0.1, 0.62, 0.13, true], ['b_goose', 0.16, 0.86, 0.17, true], ['b_robot', 0.86, 0.6, 0.12], ['b_owl', 0.9, 0.36, 0.13], ['b_rac', 0.84, 0.86, 0.16]].forEach(([k2, fx, fy, fh, fl]) => { g.save(); g.globalAlpha = alpha * 0.85; opImg(g, k2, W * fx, H * fy, H * fh, fl); g.restore(); }); // 멀리서 지켜보는 다섯 친구\n    opImg(g, 'c_love', W * 0.38, H * 0.92, H * 0.42); opImg(g, 'w_nuzzle', W * 0.64, H * 0.92, H * 0.34);")
P.write_text(s, encoding='utf-8'); print('ok')
