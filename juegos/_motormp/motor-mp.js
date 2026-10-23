/* Moto Fury y Monster Smash · carrera multijugador de 2 a 4 móviles (WebRTC / PeerJS)
   El mismo mundo y la misma carrera (la pista sale de la misma semilla), salida a la vez con la cuenta atrás
   del juego y los vehículos de los demás como fantasmas en la pista. Gana el mejor tiempo hasta la meta.
   El juego expone window.__motor y llama a window.__motorMP.fin()/fuera() al llegar a la meta o volcar. */
(function(){
'use strict';
const __invSrc=(document.currentScript&&document.currentScript.src)||'';
function conInvita(cb){if(window.SalaInvita)return cb();const s=document.createElement('script');s.src=new URL('../_sala/invita.js',__invSrc||location.href).href;s.onload=cb;document.head.appendChild(s);}
const A=()=>window.__motor;
const MAXP=4;
const $q=id=>document.getElementById(id);
const esc=t=>String(t==null?'':t).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const M={on:false,host:false,me:0,peer:null,conn:null,code:'',fase:'off',jug:[],listo:false,w:0,c:0,res:{},envT:null,raf:0};
let miNom='';try{miNom=(localStorage.getItem('motorrace-nom')||'').slice(0,12);}catch(e){}
const NOMBRE=()=>(A()&&A().nombre)||'Carrera';
const COLS=[0xff4fd8,0x38e8ff,0xffd23f,0x6dff8a];

const css=document.createElement('style');css.textContent=`
#mmpBtn{display:block;margin:10px auto 0;font:800 15px system-ui,sans-serif;color:#fff;background:rgba(10,14,30,.75);border:2px solid rgba(255,255,255,.55);border-radius:999px;padding:10px 20px;cursor:pointer}
#mmp{z-index:60;background:rgba(6,8,20,.86);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
#mmp .mc{width:min(440px,94vw);max-height:92vh;overflow-y:auto;background:linear-gradient(180deg,rgba(30,34,70,.96),rgba(12,14,32,.98));border:1.5px solid rgba(255,255,255,.3);border-radius:22px;padding:18px 16px;color:#fff;font-family:system-ui,-apple-system,'Segoe UI',sans-serif;text-align:center}
#mmp h2{margin:0 0 6px;font-size:26px;font-weight:900;letter-spacing:.03em}
#mmp p{margin:6px 0 10px;font-size:14.5px;opacity:.88;line-height:1.35}
#mmp .et{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:800;opacity:.7;margin:12px 0 6px}
#mmp button.b{font:800 16px system-ui,sans-serif;color:#1a1300;background:#ffd23f;border:0;border-radius:999px;padding:11px 22px;margin:4px;cursor:pointer;box-shadow:0 4px 0 #b88a00}
#mmp button.b2{font:700 14px system-ui,sans-serif;color:#fff;background:rgba(255,255,255,.1);border:1.5px solid rgba(255,255,255,.4);border-radius:999px;padding:9px 18px;margin:4px;cursor:pointer}
#mmp button:disabled{opacity:.5;cursor:default}
#mmp input{font:800 20px system-ui,sans-serif;color:#fff;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.45);border-radius:14px;padding:9px 12px;text-align:center;width:100%;max-width:240px;outline:none;user-select:text;-webkit-user-select:text}
#mmp input:disabled{opacity:.55}
#mmpCodIn{text-transform:uppercase;letter-spacing:.2em;width:8ch!important}
#mmp .fila{display:flex;gap:6px;justify-content:center;align-items:center;flex-wrap:wrap}
#mmp .cod{font-size:clamp(42px,13vw,58px);font-weight:900;letter-spacing:.2em;color:#ffd23f;line-height:1.05}
#mmp .jl{display:flex;flex-direction:column;gap:6px;margin:8px 0;text-align:left}
#mmp .jl div{display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.18);border-radius:14px;padding:7px 12px}
#mmp .jl div.yo{border-color:#ffd23f}
#mmp .jl b{flex:1;font-size:16px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#mmp .jl em{font-style:normal;font-weight:700;font-size:12.5px;opacity:.8;white-space:nowrap}
#mmp .jl div.vacio{justify-content:center;border-style:dashed;opacity:.7;font-size:13.5px}
#mmp .ops{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
#mmp .ops button{font:700 13.5px system-ui,sans-serif;color:#fff;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.25);border-radius:12px;padding:8px 11px;cursor:pointer}
#mmp .ops button.sel{background:#ffd23f;border-color:#ffd23f;color:#1a1300}
#mmp .ops.solo button{pointer-events:none}
#mmp table{width:100%;border-collapse:collapse;margin:10px 0;font-size:15px}
#mmp td,#mmp th{padding:6px 4px;border-bottom:1px solid rgba(255,255,255,.12)}
#mmp th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;opacity:.7}
#mmp tr.yo td{color:#ffd23f;font-weight:800}
#mmpHud{position:fixed;left:10px;top:calc(140px + env(safe-area-inset-top,0px));z-index:30;display:flex;flex-direction:column;gap:4px;pointer-events:none;font:800 13px/1 system-ui,sans-serif;color:#fff}
#mmpHud[hidden]{display:none}
#mmpHud div{display:flex;gap:7px;align-items:center;background:rgba(8,10,26,.7);border:1.5px solid rgba(255,255,255,.25);border-radius:999px;padding:5px 10px;min-width:130px}
#mmpHud div.yo{border-color:#ffd23f}
#mmpHud div.fuera{opacity:.45;text-decoration:line-through}
#mmpHud i{font-style:normal;width:16px;text-align:center;color:#ffd23f}
#mmpHud b{flex:1;max-width:80px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#mmpHud span{font-variant-numeric:tabular-nums}
`;document.head.appendChild(css);
const ov=document.createElement('div');ov.id='mmp';ov.className='ov hide';ov.innerHTML=`
<div class="mc" id="mmpIni"><h2>🏁 Carrera con amigos</h2><p>De 2 a 4 jugadores, cada uno en su móvil: la misma pista, salida a la vez y los demás como fantasmas a tu lado. Gana el mejor tiempo. Vale con wifi distintos o datos móviles.</p>
  <button class="b" id="mmpCrea">Crear sala</button><div class="et">— o únete con un código —</div>
  <div class="fila"><input id="mmpCodIn" maxlength="4" placeholder="CÓDIGO" autocomplete="off" autocapitalize="characters" spellcheck="false"><button class="b2" id="mmpUne" style="font-size:16px">Unirme</button></div>
  <p id="mmpInfo" style="min-height:20px;margin-bottom:4px"></p><button class="b2" id="mmpSal1">Volver</button></div>
<div class="mc" id="mmpSala" hidden><div class="et" style="margin-top:0">Código de la sala</div><div class="cod" id="mmpCod">----</div>
  <div class="jl" id="mmpJug"></div>
  <div class="et">Tu nombre</div><input id="mmpNom" maxlength="12" autocomplete="off" spellcheck="false" placeholder="Nombre">
  <div class="et">Mundo</div><div class="ops" id="mmpW"></div>
  <div class="et">Carrera</div><div class="ops" id="mmpC"></div>
  <p id="mmpInfoS"></p><button class="b" id="mmpListo">¡Listo!</button><button class="b" id="mmpEmp">Empezar</button><br><button class="b2" id="mmpSal2">Salir</button></div>
<div class="mc" id="mmpRes" hidden><h2 id="mmpResT">Resultado</h2><p id="mmpResS"></p>
  <table><thead><tr><th></th><th style="text-align:left">Piloto</th><th>Tiempo</th><th>Caídas</th></tr></thead><tbody id="mmpResL"></tbody></table>
  <button class="b" id="mmpRev">Revancha</button><br><button class="b2" id="mmpSal3">Salir del multijugador</button></div>`;
document.body.appendChild(ov);
const hud=document.createElement('div');hud.id='mmpHud';hud.hidden=true;document.body.appendChild(hud);
function abre(k){ov.classList.remove('hide');['mmpIni','mmpSala','mmpRes'].forEach(id=>$q(id).hidden=id!==k);}
function cierra(){ov.classList.add('hide');}
function info(id,t){$q(id).textContent=t;}
(function(){const pb=$q('play');if(!pb)return;const b=document.createElement('button');b.id='mmpBtn';b.type='button';b.textContent='👥 Carrera con amigos · 2 a 4 móviles';
  pb.parentNode.insertBefore(b,pb.nextSibling);
  ['pointerdown','click'].forEach(ev=>b.addEventListener(ev,e=>{e.stopPropagation();if(ev==='click'){info('mmpInfo','');abre('mmpIni');}}));})();
ov.addEventListener('pointerdown',e=>e.stopPropagation());

/* ---------- red ---------- */
const PREFIX=()=>'motorrace-'+((A()&&A().kind)||'x')+'-';
function envia(o){o.from=M.me;
  if(M.host)M.jug.forEach(j=>{if(j.conn&&j.conn.open){try{j.conn.send(o);}catch(e){}}});
  else{try{if(M.conn&&M.conn.open)M.conn.send(o);}catch(e){}}}
function reenvia(m,menos){M.jug.forEach(j=>{if(j.conn&&j.conn!==menos&&j.conn.open){try{j.conn.send(m);}catch(e){}}});}
function cargaPeer(cb){if(window.Peer)return cb(true);
  const urls=['https://cdn.jsdelivr.net/npm/peerjs@1.5.4/dist/peerjs.min.js','https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js','https://cdnjs.cloudflare.com/ajax/libs/peerjs/1.5.4/peerjs.min.js'];
  let i=0;(function sig(){if(i>=urls.length)return cb(false);const s=document.createElement('script');s.src=urls[i++];s.onload=()=>cb(!!window.Peer);s.onerror=sig;document.head.appendChild(s);})();}

/* ---------- sala ---------- */
const datosSala=()=>M.jug.map(j=>({nom:j.nom,listo:!!j.listo}));
function difunde(){M.jug.forEach((j,i)=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'sala',tu:i,cod:M.code,w:M.w,c:M.c,jug:datosSala()});}catch(e){}}});pinta();}
function abreSala(){M.fase='sala';M.listo=false;M.res={};hud.hidden=true;paraFantasmas();if(!$q('mmpNom').value)$q('mmpNom').value=miNom||'Piloto';abre('mmpSala');pinta();}
function elige(){const nom=($q('mmpNom').value||'').trim().slice(0,12)||'Piloto';miNom=nom;try{localStorage.setItem('motorrace-nom',nom);}catch(e){}
  if(M.host){M.jug[0].nom=nom;difunde();}else envia({t:'elige',nom,listo:M.listo});}
