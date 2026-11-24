#!/usr/bin/env python3
"""풍년이의 모험 오프닝 컷신 넣기 (pung_fun_v23.py 다음에 적용)"""
import sys, pathlib
D = pathlib.Path(__file__).resolve().parent
P = D.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'id="op-cv"' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, a[:60]; s = s.replace(a, b)
rep('#shop-grid{', '#op{position:fixed;inset:0;z-index:30;background:#140c24}#op[hidden],#op-tap[hidden]{display:none}#op-cv{position:absolute;inset:0;width:100%;height:100%}#op-tap{position:absolute;inset:0;border:0;background:transparent;color:#fff;font-family:Jua,"Noto Sans KR",sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;cursor:pointer}#op-tap b{font-weight:400;font-size:min(64px,11vw);color:#ffe27a;text-shadow:0 3px 0 #7a3a10,0 0 24px rgba(255,200,120,.6)}#op-tap span{font-size:20px;animation:opb 1.2s ease-in-out infinite}@keyframes opb{50%{opacity:.35}}#op-skip{position:absolute;right:max(16px,env(safe-area-inset-right));bottom:14px;z-index:2;border:0;border-radius:14px;padding:8px 14px;font:16px Jua,"Noto Sans KR",sans-serif;background:rgba(255,255,255,.2);color:#fff;cursor:pointer}\n#shop-grid{')
rep('<div class="ov" id="shop" hidden', '<div id="op" hidden><canvas id="op-cv"></canvas><button id="op-tap" hidden><b>풍년이의 모험</b><span>화면을 눌러 시작 ▶</span></button><button id="op-skip">건너뛰기 ▶▶</button></div>\n<div class="ov" id="shop" hidden')
rep('<button class="btn ghost" id="rank-btn">', '<button class="btn ghost" id="op-btn">🎬 오프닝</button><button class="btn ghost" id="rank-btn">')
rep('window.__G = G;', (D / 'pung_opening_v23.js').read_text(encoding='utf-8') + 'window.__G = G; window.__op = { opOpen, opEnd, OP };')
rep("PungRank.entryInvite('pungadventure', { host: wrap, onlyIf: () => !$('home').hidden,", "PungRank.entryInvite('pungadventure', { host: wrap, onlyIf: () => !$('home').hidden && $('op').hidden,")
P.write_text(s, encoding='utf-8'); print('ok')
