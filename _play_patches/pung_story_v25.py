#!/usr/bin/env python3
"""풍년이의 모험 v25: 이야기(집 창가→호수공원, N번째 만남 엔딩) + 왕년이(겁쟁이 형) + 투쟁 머리띠
순서: pung_fun_v23.py → pung_opening_v23.py → 이 파일. 왕년이 그림은 pung_wang_spr.json"""
import sys, pathlib, json
D = pathlib.Path(__file__).resolve().parent
P = D.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'function storyEnding' in s: print('already'); sys.exit(0)
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:70]); s = s.replace(a, b)
# 1) 왕년이 그림
i = s.index('Object.assign(SPR,{"dp0"'); j = s.index('</script>', i) + 9
s = s[:j] + '\n<script>Object.assign(SPR,' + (D / 'pung_wang_spr.json').read_text() + ');</script>' + s[j:]
# 2) 오프닝 블록 교체
a = s.index('/* 11-24 오프닝'); b = s.index("$('op-tap').addEventListener")
old = s[a:b]
helpers = old[old.index('function opSize'):old.index('function opScene')]
music = old[old.index('function opMusic'):old.index('function opStart')].replace('OP_T', 'OP.T')
blk = (D / 'pung_story_v25.js').read_text(encoding='utf-8').replace('//__HELPERS__\n', helpers + music)
s = s[:a] + blk + s[b:]
rep("$('op-btn').addEventListener('click', () => opOpen(false));", "$('op-btn').addEventListener('click', () => opOpen(false));\n{ const m = meetN(), d = document.querySelector('.home .desc'); if (m > 0 && d) d.textContent += ` · 벌써 ${m}번 만났어요`; }")
# 3) 게임 연결
rep("if (G.state === 'pick') { updFx(dt * 0.3); return; }", "if (G.state === 'pick' || G.state === 'story') { updFx(dt * 0.3); return; }")
rep("G.stage++; G.pieces = 0; setTimeout(() => { if (G.state === 'play' && !G.demo) startRest(G.stage - 1, ''); }, 3200);",
    "G.stage++; G.pieces = 0; const fin = G.bossWin % 4 === 0; setTimeout(() => { if (G.state !== 'play' || G.demo) return; if (fin) storyEnding(); else startRest(G.stage - 1, ''); }, fin ? 2400 : 3200);")
rep("  if (x > nextPiece) {", "  if (!(G.wang > 0) && !(G.wangOut > 0) && G.stage >= 2 && Math.random() < 0.05) { objs.push({ t: 'wbox', x: x + 90, y: GY - 70 }); snackLine(x, 4, GY - 30); return 240; }\n  if (x > nextPiece) {")
rep("if (o.t === 'snack' || o.t === 'piece' || o.t === 'heart' || o.t === 'yarn') {", "if (o.t === 'snack' || o.t === 'piece' || o.t === 'heart' || o.t === 'yarn' || o.t === 'wbox') {")
rep("  else if (o.t === 'yarn') getYarn(o);", "  else if (o.t === 'yarn') getYarn(o);\n  else if (o.t === 'wbox') getWang(o);")
rep("      case 'sign': put(ART.sign(), x, GY + 4); break;",
    "      case 'sign': { put(ART.sign(), x, GY + 4); const im = IMG.w_sleep; if (!(G.wang > 0) && im && im.complete && im.naturalWidth) { const h = 46, w = im.naturalWidth * h / im.naturalHeight; ctx.drawImage(im, x + 46, GY + 6 - h, w, h); if (Math.random() < 0.02) pops.push({ x: o.x + 80, y: GY - 50, txt: 'z', col: '#e8e0ff', size: 14, life: 1.2 }); } break; }\n      case 'wbox': ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = `rgba(255,255,255,${0.25 + 0.12 * Math.sin(G.t * 6)})`; ctx.beginPath(); ctx.arc(x, o.y, 34, 0, 7); ctx.fill(); ctx.restore(); put(ART.wbox(), x, o.y + Math.sin(G.t * 4) * 4, { rot: Math.sin(G.t * 3) * 0.1, s: 1.1 }); break;")
rep("drawBoss(); drawCat();", "drawBoss(); drawWang(); drawCat();")
rep("  if (!G.demo) stepX(dt);\n", "  if (!G.demo) { stepX(dt); stepWang(dt); }\n")
rep("  G.combo = 0; G.nmT = 0;\n", "  G.combo = 0; G.nmT = 0;\n  if (wangHurt()) return;\n")
rep("cush: permL('cushion'),", "cush: permL('cushion'), wang: 0, wangOut: 0,")
# 4) 보스 친구 대사
for k, line in [('crow', '츄르를 반 나눠 줬더니 웃었어요'), ('goose', '"수고 많으세요~" 인사에 꽥장군도 웃었어요'), ('robot', '집 가는 길을 알려 줬어요'), ('owl', '"진짜 가고 싶구나" 별자리 길을 열어 줬어요')]:
    a = s.index(f"  {k}: {{ n: "); b2 = s.index("win: ", a); s = s[:b2] + f"story: '{line}', " + s[b2:]
rep("  sfx('big'); feverJingle(); vib([40, 40, 80]); burst(B.x, bossCY(B), 60,", "  pop(B.x, bossCY(B) - 90, D.story, '#fff3c8', 17); sfx('big'); feverJingle(); vib([40, 40, 80]); burst(B.x, bossCY(B), 60,")
# 5) 투쟁 머리띠
rep("  { k: 'backpack', name: '소풍 가방', icon: '🎒', days: 7 },\n", "  { k: 'backpack', name: '소풍 가방', icon: '🎒', days: 7 },\n  { k: 'band', name: '투쟁 머리띠', icon: '🎌', bk: 4 },\n")
rep("const decoOpen = d => d.days ?", "const decoOpen = d => d.bk ? beatK().length >= d.bk : d.days ?")
rep("d.days ? `발도장 ${d.days}개` :", "d.bk ? '보스 4종 친구' : d.days ? `발도장 ${d.days}개` :")
rep("function drawDeco(k, x, y, hw) {\n  const c = ctx; c.save(); c.lineJoin = 'round'; c.lineWidth = Math.max(1, hw * 0.05); c.strokeStyle = 'rgba(60,30,50,.85)';\n",
    "function drawDeco(k, x, y, hw) {\n  const c = ctx; c.save(); c.lineJoin = 'round'; c.lineWidth = Math.max(1, hw * 0.05); c.strokeStyle = 'rgba(60,30,50,.85)';\n  if (k === 'band') { const bw = hw * 1.02, bh = hw * 0.2, bx = x - bw / 2 + hw * 0.04, by = y + hw * 0.16; c.translate(bx + bw / 2, by + bh / 2); c.rotate(-0.06); rr(c, -bw / 2, -bh / 2, bw, bh, bh * 0.3); c.fillStyle = '#c8322a'; c.fill(); c.stroke(); c.fillStyle = '#fff'; c.font = `${Math.round(bh * 0.72)}px Jua, sans-serif`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText('투쟁결의단결', 0, bh * 0.04); c.restore(); return; }\n")
P.write_text(s, encoding='utf-8'); print('ok')
