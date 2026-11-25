#!/usr/bin/env python3
"""블락풍 v65: '올 클리어 기회'를 크레용 새 화면에 다시 넣기 (v37 일부 + v44 blockpung_acplan_v44.py)
- 판에 칸이 30개 이하로 남으면, 새 블록 3개를 줄 때 판을 싹 비울 수 있는 조합을 찾아 우선으로 줘요(빔 탐색, 최대 0.18초)
- 찾으면 '올 클리어 기회!' 알림, 4초 머뭇거리면 다음 놓을 자리가 노랗게 빛나요(계획대로 놓을 때만 이어짐, 돌리기도 반영)
- 올 클리어 보상 +300 → +1000, 축하 연출 크게
"""
import pathlib, sys
P = pathlib.Path(__file__).resolve().parent.parent / 'play/blockpung/index.html'; s = P.read_text(encoding='utf-8')
if 'ACPLAN_V65' in s: print('already'); sys.exit(0)
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:80]); s = s.replace(a, b)
rep("function newTray() {", r"""/* ACPLAN_V65 올 클리어 기회 */
const PERMS3 = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]], shKey = sh => JSON.stringify(sh.cells);
function findAllClear(b) { // 판을 싹 비울 블록 3개 + 놓을 자리 (순서 6가지 × 상위 6개 판을 이어 보는 빔 탐색)
  const b0 = b.map(r => r.map(x => !!x)), t0 = performance.now();
  const conc = nb => { let s = 0; for (let r = 0; r < N; r++) { let k = 0; for (let c = 0; c < N; c++) if (nb[r][c]) k++; s += k * k; } for (let c = 0; c < N; c++) { let k = 0; for (let r = 0; r < N; r++) if (nb[r][c]) k++; s += k * k; } return s; };
  const pool = SHAPES.filter(x => x.cells.length <= 6), hit = pool.filter(x => clearsLine(b0, x)), pick = a => a[Math.floor(Math.random() * a.length)];
  for (let t = 0; t < 200 && performance.now() - t0 < 180; t++) {
    const cand = t % 2 && hit.length ? [pick(hit), pick(pool), pick(pool)] : [pick(pool), pick(pool), pick(pool)];
    if (new Set(cand.map(x => x.id)).size < 3) continue;
    for (const ord of PERMS3) {
      let beam = [{ nb: b0, path: [] }];
      for (const i of ord) { const sh = cand[i], next = [];
        for (const e of beam) for (let r = 0; r <= N - sh.h; r++) for (let c = 0; c <= N - sh.wd; c++) { if (!fits(e.nb, sh, r, c)) continue; const a = boardAfter(e.nb, sh, r, c); let f = 0; for (const rr of a.nb) for (const x of rr) if (x) f++;
          const path = e.path.concat([{ k: shKey(sh), id: sh.id, r, c }]);
          if (f === 0 && a.lines) return { set: cand, plan: path };
          next.push({ nb: a.nb, path, v: a.lines * 200 - f * 6 + conc(a.nb) }); }
        if (!next.length) { beam = null; break; }
        next.sort((x, y) => y.v - x.v); beam = next.slice(0, 6);
      }
    }
  }
  return null;
}
function newTray() {""")
rep("  let set = null;\n  for (let tries = 0; tries < 40; tries++) {",
    "  let set = null, ac = null; G.acPlan = null;\n  if (fill > 0 && fill <= 30) { ac = findAllClear(b); if (ac) { set = ac.set; G.acPlan = ac.plan; G.acT = G.t; G.acFound = (G.acFound || 0) + 1; if (G.state === 'play') fxPop('올 클리어 기회!', L.W / 2, L.by - 14, { size: 24, rainbow: true, life: 1.8 }); } }\n"
    "  for (let tries = 0; tries < 40 && !set; tries++) {")
# 놓을 때: 계획대로면 다음 단계, 아니면 계획 취소
rep("function place(i, gr, gc) {\n  const pc = G.tray[i]; G.tray[i] = null;",
    "function place(i, gr, gc) {\n  const pc = G.tray[i]; G.tray[i] = null;\n  if (G.acPlan) { const st = G.acPlan[0]; if (st && st.k === shKey(pc.sh) && st.r === gr && st.c === gc) { G.acPlan.shift(); G.acT = G.t; if (!G.acPlan.length) G.acPlan = null; } else G.acPlan = null; }")
# 보상
rep("""      G.score += 300; SND.sweep(); fxConfetti(80); fxFlash(0.5, '255,220,90'); JE.shake.add(12);
      fxPop('판 싹쓸이! +300', L.W / 2, L.by + L.bs * 0.35, { size: 42, rainbow: true, life: 1.6, delay: 0.25 });""",
    """      G.score += 1000; G.allClear = (G.allClear || 0) + 1; SND.sweep(); fxConfetti(140); fxFlash(0.6, '255,220,90'); JE.shake.add(14); JE.haptic('success');
      fxPop('올 클리어!', L.W / 2, L.by + L.bs * 0.32, { size: 52, rainbow: true, life: 1.8, delay: 0.2 });
      fxPop('+1000', L.W / 2, L.by + L.bs * 0.32 + 56, { size: 34, c1: '#fff', c2: '#ffd23f', life: 1.6, delay: 0.35 });""")
# 힌트: 4초 머뭇거리면 다음 자리 빛 (계획한 모양이 대기칸에 있을 때만)
rep("  // 놓기 미리보기: 지워질 줄 테두리 빛",
    """  if (G.acPlan && G.acPlan.length && !G.drag && G.state === 'play' && G.t - (G.acT || 0) > 4) { const st = G.acPlan[0], tp = G.tray.find(t => t && shKey(t.sh) === st.k);
    if (tp) { const a = 0.35 + 0.25 * Math.sin(G.t * 5); c.save(); c.shadowColor = 'rgba(255,220,90,.95)'; c.shadowBlur = 16; c.strokeStyle = `rgba(255,190,40,${a + 0.4})`; c.fillStyle = `rgba(255,230,120,${a * 0.6})`; c.lineWidth = 3;
      tp.sh.cells.forEach(([r, cc]) => { rr(c, cellX(st.c + cc) + 3, cellY(st.r + r) + 3, s - 6, s - 6, s * 0.25); c.fill(); c.stroke(); }); c.restore(); } }
  // 놓기 미리보기: 지워질 줄 테두리 빛""")
P.write_text(s, encoding='utf-8'); print('OK')