function pinta(){
  if(M.fase!=='sala')return;const a=A();
  $q('mmpCod').textContent=M.code||'----';
  $q('mmpJug').innerHTML=M.jug.map((j,i)=>'<div class="'+(i===M.me?'yo':'')+'"><span>'+(a.kind==='monster'?'🛻':'🏍️')+'</span><b>'+esc(j.nom)+(i===M.me?' (tú)':'')+'</b><em>'+(i===0?'Anfitrión':j.listo?'✅ ¡Listo!':'Eligiendo…')+'</em></div>').join('')
    +(M.jug.length<MAXP?'<div class="vacio">'+(M.jug.length<2?'Esperando jugadores… comparte el código':'Puede entrar alguien más (máx. '+MAXP+')')+'</div>':'');
  $q('mmpNom').disabled=M.listo;
  const W=$q('mmpW'),C=$q('mmpC');W.classList.toggle('solo',!M.host);C.classList.toggle('solo',!M.host);
  const ws=a.LEVELS.map((l,i)=>({l,i})),cs=a.CIRCUITS.map((c,i)=>({c,i})).filter(o=>o.c.len>0);
  W.innerHTML=(M.host?ws:ws.filter(o=>o.i===M.w)).map(o=>'<button data-w="'+o.i+'" class="'+(o.i===M.w?'sel':'')+'">'+esc((o.l.emoji||'')+' '+o.l.name)+'</button>').join('');
  C.innerHTML=(M.host?cs:cs.filter(o=>o.i===M.c)).map(o=>'<button data-c="'+o.i+'" class="'+(o.i===M.c?'sel':'')+'">'+(o.i+1)+' · '+esc(o.c.n.toLowerCase())+'</button>').join('');
  if(M.host){W.querySelectorAll('button').forEach(b=>b.onclick=()=>{M.w=+b.dataset.w;difunde();});C.querySelectorAll('button').forEach(b=>b.onclick=()=>{M.c=+b.dataset.c;difunde();});}
  const bl=$q('mmpListo'),be=$q('mmpEmp');
  if(M.host){bl.hidden=true;be.hidden=false;const otros=M.jug.slice(1),todos=otros.length>=1&&otros.every(j=>j.listo);be.disabled=!todos;
    be.textContent=otros.length<1?'Esperando jugadores…':todos?'¡Empezar la carrera! ('+M.jug.length+')':'Esperando a que estén listos…';
    info('mmpInfoS','Tú eliges el mundo y la carrera. Cada piloto pone su nombre y pulsa «¡Listo!».');}
  else{be.hidden=true;bl.hidden=false;bl.textContent=M.listo?'✓ ¡Listo! (cambiar)':'¡Listo!';info('mmpInfoS',M.listo?'Esperando a que el anfitrión empiece…':'Pon tu nombre y pulsa «¡Listo!».');}
}
/* ---------- carrera ---------- */
function empieza(){if(!M.host||$q('mmpEmp').disabled)return;elige();const jug=M.jug.map(j=>({nom:j.nom}));
  M.jug.forEach((j,i)=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'sala',tu:i,cod:M.code,w:M.w,c:M.c,jug:datosSala()});j.conn.send({t:'va',w:M.w,c:M.c,jug});}catch(e){}}});
  arranca(M.w,M.c,jug);}
