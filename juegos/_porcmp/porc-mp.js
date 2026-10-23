/* © 2026 Enric Alicarte · Alica Games Studio · Salón Recreativo. Todos los derechos reservados. Prohibida la copia, redistribución o publicación de este código en otros sitios sin permiso escrito. */
/* Aventura Porc · multijugador de 2 a 4 móviles (WebRTC / PeerJS)
   Todos montan en la MISMA atracción y nivel, con los MISMOS obstáculos (la vía se genera con la misma semilla),
   salen a la vez y ven en directo los puntos y las vidas de los demás. Gana quien más puntos hace.
   El juego expone window.__porc y llama a window.__porcMP.fin() al acabar (meta o sin vidas). */
(function(){
'use strict';
const __invSrc=(document.currentScript&&document.currentScript.src)||'';function conInvita(cb){if(window.SalaInvita)return cb();const s=document.createElement('script');s.src=new URL('../_sala/invita.js',__invSrc||location.href).href;s.onload=cb;document.head.appendChild(s);}
const A=()=>window.__porc;
const MAXP=4,PREFIX='aventuraporc-';
const $p=id=>document.getElementById(id);
const esc=t=>String(t==null?'':t).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const M={on:false,host:false,me:0,peer:null,conn:null,code:'',fase:'off',jug:[],listo:false,ri:0,L:1,res:{},envT:null,seed:0};
let miNom='';try{miNom=(localStorage.getItem('aventuraporc-nom')||'').slice(0,12);}catch(e){}

const css=document.createElement('style');css.textContent=`
#pmpBtn{margin-top:2px}
#pmp{z-index:40;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 30%,rgba(120,40,100,.92),rgba(40,10,36,.97))}
#pmp .sheet{max-height:100%;overflow-y:auto;gap:10px}
#pmp p{margin:0;color:var(--cream,#fff);opacity:.9;font-size:15px;line-height:1.35}
#pmp input{font:700 20px var(--body,system-ui),sans-serif;color:var(--cream,#fff);background:var(--panel,rgba(255,255,255,.08));border:2px solid var(--line,rgba(255,255,255,.3));border-radius:14px;padding:10px 14px;text-align:center;max-width:260px;width:100%;outline:none;user-select:text;-webkit-user-select:text}
#pmp input:disabled{opacity:.55}
#pmpCodIn{text-transform:uppercase;letter-spacing:.2em;width:8ch!important}
#pmp .cod{font-family:var(--display,inherit);font-size:clamp(44px,13vw,64px);letter-spacing:.18em;color:var(--sun,#ffd23f);line-height:1}
#pmp .jl{display:flex;flex-direction:column;gap:6px}
#pmp .jl div{display:flex;align-items:center;gap:10px;background:var(--panel,rgba(255,255,255,.08));border:2px solid var(--line,rgba(255,255,255,.25));border-radius:14px;padding:7px 12px}
#pmp .jl div.yo{border-color:var(--sun,#ffd23f)}
#pmp .jl b{flex:1;font-size:16px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#pmp .jl em{font-style:normal;font-size:12.5px;opacity:.8;white-space:nowrap}
#pmp .jl div.vacio{justify-content:center;border-style:dashed;opacity:.75;font-size:13.5px}
#pmp .ops{display:flex;flex-wrap:wrap;gap:6px}
#pmp .ops button{font:700 14px var(--body,system-ui),sans-serif;color:var(--cream,#fff);background:var(--panel,rgba(255,255,255,.08));border:2px solid var(--line,rgba(255,255,255,.25));border-radius:12px;padding:8px 12px;cursor:pointer}
#pmp .ops button.sel{background:var(--sun,#ffd23f);border-color:var(--sun,#ffd23f);color:#2a1b00}
#pmp .ops.solo button{pointer-events:none}
#pmp .btn:disabled{opacity:.5}
#pmp table{width:100%;border-collapse:collapse;font-size:15px}
#pmp td,#pmp th{padding:6px 4px;border-bottom:1px solid rgba(255,255,255,.15);text-align:center}
#pmp th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;opacity:.75}
#pmp tr.yo td{color:var(--sun,#ffd23f);font-weight:800}
#pmpHud{position:fixed;left:10px;top:calc(168px + env(safe-area-inset-top,0px));z-index:30;display:flex;flex-direction:column;gap:4px;pointer-events:none;font:800 13px/1 var(--body,system-ui),sans-serif;color:#fff}
#pmpHud[hidden]{display:none}
#pmpHud div{display:flex;gap:7px;align-items:center;background:rgba(60,16,52,.72);border:1.5px solid rgba(255,255,255,.25);border-radius:999px;padding:5px 10px;min-width:128px}
#pmpHud div.yo{border-color:#ffd23f}
#pmpHud div.fuera{opacity:.45;text-decoration:line-through}
#pmpHud i{font-style:normal;width:14px;text-align:center;color:#ffd23f}
#pmpHud b{flex:1;max-width:80px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#pmpHud span{font-variant-numeric:tabular-nums}
#pmpHud small{font-size:11px;opacity:.85}
`;document.head.appendChild(css);
const ov=document.createElement('div');ov.className='overlay';ov.id='pmp';ov.hidden=true;ov.innerHTML=`
<div class="sheet" id="pmpIni"><div class="eyebrow">Multijugador</div><h2>Carrera de cerditos</h2>
  <p>De 2 a 4 amigos, cada uno en su móvil: la misma atracción, los mismos obstáculos y salida a la vez. Gana quien más puntos hace. Vale con wifi distintos o datos móviles.</p>
  <div class="row"><button class="btn main" id="pmpCrea">Crear sala</button></div>
  <div class="row"><input id="pmpCodIn" maxlength="4" placeholder="CÓDIGO" autocomplete="off" autocapitalize="characters" spellcheck="false"><button class="btn" id="pmpUne">Unirme</button></div>
  <p id="pmpInfo" style="min-height:20px"></p><div class="row"><button class="btn" id="pmpSal1">Volver</button></div></div>
<div class="sheet" id="pmpSala" hidden><div class="eyebrow">Código de la sala</div><div class="cod" id="pmpCod">----</div>
  <div class="jl" id="pmpJug"></div>
  <div class="eyebrow">Tu nombre</div><input id="pmpNom" maxlength="12" autocomplete="off" spellcheck="false" placeholder="Nombre">
  <div class="eyebrow">Atracción</div><div class="ops" id="pmpRides"></div>
  <div class="eyebrow">Nivel</div><div class="ops" id="pmpLv"></div>
  <p id="pmpInfoS"></p><div class="row"><button class="btn main" id="pmpListo">¡Listo!</button><button class="btn main" id="pmpEmp">Empezar</button><button class="btn" id="pmpSal2">Salir</button></div></div>
<div class="sheet" id="pmpRes" hidden><div class="eyebrow" id="pmpResE">Carrera terminada</div><h2 id="pmpResT">Resultado</h2>
  <table><thead><tr><th></th><th style="text-align:left">Jugador</th><th>Puntos</th><th>Distancia</th><th>Meta</th></tr></thead><tbody id="pmpResL"></tbody></table>
  <div class="row"><button class="btn main" id="pmpRev">Revancha</button><button class="btn" id="pmpSal3">Salir del multijugador</button></div></div>`;
(document.querySelector('.overlay')?document.querySelector('.overlay').parentNode:document.body).appendChild(ov);
const hud=document.createElement('div');hud.id='pmpHud';hud.hidden=true;document.body.appendChild(hud);
function abre(k){ov.hidden=false;['pmpIni','pmpSala','pmpRes'].forEach(id=>$p(id).hidden=id!==k);}
function cierra(){ov.hidden=true;}
function info(id,t){$p(id).textContent=t;}
(function(){const pb=$p('playBtn');if(!pb)return;const b=document.createElement('button');b.className='btn';b.id='pmpBtn';b.textContent='👥 Multijugador · 2 a 4 móviles';
  pb.parentNode.insertBefore(b,pb.nextSibling);b.addEventListener('click',()=>{info('pmpInfo','');abre('pmpIni');});})();

/* ---------- red ---------- */
function envia(o){o.from=M.me;
  if(M.host)M.jug.forEach(j=>{if(j.conn&&j.conn.open){try{j.conn.send(o);}catch(e){}}});
  else{try{if(M.conn&&M.conn.open)M.conn.send(o);}catch(e){}}}
function reenvia(m,menos){M.jug.forEach(j=>{if(j.conn&&j.conn!==menos&&j.conn.open){try{j.conn.send(m);}catch(e){}}});}
function cargaPeer(cb){if(window.Peer)return cb(true);
  const urls=['https://cdn.jsdelivr.net/npm/peerjs@1.5.4/dist/peerjs.min.js','https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js','https://cdnjs.cloudflare.com/ajax/libs/peerjs/1.5.4/peerjs.min.js'];
  let i=0;(function sig(){if(i>=urls.length)return cb(false);const s=document.createElement('script');s.src=urls[i++];s.onload=()=>cb(!!window.Peer);s.onerror=sig;document.head.appendChild(s);})();}

/* ---------- sala ---------- */
const datosSala=()=>M.jug.map(j=>({nom:j.nom,listo:!!j.listo}));
function difunde(){M.jug.forEach((j,i)=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'sala',tu:i,cod:M.code,ri:M.ri,L:M.L,jug:datosSala()});}catch(e){}}});pinta();}
function abreSala(){M.fase='sala';M.listo=false;M.res={};hud.hidden=true;clearInterval(M.envT);if(!$p('pmpNom').value)$p('pmpNom').value=miNom||'Jugador';abre('pmpSala');pinta();}
function elige(){const nom=($p('pmpNom').value||'').trim().slice(0,12)||'Jugador';miNom=nom;try{localStorage.setItem('aventuraporc-nom',nom);}catch(e){}
  if(M.host){M.jug[0].nom=nom;difunde();}else envia({t:'elige',nom,listo:M.listo});}
