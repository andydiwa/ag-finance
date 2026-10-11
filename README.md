# A&G Finance

Shared finance tracker for Andy and Geri: installments, bills, loans and PayLater, shared expenses with 50/50 splits, IOUs with repayment confirmation, mutual offsets, shared savings and an audit history.

- **App:** a single static page (`index.html`) hosted on GitHub Pages.
- **Data and sign-in:** Supabase (Postgres + Auth + Realtime). Only the two emails in `public.members` can sign up, read or write.
- **Money** is stored as integer centavos; shared amounts split with Andy taking the rounded half.

## Setup

1. Supabase → SQL Editor → run `supabase/setup.sql`.
2. Supabase → Authentication → Sign In / Providers → Email: turn off **Confirm email** (sign-ups are already limited to the two member emails).
3. Put the Project URL and anon public key in `config.js`.
4. GitHub → Settings → Pages → Deploy from branch `main`, folder `/ (root)`.

Each person opens the site, taps **Create account** once with their member email, then signs in on any device.
