# v61 풍년이의 모험: 선물로 친구 만들기 (부수지 않고 친구로)
# - 선물 3종을 주우면 9초 동안 자동으로 선물을 건네요
#   생선 부메랑: 앞으로 날아갔다 돌아오며 닿는 동물을 친구로
#   방울: 딸랑! 울릴 때마다 퍼지는 소리 고리에 닿는 동물을 친구로
#   츄르 폭죽: 앞으로 던지면 펑! 주변 동물을 친구로 + 간식이 쏟아짐
# - 친구가 된 동물은 20초 동안 풍년이를 따라오며 도와줘요 (최대 3마리)
#   까마귀·박쥐: 반짝이는 걸 좋아해서 먼 간식도 물어 와요(자석)
#   거위: 한 번 대신 막아 줘요
#   비둘기: 구덩이에 빠지면 한 번 들어 올려 줘요
# - 새 동물: 비둘기(위아래로 크게 날며 다가와요)
# - 처음 사귄 동물은 '새 친구!' 알림, 사귄 수는 기기에 저장(pa2_dex)
# 그림: _art_new/obstacles/o_pigeon.webp, _art_new/items/i_fishboom·i_bell·i_bomb.webp
import base64
P = 'play/pungnyeon/index.html'
A = '_art_new/'
s = open(P, encoding='utf8').read()
def rep(o, n):
    global s
    assert s.count(o) == 1, ('못 찾음/여러 개', s.count(o), o[:90]); s = s.replace(o, n)
def spr(k, f):
    from PIL import Image
    im = Image.open(A + f); return f'"{k}": {{"src": "data:image/webp;base64,{base64.b64encode(open(A + f, "rb").read()).decode()}", "w": {im.width}, "h": {im.height}}}'
