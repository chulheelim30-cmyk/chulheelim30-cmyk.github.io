# v78 풍년이의 모험: 판 도중에 나가도 점수 기록 (11-26 대표)
# - 점수는 '처음부터'든 '모험 시작(이어하기)'든 판마다 0부터 (원래 reset에서 dist·bonus 0 → 그대로)
# - 문제: 점수는 털썩 → '쉴게요'로 판이 끝날 때만 올라감. 에필로그 보고 앱을 닫거나
#   뒤로가기·화면 끄기로 나가면 그 판 점수가 사라졌음
# - 고침: 판 중(play·ask·story·pick)에 화면이 가려지면(앱 전환·닫기·화면 끔) 그때까지 점수를
#   최고 기록(pa2_best)에 반영하고 랭킹에 올림. 상점 간식(COIN)도 저장
#   같은 판에서 점수가 안 늘었으면 다시 보내지 않음
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'play/pungnyeon/index.html'
s = open(P, encoding='utf8').read()
def rep(o, n):
    global s
    assert s.count(o) == 1, ('못 찾음/여러 개', s.count(o), o[:90]); s = s.replace(o, n)
if 'MIDSAVE_V78' not in s:
    rep("$('go').addEventListener('click', start);",
        "$('go').addEventListener('click', start);\n"
        "/* MIDSAVE_V78 */ { let pTok = null, pSc = 0;\n"
        "  const live = () => !G.demo && ['play', 'ask', 'story', 'pick'].includes(G.state);\n"
        "  const midSave = () => { try { if (!live()) return; const sc = score(); if (!(sc > 0)) return;\n"
        "    if (sc > G.best) { G.best = sc; localStorage.setItem('pa2_best', sc); } localStorage.setItem('pa2_coin', COIN);\n"
        "    if (pTok === G.tok && sc <= pSc) return; pTok = G.tok; pSc = sc; PungRank.submit('pungadventure', sc); } catch (e) {} };\n"
        "  document.addEventListener('visibilitychange', () => { if (document.hidden) midSave(); });\n"
        "  window.addEventListener('pagehide', midSave); }")
    open(P, 'w', encoding='utf8').write(s)
    print('v78 적용', P)
else:
    print('이미 있음')
