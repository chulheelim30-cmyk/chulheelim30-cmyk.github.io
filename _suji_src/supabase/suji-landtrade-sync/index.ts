// 수지들: 국토부 토지 매매 실거래 → Supabase (토지비 주변 비교용)
// 범위: 전국(2026-11-23 운영계정 승인 후 확대; 2026-07 개편 반영 — 전남광주통합특별시 12xxx, 인천 제물포구·영종구·서해구·검단구. 옛 코드는 전 기간 0건이라 제외. 검단구 28290 확인. 광주 동구 12210·서구 12240·남구 12270·북구 12300 확인, 광산구는 12330 후보), 2024-01~이번 달. 지분거래·해제건·100㎡ 미만은 저장하지 않음. 최근 3개월은 하루 1번 다시 받음(신고 지연 반영)
import { createClient } from "npm:@supabase/supabase-js@2.49.4";

const URL_ = "https://apis.data.go.kr/1613000/RTMSDataSvcLandTrade/getRTMSDataSvcLandTrade";
const LAWD = ("11110,11140,11170,11200,11215,11230,11260,11290,11305,11320,11350,11380,11410,11440,11470,11500,11530,11545,11560,11590"
  + ",11620,11650,11680,11710,11740,28177,28185,28200,28237,28245,28710,28720,41111,41113,41115,41117,41131,41133,41135,41150"
  + ",41171,41173,41192,41194,41196,41210,41220,41250,41271,41273,41281,41285,41287,41290,41310,41360,41370,41390,41410,41430"
  + ",41450,41461,41463,41465,41480,41500,41550,41570,41591,41593,41595,41597,41610,41630,41650,41670,41800,41820,41830,43111"
  + ",43112,43113,43114,43130,43150,43720,43730,43745,43750,43760,43770,43800,44131,44133,44150,44180,44200,44210,44230,44250"
  + ",44270,44710,44760,44770,44790,44800,44810,44825,26110,26140,26170,26200,26230,26260,26290,26320,26350,26380,26410,26440"
  + ",26470,26500,26530,26710,27110,27140,27170,27200,27230,27260,27290,27710,27720,30110,30140,30170,30200,30230,31110,31140"
  + ",31170,31200,31710,36110,51110,51130,51150,51170,51190,51210,51230,51720,51730,51750,51760,51770,51780,51790,51800,51810"
  + ",51820,51830,52111,52113,52130,52140,52180,52190,52210,52710,52720,52730,52740,52750,52770,52790,52800,47111,47113,47130"
  + ",47150,47170,47190,47210,47230,47250,47280,47290,47730,47750,47760,47770,47820,47830,47840,47850,47900,47920,47930,47940"
  + ",48121,48123,48125,48127,48129,48170,48220,48240,48250,48270,48310,48330,48720,48730,48740,48820,48840,48850,48860,48870"
  + ",48880,48890,50110,50130,28125,28155,28275,28290,12110,12130,12150,12170,12190,12210,12270,12710,12720,12730,12740,12750"
  + ",12760,12770,12780,12790,12800,12810,12820,12830,12840,12850,12860,12870,12240,12300,12330,12320,12340").split(",");
const START = "202401";
const PER_RUN = 900; // 시간 제한(100초)에 먼저 걸리면 거기서 멈추고 다음 실행에서 이어감
const PARALLEL = 8;

const json = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "Content-Type": "application/json" } });
const num = (v?: string) => { if (!v) return null; const n = Number(v.replace(/,/g, "").trim()); return Number.isFinite(n) ? n : null; };

function months(): string[] {
  const out: string[] = []; const now = new Date(Date.now() + 9 * 3600e3);
  let y = +START.slice(0, 4), m = +START.slice(4);
  while (y < now.getUTCFullYear() || (y === now.getUTCFullYear() && m <= now.getUTCMonth() + 1)) {
    out.push(`${y}${String(m).padStart(2, "0")}`); m++; if (m > 12) { m = 1; y++; }
  }
  return out;
}
function parseItems(xml: string) {
  const items: Record<string, string>[] = [];
  for (const m of xml.matchAll(/<item>([\s\S]*?)<\/item>/g)) {
    const o: Record<string, string> = {};
    for (const f of m[1].matchAll(/<(\w+)>([\s\S]*?)<\/\1>/g)) o[f[1]] = f[2].trim();
    items.push(o);
  }
  const total = Number(xml.match(/<totalCount>(\d+)<\/totalCount>/)?.[1] ?? "0");
  const code = xml.match(/<resultCode>(\w+)<\/resultCode>/)?.[1] ?? xml.match(/<returnReasonCode>(\w+)<\/returnReasonCode>/)?.[1] ?? "";
  const msg = xml.match(/<resultMsg>([^<]*)<\/resultMsg>/)?.[1] ?? xml.match(/<returnAuthMsg>([^<]*)<\/returnAuthMsg>/)?.[1] ?? "";
  return { items, total, code, msg };
}
async function sha(s: string) {
  const b = await crypto.subtle.digest("SHA-1", new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, "0")).join("");
}
async function fetchMonth(key: string, lawd: string, ym: string) {
  const all: Record<string, string>[] = [];
  for (let page = 1; page <= 20; page++) {
    const u = new URL(URL_);
    u.searchParams.set("serviceKey", key); u.searchParams.set("LAWD_CD", lawd); u.searchParams.set("DEAL_YMD", ym);
    u.searchParams.set("pageNo", String(page)); u.searchParams.set("numOfRows", "1000");
    const t = await (await fetch(u)).text();
    const p = parseItems(t);
    if (p.code && !["00", "000"].includes(p.code)) throw new Error(`API ${p.code} ${p.msg || t.slice(0, 120)}`);
    if (!p.code && !t.includes("<response")) throw new Error(`API 응답 이상: ${t.slice(0, 120)}`);
    all.push(...p.items);
    if (all.length >= p.total || p.items.length === 0) break;
  }
  return all;
}

