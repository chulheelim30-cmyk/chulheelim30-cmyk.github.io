/* 11-24 이야기: 송도의 밤 → 호수공원까지 달려가 '처음 만난 날'을 다시 만남. 보스 4종을 다 친구로 만들면 엔딩 → 만남 횟수 +1 → 다음 오프닝은 'N번째 만남' */
const OP = { on: false, t: 0, cv: null, g: null, W: 0, H: 0, raf: 0, music: null, last: 0, sc: [], T: 0, done: null, kind: 'op' };
const ORD = ['첫', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열'];
const meetN = () => +(localStorage.getItem('pa2_meet') || 0);
const ordOf = n => (n <= 10 ? ORD[n - 1] : n) + ' 번째';
const beatK = () => { try { return JSON.parse(localStorage.getItem('pa2_bk') || '[]'); } catch (e) { return []; } };
function opLine(m) { return m === 0 ? '호수공원까지, 달려 볼까요?' : m === 1 ? '또 만났네. 몇 번이라도 고를 거야.' : m === 2 ? '행복은 같은 날을 또 사는 거래.' : m < 6 ? '오늘도 호수공원에서 만나요.' : '언제나, 여기서 만나요.'; }
function opScenes() {
  return [
    { d: 4.0, k: 'home', cap: '송도의 밤, 풍년이 귀가 쫑긋', sub: '창밖 별 하나가 서쪽을 가리켜요' },
    { d: 5.2, k: 'run', cap: '멀어도 괜찮아', sub: '길은 기억하고 있으니까' },
    { d: 3.4, k: 'arrive', img: 'bg_sunset', cap: '노을 진 일산호수공원', sub: '' },
    { d: 3.8, k: 'pic', img: 'dp0', cap: '그날, 작은 회색 고양이가', sub: '우리 가족을 골랐어요' },
    { d: 4.6, k: 'title', img: 'bg_sunset' },
  ];
}
function endScenes(m) {
  return [
    { d: 3.2, k: 'arrive', img: 'bg_sunset', cap: '호수공원이 보여요!', sub: '' },
    { d: 3.8, k: 'pic', img: 'dp0', cap: '벤치 앞에서 누가 불렀어요', sub: '"풍년아!"' },
    { d: 5.0, k: 'love', cap: `${ordOf(m)} 만남`, sub: '몇 번이라도, 여기서 다시 만나요' },
  ];
}
//__HELPERS__
function opImg(g, key, x, yb, h, flip) { const im = IMG[key]; if (!im || !im.complete || !im.naturalWidth) return 0; const w = im.naturalWidth * h / im.naturalHeight; g.save(); g.translate(x, yb); if (flip) g.scale(-1, 1); g.drawImage(im, -w / 2, -h, w, h); g.restore(); return w; }
function opScene(g, i, p, alpha) {
  const S = OP.sc[i], W = OP.W, H = OP.H, ease = x => x * x * (3 - 2 * x), fs = Math.min(32, W * 0.042);
  g.save(); g.globalAlpha = alpha;
  if (S.k === 'home') { // 송도 집 창가: 창밖 밤하늘 + 창틀 + 두 고양이
    opCover(g, IMG.bg_night, 0.3 + p * 0.1, 0.25, 1.15);
    const sx = W * 0.3, sy = H * 0.22, tw = 1 + Math.sin(OP.t * 5) * 0.3; g.save(); g.globalCompositeOperation = 'lighter'; g.fillStyle = `rgba(255,240,170,${0.5 * tw})`; g.beginPath(); g.arc(sx, sy, 26 * tw, 0, 7); g.fill(); g.restore(); g.fillStyle = '#fffbe0'; g.beginPath(); g.arc(sx, sy, 5, 0, 7); g.fill();
    g.fillStyle = '#efe6dc'; g.fillRect(0, 0, W * 0.08, H); g.fillRect(W * 0.92, 0, W * 0.08, H); g.fillRect(W * 0.49, 0, W * 0.02, H * 0.72); g.fillRect(0, 0, W, H * 0.06);
    g.fillStyle = '#d8ccbe'; g.fillRect(0, H * 0.72, W, H * 0.28); g.fillStyle = '#c4b4a2'; g.fillRect(0, H * 0.72, W, H * 0.025);
    opImg(g, 'w_sleep', W * 0.7, H * 0.9, H * 0.24); // 왕년이는 쿨쿨
    const up = p > 0.35; opImg(g, up ? 'c_wave' : 'c_doze', W * 0.36, H * 0.92, H * 0.36);
    if (up) opText(g, '!', W * 0.36 + H * 0.12, H * 0.5, fs * 1.4, '#ffe27a', (p - 0.35) * 5);
  } else if (S.k === 'run') { // 달리기 몽타주: 배경이 밤 → 눈 → 벚꽃 → 노을로
    const BG = ['bg_night', 'bg_snow', 'bg_spring', 'bg_sunset'], f = p * BG.length, bi = Math.min(BG.length - 1, Math.floor(f)), fr = f - bi;
    opCover(g, IMG[BG[bi]], (OP.t * 0.25) % 1, 0.6, 1.3);
    if (bi < BG.length - 1 && fr > 0.75) { g.save(); g.globalAlpha = alpha * (fr - 0.75) * 4; opCover(g, IMG[BG[bi + 1]], 0, 0.6, 1.3); g.restore(); }
    g.strokeStyle = 'rgba(255,255,255,.35)'; g.lineWidth = 2; for (let k = 0; k < 10; k++) { const y = H * (0.25 + (k * 0.071) % 0.6), x = ((k * 211 - OP.t * 900) % (W + 200) + W + 200) % (W + 200) - 100; g.beginPath(); g.moveTo(x, y); g.lineTo(x + 60 + k * 6, y); g.stroke(); }
    const gy = H * 0.86, fi = Math.floor(OP.t * 12) % 8, bob = Math.abs(Math.sin(OP.t * 12)) * 6;
    const bk = beatK(); if (bk.includes('crow')) opImg(g, 'o_crow', W * 0.62 + Math.sin(OP.t * 2) * 20, H * 0.32, H * 0.14, true);
    if (bk.includes('goose')) opImg(g, 'o_goose', W * 0.18, gy - bob * 0.5, H * 0.16, true);
    if (p > 0.3) opImg(g, 'w_run' + (Math.floor(OP.t * 8) % 2), W * (0.08 + Math.min(0.17, (p - 0.3) * 0.5)), gy - bob, H * 0.22); // 겁쟁이 형도 몰래 따라와요
    opImg(g, 'g_r' + fi, W * 0.5, gy - bob, H * 0.3);
    if (p > 0.3 && p < 0.7) opText(g, '(왕년이도 몰래 따라왔어요)', W * 0.25, gy - H * 0.27, fs * 0.6, '#e8e0ff', Math.min(1, (p - 0.3) * 6, (0.7 - p) * 6));
  } else if (S.k === 'arrive' || S.k === 'title') {
    opCover(g, IMG.bg_sunset, S.k === 'title' ? 0.5 - p * 0.15 : 0.35 + p * 0.25, 0.6, S.k === 'title' ? 1.25 : 1.12 + p * 0.1);
    if (S.k === 'arrive') { const x = W * (0.1 + 0.32 * ease(Math.min(1, p * 1.4))); opImg(g, p < 0.7 ? 'g_r' + (Math.floor(OP.t * 10) % 8) : 'c_wave', x, H * 0.9, H * (p < 0.7 ? 0.28 : 0.34)); }
    else {
      g.fillStyle = 'rgba(30,10,40,.18)'; g.fillRect(0, 0, W, H);
      const x = -W * 0.2 + (W * 0.7) * Math.min(1, ease(Math.min(1, p * 1.6))), gy = H * 0.88, bob = Math.abs(Math.sin(OP.t * 12)) * 6;
      opImg(g, 'w_run' + (Math.floor(OP.t * 8) % 2), x - H * 0.36, gy - bob, H * 0.22); opImg(g, 'g_r' + (Math.floor(OP.t * 12) % 8), x, gy - bob, H * 0.3);
      const k = Math.max(0, (p - 0.28) / 0.3), s = 1 + (1 - Math.min(1, k)) * 0.4;
      if (k > 0) { g.save(); g.translate(W / 2, H * 0.27); g.scale(s, s); opText(g, '풍년이의 모험', 0, 0, Math.min(64, W * 0.09), '#ffe27a', k); g.restore(); opText(g, `— ${ordOf(meetN() + 1)} 만남 —`, W / 2, H * 0.27 + Math.min(48, W * 0.068), Math.min(20, W * 0.032), '#fff', k); }
      opText(g, opLine(meetN()), W / 2, H * 0.47, Math.min(24, W * 0.04), '#fff', (p - 0.55) * 4);
    }
  } else if (S.k === 'love') { // 엔딩: 가족 품의 풍년이 + 상자째 따라온 왕년이
    opCover(g, IMG.bg_sunset, 0.5, 0.6, 1.2 + p * 0.05); g.fillStyle = `rgba(255,200,220,${0.12 + 0.08 * Math.sin(OP.t * 2)})`; g.fillRect(0, 0, W, H);
    for (let k = 0; k < 14; k++) { const hx = W * (0.15 + (k * 0.137) % 0.7), hy = H - ((OP.t * (40 + k * 7) + k * 60) % (H * 1.1)); opText(g, '♥', hx, hy, 14 + (k % 4) * 6, '#ff9ac0', 0.7); }
    opImg(g, 'c_love', W * 0.4, H * 0.92, H * 0.42); opImg(g, 'w_box', W * 0.66, H * 0.92, H * 0.28);
    opText(g, S.cap, W / 2, H * 0.2, Math.min(44, W * 0.06), '#ffe27a', p * 3); opText(g, S.sub, W / 2, H * 0.2 + Math.min(46, W * 0.064), fs * 0.85, '#fff', p * 3 - 0.8);
  } else { // 그림일기 한 장 + 흐린 배경
    opCover(g, IMG.bg_sunset, 0.5, 0.5, 1.3); g.fillStyle = 'rgba(30,14,40,.45)'; g.fillRect(0, 0, W, H);
    const im = IMG[S.img], side = Math.min(H * 0.62, W * 0.42), z = 1 + p * 0.06, x = W * 0.3, y = H * 0.5 + (1 - ease(Math.min(1, p * 3))) * 30;
    g.save(); g.translate(x, y); g.rotate(-0.04); g.scale(z, z);
    g.fillStyle = '#fffaf0'; g.shadowColor = 'rgba(0,0,0,.45)'; g.shadowBlur = 24; g.fillRect(-side / 2 - 12, -side / 2 - 12, side + 24, side + 52); g.shadowBlur = 0;
    if (im && im.complete) g.drawImage(im, -side / 2, -side / 2, side, side);
    g.restore();
    const n1 = Math.floor(Math.max(0, p - 0.12) * 40), n2 = Math.floor(Math.max(0, p - 0.4) * 40), tx = W * 0.56;
    opText(g, S.cap.slice(0, n1), tx, H * 0.44, fs, '#fff', 1, 'left'); opText(g, S.sub.slice(0, n2), tx, H * 0.44 + fs * 1.5, fs, '#ffe27a', 1, 'left');
  }
  if ((S.k === 'home' || S.k === 'run' || S.k === 'arrive') && S.cap) { const y = H * 0.2; opText(g, S.cap, W / 2, y, fs, '#fff', p * 3 - 0.3); if (S.sub) opText(g, S.sub, W / 2, y + fs * 1.4, fs * 0.85, '#ffe27a', p * 3 - 1); }
  g.restore();
}
function opFrame(now) {
  if (!OP.on) return; const dt = Math.min(0.05, (now - OP.last) / 1000 || 0); OP.last = now; OP.t += dt;
  const g = OP.g, W = OP.W, H = OP.H, SC = OP.sc; g.fillStyle = '#140c24'; g.fillRect(0, 0, W, H);
  let t0 = 0, i = 0; while (i < SC.length - 1 && OP.t > t0 + SC[i].d) { t0 += SC[i].d; i++; }
  const p = Math.min(1, (OP.t - t0) / SC[i].d), XF = 0.7;
  if (i > 0 && OP.t - t0 < XF) opScene(g, i - 1, 1, 1);
  opScene(g, i, p, i > 0 ? Math.min(1, (OP.t - t0) / XF) : Math.min(1, OP.t / 0.8));
  for (let k = 0; k < 18; k++) { const sx = ((k * 151 + OP.t * (20 + k * 3)) % (W + 40)) - 20, sy = H - ((k * 97 + OP.t * (30 + k * 2)) % H); g.fillStyle = `rgba(255,230,170,${0.25 + 0.2 * Math.sin(OP.t * 2 + k)})`; g.beginPath(); g.arc(sx, sy, 1.5 + (k % 3), 0, 7); g.fill(); }
  const bar = H * 0.07 * Math.min(1, OP.t * 2); g.fillStyle = '#000'; g.fillRect(0, 0, W, bar); g.fillRect(0, H - bar, W, bar);
  if (OP.t > OP.T - 0.8) { const k = Math.min(1, (OP.t - (OP.T - 0.8)) / 0.8); g.fillStyle = OP.kind === 'end' ? `rgba(255,252,240,${k})` : `rgba(20,12,36,${k})`; g.fillRect(0, 0, W, H); }
  if (OP.t >= OP.T) return opEnd();
  OP.raf = requestAnimationFrame(opFrame);
}
function opStart() {
  if (OP.on) return; OP.on = true; OP.t = 0; OP.last = performance.now(); $('op').hidden = false; $('op-tap').hidden = true; opSize(); opMusic();
  OP.raf = requestAnimationFrame(opFrame);
}
function opEnd() {
  if (!OP.on && $('op').hidden) return; OP.on = false; cancelAnimationFrame(OP.raf);
  if (OP.music) { try { OP.music.gain.setTargetAtTime(0.0001, AC.currentTime, 0.15); const m = OP.music; setTimeout(() => { try { m.disconnect(); } catch (e) {} }, 600); } catch (e) {} OP.music = null; }
  $('op').hidden = true; const done = OP.done; OP.done = null;
  if (OP.kind === 'op') { localStorage.setItem('pa2_op', '1'); setTimeout(() => { try { PungRank.entryInvite('pungadventure', { host: wrap, onlyIf: () => !$('home').hidden && $('op').hidden }); } catch (e) {} }, 400); }
  if (done) try { done(); } catch (e) {}
}
function opOpen(autoTap, sc, kind, done) { // 첫 실행: '눌러서 시작' 카드 (소리를 켜려면 한 번 눌러야 해서)
  OP.sc = sc || opScenes(); OP.T = OP.sc.reduce((a, s) => a + s.d, 0); OP.kind = kind || 'op'; OP.done = done || null;
  OP.cv = $('op-cv'); OP.g = OP.cv.getContext('2d'); $('op').hidden = false; opSize();
  if (autoTap) { $('op-tap').hidden = false; const g = OP.g; g.fillStyle = '#140c24'; g.fillRect(0, 0, OP.W, OP.H); opCover(g, IMG.bg_sunset, 0.5, 0.55, 1.1); g.fillStyle = 'rgba(20,12,36,.45)'; g.fillRect(0, 0, OP.W, OP.H); }
  else opStart();
}
function storyEnding() { // 보스 4종을 다 친구로 만들면: 호수공원 도착 → 만남 횟수 +1 → 계속 달리기
  const m = meetN() + 1; localStorage.setItem('pa2_meet', m); G.state = 'story'; slideHeld = false;
  opOpen(false, endScenes(m), 'end', () => { G.state = 'play'; PL.hurt = 1.5; startRest(G.stage - 1, ''); G.banner = 2.8; G.bannerTxt = `${ordOf(m)} 만남!`; G.bannerSub = '친구들과 한 바퀴 더 달려요 · 보스가 조금 더 세져요'; });
}
/* ---------- 왕년이: 겁 많은 형 (상자 아이템) ---------- */
const WANG_T = 10;
function getWang(o) { G.wang = WANG_T; G.wangOut = 0; G.banner = 1.9; G.bannerTxt = '겁쟁이 형 왕년이 등장!'; G.bannerSub = '한 번 부딪혀도 왕년이가 대신 놀라 줘요'; sfx('big'); vib(20); burst(o.x, o.y, 20, 'spark', ['#fff', '#ddd', '#ffe27a'], 260); }
function wangHurt() { if (!(G.wang > 0) || G.boss) return false; G.wang = 0; G.wangOut = 1.4; PL.hurt = 1.2; vib(25); sfx('hit'); pop(PX() - 90, PL.y - 120, '으악!! 왕년이가 대신 놀랐어요', '#ffffff', 18); burst(SX() - 90, GY - 50, 18, 'puff', ['#fff'], 200); return true; }
function stepWang(dt) { if (G.wang > 0 && !(G.boss && G.boss.hp > 0)) { G.wang -= dt; if (G.wang <= 0) { G.wang = 0; G.wangOut = 0.01; pop(PX() - 90, GY - 140, '나… 먼저 갈게…', '#e8e0ff', 15); } } if (G.wangOut > 0) G.wangOut += dt; if (G.wangOut > 2.2) G.wangOut = 0; }
function drawWang() {
  if (!(G.wang > 0) && !(G.wangOut > 0)) return; const hide = G.boss && G.boss.hp > 0;
  let x = SX() - 104, yb = GY + 4, key, h;
  if (G.wangOut > 0) { if (G.wangOut < 1.1) { key = 'w_scare'; h = 92; x -= G.wangOut * 10; } else { key = 'w_run' + (Math.floor(G.t * 10) % 2); h = 78; x -= (G.wangOut - 1.1) * 520; } }
  else if (hide) { key = 'w_box'; h = 70; if (G.boss.hit > 0 && Math.random() < 0.2) pop(PX() - 92, GY - 70, '덜덜', '#e8e0ff', 12); }
  else if (!PL.ground) { key = 'w_jump'; h = 98; yb = Math.min(GY + 4, PL.y + 26); }
  else { key = 'w_run' + (Math.floor(PL.anim * 0.8) % 2); h = 80; yb -= Math.abs(Math.sin(PL.anim * 2.5)) * 3; }
  const im = IMG[key]; if (!im || !im.complete || !im.naturalWidth) return; const w = im.naturalWidth * h / im.naturalHeight;
  ctx.fillStyle = 'rgba(30,20,50,.25)'; ctx.beginPath(); ctx.ellipse(x, GY + 3, w * 0.35, 5, 0, 0, 7); ctx.fill();
  if (G.wang > 0 && G.wang < 2 && Math.floor(G.t * 8) % 2) return;
  ctx.drawImage(im, x - w / 2, yb - h, w, h);
}
ART.wbox = () => imgArt('w_box', 52, 40, 0.5, 0.5) || ART.yarn();