function pinta(){
  if(M.fase!=='sala')return;const a=A();
  $p('pmpCod').textContent=M.code||'----';
  $p('pmpJug').innerHTML=M.jug.map((j,i)=>'<div class="'+(i===M.me?'yo':'')+'"><span>🐷</span><b>'+esc(j.nom)+(i===M.me?' (tú)':'')+'</b><em>'+(i===0?'Anfitrión':j.listo?'✅ ¡Listo!':'Eligiendo…')+'</em></div>').join('')
    +(M.jug.length<MAXP?'<div class="vacio">'+(M.jug.length<2?'Esperando jugadores… comparte el código':'Puede entrar alguien más (máx. '+MAXP+')')+'</div>':'');
  $p('pmpNom').disabled=M.listo;
  const rd=$p('pmpRides'),lv=$p('pmpLv');rd.classList.toggle('solo',!M.host);lv.classList.toggle('solo',!M.host);
  const rides=a.RIDES.map((r,i)=>({r,i}));
  rd.innerHTML=(M.host?rides:rides.filter(o=>o.i===M.ri)).map(o=>'<button data-r="'+o.i+'" class="'+(o.i===M.ri?'sel':'')+'">'+esc(o.r.name)+'</button>').join('');
  lv.innerHTML=(M.host?[1,2,3,4,5]:[M.L]).map(n=>'<button data-l="'+n+'" class="'+(n===M.L?'sel':'')+'">'+n+'</button>').join('');
  if(M.host){rd.querySelectorAll('button').forEach(b=>b.onclick=()=>{M.ri=+b.dataset.r;difunde();});lv.querySelectorAll('button').forEach(b=>b.onclick=()=>{M.L=+b.dataset.l;difunde();});}
  const bl=$p('pmpListo'),be=$p('pmpEmp');
  if(M.host){bl.hidden=true;be.hidden=false;const otros=M.jug.slice(1),todos=otros.length>=1&&otros.every(j=>j.listo);be.disabled=!todos;
    be.textContent=otros.length<1?'Esperando jugadores…':todos?'¡Empezar! ('+M.jug.length+')':'Esperando a que estén listos…';
    info('pmpInfoS','Tú eliges la atracción y el nivel. Cada jugador pone su nombre y pulsa «¡Listo!».');}
  else{be.hidden=true;bl.hidden=false;bl.textContent=M.listo?'✓ ¡Listo! (cambiar)':'¡Listo!';info('pmpInfoS',M.listo?'Esperando a que el anfitrión empiece…':'Pon tu nombre y pulsa «¡Listo!».');}
}
/* ---------- carrera ---------- */
function empieza(){if(!M.host||$p('pmpEmp').disabled)return;elige();const jug=M.jug.map(j=>({nom:j.nom})),seed=(Math.random()*4294967295)>>>0||1;
  M.jug.forEach((j,i)=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'sala',tu:i,cod:M.code,ri:M.ri,L:M.L,jug:datosSala()});j.conn.send({t:'va',ri:M.ri,L:M.L,seed,jug});}catch(e){}}});
  arranca(M.ri,M.L,seed,jug);}
