# v68 풍년이의 모험: 대표 피드백(11-25 21:37~22:42)
# 1) 단계 구조: 50단계 = 보스 10명 × 레벨 5. 1~10단계 레벨1, 11~20단계 레벨2 … 41~50단계 레벨5
#    단계마다 보스 한 명(1단계 큰까마귀 → 10단계 달토끼 순서), 동네·배경도 단계마다(보스 10명 ↔ 배경 10장)
#    보스는 2구간마다(예전 3구간마다) → 50단계 여행이 더 빨리 돌아가요
# 2) 10단계마다 이야기 이벤트, 모두 5번: 1~4번은 옛 장 끝 장면을 둘씩 묶어서, 5번째(50단계)는 꿈에서 깨는 엔딩
# 3) 배경 10장을 단계마다 고르게: 공원(노을)·시장·지붕·밤길·강 다리·빗물 골목·은행잎·바람 언덕·눈 놀이터·별자리 길(벚꽃)
# 4) 피버 더 드물고 짧게: 8초 → 5초, 게이지 간식 0.55 → 0.35, 큰 간식 8 → 5
# 5) 난이도 올리기: 시작 속도 340 → 380, 장애물 오르막 45000 → 32000, 배부름 75초 → 62초, 부딪힘 -28 → -32
# 6) 전체화면 버튼(처음 화면 오른쪽 위 ⛶). 켜 두면 '달리기 시작'할 때도 전체화면으로. 아이폰 사파리는 홈 화면에 추가 안내
P = 'play/pungnyeon/index.html'
s = open(P, encoding='utf8').read()
def rep(o, n, cnt=1):
    global s
    assert s.count(o) == cnt, ('못 찾음/여러 개', s.count(o), o[:90]); s = s.replace(o, n)
