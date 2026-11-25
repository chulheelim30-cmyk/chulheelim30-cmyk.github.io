# v69 풍년이의 모험: 피버 때 망토 두른 풍년이 그림(Bing, 망토와 고양이가 한 그림) 4장으로 달리기
# - 땅에서 달릴 때만(점프·앉기·부딪힘은 원래 그림 + 망토 따로)
# 그림: _art_new/cape_cat/fc0~3.webp
import base64
P = 'play/pungnyeon/index.html'
A = '_art_new/cape_cat/'
s = open(P, encoding='utf8').read()
def rep(o, n):
    global s
    assert s.count(o) == 1, ('못 찾음/여러 개', s.count(o), o[:90]); s = s.replace(o, n)
def spr(k, f, dw):
    from PIL import Image
    im = Image.open(A + f); return f'"{k}": {{"src": "data:image/webp;base64,{base64.b64encode(open(A + f, "rb").read()).decode()}", "w": {im.width}, "h": {im.height}, "dw": {round(dw * im.width / 300)}}}'
if 'CAPECAT_V69' not in s:
    rep("/* DECOIMG_V40 */ Object.assign(SPR,{",
        "/* CAPECAT_V69 */ Object.assign(SPR,{" + ', '.join(spr(f'fc{i}', f'fc{i}.webp', 150) for i in range(4)) + "});\n/* DECOIMG_V40 */ Object.assign(SPR,{")
    rep("  if (f.startsWith('c_') && !(IMG[f]",
        "  G.fcOn = false; if (G.fever > 0 && G.state === 'play' && PL.ground && !PL.slide && !(PL.hurt > 1.0) && IMG.fc0 && IMG.fc0.complete && IMG.fc0.naturalWidth) { f = 'fc' + (Math.floor(PL.anim * 1.4) % 4); G.fcOn = true; }\n"
        "  if (f.startsWith('c_') && !(IMG[f]")
    rep("if (!(G.fever > 0) || G.state !== 'play' ||", "if (G.fcOn || !(G.fever > 0) || G.state !== 'play' ||")
    open(P, 'w', encoding='utf8').write(s); print('OK')
