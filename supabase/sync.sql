-- A&G Finance — faster syncing. Run once in Supabase → SQL Editor (safe to run again).
-- Stamps every saved row with the server's clock so phones can download only what changed.
create or replace function public.items_touch() returns trigger
language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end $$;
drop trigger if exists items_touch on public.items;
create trigger items_touch before insert or update on public.items
  for each row execute function public.items_touch();
create index if not exists items_updated_at_idx on public.items (updated_at);
