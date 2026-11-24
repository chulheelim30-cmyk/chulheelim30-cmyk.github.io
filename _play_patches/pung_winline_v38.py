#!/usr/bin/env python3
"""풍년이의 모험 v38: 투쟁 머리띠 아이콘 🎌→🇰🇷, 보스 이긴 뒤 큰 글씨를 장마다 자연스럽게(1장 친구가 됐어요 / 2장 우정이 깊어졌어요 / 3장 고마워, 친구야)"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'WINLINE_V38' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("{ k: 'band', name: '투쟁 머리띠', icon: '🎌', bk: 5 },", "{ k: 'band', name: '투쟁 머리띠', icon: '🇰🇷', bk: 5 },")
rep("G.banner = 3; G.bannerTxt = D.win; G.bannerSub = `보너스 +${bon}` + (first ? ' · 첫 승리 선물 🐟 간식 100개 (상점)' : ` · 상점 간식 +${30 * B.lv}`);",
    "const chW = Math.floor((((bIdx() - 1) % 15) + 15) % 15 / 5); // WINLINE_V38\n  G.banner = 3; G.bannerTxt = ['친구가 됐어요!', '우정이 깊어졌어요!', '고마워, 친구야!'][chW]; G.bannerSub = `${D.n} · +${bon}` + (first ? ' · 첫 승리 간식 100개' : '');")
P.write_text(s, encoding='utf-8'); print('ok')
