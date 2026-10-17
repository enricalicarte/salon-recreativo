/* Salón Recreativo: service worker. Portada y recursos básicos disponibles sin conexión; los juegos se guardan al jugarlos. */
const V='sr-2026-10-18',CORE=['./','assets/fonts.css','assets/lenis.min.js','manifest.webmanifest','icons/icon-192.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>Promise.all(CORE.map(u=>c.add(u).catch(()=>{})))).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const r=e.request,u=new URL(r.url);
  if(r.method!=='GET'||u.origin!==location.origin||r.headers.has('range')||/\/media\//.test(u.pathname))return;
  const put=res=>{if(res&&res.status===200&&res.type==='basic'){const c=res.clone();caches.open(V).then(x=>x.put(r,c));}return res;};
  if(r.mode==='navigate'||/\/(juegos)\//.test(u.pathname)){
    e.respondWith(fetch(r).then(put).catch(()=>caches.match(r).then(m=>m||caches.match('./'))));return;}
  e.respondWith(caches.match(r).then(m=>{const f=fetch(r).then(put).catch(()=>m);return m||f;}));
});