function arranca(ri,L,seed,jug){
  jug.forEach((q,i)=>{const j=M.jug[i]||(M.jug[i]={});j.nom=q.nom;j.fuera=false;j.p=0;j.d=0;j.v=3;});M.jug.length=jug.length;
  M.ri=ri;M.L=L;M.seed=seed;M.res={};M.fase='juego';cierra();
  window.__porcSeed=seed;try{A().startGame(ri,L);}finally{window.__porcSeed=0;}
  hud.hidden=false;clearInterval(M.envT);M.envT=setInterval(tic,300);pintaHud();
}
function tic(){
  if(M.fase!=='juego')return;const G=A().G,yo=M.jug[M.me];
  if(!M.res[M.me]){yo.p=Math.round(G.score+G.coins*10);yo.d=Math.max(0,Math.round(G.s-G.startS));yo.v=G.lives;envia({t:'p',p:yo.p,d:yo.d,v:yo.v});}
  pintaHud();
}
function fin(r){
  if(M.fase!=='juego'||M.res[M.me])return;const G=A().G,yo=M.jug[M.me];
  const x={p:r.t|0,d:Math.max(0,Math.round(G.s-G.startS)),c:r.c?1:0};M.res[M.me]=x;yo.p=x.p;yo.d=x.d;
  envia(Object.assign({t:'fin'},x));revisa();
}
function revisa(){
  const act=M.jug.map((j,i)=>i).filter(i=>!M.jug[i].fuera);pintaHud();
  if(!M.res[M.me])return;
  if(act.every(i=>M.res[i])){M.fase='fin';clearInterval(M.envT);hud.hidden=true;setTimeout(resultado,1800);}
}
function pintaHud(){
  if(M.fase!=='juego'){hud.hidden=true;return;}hud.hidden=false;
  const ord=M.jug.map((j,i)=>({j,i,p:M.res[i]?M.res[i].p:j.p|0})).sort((a,b)=>b.p-a.p);
  hud.innerHTML=ord.map((o,k)=>'<div class="'+(o.i===M.me?'yo':'')+(o.j.fuera?' fuera':'')+'"><i>'+(M.res[o.i]?(M.res[o.i].c?'🏁':'✕'):(k+1))+'</i><b>'+esc(o.i===M.me?'Tú':o.j.nom)+'</b><span>'+o.p.toLocaleString('es')+'</span><small>'+(M.res[o.i]?'':'❤'.repeat(Math.max(0,o.j.v|0)))+'</small></div>').join('');
}
function resultado(){
  const ord=M.jug.map((j,i)=>({j,i,r:M.res[i]||{p:j.p|0,d:j.d|0,c:0}})).sort((a,b)=>b.r.p-a.r.p);
  const pos=o=>ord.filter(x=>x.r.p>o.r.p).length,med=['🥇','🥈','🥉','4º'],yo=ord.find(o=>o.i===M.me),top=ord.filter(o=>pos(o)===0);
  $p('pmpResT').textContent=top.length>1&&top.some(o=>o.i===M.me)?'¡Empate!':pos(yo)===0?'🏆 ¡Has ganado!':'¡Gana '+top[0].j.nom+'!';
  $p('pmpResE').textContent=A().RIDES[M.ri].name+' · Nivel '+M.L;
  $p('pmpResL').innerHTML=ord.map(o=>'<tr class="'+(o.i===M.me?'yo':'')+'"><td>'+med[pos(o)]+'</td><td style="text-align:left">'+esc(o.i===M.me?'Tú':o.j.nom)+(o.j.fuera?' <small>(se fue)</small>':'')+'</td><td>'+o.r.p.toLocaleString('es')+'</td><td>'+(o.r.d|0).toLocaleString('es')+' m</td><td>'+(o.r.c?'🏁':'—')+'</td></tr>').join('');
  $p('pmpRev').textContent='Revancha';
  ['end','clear'].forEach(id=>{const e=$p(id);if(e)e.hidden=true;});abre('pmpRes');
}
function volver(){if(M.host)volverSala();else{envia({t:'revancha'});$p('pmpRev').textContent='Volviendo…';}}
function volverSala(){
  M.jug=M.jug.filter((j,i)=>i===0||(!j.fuera&&j.conn&&j.conn.open));M.jug.forEach(j=>j.listo=false);M.me=0;
  M.jug.forEach(j=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'abresala'});}catch(e){}}});
  try{A().toMenu();}catch(e){}abreSala();difunde();
}
// en multijugador no se puede reiniciar a mitad; salir del juego = salir del multijugador
function intercepta(id,fn){const b=$p(id);if(b)b.addEventListener('click',e=>{if(M.fase==='juego'||M.fase==='fin'){e.stopImmediatePropagation();e.preventDefault();fn();}},true);}
intercepta('restartBtn',()=>{});
['quitBtn','menuBtn','clearMenuBtn'].forEach(id=>intercepta(id,()=>{sal();try{A().toMenu();}catch(e){}}));
['againBtn','nextBtn','nextRideBtn'].forEach(id=>intercepta(id,()=>{if(M.fase==='fin')resultado();}));

