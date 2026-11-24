/* 11-24 보스 4종: 3스테이지마다 번갈아 — 큰까마귀(털실공) → 꽥장군(돌진·밟기) → 빙글이 로봇(공 피하기·과열 밟기) → 부엉 할매(어둠 급강하·내려앉으면 밟기) */
const BOSS_EVERY = 3;
const BOSSES = {
  crow: { n: '심술 큰까마귀', sub: '간식을 몽땅 훔쳐 갔어요 · 털실공 친구와 혼내 주세요', win: '큰까마귀랑 친구가 됐어요!', hp: 24, col: ['#c9a8ff', '#7a4ad8'] },
  goose: { n: '꽥장군', sub: '돌진해 와요 · 점프해서 머리를 콩! 밟아 주세요', win: '꽥장군이 항복했어요!', hp: 24, col: ['#ffe08a', '#e08a1a'] },
  robot: { n: '빙글이 로봇', sub: '낮은 공은 점프, 높은 공은 슬라이드 · 과열되면 콩!', win: '빙글이가 착해졌어요!', hp: 22, col: ['#9ee8ff', '#2a8ac8'] },
  owl: { n: '부엉 할매', sub: '어둠 속 급강하! 빨간 줄 높이를 보고 피하세요', win: '부엉 할매가 웃었어요!', hp: 22, col: ['#ffc09a', '#b8562a'] },
};
const BOSS_ORDER = ['crow', 'goose', 'robot', 'owl'];
const NM = { bin: 1, pot: 1, branch: 1, crow: 1, goose: 1, cone: 1, bike: 1, chimney: 1, bat: 1, bolt: 1 };
const HOME_X = { crow: 0.74, goose: 0.8, robot: 0.76, owl: 0.8 };
const homeY = B => B.kind === 'goose' ? GY : B.kind === 'robot' ? GY - 168 + Math.sin(B.t * 2) * 14 : B.kind === 'owl' ? GY - 226 + Math.sin(B.t * 1.8) * 10 : GY - 196 + Math.sin(B.t * 1.6) * 28;
const bossCY = B => B.kind === 'goose' ? B.y - 60 : B.kind === 'robot' ? B.y - 36 : B.y;
function startBoss() {
  const kind = BOSS_ORDER[(G.bossWin || 0) % 4], D = BOSSES[kind], lv = 1 + Math.floor((G.bossWin || 0) / 4), hp = D.hp + (lv - 1) * 10;
  G.boss = { kind, sx: LW + 200, x: G.cam + LW + 200, y: GY - 200, hp, max: hp, in: 0, t: 0, cd: 1.8, hit: 0, lv, out: 0, throw: 0, ph: 'idle', pt: 0, n: 0, stomp: false };
  G.boss.y = homeY(G.boss);
  G.banner = 2.8; G.bannerTxt = D.n + ' 등장!'; G.bannerSub = D.sub;
  sfx('fever'); vib([30, 30, 60]); objs.forEach(o => { if (['piece', 'crow', 'goose', 'bat', 'bike', 'chimney'].includes(o.t)) o.gone = true; });
  objs.push({ t: 'yarn', x: PX() + 520, y: GY - 110 });
}
function placeBoss(x) {
  const r = Math.random(), k = G.boss.kind;
  if (G.yarn < 2 && !objs.some(o => o.t === 'yarn' && !o.gone) && r < 0.6) { objs.push({ t: 'yarn', x: x + 90, y: GY - 110 }); snackLine(x, 3); return 240; }
  if (k !== 'crow' || r < 0.8) { snackLine(x, 5, GY - 30 - (Math.random() < 0.4 ? 80 : 0)); return 250; }
  objs.push({ t: Math.random() < 0.5 ? 'pot' : 'puddle', x: x + 80 }); snackArc(x + 10, 140, 120); return 290;
}
function bossBox(B) {
  if (B.kind === 'goose') return { x0: B.x - 38, x1: B.x + 34, y0: B.y - 96, y1: B.y };
  if (B.kind === 'robot') return { x0: B.x - 32, x1: B.x + 32, y0: B.y - 68, y1: B.y };
  if (B.kind === 'owl') return B.ph === 'walk' ? { x0: B.x - 28, x1: B.x + 28, y0: B.y - 34, y1: B.y + 34 } : { x0: B.x - 28, x1: B.x + 28, y0: B.y - 13, y1: B.y + 13 };
  return null;
}
function bossTouch(B) {
  if (G.state !== 'play' || B.hp <= 0) return; if (!(B.stomp || (B.kind === 'owl' && B.ph === 'atk'))) return;
  const box = bossBox(B), pb = { x0: PX() - 28, x1: PX() + 30, y0: PL.y - (PL.slide ? 36 : 60), y1: PL.y - 4 };
  if (!(pb.x1 > box.x0 && pb.x0 < box.x1 && pb.y1 > box.y0 && pb.y0 < box.y1)) return;
  if (B.stomp && PL.vy > 0 && pb.y1 < box.y0 + 30) return stomp(B);
  if (G.fever > 0) return; hurt();
}
function stomp(B) {
  const dmg = 6; B.hp -= dmg; B.hit = 0.3; B.stomp = false; B.ph = 'retreat';
  PL.vy = -980; PL.jumps = 1; PL.ground = false; PL.sq = 0.75; G.shake = 2.5; G.bonus += 200; addGauge(12);
  pop(B.x, bossCY(B) - 50, '콩! +200', '#ffe27a', 26); burst(B.x, bossCY(B) - 30, 22, 'spark', FX, 320); burst(B.x, bossCY(B) - 30, 8, 'puff', ['#fff'], 160); sfx('kill'); vib([20, 20, 40]);
  if (B.hp <= 0) bossWin();
}
function stepBoss(dt) {
  const B = G.boss; B.t += dt; B.hit = Math.max(0, B.hit - dt); B.throw = Math.max(0, B.throw - dt);
  const hx = LW * HOME_X[B.kind];
  if (B.hp <= 0) { B.out += dt; B.sx = Math.max(B.sx, hx) + B.out * B.out * 30; B.y += (GY - 200 - B.out * 50 - B.y) * Math.min(1, dt * 3); B.x = G.cam + B.sx; if (Math.random() < dt * 5) pops.push({ x: B.x + rnd(-30, 30), y: B.y - 30, txt: '♥', col: '#ff9ac0', size: 18 + Math.random() * 10, life: 1.2 }); if (B.out > 3.2) G.boss = null; return; }
  if (B.in < 1) { B.in = Math.min(1, B.in + dt * 0.7); B.sx = hx + (1 - B.in) * 300; B.y = homeY(B); B.x = G.cam + B.sx; return; }
  if (G.nap > 0) { B.x = G.cam + B.sx; return; }
  const hard = B.lv >= 2 || B.hp < B.max * 0.4;
  if (B.kind === 'crow') {
    B.sx = hx; B.y = homeY(B); B.cd -= dt;
    if (B.cd <= 0) {
      B.cd = Math.max(1.0, 2.1 - B.lv * 0.2) + Math.random() * 0.7; B.throw = 0.35; B.x = G.cam + B.sx;
      const n = hard && Math.random() < 0.45 ? 2 : 1;
      for (let i = 0; i < n; i++) { const T = 0.85, land = PX() + G.speed * (T + 0.75 + Math.random() * 0.5) + i * 170, vx = (land - B.x) / T, vy = (GY - B.y - 0.5 * 1400 * T * T) / T; objs.push({ t: 'cone', x: B.x - 30, y: B.y + 10, vx, vy, hp: 1 }); }
      sfx('jump2');
    }
  } else if (B.kind === 'goose') {
    if (B.ph === 'idle') { B.sx += (hx - B.sx) * Math.min(1, dt * 4); B.y = GY; B.cd -= dt; if (B.cd <= 0) { B.ph = 'warn'; B.pt = 0.8; sfx('hit'); vib(15); pop(G.cam + B.sx, GY - 120, '꽥!!', '#ff6a5a', 28); } }
    else if (B.ph === 'warn') { B.pt -= dt; B.sx = hx + Math.sin(B.t * 60) * 3; if (B.pt <= 0) { B.ph = 'atk'; B.stomp = true; } }
    else if (B.ph === 'atk') { B.sx -= (540 + B.lv * 60) * dt; if (Math.random() < dt * 20) parts.push({ x: G.cam + B.sx + 30, y: GY - 4, vx: 60, vy: -40, life: 0.5, max: 0.5, kind: 'puff', col: '#fff', size: 0.8, rot: 0, vr: 0, g: 0 }); if (B.sx < -140) { B.ph = 'back'; B.stomp = false; B.sx = LW + 150; } }
    else if (B.ph === 'back') { B.sx -= 320 * dt; if (B.sx <= hx) { B.ph = 'idle'; B.cd = (hard ? 0.7 : 1.4) + Math.random() * 0.6; } }
    else if (B.ph === 'retreat') { B.sx += 620 * dt; if (B.sx >= hx) { B.sx = hx; B.ph = 'idle'; B.cd = 1.6; } }
  } else if (B.kind === 'robot') {
    if (B.ph === 'idle') {
      B.sx += (hx - B.sx) * Math.min(1, dt * 3); B.y += (homeY(B) - B.y) * Math.min(1, dt * 4); B.cd -= dt;
      if (B.cd <= 0) {
        B.n++;
        if (B.n % 3 === 0) { B.ph = 'fall'; pop(G.cam + B.sx, B.y - 90, '과열! 삐-', '#ff6a5a', 22); sfx('hurt'); }
        else { const hi = Math.random() < 0.5, n = hard && Math.random() < 0.45 ? 2 : 1; for (let i = 0; i < n; i++) { const h2 = i ? !hi : hi; objs.push({ t: 'bolt', x: G.cam + B.sx - 40 + i * 170, y: h2 ? GY - 56 : GY - 18, vx: -230, hp: 1 }); } B.throw = 0.3; sfx('shot'); }
        B.cd = Math.max(0.9, 1.6 - B.lv * 0.15) + Math.random() * 0.5;
      }
    } else if (B.ph === 'fall') { B.y = Math.min(GY, B.y + 520 * dt); if (B.y >= GY) { B.ph = 'roll'; B.stomp = true; G.shake = 2; burst(G.cam + B.sx, GY, 10, 'puff', ['#fff'], 140); } }
    else if (B.ph === 'roll') { B.sx -= (300 + B.lv * 30) * dt; if (Math.random() < dt * 8) parts.push({ x: G.cam + B.sx, y: B.y - 70, vx: rnd(-20, 20), vy: -60, life: 0.9, max: 0.9, kind: 'puff', col: '#fff', size: 1, rot: 0, vr: 0, g: -20 }); if (B.sx < -120) { B.ph = 'back'; B.stomp = false; B.sx = LW + 130; B.y = GY - 168; } }
    else if (B.ph === 'back') { B.sx -= 320 * dt; B.y = homeY(B); if (B.sx <= hx) B.ph = 'idle'; }
    else if (B.ph === 'retreat') { B.sx += 560 * dt; B.y += (GY - 168 - B.y) * Math.min(1, dt * 3); if (B.sx >= hx) { B.sx = hx; B.ph = 'idle'; B.cd = 1.4; } }
  } else if (B.kind === 'owl') {
    if (B.ph === 'idle') {
      B.sx += (hx - B.sx) * Math.min(1, dt * 3); B.y += (homeY(B) - B.y) * Math.min(1, dt * 4); B.cd -= dt;
      if (B.cd <= 0) { B.n++; if (B.n % 2 === 0) { B.ph = 'land'; } else { B.ph = 'warn'; B.lane = Math.random() < 0.5 ? 'lo' : 'hi'; B.pt = hard ? 0.75 : 0.95; sfx('jump2'); } }
    } else if (B.ph === 'warn') { B.pt -= dt; if (B.pt <= 0) { B.ph = 'atk'; } }
    else if (B.ph === 'atk') { const ty = B.lane === 'lo' ? GY - 24 : GY - 66; B.sx -= (900 + B.lv * 60) * dt; B.y += (ty - B.y) * Math.min(1, dt * 12); if (B.sx < -120) { B.ph = 'back'; B.sx = LW + 120; B.y = GY - 226; B.cd = (hard ? 0.5 : 1.0) + Math.random() * 0.5; } }
    else if (B.ph === 'land') { B.y += (GY - 34 - B.y) * Math.min(1, dt * 5); if (B.y > GY - 40) { B.ph = 'walk'; B.stomp = true; pop(G.cam + B.sx, B.y - 70, '아이고 허리야~', '#ffd0b0', 18); } }
    else if (B.ph === 'walk') { B.sx -= 230 * dt; B.y = GY - 34 - Math.abs(Math.sin(B.t * 8)) * 4; if (B.sx < -110) { B.ph = 'back'; B.stomp = false; B.sx = LW + 120; B.y = GY - 226; B.cd = 1; } }
    else if (B.ph === 'back') { B.sx -= 320 * dt; B.y += (homeY(B) - B.y) * Math.min(1, dt * 4); if (B.sx <= hx) { B.ph = 'idle'; } }
    else if (B.ph === 'retreat') { B.sx += 520 * dt; B.y += (GY - 226 - B.y) * Math.min(1, dt * 3); if (B.sx >= hx) { B.sx = hx; B.ph = 'idle'; B.cd = 1.2; } }
  }
  B.x = G.cam + B.sx;
  bossTouch(B);
}
function bossHit() { const B = G.boss; B.hp--; B.hit = 0.12; sfx('hit'); G.bonus += 10; if (B.hp <= 0) bossWin(); }
function bossWin() {
  const B = G.boss, D = BOSSES[B.kind], bon = 3000 * B.lv; B.out = 0; B.stomp = false; G.bonus += bon; G.bossWin++;
  let beat = []; try { beat = JSON.parse(localStorage.getItem('pa2_bk') || '[]'); } catch (e) {}
  const first = !beat.includes(B.kind); if (first) { beat.push(B.kind); localStorage.setItem('pa2_bk', JSON.stringify(beat)); }
  addCoin(30 * B.lv + (first ? 100 : 0));
  G.banner = 3; G.bannerTxt = D.win; G.bannerSub = `보너스 +${bon}` + (first ? ' · 첫 승리 선물 🐟 간식 100개 (상점)' : ` · 상점 간식 +${30 * B.lv}`);
  sfx('big'); feverJingle(); vib([40, 40, 80]); burst(B.x, bossCY(B), 60, 'conf', FX, 520); burst(B.x, bossCY(B), 30, 'spark', FX, 380);
  objs.forEach(o => { if (o.t === 'cone' || o.t === 'bolt') o.gone = true; }); buls = [];
  for (let i = 0; i < 36; i++) objs.push({ t: 'snack', k: i % 9 === 4 ? 'sack' : SNACKS[i % 5], x: PX() + 260 + i * 30, y: GY - 36 - Math.abs(Math.sin(i * 0.45)) * 140 });
  G.stage++; G.pieces = 0; setTimeout(() => { if (G.state === 'play' && !G.demo) startRest(G.stage - 1, ''); }, 3200); localStorage.setItem('pa2_boss', +(localStorage.getItem('pa2_boss') || 0) + 1);
}
function drawBoss() {
  const B = G.boss; if (!B) return; const x = B.x - G.cam + (B.hit ? rnd(-3, 3) : 0), y = B.y, fl = Math.floor(G.t * (B.hp > 0 ? 6 : 10)) % 2, cy = bossCY(B);
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = rg(ctx, x, cy, 10, 110, [B.hp > 0 ? 'rgba(120,80,200,.24)' : 'rgba(255,170,220,.4)', 'rgba(0,0,0,0)']); ctx.fillRect(x - 120, cy - 120, 240, 240); ctx.restore();
  const a = B.hit > 0 ? 0.65 : 1;
  if (B.kind === 'crow') {
    if (B.hp > 0) put(ART.sack(), x + 6, y + 70, { rot: Math.sin(G.t * 3) * 0.25, s: 1.1 });
    const e = imgArt('o_crow', 176, 140, 0.5, 0.5, true, fl ? 0.9 : 0) || ART.crow(fl);
    put(e, x, y, { s: e.ww < 100 ? 2.5 : 1, rot: B.throw > 0 ? -0.18 : Math.sin(G.t * 2) * 0.05, a });
  } else if (B.kind === 'goose') drawGooseB(x, y, B, a);
  else if (B.kind === 'robot') drawRobot(x, y, B, a);
  else drawOwl(x, y, B, a);
  if (B.hp > 0 && B.kind === 'crow') { // 심술 표시
    const ax = x - 44, ay = cy - 62, s = 1 + Math.sin(G.t * 8) * 0.12; ctx.save(); ctx.translate(ax, ay); ctx.scale(s, s); ctx.strokeStyle = '#ff4a5a'; ctx.lineWidth = 3.2; ctx.lineCap = 'round';
    for (let i = 0; i < 4; i++) { ctx.rotate(Math.PI / 2); ctx.beginPath(); ctx.moveTo(3, -9); ctx.quadraticCurveTo(4, -4, 9, -3); ctx.stroke(); } ctx.restore();
  }
  if (B.ph === 'retreat' || (B.kind === 'robot' && (B.ph === 'fall' || B.ph === 'roll'))) for (let i = 0; i < 3; i++) { const q = G.t * 6 + i * 2.09; put(ART.star(), x + Math.cos(q) * 30, cy - 52 + Math.sin(q) * 7, { s: 0.6, rot: q }); }
}
function drawGooseB(x, y, B, a) { // 꽥장군: 큰 거위 + 장군 투구
  const s = 1.9, run = B.ph === 'atk', e = ART.goose(Math.floor(G.t * (run ? 14 : 5)) % 2);
  ctx.fillStyle = 'rgba(30,20,50,.28)'; ctx.beginPath(); ctx.ellipse(x, GY + 3, 50, 8, 0, 0, 7); ctx.fill();
  put(e, x, y + 2, { s, rot: run ? -0.1 + Math.sin(G.t * 30) * 0.05 : Math.sin(G.t * 3) * 0.03, a });
  const hx = x - 43, hy = y - 102 + (run ? 6 : 0); ctx.save(); ctx.translate(hx, hy); ctx.rotate(run ? -0.15 : 0);
  ctx.beginPath(); ctx.arc(0, 0, 15, Math.PI, 0); ctx.closePath(); ctx.fillStyle = lg(ctx, -15, 0, ['#ff6a5a', '#c22a2a']); ctx.fill(); stroke(ctx, 2, '#5a1010');
  ctx.fillStyle = '#ffd23f'; ctx.fillRect(-18, -2, 36, 5); ctx.strokeStyle = '#8a5a10'; ctx.lineWidth = 1.4; ctx.strokeRect(-18, -2, 36, 5);
  ctx.beginPath(); ctx.moveTo(0, -14); ctx.quadraticCurveTo(14, -34, 26, -24); ctx.quadraticCurveTo(12, -22, 4, -12); ctx.closePath(); ctx.fillStyle = '#ffd23f'; ctx.fill(); stroke(ctx, 1.4, '#8a5a10');
  ctx.restore();
  if (B.ph === 'warn' && Math.floor(G.t * 10) % 2) text('!', x, y - 140, 40, 'center', '#ff4a5a');
}
function drawRobot(x, y, B, a) { // 빙글이: y = 바닥
  const spin = B.ph === 'roll', hot = B.ph === 'fall' || spin || B.ph === 'retreat', cy = y - 36;
  ctx.save(); ctx.globalAlpha = a;
  if (!spin) { ctx.strokeStyle = '#2a3a5a'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, cy - 32); ctx.lineTo(x, cy - 46); ctx.stroke(); const w = 30 * Math.abs(Math.sin(G.t * (hot ? 6 : 30))); ctx.fillStyle = '#ff9ac0'; ctx.beginPath(); ctx.ellipse(x, cy - 48, w + 4, 5, 0, 0, 7); ctx.fill(); stroke(ctx, 1.6, '#7a2a5a'); }
  else { ctx.fillStyle = 'rgba(30,20,50,.28)'; ctx.beginPath(); ctx.ellipse(x, GY + 3, 38, 7, 0, 0, 7); ctx.fill(); }
  ctx.translate(x, cy); if (spin) ctx.rotate(-G.t * 14); else ctx.rotate(B.throw > 0 ? -0.12 : Math.sin(G.t * 2) * 0.06);
  rr(ctx, -34, -32, 68, 64, 18); ctx.fillStyle = lg(ctx, -32, 32, hot ? ['#ffe0d8', '#f0a08a', '#c05a4a'] : ['#eef8ff', '#a8cceb', '#5a86b0']); ctx.fill(); stroke(ctx, 2.6, '#2a3a5a');
  rr(ctx, -25, -21, 50, 30, 10); ctx.fillStyle = '#1a2440'; ctx.fill();
  if (hot) { ctx.strokeStyle = '#ff6a7a'; ctx.lineWidth = 3; [-11, 11].forEach(ex => { ctx.beginPath(); ctx.moveTo(ex - 5, -11); ctx.lineTo(ex + 5, -1); ctx.moveTo(ex + 5, -11); ctx.lineTo(ex - 5, -1); ctx.stroke(); }); }
  else { ctx.fillStyle = '#7ff0ff'; ctx.shadowColor = '#7ff0ff'; ctx.shadowBlur = 8; [-11, 11].forEach(ex => { ctx.beginPath(); ctx.ellipse(ex, -6, 5, 7 * (Math.floor(G.t * 3) % 7 ? 1 : 0.2), 0, 0, 7); ctx.fill(); }); ctx.shadowBlur = 0; }
  ctx.fillStyle = 'rgba(255,140,170,.55)'; ctx.beginPath(); ctx.ellipse(-26, 14, 5, 3, 0, 0, 7); ctx.ellipse(26, 14, 5, 3, 0, 0, 7); ctx.fill();
  ctx.fillStyle = '#ffd23f'; ctx.beginPath(); ctx.arc(0, 20, 5, 0, 7); ctx.fill(); stroke(ctx, 1.4, '#8a5a10');
  ctx.restore();
}
function drawOwl(x, y, B, a) { // 부엉 할매: y = 가운데
  const dive = B.ph === 'atk', flap = Math.sin(G.t * (dive ? 26 : B.ph === 'walk' ? 3 : 9));
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); if (dive) ctx.rotate(-0.3); const s = 0.95; ctx.scale(s, s);
  ctx.fillStyle = '#7a5236'; [-1, 1].forEach(d => { ctx.save(); ctx.scale(d, 1); ctx.rotate(dive ? 0.7 : flap * 0.45); ctx.beginPath(); ctx.ellipse(32, 0, 26, 12, 0.5, 0, 7); ctx.fill(); stroke(ctx, 2, '#3a2414'); ctx.restore(); });
  ctx.beginPath(); ctx.moveTo(-20, -28); ctx.lineTo(-26, -46); ctx.lineTo(-8, -32); ctx.moveTo(20, -28); ctx.lineTo(26, -46); ctx.lineTo(8, -32); ctx.fillStyle = '#7a5236'; ctx.fill(); stroke(ctx, 1.8, '#3a2414');
  ctx.beginPath(); ctx.ellipse(0, 4, 32, 36, 0, 0, 7); ctx.fillStyle = lg(ctx, -32, 40, ['#b98458', '#7a5236']); ctx.fill(); stroke(ctx, 2.2, '#3a2414');
  ctx.beginPath(); ctx.ellipse(0, 16, 19, 20, 0, 0, 7); ctx.fillStyle = '#f2dcb8'; ctx.fill();
  ctx.beginPath(); ctx.arc(0, -36, 9, 0, 7); ctx.fillStyle = '#e8e0ee'; ctx.fill(); stroke(ctx, 1.6, '#6a6070'); ctx.strokeStyle = '#d84a6a'; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(-10, -40); ctx.lineTo(10, -32); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(-30, -2); ctx.quadraticCurveTo(0, 18, 30, -2); ctx.lineTo(26, 8); ctx.quadraticCurveTo(0, 28, -26, 8); ctx.closePath(); ctx.fillStyle = '#b07ad8'; ctx.fill(); stroke(ctx, 1.6, '#5a2a7a');
  [-12, 12].forEach(ex => { ctx.beginPath(); ctx.arc(ex, -14, 10, 0, 7); ctx.fillStyle = '#fff8e0'; ctx.fill(); ctx.fillStyle = '#2a1a10'; ctx.beginPath(); ctx.arc(ex + (dive ? -3 : 0), -13, 5, 0, 7); ctx.fill(); ctx.strokeStyle = '#d8a83a'; ctx.lineWidth = 2.2; ctx.beginPath(); ctx.arc(ex, -14, 12, 0, 7); ctx.stroke(); });
  ctx.beginPath(); ctx.moveTo(-1, -14); ctx.lineTo(1, -14); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(-5, -4); ctx.lineTo(5, -4); ctx.lineTo(0, 4); ctx.closePath(); ctx.fillStyle = '#ffb02e'; ctx.fill(); stroke(ctx, 1.4, '#8a5a10');
  if (B.ph === 'walk') { ctx.fillStyle = '#ffb02e'; ctx.fillRect(-12, 36, 6, 6); ctx.fillRect(6, 36, 6, 6); }
  ctx.restore();
}
function drawBolt(x, y) {
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = rg(ctx, x, y, 2, 26, ['rgba(255,240,140,.85)', 'rgba(255,200,80,0)']); ctx.fillRect(x - 28, y - 28, 56, 56); ctx.restore();
  rr(ctx, x - 13, y - 8, 26, 16, 8); ctx.fillStyle = lg(ctx, y - 8, y + 8, ['#fffbe0', '#ffd23f', '#e08a1a']); ctx.fill(); stroke(ctx, 1.6, '#8a5a10');
  ctx.strokeStyle = 'rgba(255,230,140,.7)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x + 14, y); ctx.lineTo(x + 34, y); ctx.stroke();
}
function bossTop() { // 어둠·경고 (화면 위 레이어)
  const B = G.boss; if (!B || B.hp <= 0 || G.state === 'home') return;
  if (B.kind === 'owl') {
    const k = Math.min(1, B.in * 1.5);
    ctx.fillStyle = rg(ctx, SX(), PL.y - 40, 70, 300, ['rgba(8,4,30,0)', `rgba(8,4,30,${0.62 * k})`]); ctx.fillRect(0, 0, LW, LH);
    if (Math.random() < 0.3) parts.push({ x: G.cam + rnd(0, LW), y: rnd(GY - 240, GY - 20), vx: rnd(-20, 20), vy: rnd(-20, 10), life: 1.4, max: 1.4, kind: 'spark', col: '#d8ff8a', size: 0.35, rot: 0, vr: 1, g: 0 });
    const x = B.x - G.cam; ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = rg(ctx, x, B.y, 10, 70, ['rgba(255,200,150,.22)', 'rgba(255,200,150,0)']); ctx.fillRect(x - 70, B.y - 70, 140, 140); [-12, 12].forEach(ex => { ctx.fillStyle = rg(ctx, x + ex, B.y - 13, 1, 16, ['rgba(255,230,120,.95)', 'rgba(255,200,60,0)']); ctx.fillRect(x + ex - 16, B.y - 29, 32, 32); }); ctx.restore();
    if (B.ph === 'warn') {
      const ly = B.lane === 'lo' ? GY - 24 : GY - 66, bl = Math.floor(G.t * 10) % 2;
      ctx.save(); ctx.setLineDash([16, 10]); ctx.lineDashOffset = -G.t * 200; ctx.strokeStyle = bl ? 'rgba(255,70,90,.95)' : 'rgba(255,140,150,.6)'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(0, ly); ctx.lineTo(LW, ly); ctx.stroke(); ctx.restore();
      text(B.lane === 'lo' ? '점프!' : '숙여요! (슬라이드)', LW * 0.5, ly - 22, 22, 'center', '#ffd0d8');
    }
  }
  if (B.kind === 'goose' && B.ph === 'warn') { ctx.save(); ctx.setLineDash([14, 10]); ctx.lineDashOffset = G.t * 200; ctx.strokeStyle = 'rgba(255,70,90,.8)'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(B.x - G.cam - 60, GY - 30); ctx.lineTo(SX() + 40, GY - 30); ctx.stroke(); ctx.restore(); text('점프해서 콩!', SX() + 110, GY - 140, 20, 'center', '#fff3a0'); }
  if (B.kind === 'robot' && B.ph === 'roll') text('지금! 밟아요', B.x - G.cam, GY - 120, 20, 'center', '#fff3a0');
  if (B.kind === 'owl' && B.ph === 'walk') text('지금! 밟아요', B.x - G.cam, GY - 110, 20, 'center', '#fff3a0');
}
function zoneFx() {
  if (G.state === 'home' || G.demo) return; const Z = ZONES[zoneI()];
  if (Z.tint) { ctx.fillStyle = Z.tint; ctx.fillRect(0, 0, LW, LH); }
  if (zoneI() === 3 && Math.random() < 0.25) parts.push({ x: G.cam + rnd(0, LW * 1.2), y: rnd(GY - 200, GY - 20), vx: rnd(-30, 10), vy: rnd(-15, 15), life: 1.6, max: 1.6, kind: 'spark', col: '#d8ff8a', size: 0.32, rot: 0, vr: 1, g: 0 });
}
function nearMiss(o) {
  if (G.demo || G.fever > 0 || G.state !== 'play') return;
  G.combo = (G.nmT > 0 ? (G.combo | 0) : 0) + 1; G.nmT = 3.5; const c = Math.min(10, G.combo), pts = 20 * c; G.bonus += pts; addGauge(3);
  pop(PX() + 10, PL.y - 100, c > 1 ? `아슬아슬 ×${c}! +${pts}` : `아슬아슬! +${pts}`, c >= 5 ? '#ffe27a' : '#8af0ff', 17 + Math.min(9, c));
  if (c >= 3) { sfx('snack'); burst(SX() + 10, PL.y - 50, 4 + c, 'spark', ['#8af0ff', '#fff'], 150); }
}
function hudX() {
  if (!G.boss) { const m = BOSS_EVERY - ((G.stage - 1) % BOSS_EVERY) - 1; text(`${ZONES[zoneI()].n} · 스테이지 ${G.stage} · ${m > 0 ? `보스까지 별자리 ${m}개` : '곧 보스!'}`, LW - 16, 78, 14, 'right', '#ffe3f0'); }
  else if (G.boss.hp > 0) {
    const B = G.boss, D = BOSSES[B.kind], w = 220, x = LW / 2 - w / 2, y = 70; text(D.n + (B.lv > 1 ? ` Lv.${B.lv}` : ''), LW / 2, y - 2, 15, 'center', '#fff');
    rr(ctx, x, y + 8, w, 11, 5.5); ctx.fillStyle = 'rgba(30,20,60,.55)'; ctx.fill(); ctx.strokeStyle = 'rgba(255,255,255,.8)'; ctx.lineWidth = 1.3; ctx.stroke();
    rr(ctx, x + 1.5, y + 9.5, (w - 3) * Math.max(0, B.hp) / B.max, 8, 4); ctx.fillStyle = lg(ctx, y + 9, y + 18, D.col); ctx.fill();
  }
  if (G.combo > 1 && G.nmT > 0) text(`아슬아슬 콤보 ×${Math.min(10, G.combo)}`, LW - 16, 98, 14, 'right', '#8af0ff');
  if (G.yarn > 0) { put(ART.yarn(), 272, 57, { s: 0.65 }); text(Math.ceil(G.yarn) + '초', 286, 58, 14, 'left', '#ffd0ea'); }
}
ART.bike = () => sprite('bike', 72, 50, 36, 50, g => { // 시장 골목: 세워 둔 자전거
  g.lineWidth = 3.4; g.strokeStyle = '#2a2a3a'; [[14, 36], [58, 36]].forEach(([cx, cy]) => { g.beginPath(); g.arc(cx, cy, 12, 0, 7); g.stroke(); g.lineWidth = 1; g.beginPath(); g.moveTo(cx - 12, cy); g.lineTo(cx + 12, cy); g.moveTo(cx, cy - 12); g.lineTo(cx, cy + 12); g.stroke(); g.lineWidth = 3.4; });
  g.strokeStyle = '#e0484a'; g.lineWidth = 4; g.beginPath(); g.moveTo(14, 36); g.lineTo(30, 18); g.lineTo(50, 18); g.lineTo(58, 36); g.moveTo(30, 18); g.lineTo(36, 36); g.lineTo(50, 18); g.stroke();
  g.strokeStyle = '#2a2a3a'; g.lineWidth = 3; g.beginPath(); g.moveTo(50, 18); g.lineTo(52, 8); g.lineTo(60, 6); g.stroke(); g.fillStyle = '#4a3020'; rr(g, 24, 11, 14, 5, 2.5); g.fill();
  g.fillStyle = '#c8a060'; rr(g, 2, 8, 22, 14, 3); g.fill(); stroke(g, 1.6, '#5a3a14'); g.fillStyle = '#ff9a3a'; g.beginPath(); g.arc(9, 8, 4, 0, 7); g.arc(17, 7, 4, 0, 7); g.fill();
});
ART.chimney = () => sprite('chimney', 44, 80, 22, 80, g => { // 지붕 위: 굴뚝
  g.fillStyle = lg(g, 0, 80, ['#c8664a', '#8a3a2a']); g.fillRect(4, 10, 36, 70); g.strokeStyle = '#4a1a10'; g.lineWidth = 2; g.strokeRect(4, 10, 36, 70);
  g.strokeStyle = 'rgba(70,20,10,.45)'; g.lineWidth = 1.2; for (let r = 0; r < 7; r++) { g.beginPath(); g.moveTo(4, 20 + r * 10); g.lineTo(40, 20 + r * 10); g.stroke(); for (let c = 0; c < 2; c++) { const bx = 4 + (r % 2 ? 9 : 18) + c * 18; g.beginPath(); g.moveTo(bx, 10 + r * 10); g.lineTo(bx, 20 + r * 10); g.stroke(); } }
  g.fillStyle = '#5a5a6a'; g.fillRect(0, 2, 44, 10); g.strokeStyle = '#2a2a3a'; g.strokeRect(0, 2, 44, 10);
});
ART.bat = (f) => sprite('bat' + f, 50, 30, 25, 15, g => { // 밤 산책길: 꼬마 박쥐
  g.fillStyle = '#4a3a6a'; g.beginPath(); g.moveTo(25, 14); f ? (g.quadraticCurveTo(10, 0, 0, 6), g.quadraticCurveTo(8, 12, 6, 20), g.quadraticCurveTo(16, 14, 25, 20)) : (g.quadraticCurveTo(10, 26, 0, 24), g.quadraticCurveTo(10, 18, 8, 12), g.quadraticCurveTo(16, 16, 25, 12)); g.fill(); stroke(g, 1.4, '#1a1030');
  g.beginPath(); g.moveTo(25, 14); f ? (g.quadraticCurveTo(40, 0, 50, 6), g.quadraticCurveTo(42, 12, 44, 20), g.quadraticCurveTo(34, 14, 25, 20)) : (g.quadraticCurveTo(40, 26, 50, 24), g.quadraticCurveTo(40, 18, 42, 12), g.quadraticCurveTo(34, 16, 25, 12)); g.fill(); stroke(g, 1.4, '#1a1030');
  g.beginPath(); g.arc(25, 15, 8, 0, 7); g.fillStyle = '#5a4a7a'; g.fill(); stroke(g, 1.4, '#1a1030');
  g.beginPath(); g.moveTo(19, 9); g.lineTo(20, 2); g.lineTo(23, 8); g.moveTo(31, 9); g.lineTo(30, 2); g.lineTo(27, 8); g.fill();
  g.fillStyle = '#ffe27a'; g.beginPath(); g.arc(22, 14, 1.8, 0, 7); g.arc(28, 14, 1.8, 0, 7); g.fill(); g.fillStyle = '#fff'; g.fillRect(23.5, 18, 1.4, 2); g.fillRect(26, 18, 1.4, 2);
});