function arranca(w,c,jug){
  jug.forEach((q,i)=>{const j=M.jug[i]||(M.jug[i]={});j.nom=q.nom;j.fuera=false;j.x=0;j.g=null;});M.jug.length=jug.length;
  M.w=w;M.c=c;M.res={};M.fase='juego';cierra();
  try{A().run(w,c);}catch(e){console.error(e);}
  hud.hidden=false;clearInterval(M.envT);M.envT=setInterval(tic,120);iniciaFantasmas();pintaHud();
}
function tic(){
  if(M.fase!=='juego')return;const a=A(),T=a.T,yo=M.jug[M.me];
  if(!M.res[M.me]&&T){yo.x=T.x;envia({t:'g',x:+T.x.toFixed(2),y:+T.y.toFixed(2),a:+T.a.toFixed(3),vx:+(T.vx||0).toFixed(2),st:a.state});}
  pintaHud();
}
function fin(r){if(M.fase!=='juego'||M.res[M.me])return;const x={t:+(+r.t).toFixed(2),f:1,k:r.k|0};M.res[M.me]=x;envia({t:'fin',tm:x.t,f:x.f,d:x.d|0,k:x.k});revisa();}
function fuera(r){if(M.fase!=='juego'||M.res[M.me])return;const x={t:0,f:0,d:Math.round(r.d||0),k:r.k|0};M.res[M.me]=x;envia({t:'fin',tm:x.t,f:x.f,d:x.d|0,k:x.k});revisa();}
function revisa(){
  const act=M.jug.map((j,i)=>i).filter(i=>!M.jug[i].fuera);pintaHud();
  if(!M.res[M.me])return;
  if(act.every(i=>M.res[i])){M.fase='fin';clearInterval(M.envT);hud.hidden=true;paraFantasmas();setTimeout(resultado,1500);}
}
function pintaHud(){
  if(M.fase!=='juego'){hud.hidden=true;return;}hud.hidden=false;const FIN=A().FIN||1;
  const ord=M.jug.map((j,i)=>({j,i,r:M.res[i],x:i===M.me?(A().T?A().T.x:0):(j.g?j.g.x:0)})).sort((a,b)=>{
    const ra=a.r,rb=b.r;if(ra&&ra.f&&rb&&rb.f)return ra.t-rb.t;if(ra&&ra.f)return -1;if(rb&&rb.f)return 1;return b.x-a.x;});
  hud.innerHTML=ord.map((o,k)=>'<div class="'+(o.i===M.me?'yo':'')+(o.j.fuera?' fuera':'')+'"><i>'+(o.r?(o.r.f?'🏁':'✕'):(k+1))+'</i><b>'+esc(o.i===M.me?'Tú':o.j.nom)+'</b><span>'+(o.r&&o.r.f?o.r.t.toFixed(1)+' s':Math.max(0,Math.min(100,Math.floor(o.x/FIN*100)))+'%')+'</span></div>').join('');
}
function resultado(){
  const ord=M.jug.map((j,i)=>({j,i,r:M.res[i]||{t:0,f:0,d:Math.round(j.g?j.g.x:0)}})).sort((a,b)=>{
    if(a.r.f&&b.r.f)return a.r.t-b.r.t;if(a.r.f)return -1;if(b.r.f)return 1;return (b.r.d||0)-(a.r.d||0);});
  const med=['🥇','🥈','🥉','4º'],yo=ord.findIndex(o=>o.i===M.me);
  $q('mmpResT').textContent=yo===0?'🏆 ¡Has ganado la carrera!':'¡Gana '+ord[0].j.nom+'!';
  const a=A();$q('mmpResS').textContent=(a.LEVELS[M.w].emoji||'')+' '+a.LEVELS[M.w].name+' · '+a.CIRCUITS[M.c].n.toLowerCase();
  $q('mmpResL').innerHTML=ord.map((o,k)=>'<tr class="'+(o.i===M.me?'yo':'')+'"><td>'+(o.r.f?med[k]:'')+'</td><td style="text-align:left">'+esc(o.i===M.me?'Tú':o.j.nom)+(o.j.fuera?' <small>(se fue)</small>':'')+'</td><td>'+(o.r.f?o.r.t.toFixed(2)+' s':'✕ '+(o.r.d||0)+' m')+'</td><td>'+(o.r.k|0)+'</td></tr>').join('');
  $q('mmpRev').textContent='Revancha';['win','over'].forEach(id=>{const e=$q(id);if(e)e.classList.add('hide');});abre('mmpRes');
}
function volver(){if(M.host)volverSala();else{envia({t:'revancha'});$q('mmpRev').textContent='Volviendo…';}}
function volverSala(){
  M.jug=M.jug.filter((j,i)=>i===0||(!j.fuera&&j.conn&&j.conn.open));M.jug.forEach(j=>j.listo=false);M.me=0;
  M.jug.forEach(j=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'abresala'});}catch(e){}}});
  try{A().toMenu();}catch(e){}abreSala();difunde();
}
// botones del juego durante el multijugador
function intercepta(id,fn){const b=$q(id);if(b)['pointerdown','click'].forEach(ev=>b.addEventListener(ev,e=>{if(M.fase==='juego'||M.fase==='fin'){e.stopImmediatePropagation();e.preventDefault();if(ev==='click')fn();}},true));}
['w-next','w-again','again'].forEach(id=>intercepta(id,()=>{if(M.fase==='fin')resultado();}));
['w-menu','tomenu','pmenu'].forEach(id=>intercepta(id,()=>{sal();try{A().toMenu();}catch(e){}}));

