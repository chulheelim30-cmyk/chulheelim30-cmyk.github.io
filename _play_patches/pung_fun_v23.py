#!/usr/bin/env python3
"""풍년이의 모험 v23 재미 보강 (2026-11-24)
- 보스: 3스테이지마다, 4종 번갈아(큰까마귀 → 꽥장군 → 빙글이 로봇 → 부엉 할매), 밟기(콩!) 공격
- 동네: 보스를 깰 때마다 공원 → 시장 골목 → 지붕 위 → 밤 산책길 (전용 장애물)
- 간식 상점(영구 강화) + 아슬아슬 보너스(콤보)
사용: python3 _play_patches/pung_fun_v23.py  (play/pungnyeon/index.html 직접 수정, 두 번 적용 금지)
"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/pungnyeon/index.html'
s = P.read_text(encoding='utf-8')
if 'BOSS_EVERY' in s:
    print('already applied'); sys.exit(0)

def rep(old, new, cnt=1):
    global s
    n = s.count(old)
    assert n == cnt, (n, old[:80])
    s = s.replace(old, new)

# ---------- CSS + 상점 화면 ----------
rep('#deco-grid{', '#shop-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:4px 0 8px}#shop-grid .dc{padding:6px 6px}#shop-grid .dc span{font-size:11.5px}#shop-grid .dc em{font-style:normal;font-size:13px;color:#c26a10;font-family:"Noto Sans KR",sans-serif;font-weight:700}#shop-grid .dc.max em{color:#2a9a5a}\n#deco-grid{')
rep('<button class="btn ghost" id="deco-btn">꾸미기</button>',
    '<button class="btn ghost" id="shop-btn">🐟 간식 상점</button><button class="btn ghost" id="deco-btn">꾸미기</button>')
rep('<div class="ov" id="deco" hidden',
    '''<div class="ov" id="shop" hidden style="background:rgba(20,14,50,.6)"><div class="card alb">
 <h2>🐟 간식 상점 <small id="shop-n"></small></h2>
 <div class="sub" style="margin:2px 0 6px">달리며 모은 간식으로 풍년이를 영구 강화해요 · 보스를 처음 이기면 간식 100개 선물</div>
 <div id="shop-grid"></div>
 <button class="btn ghost" id="shop-close">닫기</button>
</div></div>
<div class="ov" id="deco" hidden''')

# ---------- 영구 강화·동네 정의 (reset보다 앞에) ----------
rep("const CAT_W = 136; // 화면에 그리는 풍년이 폭\n", r"""const CAT_W = 136; // 화면에 그리는 풍년이 폭
/* 11-24 간식 상점: 영구 강화 (지갑 pa2_coin, 단계 pa2_perm) */
const PERM = [
  { k: 'cushion', icon: '🛋️', n: '푹신 방석', d: '한 판에 한 번, 부딪혀도 괜찮아요', max: 1, cost: () => 300 },
  { k: 'dash', icon: '💨', n: '출발 대시', d: '시작하자마자 3초 무적 질주', max: 1, cost: () => 400 },
  { k: 'mag', icon: '🧲', n: '간식 자석', d: '간식 끌어오는 거리 +20', max: 3, cost: l => 120 * (l + 1) },
  { k: 'yarnT', icon: '🧶', n: '털실공 오래', d: '털실공 친구 +1초', max: 3, cost: l => 150 * (l + 1) },
  { k: 'fever', icon: '🌈', n: '피버 오래', d: '피버 타임 +1초', max: 3, cost: l => 180 * (l + 1) },
  { k: 'snk', icon: '🐟', n: '간식 점수', d: '간식 점수 +10%', max: 5, cost: l => 100 * (l + 1) },
];
let PERM_LV = {}; try { PERM_LV = JSON.parse(localStorage.getItem('pa2_perm') || '{}') || {}; } catch (e) {}
const permL = k => PERM_LV[k] | 0;
let COIN = +(localStorage.getItem('pa2_coin') || 0), coinSave = 0;
function addCoin(n) { COIN += n; G.coinRun = (G.coinRun | 0) + n; if ((coinSave += n) >= 10 || n >= 20) { coinSave = 0; localStorage.setItem('pa2_coin', COIN); } }
/* 11-24 동네: 보스를 깰 때마다 바뀜 */
const ZONES = [
  { n: '호수공원', tint: null },
  { n: '시장 골목', tint: 'rgba(255,150,70,.14)' },
  { n: '지붕 위', tint: 'rgba(100,130,255,.16)' },
  { n: '밤 산책길', tint: 'rgba(16,8,50,.38)' },
];
const zoneI = () => (G.bossWin || 0) % ZONES.length;
""")

rep("tok: Math.random(), nextCard: 50,", "tok: Math.random(), cush: permL('cushion'), combo: 0, nmT: 0, coinRun: 0, nextCard: 50,")

# 구덩이: 보스전(까마귀 제외) 중엔 없음, 지붕 위는 더 넓고 자주
rep("if (!G.demo && Math.random() < 0.45 + diff * 0.2) { gap = Math.round(110 + Math.random() * (40 + diff * 70)); snackArc(genX - 30, gap + 60, 120); }",
    "const roof = zoneI() === 2; if (!G.demo && !(G.boss && G.boss.kind !== 'crow') && Math.random() < 0.45 + diff * 0.2 + (roof ? 0.15 : 0)) { gap = Math.round(110 + (roof ? 30 : 0) + Math.random() * (40 + diff * 70)); snackArc(genX - 30, gap + 60, 120); }")
rep("diffO = diff + Math.min(0.6, Math.floor(((G.stage || 1) - 1) / 10) * 0.3);",
    "diffO = diff + Math.min(0.6, (G.bossWin || 0) * 0.15);")
rep("['bowl', 0.8], ['heart', G.hp < 3 ? 0.5 : 0]];",
    "['bowl', 0.8], ['heart', G.hp < 3 ? 0.5 : 0]]; const z = zoneI(); if (z === 1) pick.push(['bike', 2.6]); if (z === 2) pick.push(['chimney', 2.4]); if (z === 3) pick.push(['bat', 2.8]);")
rep("    case 'heart': objs.push({ t: 'heart', x: x + 60, y: GY - 130 }); return 220;\n",
    """    case 'heart': objs.push({ t: 'heart', x: x + 60, y: GY - 130 }); return 220;
    case 'bike': objs.push({ t: 'bike', x: x + 90 }); snackArc(x + 20, 150, 140); return 300;
    case 'chimney': objs.push({ t: 'chimney', x: x + 90 }); snackArc(x + 20, 150, 170); return 300;
    case 'bat': { const y = GY - 70; objs.push({ t: 'bat', x: x + 380, y, by: y, hp: 1, ph: Math.random() * 6 }); snackLine(x, 3, GY - 18); return 290; }
