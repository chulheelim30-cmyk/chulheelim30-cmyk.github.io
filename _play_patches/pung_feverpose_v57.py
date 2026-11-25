# v57 풍년이의 모험: 피버 때 '앉아서 달리는' 것처럼 보이던 문제
# 피버 땐 달리기 그림 8장 중 몸을 웅크린 3·4번을 빼고, 넘기는 속도도 2.6배 → 1.9배로
P = 'play/pungnyeon/index.html'
s = open(P, encoding='utf8').read()
old = "'g_r' + (Math.floor(PL.anim * (G.fever > 0 ? 2.6 : 1.5)) % 8)"
new = "'g_r' + (G.fever > 0 ? [0, 1, 2, 5, 6, 7][Math.floor(PL.anim * 1.9) % 6] : Math.floor(PL.anim * 1.5) % 8) /* FEVERPOSE_V57 */"
if 'FEVERPOSE_V57' not in s:
    assert s.count(old) == 1; s = s.replace(old, new)
    open(P, 'w', encoding='utf8').write(s); print('OK')
