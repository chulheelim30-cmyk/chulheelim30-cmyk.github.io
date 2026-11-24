#!/usr/bin/env python3
"""풍년이의 모험 v26 (2): 왕년이 그림 6종 추가 — 꿀잠 깨우기, 쉼터 그루밍·츄르, 부엉 할매 땐 가로등 뒤, 3장 마지막 보스 전 '용기' 컷, 엔딩 머리 콩 + 창가로 돌아오기
순서: … → pung_chapter_v26.py → 이 파일"""
import sys, pathlib
D = pathlib.Path(__file__).resolve().parent
P = D.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'w_wake' in s and 'braveScenes' in s: print('already'); sys.exit(0)
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)
i = s.index('Object.assign(SPR,{"w_'); j = s.index('</script>', i) + 9
s = s[:j] + '\n<script>Object.assign(SPR,' + (D / 'pung_wang2_spr.json').read_text() + ');</script>' + s[j:]
# 꿀잠 → 왕년이가 깨움 (2.6초 → 1.8초)
rep("G.napWant = false; G.nap = 2.6;", "G.napWant = false; G.nap = 1.8; G.napT0 = 1.8;")
rep("G.bannerTxt = '다시 출발!'; G.bannerSub = '꿀잠 자고 하트 +1';", "G.bannerTxt = '다시 출발!'; G.bannerSub = '왕년이가 깨워 줬어요 · 하트 +1';")
rep("  if (!(G.wang > 0) && !(G.wangOut > 0)) return; const hide = G.boss && G.boss.hp > 0;",
    """  if (G.nap > 0) { // 꿀잠: 동생이 달려와 톡톡
    const e = (G.napT0 || 1.8) - G.nap, arrive = Math.min(1, e / 0.6), x = SX() - 250 + arrive * 175, key = arrive < 1 ? 'w_run' + (Math.floor(G.t * 10) % 2) : 'w_wake', h = arrive < 1 ? 78 : 66;
    if (arrive >= 1 && !G.napSaid) { G.napSaid = true; pop(PX() + 30, GY - 125, '형, 일어나… 무섭단 말이야', '#ffffff', 16); }
    const im = IMG[key]; if (im && im.complete && im.naturalWidth) { const w = im.naturalWidth * h / im.naturalHeight; ctx.drawImage(im, x - w / 2, GY + 4 - h - (arrive >= 1 ? Math.abs(Math.sin(G.t * 9)) * 3 : 0), w, h); }
    return;
  }
  G.napSaid = false;
  if (!(G.wang > 0) && !(G.wangOut > 0)) return; const hide = G.boss && G.boss.hp > 0 && !G.braveB;""")