if 'STAGE_V68' not in s:
    # 1) 동네 = 단계 % 10, 보스 = 단계 % 10, 레벨 = 단계 / 10
    rep("const zoneI = () => chOf(bIdx()); // 장마다 동네 하나", "const zoneI = () => (((bIdx() % TOT) + TOT) % TOT) % 10; // STAGE_V68: 단계마다 동네(보스) 하나\nconst lvOf = i => Math.floor((((i % TOT) + TOT) % TOT) / 10);")
    i = s.index("function bossAt(idx) {"); j = s.index("\n}", i) + 2
    s = s[:i] + "function bossAt(idx) { return CH_FRIEND[(((idx % TOT) + TOT) % TOT) % 10]; } // STAGE_V68: 1단계 큰까마귀 … 10단계 달토끼, 11단계부터 레벨2로 다시\n" + s[j:]
    rep("lv = Math.min(5, 1 + Math.floor(chOf(idx) / 2) + Math.min(2, meetN()))", "lv = Math.min(5, 1 + lvOf(idx) + Math.min(1, meetN()))")
    rep("const BOSS_EVERY = 3;", "const BOSS_EVERY = 2;")
    # 시작 알림: 단계·동네·레벨
    rep("G.bannerTxt = `${c + 1}장 · ${CH[c]}`; G.bannerSub = `보스 ${P % 5}/5`;",
        "G.bannerTxt = `${P + 1}단계 · ${ZONES[P % 10].n}`; G.bannerSub = `레벨 ${Math.floor(P / 10) + 1} · ${(NEWF[bossAt(P)] || BOSSES[bossAt(P)]).n}`;")
    # 2) 이벤트: 10단계마다
    rep("const ch = P % 5 === 0 ? (P === 0 ? 10 : P / 5) : 0; setTimeout(() => { if (G.state !== 'play' || G.demo) return; if (ch === 10) storyEnding(); else if (ch) storyChapter(ch); else startRest(G.stage - 1, ''); }, ch ? 2400 : 3200);",
        "const ev = P % 10 === 0 ? (P === 0 ? 5 : P / 10) : 0; setTimeout(() => { if (G.state !== 'play' || G.demo) return; if (ev === 5) storyEnding(); else if (ev) storyEvent(ev); else startRest(G.stage - 1, ''); }, ev ? 2400 : 3200);")
    rep("function storyChapter(ch) {", """function storyEvent(e) { // STAGE_V68: 10단계마다 이벤트(1~4), 옛 장 끝 장면을 둘씩 묶음 → 다음 레벨 표지
  const pick = c => chapterScenes(c).filter(x => x.k !== 'chapter').slice(0, 2), Z = ZONES[(e * 10) % 10];
  const cover = { d: 3.6, k: 'chapter', bg: coverK(e * 2), cap: `레벨 ${e + 1} 시작!`, sub: `${e * 10}단계 클리어 · 친구들이 조금 더 세졌어요` };
  G.state = 'story'; slideHeld = false;
  opOpen(false, pick(e * 2 - 1).concat(pick(e * 2), [cover]), 'chap', () => { G.state = 'play'; PL.hurt = 1.5; startRest(G.stage - 1, ''); G.banner = 2.6; G.bannerTxt = `레벨 ${e + 1} · ${e * 10 + 1}단계`; G.bannerSub = Z.n; });
}
function storyChapter(ch) {""")
    # 3) 배경 10장 고르게
    rep("{ n: '동네 공원', tint: null }", "{ n: '동네 공원', tint: null, bg: 'sunset' }")
    rep("{ n: '밤 산책길', tint: 'rgba(16,8,50,.38)' }", "{ n: '밤 산책길', tint: 'rgba(16,8,50,.38)', bg: 'night' }")
    rep("{ n: '별자리 길', tint: 'rgba(16,8,50,.40)', base: 1, fx: 'firefly' }", "{ n: '별자리 길', tint: 'rgba(16,8,50,.40)', base: 1, fx: 'firefly', bg: 'spring' }")
    # 4) 피버
    rep("const FEVER_T = 8;", "const FEVER_T = 5;")
    rep("if (!o.nog) addGauge(big ? 8 : 0.55);", "if (!o.nog) addGauge(big ? 5 : 0.35);")
    # 5) 난이도
    rep("340 + prD() * 140 + G.dist * 0.005", "380 + prD() * 140 + G.dist * 0.0055")
    rep("diff = Math.min(1, G.dist / 45000 + pd * 0.7)", "diff = Math.min(1, G.dist / 32000 + pd * 0.7)")
    rep("const FOOD_DRAIN = 100 / 75;", "const FOOD_DRAIN = 100 / 62;")
    rep("G.food = Math.max(0, (G.food || 0) - 28)", "G.food = Math.max(0, (G.food || 0) - 32)")
    # 6) 전체화면
    rep('<div class="ov" id="home"><div class="home">',
        '<div class="ov" id="home"><button id="fsbtn" aria-label="전체화면" style="position:absolute;top:max(10px,env(safe-area-inset-top));right:max(12px,env(safe-area-inset-right));z-index:5;border:0;border-radius:12px;padding:8px 12px;font:700 15px/1 inherit;color:#fff;background:rgba(40,24,80,.55);backdrop-filter:blur(4px)">⛶ 전체화면</button><div class="home">')
    rep("function start() {", """const FS = { can: () => !!(document.documentElement.requestFullscreen || document.documentElement.webkitRequestFullscreen), on: () => !!(document.fullscreenElement || document.webkitFullscreenElement),
  go() { const el = document.documentElement; try { const p = (el.requestFullscreen || el.webkitRequestFullscreen).call(el, { navigationUI: 'hide' }); if (p && p.then) p.then(() => { try { screen.orientation && screen.orientation.lock && screen.orientation.lock('landscape').catch(() => {}); } catch (e) {} }).catch(() => {}); } catch (e) {} },
  off() { try { (document.exitFullscreen || document.webkitExitFullscreen).call(document); } catch (e) {} } };
function fsLabel() { const b = document.getElementById('fsbtn'); if (b) b.textContent = FS.on() ? '⛶ 전체화면 끄기' : '⛶ 전체화면'; }
document.addEventListener('fullscreenchange', fsLabel); document.addEventListener('webkitfullscreenchange', fsLabel);
document.getElementById('fsbtn').addEventListener('click', e => { e.stopPropagation();
  if (!FS.can()) { alert('이 기기에선 브라우저 전체화면이 안 돼요.\\n공유 버튼 → "홈 화면에 추가"로 앱처럼 꽉 찬 화면으로 즐겨 주세요!'); return; }
  if (FS.on()) { FS.off(); localStorage.setItem('pa2_fs', '0'); } else { FS.go(); localStorage.setItem('pa2_fs', '1'); } });
function start() { if (localStorage.getItem('pa2_fs') === '1' && FS.can() && !FS.on()) FS.go();""")
    # 미리보기: ?stage=23 (1~50) → 그 단계로 시작, &boss=1 이면 보스 바로 (?ch=N 은 N*10-9단계로)
    rep("const progN = () => CHQ ? (CHQ - 1) * 5 + (BQ ? BQ - 1 : 0) : (+(localStorage.getItem('pa2_prog') || 0)) % TOT;",
        "const SQ = Math.max(0, Math.min(50, +(new URLSearchParams(location.search).get('stage')) || 0));\n"
        "const progN = () => SQ ? SQ - 1 : CHQ ? (CHQ - 1) * 5 + (BQ ? BQ - 1 : 0) : (+(localStorage.getItem('pa2_prog') || 0)) % TOT;")
    rep("if (!CHQ) localStorage.setItem('pa2_prog', P);", "if (!CHQ && !SQ) localStorage.setItem('pa2_prog', P);")
    rep("if (CHQ && BQ) setTimeout(", "if ((CHQ || SQ) && BQ) setTimeout(")
    open(P, 'w', encoding='utf8').write(s); print('OK')
