# v59 풍년이의 모험
# 1) 부딪히면 계속 앉아 있던 문제: '다친 시간'을 줄이는 코드가 주석(// 발밑 먼지) 안에 들어가 실행이 안 됐음 → 꺼내기
#    같은 실수로 부딪힐 때 흔들림·소리·'앗!' 글씨가 안 나오던 것도 꺼내기 (// NOHEART_V35)
# 2) 난이도: 예전엔 약 2분 뒤로 더 빨라지지도 어려워지지도 않았음
#    → 속도: 340에서 시작해 거리마다 꾸준히 오르고, 최고 속도도 오래 달릴수록 조금씩 오름(최대 +120)
#    → 장애물: 1분 40초에 끝나던 오르막을 계속 이어감(오래 달릴수록 장애물 비율 +, 간격 -)
# 3) 언덕: 길 위에 가끔 언덕이 나오고, 풍년이가 올라갔다 내려와요. 언덕 위엔 장애물 없이 간식 줄
#    올라갈 땐 조금 느려지고 내려갈 땐 조금 빨라져요. 보스전·쉼터에는 안 나와요.
P = 'play/pungnyeon/index.html'
s = open(P, encoding='utf8').read()
def rep(o, n, cnt=1):
    global s
    assert s.count(o) == cnt, ('못 찾음/여러 개', s.count(o), o[:80]); s = s.replace(o, n)
