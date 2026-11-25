#!/usr/bin/env python3
"""풍년이의 모험 v43: 몸에 두르는 꾸미기 5종(목도리·나비넥타이·망토·우비·가방)을 '달리기 효과'로 교체 — 꽃잎·별가루·무지개·비눗방울·하트 발자국"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'TRAIL_V43' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("{ k: 'scarf', name: '빨간 목도리', icon: '🧣', need: 200 },", "{ k: 'scarf', name: '꽃잎 바람', icon: '🌸', need: 200 },")
rep("{ k: 'flower', name: '꽃 화관', icon: '🌸', need: 1200 },", "{ k: 'flower', name: '꽃 화관', icon: '💐', need: 1200 },")
rep("{ k: 'bowtie', name: '나비넥타이', icon: '🎩', need: 2000 },", "{ k: 'bowtie', name: '반짝 별가루', icon: '✨', need: 2000 },")
rep("{ k: 'cape', name: '히어로 망토', icon: '🦸', days: 5 },", "{ k: 'cape', name: '무지개 꼬리', icon: '🌈', days: 5 },")
rep("{ k: 'raincoat', name: '노란 우비', icon: '🌂', naps: 10 },", "{ k: 'raincoat', name: '비눗방울', icon: '🫧', naps: 10 },")
rep("{ k: 'backpack', name: '소풍 가방', icon: '🎒', days: 7 },", "{ k: 'backpack', name: '하트 발자국', icon: '💗', days: 7 },")
# 효과 꾸미기는 머리에 그리지 않음
rep("function decoAt(x, y, w) {", "function decoAt(x, y, w) {\n  if (TRAIL[DECO.cur]) return;")
# 고양이 그리기 직전에 효과(고양이 뒤에)
rep("  const sx = 1 / Math.sqrt(PL.sq), sy = PL.sq;", "  drawTrail(f, h);\n  const sx = 1 / Math.sqrt(PL.sq), sy = PL.sq;")
rep("function drawDeco(k, x, y, hw) { // DECO_V30", r"""/* TRAIL_V43: 달리기 효과 꾸미기 — 풍년이 뒤로 흩날려요 */
const TRAIL = { scarf: 1, bowtie: 1, cape: 1, raincoat: 1, backpack: 1 }, TR = { p: [], t: -1, rb: [], foot: 0 };
function drawTrail(f, h) {
  const k = DECO.cur; if (!TRAIL[k] || G.state === 'home' && !G.demo && false) { TR.p.length = 0; TR.rb.length = 0; return; }
  const dt = TR.t < 0 ? 0 : Math.min(0.05, Math.max(0, G.t - TR.t)); TR.t = G.t;
  const wx = G.cam + SX(), cy = PL.y - h * 0.45, back = wx - 34, run = G.state === 'play';
  const add = (o) => { if (TR.p.length < 90) TR.p.push(o); };
  if (dt > 0 && run) {
    if (k === 'scarf' && Math.random() < dt * 18) add({ x: back, y: cy + rnd(-18, 18), vx: rnd(-60, -20), vy: rnd(-10, 25), life: 1.6, max: 1.6, r: rnd(0, 6), vr: rnd(-4, 4), s: rnd(4, 7), c: ['#ffb3cf', '#ffd1e0', '#ff9ec0'][Math.floor(Math.random() * 3)], t: 'petal' });
    if (k === 'bowtie' && Math.random() < dt * 22) add({ x: back + rnd(-6, 10), y: cy + rnd(-26, 22), vx: rnd(-30, 0), vy: rnd(-20, 20), life: 0.9, max: 0.9, r: 0, vr: 0, s: rnd(3, 6), c: ['#fff6b0', '#ffe066', '#ffffff', '#b8e6ff'][Math.floor(Math.random() * 4)], t: 'star' });
    if (k === 'raincoat' && Math.random() < dt * 7) add({ x: back, y: cy + rnd(-12, 14), vx: rnd(-40, -10), vy: rnd(-45, -20), life: 2.2, max: 2.2, r: rnd(0, 6), vr: 0, s: rnd(6, 11), t: 'bub' });
    if (k === 'backpack' && PL.ground && G.t - TR.foot > 0.16) { TR.foot = G.t; add({ x: wx - 8, y: GY + 2, vx: 0, vy: 0, life: 1.4, max: 1.4, r: 0, vr: 0, s: 6, t: 'heart' }); }
  }
  if (k === 'cape') { if (run && dt > 0) { TR.rb.unshift({ x: wx - 30, y: cy + 4 }); if (TR.rb.length > 26) TR.rb.length = 26; } }
  else TR.rb.length = 0;
  const c = ctx; c.save();
  if (k === 'cape' && TR.rb.length > 2) {
    const cols = ['#ff6b8a', '#ffb35c', '#ffe066', '#7fdc8a', '#6fb8ff', '#b48cff'];
    cols.forEach((col, i) => { c.beginPath(); TR.rb.forEach((p, j) => { const x = p.x - G.cam - j * 7, y = p.y + (i - 2.5) * 3.2 + Math.sin(G.t * 9 - j * 0.5) * 2; j ? c.lineTo(x, y) : c.moveTo(x, y); });
      c.strokeStyle = col; c.globalAlpha = 0.75; c.lineWidth = 3.4; c.lineCap = 'round'; c.stroke(); });
    c.globalAlpha = 1;
  }
  for (let i = TR.p.length - 1; i >= 0; i--) {
    const p = TR.p[i]; p.life -= dt; if (p.life <= 0) { TR.p.splice(i, 1); continue; }
    p.x += p.vx * dt; p.y += p.vy * dt; p.r += p.vr * dt; if (p.t === 'bub') p.vx *= 0.99;
    const x = p.x - G.cam, a = Math.min(1, p.life / p.max * 1.6); if (x < -30 || x > LW + 30) continue;
    c.save(); c.translate(x, p.y); c.rotate(p.r); c.globalAlpha = a;
    if (p.t === 'petal') { c.fillStyle = p.c; c.beginPath(); c.ellipse(0, 0, p.s, p.s * 0.55, 0, 0, 7); c.fill(); c.fillStyle = 'rgba(255,255,255,.5)'; c.beginPath(); c.ellipse(-p.s * 0.3, -p.s * 0.1, p.s * 0.35, p.s * 0.18, 0, 0, 7); c.fill(); }
    else if (p.t === 'star') { const r = p.s * (0.6 + 0.4 * Math.sin(G.t * 20 + p.x)); c.fillStyle = p.c; c.beginPath(); for (let j = 0; j < 8; j++) { const rr = j % 2 ? r * 0.35 : r, an = j * Math.PI / 4; c.lineTo(Math.cos(an) * rr, Math.sin(an) * rr); } c.closePath(); c.fill(); }
    else if (p.t === 'bub') { c.strokeStyle = 'rgba(180,225,255,.9)'; c.lineWidth = 1.4; c.fillStyle = 'rgba(220,240,255,.25)'; c.beginPath(); c.arc(0, 0, p.s, 0, 7); c.fill(); c.stroke(); c.fillStyle = 'rgba(255,255,255,.85)'; c.beginPath(); c.arc(-p.s * 0.35, -p.s * 0.35, p.s * 0.22, 0, 7); c.fill(); }
    else if (p.t === 'heart') { c.globalAlpha = a * 0.85; c.fillStyle = '#ff7aa8'; c.scale(1, 0.55); c.beginPath(); c.moveTo(0, p.s * 0.9); c.bezierCurveTo(-p.s * 1.6, -p.s * 0.2, -p.s * 0.6, -p.s * 1.4, 0, -p.s * 0.4); c.bezierCurveTo(p.s * 0.6, -p.s * 1.4, p.s * 1.6, -p.s * 0.2, 0, p.s * 0.9); c.fill(); }
    c.restore();
  }
  c.restore();
}
function drawDeco(k, x, y, hw) { // DECO_V30""")
P.write_text(s, encoding='utf-8'); print('ok')
# (수동 반영) 효과 시작점 뒤로(-62), 별가루·비눗방울·하트 크기와 개수 키움
# (수동 반영) 하트 발자국 GY-12, 흰 테두리
