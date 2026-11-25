#!/usr/bin/env python3
"""블락풍 v44: 올 클리어 더 자주 + 보이게
- 탐색: 판 칸 30개 이하에서, 시간 180ms·조합 200개·빔 6, 절반은 '지금 줄을 지우는 블록' 위주로 뽑기
- 찾으면 '올 클리어 기회!' 알림, 4초 머뭇거리면 다음 놓을 자리를 살짝 빛나게(그대로 따라 놓을 때만 이어짐)"""
import sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'play/blockpung/index.html'; s = P.read_text(encoding='utf-8')
if 'ACPLAN_V44' in s: print('already'); sys.exit(0)
def rep(a, b):
    global s; assert s.count(a) == 1, (s.count(a), a[:70]); s = s.replace(a, b)
i = s.index('function findAllClear(b) {'); j = s.index('function newTray() {')
s = s[:i] + r"""function findAllClear(b) { // ACPLAN_V44: 판을 싹 비울 블록 3개 + 놓을 자리 찾기 (빔 탐색)
  const b0 = b.map(r => r.map(x => !!x)), t0 = performance.now();
  const conc = nb => { let s = 0; for (let r = 0; r < N; r++) { let k = 0; for (let c = 0; c < N; c++) if (nb[r][c]) k++; s += k * k; } for (let c = 0; c < N; c++) { let k = 0; for (let r = 0; r < N; r++) if (nb[r][c]) k++; s += k * k; } return s; };
  const pool = SHAPES.filter(x => x.cells.length <= 6), hit = pool.filter(x => clearsLine(b0, x));
  const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
  for (let t = 0; t < 200 && performance.now() - t0 < 180; t++) {
    const cand = t % 2 && hit.length ? [pick(hit), pick(pool), pick(pool)] : [pick(pool), pick(pool), pick(pool)];
    if (new Set(cand.map(x => x.id)).size < 3) continue;
    for (const ord of PERMS3) {
      let beam = [{ nb: b0, path: [] }];
      for (const i of ord) { const sh = cand[i], next = [];
        for (const e of beam) for (let r = 0; r <= N - sh.h; r++) for (let c = 0; c <= N - sh.wd; c++) { if (!fits(e.nb, sh, r, c)) continue; const a = boardAfter(e.nb, sh, r, c); let f = 0; for (const rr of a.nb) for (const x of rr) if (x) f++;
          const path = e.path.concat([{ id: sh.id, r, c }]);
          if (f === 0 && a.lines) return { set: cand, plan: path }; // 중간에 판이 비면 올 클리어
          next.push({ nb: a.nb, path, v: a.lines * 200 - f * 6 + conc(a.nb) }); }
        if (!next.length) { beam = null; break; }
        next.sort((x, y) => y.v - x.v); beam = next.slice(0, 6);
      }
    }
  }
  return null;
}
""" + s[j:]
rep("let acSet = null; if (fill > 0 && fill <= 24) acSet = findAllClear(b); // 올 클리어 기회 만들기",
    "let acSet = null, ac = null; G.acPlan = null; if (fill > 0 && fill <= 30) { ac = findAllClear(b); if (ac) acSet = ac.set; } // 올 클리어 기회 만들기")
rep("  if (acSet) { set = acSet; G.acFound = (G.acFound || 0) + 1; }",
    "  if (acSet) { set = acSet; G.acFound = (G.acFound || 0) + 1; G.acPlan = ac.plan; G.acT = G.t; if (G.state === 'play') fxPop('올 클리어 기회!', L.W / 2, L.by - 14, { size: 22, rainbow: true, life: 1.6 }); }")
# 놓을 때: 계획대로면 다음 단계, 아니면 계획 취소
rep("function place(i, gr, gc) {\n  const pc = G.tray[i]; G.tray[i] = null;",
    "function place(i, gr, gc) {\n  const pc = G.tray[i]; G.tray[i] = null;\n  if (G.acPlan) { const st = G.acPlan[0]; if (st && st.id === pc.sh.id && st.r === gr && st.c === gc) { G.acPlan.shift(); G.acT = G.t; if (!G.acPlan.length) G.acPlan = null; } else G.acPlan = null; }")
# 힌트: 4초 머뭇거리면 다음 자리 빛
rep("  for (let r = 0; r < N; r++) for (let col = 0; col < N; col++) {\n    const x = G.board[r][col]; if (!x) continue;",
    """  if (G.acPlan && G.acPlan.length && !d && G.state === 'play' && G.t - G.acT > 4) { const st = G.acPlan[0], tp = G.tray.find(t => t && t.sh.id === st.id);
    if (tp) { const a = 0.35 + 0.25 * Math.sin(G.t * 5); c.save(); c.shadowColor = 'rgba(255,240,150,.9)'; c.shadowBlur = 14; c.strokeStyle = `rgba(255,236,140,${a + 0.3})`; c.fillStyle = `rgba(255,236,140,${a * 0.5})`; c.lineWidth = 2;
      tp.sh.cells.forEach(([r, cc]) => { rr(c, cellX(st.c + cc) + 3, cellY(st.r + r) + 3, s - 6, s - 6, s * 0.25); c.fill(); c.stroke(); }); c.restore(); } }
  for (let r = 0; r < N; r++) for (let col = 0; col < N; col++) {
    const x = G.board[r][col]; if (!x) continue;""")
P.write_text(s, encoding='utf-8'); print('ok')
# (수동 반영) 계획 비교는 블록 모양(칸 좌표) 기준 shKey, exactCover(줄 3개 이하를 블록 3개 이하로 딱 채우기, 실제로 놓아 보며 순서 확인),
# 판 시작 퍼즐 openPuzzle(한두 줄에 3~5칸), 판이 가벼울 때 줄 적게 퍼지도록 setValue 보정, 힌트 빛 진하게
