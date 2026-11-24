#!/usr/bin/env python3
"""풍년이의 모험 v34: 최종 엔딩 = 꿈에서 깨어 우리 집(부부+두 고양이), 첫 만남 그림 교체(아이 없는 두 사람), 보스 한마디를 장마다 다르게(15줄). 맨 마지막에 적용"""
import sys, pathlib
D = pathlib.Path(__file__).resolve().parent
P = D.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'e_home' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
i = s.index('Object.assign(SPR,{"b_crow"'); j = s.index('</script>', i) + 9
s = s[:j] + '\n<script>Object.assign(SPR,' + (D / 'pung_ending_spr.json').read_text() + ');</script>' + s[j:]
rep("{ d: 3.8, k: 'pic', img: 'dp0', cap: '그날, 작은 회색 고양이가', sub: '우리 가족을 골랐어요' },", "{ d: 3.8, k: 'pic', img: 'e_meet', cap: '그날, 호수공원에서', sub: '우리는 가족이 됐어요' },")
rep("{ d: 3.8, k: 'pic', img: 'dp0', cap: '벤치 앞에서 누가 불렀어요', sub: '\"풍년아! 왕년아!\"' },", "{ d: 3.8, k: 'pic', img: 'e_meet', cap: '벤치 앞에서 누가 불렀어요', sub: '\"풍년아! 왕년아!\"' },")
rep("{ d: 4.2, k: 'home', wake: true, cap: '창가에서 눈을 떴어요', sub: '옆에는 왕년이' },",
    "{ d: 3.6, k: 'pic', img: 'e_wake', big: true, cap: '…꿈이었어요', sub: '둘이 같이 눈을 떴어요' },\n    { d: 5.4, k: 'pic', img: 'e_home', big: true, cap: '진짜 행복은', sub: '여기, 우리 집에 있었어요' },")
# 그림 비율 그대로, 큰 그림은 더 크게·안 기울게
rep("const im = IMG[S.img], side = Math.min(H * 0.62, W * 0.42), z = 1 + p * 0.06, x = W * 0.3,", "const im = IMG[S.img], side = S.big ? Math.min(H * 0.74, W * 0.44) : Math.min(H * 0.62, W * 0.42), ar = im && im.naturalWidth ? im.naturalWidth / im.naturalHeight : 1, z = 1 + p * 0.06, x = W * 0.3,")
rep("g.fillRect(-side / 2 - 12, -side / 2 - 12, side + 24, side + 52); g.shadowBlur = 0;", "g.fillRect(-side * ar / 2 - 12, -side / 2 - 12, side * ar + 24, side + 52); g.shadowBlur = 0;")
rep("if (im && im.complete) g.drawImage(im, -side / 2, -side / 2, side, side);", "if (im && im.complete) g.drawImage(im, -side * ar / 2, -side / 2, side * ar, side);")
# 보스 한마디: 1장 첫 만남 · 2장 시합 · 3장 배웅
L = {'crow': ['츄르 나눠 먹고 친구!', '"또 나눠 줄 거지?"', '"하늘에서 길 봐 줄게!"'],
     'goose': ['"수고 많으세요~"', '"통행증 확인 완료!"', '꽥! 경례로 배웅'],
     'robot': ['길 알려 주고 친구!', '"또 길 잃었어요…"', '"지름길 안내 시작!"'],
     'owl': ['별자리 길이 열렸어요', '"왕년이 놀래켜서 미안~"', '"이제 다 왔다"'],
     'raccoon': ['꺼내 주고 친구!', '"츄르 또 있어?"', '"다리 건너가!"']}
js = 'const BOSS_LINES = ' + repr(L).replace("'", '"').replace('"', "'").replace("'\\'", "'\"").replace('"', '\\"') + ';'
js = 'const BOSS_LINES = {' + ', '.join(f"{k}: [{', '.join(repr(x) for x in v)}]" for k, v in L.items()) + '};'
rep("pop(B.x, bossCY(B) - 90, D.story,", js.replace('\n', ' ') + " pop(B.x, bossCY(B) - 90, (BOSS_LINES[B.kind] || [D.story])[Math.floor((((bIdx() - 1) % 15) + 15) % 15 / 5)] || D.story,")
rep("opCover(g, IMG.bg_sunset, 0.5, 0.5, 1.3); g.fillStyle = 'rgba(30,14,40,.45)';", "if (S.big) { g.save(); try { g.filter = 'blur(10px)'; } catch (e) {} opCover(g, IMG[S.img], 0.5, 0.5, 1.3); g.restore(); } else opCover(g, IMG.bg_sunset, 0.5, 0.5, 1.3); g.fillStyle = 'rgba(30,14,40,.45)';")
P.write_text(s, encoding='utf-8'); print('ok')
