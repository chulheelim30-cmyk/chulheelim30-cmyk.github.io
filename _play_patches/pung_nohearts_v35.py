#!/usr/bin/env python3
"""풍년이의 모험 v35: 하트 없애고 배부름 하나로 (쿠키런 에너지처럼). 부딪히면 배부름 -20, 0이면 털썩. 맨 마지막에 적용"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'NOHEART_V35' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
rep("['heart', G.hp < 3 ? 0.5 : 0]]", "['heart', G.food < 60 ? 0.7 : 0]]")
rep("G.hp = Math.min(3, G.hp + 1); G.banner = 1.4; G.bannerTxt = '다시 출발!'; G.bannerSub = '하트 +1';", "G.food = Math.min(100, (G.food || 0) + 10); G.banner = 1.4; G.bannerTxt = '다시 출발!'; G.bannerSub = '배부름 +10';")
rep("G.hp--; G.food = Math.max(0, (G.food || 0) - 8); PL.hurt = 1.4;", "G.food = Math.max(0, (G.food || 0) - 20); PL.hurt = 1.4; // NOHEART_V35: 하트 대신 배부름 -20")
rep("  if (G.hp <= 0 && !G.noRevive && (G.revived | 0) < REVIVE_MAX) {", "  if (G.food <= 0) { PL.hurt = 0; G.state = 'play'; starve(); return; }\n  if (G.hp <= 0 && !G.noRevive && (G.revived | 0) < REVIVE_MAX) {")
rep("else if (o.t === 'heart') { G.hp = Math.min(3, G.hp + 1); pop(o.x, o.y - 24, '하트 +1', '#ffd27a', 22);", "else if (o.t === 'heart') { G.food = Math.min(100, (G.food || 0) + 25); pop(o.x, o.y - 24, '배부름 +25', '#9af07a', 22);")
rep("G.bannerSub = '하트 +1 · 잠깐 무적';", "G.bannerSub = '배부름 충전 · 잠깐 무적';")
rep("{ k: 'heart', i: '❤️', n: '하트 채우기', d: '하트 1개를 바로 채워요', once: 1 },", "{ k: 'heart', i: '🍖', n: '배부름 채우기', d: '배부름 +40', once: 1 },")
rep("(c.k === 'heart' ? G.hp < 3 :", "(c.k === 'heart' ? G.food < 80 :")
rep("if (k === 'heart') G.hp = Math.min(3, G.hp + 1);", "if (k === 'heart') G.food = Math.min(100, (G.food || 0) + 40);")
rep("if (G.hp < 3) { G.hp++; pop(PX(), PL.y - 100, '하트 +1', '#ffd27a', 20); }", "pop(PX(), PL.y - 100, '배부름 +15', '#9af07a', 20);")
rep("광고를 보면 하트 1개로 이어 달릴 수 있어요", "광고를 보면 배부름을 채우고 이어 달릴 수 있어요")
# HUD: 하트 줄 없애고, 배부름 막대를 맨 위로(크게), 피버 게이지는 그 아래
rep("  for (let i = 0; i < 3; i++) put(ART.heart(i >= G.hp), 76 + i * 34, 30, i < G.hp && G.hp === 1 ? { s: 1 + Math.sin(G.t * 10) * 0.1 } : null);\n", "")
rep("const gx = 64, gy = 52,", "const gx = 64, gy = 44,")
rep("{ const fx = 16, fy = 70, fw = 150, fh = 12,", "{ const fx = 44, fy = 18, fw = 150, fh = 16,")
rep("put(ART.fish(), fx + 9, fy + 6, { s: 0.55 });", "")
rep("text(low ? '배고파!' : '배부름', fx + fw + 28, fy + 6, 12, 'left'", "text(low ? '배고파!' : '배부름', fx + fw + 28, fy + 8, 13, 'left'")
P.write_text(s, encoding='utf-8'); print('ok')
