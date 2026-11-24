#!/usr/bin/env python3
"""풍년이의 모험 v26: 보스 5종(너굴 대장 추가)·동네 5곳(강 다리) · 5보스마다 한 장(1~3장) 스토리 · 15보스 최종 엔딩 · 진행은 판이 끝나도 저장(pa2_prog)
순서: pung_fun_v23 → pung_opening_v23 → pung_story_v25 → 이 파일"""
import sys, pathlib
D = pathlib.Path(__file__).resolve().parent
P = D.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'function storyChapter' in s: print('already'); sys.exit(0)
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)
# 진행도·동네
rep("  { n: '밤 산책길', tint: 'rgba(16,8,50,.38)' },\n];\nconst zoneI = () => (G.bossWin || 0) % ZONES.length;",
    "  { n: '밤 산책길', tint: 'rgba(16,8,50,.38)' },\n  { n: '강 다리', tint: 'rgba(90,150,210,.14)' },\n];\n/* 11-24 v26 진행도: 이야기 속 보스 순번(0~14)은 판이 끝나도 저장 */\nconst progN = () => (+(localStorage.getItem('pa2_prog') || 0)) % 15;\nconst bIdx = () => (G.p0 | 0) + (G.bossWin | 0);\nconst CH = ['집을 나서요', '별을 따라서', '다시, 호수공원'];\nconst zoneI = () => bIdx() % ZONES.length;")
rep("cush: permL('cushion'), wang: 0,", "cush: permL('cushion'), p0: progN(), wang: 0,")
rep("const roof = zoneI() === 2;", "const roof = zoneI() === 2 || zoneI() === 4;")
rep("if (z === 3) pick.push(['bat', 2.8]);", "if (z === 3) pick.push(['bat', 2.8]); if (z === 4) pick.push(['tcone', 2.6]);")
rep("    case 'chimney': objs.push(", "    case 'tcone': objs.push({ t: 'tcone', x: x + 90 }); snackArc(x + 20, 140, 130); return 290;\n    case 'chimney': objs.push(")
rep("    case 'bolt': return { x0: o.x - 12,", "    case 'tcone': return { x0: o.x - 15, x1: o.x + 15, y0: GY - 42, y1: GY };\n    case 'wave': return { x0: o.x - 16, x1: o.x + 16, y0: GY - 26, y1: GY };\n    case 'bolt': return { x0: o.x - 12,")
rep("    if (o.t === 'bolt') o.x += o.vx * dt;", "    if (o.t === 'bolt' || o.t === 'wave') o.x += o.vx * dt;")
rep("      case 'bolt': drawBolt(x, o.y); break;", "      case 'bolt': drawBolt(x, o.y); break;\n      case 'tcone': put(ART.tcone(), x, GY + 4); break;\n      case 'wave': drawWave(x); break;")
rep("bat: 1, bolt: 1 };", "bat: 1, bolt: 1, tcone: 1, wave: 1 };")
# 보스 5종
rep("const BOSS_ORDER = ['crow', 'goose', 'robot', 'owl'];", "BOSSES.raccoon = { n: '너굴 대장', sub: '쿵! 땅 물결은 점프로 · 쓰레기통에 머리가 끼면 콩!', story: '쓰레기통에서 꺼내 줬더니 고마워했어요', win: '너굴 대장이 웃었어요!', hp: 24, col: ['#e8dcd4', '#6e625c'] };\nconst BOSS_ORDER = ['crow', 'goose', 'robot', 'owl', 'raccoon'];")
rep("const HOME_X = { crow: 0.74, goose: 0.8, robot: 0.76, owl: 0.8 };", "const HOME_X = { crow: 0.74, goose: 0.8, robot: 0.76, owl: 0.8, raccoon: 0.78 };")
rep("const homeY = B => B.kind === 'goose' ? GY :", "const homeY = B => B.kind === 'goose' || B.kind === 'raccoon' ? GY :")
rep("const bossCY = B => B.kind === 'goose' ? B.y - 60 :", "const bossCY = B => B.kind === 'raccoon' ? B.y - 50 : B.kind === 'goose' ? B.y - 60 :")
rep("const kind = BOSS_ORDER[(G.bossWin || 0) % 4], D = BOSSES[kind], lv = 1 + Math.floor((G.bossWin || 0) / 4), hp = D.hp + (lv - 1) * 10;",
    "const idx = bIdx(), kind = BOSS_ORDER[idx % 5], D = BOSSES[kind], lv = 1 + Math.floor((idx % 15) / 5) + Math.min(2, meetN()), hp = D.hp + (lv - 1) * 6;")
