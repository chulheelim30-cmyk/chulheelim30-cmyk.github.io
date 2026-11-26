#!/usr/bin/env python3
"""풍년게임즈 10종 박진감 v1126 (11-26 사용자 "조금 더 박진감 있게, 더 재밌게")
공개본(play/<id>/index.html)이 기준이라 그 위에 덧씌운다. 화면 흔들림은 늘리지 않음(11-23 멀미).
- 공통 키트: 위기 때 빨간 가장자리 + 심장 소리(K.danger), 최고점 다가가기 줄·'최고점이 코앞!'·'신기록 돌파!'(자동),
  깜짝 보상 K.lucky, 속도 UP K.speedUp, 콤보 소리 계단 K.rush
- 게임별: 템포·위기·재미 요소 1개씩 (게임 코드 바꾼 자리에 '11-26' 주석)
쓰는 법: python3 thrill_v1126.py [대상 폴더=../play]  (앱: pung-apps/<id>/www 도 같은 방식, ROOT/<id>/index.html 또는 ROOT/<id>/www/index.html)
변경 조각은 이 파일 옆 thrill_v1126.json (원래 → 바뀐 글, 게임별)
"""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / 'play'
D = json.loads((HERE / 'thrill_v1126.json').read_text(encoding='utf-8'))
MARK = 'THRILL_V1126'
for gid, chunks in D.items():
    f = ROOT / gid / 'index.html'
    if not f.exists(): f = ROOT / gid / 'www' / 'index.html'
    s = f.read_text(encoding='utf-8')
    if MARK in s: print(gid, 'already'); continue
    for a, b in chunks:
        if a.startswith('RE:'):
            s2, n = re.subn(a[3:], b, s); assert n == 1, (gid, n, a[:80]); s = s2; continue
        assert s.count(a) == 1, (gid, s.count(a), a[:120])
        s = s.replace(a, b)
    s = s.replace('/* ---------------- 4-1. 박진감 장치', '/* ' + MARK + ' */\n  /* ---------------- 4-1. 박진감 장치', 1)
    assert MARK in s, gid
    f.write_text(s, encoding='utf-8'); print(gid, 'OK', len(chunks))
