# v66 풍년이의 모험: 대표 피드백(11-25 21:08) 반영
# 1) 피버는 예전처럼 땅에서 달리기(망토 비행 취소), 망토는 입힌 채로: 망토를 풍년이 위에 그려 목에 걸린 것처럼
# 2) 너무 쉬움: 이어 달리기 무제한 → 한 판 2번, 부딪히면 배부름 -20 → -28, 보스 버티기 시간 42~60초 → 60~90초
# 3) 피버가 너무 흔함: 쉼터에서 출발할 때마다 10초 피버(별빛 타임) → 3초 무적 출발로,
#    피버 게이지 간식 1.0 → 0.55, 아슬아슬 2 → 1, 동물 재우기 4·6 → 2·3, '배부름 쑥쑥' 카드(사실 피버 게이지 +30%) → '피버 조금 빨리 +15%'
# 4) 새 장애물 5종(그림 Bing, _art_new/obstacles): 거리에 따라 하나씩 등장, 처음 볼 때 한 줄 안내
#    상자 탑(높음: 2단 점프) 2000~ / 빨래줄(앉아서 지나가기) 4000~ / 굴러오는 호박(다가옴) 6000~ / 시장 수레(길어서 일찍 점프) 8000~ / 맨홀 물줄기(솟을 때 피하기) 10000~
# 5) 선물이 더 자주 나와요(0.06 → 0.09)
import base64
P = 'play/pungnyeon/index.html'
A = '_art_new/obstacles/'
s = open(P, encoding='utf8').read()
def rep(o, n, cnt=1):
    global s
    assert s.count(o) == cnt, ('못 찾음/여러 개', s.count(o), o[:90]); s = s.replace(o, n)
def spr(k, f):
    from PIL import Image
    im = Image.open(A + f); return f'"{k}": {{"src": "data:image/webp;base64,{base64.b64encode(open(A + f, "rb").read()).decode()}", "w": {im.width}, "h": {im.height}}}'