/* ---------- fantasmas ---------- */
const GH={};
function fantasma(i){
  const a=A();if(GH[i])return GH[i];
  const g=a.truck.clone(true);g.traverse(o=>{if(o.material){const ms=Array.isArray(o.material)?o.material:[o.material];const nm=ms.map(m=>{const c=m.clone();c.transparent=true;c.opacity=.45;c.depthWrite=false;return c;});o.material=Array.isArray(o.material)?nm:nm[0];}});
  const cv=document.createElement('canvas');cv.width=256;cv.height=64;const x=cv.getContext('2d');x.font='bold 34px system-ui,sans-serif';x.textAlign='center';x.textBaseline='middle';
  x.fillStyle='#'+COLS[i%4].toString(16).padStart(6,'0');x.beginPath();if(x.roundRect)x.roundRect(8,8,240,48,24);else x.rect(8,8,240,48);x.fill();x.fillStyle='#111';x.fillText(String(M.jug[i].nom||'').slice(0,12),128,34);
  const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:new THREE.CanvasTexture(cv),depthTest:false,transparent:true,fog:false}));sp.scale.set(3.2,.8,1);sp.renderOrder=999;
  a.scene.add(g);a.scene.add(sp);GH[i]={g,sp,x:0,y:0};return GH[i];
}
function iniciaFantasmas(){
  cancelAnimationFrame(M.raf);
  const loop=()=>{M.raf=requestAnimationFrame(loop);if(M.fase!=='juego')return;const now=performance.now();
    M.jug.forEach((j,i)=>{if(i===M.me)return;const g=j.g,vis=!j.fuera&&g&&now-g.t<2000&&!(M.res[i]&&M.res[i].f&&now-g.t>800);
      const f=GH[i]||(vis?fantasma(i):null);if(!f)return;f.g.visible=f.sp.visible=!!vis;if(!vis)return;
      const ex=g.x+g.vx*Math.min(.25,(now-g.t)/1000);if(Math.abs(ex-f.x)>15){f.x=ex;f.y=g.y;}else{f.x+=(ex-f.x)*.3;f.y+=(g.y-f.y)*.3;}
      f.g.position.set(f.x,f.y,-2.6-i*.6);f.g.rotation.set(0,0,g.a);f.sp.position.set(f.x,f.y+3.2,-2.6-i*.6);});};
  loop();
}
function paraFantasmas(){cancelAnimationFrame(M.raf);const a=A();for(const k in GH){try{a.scene.remove(GH[k].g);a.scene.remove(GH[k].sp);}catch(e){}delete GH[k];}}