if 'HILL_V59' not in s:
    # 1) 주석에 갇힌 코드 꺼내기
    rep("// 발밑 먼지 PL.hurt = Math.max(0, PL.hurt - dt);", "// 발밑 먼지\n  PL.hurt = Math.max(0, PL.hurt - dt); // FIX_V59")
    rep("// NOHEART_V35: 하트 대신 배부름 -20 G.shake = 3;", "// NOHEART_V35: 하트 대신 배부름 -20\n  G.shake = 3;")

    # 2) 난이도 곡선
    rep("G.speed = Math.min(600 + prD() * 90 + Math.min(60, (G.bossWin || 0) * 15), 340 + prD() * 140 + G.dist * 0.005)",
        "G.speed = Math.min(600 + prD() * 90 + Math.min(60, (G.bossWin || 0) * 15) + Math.min(120, G.dist / 1500), 340 + prD() * 140 + G.dist * 0.005) * hillK()")
    rep("diffO = diff + Math.min(0.6, (G.bossWin || 0) * 0.15) + pd * 0.6;",
        "diffO = diff + Math.min(0.6, (G.bossWin || 0) * 0.15) + pd * 0.6 + Math.min(0.6, Math.max(0, G.dist - 45000) / 90000); /* HILL_V59: 오래 달릴수록 계속 어려워짐 */")
    rep("let x = x0 + 160; while (x < x1 - 220) { x += place(x, diffO) * (1 - pd * 0.18); }",
        "let hx0 = 1e12, hx1 = -1e12;\n"
        "    if (!G.demo && !G.boss && !(G.rest > 0) && n >= 6 && G.dist > 3000 && Math.random() < 0.35 + pd * 0.1) { const L = Math.min(900, x1 - x0 - 300); if (L >= 460) { hx0 = x0 + 170; hx1 = hx0 + L; const h = Math.round(60 + Math.random() * 40 + pd * 20); hills.push({ x0: hx0, x1: hx1, h }); for (let hx = hx0 + 40; hx < hx1 - 20; hx += 46) objs.push({ t: 'snack', k: SNACKS[Math.floor(hx / 46) % 5], x: hx, y: GY - hillH(hx) - 34 }); } }\n"
        "    const tight = 1 - pd * 0.18 - Math.min(0.12, Math.max(0, G.dist - 45000) / 300000);\n"
        "    let x = x0 + 160; while (x < x1 - 220) { if (x > hx0 - 260 && x < hx1 + 60) { x = hx1 + 160; continue; } x += place(x, diffO) * tight; }")
    rep("segs = [{ x0: -600, n: 14,", "hills = []; segs = [{ x0: -600, n: 14,")
    rep("segs = segs.filter(s => s.x1 > G.dist - LW);", "segs = segs.filter(s => s.x1 > G.dist - LW); hills = hills.filter(h => h.x1 > G.dist - LW);")
    rep("let segs = [], objs = [],", """let hills = []; /* HILL_V59 언덕 */
function hillH(x) { for (const h of hills) if (x > h.x0 && x < h.x1) { const t = (x - h.x0) / (h.x1 - h.x0), r = 0.3, e = t < r ? t / r : t > 1 - r ? (1 - t) / r : 1; return h.h * e * e * (3 - 2 * e); } return 0; }
function hillK() { if (!PL.ground) return 1; const d = hillH(PX() + 20) - hillH(PX() - 20); return d > 2 ? 0.9 : d < -2 ? 1.08 : 1; }
let segs = [], objs = [],""")
    # 착지: 바닥 높이 = GY - 언덕 높이
    rep("if (PL.vy >= 0 && PL.y >= GY && prevY <= GY + 6 && over) { if (!PL.ground) { PL.sq = 1.18; burst(SX(), GY, 5, 'puff', ['#fff'], 70); } PL.y = GY; PL.vy = 0; PL.ground = true; PL.jumps = 0; }",
        "const gy = GY - hillH(PX());\n"
        "  if (PL.ground && over && PL.vy >= 0 && PL.y < gy && PL.y > gy - 26) { PL.y = gy; PL.vy = 0; } // 언덕 내려갈 때 붙어서 내려가기\n"
        "  if (PL.vy >= 0 && PL.y >= gy && prevY <= gy + 26 && over) { if (!PL.ground) { PL.sq = 1.18; burst(SX(), gy, 5, 'puff', ['#fff'], 70); } PL.y = gy; PL.vy = 0; PL.ground = true; PL.jumps = 0; }")
    rep("parts.push({ x: PX() - 18 + rnd(-6, 6), y: GY - 4, vx: -G.speed * 0.12", "parts.push({ x: PX() - 18 + rnd(-6, 6), y: PL.y - 4, vx: -G.speed * 0.12")
    # 그림자도 언덕 위로
    rep("const hgt = Math.max(0, GY - PL.y);", "const sgy = GY - hillH(PX()), hgt = Math.max(0, sgy - PL.y);")
    rep("ctx.ellipse(SX() + 4, GY + 3, 46 * Math.max(0.4, 1 - hgt / 300), 7, 0, 0, 7)", "ctx.ellipse(SX() + 4, sgy + 3, 46 * Math.max(0.4, 1 - hgt / 300), 7, 0, 0, 7)")
    # 언덕 그리기 (흙길과 같은 색)
    rep("tile('R', 0, sx + 40 + s.n * 120); }\n  for (const o of objs) {",
        """tile('R', 0, sx + 40 + s.n * 120); }
  for (const h of hills) { const a = h.x0 - G.cam, b = h.x1 - G.cam; if (a > LW + 10 || b < -10) continue;
    const top = []; for (let x = Math.max(a, -20); x <= Math.min(b, LW + 20) + 12; x += 12) { const xx = Math.min(x, b); top.push([xx, GY - hillH(xx + G.cam)]); }
    ctx.save(); ctx.beginPath(); ctx.moveTo(top[0][0], GY + 4); for (const [x, y] of top) ctx.lineTo(x, y - 2); ctx.lineTo(top[top.length - 1][0], GY + 4); ctx.closePath();
    const lgH = ctx.createLinearGradient(0, GY - h.h, 0, GY + 4); lgH.addColorStop(0, '#d9b08a'); lgH.addColorStop(0.6, '#c39470'); lgH.addColorStop(1, '#b0835f'); ctx.fillStyle = lgH; ctx.fill();
    ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.beginPath(); top.forEach(([x, y], i) => i ? ctx.lineTo(x, y - 3) : ctx.moveTo(x, y - 3)); ctx.strokeStyle = '#6f9a4a'; ctx.lineWidth = 9; ctx.stroke(); ctx.strokeStyle = '#9fd36f'; ctx.lineWidth = 5; ctx.stroke();
    for (let i = 0; i < top.length; i += 3) { const [x, y] = top[i]; ctx.fillStyle = 'rgba(110,70,50,.14)'; ctx.beginPath(); ctx.ellipse(x + 6, y + (GY - y) * 0.55, 6, 2.4, 0, 0, 7); ctx.fill(); }
    ctx.restore(); }
  for (const o of objs) {""")
    open(P, 'w', encoding='utf8').write(s); print('OK')