rep("  if (B.kind === 'owl') return B.ph === 'walk'", "  if (B.kind === 'raccoon') return { x0: B.x - 34, x1: B.x + 34, y0: B.y - 104, y1: B.y };\n  if (B.kind === 'owl') return B.ph === 'walk'")
rep("  }\n  B.x = G.cam + B.sx;\n  bossTouch(B);", """  } else if (B.kind === 'raccoon') {
    if (B.ph === 'idle') { B.sx += (hx - B.sx) * Math.min(1, dt * 3); B.y = GY; B.cd -= dt; if (B.cd <= 0) { B.n++; B.ph = 'leap'; B.vy = -1050; sfx('jump'); } }
    else if (B.ph === 'leap') { B.vy += 2200 * dt; B.y += B.vy * dt; if (B.y >= GY && B.vy > 0) { B.y = GY; G.shake = 3; burst(G.cam + B.sx, GY, 12, 'puff', ['#fff'], 180); sfx('hurt');
      if (B.n % 3 === 0) { B.ph = 'stuck'; B.pt = 0.6; pop(G.cam + B.sx, GY - 120, '앗! 쓰레기통에 머리가 꼈어요', '#ffe3a0', 17); }
      else { const n = hard ? 2 : 1; for (let i = 0; i < n; i++) objs.push({ t: 'wave', x: G.cam + B.sx - 50 + i * 160, vx: -240, hp: 1 }); B.ph = 'idle'; B.cd = Math.max(0.8, 1.5 - B.lv * 0.12) + Math.random() * 0.5; } } }
    else if (B.ph === 'stuck') { B.pt -= dt; if (B.pt <= 0) { B.ph = 'slide'; B.stomp = true; } }
    else if (B.ph === 'slide') { B.sx -= (320 + B.lv * 30) * dt; if (B.sx < -120) { B.ph = 'back'; B.stomp = false; B.sx = LW + 120; } }
    else if (B.ph === 'back') { B.sx -= 320 * dt; if (B.sx <= hx) { B.ph = 'idle'; B.cd = 1.2; } }
    else if (B.ph === 'retreat') { B.sx += 560 * dt; if (B.sx >= hx) { B.sx = hx; B.ph = 'idle'; B.cd = 1.4; } }
  }
  B.x = G.cam + B.sx;
  bossTouch(B);""")
rep("objs.forEach(o => { if (o.t === 'cone' || o.t === 'bolt') o.gone = true; }); buls = [];", "objs.forEach(o => { if (o.t === 'cone' || o.t === 'bolt' || o.t === 'wave') o.gone = true; }); buls = [];")
rep("else drawOwl(x, y, B, a);", "else if (B.kind === 'owl') drawOwl(x, y, B, a);\n  else drawRaccoon(x, y, B, a);")
rep("  if (B.kind === 'robot' && B.ph === 'roll') text(", "  if (B.kind === 'raccoon' && B.ph === 'slide') text('지금! 밟아요', B.x - G.cam, GY - 140, 20, 'center', '#fff3a0');\n  if (B.kind === 'robot' && B.ph === 'roll') text(")
# 장 끝 → 스토리, 15보스 → 최종 엔딩
rep("G.stage++; G.pieces = 0; const fin = G.bossWin % 4 === 0; setTimeout(() => { if (G.state !== 'play' || G.demo) return; if (fin) storyEnding(); else startRest(G.stage - 1, ''); }, fin ? 2400 : 3200);",
    "G.stage++; G.pieces = 0; const P = bIdx() % 15; localStorage.setItem('pa2_prog', P); const ch = P % 5 === 0 ? (P === 0 ? 3 : P / 5) : 0; setTimeout(() => { if (G.state !== 'play' || G.demo) return; if (ch === 3) storyEnding(); else if (ch) storyChapter(ch); else startRest(G.stage - 1, ''); }, ch ? 2400 : 3200);")