/* ---------- mensajes ---------- */
function recibe(m){
  if(!m||!m.t)return;
  if(m.t==='sala'){M.me=m.tu;M.code=m.cod||M.code;M.w=m.w|0;M.c=m.c|0;const ant=M.jug;M.jug=m.jug.map((q,i)=>Object.assign(ant[i]||{},{nom:q.nom,listo:q.listo}));
    if(M.fase!=='sala'&&M.fase!=='juego')abreSala();else pinta();return;}
  if(m.t==='abresala'){try{A().toMenu();}catch(e){}abreSala();return;}
  if(m.t==='lleno'){M.on=false;info('mmpInfo',m.por||'La sala está llena.');return;}
  if(m.t==='va'){arranca(m.w|0,m.c|0,m.jug);return;}
  const j=M.jug[m.from];if(!j)return;
  if(m.t==='g'){j.g={x:+m.x,y:+m.y,a:+m.a,vx:+m.vx||0,st:m.st,t:performance.now()};}
  else if(m.t==='fin'){M.res[m.from]={t:+m.tm,f:m.f|0,d:m.d|0,k:m.k|0};revisa();}
  else if(m.t==='fuera')seVa(m.asiento);
}
function anfRecibe(conn,m){
  const i=M.jug.findIndex(j=>j.conn===conn);if(i<0||!m||!m.t)return;m.from=i;
  if(m.t==='elige'){const j=M.jug[i];j.nom=String(m.nom||'').slice(0,12)||'Piloto';j.listo=!!m.listo;difunde();return;}
  if(m.t==='revancha'){if(M.fase==='fin'||M.fase==='juego')volverSala();return;}
  reenvia(m,conn);recibe(m);
}
function seVa(i){const j=M.jug[i];if(!j||j.fuera)return;j.fuera=true;
  if(M.fase==='sala'&&M.host){M.jug.splice(i,1);difunde();return;}
  if(M.host)reenvia({t:'fuera',asiento:i,from:0},j.conn);
  if(M.fase==='juego')revisa();}
