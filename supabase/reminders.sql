-- A&G Finance — due-date reminders. Run once in Supabase → SQL Editor (after setup.sql).
-- Stores each phone's notification address. Only the owner can see or change their own rows;
-- the daily reminder job reads them with the service key.
create table if not exists public.push_subs (
  endpoint    text primary key,
  email       text not null,
  sub         jsonb not null,
  days_before int  not null default 1 check (days_before between 0 and 7),
  created_at  timestamptz not null default now()
);
alter table public.push_subs enable row level security;
drop policy if exists "own push subscriptions" on public.push_subs;
create policy "own push subscriptions" on public.push_subs
  for all to authenticated
  using (public.is_member() and email = lower(auth.jwt() ->> 'email'))
  with check (public.is_member() and email = lower(auth.jwt() ->> 'email'));
revoke all on public.push_subs from anon;
grant select, insert, update, delete on public.push_subs to authenticated;
