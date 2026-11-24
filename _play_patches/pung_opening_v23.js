/* 11-24 오프닝: 그림책처럼 넘어가는 20초 컷신 (처음 한 번 자동, 처음 화면 '오프닝'으로 다시 보기) */
const OP = { on: false, t: 0, cv: null, g: null, W: 0, H: 0, raf: 0, music: null, last: 0 };
const OP_SC = [ // [길이(초), 그림, 자막]
  { d: 3.6, k: 'bg', img: 'bg_sunset', cap: '어느 가을 저녁, 일산호수공원', sub: '' },
  { d: 4.0, k: 'pic', img: 'dp0', cap: '작은 회색 고양이가', sub: '우리 가족을 골랐어요' },
  { d: 3.8, k: 'pic', img: 'dp4', cap: '소파 한가운데는', sub: '언제나 풍년이 자리' },
  { d: 3.8, k: 'pic', img: 'dp3', cap: '밥 달라고 열 번 부르면', sub: '열 번 다 들어줬죠' },
  { d: 4.2, k: 'night', img: 'bg_night', cap: '밤하늘에 흩어진 기억 조각들', sub: '모으면 별자리가 돼요' },
  { d: 4.6, k: 'run', img: 'bg_sunset', cap: '', sub: '' },
];
const OP_T = OP_SC.reduce((a, s) => a + s.d, 0);
function opSize() { const d = Math.min(2.5, window.devicePixelRatio || 1); const el = $('op'); OP.W = el.clientWidth || innerWidth; OP.H = el.clientHeight || innerHeight; /* 세로 화면에선 게임 전체가 90도 돌아가 있어서 창 크기 대신 실제 영역 크기 */ OP.cv.width = OP.W * d; OP.cv.height = OP.H * d; OP.g.setTransform(d, 0, 0, d, 0, 0); }
function opCover(g, im, zx, zy, z) { // 화면을 덮게 그리기 (zx,zy: 0~1 초점, z: 확대)
  if (!im || !im.complete || !im.naturalWidth) return; const W = OP.W, H = OP.H, s = Math.max(W / im.naturalWidth, H / im.naturalHeight) * z, w = im.naturalWidth * s, h = im.naturalHeight * s;
  g.drawImage(im, (W - w) * zx, (H - h) * zy, w, h);
}
function opText(g, str, x, y, size, col, a, align = 'center') {
  if (!str || a <= 0) return; g.save(); g.globalAlpha = Math.min(1, a); g.font = `${size}px Jua, "Noto Sans KR", sans-serif`; g.textAlign = align; g.textBaseline = 'middle';
  g.lineJoin = 'round'; g.lineWidth = size * 0.22; g.strokeStyle = 'rgba(40,20,50,.75)'; g.strokeText(str, x, y); g.fillStyle = col; g.fillText(str, x, y); g.restore();
}
function opScene(g, i, p, alpha) {
  const S = OP_SC[i], W = OP.W, H = OP.H, im = IMG[S.img], ease = x => x * x * (3 - 2 * x);
  g.save(); g.globalAlpha = alpha;
  if (S.k === 'bg' || S.k === 'night' || S.k === 'run') {
    if (S.k === 'run') opCover(g, im, 0.5 - p * 0.15, 0.6, 1.25); else opCover(g, im, 0.35 + p * 0.3, S.k === 'night' ? 0.3 + p * 0.3 : 0.55, 1.12 + p * 0.1);
    if (S.k === 'night') { for (let k = 0; k < 40; k++) { const sx = (k * 197) % W, sy = (k * 89) % (H * 0.55), tw = 0.4 + 0.6 * Math.sin(OP.t * 3 + k) ** 2; g.fillStyle = `rgba(255,250,210,${tw * Math.min(1, p * 3)})`; g.beginPath(); g.arc(sx, sy, 1.2 + (k % 3), 0, 7); g.fill(); }
      const cx = W * 0.5, cy = H * 0.32, pts = [[-120, 20], [-60, -30], [0, 0], [60, -40], [130, 10]], n = Math.min(pts.length, Math.floor(p * 7));
      g.strokeStyle = 'rgba(255,240,180,.7)'; g.lineWidth = 2; g.beginPath(); pts.slice(0, n).forEach(([x, y], j) => j ? g.lineTo(cx + x, cy + y) : g.moveTo(cx + x, cy + y)); g.stroke();
      pts.slice(0, n).forEach(([x, y]) => { g.fillStyle = 'rgba(255,240,170,.35)'; g.beginPath(); g.arc(cx + x, cy + y, 12, 0, 7); g.fill(); g.fillStyle = '#fff6c8'; g.beginPath(); g.arc(cx + x, cy + y, 4, 0, 7); g.fill(); });
      const cat = IMG.c_doze; if (cat && cat.complete) { const h = H * 0.26, w = cat.naturalWidth * h / cat.naturalHeight; g.drawImage(cat, W * 0.16 - w / 2, H * 0.9 - h, w, h); } }
    if (S.k === 'run') {
      g.fillStyle = 'rgba(30,10,40,.18)'; g.fillRect(0, 0, W, H);
      const fr = IMG['g_r' + (Math.floor(OP.t * 12) % 8)], h = H * 0.3; if (fr && fr.complete) { const w = fr.naturalWidth * h / fr.naturalHeight, x = -w + (W * 0.5 + w * 0.5) * Math.min(1, ease(Math.min(1, p * 1.6))); g.drawImage(fr, x, H * 0.88 - h - Math.abs(Math.sin(OP.t * 12)) * 6, w, h);
        for (let k = 0; k < 6; k++) { g.fillStyle = `rgba(255,240,200,${0.5 - k * 0.08})`; g.beginPath(); g.arc(x + w * 0.15 - k * 22, H * 0.86 - k * 3, 6 - k * 0.7, 0, 7); g.fill(); } }
      const k = Math.max(0, (p - 0.28) / 0.3), s = 1 + (1 - Math.min(1, k)) * 0.4;
      if (k > 0) { g.save(); g.translate(W / 2, H * 0.3); g.scale(s, s); opText(g, '풍년이의 모험', 0, 0, Math.min(64, W * 0.09), '#ffe27a', k); g.restore(); opText(g, "PUNGNYEON'S ADVENTURE", W / 2, H * 0.3 + Math.min(46, W * 0.065), Math.min(18, W * 0.03), '#fff', k); }
      opText(g, '간식 훔쳐 간 큰까마귀를 혼내 주러 출발!', W / 2, H * 0.48, Math.min(24, W * 0.04), '#fff', (p - 0.55) * 4);
    }
  } else { // 그림일기 한 장 + 흐린 배경
    opCover(g, IMG.bg_sunset, 0.5, 0.5, 1.3); g.fillStyle = 'rgba(30,14,40,.45)'; g.fillRect(0, 0, W, H);
    const side = Math.min(H * 0.62, W * 0.42), z = 1 + p * 0.06, x = W * 0.3, y = H * 0.5 + (1 - ease(Math.min(1, p * 3))) * 30;
    g.save(); g.translate(x, y); g.rotate((i % 2 ? 1 : -1) * 0.04); g.scale(z, z);
    g.fillStyle = '#fffaf0'; g.shadowColor = 'rgba(0,0,0,.45)'; g.shadowBlur = 24; g.fillRect(-side / 2 - 12, -side / 2 - 12, side + 24, side + 52); g.shadowBlur = 0;
    if (im && im.complete) g.drawImage(im, -side / 2, -side / 2, side, side);
    g.restore();
    const n1 = Math.floor(Math.max(0, p - 0.12) * 40), n2 = Math.floor(Math.max(0, p - 0.38) * 40), fs = Math.min(34, W * 0.045), tx = W * 0.56;
    opText(g, S.cap.slice(0, n1), tx, H * 0.44, fs, '#fff', 1, 'left'); opText(g, S.sub.slice(0, n2), tx, H * 0.44 + fs * 1.5, fs, '#ffe27a', 1, 'left');
  }
  if (S.k === 'bg') { opText(g, S.cap, W / 2, H * 0.78, Math.min(34, W * 0.045), '#fff', p * 3 - 0.3); }
  if (S.k === 'night') { opText(g, S.cap, W / 2, H * 0.58, Math.min(30, W * 0.042), '#fff', p * 3 - 0.3); opText(g, S.sub, W / 2, H * 0.58 + Math.min(44, W * 0.06), Math.min(30, W * 0.042), '#ffe27a', p * 3 - 1); }
  g.restore();
}
function opFrame(now) {
  if (!OP.on) return; const dt = Math.min(0.05, (now - OP.last) / 1000 || 0); OP.last = now; OP.t += dt;
  const g = OP.g, W = OP.W, H = OP.H; g.fillStyle = '#140c24'; g.fillRect(0, 0, W, H);
  let t0 = 0, i = 0; while (i < OP_SC.length - 1 && OP.t > t0 + OP_SC[i].d) { t0 += OP_SC[i].d; i++; }
  const p = Math.min(1, (OP.t - t0) / OP_SC[i].d), XF = 0.7;
  if (i > 0 && OP.t - t0 < XF) opScene(g, i - 1, 1, 1);
  opScene(g, i, p, i > 0 ? Math.min(1, (OP.t - t0) / XF) : Math.min(1, OP.t / 0.8));
  for (let k = 0; k < 18; k++) { const sx = ((k * 151 + OP.t * (20 + k * 3)) % (W + 40)) - 20, sy = H - ((k * 97 + OP.t * (30 + k * 2)) % H); g.fillStyle = `rgba(255,230,170,${0.25 + 0.2 * Math.sin(OP.t * 2 + k)})`; g.beginPath(); g.arc(sx, sy, 1.5 + (k % 3), 0, 7); g.fill(); } // 떠다니는 반짝이
  const bar = H * 0.07 * Math.min(1, OP.t * 2); g.fillStyle = '#000'; g.fillRect(0, 0, W, bar); g.fillRect(0, H - bar, W, bar); // 영화 같은 위아래 띠
  if (OP.t > OP_T - 0.8) { g.fillStyle = `rgba(20,12,36,${Math.min(1, (OP.t - (OP_T - 0.8)) / 0.8)})`; g.fillRect(0, 0, W, H); }
  if (OP.t >= OP_T) return opEnd();
  OP.raf = requestAnimationFrame(opFrame);
}
function opMusic() { // 오르골 느낌 멜로디 (효과음과 같은 AudioContext)
  if (muted) return; try { AC = AC || new (window.AudioContext || window.webkitAudioContext)(); AC.resume(); } catch (e) { return; }
  const mel = [72, 76, 79, 84, 83, 79, 76, 79, 77, 81, 84, 88, 86, 84, 81, 79, 76, 79, 84, 83, 81, 79, 77, 76, 74, 77, 81, 79, 76, 72, 74, 72], bass = [48, 53, 55, 48], t0 = AC.currentTime + 0.1, step = 0.32, master = AC.createGain(); master.gain.value = 0.9; master.connect(AC.destination); OP.music = master;
  const note = (m, t, len, vol, type) => { const o = AC.createOscillator(), g = AC.createGain(); o.type = type; o.frequency.value = 440 * Math.pow(2, (m - 69) / 12); o.connect(g); g.connect(master); g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t + 0.015); g.gain.exponentialRampToValueAtTime(0.0001, t + len); o.start(t); o.stop(t + len + 0.05); };
  const total = Math.floor((OP_T - 1) / step);
  for (let i = 0; i < total; i++) { const t = t0 + i * step; note(mel[i % mel.length], t, 1.2, 0.07, 'triangle'); note(mel[i % mel.length] + 12, t, 0.5, 0.015, 'sine'); if (i % 8 === 0) note(bass[(i / 8) % 4], t, step * 8, 0.05, 'sine'); }
}
function opStart() {
  if (OP.on) return; OP.on = true; OP.t = 0; OP.last = performance.now(); $('op').hidden = false; $('op-tap').hidden = true; opSize(); opMusic();
  OP.raf = requestAnimationFrame(opFrame);
}
function opEnd() {
  OP.on = false; cancelAnimationFrame(OP.raf); localStorage.setItem('pa2_op', '1');
  if (OP.music) { try { OP.music.gain.setTargetAtTime(0.0001, AC.currentTime, 0.15); setTimeout(() => { try { OP.music.disconnect(); } catch (e) {} }, 600); } catch (e) {} OP.music = null; }
  $('op').hidden = true;
  setTimeout(() => { try { PungRank.entryInvite('pungadventure', { host: wrap, onlyIf: () => !$('home').hidden && $('op').hidden }); } catch (e) {} }, 400);
}
function opOpen(autoTap) { // 첫 실행: '눌러서 시작' 카드 (소리를 켜려면 한 번 눌러야 해서)
  OP.cv = $('op-cv'); OP.g = OP.cv.getContext('2d'); $('op').hidden = false; opSize();
  if (autoTap) { $('op-tap').hidden = false; const g = OP.g; g.fillStyle = '#140c24'; g.fillRect(0, 0, OP.W, OP.H); opCover(g, IMG.bg_sunset, 0.5, 0.55, 1.1); g.fillStyle = 'rgba(20,12,36,.45)'; g.fillRect(0, 0, OP.W, OP.H); }
  else opStart();
}
$('op-tap').addEventListener('click', opStart);
$('op-skip').addEventListener('click', e => { e.stopPropagation(); opEnd(); });
$('op-btn').addEventListener('click', () => opOpen(false));
addEventListener('resize', () => { if (!$('op').hidden && OP.cv) setTimeout(opSize, 60); });
if (!localStorage.getItem('pa2_op') && !/[?&]noop/.test(location.search)) { const go = () => opOpen(true); if (IMG.bg_sunset.complete) go(); else IMG.bg_sunset.addEventListener('load', go, { once: true }); }