if 'BAL_V66' not in s:
    # 1) 피버 비행 취소, 망토는 위에
    i = s.index("/* CAPE_V62 */ if (fv && !G.demo && G.state === 'play') {"); j = s.index("} else { PL.vy += 2500 * dt; PL.y += PL.vy * dt; }", i) + len("} else { PL.vy += 2500 * dt; PL.y += PL.vy * dt; }")
    s = s[:i] + "/* BAL_V66: 피버도 땅에서 달려요 */ PL.vy += 2500 * dt; PL.y += PL.vy * dt;" + s[j:]
    rep("drawTrail(f, h); drawCape();", "drawTrail(f, h);")
    rep("drawCat(); ctx.restore(); if (G.yarn > 0) drawBud();", "drawCat(); ctx.restore(); drawCape(); if (G.yarn > 0) drawBud();")
    rep("if (!(G.fever > 0) || !G.flying || G.state !== 'play') return;", "if (!(G.fever > 0) || G.state !== 'play' || (PL.hurt > 0 && PL.hurt <= 1.0 && Math.floor(G.t * 14) % 2)) return;")
    rep("const W = 140, H = W * sp.h / sp.w, cx = SX() + 22, cy = PL.y - 60;",
        "const W = PL.slide ? 96 : 112, H = W * sp.h / sp.w, cx = SX() + (PL.slide ? 26 : 30), cy = PL.y - (PL.slide ? 30 : 56) - (PL.ground ? Math.abs(Math.sin(G.t * 16)) * 3 : 0);")
    # 2) 난이도
    rep("REVIVE_MAX = Infinity;", "REVIVE_MAX = 2; // BAL_V66: 무제한 → 한 판 2번")
    rep("G.food = Math.max(0, (G.food || 0) - 20)", "G.food = Math.max(0, (G.food || 0) - 28)")
    rep("B.hp -= B.max / (42 + prD()", "B.hp -= B.max / (60 + prD() * 12 + prD()")
    # 3) 피버 빈도
    rep("function memTime() { G.memT = true; if (G.fever > 0) G.fever = Math.max(G.fever, 10); else { startFever(); G.fever = 10 + upL('fever') * 2 + permL('fever'); } G.bannerTxt = '다시 출발! 별빛 타임'; G.bannerSub = '무적 · 점수 2배 · 간식 비'; G.banner = 2.4; }",
        "function memTime() { G.memT = true; G.dashT = Math.max(G.dashT || 0, 3); G.bonus += 300; G.bannerTxt = '다시 출발!'; G.bannerSub = '3초 무적 · 별빛 보너스 +300'; G.banner = 2.2; }")
    rep("if (!o.nog) addGauge(big ? 10 : 1.0);", "if (!o.nog) addGauge(big ? 8 : 0.55);")
    rep("G.bonus += pts; addGauge(2);", "G.bonus += pts; addGauge(1);")
    rep("sfx('kill'); vib(15); addGauge(6);", "sfx('kill'); vib(15); addGauge(3);")
    rep("sfx('kill'); vib(12); addGauge(4);", "sfx('kill'); vib(12); addGauge(2);")
    rep("G.gauge + v * (1 + upL('gauge') * 0.3)", "G.gauge + v * (1 + upL('gauge') * 0.15)")
    rep("{ k: 'gauge', i: '🍚', n: '배부름 쑥쑥', d: '배부름 게이지가 30% 빨리 차요'", "{ k: 'gauge', i: '🌈', n: '피버 조금 빨리', d: '피버 게이지가 15% 빨리 차요'")
    rep("nextPiece = x + 1100 + Math.random() * 500", "nextPiece = x + 1700 + Math.random() * 700")
    # 5) 선물 더 자주
    rep("Math.random() < 0.06 + diff * 0.03", "Math.random() < 0.09 + diff * 0.03")
    # 4) 새 장애물
    rep("/* DECOIMG_V40 */ Object.assign(SPR,{",
        "/* OBS_V66 */ Object.assign(SPR,{" + ', '.join(spr(k, k + '.webp') for k in ['o_boxes', 'o_cart', 'o_pumpkin', 'o_laundry', 'o_manhole']) + "});\n/* DECOIMG_V40 */ Object.assign(SPR,{")
    rep("if (G.dist > 3000) pick.push(['pigeon', 1 + diff * 2]);",
        "if (G.dist > 3000) pick.push(['pigeon', 1 + diff * 2]); for (const [k, d0, w] of NEWOBS) if (G.dist > d0) pick.push([k, w + diff * 1.2]);")
    rep("case 'bike': objs.push({ t: 'bike', x: x + 90 }); snackArc(x + 20, 150, 140); return 300;",
        "case 'bike': objs.push({ t: 'bike', x: x + 90 }); snackArc(x + 20, 150, 140); return 300;\n"
        "    case 'boxes': objs.push({ t: 'boxes', x: x + 100 }); snackArc(x + 30, 230, 160); obsIntro('boxes'); return 320;\n"
        "    case 'laundry': objs.push({ t: 'laundry', x: x + 110 }); snackLine(x + 50, 4, GY - 20); obsIntro('laundry'); return 330;\n"
        "    case 'pumpkin': objs.push({ t: 'pumpkin', x: x + 560, rot: 0 }); snackLine(x, 3, GY - 30); obsIntro('pumpkin'); return 330;\n"
        "    case 'cart': objs.push({ t: 'cart', x: x + 130 }); snackArc(x + 40, 170, 240); obsIntro('cart'); return 380;\n"
        "    case 'manhole': objs.push({ t: 'manhole', x: x + 110, ph: Math.random() * 2.2 }); snackLine(x + 20, 3, GY - 30); obsIntro('manhole'); return 320;")
    rep("case 'pigeon': return { x0: o.x - 18,",
        "case 'boxes': return { x0: o.x - 24, x1: o.x + 24, y0: GY - 116, y1: GY };\n"
        "    case 'laundry': return { x0: o.x - 44, x1: o.x + 44, y0: GY - 140, y1: GY - 42 };\n"
        "    case 'pumpkin': return { x0: o.x - 24, x1: o.x + 24, y0: GY - 48, y1: GY };\n"
        "    case 'cart': return { x0: o.x - 62, x1: o.x + 58, y0: GY - 58, y1: GY };\n"
        "    case 'manhole': return manholeUp(o) ? { x0: o.x - 20, x1: o.x + 20, y0: GY - 160, y1: GY } : null;\n"
        "    case 'pigeon': return { x0: o.x - 18,")
    rep("if (o.t === 'pigeon') { o.x -= 150 * dt;",
        "if (o.t === 'pumpkin' && o.x - PX() < LW) { o.x -= 170 * dt; o.rot -= dt * 5.5; }\n    if (o.t === 'manhole') o.ph += dt;\n    if (o.t === 'pigeon') { o.x -= 150 * dt;")
    rep("case 'pigeon': put(ART.pigeon(),",
        "case 'boxes': put(ART.boxes(), x, GY + 4, { rot: Math.sin(G.t * 3 + o.x) * 0.015 }); break;\n"
        "      case 'cart': put(ART.cart(), x, GY + 4); break;\n"
        "      case 'pumpkin': put(ART.pumpkin(), x, GY - 26, { rot: o.rot }); break;\n"
        "      case 'laundry': { const e = ART.laundry(); ctx.fillStyle = '#7a5232'; ctx.fillRect(x - 58, GY - 44, 6, 48); ctx.fillRect(x + 52, GY - 44, 6, 48); put(e, x, GY - 40, { rot: Math.sin(G.t * 2.4 + o.x) * 0.02 }); break; }\n"
        "      case 'manhole': drawManhole(o, x); break;\n"
        "      case 'pigeon': put(ART.pigeon(),")
    rep("const HAZ = new Set(['pigeon', 'cone'", "const HAZ = new Set(['boxes', 'laundry', 'pumpkin', 'cart', 'manhole', 'pigeon', 'cone'")
    rep("const NM = { pigeon: 1, bin: 1", "const NM = { boxes: 1, laundry: 1, pumpkin: 1, cart: 1, manhole: 1, pigeon: 1, bin: 1")
    rep("objs.forEach(o => { if (['piece', 'crow', 'goose', 'bat', 'bike', 'chimney', 'pigeon'].includes(o.t)) o.gone = true; });",
        "objs.forEach(o => { if (['piece', 'crow', 'goose', 'bat', 'bike', 'chimney', 'pigeon', 'boxes', 'laundry', 'pumpkin', 'cart', 'manhole'].includes(o.t)) o.gone = true; });")
    rep("function getGift(o) {", r"""const NEWOBS = [['boxes', 2000, 1.6], ['laundry', 4000, 1.6], ['pumpkin', 6000, 1.5], ['cart', 8000, 1.4], ['manhole', 10000, 1.5]];
const OBSTIP = { boxes: ['높은 상자 탑!', '점프 두 번으로 넘어요'], laundry: ['빨래줄!', '앉아서 쏙 지나가요'], pumpkin: ['호박이 굴러와요!', '다가올 때 맞춰 점프'], cart: ['긴 시장 수레!', '조금 일찍 점프해요'], manhole: ['맨홀 물줄기!', '물이 솟을 땐 기다렸다 지나가요'] };
function obsIntro(k) { let seen = {}; try { seen = JSON.parse(localStorage.getItem('pa2_obs') || '{}'); } catch (e) {} if (seen[k] || G.demo) return; seen[k] = 1; try { localStorage.setItem('pa2_obs', JSON.stringify(seen)); } catch (e) {} G.obsTip = k; }
ART.boxes = () => imgArt('o_boxes', 70, 122, 0.5, 1) || ART.bin(); ART.cart = () => imgArt('o_cart', 140, 92, 0.5, 1) || ART.bike(); ART.pumpkin = () => imgArt('o_pumpkin', 54, 58, 0.5, 0.5) || ART.pot();
ART.laundry = () => imgArt('o_laundry', 132, 100, 0.5, 1) || ART.branch(); ART.manhole = () => imgArt('o_manhole', 64, 40, 0.5, 1) || ART.puddle();
const manholeUp = o => { const p = o.ph % 2.2; return p > 1.3 && p < 2.1; };
function drawManhole(o, x) { const p = o.ph % 2.2; put(ART.manhole(), x, GY + 6);
  if (p > 0.8 && p <= 1.3) { for (let i = 0; i < 3; i++) { ctx.fillStyle = 'rgba(140,210,255,.9)'; ctx.beginPath(); ctx.arc(x - 10 + i * 10, GY - 6 - ((G.t * 60 + i * 9) % 18), 3, 0, 7); ctx.fill(); } }
  if (p > 1.3 && p < 2.1) { const k = Math.min(1, (p - 1.3) / 0.15) * Math.min(1, (2.1 - p) / 0.15), h = 160 * k, w = 26;
    const g = ctx.createLinearGradient(0, GY - h, 0, GY); g.addColorStop(0, 'rgba(220,245,255,.95)'); g.addColorStop(1, 'rgba(70,170,255,.95)'); ctx.fillStyle = g;
    ctx.beginPath(); ctx.moveTo(x - w / 2, GY); ctx.quadraticCurveTo(x - w * 0.7, GY - h * 0.5, x - w * 0.3, GY - h); ctx.lineTo(x + w * 0.3, GY - h); ctx.quadraticCurveTo(x + w * 0.7, GY - h * 0.5, x + w / 2, GY); ctx.closePath(); ctx.fill();
    ctx.lineWidth = 2.5; ctx.strokeStyle = '#2a6fb0'; ctx.stroke(); for (let i = 0; i < 4; i++) { ctx.fillStyle = 'rgba(255,255,255,.9)'; ctx.beginPath(); ctx.arc(x + Math.sin(G.t * 9 + i) * 14, GY - h - 4 + Math.cos(G.t * 7 + i) * 6, 5, 0, 7); ctx.fill(); } } }
function getGift(o) {""")
    # 처음 본 장애물 안내: 화면에 나타날 때 한 번
    rep("function stepGift(dt) {", "function stepGift(dt) {\n  if (G.obsTip && objs.some(o => !o.gone && o.t === G.obsTip && o.x - G.cam < LW + 40)) { const [a, b] = OBSTIP[G.obsTip]; G.banner = 2; G.bannerTxt = a; G.bannerSub = b; G.obsTip = null; }")
    open(P, 'w', encoding='utf8').write(s); print('OK')
