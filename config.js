// Supabase connection for A&G Finance.
// The anon key is meant to be public: access is protected by the row-level security rules in supabase/setup.sql.
window.AG_CONFIG = {
  url: 'https://vfgaopmunjrdjjtsdvrs.supabase.co',
  anonKey: 'sb_publishable_UZ4Vxm5p3fz16Db8Qan7zA_Uf7rfe-h',
  // Public half of the push-notification key (the private half is a GitHub secret).
  vapidPublicKey: 'BEvr3DocmrVbShbp0btUZkDBc2dzFACoL2ZHnwo9xDjX60aIAr3HUZFmi5OoDhTzeGojm1SXy2TfvbgQzJjeDWM'
};
