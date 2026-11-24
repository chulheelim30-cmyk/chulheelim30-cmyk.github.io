#!/usr/bin/env python3
"""풍년이의 모험 v42: 꾸미기 위치를 '눈 위치' 기준으로 프레임마다 다시 잡고(머리 크기 고정), 따라가기 지연 없앰"""
import sys, json, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'HD42' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
HD = json.load(open(str(pathlib.Path(__file__).resolve().parent/'pung_hd42.json'))); HD.pop('g_roll', None)
rep("if (sp.hd && DECO.cur) decoAt(-w * 0.55 + sp.hd[0] * s, -h + sp.hd[1] * s, sp.hd[2] * s);",
    "const hd = HD42[f] || sp.hd; if (hd && DECO.cur) decoAt(-w * 0.55 + hd[0] * s, -h + hd[1] * s, hd[2] * s);")
rep("const DS = { x: 0, y: 0, w: 0, t: -1 };",
    "const HD42 = " + json.dumps(HD, separators=(',', ':')) + "; // 눈 위치로 잡은 머리 기준 [가운데x, 머리 위y, 머리 폭] (원본 그림 px)\nconst DS = { x: 0, y: 0, w: 0, t: -1 };")
rep("const fresh = G.t - DS.t > 0.3; DS.t = G.t; const a = fresh ? 1 : 0.4;", "const fresh = true; DS.t = G.t; const a = 1; // v42: 프레임에 바로 붙임")
P.write_text(s, encoding='utf-8'); print('ok')
# (수동 반영) 프레임별 머리 기준을 눈 위치 기준 -0.08폭 왼쪽으로, 점프 1.1배·슬라이드 1.12배; DIMG 위치표 재조정(본문); 나비넥타이 고리 잘라냄(pung_deco_v40.json)