/* ---------- mensajes ---------- */
function recibe(m){
  if(!m||!m.t)return;
  if(m.t==='sala'){M.me=m.tu;M.code=m.cod||M.code;M.ri=m.ri|0;M.L=m.L|0||1;const ant=M.jug;M.jug=m.jug.map((q,i)=>Object.assign(ant[i]||{},{nom:q.nom,listo:q.listo}));
    if(M.fase!=='sala'&&M.fase!=='juego')abreSala();else pinta();return;}
  if(m.t==='abresala'){try{A().toMenu();}catch(e){}abreSala();return;}
  if(m.t==='lleno'){M.on=false;info('pmpInfo',m.por||'La sala está llena.');return;}
  if(m.t==='va'){arranca(m.ri|0,m.L|0||1,m.seed>>>0,m.jug);return;}
  const j=M.jug[m.from];if(!j)return;
  if(m.t==='p'){j.p=m.p|0;j.d=m.d|0;j.v=m.v|0;pintaHud();}
  else if(m.t==='fin'){M.res[m.from]={p:m.p|0,d:m.d|0,c:m.c|0};j.p=m.p|0;revisa();}
  else if(m.t==='fuera')seVa(m.asiento);
}
function anfRecibe(conn,m){
  const i=M.jug.findIndex(j=>j.conn===conn);if(i<0||!m||!m.t)return;m.from=i;
  if(m.t==='elige'){const j=M.jug[i];j.nom=String(m.nom||'').slice(0,12)||'Jugador';j.listo=!!m.listo;difunde();return;}
  if(m.t==='revancha'){if(M.fase==='fin'||M.fase==='juego')volverSala();return;}
  reenvia(m,conn);recibe(m);
}
function seVa(i){const j=M.jug[i];if(!j||j.fuera)return;j.fuera=true;
  if(M.fase==='sala'&&M.host){M.jug.splice(i,1);difunde();return;}
  if(M.host)reenvia({t:'fuera',asiento:i,from:0},j.conn);
  if(M.fase==='juego')revisa();}
