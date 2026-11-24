#!/usr/bin/env python3
"""풍년이의 모험 v41: 장 그림(1장 봄 발자국·2장 반딧불·3장 눈 오는 밤)을 오프닝 제목·장 넘김 화면에, 공유 미리보기 그림(og.jpg)"""
import sys, json, pathlib
D = pathlib.Path(__file__).resolve().parent
P = D.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'CHART_V41' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
art = json.load(open(D / 'pung_ch_v41.json'))
i = s.index('const IMG = {};')
s = s[:i] + '/* CHART_V41 */ Object.assign(SPR,' + json.dumps(art, separators=(',', ':')) + ');\n' + s[i:]
rep('<meta property="og:image" content="https://chulheelim30-cmyk.github.io/play/pungnyeon/icon.png">',
    '<meta property="og:image" content="https://chulheelim30-cmyk.github.io/play/pungnyeon/og.jpg">\n<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n<meta name="twitter:card" content="summary_large_image">\n<link rel="apple-touch-icon" href="icon512.png">')
# 오프닝 제목: 지금 장의 그림 위로 두 마리가 달려요
rep("    opCover(g, IMG.bg_sunset, S.k === 'title' ? 0.5 - p * 0.15 : 0.35 + p * 0.25, 0.6, S.k === 'title' ? 1.25 : 1.12 + p * 0.1);",
    "    const chI = IMG['ch' + (Math.floor(progN() / 5) + 1)], useCh = S.k === 'title' && chI && chI.complete && chI.naturalWidth;\n    opCover(g, useCh ? chI : IMG.bg_sunset, S.k === 'title' ? 0.5 - p * 0.15 : 0.35 + p * 0.25, useCh ? 0.5 : 0.6, S.k === 'title' ? 1.25 : 1.12 + p * 0.1);")
# 장 넘김 화면: 그 장의 그림 + 어둡게 깔고 글자
rep("    g.fillStyle = '#1a1030'; g.fillRect(0, 0, W, H); opText(g, S.cap,",
    "    g.fillStyle = '#1a1030'; g.fillRect(0, 0, W, H); if (S.bg && IMG[S.bg] && IMG[S.bg].complete) { opCover(g, IMG[S.bg], 0.5, 0.5, 1.08 + p * 0.06); g.fillStyle = 'rgba(20,10,40,.38)'; g.fillRect(0, 0, W, H); } opText(g, S.cap,")
rep("{ d: 3.2, k: 'chapter', cap: '2장 · 별을 따라서', sub: '1장 끝!' },", "{ d: 3.6, k: 'chapter', bg: 'ch2', cap: '2장 · 별을 따라서', sub: '1장 끝!' },")
rep("{ d: 3.2, k: 'chapter', cap: '3장 · 다시, 호수공원', sub: '보스 다섯만 더!' },", "{ d: 3.6, k: 'chapter', bg: 'ch3', cap: '3장 · 다시, 호수공원', sub: '보스 다섯만 더!' },")
P.write_text(s, encoding='utf-8'); print('ok')
