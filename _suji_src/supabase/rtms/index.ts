// 수지들 실거래 조회: 국토교통부 실거래가 공개 API(공공데이터포털)를 서버에서 대신 조회해 통계만 돌려준다.
// 인증키는 서버 비밀값 DATA_GO_KR_KEY. 개인정보 없음. 결과는 rtms_cache에 하루 저장(호출 한도 절약).
import { createClient } from 'jsr:@supabase/supabase-js@2';

const ALLOW = ['https://chulheelim30-cmyk.github.io'];
const EP: Record<string, string> = {
  apt: 'RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade',      // 아파트 매매
  silv: 'RTMSDataSvcSilvTrade/getRTMSDataSvcSilvTrade',   // 아파트 분양권전매
  offi: 'RTMSDataSvcOffiTrade/getRTMSDataSvcOffiTrade',   // 오피스텔 매매
  nrg: 'RTMSDataSvcNrgTrade/getRTMSDataSvcNrgTrade',      // 상업업무용 매매
  indu: 'RTMSDataSvcInduTrade/getRTMSDataSvcInduTrade'    // 공장·창고 매매
};
const cors = (o: string | null) => ({
  'Access-Control-Allow-Origin': o && (ALLOW.includes(o) || o.startsWith('http://localhost') || o === 'null') ? o : ALLOW[0],
  'Access-Control-Allow-Headers': 'content-type',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Content-Type': 'application/json; charset=utf-8'
});
const tag = (x: string, t: string) => { const m = new RegExp('<' + t + '>([^<]*)</' + t + '>', 'i').exec(x); return m ? m[1].trim() : ''; };
const num = (s: string) => parseFloat(String(s).replace(/[^\d.]/g, '')) || 0;
const q = (a: number[], p: number) => { if (!a.length) return 0; const s = [...a].sort((x, y) => x - y); const i = (s.length - 1) * p; const lo = Math.floor(i), hi = Math.ceil(i); return Math.round(s[lo] + (s[hi] - s[lo]) * (i - lo)); };

Deno.serve(async (req) => {
  const o = req.headers.get('origin');
  const H = cors(o);
  if (req.method === 'OPTIONS') return new Response('ok', { headers: H });
  try {
    const u = new URL(req.url);
    const type = u.searchParams.get('type') || 'apt';
    const lawd = (u.searchParams.get('lawd') || '').replace(/\D/g, '').slice(0, 5);
    const months = Math.min(12, Math.max(1, +(u.searchParams.get('months') || 12)));
    if (!EP[type] || lawd.length !== 5) return new Response(JSON.stringify({ error: 'type·lawd(시군구 5자리) 확인' }), { status: 400, headers: H });
    const key = Deno.env.get('DATA_GO_KR_KEY');
    if (!key) return new Response(JSON.stringify({ error: '서버에 인증키가 없습니다' }), { status: 500, headers: H });
    const db = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
    const now = new Date(Date.now() + 9 * 3600e3);
    const yms: string[] = [];
    for (let i = 1; i <= months; i++) { const d = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() - i, 1)); yms.push(d.getUTCFullYear() + String(d.getUTCMonth() + 1).padStart(2, '0')); }
    const ck = `${type}|${lawd}|${yms[0]}|${months}`;
    const { data: hit } = await db.from('rtms_cache').select('data,at').eq('k', ck).maybeSingle();
    if (hit && Date.now() - new Date(hit.at).getTime() < 24 * 3600e3) return new Response(JSON.stringify({ ...hit.data, cached: true }), { headers: H });
    const rows: any[] = [];
    let apiErr = '';
    await Promise.all(yms.map(async ym => {
      const url = `https://apis.data.go.kr/1613000/${EP[type]}?serviceKey=${encodeURIComponent(key)}&LAWD_CD=${lawd}&DEAL_YMD=${ym}&pageNo=1&numOfRows=1000`;
      const r = await fetch(url); const x = await r.text();
      const code = tag(x, 'resultCode');
      if (code && code !== '00' && code !== '000') { apiErr = tag(x, 'resultMsg') || code; return; }
      if (!r.ok) { apiErr = 'HTTP ' + r.status; return; }
      for (const it of x.split(/<item>/i).slice(1)) {
        if (/^O$/i.test(tag(it, 'cdealType'))) continue; // 해제 거래 제외
        const amt = num(tag(it, 'dealAmount'));
        const ar = num(tag(it, 'excluUseAr')) || num(tag(it, 'buildingAr'));
        if (!amt || !ar) continue;
        rows.push({ ym, amt, ar, py: amt / (ar / 3.3058), by: +tag(it, 'buildYear') || 0, nm: tag(it, 'aptNm') || tag(it, 'offiNm') || tag(it, 'buildingUse') || '', umd: tag(it, 'umdNm'), use: tag(it, 'buildingUse') });
      }
    }));
    if (!rows.length && apiErr) return new Response(JSON.stringify({ error: 'API: ' + apiErr }), { status: 502, headers: H });
    const y = now.getUTCFullYear();
    const newer = rows.filter(r => r.by && r.by >= y - 5);
    const stat = (a: any[]) => ({ n: a.length, med: q(a.map(r => r.py), 0.5), p25: q(a.map(r => r.py), 0.25), p75: q(a.map(r => r.py), 0.75) });
    const out = {
      type, lawd, from: yms[yms.length - 1], to: yms[0], basis: type === 'nrg' || type === 'indu' ? '건물면적' : '전용면적',
      all: stat(rows), recent5y: stat(newer),
      samples: rows.sort((a, b) => b.ym.localeCompare(a.ym)).slice(0, 5).map(r => ({ ym: r.ym, nm: r.nm, umd: r.umd, ar: Math.round(r.ar * 10) / 10, amt: r.amt, py: Math.round(r.py), by: r.by })),
      src: '국토교통부 실거래가 공개시스템(공공데이터포털)', at: new Date().toISOString().slice(0, 10)
    };
    await db.from('rtms_cache').upsert({ k: ck, data: out, at: new Date().toISOString() });
    return new Response(JSON.stringify(out), { headers: H });
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e).slice(0, 200) }), { status: 500, headers: H });
  }
});
