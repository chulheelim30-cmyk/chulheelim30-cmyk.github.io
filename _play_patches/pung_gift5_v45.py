#!/usr/bin/env python3
"""풍년이의 모험 v45: 보스 첫 승리 간식 100개 → 보스 5종을 모두 처음 이겼을 때 한 번만 간식 500개"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'GIFT5_V45' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("  addCoin(30 * B.lv + (first ? 100 : 0));",
    "  const allFive = first && beat.length === 5; // GIFT5_V45: 다섯 보스 모두 처음 이긴 그 순간 한 번\n  addCoin(30 * B.lv + (allFive ? 500 : 0));")
rep("G.bannerSub = `${D.n} · +${bon}` + (first ? ' · 첫 승리 간식 100개' : '');",
    "G.bannerSub = `${D.n} · +${bon}` + (allFive ? ' · 보스 5종 완료! 간식 500개' : '');")
P.write_text(s, encoding='utf-8'); print('ok')
rep('보스를 처음 이기면 간식 100개 선물</div>', '보스 5종을 모두 이기면 간식 500개 선물</div>')  # (수동 반영)
