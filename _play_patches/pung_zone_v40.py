#!/usr/bin/env python3
"""풍년이의 모험 v40: 구역 배경 그림(시장 골목·지붕 위·강 다리) + 장애물 그림(자전거·고깔·굴뚝·박쥐)"""
import sys, json, pathlib
D = pathlib.Path(__file__).resolve().parent
P = D.parent / 'play/pungnyeon/index.html'; s = P.read_text(encoding='utf-8')
if 'ZONEART_V40' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
art = json.load(open(D / 'pung_art_v40.json'))
i = s.index('const IMG = {};')
s = s[:i] + '/* ZONEART_V40 */ Object.assign(SPR,' + json.dumps(art, separators=(',', ':')) + ');\n' + s[i:]
rep("  { n: '시장 골목', tint: 'rgba(255,150,70,.14)' },\n  { n: '지붕 위', tint: 'rgba(100,130,255,.16)' },",
    "  { n: '시장 골목', tint: 'rgba(255,150,70,.14)', bg: 'market' },\n  { n: '지붕 위', tint: 'rgba(100,130,255,.16)', bg: 'roof' },")
rep("  { n: '강 다리', tint: 'rgba(90,150,210,.14)' },", "  { n: '강 다리', tint: 'rgba(90,150,210,.14)', bg: 'bridge' },")
rep("const SEASON = ['sunset', 'night', 'spring', 'snow'];", "const SEASON = ['sunset', 'night', 'spring', 'snow', 'market', 'roof', 'bridge'];")
rep("  const want = G.state === 'home' ? 0 : (G.stage - 1) % SEASON.length;",
    "  const zb = G.state !== 'home' && !G.demo && ZONES[zoneI()].bg, zw = zb && bgLayer(zb) ? SEASON.indexOf(zb) : -1;\n  const want = G.state === 'home' ? 0 : zw >= 0 ? zw : (G.stage - 1) % 4;")
rep("  if (Z.tint) { ctx.fillStyle = Z.tint;", "  if (Z.tint && !(Z.bg && bgLayer(Z.bg))) { ctx.fillStyle = Z.tint;")
rep("});\n/* 능력 카드: 간식 50개마다 3장 중 1장 */",
    "});\n{ const wrap = (k, f) => { const old = ART[k]; ART[k] = (...a) => f(...a) || old(...a); }; // 구역 장애물 그림 (ZONEART_V40)\n  wrap('bike', () => imgArt('o_bike', 80, 54, 0.5, 1));\n  wrap('tcone', () => imgArt('o_tcone', 40, 46, 0.5, 1));\n  wrap('chimney', () => imgArt('o_chimney', 56, 82, 0.5, 1));\n  wrap('bat', f => imgArt('o_bat', 56, 36, 0.5, 0.5, false, f ? 0.72 : 0)); }\n/* 능력 카드: 간식 50개마다 3장 중 1장 */")
rep("{ name: '눈 오는 날', k: 'snow' }];", "{ name: '눈 오는 날', k: 'snow' }, { name: '시장 골목', k: 'market' }, { name: '지붕 위', k: 'roof' }, { name: '강 다리', k: 'bridge' }];")
rep("(G.stage - 1) % THEMES.length;", "(G.stage - 1) % 4;")
P.write_text(s, encoding='utf-8'); print('ok')
