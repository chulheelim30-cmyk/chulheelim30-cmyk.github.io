# 풍년이의 모험 v54: 간식 콤보 + 피버 막판 와르르
# 사용: python3 _play_patches/pung_combo_v54.py  (저장소 맨 위에서)
import sys
P = 'play/pungnyeon/index.html'
s = open(P, encoding='utf8').read()
if 'COMBO_V54' in s:
    print('이미 적용됨'); sys.exit()

def rep(old, new):
    global s
    assert s.count(old) == 1, ('못 찾음/여러 개', old[:60])
    s = s.replace(old, new)

# 1) 간식 먹을 때 콤보 쌓기 (0.9초 안에 다음 간식을 먹으면 이어짐, 최대 2배)
rep("G.snacks++; if (!G.demo) addSnackTotal(); const v = Math.round(",
    "G.snacks++; if (!G.demo) addSnackTotal(); /* COMBO_V54 */ G.sc = (G.scT > 0 ? (G.sc | 0) : 0) + 1; G.scT = 0.9; snackCombo(o); const v = Math.round((1 + Math.min(G.sc, 50) * 0.02) * ")

# 2) 콤보 시간 줄이기 + 피버 막판 와르르
rep("if (fv) { G.fever -= dt; if (G.fever <= 0) {",
    "if (G.scT > 0) { G.scT -= dt; if (G.scT <= 0) { if ((G.sc | 0) >= 10 && !G.demo) pop(PX(), PL.y - 120, '간식 콤보 ' + G.sc + '!', '#ffd27a', 18); G.sc = 0; } } "
    "if (fv && !G.wr && G.fever <= 1.6 && !G.demo) { G.wr = true; feverWarr(); } "
    "if (fv) { G.fever -= dt; if (G.fever <= 0) {")

# 3) 피버 시작 때 와르르 다시 준비
rep("function startFever() { G.fevers++; G.feverEat = 0;",
    "function startFever() { G.fevers++; G.feverEat = 0; G.wr = false;")

# 4) 부딪히면 콤보 끊김
rep("function hurt() {", "function hurt() { if ((G.sc | 0) >= 10) pop(PX(), PL.y - 120, '콤보 끊김…', '#ffe3f0', 16); G.sc = 0; G.scT = 0;")

# 5) 화면 위 콤보 숫자
rep("function hudX() {",
    "function hudX() {\n  if ((G.sc | 0) >= 5) { const k = G.sc, big = k >= 30; text('간식 콤보 ' + k + (big ? ' 🔥' : ''), LW / 2, 126, big ? 22 : 18, 'center', big ? '#ff9ad0' : '#ffd27a', { grad: big }); }")

# 6) 새 함수
rep("function nearMiss(o) {", """function snackCombo(o) {
  const c = G.sc | 0; if (G.demo || c < 10 || c % 10) return;
  const pts = c * 10; G.bonus += pts; if (!G.fever) addGauge(4);
  pop(o.x, o.y - 40, '간식 콤보 ' + c + '! +' + pts, c >= 30 ? '#ff9ad0' : '#ffd27a', 20 + Math.min(8, c / 10));
  sfx('big'); vib(20); burst(o.x, o.y, 10 + Math.min(20, c / 2), 'spark', ['#ffd27a', '#fff', '#ff9ad0'], 220);
}
function feverWarr() {
  // 피버가 끝나기 직전, 앞쪽에 간식이 와르르 쏟아져요
  G.banner = 1.6; G.bannerTxt = '막판 와르르!'; G.bannerSub = '마지막까지 다 먹어요!';
  const x0 = G.cam + LW * 0.45;
  for (let i = 0; i < 34; i++) { const t = i / 33; objs.push({ t: 'snack', k: SNACKS[i % 5], x: x0 + t * LW * 1.1, y: GY - 50 - Math.sin(t * Math.PI * 3) * 70 - rnd(0, 40) }); }
  for (let i = 0; i < 3; i++) objs.push({ t: 'snack', k: 'bowl', x: x0 + LW * (0.35 + i * 0.35), y: GY - 150 });
  sfx('big'); feverJingle(); vib([30, 30, 60]); burst(SX() + 120, GY - 220, 50, 'conf', ['#ffd27a', '#ff9ad0', '#8af0ff', '#fff'], 480);
}
function nearMiss(o) {""")

open(P, 'w', encoding='utf8').write(s)
print('적용 완료')