""")
rep("    case 'cone': return { x0: o.x - 13, x1: o.x + 13, y0: o.y - 24, y1: o.y };\n",
    """    case 'cone': return { x0: o.x - 13, x1: o.x + 13, y0: o.y - 24, y1: o.y };
    case 'bike': return { x0: o.x - 30, x1: o.x + 30, y0: GY - 44, y1: GY };
    case 'chimney': return { x0: o.x - 19, x1: o.x + 19, y0: GY - 76, y1: GY };
    case 'bat': return { x0: o.x - 16, x1: o.x + 16, y0: o.y - 10, y1: o.y + 10 };
    case 'bolt': return { x0: o.x - 12, x1: o.x + 12, y0: o.y - 8, y1: o.y + 8 };
""")

# 속도: 보스 깬 횟수 기준
rep("const loop = Math.floor(((G.stage || 1) - 1) / 10);\n  G.speed = Math.min(600 + Math.min(60, loop * 30),",
    "G.speed = Math.min(600 + Math.min(60, (G.bossWin || 0) * 15),")

# 이동·자석·아슬아슬
rep("    if (o.t === 'goose' && o.x - PX() < LW) o.x -= 120 * dt;\n",
    """    if (o.t === 'goose' && o.x - PX() < LW) o.x -= 120 * dt;
    if (o.t === 'bat') { o.x -= 60 * dt; o.ph += dt * 3.4; o.y = o.by + Math.sin(o.ph) * 26; }
    if (o.t === 'bolt') o.x += o.vx * dt;