# HUD·시작·처음 화면
rep("text(`${ZONES[zoneI()].n} · 스테이지 ${G.stage} · ${m > 0 ?", "const P = bIdx() % 15; text(`${Math.floor(P / 5) + 1}장 보스 ${P % 5}/5 · ${ZONES[zoneI()].n} · ${m > 0 ?")
rep("reset(false); G.state = 'play';", "reset(false); G.state = 'play'; { const P = G.p0 | 0, c = Math.floor(P / 5); G.banner = 2.4; G.bannerTxt = `${c + 1}장 · ${CH[c]}`; G.bannerSub = `이번 장 보스 ${P % 5}/5 · 최종 엔딩까지 보스 ${15 - P}`; }")
rep("{ const m = meetN(), d = document.querySelector('.home .desc'); if (m > 0 && d) d.textContent += ` · 벌써 ${m}번 만났어요`; }",
    "{ const m = meetN(), P = progN(), d = document.querySelector('.home .desc'), t = []; if (P || m) t.push(`${Math.floor(P / 5) + 1}장 ${P % 5}/5`); if (m) t.push(`벌써 ${m}번 만났어요`); if (t.length && d) d.textContent += ' · ' + t.join(' · '); }")
rep("opText(g, `— ${ordOf(meetN() + 1)} 만남 —`,", "opText(g, `— ${ordOf(meetN() + 1)} 만남 · ${Math.floor(progN() / 5) + 1}장 —`,")
rep("{ k: 'band', name: '투쟁 머리띠', icon: '🎌', bk: 4 },", "{ k: 'band', name: '투쟁 머리띠', icon: '🎌', bk: 5 },")
rep("d.bk ? '보스 4종 친구' :", "d.bk ? '보스 5종 친구' :")
# 장면 종류 추가
rep("  } else if (S.k === 'love') {", """  } else if (S.k === 'card') {
    opCover(g, IMG[S.bg], 0.4 + p * 0.2, 0.6, 1.15 + p * 0.05); g.fillStyle = 'rgba(20,10,40,.15)'; g.fillRect(0, 0, W, H);
    (S.chars || []).forEach(([k, cx, hh, fl], j) => opImg(g, k, W * cx, H * 0.9 - Math.abs(Math.sin(OP.t * 3 + j)) * 3, H * hh, fl));
  } else if (S.k === 'chapter') {
    g.fillStyle = '#1a1030'; g.fillRect(0, 0, W, H); opText(g, S.cap, W / 2, H * 0.42, Math.min(52, W * 0.075), '#ffe27a', p * 3); opText(g, S.sub, W / 2, H * 0.42 + Math.min(56, W * 0.08), fs * 0.8, '#fff', p * 3 - 1);
  } else if (S.k === 'love') {""")
