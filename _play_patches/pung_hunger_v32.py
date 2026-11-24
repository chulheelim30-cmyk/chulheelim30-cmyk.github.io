#!/usr/bin/env python3
"""풍년이의 모험 v32 (B안, 쿠키런식): 배부름 게이지가 계속 줄어듦(약 90초) · 참치캔·사료·쉼터·보스 친구로만 채움 · 0이면 털썩
피버는 드물게(간식 4%→1%) · 간식 줄 6→4. 맨 마지막에 적용"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'FOOD_DRAIN' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
# 피버 게이지: 드물게
rep("addGauge(big ? 18 : 4);", "addGauge(big ? 8 : 1); if (big && !G.demo) { G.food = Math.min(100, (G.food || 0) + 20); pop(o.x, o.y - 50, '배부름 +20', '#9af07a', 18); }")
rep("addGauge(14)", "addGauge(6)"); rep("addGauge(10)", "addGauge(4)"); rep("addGauge(12)", "addGauge(10)"); rep("addGauge(3)", "addGauge(2)")
rep("'참치캔 한 통! +300' : '사료 한 그릇! +300'", "'참치캔! +300' : '사료! +300'")
# 간식 줄
rep("case 'snack': snackLine(x, 6, GY - 30", "case 'snack': snackLine(x, 4, GY - 30")
# 배부름 게이지
rep("cush: permL('cushion'), p0: progN(),", "cush: permL('cushion'), food: 100, p0: progN(),")
rep("  G.nmT = Math.max(0, (G.nmT || 0) - dt); if (G.nmT <= 0) G.combo = 0;",
    """  G.nmT = Math.max(0, (G.nmT || 0) - dt); if (G.nmT <= 0) G.combo = 0;
  if (!G.demo && G.state === 'play' && !(G.fever > 0) && !(G.rest > 0) && !(G.boss && G.boss.hp <= 0)) { // 배부름이 조금씩 줄어요 (쿠키런 에너지처럼)
    G.food = Math.max(0, (G.food == null ? 100 : G.food) - dt * FOOD_DRAIN);
    if (G.food < 50 && !localStorage.getItem('pa2_tipfood')) { localStorage.setItem('pa2_tipfood', '1'); G.banner = 2.4; G.bannerTxt = '배고파져요!'; G.bannerSub = '참치캔·사료로 채워요'; }
    if (G.food <= 0) starve();
  }""")
rep("  G.hp--; PL.hurt = 1.4;", "  G.hp--; G.food = Math.max(0, (G.food || 0) - 8); PL.hurt = 1.4;")
rep("function hurt() {", """const FOOD_DRAIN = 100 / 75; // 가만히 달리면 약 75초에 바닥 (참치캔 놓치면 점점 배고파짐)
function starve() { // 배고파서 털썩 → 이어 달리기(광고) 또는 끝
  if (G.state !== 'play') return; G.hp = 0; G.shake = 3; vib(60); sfx('hurt'); pop(PX(), PL.y - 90, '배고파…', '#ffe3f0', 22);
  if (!G.noRevive && (G.revived | 0) < REVIVE_MAX) { G.state = 'ask'; PL.vy = 0; if (PL.y > GY) PL.y = GY; setTimeout(showRevive, 800); return; }
  G.state = 'over'; PL.vy = 0; if (PL.y > GY) PL.y = GY; const sc = score(); if (sc > G.best) { G.best = sc; localStorage.setItem('pa2_best', sc); } setTimeout(showOver, 1000);
}
function hurt() {""")
rep("G.revived = (G.revived | 0) + 1; G.hp = 1;", "G.revived = (G.revived | 0) + 1; G.hp = 1; G.food = Math.max(G.food || 0, 60);")
rep("G.rest = 0; if (G.hp < 3) { G.hp++; pop(PX(), PL.y - 100, '하트 +1', '#ffd27a', 20); }", "G.rest = 0; G.food = Math.min(100, (G.food || 0) + 15); if (G.hp < 3) { G.hp++; pop(PX(), PL.y - 100, '하트 +1', '#ffd27a', 20); }")
rep("G.bonus += bon; G.bossWin++; if (G.braveB)", "G.bonus += bon; G.food = Math.min(100, (G.food || 0) + 40); G.bossWin++; if (G.braveB)")
# HUD: 피버 게이지 이름, 제목 자리에 배부름 막대
rep("else text('배부름', gx + gw + 8, gy + 5, 12, 'left', '#ffe3f0');", "else text('피버', gx + gw + 8, gy + 5, 12, 'left', '#ffe3f0');")
rep("""  text('풍년이의 모험', 16, 84, 22, 'left', '#ffffff', { out: '#4a2a14' }); text("PUNGNYEON'S ADVENTURE", 17, 104, 10, 'left', '#ffffff', { out: '#4a2a14' });""",
    """  { const fx = 16, fy = 70, fw = 150, fh = 12, fk = Math.max(0, Math.min(1, (G.food == null ? 100 : G.food) / 100)), low = fk < 0.25, bl = low && Math.floor(G.t * 6) % 2; // 배부름 막대
    put(ART.fish(), fx + 9, fy + 6, { s: 0.55 });
    rr(ctx, fx + 22, fy, fw, fh, 6); ctx.fillStyle = 'rgba(30,20,60,.55)'; ctx.fill(); ctx.strokeStyle = bl ? '#ff6a7a' : 'rgba(255,255,255,.8)'; ctx.lineWidth = bl ? 2.2 : 1.2; ctx.stroke();
    if (fk > 0.005) { rr(ctx, fx + 23.5, fy + 1.5, (fw - 3) * fk, fh - 3, 4.5); ctx.fillStyle = fk > 0.5 ? '#7fd84a' : fk > 0.25 ? '#ffd23f' : '#ff5a6a'; ctx.fill(); }
    text(low ? '배고파!' : '배부름', fx + fw + 28, fy + 6, 12, 'left', low ? '#ff9aa8' : '#e8ffe0'); }""")
P.write_text(s, encoding='utf-8'); print('ok')
# (v33) 처음 화면 '오픈소스 라이선스' 링크는 play/pungnyeon/index.html 에 직접 추가함: <a id="lic" href="../licenses.html" ...> (#go 버튼 다음)