""")
rep("mag = fv ? 240 : 52 + upL('mag') * 45;", "mag = fv ? 240 : 52 + upL('mag') * 45 + permL('mag') * 20;")
rep("    if (pb.x1 > box.x0 && pb.x0 < box.x1 && pb.y1 > box.y0 && pb.y0 < box.y1) { if (!o.passed) { o.passed = true; if (fv) { burst(o.x, PL.y - 40, 10, 'spark', FX, 200); } else hurt(); } }\n",
    """    if (pb.x1 > box.x0 && pb.x0 < box.x1 && pb.y1 > box.y0 && pb.y0 < box.y1) { if (!o.passed) { o.passed = true; if (fv) { burst(o.x, PL.y - 40, 10, 'spark', FX, 200); } else hurt(); } }
    else if (!o.passed && NM[o.t]) { // 아슬아슬: 가까이 스쳐 지나가면 보너스
      if (pb.x1 > box.x0 - 6 && pb.x0 < box.x1 + 6) { const gap = Math.max(box.y0 - pb.y1, pb.y0 - box.y1); if (gap > 0 && gap < 24) o.close = true; }
      else if (o.close && !o.nm && box.x1 < pb.x0) { o.nm = true; nearMiss(o); }
    }
""")
rep("  if (!G.demo) stepX(dt);\n", "  G.nmT = Math.max(0, (G.nmT || 0) - dt); if (G.nmT <= 0) G.combo = 0;\n  if (!G.demo) stepX(dt);\n")

# 방석
rep("  if (PL.hurt > 0 || G.fever > 0 || G.demo || G.safe > 0) return;\n",
    "  if (PL.hurt > 0 || G.fever > 0 || G.demo || G.safe > 0) return;\n  G.combo = 0; G.nmT = 0;\n  if (G.cush > 0) { G.cush--; PL.hurt = 1.2; vib(20); sfx('hit'); pop(PX(), PL.y - 96, '푹신 방석이 막아 줬어요!', '#ffe3a0', 18); burst(SX(), PL.y - 36, 14, 'puff', ['#fff', '#ffd8a8'], 170); return; }\n")
rep("const pts = ({ crow: 50, goose: 80 }[o.t] || 30)", "const pts = ({ crow: 50, goose: 80, bat: 60 }[o.t] || 30)")

# 간식 점수·지갑
rep("(1 + upL('snk') * 0.5));", "(1 + upL('snk') * 0.5 + permL('snk') * 0.1)); if (!G.demo) addCoin(big ? 5 : 1);")
rep("G.fever = FEVER_T + upL('fever') * 2;", "G.fever = FEVER_T + upL('fever') * 2 + permL('fever');")
rep("G.fever = 10 + upL('fever') * 2;", "G.fever = 10 + upL('fever') * 2 + permL('fever');")
rep("T = YARN_T + upL('yarnT') * 3,", "T = YARN_T + upL('yarnT') * 3 + permL('yarnT'),")
rep("G.yarn = YARN_T + upL('yarnT') * 3;", "G.yarn = YARN_T + upL('yarnT') * 3 + permL('yarnT');")

# 시작 대시, 게임오버 저장
rep("reset(false); G.state = 'play';", "reset(false); G.state = 'play'; if (permL('dash')) { G.fever = 3; G.bannerTxt = '출발 대시!'; G.bannerSub = '3초 동안 무적 질주'; G.banner = 1.6; }")
rep("function showOver() { ", "function showOver() { localStorage.setItem('pa2_coin', COIN); ")
rep("<span>꿀잠 <b>${G.naps}번</b></span>`;", "<span>꿀잠 <b>${G.naps}번</b></span><span>상점 간식 <b>+${G.coinRun | 0}</b></span>`;")

# 그리기: 새 장애물 + 동네 색 + 보스 위 레이어
rep("      case 'goose': put(ART.goose(Math.floor(G.t * 8) % 2), x + j, GY + 2, { rot: Math.sin(G.t * 16) * 0.04 }); break;\n",
    """      case 'goose': put(ART.goose(Math.floor(G.t * 8) % 2), x + j, GY + 2, { rot: Math.sin(G.t * 16) * 0.04 }); break;
      case 'bike': put(ART.bike(), x, GY + 4); break;
      case 'chimney': put(ART.chimney(), x, GY + 4); if (Math.random() < 0.08) parts.push({ x: o.x - 6, y: GY - 84, vx: -20, vy: -50, life: 1.2, max: 1.2, kind: 'puff', col: '#fff', size: 0.9, rot: 0, vr: 0, g: -10 }); break;
      case 'bat': put(ART.bat(Math.floor(G.t * 12) % 2), x + j, o.y); break;
      case 'bolt': drawBolt(x, o.y); break;
