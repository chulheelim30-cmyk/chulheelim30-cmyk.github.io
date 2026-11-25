# v60 풍년이의 모험: 장애물이 눈에 잘 띄게
# - 장애물 테두리: 흰 테두리 두껍게 + 바깥에 빨간 빛 (먹을 것·친구와 구분)
# - 땅 장애물 밑에 빨간 그림자 표시, 날아오는 장애물은 빨간 빛만
P = 'play/pungnyeon/index.html'
s = open(P, encoding='utf8').read()
def rep(o, n):
    global s
    assert s.count(o) == 1, ('못 찾음/여러 개', s.count(o), o[:80]); s = s.replace(o, n)
if 'VIS_V60' not in s:
    rep("const OUTF = 'drop-shadow(0 0 2px #fff) drop-shadow(0 0 1px #fff) drop-shadow(0 2px 2px rgba(60,20,40,.55))'",
        "const OUTF = 'drop-shadow(0 0 2px #fff) drop-shadow(0 0 2px #fff) drop-shadow(0 0 1px #fff) drop-shadow(0 0 7px rgba(255,60,50,.9)) drop-shadow(0 2px 2px rgba(60,20,40,.55))' /* VIS_V60 */")
    rep("const hz = HAZ.has(o.t); if (hz) { ctx.save(); ctx.filter = OUTF; }",
        "const hz = HAZ.has(o.t); if (hz && !['crow', 'bat', 'cone', 'bolt', 'branch'].includes(o.t)) { const w = o.t === 'bike' ? 34 : o.t === 'puddle' ? 30 : 24, a = 0.35 + 0.15 * Math.sin(G.t * 8); ctx.fillStyle = `rgba(255,50,60,${a})`; ctx.beginPath(); ctx.ellipse(x, GY + 4, w, 6, 0, 0, 7); ctx.fill(); }\n"
        "    if (hz) { ctx.save(); ctx.filter = OUTF; }")
    open(P, 'w', encoding='utf8').write(s); print('OK')
