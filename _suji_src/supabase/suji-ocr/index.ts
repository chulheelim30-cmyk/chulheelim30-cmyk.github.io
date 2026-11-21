// 수지들 토지조서 사진 인식: Gemini 키를 서버에 숨겨 공용으로 쓴다.
// 비밀값: GEMINI_API_KEY (필수), SUJI_OCR_CAP_WHO(1인 하루, 기본 30), SUJI_OCR_CAP_ALL(전체 하루, 기본 200)
// ※ 일반 주소(/suji)에서는 앱 쪽에서 Gemini 정밀 인식을 꺼 둠(토지조서 소유자 성명 — 개인정보 정리 전). DB 함수 suji_ocr_hit 사용
import { createClient } from 'npm:@supabase/supabase-js@2';

const ALLOW = [/^https:\/\/chulheelim30-cmyk\.github\.io$/, /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/];
const API = 'https://generativelanguage.googleapis.com/v1beta';
let MODELS: string[] | null = null;

async function pickModels(key: string) {
  if (MODELS) return MODELS;
  const fallback = ['gemini-flash-lite-latest', 'gemini-flash-latest'];
  try {
    const r = await fetch(`${API}/models?pageSize=200`, { headers: { 'x-goog-api-key': key } });
    const j = await r.json();
    const names: string[] = (j.models || []).filter((m: any) => (m.supportedGenerationMethods || []).includes('generateContent')).map((m: any) => String(m.name).replace('models/', ''));
    const ver = (n: string) => parseFloat((n.match(/gemini-(\d+(?:\.\d+)?)/) || [])[1] || '0');
    const flash = names.filter(n => /^gemini-\d+(\.\d+)?-flash$/.test(n)).sort((a, b) => ver(b) - ver(a));
    const lite = names.filter(n => /^gemini-\d+(\.\d+)?-flash-lite$/.test(n)).sort((a, b) => ver(b) - ver(a));
    const list = [...names.filter(n => n === 'gemini-flash-lite-latest'), ...lite.slice(0, 1), ...names.filter(n => n === 'gemini-flash-latest'), ...flash.slice(0, 1)];
    MODELS = list.length ? [...new Set(list)].slice(0, 3) : fallback;
  } catch {
    MODELS = fallback;
  }
  return MODELS;
}

function cors(origin: string | null) {
  const ok = origin && ALLOW.some(r => r.test(origin));
  return {
    'Access-Control-Allow-Origin': ok ? origin! : 'https://chulheelim30-cmyk.github.io',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'content-type, authorization, apikey, x-client-info',
    'Vary': 'Origin'
  };
}

async function sha(s: string) {
  const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s));
  return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join('').slice(0, 32);
}

Deno.serve(async req => {
  const origin = req.headers.get('origin');
  const h = { ...cors(origin), 'Content-Type': 'application/json' };
  const out = (status: number, body: unknown) => new Response(JSON.stringify(body), { status, headers: h });
  if (req.method === 'OPTIONS') return new Response('ok', { headers: h });
  if (req.method !== 'POST') return out(405, { error: 'method' });
  if (!origin || !ALLOW.some(r => r.test(origin))) return out(403, { error: 'origin' });
  const key = Deno.env.get('GEMINI_API_KEY');
  if (!key) return out(503, { error: 'not_configured' });
  let body: { image?: string; mime?: string; prompt?: string };
  try { body = await req.json(); } catch { return out(400, { error: 'bad_json' }); }
  const image = String(body.image || '');
  const prompt = String(body.prompt || '').slice(0, 4000);
  if (!image || !prompt) return out(400, { error: 'missing' });
  if (image.length > 8_000_000) return out(413, { error: 'too_large' });
  const mime = /^image\/(png|jpeg|webp|heic|heif)$/.test(String(body.mime)) ? String(body.mime) : 'image/jpeg';
  // 사용량 제한(접속 IP 해시 기준, 원본 IP는 저장하지 않음)
  const ip = (req.headers.get('x-forwarded-for') || '').split(',')[0].trim() || 'unknown';
  const who = await sha('suji:' + ip);
  const sb = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
  const capWho = +(Deno.env.get('SUJI_OCR_CAP_WHO') || 30);
  const capAll = +(Deno.env.get('SUJI_OCR_CAP_ALL') || 200);
  const { data: hit, error: hitErr } = await sb.rpc('suji_ocr_hit', { p_who: who, p_cap_who: capWho, p_cap_all: capAll });
  if (hitErr) return out(500, { error: 'usage_db', detail: hitErr.message });
  if (!hit?.ok) return out(429, { error: hit?.why === 'all' ? 'cap_all' : 'cap_who' });
  const tried: string[] = [];
  let quota = 0;
  const t0 = Date.now();
  for (const model of await pickModels(key)) {
    if (Date.now() - t0 > 70_000) { tried.push(model + ':skip_time'); continue; }
    const ctl = new AbortController();
    const tm = setTimeout(() => ctl.abort(), Math.max(10_000, 110_000 - (Date.now() - t0)));
    let r: Response;
    try {
      r = await fetch(`${API}/models/${model}:generateContent`, {
        signal: ctl.signal, method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }, { inline_data: { mime_type: mime, data: image } }] }],
          generationConfig: { responseMimeType: 'application/json', temperature: 0 }
        })
      });
    } catch { tried.push(model + ':timeout'); continue; } finally { clearTimeout(tm); }
    const j = await r.json().catch(() => ({}));
    if (r.ok) {
      const txt = (j?.candidates?.[0]?.content?.parts || []).filter((p: any) => !p.thought).map((p: { text?: string }) => p.text || '').join('');
      try { return out(200, { ok: true, model, tried, data: JSON.parse(txt.replace(/^```(json)?|```$/g, '').trim()), left: capWho - hit.mine }); }
      catch { tried.push(model + ':bad_json'); continue; }
    }
    const msg = String(j?.error?.message || r.status).slice(0, 120);
    tried.push(`${model}:${r.status}:${msg}`);
    if (r.status === 429) { quota++; continue; }
    if (r.status === 400 && /API key/i.test(msg) || r.status === 401 || r.status === 403) return out(503, { error: 'bad_key', tried });
  }
  return out(quota ? 429 : 502, { error: quota ? 'gemini_quota' : 'gemini', tried });
});