""")
rep("  themeFall();\n  if (G.fever > 0) feverFx();\n", "  themeFall();\n  zoneFx(); bossTop();\n  if (G.fever > 0) feverFx();\n")

# 동네가 바뀌는 쉼터 안내
rep("G.bannerTxt = title || '큰까마귀와 화해했어요'; G.bannerSub = `잠깐 쉬어 가요 · 다음은 ${THEMES[(G.stage - 1) % THEMES.length].name} 풍경`;",
    "G.bannerTxt = title || `다음 동네: ${ZONES[zoneI()].n}`; G.bannerSub = title ? `잠깐 쉬어 가요 · 다음은 ${THEMES[(G.stage - 1) % THEMES.length].name} 풍경` : '잠깐 쉬어 가요 · 새 장애물이 나와요';")
rep("if (G.stage % 10 === 0 && !G.boss) startBoss();", "if (G.stage % BOSS_EVERY === 0 && !G.boss) startBoss();")

# 털실공 목표
rep("const tgtY = o => o === G.boss ? o.y : o.t === 'crow' ? o.y : o.t === 'cone' ? o.y - 12 : GY - 32;",
    "const tgtY = o => o === G.boss ? bossCY(o) : (o.t === 'crow' || o.t === 'bat' || o.t === 'bolt') ? o.y : o.t === 'cone' ? o.y - 12 : GY - 32;")
rep("(o.t === 'crow' || o.t === 'goose' || o.t === 'cone') && o.x > PX() + 10",
    "(o.t === 'crow' || o.t === 'goose' || o.t === 'cone' || o.t === 'bat' || o.t === 'bolt') && o.x > PX() + 10")
rep("const pts = ({ crow: 50, goose: 80, cone: 20 }[o.t] || 30)", "const pts = ({ crow: 50, goose: 80, cone: 20, bat: 60, bolt: 20 }[o.t] || 30)")
rep("(o.t === 'crow' ? '쿨쿨… ' : o.t === 'goose' ? '꽥! 도망~ ' : '')", "(o.t === 'crow' || o.t === 'bat' ? '쿨쿨… ' : o.t === 'goose' ? '꽥! 도망~ ' : '')")

# ---------- 보스 블록 통째 교체 ----------
a = s.index('/* 보스: 심술 큰까마귀 — 10스테이지마다 */')
b = s.index('/* 능력 카드: 간식 50개마다 3장 중 1장 */')
BOSS = (pathlib.Path(__file__).resolve().parent / 'pung_boss_v23.js').read_text(encoding='utf-8')
s = s[:a] + BOSS + s[b:]

# 상점 열기 (꾸미기 다음)
rep("$('deco-btn').addEventListener('click', openDeco);",
    r"""function openShop() {
  localStorage.setItem('pa2_coin', COIN);
  $('shop-grid').innerHTML = PERM.map(p => { const l = permL(p.k), mx = l >= p.max, c = mx ? 0 : p.cost(l), ok = !mx && COIN >= c;
    return `<button class="dc${mx ? ' max on' : ''}${ok || mx ? '' : ' lock'}" data-k="${p.k}" ${ok ? '' : 'disabled'}><i>${p.icon}</i><b>${p.n} ${p.max > 1 ? `${l}/${p.max}` : ''}</b><span>${p.d}</span><em>${mx ? '완료' : `🐟 ${c.toLocaleString()}`}</em></button>`; }).join('');
  $('shop-n').textContent = `가진 간식 ${COIN.toLocaleString()}개`; $('shop').hidden = false;
}
$('shop-grid').addEventListener('click', e => { const b = e.target.closest('.dc'); if (!b || b.disabled) return; const p = PERM.find(p => p.k === b.dataset.k), l = permL(p.k); if (l >= p.max) return; const c = p.cost(l); if (COIN < c) return;
  COIN -= c; PERM_LV[p.k] = l + 1; localStorage.setItem('pa2_coin', COIN); localStorage.setItem('pa2_perm', JSON.stringify(PERM_LV)); sfx('big'); openShop(); });
$('shop-btn').addEventListener('click', openShop); $('shop-close').addEventListener('click', () => { $('shop').hidden = true; });
$('deco-btn').addEventListener('click', openDeco);""")

rep("window.__G = G;", "window.__G = G; window.__startBoss = startBoss; window.__shop = { addCoin, openShop, PERM_LV }; window.__objsPush = o => objs.push(o);")
P.write_text(s, encoding='utf-8')
print('ok', len(s))