function creaSala(intento){
  info('pmpInfo','Conectando…');
  cargaPeer(ok=>{
    if(!ok){info('pmpInfo','No se ha podido cargar el modo online. Revisa la conexión.');return;}
    const L='ABCDEFGHJKLMNPQRSTUVWXYZ',code=[0,1,2,3].map(()=>L[Math.floor(Math.random()*L.length)]).join('');
    let peer;try{peer=new Peer(PREFIX+code,window.PORC_PEER_OPTS||{});}catch(e){info('pmpInfo','Error al crear la sala.');return;}
    M.peer=peer;
    peer.on('open',()=>{M.on=true;M.host=true;M.me=0;M.code=code;M.jug=[{nom:miNom||'Jugador',listo:true,conn:null}];abreSala();elige();});
    peer.on('error',e=>{if(e&&e.type==='unavailable-id'&&(intento||0)<4){try{peer.destroy();}catch(_){}creaSala((intento||0)+1);}else if(M.fase==='off')info('pmpInfo','Error de conexión ('+(e&&e.type||'?')+'). Inténtalo de nuevo.');});
    peer.on('connection',conn=>{
      conn.on('open',()=>{if(M.fase!=='sala'||M.jug.length>=MAXP){try{conn.send({t:'lleno',por:M.fase!=='sala'?'La carrera ya ha empezado. Espera a la siguiente.':'La sala está llena (máximo '+MAXP+').'});}catch(e){}setTimeout(()=>{try{conn.close();}catch(e){}},400);return;}
        M.jug.push({nom:'Jugador '+(M.jug.length+1),listo:false,conn});difunde();});
      conn.on('data',m=>anfRecibe(conn,m));
      conn.on('close',()=>{const i=M.jug.findIndex(j=>j.conn===conn);if(i>=0)seVa(i);});
    });
  });
}
function unirse(){
  const code=($p('pmpCodIn').value||'').trim().toUpperCase();if(code.length!==4){info('pmpInfo','Escribe el código de 4 letras.');return;}
  info('pmpInfo','Conectando…');
  cargaPeer(ok=>{
    if(!ok){info('pmpInfo','No se ha podido cargar el modo online. Revisa la conexión.');return;}
    let peer;try{peer=new Peer(window.PORC_PEER_OPTS||{});}catch(e){info('pmpInfo','Error de conexión.');return;}
    M.peer=peer;let hecho=false;const falla=t=>{if(hecho)return;hecho=true;info('pmpInfo',t);try{peer.destroy();}catch(_){}};
    const to=setTimeout(()=>falla('No se encuentra la sala. Revisa el código (o puede que tu red bloquee la conexión).'),22000);
    peer.on('error',e=>{if(!M.on)falla(e&&e.type==='peer-unavailable'?'No existe esa sala. Revisa el código.':'Error de conexión ('+(e&&e.type||'?')+').');});
    peer.on('open',()=>{const conn=peer.connect(PREFIX+code,{reliable:true});M.conn=conn;M.code=code;
      conn.on('data',recibe);conn.on('close',pierdeAnf);
      conn.on('open',()=>{clearTimeout(to);hecho=true;M.on=true;M.host=false;info('pmpInfo','¡Conectado! Entrando en la sala…');setTimeout(()=>{M.listo=false;elige();},300);});});
  });
}
function pierdeAnf(){if(!M.on)return;const jugando=M.fase==='juego';M.on=false;M.fase='off';clearInterval(M.envT);hud.hidden=true;
  if(jugando)return;abre('pmpIni');info('pmpInfo','Se ha cerrado la sala. Crea una nueva o únete con otro código.');}
