// Daily due-date reminders for A&G Finance (run by .github/workflows/reminders.yml).
// Reads bills, installments and loans from Supabase and sends a Web Push notification to each
// subscribed phone for anything due today or N days from today that is not yet paid this month.
import webpush from 'web-push';

const { SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY: KEY, VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, TEST } = process.env;
if (!KEY || !VAPID_PRIVATE_KEY) { console.error('Missing secrets: SUPABASE_SERVICE_ROLE_KEY and/or VAPID_PRIVATE_KEY'); process.exit(1); }
webpush.setVapidDetails('https://andydiwa.github.io/ag-finance/', VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY);

const H = KEY.startsWith('sb_') ? { apikey: KEY } : { apikey: KEY, Authorization: 'Bearer ' + KEY };
async function api(path, opts = {}) {
  const r = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, { ...opts, headers: { ...H, ...(opts.headers || {}) } });
  if (!r.ok) throw new Error(`${path} → ${r.status} ${await r.text()}`);
  return r.status === 204 ? null : r.json();
}
async function allRecords() {
  const out = [];
  for (let from = 0; ; from += 1000) {
    const page = await api('items?select=data&collection=eq.records&order=id', { headers: { Range: `${from}-${from + 999}` } });
    out.push(...page.map(x => x.data));
    if (page.length < 1000) return out;
  }
}

const peso = c => '₱' + (c / 100).toLocaleString('en-PH', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
const shareOf = (a, u) => (u === 'Andy' ? Math.round(a / 2) : a - Math.round(a / 2));
// "Today" in Manila.
const now = new Date(Date.now() + 8 * 3600e3);
const Y = now.getUTCFullYear(), M = now.getUTCMonth(), D = now.getUTCDate();
const ym = `${Y}-${String(M + 1).padStart(2, '0')}`;
const dim = new Date(Date.UTC(Y, M + 1, 0)).getUTCDate();

function dueItems(records, name, daysBefore) {
  const pays = records.filter(p => p.kind === 'payment' && !p.deleted);
  const out = [];
  for (const r of records) {
    if (r.deleted || !['bill', 'installment', 'loan'].includes(r.kind)) continue;
    if (r.owner !== name && r.owner !== 'Shared') continue;
    const dueDay = Math.min(Number(r.dueDay) || 0, dim);
    if (!dueDay) continue;
    const until = dueDay - D;
    if (until !== 0 && until !== daysBefore) continue;
    const monthly = r.kind === 'loan' ? Number(r.monthlyPayment) || 0 : Number(r.amount) || 0;
    const mine = r.owner === 'Shared' ? shareOf(monthly, name) : monthly;
    const mineOnly = p => r.owner !== 'Shared' || p.paidBy === name;
    const rp = pays.filter(p => p.parentId === r.id && mineOnly(p));
    const paidThisMonth = rp.filter(p => (p.date || '').startsWith(ym)).reduce((s, p) => s + p.amount, 0);
    if (mine > 0 && paidThisMonth >= mine) continue;
    if (r.kind !== 'bill' && r.loanMonthsLeft !== null && r.loanMonthsLeft !== undefined && r.loanMonthsLeft !== '') {
      const since = r.loanMonthsSetISO || '';
      const paidSince = rp.filter(p => (p.createdAtISO || '') >= since).reduce((s, p) => s + p.amount, 0);
      if (Number(r.loanMonthsLeft) * mine - paidSince <= 0) continue;           // fully paid
      const set = since ? new Date(new Date(since).getTime() + 8 * 3600e3) : null; // set after this month's due day → this month counted as paid
      if (set && set.getUTCFullYear() === Y && set.getUTCMonth() === M && set.getUTCDate() > dueDay && paidThisMonth === 0) continue;
    }
    out.push({ name: r.name, amount: Math.max(0, mine - paidThisMonth), until });
  }
  return out.sort((a, b) => a.until - b.until);
}

const members = await api('members?select=email,name');
const subs = await api('push_subs?select=endpoint,email,sub,days_before');
const records = TEST === 'true' ? [] : await allRecords();
let sent = 0, removed = 0;
for (const s of subs) {
  const m = members.find(x => x.email === s.email);
  if (!m) continue;
  let payload;
  if (TEST === 'true') {
    payload = { title: 'A&G Finance', body: `Reminders are working for ${m.name} ✓`, tag: 'ag-test' };
  } else {
    const items = dueItems(records, m.name, s.days_before);
    if (!items.length) continue;
    const when = u => (u === 0 ? 'today' : u === 1 ? 'tomorrow' : `in ${u} days`);
    const total = items.reduce((z, i) => z + i.amount, 0);
    payload = items.length === 1
      ? { title: `Due ${when(items[0].until)}: ${items[0].name}`, body: `${peso(items[0].amount)} · Tap to open A&G Finance` }
      : { title: `${items.length} payments due soon · ${peso(total)}`, body: items.map(i => `${i.name} ${peso(i.amount)} (${when(i.until)})`).join('\n') };
    payload.tag = 'ag-due-' + ym + '-' + D;
  }
  try { await webpush.sendNotification(s.sub, JSON.stringify({ ...payload, url: './' })); sent++; }
  catch (e) {
    if (e.statusCode === 404 || e.statusCode === 410) { await api(`push_subs?endpoint=eq.${encodeURIComponent(s.endpoint)}`, { method: 'DELETE' }); removed++; }
    else console.error('Push failed for', m.name, e.statusCode || '', e.body || e.message);
  }
}
console.log(`Checked ${subs.length} device(s); sent ${sent}; removed ${removed} expired.`);