rep("if ((S.k === 'home' || S.k === 'run' || S.k === 'arrive') && S.cap)", "if ((S.k === 'home' || S.k === 'run' || S.k === 'arrive' || S.k === 'card') && S.cap)")
rep("function storyEnding() {", r"""function chapterScenes(ch) {
  return ch === 1 ? [
    { d: 3.6, k: 'card', bg: 'bg_snow', chars: [['c_daze', 0.38, 0.36], ['w_scare', 0.66, 0.34]], cap: '뒤에서 누가 따라오는데…?', sub: '…왕년이?!' },
    { d: 3.8, k: 'card', bg: 'bg_spring', chars: [['c_yay', 0.38, 0.36], ['w_run1', 0.64, 0.28]], cap: '"혼자 있으면 무섭잖아…"', sub: '왕년이랑 같이 가기로 했어요' },
    { d: 3.2, k: 'chapter', cap: '2장 · 별을 따라서', sub: '1장 끝! 다음 보스 다섯은 조금 더 세요' },
  ] : [
    { d: 3.8, k: 'card', bg: 'bg_night', chars: [['o_goose', 0.18, 0.22, true], ['c_wave', 0.42, 0.36], ['w_run0', 0.68, 0.24]], cap: '친구가 된 보스들이 모였어요', sub: '"호수공원은 저쪽이야!"' },
    { d: 3.6, k: 'card', bg: 'bg_night', chars: [['c_doze', 0.4, 0.34], ['w_sleep', 0.66, 0.24]], cap: '오늘 밤은 여기서 한숨 자고', sub: '내일은 꼭 도착할 거예요' },
    { d: 3.2, k: 'chapter', cap: '3장 · 다시, 호수공원', sub: '마지막 보스 다섯을 넘으면 그날을 만나요' },
  ];
}
function storyChapter(ch) {
  G.state = 'story'; slideHeld = false;
  opOpen(false, chapterScenes(ch), 'chap', () => { G.state = 'play'; PL.hurt = 1.5; startRest(G.stage - 1, ''); G.banner = 2.6; G.bannerTxt = `${ch + 1}장 · ${CH[ch]}`; G.bannerSub = `최종 엔딩까지 보스 ${15 - ch * 5}`; });
}
function storyEnding() {""")
rep("G.bannerSub = '친구들과 한 바퀴 더 달려요 · 보스가 조금 더 세져요'; });", "G.bannerSub = '다시 1장부터 · 친구들과 한 바퀴 더 (보스가 조금 더 세져요)'; });")
# 그림: 너굴 대장·땅 물결·고깔
rep("ART.bike = () =>", r"""function drawRaccoon(x, y, B, a) { // 너굴 대장: y = 바닥
  const stuck = B.ph === 'stuck' || B.ph === 'slide' || B.ph === 'retreat';
  ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = 'rgba(30,20,50,.25)'; ctx.beginPath(); ctx.ellipse(x, GY + 3, 40 * (B.ph === 'leap' ? Math.max(0.4, 1 - (GY - y) / 300) : 1), 7, 0, 0, 7); ctx.fill();
  ctx.translate(x, y); if (B.ph === 'slide') ctx.rotate(Math.sin(G.t * 20) * 0.06);
  ctx.save(); ctx.translate(30, -30); ctx.rotate(-0.6 + Math.sin(G.t * 4) * 0.15); for (let i = 3; i >= 0; i--) { ctx.beginPath(); ctx.ellipse(0, -i * 12, 11 - i, 8, 0, 0, 7); ctx.fillStyle = i % 2 ? '#3a3238' : '#9a8a84'; ctx.fill(); } ctx.restore();
  ctx.beginPath(); ctx.ellipse(0, -34, 36, 32, 0, 0, 7); ctx.fillStyle = lg(ctx, -66, 0, ['#a8988f', '#6e625c']); ctx.fill(); stroke(ctx, 2.2, '#2a2024');
  ctx.beginPath(); ctx.ellipse(0, -26, 22, 20, 0, 0, 7); ctx.fillStyle = '#e0d4cc'; ctx.fill();
  ctx.fillStyle = '#3a3238'; ctx.beginPath(); ctx.ellipse(-16, -3, 9, 5, 0, 0, 7); ctx.ellipse(16, -3, 9, 5, 0, 0, 7); ctx.fill();
  if (stuck) {
    rr(ctx, -26, -100, 52, 46, 6); ctx.fillStyle = lg(ctx, -100, -54, ['#8fb8a0', '#4a7a5e']); ctx.fill(); stroke(ctx, 2, '#1a3a2a'); ctx.fillStyle = '#3a6a4e'; ctx.fillRect(-30, -104, 60, 8);
    ctx.strokeStyle = 'rgba(20,50,30,.5)'; ctx.lineWidth = 2; for (let i = -1; i <= 1; i++) { ctx.beginPath(); ctx.moveTo(i * 12, -92); ctx.lineTo(i * 12, -60); ctx.stroke(); }
  } else {
    ctx.fillStyle = '#8a7a74'; ctx.beginPath(); ctx.moveTo(-30, -82); ctx.lineTo(-26, -102); ctx.lineTo(-12, -90); ctx.moveTo(8, -92); ctx.lineTo(20, -104); ctx.lineTo(22, -84); ctx.fill(); stroke(ctx, 1.8, '#2a2024');
    ctx.beginPath(); ctx.ellipse(-4, -72, 28, 24, 0, 0, 7); ctx.fillStyle = '#a8988f'; ctx.fill(); stroke(ctx, 2.2, '#2a2024');
    ctx.beginPath(); ctx.ellipse(-6, -74, 25, 9, 0, 0, 7); ctx.fillStyle = '#2a2024'; ctx.fill();
    [-15, 3].forEach(ex => { ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(ex, -75, 4.5, 0, 7); ctx.fill(); ctx.fillStyle = '#1a1014'; ctx.beginPath(); ctx.arc(ex - 1, -75, 2.2, 0, 7); ctx.fill(); });
    ctx.beginPath(); ctx.ellipse(-8, -60, 11, 7, 0, 0, 7); ctx.fillStyle = '#e8dcd4'; ctx.fill(); ctx.fillStyle = '#1a1014'; ctx.beginPath(); ctx.arc(-10, -63, 3.5, 0, 7); ctx.fill();
    ctx.save(); ctx.translate(26, -46); ctx.rotate(-0.5); rr(ctx, -4, -14, 8, 26, 3); ctx.fillStyle = '#ff9a3a'; ctx.fill(); stroke(ctx, 1.4, '#7a3a10'); ctx.restore();
  }
  ctx.restore();
}
function drawWave(x) { // 땅 물결
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = rg(ctx, x, GY - 10, 2, 30, ['rgba(160,220,255,.7)', 'rgba(160,220,255,0)']); ctx.fillRect(x - 30, GY - 40, 60, 44); ctx.restore();
  ctx.beginPath(); ctx.moveTo(x - 18, GY); ctx.quadraticCurveTo(x - 10, GY - 30, x + 4, GY - 26); ctx.quadraticCurveTo(x + 16, GY - 22, x + 18, GY); ctx.closePath(); ctx.fillStyle = lg(ctx, GY - 30, GY, ['#f0fbff', '#8ad0f0']); ctx.fill(); stroke(ctx, 1.6, '#2a6a9a');
}
ART.tcone = () => sprite('tcone', 36, 44, 18, 44, g => { // 강 다리: 고깔
  g.beginPath(); g.moveTo(18, 2); g.lineTo(30, 38); g.lineTo(6, 38); g.closePath(); g.fillStyle = '#ff6a2a'; g.fill(); stroke(g, 1.8, '#7a2a0a');
  g.fillStyle = '#fff'; g.beginPath(); g.moveTo(13, 17); g.lineTo(23, 17); g.lineTo(25, 23); g.lineTo(11, 23); g.closePath(); g.fill(); g.beginPath(); g.moveTo(9, 29); g.lineTo(27, 29); g.lineTo(28, 33); g.lineTo(8, 33); g.closePath(); g.fill();
  rr(g, 1, 37, 34, 6, 2); g.fillStyle = '#e0501a'; g.fill(); stroke(g, 1.6, '#7a2a0a');
});
ART.bike = () =>""")
P.write_text(s, encoding='utf-8'); print('ok')
