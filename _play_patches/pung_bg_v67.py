# v67 풍년이의 모험: Bing 배경 5장을 동네 배경으로
# 지붕 위(3장)·강 다리(5장)는 그림 파일이 없어 색만 덮었고, 빗물 골목·은행잎 숲길·바람 부는 언덕(6~8장)은 '그림 오기 전' 색·효과뿐이었음
# → bg_roof·bg_bridge·bg_rain·bg_ginkgo·bg_hill 넣기 (그림: _art_new/bg, Bing 장 표지 그림에서 남산타워·글자 없는 판 골라 자름)
# + 미리보기: 주소 끝에 ?ch=7 처럼 붙이면 그 장 동네로 시작, ?ch=6&boss=5 는 그 장 5번째 보스가 바로 나옴(저장된 진행은 안 바뀜)
import base64
P = 'play/pungnyeon/index.html'
A = '_art_new/bg/'
s = open(P, encoding='utf8').read()
def rep(o, n):
    global s
    assert s.count(o) == 1, ('못 찾음/여러 개', s.count(o), o[:90]); s = s.replace(o, n)
def spr(k, f):
    from PIL import Image
    im = Image.open(A + f); return f'"{k}": {{"src": "data:image/webp;base64,{base64.b64encode(open(A + f, "rb").read()).decode()}", "w": {im.width}, "h": {im.height}}}'
if 'BG_V67' not in s:
    rep("/* DECOIMG_V40 */ Object.assign(SPR,{",
        "/* BG_V67 */ Object.assign(SPR,{" + ', '.join(spr('bg_' + k, f'bg_{k}.webp') for k in ['roof', 'bridge', 'rain', 'ginkgo', 'hill']) + "});\n/* DECOIMG_V40 */ Object.assign(SPR,{")
    rep("const SEASON = ['sunset', 'night', 'spring', 'snow', 'market', 'roof', 'bridge'];", "const SEASON = ['sunset', 'night', 'spring', 'snow', 'market', 'roof', 'bridge', 'rain', 'ginkgo', 'hill'];")
    rep("{ name: '강 다리', k: 'bridge' }];", "{ name: '강 다리', k: 'bridge' }, { name: '빗물 골목', k: 'rain' }, { name: '은행잎 숲길', k: 'ginkgo' }, { name: '바람 부는 언덕', k: 'hill' }];")
    rep("{ n: '빗물 골목', tint: 'rgba(60,90,140,.26)', base: 2, fx: 'rain' },", "{ n: '빗물 골목', tint: 'rgba(60,90,140,.26)', base: 2, fx: 'rain', bg: 'rain' },")
    rep("{ n: '은행잎 숲길', tint: 'rgba(255,190,40,.18)', base: 0, fx: 'leaf' },", "{ n: '은행잎 숲길', tint: 'rgba(255,190,40,.18)', base: 0, fx: 'leaf', bg: 'ginkgo' },")
    rep("{ n: '바람 부는 언덕', tint: 'rgba(255,200,140,.14)', base: 0, fx: 'wind' },", "{ n: '바람 부는 언덕', tint: 'rgba(255,200,140,.14)', base: 0, fx: 'wind', bg: 'hill' },")
    # 미리보기 ?ch=N (1~10)
    rep("const progN = () => (+(localStorage.getItem('pa2_prog') || 0)) % TOT;",
        "const CHQ = Math.max(0, Math.min(10, +(new URLSearchParams(location.search).get('ch')) || 0)); // ?ch=7 미리보기\n"
        "const BQ = Math.max(0, Math.min(5, +(new URLSearchParams(location.search).get('boss')) || 0)); // ?ch=6&boss=5 → 그 장 5번째 보스로 바로\n"
        "const progN = () => CHQ ? (CHQ - 1) * 5 + (BQ ? BQ - 1 : 0) : (+(localStorage.getItem('pa2_prog') || 0)) % TOT;")
    rep("const P = bIdx() % TOT; localStorage.setItem('pa2_prog', P);", "const P = bIdx() % TOT; if (!CHQ) localStorage.setItem('pa2_prog', P);")
    rep("function start() { try { PungRank.start(); } catch (e) {}", "function start() { if (CHQ && BQ) setTimeout(() => { if (G.state === 'play' && !G.boss) startBoss(); }, 1800); try { PungRank.start(); } catch (e) {}")
    open(P, 'w', encoding='utf8').write(s); print('OK')
