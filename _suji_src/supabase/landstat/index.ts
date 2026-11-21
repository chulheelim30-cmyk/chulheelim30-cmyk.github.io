// SuziQ 토지 실거래 통계 수집(관리용, 1회성): 국토부 토지 매매 실거래 → 시군구×용도지역 평당가 [중앙, 건수, 하위25%, 상위25%]
// 원자료는 저장하지 않고 통계만 land_stat 표에 저장. 순차 호출. 인증키는 서버 비밀값 DATA_GO_KR_KEY
// 호출: pg_net으로 GET ?t=<토큰>&name=<ASCII 이름>&m=12&lawd=26500,26350  (이름에 한글·| 넣으면 400)
// ※ 공개 저장소이므로 실제 토큰은 여기 적지 않음 — 배포본(Supabase 대시보드 > Edge Functions > landstat)에서 확인
import { createClient } from 'jsr:@supabase/supabase-js@2';
const TOKEN = '<배포본 참조>';
const tag = (x: string, t: string) => { const m = new RegExp('<' + t + '>([^<]*)</' + t + '>', 'i').exec(x); return m ? m[1].trim() : ''; };
const num = (s: string) => parseFloat(String(s).replace(/[^\d.]/g, '')) || 0;
const q = (a: number[], p: number) => { const s = [...a].sort((x, y) => x - y); const i = (s.length - 1) * p; const lo = Math.floor(i), hi = Math.ceil(i); return Math.round(s[lo] + (s[hi] - s[lo]) * (i - lo)); };
const grp = (u: string) => /제1종일반주거|전용주거/.test(u) ? 'g1' : /제2종일반주거/.test(u) ? 'g2' : /제3종일반주거/.test(u) ? 'g3' : /준주거/.test(u) ? 'sr' : /상업/.test(u) ? 'com' : /공업/.test(u) ? 'ind' : /계획관리/.test(u) ? 'pm' : '';
const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));
Deno.serve(async (req) => {
  const u = new URL(req.url);
  if (u.searchParams.get('t') !== TOKEN) return new Response('no', { status: 403 });
  const name = u.searchParams.get('name') || '';
  const nm = +(u.searchParams.get('m') || 12);
  const lawds = (u.searchParams.get('lawd') || '').split(',').map(s => s.replace(/\D/g, '')).filter(s => s.length === 5);
  const key = Deno.env.get('DATA_GO_KR_KEY')!;
  const db = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
  const now = new Date(Date.now() + 9 * 3600e3);
  const yms: string[] = [];
  for (let i = 1; i <= nm; i++) { const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() - i, 1)); yms.push(d.getUTCFullYear() + String(d.getUTCMonth() + 1).padStart(2, '0')); }
  const by: Record<string, number[]> = {};
  let n = 0, err = '';
  outer: for (const lawd of lawds) for (const ym of yms) {
    try {
      const url = `https://apis.data.go.kr/1613000/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade?serviceKey=${encodeURIComponent(key)}&LAWD_CD=${lawd}&DEAL_YMD=${ym}&pageNo=1&numOfRows=1000`;
      const x = await (await fetch(url)).text();
      const em = tag(x, 'errMsg'); if (em) { err = em + ' ' + tag(x, 'returnReasonCode'); break outer; }
      const code = tag(x, 'resultCode'); if (code && code !== '00' && code !== '000') { err = tag(x, 'resultMsg') || code; break outer; }
      for (const it of x.split(/<item>/i).slice(1)) {
        if (/^O$/i.test(tag(it, 'cdealType'))) continue;
        if (/지분/.test(tag(it, 'shareDealingType'))) continue;
        const amt = num(tag(it, 'dealAmount')), ar = num(tag(it, 'dealArea'));
        if (!amt || ar < 100) continue;
        const use = tag(it, 'landUse'); const g = grp(use); const py = amt / (ar / 3.3058); n++;
        if (g) (by[g] = by[g] || []).push(py);
        if (/주거/.test(use)) (by.res = by.res || []).push(py);
      }
    } catch (e) { err = String(e).slice(0, 80); }
    await sleep(150);
  }
  const out: Record<string, number[]> = {};
  for (const [g, a] of Object.entries(by)) if (a.length >= 5) out[g] = [q(a, .5), a.length, q(a, .25), q(a, .75)];
  await db.from('land_stat').upsert({ k: name, v: { out, n, err, from: yms[yms.length - 1], to: yms[0], lawds }, at: new Date().toISOString() });
  return new Response(JSON.stringify({ name, n, err }), { headers: { 'content-type': 'application/json' } });
});
