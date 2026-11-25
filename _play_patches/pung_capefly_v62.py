# v62 풍년이의 모험: 피버 = 망토 비행
# - 피버가 되면 빨간 망토를 두르고 하늘로 날아올라 간식 길 위를 날아가요(슈퍼맨 대시 그림)
# - 땅의 장애물·구덩이는 신경 쓰지 않아도 돼요
# - 피버가 끝나면 사뿐히 내려오고, 내려앉을 자리가 구덩이면 길을 이어 줘요(잠깐 무적)
P = 'play/pungnyeon/index.html'
s = open(P, encoding='utf8').read()
def rep(o, n):
    global s
    assert s.count(o) == 1, ('못 찾음/여러 개', s.count(o), o[:90]); s = s.replace(o, n)
if 'CAPE_V62' not in s:
    rep("const prevY = PL.y; PL.vy += 2500 * dt; PL.y += PL.vy * dt;",
        "const prevY = PL.y; /* CAPE_V62 */ if (fv && !G.demo && G.state === 'play') { const ty = GY - 118 + Math.sin(G.t * 2.6) * 12; PL.vy = (ty - PL.y) * 4; PL.y += PL.vy * dt; PL.ground = false; PL.jumps = 2; G.flying = 1; } else { PL.vy += 2500 * dt; PL.y += PL.vy * dt; }")
    rep("if (fv) { G.fever -= dt; if (G.fever <= 0) {",
        "if (fv) { G.fever -= dt; if (G.fever <= 0) { if (G.flying) { G.flying = 0; PL.vy = 120; G.safe = Math.max(G.safe || 0, 1.4); segs.forEach(sg => { if (sg.x1 < PX() + 900 && sg.x1 > PX() - 100) sg.x1 = PX() + 1000; }); pop(PX(), PL.y - 80, '사뿐!', '#fff3b0', 18); }")
    rep("Object.assign(G, { gift: null,", "Object.assign(G, { flying: 0, gift: null,")
    rep("const c = G.sc | 0; if (G.demo || c < 10 || c % 10) return;", "const c = G.sc | 0; if (G.demo || c < 10 || c % 10 || G.fever > 0) return;")
    rep("if ((G.sc | 0) >= 5) {", "if ((G.sc | 0) >= 5 && !(G.fever > 0)) {")
    rep("/피버/.test(G.bannerTxt) ? 'c_love'", "/피버/.test(G.bannerTxt) && !G.flying ? 'c_love'")
    rep("  drawTrail(f, h);", "  drawTrail(f, h); drawCape();")
    rep("function drawCat() {", """function drawCape() { // 피버 비행 망토: 풍년이 등에서 뒤로 펄럭
  if (!(G.fever > 0) || !G.flying || G.state !== 'play') return;
  const ax = SX() + 18, ay = PL.y - 66, L = 104, t = G.t * 9, w = k => Math.sin(t - k * 3.2) * (6 + k * 16);
  ctx.save(); ctx.filter = 'none'; ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1; ctx.lineJoin = 'round';
  ctx.beginPath(); ctx.moveTo(ax + 10, ay - 4);
  ctx.bezierCurveTo(ax - L * 0.35, ay - 14 + w(0.3), ax - L * 0.7, ay - 8 + w(0.6), ax - L, ay - 10 + w(1));
  ctx.lineTo(ax - L * 0.96, ay + 30 + w(1));
  ctx.bezierCurveTo(ax - L * 0.7, ay + 22 + w(0.65), ax - L * 0.35, ay + 18 + w(0.3), ax - 4, ay + 14);
  ctx.closePath();
  const g = ctx.createLinearGradient(ax, ay, ax - L, ay); g.addColorStop(0, '#e8323c'); g.addColorStop(1, '#ff6a5a'); ctx.fillStyle = g; ctx.fill();
  ctx.lineWidth = 4; ctx.strokeStyle = '#5a1420'; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ax - L * 0.3, ay + 2 + w(0.3) * 0.6); ctx.quadraticCurveTo(ax - L * 0.6, ay + 8 + w(0.6) * 0.8, ax - L * 0.9, ay + 10 + w(0.9)); ctx.lineWidth = 2; ctx.strokeStyle = 'rgba(255,220,200,.55)'; ctx.stroke();
  ctx.fillStyle = '#ffd23f'; ctx.beginPath(); ctx.arc(ax + 6, ay + 4, 6, 0, 7); ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = '#7a4a10'; ctx.stroke();
  if (Math.random() < 0.5) parts.push({ x: G.cam + ax - L + rnd(-6, 6), y: ay + 10 + rnd(-10, 20), vx: -G.speed * 0.2, vy: rnd(-20, 20), life: 0.5, max: 0.5, kind: 'spark', col: ['#fff3b0', '#ff9ad0', '#fff'][Math.floor(Math.random() * 3)], size: 0.45, rot: 0, vr: 0, g: 0 });
  ctx.restore();
}
function drawCat() {""")
    open(P, 'w', encoding='utf8').write(s); print('OK')
