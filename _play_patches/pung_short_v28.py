#!/usr/bin/env python3
"""풍년이의 모험 v28: 플레이 중 글을 짧고 명료하게 (대표: '글 볼 시간 없다'). '기억 조각' → '별'. 맨 마지막에 적용"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'SHORT_V28' in s: print('already'); sys.exit(0)
R = [
 ("G.bannerSub = '왕년이가 깨워 줬어요 · 하트 +1'", "G.bannerSub = '하트 +1'"),
 ("G.bannerSub = `피버 때 간식 ${G.feverEat}개 냠냠 · 잠깐 꿀잠`", "G.bannerSub = ''"),
 ("G.bannerSub = '보너스 +1000 · ' + G.bannerSub;", "G.bannerSub = '+1000';"),
 ("G.bannerTxt = `기억 조각 ${G.pieces}/6`; G.bannerSub = consOf(G.stage).n + ' 별자리에 별 하나가 켜졌어요';", "G.bannerTxt = `★ ${G.pieces}/6`; G.bannerSub = '';"),
 ("G.bannerSub = '무적 · 점수 2배 · 간식 비 (너무 많이 먹으면 꿀잠)'", "G.bannerSub = '무적 · 점수 2배'"),
 ("G.bannerSub = `이번 장 보스 ${P % 5}/5 · 최종 엔딩까지 보스 ${15 - P}`", "G.bannerSub = `보스 ${P % 5}/5`"),
 ("G.bannerSub = '3초 동안 무적 질주'", "G.bannerSub = '3초 무적'"),
 ("G.bannerSub = '처음 화면 \\'꾸미기\\'에서 입혀 보세요'", "G.bannerSub = '꾸미기에서 입혀요'"),
 ("G.bannerSub = '까마귀는 재우고, 거위는 쫓아내요'", "G.bannerSub = '자동 공격!'"),
 ("sub: '간식을 몽땅 훔쳐 갔어요 · 털실공 친구와 혼내 주세요'", "sub: '털실공으로 공격!'"),
 ("sub: '돌진해 와요 · 점프해서 머리를 콩! 밟아 주세요'", "sub: '점프해서 머리 콩!'"),
 ("sub: '낮은 공은 점프, 높은 공은 슬라이드 · 과열되면 콩!'", "sub: '낮은 공 점프 · 높은 공 슬라이드'"),
 ("sub: '어둠 속 급강하! 빨간 줄 높이를 보고 피하세요'", "sub: '빨간 줄 보고 피하기'"),
 ("sub: '쿵! 땅 물결은 점프로 · 쓰레기통에 머리가 끼면 콩!'", "sub: '물결 점프 · 머리 끼면 콩!'"),
 ("story: '츄르를 반 나눠 줬더니 웃었어요'", "story: '츄르 나눠 먹고 친구!'"),
 ("story: '\"수고 많으세요~\" 인사에 꽥장군도 웃었어요'", "story: '\"수고 많으세요~\"'"),
 ("story: '집 가는 길을 알려 줬어요'", "story: '길 알려 주고 친구!'"),
 ("story: '\"진짜 가고 싶구나\" 별자리 길을 열어 줬어요'", "story: '별자리 길이 열렸어요'"),
 ("story: '쓰레기통에서 꺼내 줬더니 고마워했어요'", "story: '꺼내 주고 친구!'"),
 ("win: '큰까마귀랑 친구가 됐어요!'", "win: '큰까마귀랑 친구!'"),
 ("win: '꽥장군이 항복했어요!'", "win: '꽥장군이랑 친구!'"),
 ("win: '빙글이가 착해졌어요!'", "win: '빙글이랑 친구!'"),
 ("win: '부엉 할매가 웃었어요!'", "win: '부엉 할매랑 친구!'"),
 ("win: '너굴 대장이 웃었어요!'", "win: '너굴 대장이랑 친구!'"),
 ("G.bannerSub = '이번 보스전은 왕년이가 함께 막아 줘요'", "G.bannerSub = '왕년이가 같이 막아 줘요'"),
 ("G.bannerSub = '다시 1장부터 · 친구들과 한 바퀴 더 (보스가 조금 더 세져요)'", "G.bannerSub = '다시 1장부터!'"),
 ("G.bannerSub = '한 번 부딪혀도 왕년이가 대신 놀라 줘요'", "G.bannerSub = '한 번 막아 줘요'"),
 ("G.bannerSub = `최종 엔딩까지 보스 ${15 - ch * 5}`", "G.bannerSub = ''"),
 ("'앗! 쓰레기통에 머리가 꼈어요'", "'머리 꼈다! 콩!'"),
 ("'으악!! 왕년이가 대신 놀랐어요'", "'으악! 왕년이가 막음'"),
 ("'푹신 방석이 막아 줬어요!'", "'방석 방어!'"),
 ("'푹 쉬었어요 · 하트 +1'", "'하트 +1'"),
 ("'형, 일어나… 무섭단 말이야'", "'형, 일어나…'"),
 ("G.bannerSub = title ? `잠깐 쉬어 가요 · 다음은 ${THEMES[(G.stage - 1) % THEMES.length].name} 풍경` : '잠깐 쉬어 가요 · 새 장애물이 나와요';", "G.bannerSub = '잠깐 쉬어 가요';"),
 ("text(`${Math.floor(P / 5) + 1}장 보스 ${P % 5}/5 · ${ZONES[zoneI()].n} · ${m > 0 ? `보스까지 별자리 ${m}개` : '곧 보스!'}`,", "text(`${Math.floor(P / 5) + 1}장 · 보스 ${P % 5}/5${m > 0 ? '' : ' · 곧 보스!'}`,"),
]
R += [("'창밖 별 하나가 서쪽을 가리켜요'", "'창밖 별 하나가 반짝'"), ("'옆에는 왕년이, 창밖 별 하나가 다시 반짝'", "'옆에는 왕년이'"), ("'마지막 보스 다섯을 넘으면 그날을 만나요'", "'보스 다섯만 더!'"), ("'1장 끝! 다음 보스 다섯은 조금 더 세요'", "'1장 끝!'"), ("'늘 형 뒤에 숨던 왕년이가 처음으로 앞에 섰어요'", "'처음으로 앞에 선 왕년이'")]
for a, b in R:
    assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
n = s.count('기억 조각'); s = s.replace('기억 조각: ', '별: ').replace('기억 조각', '별')
s = s.replace("function memPiece() {", "/* SHORT_V28 */\nfunction memPiece() {", 1)
P.write_text(s, encoding='utf-8'); print('ok', n)
