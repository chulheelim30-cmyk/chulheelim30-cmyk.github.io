# v59 풍년이의 모험
# 1) 부딪히면 계속 앉아 있던 문제: '다친 시간'을 줄이는 코드가 주석(// 발밑 먼지) 안에 들어가 실행이 안 됐음 → 꺼내기
#    같은 실수로 부딪힐 때 흔들림·소리·'앗!' 글씨가 안 나오던 것도 꺼내기 (// NOHEART_V35)
# 2) 난이도: 예전엔 약 2분 뒤로 더 빨라지지도 어려워지지도 않았음
#    → 속도: 340에서 시작해 거리마다 꾸준히 오르고, 최고 속도도 오래 달릴수록 조금씩 오름(최대 +120)
#    → 장애물: 1분 40초에 끝나던 오르막을 계속 이어감(오래 달릴수록 장애물 비율 +, 간격 -)
# (언덕은 대표 의견으로 v60에서 뺐어요)
P = 'play/pungnyeon/index.html'
s = open(P, encoding='utf8').read()
def rep(o, n, cnt=1):
    global s
    assert s.count(o) == cnt, ('못 찾음/여러 개', s.count(o), o[:80]); s = s.replace(o, n)
if 'DIFF_V59' not in s:
    # 1) 주석에 갇힌 코드 꺼내기
    rep("// 발밑 먼지 PL.hurt = Math.max(0, PL.hurt - dt);", "// 발밑 먼지\n  PL.hurt = Math.max(0, PL.hurt - dt); // FIX_V59")
    rep("// NOHEART_V35: 하트 대신 배부름 -20 G.shake = 3;", "// NOHEART_V35: 하트 대신 배부름 -20\n  G.shake = 3;")

    # 2) 난이도 곡선
    rep("G.speed = Math.min(600 + prD() * 90 + Math.min(60, (G.bossWin || 0) * 15), 340 + prD() * 140 + G.dist * 0.005)",
        "G.speed = Math.min(600 + prD() * 90 + Math.min(60, (G.bossWin || 0) * 15) + Math.min(120, G.dist / 1500), 340 + prD() * 140 + G.dist * 0.005)")
    rep("diffO = diff + Math.min(0.6, (G.bossWin || 0) * 0.15) + pd * 0.6;",
        "diffO = diff + Math.min(0.6, (G.bossWin || 0) * 0.15) + pd * 0.6 + Math.min(0.6, Math.max(0, G.dist - 45000) / 90000); /* DIFF_V59: 오래 달릴수록 계속 어려워짐 */")
    rep("let x = x0 + 160; while (x < x1 - 220) { x += place(x, diffO) * (1 - pd * 0.18); }",
        "const tight = 1 - pd * 0.18 - Math.min(0.12, Math.max(0, G.dist - 45000) / 300000);\n    let x = x0 + 160; while (x < x1 - 220) { x += place(x, diffO) * tight; }")
    open(P, 'w', encoding='utf8').write(s); print('OK')