function creaSala(intento){
  info('mmpInfo','Conectando…');
  cargaPeer(ok=>{
    if(!ok){info('mmpInfo','No se ha podido cargar el modo online. Revisa la conexión.');return;}
    const L='ABCDEFGHJKLMNPQRSTUVWXYZ',code=[0,1,2,3].map(()=>L[Math.floor(Math.random()*L.length)]).join('');
    let peer;try{peer=new Peer(PREFIX()+code,window.MOTOR_PEER_OPTS||{});}catch(e){info('mmpInfo','Error al crear la sala.');return;}
    M.peer=peer;
    peer.on('open',()=>{M.on=true;M.host=true;M.me=0;M.code=code;M.w=A().selLevel|0;M.jug=[{nom:miNom||'Piloto',listo:true,conn:null}];abreSala();elige();});
    peer.on('error',e=>{if(e&&e.type==='unavailable-id'&&(intento||0)<4){try{peer.destroy();}catch(_){}creaSala((intento||0)+1);}else if(M.fase==='off')info('mmpInfo','Error de conexión ('+(e&&e.type||'?')+'). Inténtalo de nuevo.');});
    peer.on('connection',conn=>{
      conn.on('open',()=>{if(M.fase!=='sala'||M.jug.length>=MAXP){try{conn.send({t:'lleno',por:M.fase!=='sala'?'La carrera ya ha empezado. Espera a la siguiente.':'La sala está llena (máximo '+MAXP+').'});}catch(e){}setTimeout(()=>{try{conn.close();}catch(e){}},400);return;}
        M.jug.push({nom:'Piloto '+(M.jug.length+1),listo:false,conn});difunde();});
      conn.on('data',m=>anfRecibe(conn,m));
      conn.on('close',()=>{const i=M.jug.findIndex(j=>j.conn===conn);if(i>=0)seVa(i);});
    });
  });
}
function unirse(){
  const code=($q('mmpCodIn').value||'').trim().toUpperCase();if(code.length!==4){info('mmpInfo','Escribe el código de 4 letras.');return;}
  info('mmpInfo','Conectando…');
  cargaPeer(ok=>{
    if(!ok){info('mmpInfo','No se ha podido cargar el modo online. Revisa la conexión.');return;}
    let peer;try{peer=new Peer(window.MOTOR_PEER_OPTS||{});}catch(e){info('mmpInfo','Error de conexión.');return;}
    M.peer=peer;let hecho=false;const falla=t=>{if(hecho)return;hecho=true;info('mmpInfo',t);try{peer.destroy();}catch(_){}};
    const to=setTimeout(()=>falla('No se encuentra la sala. Revisa el código (o puede que tu red bloquee la conexión).'),22000);
    peer.on('error',e=>{if(!M.on)falla(e&&e.type==='peer-unavailable'?'No existe esa sala. Revisa el código.':'Error de conexión ('+(e&&e.type||'?')+').');});
    peer.on('open',()=>{const conn=peer.connect(PREFIX()+code,{reliable:true});M.conn=conn;M.code=code;
      conn.on('data',recibe);conn.on('close',pierdeAnf);
      conn.on('open',()=>{clearTimeout(to);hecho=true;M.on=true;M.host=false;info('mmpInfo','¡Conectado! Entrando en la sala…');setTimeout(()=>{M.listo=false;elige();},300);});});
  });
}
function pierdeAnf(){if(!M.on)return;const jugando=M.fase==='juego';M.on=false;M.fase='off';clearInterval(M.envT);hud.hidden=true;paraFantasmas();
  if(jugando)return;abre('mmpIni');info('mmpInfo','Se ha cerrado la sala. Crea una nueva o únete con otro código.');}
