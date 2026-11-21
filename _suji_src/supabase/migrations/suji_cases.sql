-- 실사업 사례 제보 (준비안 2026-11-21, 아직 적용하지 않음 — plan/case-collect.md 참고)
create table if not exists public.suji_cases (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  device_hash text not null,
  product text not null,
  sido text not null,
  sigungu text not null,
  zone text,
  biz_year int check (biz_year between 2010 and 2035),
  site_py numeric check (site_py > 0),
  gfa_py numeric check (gfa_py > 0),
  units int check (units >= 0),
  structure text check (structure in ('pf','bunyangbul','trust')),
  land_eok numeric check (land_eok >= 0),
  cost_eok numeric check (cost_eok > 0),
  total_eok numeric check (total_eok > 0),
  sales_eok numeric check (sales_eok > 0),
  est jsonb not null default '{}'::jsonb,      -- 같은 조건의 SuziQ 추정치
  app_ver text,
  consent_ver text not null,
  status text not null default 'pending' check (status in ('pending','review','dup','ok','rejected'))
);
alter table public.suji_cases enable row level security;
-- 정책 없음 = anon/authenticated 직접 읽기·쓰기 불가. 쓰기는 아래 RPC로만.

create or replace function public.suji_case_submit(c jsonb)
returns jsonb language plpgsql security definer set search_path = public as $$
declare d text := c->>'device_hash'; n int; st text := 'pending';
  tot numeric := (c->>'total_eok')::numeric; sal numeric := (c->>'sales_eok')::numeric;
  cost numeric := (c->>'cost_eok')::numeric; gfa numeric := (c->>'gfa_py')::numeric;
begin
  if d is null or length(d) < 8 or coalesce(c->>'consent_ver','') = '' then
    return jsonb_build_object('ok', false, 'err', 'invalid');
  end if;
  select count(*) into n from suji_cases where device_hash = d and created_at > now() - interval '1 day';
  if n >= 5 then return jsonb_build_object('ok', false, 'err', 'limit'); end if;
  if tot / nullif(sal, 0) not between 0.5 and 1.3
     or cost * 1e4 / nullif(gfa, 0) not between 200 and 3000 then st := 'review'; end if;
  if exists (select 1 from suji_cases where sigungu = c->>'sigungu' and biz_year = (c->>'biz_year')::int
             and abs(gfa_py - gfa) <= gfa * 0.02) then st := 'dup'; end if;
  insert into suji_cases (device_hash, product, sido, sigungu, zone, biz_year, site_py, gfa_py, units, structure,
    land_eok, cost_eok, total_eok, sales_eok, est, app_ver, consent_ver, status)
  values (d, c->>'product', c->>'sido', c->>'sigungu', c->>'zone', (c->>'biz_year')::int, (c->>'site_py')::numeric,
    gfa, (c->>'units')::int, c->>'structure', (c->>'land_eok')::numeric, cost, tot, sal,
    coalesce(c->'est', '{}'::jsonb), c->>'app_ver', c->>'consent_ver', st);
  return jsonb_build_object('ok', true, 'status', st);
end $$;
revoke all on function public.suji_case_submit(jsonb) from public;
grant execute on function public.suji_case_submit(jsonb) to anon, authenticated;
