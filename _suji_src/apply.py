p='suji/beta/index.html'; s=open('_suji_src/base.html').read()
def E(o,n,c=1):
  global s; assert s.count(o)==c,(o[:60],s.count(o)); s=s.replace(o,n)
css=open('_suji_src/pro.css').read()
E('<style id="theme-c">','<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">'+css+'<style id="theme-c">')
E('className: "min-h-screen bg-slate-50 text-slate-900",','className: "min-h-screen bg-slate-50 text-slate-900 sj-shell",')
E('React.createElement("header", {\n    className: "bg-slate-900 text-white",','React.createElement("header", {\n    className: "bg-slate-900 text-white sj-head",')
E('React.createElement("nav", {\n    className: "z-20",','React.createElement("nav", {\n    className: "z-20 sj-nav",')
E('className: "max-w-4xl mx-auto px-4 py-4 space-y-3",\n    style: { paddingBottom: 96 }\n  }, ','className: "max-w-4xl mx-auto px-4 py-4 space-y-3 sj-main",\n    style: { paddingBottom: 96 }\n  }, (sheet === \'cost\' || sheet === \'pf\') && live && !live.empty && React.createElement(ProDash, { f, set, live, go, sheet }), ')
js=open('_suji_src/pro_dash.js').read()
E('// 내 사업지 저장·불러오기', js+'\n// 내 사업지 저장·불러오기')
# 베타 표시
E('"SuziQ"))), usage.owner','"SuziQ", React.createElement("span", { style: { marginLeft: 6, fontSize: 10, fontWeight: 800, color: "#0E1116", background: "#C5F04A", borderRadius: 5, padding: "1px 5px", verticalAlign: 3 } }, "BETA")))), usage.owner')
open(p,'w').write(s)
print('ok')
s=open(p).read()
def R(o,n):
  global s; assert o in s,o; s=s.replace(o,n)
R("register('sw.js', { updateViaCache: 'none' })","register('../sw.js', { updateViaCache: 'none', scope: '../' })")
R('href="manifest.webmanifest?v=1"','href="../manifest.webmanifest?v=1"'); R('href="apple-touch-icon.png?v=1"','href="../apple-touch-icon.png?v=1"')
open(p,'w').write(s)
# ── 사업개요 화면 순서(2026-11-20): 사업명·저장 → 토지 → 상품 → 공사비 조건 → 분양가·목표이익률 → 결과, 맨 위에 작은 결과 요약 고정 ──
s=open(p).read()
def R(o,n):
  global s; assert s.count(o)==1,o[:60]; s=s.replace(o,n)
nameBlk='''/*#__PURE__*/React.createElement("label", {
    className: "block col-span-2"
  }, /*#__PURE__*/React.createElement("span", {
    className: "block text-[11px] font-bold text-slate-600 mb-1"
  }, "\\uC0AC\\uC5C5\\uBA85"), /*#__PURE__*/React.createElement("input", {
    className: inputCls,
    value: f.name,
    onChange: e => set('name')(e.target.value)
  })), React.createElement(SavedSites, { f, setF, live }), '''
