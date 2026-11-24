#!/usr/bin/env python3
"""풍년이의 모험 v27: 그림일기(그림 9장 반복) 빼기 — 조각을 먹으면 별만 켜짐. 처음 화면 '그림일기' 버튼 숨김.
되살리려면 이 파일이 바꾼 두 곳만 되돌리면 됨 (DIARY·dp 그림 데이터는 남겨 둠)"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'NO_DIARY' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, a[:60]; s = s.replace(a, b)
rep("""  const el = $('polar'); el.classList.add('diary'); el.querySelector('img').src = pageImg(i); el.querySelector('span').innerHTML = `<b>풍년이 일기 ${i + 1}쪽</b>${DIARY[i][1]}`;
  el.classList.remove('show'); void el.offsetWidth; el.classList.add('show'); clearTimeout(polT); polT = setTimeout(() => el.classList.remove('show'), 4200);
""", """  if (!NO_DIARY) { const el = $('polar'); el.classList.add('diary'); el.querySelector('img').src = pageImg(i); el.querySelector('span').innerHTML = `<b>풍년이 일기 ${i + 1}쪽</b>${DIARY[i][1]}`;
  el.classList.remove('show'); void el.offsetWidth; el.classList.add('show'); clearTimeout(polT); polT = setTimeout(() => el.classList.remove('show'), 4200); }
""")
rep("function memPiece() {", "const NO_DIARY = true; // 11-24 대표: 그림 반복이 많아 그림일기는 뺌 (100종 만들면 다시 켜기)\nfunction memPiece() {")
rep('<button class="btn ghost" id="diary-btn">그림일기</button>', '<button class="btn ghost" id="diary-btn" style="display:none">그림일기</button>')
P.write_text(s, encoding='utf-8'); print('ok')
