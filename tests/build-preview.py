import re,sys
src=open(__import__('os').path.join(__import__('os').path.dirname(__file__),'..','index.html'),encoding='utf-8').read()
title=re.search(r'<title>.*?</title>',src).group(0)
style=re.search(r'<style>.*?</style>',src,re.S).group(0)
body=re.search(r'<body>(.*)</body>',src,re.S).group(1)
mock=r"""<script>
// ===== PREVIEW ONLY: pretend database with demo data (nothing is sent anywhere) =====
window.AG_CONFIG={url:'https://preview.local',anonKey:'preview',vapidPublicKey:'BEvr3DocmrVbShbp0btUZkDBc2dzFACoL2ZHnwo9xDjX60aIAr3HUZFmi5OoDhTzeGojm1SXy2TfvbgQzJjeDWM'};
(()=>{const LS={get(k){try{return localStorage.getItem(k)}catch{return null}},set(k,v){try{localStorage.setItem(k,v)}catch{}},del(k){try{localStorage.removeItem(k)}catch{}}};
const MEM={'andyroblesdiwa@gmail.com':'Andy','cyllemagallano@gmail.com':'Geri','andy':'Andy','geri':'Geri'};
let rows=JSON.parse(LS.get('pv-rows')||'null');
if(!rows){rows={};const t=new Date(),ym=t.toISOString().slice(0,7),iso=t.toISOString(),at=t.toLocaleString();let id=Date.now()*1000;const add=(c,o)=>{o.id=++id;o.createdAt=at;o.createdAtISO=iso;o.date=o.date||ym+'-01';o.repayments=o.repayments||[];rows[c+'/'+o.id]={collection:c,id:String(o.id),data:o}};
 add('records',{kind:'income',name:'Income / Payroll',amount:2500000,date:ym+'-01',owner:'Andy',scope:'personal',paidBy:'Andy'});
 add('records',{kind:'income',name:'Income / Payroll',amount:100000,owner:'Andy',scope:'personal',paidBy:'Andy',asCash:true,date:ym+'-02'});
 add('records',{kind:'cashin',date:ym+'-03',name:'Cash withdrawn',amount:200000,owner:'Andy',scope:'personal',source:'withdraw'});
 add('records',{kind:'bill',name:'Meralco',amount:150000,owner:'Andy',scope:'personal',paidBy:'Andy',dueDay:20,cutoff:'15'});
 add('records',{kind:'bill',name:'Netflix',amount:54900,owner:'Andy',scope:'personal',paidBy:'Andy',dueDay:5,cutoff:'15',autoPay:true});
 add('records',{kind:'bill',name:'Internet (PLDT)',amount:169900,owner:'Shared',scope:'shared',paidBy:'Andy',dueDay:25,cutoff:'30'});
 add('records',{kind:'loan',name:'Home Credit',amount:3000000,monthlyPayment:250000,loanTotalMonths:12,loanMonthsLeft:8,loanMonthsSetISO:iso,owner:'Andy',borrower:'Andy',holder:'Andy',scope:'personal',paidBy:'Andy',dueDay:22,cutoff:'15'});
 add('records',{kind:'installment',name:'iPhone 16',amount:300000,totalMonths:12,paidMonths:6,loanMonthsLeft:6,loanMonthsSetISO:iso,owner:'Andy',scope:'personal',paidBy:'Andy',dueDay:28,cutoff:'30'});
 add('records',{kind:'expense',name:'Groceries',date:ym+'-05',amount:80000,owner:'Andy',scope:'personal',paidBy:'Andy',deductBalance:true,deductFrom:'balance',cutoff:'15'});
 add('records',{kind:'expense',name:'Taho',date:ym+'-06',amount:4000,owner:'Andy',scope:'personal',paidBy:'Andy',cashOnHand:true,deductFrom:'cash',deductBalance:false,cutoff:'15'});
 add('records',{kind:'dump',name:'Grab to BGC',date:ym+'-07',amount:28500,owner:'Andy',scope:'personal',paidWith:'GCash',addedBy:'Andy'});
 add('records',{kind:'dump',name:'Groceries at SM',date:ym+'-08',amount:240000,owner:'Shared',scope:'shared',paidWith:'Card',addedBy:'Geri'});
 LS.set('pv-rows',JSON.stringify(rows))}
const save=()=>LS.set('pv-rows',JSON.stringify(rows));let handler=null,authCb=null,sess=JSON.parse(LS.get('pv-sess')||'null');
function q(t){let f={},gtv=null,cols='',op='select',payload=null,rng=[0,99999];const b={select(c){cols=c||'';return b},gt(k,v){gtv=v;return b},order(){return b},range(a,z){rng=[a,z];return b},eq(k,v){f[k]=v;return b},maybeSingle(){if(t==='members'){const n=MEM[f.email];return Promise.resolve({data:n?{name:n}:null,error:null})}return Promise.resolve({data:null,error:null})},upsert(p){op='upsert';payload=p;return b},delete(){op='delete';return b},then(res,rej){let out={data:[],error:null};if(t==='items'){if(op==='select'){let all=Object.values(rows).filter(r=>!gtv||(r.updated_at||'')>gtv).sort((a,b)=>(a.updated_at||'').localeCompare(b.updated_at||'')||(a.id>b.id?1:-1));if(!cols.includes('data'))all=all.map(r=>({collection:r.collection,id:r.id}));window.__rowsSent=(window.__rowsSent||0)+Math.min(all.length,rng[1]-rng[0]+1);out={data:all.slice(rng[0],rng[1]+1),error:null}}else if(op==='upsert'){payload={...payload,updated_at:new Date().toISOString()};rows[payload.collection+'/'+payload.id]=payload;save();setTimeout(()=>handler&&handler({eventType:'UPDATE',new:payload}))}else{delete rows[f.collection+'/'+f.id];save();setTimeout(()=>handler&&handler({eventType:'DELETE',old:{collection:f.collection,id:f.id}}))}}return new Promise(r=>setTimeout(()=>r(out),t==='items'&&op==='select'&&!window.__pvLoaded?(window.__pvLoaded=1,900):0)).then(res,rej)}};return b}
const client={from:q,auth:{getSession:async()=>({data:{session:sess}}),onAuthStateChange(cb){authCb=cb},
 signInWithPassword:async({email})=>{if(!MEM[email])return {error:{message:'Preview: use andyroblesdiwa@gmail.com or cyllemagallano@gmail.com (any password).'}};sess={user:{email}};LS.set('pv-sess',JSON.stringify(sess));authCb&&authCb('SIGNED_IN',sess);return {data:{session:sess}}},
 signUp:async({email})=>MEM[email]?client.auth.signInWithPassword({email}):{error:{message:'Database error saving new user'}},
 signOut:async()=>{sess=null;LS.del('pv-sess');authCb&&authCb('SIGNED_OUT',null)}},
 channel(){const c={on(_a,_b,h){handler=h;return c},subscribe(cb){setTimeout(()=>cb('SUBSCRIBED'));return c}};return c},removeChannel(){}};
window.supabase={createClient:()=>client};
window.__pvReset=()=>{LS.del('pv-rows');LS.del('pv-sess');location.reload()};})();
</script>"""
banner='<div class="pvbanner">PREVIEW · demo data · <button onclick="__pvReset()">Reset</button></div>'
pvcss='<style>.pvbanner{position:fixed;top:calc(6px + env(safe-area-inset-top,0px));left:50%;transform:translateX(-50%);z-index:50;background:#e2a03f;color:#2b1a00;font:700 11px/1 -apple-system,BlinkMacSystemFont,sans-serif;letter-spacing:.4px;padding:6px 6px 6px 12px;border-radius:999px;display:flex;align-items:center;gap:8px;box-shadow:0 6px 18px #0002;white-space:nowrap}.pvbanner button{border:0;background:#2b1a00;color:#fff;font:700 10px/1 inherit;padding:5px 9px;border-radius:999px}</style>'
body=body.replace('<script src="vendor/supabase.js"></script><script src="config.js"></script>',mock)
assert mock in body
# hint on the login screen
body=body.replace("Only Andy and Geri can sign in. Your data syncs live across your devices.","Preview: sign in as andyroblesdiwa@gmail.com or cyllemagallano@gmail.com with any password.")
open(sys.argv[1],'w',encoding='utf-8').write(title.replace('A&G Finance','A&G Finance Preview')+'\n'+style+pvcss+'\n'+banner+body)