R(nameBlk,'')
O=lambda n,el: f'React.createElement("div", {{ style: {{ order: {n} }} }}, {el})'
R("sheet === 'cost' && vwOn() && React.createElement(LandLookup, { f, setF })","sheet === 'cost' && vwOn() && "+O(2,"React.createElement(LandLookup, { f, setF })"))
R("sheet === 'cost' && React.createElement(LandSheet, { f, setF })","sheet === 'cost' && "+O(2,"React.createElement(LandSheet, { f, setF })"))
R('sheet === \'cost\' && React.createElement("div", { className: "bg-white rounded-xl border border-slate-200 p-4 space-y-3" },','sheet === \'cost\' && React.createElement("div", { className: "bg-white rounded-xl border border-slate-200 p-4 space-y-3", style: { order: 2 } },')
R("sheet === 'cost' && React.createElement(QuickCompare, { f, setProduct })","sheet === 'cost' && "+O(3,"React.createElement(QuickCompare, { f, setProduct })"))
R("sheet === 'cost' && React.createElement(MaxLand, { f, set, jiga: f.jigaEok || 0, go })","sheet === 'cost' && "+O(5,"React.createElement(MaxLand, { f, set, jiga: f.jigaEok || 0, go })"))
R("sheet === 'cost' && /*#__PURE__*/React.createElement(\"section\", {","sheet === 'cost' && /*#__PURE__*/React.createElement(\"section\", {\n    style: { order: 4 },")
# 대시보드: 사업개요에서는 맨 아래(결과), 사업수지에서는 맨 위. 사업개요 맨 위에는 사업명·저장 카드 + 작은 결과 요약
R("(sheet === 'cost' || sheet === 'pf') && live && !live.empty && React.createElement(ProDash, { f, set, live, go, sheet }), ",
  "sheet !== 'pf' && React.createElement(ProTop, { f: { ...f, _bar: 1 }, set, setF, live }), sheet === 'cost' && React.createElement(ProTop, { f, set, setF, live }), (sheet === 'cost' || sheet === 'pf') && live && !live.empty && React.createElement(\"div\", { className: 'space-y-3', style: { order: sheet === 'cost' ? 8 : 0 } }, React.createElement(ProDash, { f, set, live, go, sheet })), ")
R("// 내 사업지 저장·불러오기", r'''// 사업개요 맨 위: 사업명·저장 + 작은 결과 요약(고정)
function ProTop({ f, set, setF, live }) {
  const ok = live && !live.empty;
  const it = (l, v, c) => React.createElement("div", { style: { minWidth: 0 } }, React.createElement("div", { style: { fontSize: 10, color: '#8A94A3' } }, l), React.createElement("div", { className: "num", style: { fontSize: 14, fontWeight: 700, color: c || '#E8EAED', whiteSpace: 'nowrap' } }, v));
  if (f._bar) return React.createElement("div", { className: "pc", style: { order: 0, position: 'sticky', top: 0, zIndex: 6, padding: '8px 12px', display: ok ? 'grid' : 'none', gridTemplateColumns: 'repeat(4,minmax(0,1fr))', gap: 8, backdropFilter: 'blur(6px)', background: 'rgba(19,23,29,.92)' } },
      ok && it('필요 분양가', `${fmt(live.t10)}만`), ok && it('손익분기', `${fmt(live.be)}만`), ok && it('이익률', `${live.margin.toFixed(1)}%`, live.profit < 0 ? '#F87171' : '#C5F04A'), ok && it('사업이익', sEok1(live.profit), live.profit < 0 ? '#F87171' : '#E8EAED'));
  return React.createElement(React.Fragment, null,
    React.createElement("div", { className: "bg-white rounded-xl border border-slate-200 p-4 space-y-2", style: { order: 1 } },
      React.createElement("label", { className: "block" }, React.createElement("span", { className: "block text-[11px] font-bold text-slate-600 mb-1" }, "사업명"), React.createElement("input", { className: inputCls, value: f.name, placeholder: '예: OO역 오피스텔 신축사업', onChange: e => set('name')(e.target.value) })),
      React.createElement("div", { className: "grid grid-cols-2 gap-2.5" }, React.createElement(SavedSites, { f, setF, live }))));
}
// 내 사업지 저장·불러오기''')
open(p,'w').write(s)
s=open(p).read()
o3='React.createElement(ScaleWarn, { f })), /*#__PURE__*/React.createElement("div", {\n    className: "grid grid-cols-2 gap-2 text-center"'
assert s.count(o3)==1
s=s.replace(o3,'React.createElement(ScaleWarn, { f })), sheet === \'cost\' && (!live || live.empty || f.landEst) && /*#__PURE__*/React.createElement("div", {\n    className: "grid grid-cols-2 gap-2 text-center"')
open(p,'w').write(s)
print('reordered')
