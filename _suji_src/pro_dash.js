
// ── 프로 대시보드 (2026-11-20 베타): KPI 3개 + 사업수지 요약표 + 우측 패널(규모 미리보기·민감도·경고). 계산은 기존 model/analyze/solveLand 그대로 사용 ──
const TAGS = { '공공': 'pub', '실사업': 'real', '추정': 'est', '입력': 'inp' };
const Bdg = ({ t }) => React.createElement("span", { className: 'bdg ' + (TAGS[t] || 'inp') }, t);
const tagOfBasis = b => { const m = /^\[(공공|실사업|추정|입력)\]/.exec(b || ''); return m ? m[1] : /추정/.test(b || '') ? '추정' : null; };
function proFlags(f, R) {
  const hasDesign = f.archAboveM2 > 0 || f.archBsmtM2 > 0 || f.gfaManual > 0;
  const cost = R.S - R.profit;
  const estV = (R.lines || []).filter(l => /추정/.test(l.basis || '')).reduce((a, l) => a + (l.v || 0), 0);
  return { hasDesign, cost, estPct: estV / Math.max(1e-9, cost) * 100 };
}
function ProKpis({ f, R }) {
  const fl = proFlags(f, R);
  const costTag = !fl.hasDesign ? '추정' : f.costMode === 'manual' ? '입력' : '실사업';
  const cap = useMemo(() => solveLand(f, R.price, R.tm), [f, R.price, R.tm]);
  const landTag = !fl.hasDesign ? '추정' : f.price > 0 ? '입력' : costTag;
  const card = (l, t, v, sub, hl) => React.createElement("div", { className: 'pc kpi' + (hl ? ' hl' : '') },
    React.createElement("div", { className: "l" }, l, React.createElement(Bdg, { t })),
    React.createElement("div", { className: "v num" }, v), React.createElement("div", { className: "s" }, sub));
  return React.createElement("div", null,
    React.createElement("div", { className: "kpis" },
      card('필요 분양가', costTag, `평당 ${fmt(R.t10)}만원`, `목표 이익률 ${R.tm}% 기준`),
      card('손익분기 분양가', costTag, `평당 ${fmt(R.be)}만원`, '이익 0원 기준'),
      card('목표이익 기준 토지비', landTag, cap >= 0 ? `${fmt(cap)}억원` : '산출 불가', `목표 이익률 ${R.tm}% 역산 · 감정가 아님`, true)),
    React.createElement("p", { style: { fontSize: 11, color: '#8A94A3', marginTop: 6 } },
      fl.hasDesign ? '설계 면적 입력 기준 계산입니다.' : '⚠ 1차 판단(추정 포함) — 설계 면적 없이 대지·용적률로 추정했습니다. 설계·견적값을 넣을수록 정밀해집니다.'));
}
function ProTable({ f, set, R }) {
  const fl = proFlags(f, R), cost = fl.cost;
  const groups = {};
  (R.lines || []).forEach(l => { const g = l.g || '기타'; (groups[g] = groups[g] || { v: 0, tags: {} }).v += l.v || 0; const t = tagOfBasis(l.basis) || '실사업'; groups[g].tags[t] = (groups[g].tags[t] || 0) + (l.v || 0); });
  const domTag = g => Object.entries(g.tags).sort((a, b) => b[1] - a[1])[0]?.[0] || '실사업';
  const donut = v => { const d = Math.max(0, Math.min(100, v / cost * 100)); return React.createElement("span", { className: "donut", title: `총사업비의 ${d.toFixed(1)}%`, style: { background: `conic-gradient(#C5F04A ${d * 3.6}deg, #2B3442 0)` } }); };
  const row = (name, tag, val, extra, cls = '') => React.createElement("tr", { className: cls },
    React.createElement("td", null, name, ' ', tag && React.createElement(Bdg, { t: tag })),
    React.createElement("td", { className: "r num" }, val),
    React.createElement("td", { className: "r", style: { width: 34 } }, extra));
  const numIn = (v, k, step) => React.createElement("input", { type: "number", inputMode: "decimal", step, className: "num", value: v || '', placeholder: '입력', onChange: e => set(k)(parseFloat(e.target.value) || 0) });
  const order = ['토지비', '공사비', '분양경비', '제세·부담금', '사업추진비', '금융비'];
  const rest = Object.keys(groups).filter(g => !order.includes(g) && g !== '토지비');
  return React.createElement("div", { className: "pc" },
    React.createElement("div", { style: { display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 } },
      React.createElement("h3", null, "사업수지표"), React.createElement("span", { style: { fontSize: 11, color: '#8A94A3' } }, "억원 · VAT 별도")),
    React.createElement("div", { style: { overflowX: 'auto' } }, React.createElement("table", { className: "st" }, React.createElement("tbody", null,
      React.createElement("tr", { className: "inp" }, React.createElement("td", null, "분양가 ", React.createElement(Bdg, { t: '입력' }), React.createElement("div", { style: { fontSize: 10.5, color: '#8A94A3' } }, f.price > 0 ? '평당 만원' : `비우면 목표 이익률 분양가 ${fmt(R.t10)}만`)), React.createElement("td", { className: "r", colSpan: 2 }, numIn(f.price, 'price', 50))),
      row('분양 매출', R.priced ? '입력' : '추정', eok1(R.S), null),
      React.createElement("tr", { className: "inp" }, React.createElement("td", null, "토지비 ", React.createElement(Bdg, { t: '입력' }), React.createElement("div", { style: { fontSize: 10.5, color: '#8A94A3' } }, '토지매입비(억)')), React.createElement("td", { className: "r", colSpan: 2 }, numIn(f.landEok, 'landEok', 10))),
      order.filter(g => groups[g]).map(g => React.createElement(React.Fragment, { key: g }, row(g === '토지비' ? '토지비 합계(부대비 포함)' : g, domTag(groups[g]), eok1(groups[g].v), donut(groups[g].v)))),
      rest.map(g => React.createElement(React.Fragment, { key: g }, row(g, domTag(groups[g]), eok1(groups[g].v), donut(groups[g].v)))),
      row('총사업비', null, eok1(cost), null, 'tot'),
      React.createElement("tr", { className: "pro" + (R.profit < 0 ? " neg" : "") }, React.createElement("td", null, "사업이익"), React.createElement("td", { className: "r num" }, sEok1(R.profit)), React.createElement("td", { className: "r num", style: { whiteSpace: 'nowrap' } }, `${R.margin.toFixed(1)}%`))))),
    React.createElement("p", { style: { fontSize: 10.5, color: '#8A94A3', marginTop: 6 } }, "도넛 = 총사업비 대비 비중 · 항목별 상세와 산출 근거는 2.사업수지 시트에 있습니다."));
}
// 규모 미리보기(시안 스타일): 라임 대지판 + 앰버 포디움 + 블루그레이 유리 트윈타워, 층이 차례로 올라감. 형태는 연출, 층수·지하·상가 층은 입력값
function proMassSvg(floors, bf, retF, twin, k, done, unitLabel) {
  const C = Math.cos(Math.PI / 6), S = Math.sin(Math.PI / 6);
  const podF = Math.max(1, Math.min(3, retF || 1)), towF = Math.max(1, floors - podF), PH = 2.6;
  const PW = 20, PD = 16, fh = Math.min(1.5, (44 - podF * PH) / (towF + 1));
  const sc = 5.4, ox = 205, oy = 262;
  const P = (x, y, z) => [ox + (x - y) * C * sc, oy + (x + y) * S * sc - z * sc];
  const pt = a => a.map(p => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
  const poly = (a, fill, ex = '') => `<polygon points="${pt(a)}" fill="${fill}" ${ex}/>`;
  const ln = (a, b, c, w = 1, ex = '') => `<line x1="${a[0].toFixed(1)}" y1="${a[1].toFixed(1)}" x2="${b[0].toFixed(1)}" y2="${b[1].toFixed(1)}" stroke="${c}" stroke-width="${w}" ${ex}/>`;
  const x0 = -PW / 2, y0 = -PD / 2;
  const box = (x, y, w, d, z, h, top, l, r, ex = '') => poly([P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)], l) + poly([P(x + w, y + d, z), P(x + w, y, z), P(x + w, y, z + h), P(x + w, y + d, z + h)], r) + poly([P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)], top, ex);
  let o = `<defs><radialGradient id="gw" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="rgba(197,240,74,.45)"/><stop offset="1" stop-color="rgba(197,240,74,0)"/></radialGradient>
   <linearGradient id="am" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2A55E"/><stop offset="1" stop-color="#B8662C"/></linearGradient>
   <linearGradient id="tl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5E7C9E"/><stop offset="1" stop-color="#3A5069"/></linearGradient>
   <linearGradient id="tr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#86A3C2"/><stop offset="1" stop-color="#55708F"/></linearGradient></defs>`;
  // 은은한 바닥 그리드 + 라임 글로우 + 라임 대지판
  for (let i = 0; i <= 8; i++) { const t = -18 + i * 4.5; o += ln(P(t, -18, 0), P(t, 18, 0), '#1A212B') + ln(P(-18, t, 0), P(18, t, 0), '#1A212B'); }
  const g = P(0, 0, 0); o += `<ellipse cx="${g[0]}" cy="${g[1]}" rx="${21 * C * sc * 1.25}" ry="${21 * S * sc * 1.25}" fill="url(#gw)"/>`;
  o += box(x0 - 3, y0 - 3, PW + 6, PD + 6, -0.7, 0.7, 'rgba(197,240,74,.9)', '#8DB32C', '#A9D03A', 'stroke="#E2FF8A" stroke-width="1"');
  for (let b = 1; b <= bf; b++) { const z = -0.7 - b * 1.2; o += poly([P(x0, y0 + PD, z), P(x0 + PW, y0 + PD, z), P(x0 + PW, y0, z)], 'none', 'stroke="rgba(147,197,253,.3)" stroke-dasharray="3 3"'); }
  // 앰버 포디움(상가)
  const podK = Math.min(k, podF), towK = Math.max(0, k - podF);
  if (podK > 0) {
    const ph = podK * PH; o += box(x0, y0, PW, PD, 0, ph, '#2B2F36', 'url(#am)', 'url(#am)');
    for (let f = 0; f < podK; f++) { const z = f * PH; for (let c = 0; c < 10; c++) { const a = x0 + PW * c / 10 + .25, b = x0 + PW * (c + 1) / 10 - .25; o += poly([P(a, y0 + PD, z + .4), P(b, y0 + PD, z + .4), P(b, y0 + PD, z + PH * .85), P(a, y0 + PD, z + PH * .85)], 'rgba(255,236,200,.75)'); }
      for (let c = 0; c < 8; c++) { const a = y0 + PD * c / 8 + .25, b = y0 + PD * (c + 1) / 8 - .25; o += poly([P(x0 + PW, a, z + .4), P(x0 + PW, b, z + .4), P(x0 + PW, b, z + PH * .85), P(x0 + PW, a, z + PH * .85)], 'rgba(255,236,200,.6)'); } }
    o += ln(P(x0, y0 + PD, ph), P(x0 + PW, y0 + PD, ph), '#FFD2A0', 1.2) + ln(P(x0 + PW, y0 + PD, ph), P(x0 + PW, y0, ph), '#FFD2A0', 1.2);
  }
  const pz = podF * PH;
  // 유리 타워: 블루그레이 면 + 층선·멀리온 격자
  const tower = (x, y, w, d, nF, kF) => { const h = kF * fh; if (h <= 0) return '';
    let r = box(x, y, w, d, pz, h, '#9FB6CF', 'url(#tl)', 'url(#tr)', 'stroke="#C5F04A" stroke-width="1.2"');
    for (let f = 1; f < kF; f++) { const z = pz + f * fh; r += ln(P(x, y + d, z), P(x + w, y + d, z), 'rgba(205,222,240,.38)', .7) + ln(P(x + w, y + d, z), P(x + w, y, z), 'rgba(225,236,248,.42)', .7); }
    const cl = Math.round(w * .9), cr = Math.round(d * .9);
    for (let c = 1; c < cl; c++) { const xx = x + w * c / cl; r += ln(P(xx, y + d, pz), P(xx, y + d, pz + h), 'rgba(20,30,42,.45)', .8); }
    for (let c = 1; c < cr; c++) { const yy = y + d * c / cr; r += ln(P(x + w, yy, pz), P(x + w, yy, pz + h), 'rgba(20,30,42,.4)', .8); }
    return r; };
  const T = twin ? [[x0 + 2, y0 + 1.5, 8.5, 9, 1], [x0 + 10.5, y0 + 5, 8, 9, .82]] : [[x0 + 4, y0 + 3, 12, 10, 1]];
  let topA = null;
  T.forEach(([x, y, w, d, hr], idx) => { const nF = Math.max(1, Math.round(towF * hr)), kF = Math.min(nF, towK); o += tower(x, y, w, d, nF, kF);
    if (idx === 0 && kF > 0) topA = [x, y, w, d, pz + kF * fh]; });
  // 지붕 라벨(세대 크기) + 층수 태그
  if (topA) { const [x, y, w, d, z] = topA, c = P(x + w / 2, y + d / 2, z);
    if (done && unitLabel) o += `<rect x="${c[0] - 15}" y="${c[1] - 10}" rx="4" width="30" height="18" fill="#C5F04A"/><text x="${c[0]}" y="${c[1] + 3.5}" font-size="11" text-anchor="middle" font-weight="800" fill="#0E1116" font-family="Space Grotesk,Noto Sans KR">${unitLabel}</text>`;
    const tF = Math.min(towF, towK) + podF, a = P(x + w, y, z), tx = a[0] + 30, ty = a[1] + 4;
    o += ln(a, [tx, ty], '#C5F04A', 1) + `<rect x="${tx}" y="${ty - 10}" rx="4" width="40" height="19" fill="#C5F04A"/><text x="${tx + 20}" y="${ty + 3.5}" font-size="11" text-anchor="middle" font-weight="800" fill="#0E1116" font-family="Space Grotesk,Noto Sans KR">${tF}F</text>`; }
  return o;
}
function ProMass({ f, R }) {
  const sc = R.sc, isRes = R.p.res && R.p.id !== 'officetel';
  const floorsIn = f.archFloorsUp > 0, bf = f.archFloorsDn > 0 ? f.archFloorsDn : (sc.gfa > sc.above ? Math.max(1, Math.round((sc.gfa - sc.above) / Math.max(1, sc.above) * 5)) : 0);
  const floors = Math.min(60, floorsIn ? f.archFloorsUp : isRes ? 25 : Math.max(3, Math.ceil(sc.far / 60)));
  const u = isRes ? 4 : 1, fpd = isRes ? Math.min(sc.above / floors, u * Math.max(20, sc.unitPy || 35)) : sc.above / floors;
  const dong = Math.max(1, Math.round(sc.above / floors / fpd));
  const retF = sc.retailPy > 0 ? Math.max(1, Math.round(sc.retailPy / fpd / dong)) : 0;
  const m = Math.sqrt(fpd * 3.3058), ar = isRes ? 2.4 : 1.2, W = m * Math.sqrt(ar), D = m / Math.sqrt(ar);
  const [k, setK] = useState(0), [run, setRun] = useState(0);
  useEffect(() => { setK(0); const tot = floors; let i = 0; const t = setInterval(() => { i++; setK(i); if (i >= tot) clearInterval(t); }, Math.max(28, 2800 / tot)); return () => clearInterval(t); }, [floors, retF, run]);
  const total = floors;
  const svg = useMemo(() => proMassSvg(floors, Math.min(bf, 6), retF, isRes && floors >= 12, Math.min(k, total), k >= total, isRes ? String(f.size || 84) : ''), [floors, bf, retF, dong, k, f.size]);
  return React.createElement("div", { className: "pc" },
    React.createElement("div", { style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center' } }, React.createElement("h3", null, "건물 규모 미리보기"), React.createElement(Bdg, { t: floorsIn ? '입력' : '추정' })),
    React.createElement("div", { style: { borderRadius: 12, marginTop: 8, background: 'radial-gradient(120% 90% at 50% 30%,#18202B 0%,#0E1116 75%)' } }, React.createElement("svg", { viewBox: "0 0 440 340", style: { width: '100%', display: 'block' }, dangerouslySetInnerHTML: { __html: svg } })),
    React.createElement("div", { style: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 8, marginTop: 8 } },
      React.createElement("span", { style: { fontSize: 11, color: '#8A94A3', lineHeight: 1.5 } }, `${floorsIn ? '' : '추정 '}지상 ${floors}층 · 지하 ${bf}층 · 대표 1개동${dong > 1 ? `(약 ${dong}개동)` : ''} · 바닥 약 ${fmt(fpd)}평`),
      React.createElement("button", { type: "button", className: "pill", onClick: () => setRun(r => r + 1) }, "다시 쌓기")),
    React.createElement("div", { style: { display: 'flex', gap: 10, flexWrap: 'wrap', fontSize: 10.5, color: '#8A94A3', marginTop: 6 } },
      [['#26364A', '주거·주용도'], ['#FDBA74', '상가(근생)'], ['rgba(147,197,253,.5)', '지하'], ['#0B0E13', '코어']].map(([c, t]) => React.createElement("span", { key: t }, React.createElement("i", { style: { display: 'inline-block', width: 9, height: 9, borderRadius: 2, background: c, border: '1px solid #3E4C60', marginRight: 4 } }), t))));
}
function ProSens({ f, R }) {
  const ds = [-10, -5, 0, 5, 10];
  const grid = useMemo(() => ds.map(dp => ds.map(dc => model(f, R.price * (1 + dp / 100), { costMode: 'manual', costManual: R.unit * (1 + dc / 100) }).margin)), [f, R.price, R.unit]);
  const tone = m => m >= R.tm ? ['rgba(197,240,74,.85)', '#0E1116'] : m >= 0 ? ['rgba(197,240,74,.22)', '#E8EAED'] : ['rgba(248,113,113,.28)', '#FCA5A5'];
  const fl = proFlags(f, R), chips = [];
  if (!f.archAboveM2 && !f.gfaManual && f.sitePy < 300 && R.sc.far >= 300) chips.push(['w', '작은 대지 고용적률']);
  if ((R.sc.gfa > 0 && R.sc.gfa < 1000) || f.archFloorsUp >= 30) chips.push(['w', '소규모·고층 공사비']);
  if (!fl.hasDesign) chips.push(['w', '추정 위주 결과']);
  if (R.priced && R.margin < R.tm && R.profit >= 0) chips.push(['w', '목표 이익률 미달']);
  if (R.profit < 0) chips.push(['d', '적자']);
  if (R.capped) chips.push(['d', '토지비 단위 확인']);
  return React.createElement("div", { className: "pc" },
    React.createElement("h3", null, "민감도 / 확인 사항"),
    React.createElement("p", { style: { fontSize: 10.5, color: '#8A94A3', margin: '4px 0 8px' } }, `이익률 · 세로 분양가, 가로 공사비(기준 평당 ${fmt(R.unit)}만)`),
    React.createElement("div", { className: "hm num" },
      React.createElement("div", null), ds.map(d => React.createElement("div", { key: 'h' + d, style: { color: '#8A94A3' } }, d > 0 ? `+${d}%` : d ? `${d}%` : '공사비')),
      ds.map((dp, i) => React.createElement(React.Fragment, { key: dp },
        React.createElement("div", { style: { color: '#8A94A3', textAlign: 'right', paddingRight: 4 } }, dp > 0 ? `+${dp}%` : dp ? `${dp}%` : '분양가'),
        grid[i].map((m, j) => { const [bg, c] = tone(m); return React.createElement("div", { key: j, style: { background: bg, color: c, fontWeight: dp === 0 && ds[j] === 0 ? 900 : 600, outline: dp === 0 && ds[j] === 0 ? '1.5px solid #E8EAED' : 'none' } }, m.toFixed(1)); })))),
    React.createElement("div", { style: { marginTop: 8 } }, chips.length ? chips.map(([c, t]) => React.createElement("span", { key: t, className: 'chip ' + c }, t)) : React.createElement("span", { style: { fontSize: 11, color: '#8A94A3' } }, "확인 사항 없음")));
}
function ProDash({ f, set, live, sheet }) {
  // 중복 정리(2026-11-20): 사업개요 = 요약 수지표 + 규모 미리보기·민감도 / 사업수지 = KPI 3개만(상세 수지표는 아래 기존 표)
  if (sheet === 'pf') return React.createElement(ProKpis, { f, R: live });
  const fl = proFlags(f, live);
  return React.createElement(React.Fragment, null,
    !fl.hasDesign && React.createElement("p", { style: { fontSize: 11, color: '#FDBA74', margin: 0 } }, '⚠ 1차 판단(추정 포함) — 설계 면적 없이 대지·용적률로 추정했습니다. 설계·견적값을 넣을수록 정밀해집니다.'),
    React.createElement(ProTable, { f, set, R: live }),
    React.createElement("aside", { className: "sj-aside" }, React.createElement(ProMass, { f, R: live }), React.createElement(ProSens, { f, R: live })));
}
