const CACHE='shellwork-57dabc4c6736';
const SHELL=["/shellwork/static/shellwork/css/shellwork.72b6f54a4805.css", "/shellwork/static/shellwork/js/rolodex.632b6c9e3c5b.js", "/shellwork/static/shellwork/js/compare.a10907f3ff26.js", "/shellwork/static/shellwork/js/helper.11f7cc9338e8.js", "/shellwork/static/shellwork/js/compare-page.d85b45e3af7c.js", "/shellwork/static/shellwork/icons/icon-192.db3ea9654ab1.png", "/shellwork/static/shellwork/icons/icon-512.ea6d3589c94f.png"];
const OFFLINE='/shellwork/offline/';
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(SHELL.concat([OFFLINE,'/shellwork/']))).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith('shellwork-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;const u=new URL(r.url);
 if(r.mode==='navigate'){e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp));return res}).catch(()=>caches.match(r).then(m=>m||caches.match(OFFLINE))));return}
 if(u.origin===location.origin||u.host.endsWith('gstatic.com')||u.host.endsWith('googleapis.com')){
  e.respondWith(caches.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok||res.type==='opaque'){const cp=res.clone();caches.open(CACHE).then(c=>c.put(r,cp))}return res})))}});
