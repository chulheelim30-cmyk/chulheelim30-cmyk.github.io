# 쇼츠 만드는 법 (1화 v5 · 2화 v1, 11-26)
- 필요: python3 + pillow numpy opencv-python-headless, ffmpeg, Jua 글꼴(Jua-Regular.ttf)
- A 폴더 = 게임 index.html 속 그림(games/pungadventure/v3/index.html에서 data:image 뽑기)
- 1화: x4 그림을 png로 /home/claude/assets_x4, Canva 장면 clips/ep1_crow_canva.mp4 → /home/claude/canva/frames/%04d.jpg(1080x1920 꽉 채움) + clip.wav
  `python3 ep1_v5.py A Jua.ttf out.mp4` (끝에 `1.5,10`처럼 초를 주면 미리보기 jpg만)
- 2화: X4B=x4_ep2 를 png로 푼 폴더 `X4B=... python3 ep2.py A Jua.ttf out.mp4`
- alive.py: 살아 있는 배경(LivingBG 노을/밤 호수공원, MarketBG 시장 골목), 입자(낙엽·꽃잎·빛 알갱이·반딧불), sway(캐릭터 숨쉬기 기울임)
- 풍년이(코랫)는 살아 있음: 추모·하늘나라 표현 금지