rep("else if (hide) { key = 'w_box'; h = 70;", "else if (hide) { key = G.boss.kind === 'owl' ? 'w_pole' : 'w_box'; h = G.boss.kind === 'owl' ? 92 : 70;")
# 쉼터: 잠·그루밍·츄르 중 하나
rep("objs.push({ t: 'sign', x: PX() + LW * 0.75 });", "objs.push({ t: 'sign', x: PX() + LW * 0.75, wp: Math.random() < 0.55 ? 'w_sleep' : Math.random() < 0.6 ? 'w_groom' : 'w_churu' });")
rep("const im = IMG.w_sleep; if (!(G.wang > 0) && im && im.complete && im.naturalWidth) { const h = 46,", "const im = IMG[o.wp || 'w_sleep']; if (!(G.wang > 0) && im && im.complete && im.naturalWidth) { const h = (o.wp || 'w_sleep') === 'w_sleep' ? 46 : 64,")
# 3장 마지막(15번째) 보스 전: 왕년이의 용기
rep("function startBoss() {", """function braveScenes() {
  return [
    { d: 3.4, k: 'card', bg: 'bg_night', chars: [['c_daze', 0.36, 0.34], ['w_pole', 0.64, 0.36]], cap: '마지막 친구 앞에서 다리가 덜덜…', sub: '' },
    { d: 3.8, k: 'card', bg: 'bg_sunset', chars: [['c_wave', 0.34, 0.34], ['w_sit', 0.62, 0.42]], cap: '"이번엔… 내가 형 지켜 줄게."', sub: '늘 형 뒤에 숨던 왕년이가 처음으로 앞에 섰어요' },
  ];
}
function startBoss() {
  if (bIdx() % 15 === 14 && !G.braveDone && !G.demo) { G.braveDone = true; G.state = 'story'; slideHeld = false; opOpen(false, braveScenes(), 'chap', () => { G.state = 'play'; G.braveB = true; G.wang = 99; G.wangOut = 0; startBoss0(); G.bannerSub = '이번 보스전은 왕년이가 함께 막아 줘요'; }); return; }
  startBoss0();
}
function startBoss0() {""")
rep("function wangHurt() { if (!(G.wang > 0) || G.boss) return false;", "function wangHurt() { if (!(G.wang > 0) || (G.boss && !G.braveB)) return false; if (G.braveB) { G.wang = 99; PL.hurt = 1.2; vib(25); sfx('hit'); pop(PX() - 90, PL.y - 120, '왕년이가 막아 줬어요!', '#ffffff', 18); burst(SX() - 90, GY - 50, 14, 'puff', ['#fff'], 200); return true; }")
rep("B.out = 0; B.stomp = false; G.bonus += bon; G.bossWin++;", "B.out = 0; B.stomp = false; G.bonus += bon; G.bossWin++; if (G.braveB) { G.braveB = false; G.wang = 3; }")
# 1장 끝 컷, 엔딩
rep("chars: [['c_daze', 0.38, 0.36], ['w_scare', 0.66, 0.34]], cap: '뒤에서 누가 따라오는데…?'", "chars: [['c_daze', 0.38, 0.36], ['w_pole', 0.66, 0.36]], cap: '뒤에서 누가 따라오는데…?'")
rep("chars: [['c_yay', 0.38, 0.36], ['w_run1', 0.64, 0.28]], cap: '\"혼자 있으면 무섭잖아…\"', sub: '왕년이랑 같이 가기로 했어요'", "chars: [['c_yay', 0.36, 0.36], ['w_sit', 0.64, 0.42]], cap: '\"형… 혼자 있으면 무섭단 말이야\"', sub: '둘이 같이 가기로 했어요'")
rep("cap: '벤치 앞에서 누가 불렀어요', sub: '\"풍년아!\"' },", "cap: '벤치 앞에서 누가 불렀어요', sub: '\"풍년아! 왕년아!\"' },")
rep("    { d: 5.0, k: 'love', cap: `${ordOf(m)} 만남`, sub: '몇 번이라도, 여기서 다시 만나요' },",
    "    { d: 5.0, k: 'love', cap: `${ordOf(m)} 만남`, sub: '몇 번이라도, 여기서 다시 만나요' },\n    { d: 4.2, k: 'home', wake: true, cap: '창가에서 눈을 떴어요', sub: '옆에는 왕년이, 창밖 별 하나가 다시 반짝' },")
rep("opImg(g, 'c_love', W * 0.4, H * 0.92, H * 0.42); opImg(g, 'w_box', W * 0.66, H * 0.92, H * 0.28);", "opImg(g, 'c_love', W * 0.38, H * 0.92, H * 0.42); opImg(g, 'w_nuzzle', W * 0.64, H * 0.92, H * 0.34);")
rep("    const up = p > 0.35; opImg(g, up ? 'c_wave' : 'c_doze', W * 0.36, H * 0.92, H * 0.36);", "    const up = !S.wake && p > 0.35; opImg(g, S.wake ? 'c_sleep' : up ? 'c_wave' : 'c_doze', W * 0.36, H * 0.92, S.wake ? H * 0.24 : H * 0.36);")
rep("cush: permL('cushion'), p0: progN(),", "cush: permL('cushion'), p0: progN(), braveDone: false, braveB: false, napSaid: false,")
P.write_text(s, encoding='utf-8'); print('ok')