function sal(){M.on=false;M.host=false;M.fase='off';clearInterval(M.envT);hud.hidden=true;
  try{if(M.conn)M.conn.close();}catch(e){}M.jug.forEach(j=>{try{if(j.conn)j.conn.close();}catch(e){}});try{if(M.peer)M.peer.destroy();}catch(e){}
  M.conn=null;M.peer=null;M.jug=[];cierra();}

$p('pmpCrea').onclick=()=>creaSala(0);
$p('pmpUne').onclick=unirse;
['pmpCodIn','pmpNom'].forEach(id=>$p(id).addEventListener('keydown',e=>{e.stopPropagation();if(e.key==='Enter'&&id==='pmpCodIn')unirse();}));
$p('pmpNom').addEventListener('change',()=>{if(M.fase==='sala')elige();});
$p('pmpListo').onclick=()=>{M.listo=!M.listo;elige();pinta();};
$p('pmpEmp').onclick=empieza;
$p('pmpRev').onclick=volver;
$p('pmpSal1').onclick=()=>sal();
$p('pmpSal2').onclick=()=>sal();
$p('pmpSal3').onclick=()=>{sal();try{A().toMenu();}catch(e){}};
conInvita(()=>{SalaInvita.monta($p('pmpCod'),()=>M.code,'Aventura Porc','es');SalaInvita.alEntrar(c=>{abre('pmpIni');$p('pmpCodIn').value=c;unirse();},2500);});
window.__porcMP={fin,activo:()=>M.fase==='juego',estado:M};
})();
