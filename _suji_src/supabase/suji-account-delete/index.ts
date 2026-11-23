// SuziQ 회원 탈퇴: 로그인한 본인 계정만 즉시 삭제(auth.users 삭제 → suji_profiles 등 연결 자료도 함께 삭제)
import { createClient } from "npm:@supabase/supabase-js@2.49.4";

const ORIGINS = ["https://chulheelim30-cmyk.github.io", "capacitor://localhost", "https://localhost", "http://localhost"];
const cors = (o: string | null) => ({
  "Access-Control-Allow-Origin": o && ORIGINS.includes(o) ? o : ORIGINS[0],
  "Access-Control-Allow-Headers": "authorization, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Vary": "Origin",
});

Deno.serve(async (req) => {
  const h = cors(req.headers.get("origin"));
  if (req.method === "OPTIONS") return new Response(null, { headers: h });
  if (req.method !== "POST") return new Response(JSON.stringify({ ok: false, error: "POST only" }), { status: 405, headers: { ...h, "Content-Type": "application/json" } });
  const token = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const { data, error } = await admin.auth.getUser(token);
  if (error || !data?.user) return new Response(JSON.stringify({ ok: false, error: "로그인이 필요합니다" }), { status: 401, headers: { ...h, "Content-Type": "application/json" } });
  const { error: delErr } = await admin.auth.admin.deleteUser(data.user.id);
  if (delErr) return new Response(JSON.stringify({ ok: false, error: "삭제하지 못했습니다. 잠시 후 다시 시도해 주세요" }), { status: 500, headers: { ...h, "Content-Type": "application/json" } });
  return new Response(JSON.stringify({ ok: true }), { headers: { ...h, "Content-Type": "application/json" } });
});