function sal(){M.on=false;M.host=false;M.fase='off';clearInterval(M.envT);hud.hidden=true;paraFantasmas();
  try{if(M.conn)M.conn.close();}catch(e){}M.jug.forEach(j=>{try{if(j.conn)j.conn.close();}catch(e){}});try{if(M.peer)M.peer.destroy();}catch(e){}
  M.conn=null;M.peer=null;M.jug=[];cierra();}

$q('mmpCrea').onclick=()=>creaSala(0);
$q('mmpUne').onclick=unirse;
['mmpCodIn','mmpNom'].forEach(id=>{const el=$q(id);el.addEventListener('keydown',e=>{e.stopPropagation();if(e.key==='Enter'&&id==='mmpCodIn')unirse();});el.addEventListener('keyup',e=>e.stopPropagation());});
$q('mmpNom').addEventListener('change',()=>{if(M.fase==='sala')elige();});
$q('mmpListo').onclick=()=>{M.listo=!M.listo;elige();pinta();};
$q('mmpEmp').onclick=empieza;
$q('mmpRev').onclick=volver;
$q('mmpSal1').onclick=()=>sal();
$q('mmpSal2').onclick=()=>sal();
$q('mmpSal3').onclick=()=>{sal();try{A().toMenu();}catch(e){}};
conInvita(()=>{SalaInvita.monta($q('mmpCod'),()=>M.code,NOMBRE(),'es');SalaInvita.alEntrar(c=>{abre('mmpIni');$q('mmpCodIn').value=c;unirse();},1800);});
window.__motorMP={fin,fuera,activo:()=>M.fase==='juego',estado:M};
})();