if 'GIFT_V61' not in s:
    rep("/* DECOIMG_V40 */ Object.assign(SPR,{",
        "/* GIFT_V61 */ Object.assign(SPR,{" + ', '.join([spr('o_pigeon', 'obstacles/o_pigeon.webp'), spr('i_fish', 'items/i_fishboom.webp'), spr('i_bell', 'items/i_bell.webp'), spr('i_churu', 'items/i_bomb.webp')]) + "});\n"
        "/* DECOIMG_V40 */ Object.assign(SPR,{")
    # 초기화
    rep("Object.assign(G, { fevers: 0,", "Object.assign(G, { gift: null, pals: [], gb: [], ring: null, newPals: 0, fevers: 0,")
    # 비둘기: 나오기·움직임·충돌·그리기·목록
    rep("if (z === 4) pick.push(['tcone', 2.6]);", "if (z === 4) pick.push(['tcone', 2.6]); if (G.dist > 3000) pick.push(['pigeon', 1 + diff * 2]);")
    rep("case 'bat': { const y = GY - 70;", "case 'pigeon': { const y = GY - 105; objs.push({ t: 'pigeon', x: x + 460, y, by: y, hp: 1, ph: Math.random() * 6 }); snackLine(x, 3, GY - 30); return 300; }\n    case 'bat': { const y = GY - 70;")
    rep("if (o.t === 'bat') { o.x -= 60 * dt;", "if (o.t === 'pigeon') { o.x -= 150 * dt; o.ph += dt * 2.4; o.y = o.by + Math.sin(o.ph) * 58; }\n    if (o.t === 'bat') { o.x -= 60 * dt;")
    rep("case 'bat': return { x0", "case 'pigeon': return { x0: o.x - 18, x1: o.x + 18, y0: o.y - 12, y1: o.y + 12 };\n    case 'bat': return { x0")
    rep("case 'bat': put(ART.bat(", "case 'pigeon': put(ART.pigeon(), x + j, o.y, { rot: Math.sin(G.t * 10) * 0.08 }); break;\n      case 'bat': put(ART.bat(")
    rep("const HAZ = new Set(['cone'", "const HAZ = new Set(['pigeon', 'cone'")
    rep("const NM = { bin: 1", "const NM = { pigeon: 1, bin: 1")
    rep("(o.t === 'crow' || o.t === 'goose' || o.t === 'cone' || o.t === 'bat' || o.t === 'bolt') && o.x > PX() + 10",
        "(o.t === 'crow' || o.t === 'goose' || o.t === 'cone' || o.t === 'bat' || o.t === 'bolt' || o.t === 'pigeon') && o.x > PX() + 10")
    rep("(o.t === 'crow' || o.t === 'bat' || o.t === 'bolt') ? o.y", "(o.t === 'crow' || o.t === 'bat' || o.t === 'bolt' || o.t === 'pigeon') ? o.y")
    rep("objs.forEach(o => { if (['piece', 'crow', 'goose', 'bat', 'bike', 'chimney'].includes(o.t)) o.gone = true; });",
        "objs.forEach(o => { if (['piece', 'crow', 'goose', 'bat', 'bike', 'chimney', 'pigeon'].includes(o.t)) o.gone = true; });")
    # 선물 줍기
    rep("if (G.yarn <= 0 && Math.random() < 0.07", "if (!G.gift && G.dist > 1500 && Math.random() < 0.06 + diff * 0.03) { const k = ['fish', 'bell', 'churu'][Math.floor(Math.random() * 3)]; objs.push({ t: 'gift', k, x: x + 90, y: GY - 120 }); snackLine(x, 4, GY - 30); return 240; }\n  if (G.yarn <= 0 && Math.random() < 0.07")
    rep("o.t === 'yarn' || o.t === 'wbox') {", "o.t === 'yarn' || o.t === 'wbox' || o.t === 'gift') {")
    rep("else if (o.t === 'yarn') getYarn(o);", "else if (o.t === 'yarn') getYarn(o);\n  else if (o.t === 'gift') getGift(o);")
    rep("case 'yarn': ctx.save();", "case 'gift': { const b = Math.sin(G.t * 4) * 4; ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = `rgba(255,230,140,${0.35 + 0.15 * Math.sin(G.t * 6)})`; ctx.beginPath(); ctx.arc(x, o.y + b, 36, 0, 7); ctx.fill(); ctx.restore(); put(ART['gift_' + o.k](), x, o.y + b, { rot: Math.sin(G.t * 3) * 0.15 }); break; }\n      case 'yarn': ctx.save();")
    # 친구 효과: 까마귀·박쥐 자석 / 거위 막기 / 비둘기 들어 올리기
    rep("mag = fv ? 240 : 52 + upL('mag') * 45 + permL('mag') * 20", "mag = fv ? 240 : 52 + upL('mag') * 45 + permL('mag') * 20 + (palHas('crow') || palHas('bat') ? 120 : 0)")
    rep("  if (wangHurt()) return;", "  if (palUse('goose', '꽥! 내가 막았어!')) { PL.hurt = 1.0; return; }\n  if (wangHurt()) return;")
    rep("if (PL.y > GY + 110) { if (G.demo)", "if (PL.y > GY + 60 && !G.demo && PL.vy > 0 && palUse('pigeon', '구구! 들어 올려 줄게!')) { PL.vy = -1250; PL.jumps = 1; burst(SX(), PL.y - 20, 14, 'spark', ['#fff', '#cfd6e6'], 200); }\n  if (PL.y > GY + 110) { if (G.demo)")
    # 그리기·HUD
    rep("drawBoss(); drawWang();", "drawBoss(); drawWang(); drawPals();")
    rep("if (G.yarn > 0) { put(ART.yarn(), 272, 57", "if (G.gift) { const gx = G.yarn > 0 ? 336 : 272; put(ART['gift_' + G.gift.k](), gx, 57, { s: 0.55 }); text(Math.ceil(G.gift.t) + '초', gx + 16, 58, 14, 'left', '#ffe7a8'); }\n  if (G.yarn > 0) { put(ART.yarn(), 272, 57")
    # 선물·친구 본체
    rep("function getYarn(o) {", r"""const GIFT_T = 9, CREAT = ['crow', 'goose', 'pigeon', 'bat'];
const PALN = { crow: '까마귀', goose: '거위', pigeon: '비둘기', bat: '박쥐' }, PALDO = { crow: '먼 간식도 물어 와요', goose: '한 번 대신 막아 줘요', pigeon: '구덩이에서 한 번 들어 올려 줘요', bat: '먼 간식도 물어 와요' };
const GIFTN = { fish: ['생선 부메랑', '날아갔다 돌아오며 동물에게 선물!'], bell: ['딸랑 방울', '소리가 닿은 동물이 친구가 돼요'], churu: ['츄르 폭죽', '펑! 주변 동물이 다 친구로'] };
ART.pigeon = () => imgArt('o_pigeon', 58, 58, 0.5, 0.5, true) || ART.crow(0);
ART.gift_fish = () => imgArt('i_fish', 48, 48, 0.5, 0.5) || ART.fish(); ART.gift_bell = () => imgArt('i_bell', 38, 40, 0.5, 0.5) || ART.yarn(); ART.gift_churu = () => imgArt('i_churu', 42, 46, 0.5, 0.5) || ART.churu();
const palHas = k => G.pals && G.pals.some(p => p.k === k);
function palUse(k, msg) { const i = (G.pals || []).findIndex(p => p.k === k); if (i < 0) return false; const p = G.pals[i]; G.pals.splice(i, 1); pop(p.x, p.y - 30, msg, '#fff1b8', 17); burst(p.x, p.y, 16, 'spark', ['#ffd27a', '#fff', '#ff9ad0'], 220); sfx('big'); vib(25); return true; }
function getGift(o) {
  G.gift = { k: o.k, t: GIFT_T, cd: 0.2 }; const [n, d] = GIFTN[o.k];
  G.banner = 1.7; G.bannerTxt = n + '!'; G.bannerSub = d; sfx('big'); vib(20); burst(o.x, o.y, 24, 'spark', ['#ffe7a8', '#fff', '#ff9ad0'], 300);
}
function befriend(o) {
  if (o.gone || o.friend) return; o.gone = true; o.friend = true; G.kills++;
  const y = o.t === 'goose' ? GY - 30 : o.y, pts = 80 * (G.fever ? 2 : 1); G.bonus += pts;
  if (G.pals.length >= 3) G.pals.shift();
  G.pals.push({ k: o.t, x: o.x, y, life: 20, ph: Math.random() * 6 });
  let dex = {}; try { dex = JSON.parse(localStorage.getItem('pa2_dex') || '{}'); } catch (e) {}
  const first = !dex[o.t]; dex[o.t] = (dex[o.t] || 0) + 1; try { localStorage.setItem('pa2_dex', JSON.stringify(dex)); } catch (e) {}
  if (first) { G.banner = 2; G.bannerTxt = '새 친구: ' + PALN[o.t] + '!'; G.bannerSub = PALDO[o.t]; }
  else pop(o.x, y - 34, PALN[o.t] + ' 친구! +' + pts, '#ffd0ea', 19);
  for (let i = 0; i < 3; i++) pops.push({ x: o.x - 10 + i * 12, y: y - 10 - i * 10, txt: '♥', col: '#ff9ad0', size: 14 + i * 3, life: 1.1 });
  burst(o.x, y, 16, 'spark', ['#ff9ad0', '#fff', '#ffd27a'], 240); sfx('kill'); vib(12);
}
function nearCreat(x, y, r) { return objs.filter(o => !o.gone && CREAT.includes(o.t) && Math.hypot(o.x - x, (o.t === 'goose' ? GY - 30 : o.y) - y) < r); }
function stepGift(dt) {
  if (G.demo) return;
  const g = G.gift;
  if (g && G.state === 'play') {
    g.t -= dt; g.cd -= dt;
    if (g.cd <= 0) {
      if (g.k === 'fish') { g.cd = 1.1; G.gb.push({ k: 'fish', s: 0, x: PX() + 20, y: PL.y - 50 }); sfx('shot'); }
      else if (g.k === 'bell') { g.cd = 1.8; G.ring = { r: 30 }; sfx('snack'); pop(PX(), PL.y - 100, '딸랑!', '#fff3b0', 18); }
      else { g.cd = 1.4; G.gb.push({ k: 'churu', x: PX() + 20, y: PL.y - 60, vx: G.speed + 360, vy: -620, rot: 0 }); sfx('shot'); }
    }
    if (g.t <= 0) { G.gift = null; pop(PX(), PL.y - 110, '선물 끝!', '#ffe7a8', 16); }
  }
  for (const b of G.gb) {
    if (b.k === 'fish') { b.s += dt; const rel = Math.sin(Math.PI * Math.min(1, b.s)) * 430; b.x = PX() + 20 + rel; b.y = PL.y - 50 - Math.sin(2 * Math.PI * b.s) * 26; nearCreat(b.x, b.y, 40).forEach(befriend); if (b.s >= 1) b.dead = true; }
    else { b.vy += 1600 * dt; b.x += b.vx * dt; b.y += b.vy * dt; b.rot += dt * 8; const hit = nearCreat(b.x, b.y, 34).length; if (hit || b.y >= GY - 8) { b.dead = true; nearCreat(b.x, b.y, 170).forEach(befriend); burst(b.x, b.y, 30, 'spark', ['#ff9ad0', '#ffd27a', '#fff', '#8af0ff'], 360); sfx('big'); vib(18); for (let i = 0; i < 6; i++) objs.push({ t: 'snack', nog: 1, k: SNACKS[i % 5], x: b.x + 40 + i * 34, y: GY - 60 - Math.sin(i / 5 * Math.PI) * 70 }); } }
  }
  G.gb = G.gb.filter(b => !b.dead);
  if (G.ring) { G.ring.r += 720 * dt; const R = G.ring.r; objs.forEach(o => { if (!o.gone && CREAT.includes(o.t) && o.x - G.cam < LW + 20 && Math.abs(Math.hypot(o.x - PX(), (o.t === 'goose' ? GY - 30 : o.y) - (PL.y - 40)) - R) < 46) befriend(o); }); if (R > LW * 0.8) G.ring = null; }
  G.pals.forEach((p, i) => { p.life -= dt; p.ph += dt * 3; const tx = PX() - 80 - i * 56, ty = p.k === 'goose' ? PL.y - 6 : PL.y - 120 - i * 12 + Math.sin(p.ph) * 8; p.x += (tx - p.x) * Math.min(1, dt * 5); p.y += (ty - p.y) * Math.min(1, dt * 5); if (p.life <= 0) pop(p.x, p.y - 30, '또 만나!', '#ffd0ea', 15); });
  G.pals = G.pals.filter(p => p.life > 0);
}
function drawPals() {
  if (!G.pals) return;
  if (G.ring) { const R = G.ring.r; ctx.save(); ctx.strokeStyle = `rgba(255,236,150,${Math.max(0, 0.8 - R / (LW * 0.8))})`; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(SX(), PL.y - 40, R, 0, 7); ctx.stroke(); ctx.lineWidth = 2; ctx.strokeStyle = 'rgba(255,255,255,.6)'; ctx.beginPath(); ctx.arc(SX(), PL.y - 40, R * 0.92, 0, 7); ctx.stroke(); ctx.restore(); }
  for (const b of G.gb) put(b.k === 'fish' ? ART.gift_fish() : ART.gift_churu(), b.x - G.cam, b.y, { rot: b.k === 'fish' ? G.t * 14 : b.rot, s: b.k === 'fish' ? 0.8 : 0.7 });
  for (const p of G.pals) { const x = p.x - G.cam, fade = p.life < 2 && Math.floor(G.t * 8) % 2; if (fade) continue;
    const e = p.k === 'crow' ? ART.crow(Math.floor(G.t * 9) % 2) : p.k === 'goose' ? ART.goose(Math.floor(G.t * 8) % 2) : p.k === 'pigeon' ? ART.pigeon() : ART.bat(Math.floor(G.t * 12) % 2);
    ctx.save(); ctx.translate(x, p.y); ctx.scale(-0.8, 0.8); put(e, 0, p.k === 'goose' ? 30 : 0); ctx.restore();
    text('♥', x, p.y - (p.k === 'goose' ? 60 : 30), 13, 'center', '#ff8fc8'); }
}
function getYarn(o) {""")
    rep("function stepX(dt) {", "function stepX(dt) {\n  stepGift(dt);")
    open(P, 'w', encoding='utf8').write(s); print('OK')
