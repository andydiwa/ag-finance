-- A&G Finance — one-time Supabase setup.
-- Paste this whole file into Supabase → SQL Editor → New query, then tap Run.
-- Safe to run again.

-- 1. Who may use the app (exactly two people).
create table if not exists public.members (
  email text primary key,
  name  text not null unique check (name in ('Andy', 'Geri'))
);
insert into public.members (email, name) values
  (lower('andyroblesdiwa@gmail.com'), 'Andy'),
  (lower('cyllemagallano@gmail.com'), 'Geri')
on conflict (name) do update set email = excluded.email;

-- 2. All app data: one row per record, account and history entry.
create table if not exists public.items (
  collection text not null check (collection in ('records', 'accounts', 'events')),
  id         text not null,
  data       jsonb not null,
  updated_at timestamptz not null default now(),
  updated_by text,
  primary key (collection, id)
);
alter table public.items replica identity full;

-- 3. Only the two members can read or change anything.
create or replace function public.is_member() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.members where email = lower(auth.jwt() ->> 'email'))
$$;

alter table public.members enable row level security;
alter table public.items   enable row level security;

drop policy if exists "members can see the member list" on public.members;
create policy "members can see the member list" on public.members
  for select to authenticated using (public.is_member());

drop policy if exists "members can use items" on public.items;
create policy "members can use items" on public.items
  for all to authenticated using (public.is_member()) with check (public.is_member());

revoke all on public.members from anon;
revoke all on public.items   from anon;
grant select on public.members to authenticated;
grant select, insert, update, delete on public.items to authenticated;

-- 4. Block sign-ups from any other email address.
create or replace function public.only_members_can_sign_up() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if not exists (select 1 from public.members where email = lower(new.email)) then
    raise exception 'This email is not on the A&G list';
  end if;
  return new;
end $$;
drop trigger if exists only_members_can_sign_up on auth.users;
create trigger only_members_can_sign_up before insert on auth.users
  for each row execute function public.only_members_can_sign_up();

-- 5. Live updates between devices.
do $$ begin
  alter publication supabase_realtime add table public.items;
exception when duplicate_object then null;
end $$;