Deno.serve(async (req) => {
  const key = Deno.env.get("DATA_GO_KR_KEY");
  if (!key) return json({ ok: false, error: "DATA_GO_KR_KEY 없음" }, 500);
  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const probe = new URL(req.url).searchParams.get("probe");

  const { data: last } = await db.from("pub_sync_log").select("started_at").eq("source", "landtrade").order("started_at", { ascending: false }).limit(1);
  if (!probe && last?.[0] && Date.now() - new Date(last[0].started_at).getTime() < 4 * 60 * 1000) return json({ ok: true, skipped: "최근 4분 안에 실행됨" });

  const ms = months(); const recent = new Set(ms.slice(-3));
  const prog: { lawd_cd: string; ym: string; done_at: string }[] = [];
  for (let from = 0; ; from += 1000) {
    const { data } = await db.from("pub_land_progress").select("lawd_cd,ym,done_at").order("lawd_cd").order("ym").range(from, from + 999);
    if (!data?.length) break; prog.push(...data); if (data.length < 1000) break;
  }
  const done = new Map(prog.map((p) => [`${p.lawd_cd}-${p.ym}`, new Date(p.done_at).getTime()]));
  const todo: [string, string][] = [];
  for (const ym of [...ms].reverse()) for (const l of LAWD) {
    const d = done.get(`${l}-${ym}`);
    if (d === undefined || (recent.has(ym) && Date.now() - d > 20 * 3600e3)) todo.push([l, ym]);
  }
  const batch = probe ? [["41500", ms[ms.length - 2]] as [string, string]] : todo.slice(0, PER_RUN);
  if (!batch.length) return json({ ok: true, nothing: true });

  const { data: logRow } = await db.from("pub_sync_log").insert({ source: "landtrade", status: "running" }).select("id").single();
  let rows = 0; const errs: string[] = []; let fatal = "";
  const t0 = Date.now(); let tried = 0;
  for (let i = 0; i < batch.length && !fatal && Date.now() - t0 < 100e3; i += PARALLEL) {
    tried = Math.min(batch.length, i + PARALLEL);
    await Promise.all(batch.slice(i, i + PARALLEL).map(async ([l, ym]) => {
      try {
        const items = await fetchMonth(key, l, ym);
        if (probe) { errs.push(JSON.stringify(items.slice(0, 2))); }
        const keep = items.filter((r) => !(r.shareDealingType || "").trim() && !(r.cdealType || "").trim() && (num(r.dealArea) ?? 0) >= 100);
        const up = await Promise.all(keep.map(async (r) => ({
          id: await sha([r.sggCd, r.umdNm, r.jibun, r.dealYear, r.dealMonth, r.dealDay, r.dealAmount, r.dealArea].join("|")),
          sgg_cd: r.sggCd ?? l, sgg_nm: r.sggNm ?? null, umd_nm: r.umdNm ?? null, jibun: r.jibun ?? null,
          deal_date: r.dealYear ? `${r.dealYear}-${String(r.dealMonth).padStart(2, "0")}-${String(r.dealDay).padStart(2, "0")}` : null,
          deal_amount: num(r.dealAmount), deal_area: num(r.dealArea), jimok: r.jimok ?? null, land_use: r.landUse ?? null,
          dealing_gbn: r.dealingGbn ?? null, share_type: r.shareDealingType || null, cdeal_type: r.cdealType || null,
          updated_at: new Date().toISOString(),
        })));
        const uniq = [...new Map(up.map((x) => [x.id, x])).values()];
        for (let k = 0; k < uniq.length; k += 500) {
          const { error } = await db.from("pub_land_trade").upsert(uniq.slice(k, k + 500), { onConflict: "id" });
          if (error) throw new Error(error.message);
        }
        rows += up.length;
        await db.from("pub_land_progress").upsert({ lawd_cd: l, ym, rows_: items.length, done_at: new Date().toISOString() });
      } catch (e) {
        const m = (e as Error).message;
        if (/^API (20|22|30|31|32)\b/.test(m) || /SERVICE_KEY|LIMITED|ACCESS_DENIED/.test(m)) fatal = m;
        errs.push(`${l}-${ym}: ${m}`.slice(0, 200));
      }
    }));
  }
  await db.from("pub_sync_log").update({ finished_at: new Date().toISOString(), status: fatal ? "error" : errs.length && !probe ? "partial" : "ok", notices: tried, models: rows, message: errs.slice(0, 5).join("\n") || null }).eq("id", logRow?.id);
  return json({ ok: !fatal, tried, rows, remaining: Math.max(0, todo.length - tried), errors: errs.slice(0, 5) });
});
