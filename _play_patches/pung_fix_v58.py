# v58 풍년이의 모험
# 1) 슬라이드(앉기)가 풀리지 않던 문제: 손가락이 화면 어디서 떨어져도, 앱이 가려져도 풀리게
# 2) 시작하자마자 피버: '출발 대시'는 피버 대신 3초 무적(반짝임만)으로
# 3) 피버가 너무 자주: 막판 와르르 간식은 게이지를 안 채움, 간식 콤보 보너스도 게이지 안 채움, 간식 게이지 1.4 → 1.0
P = 'play/pungnyeon/index.html'
s = open(P, encoding='utf8').read()
def rep(o, n):
    global s
    assert s.count(o) == 1, ('못 찾음/여러 개', o[:70]); s = s.replace(o, n)
if 'FIX_V58' not in s:
    # 1) 슬라이드
    rep("bS.addEventListener('pointerdown', e => { e.preventDefault(); e.stopPropagation(); bS.setPointerCapture(e.pointerId); bS.classList.add('dn'); setSlide(true); });",
        "let slidePid = null; /* FIX_V58 */\nbS.addEventListener('pointerdown', e => { e.preventDefault(); e.stopPropagation(); slidePid = e.pointerId; try { bS.setPointerCapture(e.pointerId); } catch (_) {} bS.classList.add('dn'); setSlide(true); });\n"
        "['pointerup', 'pointercancel'].forEach(ev => addEventListener(ev, e => { if (slideHeld && (slidePid === null || e.pointerId === slidePid)) { slidePid = null; bS.classList.remove('dn'); setSlide(false); } }, true));\n"
        "setInterval(() => { if (slideHeld && G.state !== 'play') { slidePid = null; slideHeld = false; bS.classList.remove('dn'); } }, 150);\n"
        "addEventListener('blur', () => { slidePid = null; bS.classList.remove('dn'); setSlide(false); }); document.addEventListener('visibilitychange', () => { if (document.hidden) { slidePid = null; bS.classList.remove('dn'); setSlide(false); } });")
    # 상태가 바뀌면(보스 이야기·쉼터·결과 등) 앉기 풀기
    # 2) 출발 대시 = 무적만
    rep("if (permL('dash')) { G.fever = 3; G.bannerTxt = '출발 대시!'; G.bannerSub = '3초 무적'; G.banner = 1.6; }",
        "if (permL('dash')) { G.dashT = 3; G.bannerTxt = '출발 대시!'; G.bannerSub = '3초 무적'; G.banner = 1.6; }")
    rep("  if (PL.hurt > 0 || G.fever > 0 || G.demo || G.safe > 0) return;",
        "  if (PL.hurt > 0 || G.fever > 0 || G.demo || G.safe > 0 || G.dashT > 0) return;")
    rep("if (G.scT > 0) { G.scT -= dt;", "if (G.dashT > 0) G.dashT -= dt; if (G.scT > 0) { G.scT -= dt;")
    # 3) 피버 빈도
    rep("addGauge(big ? 10 : 1.4);", "if (!o.nog) addGauge(big ? 10 : 1.0);")
    rep("const pts = c * 10; G.bonus += pts; if (!G.fever) addGauge(4);", "const pts = c * 10; G.bonus += pts;")
    rep("objs.push({ t: 'snack', k: SNACKS[i % 5], x: x0 + t * LW * 1.1,", "objs.push({ t: 'snack', nog: 1, k: SNACKS[i % 5], x: x0 + t * LW * 1.1,")
    rep("objs.push({ t: 'snack', k: 'bowl', x: x0 + LW * (0.35 + i * 0.35), y: GY - 150 });", "objs.push({ t: 'snack', nog: 1, k: 'bowl', x: x0 + LW * (0.35 + i * 0.35), y: GY - 150 });")
    # 피버 중에 나오는 간식도 피버가 끝난 뒤 게이지를 채우지 않게
    rep("if (fv) { G.flash = Math.max(0, (G.flash || 0) - dt); if (Math.random() < dt * 20) objs.push({ t: 'snack', k:",
        "if (fv) { G.flash = Math.max(0, (G.flash || 0) - dt); if (Math.random() < dt * 20) objs.push({ t: 'snack', nog: 1, k:")
    open(P, 'w', encoding='utf8').write(s); print('OK')
# 피버 모양 간식(앞쪽에 미리 깔림)도 게이지 안 채움
s = open(P, encoding='utf8').read()
if 'FIXB_V58' not in s:
    o = "add = (x, y, i) => objs.push({ t: 'snack', k: i === 0"
    assert s.count(o) == 1
    s = s.replace(o, "add = (x, y, i) => objs.push({ t: 'snack', nog: 1 /* FIXB_V58 */, k: i === 0")
    open(P, 'w', encoding='utf8').write(s); print('OK2')
