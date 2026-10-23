/* © 2026 Enric Alicarte · Alica Games Studio · Salón Recreativo. Todos los derechos reservados. Prohibida la copia, redistribución o publicación de este código en otros sitios sin permiso escrito. */
/* Duelo de guitarras · multijugador de 2 a 4 móviles (WebRTC / PeerJS)
   Se añade al final de Martín, Supernova Guitar y Cosmic Guitar. Usa las funciones del juego
   (SLOTS, slotSong, startSong, endSession, show, loadMp3, DEC, S, diff…), que comparten el ámbito global.
   Sala: cada jugador pone su nombre y pulsa «¡Listo!»; el anfitrión elige canción y dificultad y empieza.
   Todos tocan la misma canción a la vez, cada uno en su móvil, con el marcador de los rivales en directo. */
(function(){
'use strict';
const __invSrc=(document.currentScript&&document.currentScript.src)||'';function conInvita(cb){if(window.SalaInvita)return cb();const s=document.createElement('script');s.src=new URL('../_sala/invita.js',__invSrc||location.href).href;s.onload=cb;document.head.appendChild(s);}
const G=window.__guitar||{};const MAXP=4,GAME=(location.pathname.match(/juegos\/([^/]+)\//)||[,'guitar'])[1],PREFIX='guitarduel-'+GAME.replace(/[^a-z]/g,'')+'-';
const $d=id=>document.getElementById(id);
const esc=t=>String(t==null?'':t).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const D={on:false,host:false,me:0,peer:null,conn:null,code:'',fase:'off',jug:[],listo:false,song:null,dif:'normal',res:{},envT:0,vigila:null,tiempo:null};
let miNom='';try{miNom=(localStorage.getItem('guitarduel-nom')||'').slice(0,12);}catch(e){}
const DIFS=[['facil','Fácil'],['normal','Normal'],['expert','Experto']].filter(d=>!G.DIFF||G.DIFF[d[0]]);

/* ---------- estilos ---------- */
const css=document.createElement('style');css.textContent=`
#dBtn{display:block;width:100%;margin:12px 0 4px;padding:12px 16px;border-radius:16px;border:2px solid rgba(255,255,255,.55);background:linear-gradient(180deg,#ff5fa8,#c02a7a);color:#fff;font:800 17px/1.15 system-ui,-apple-system,'Segoe UI',sans-serif;letter-spacing:.02em;cursor:pointer;box-shadow:0 5px 0 rgba(0,0,0,.35),0 0 22px rgba(255,95,168,.45)}
#dBtn small{display:block;font-weight:600;font-size:12px;opacity:.9;margin-top:2px}
#dBtn:active{transform:translateY(3px)}
#duel{position:fixed;inset:0;z-index:60;display:flex;align-items:center;justify-content:center;padding:max(14px,env(safe-area-inset-top)) 12px max(14px,env(safe-area-inset-bottom));background:rgba(8,6,24,.72);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);overflow-y:auto;font-family:system-ui,-apple-system,'Segoe UI',sans-serif;color:#fff}
#duel[hidden]{display:none}
#duel .dc{width:min(460px,100%);margin:auto;background:linear-gradient(180deg,rgba(46,30,96,.96),rgba(18,12,46,.98));border:1.5px solid rgba(255,140,210,.45);border-radius:24px;box-shadow:0 0 40px rgba(255,90,170,.25),0 20px 40px rgba(0,0,0,.5);padding:20px 18px;text-align:center}
#duel h2{margin:0 0 4px;font-size:26px;font-weight:900;letter-spacing:.02em}
#duel p{margin:8px 0 12px;color:#e3dcff;font-size:15px;line-height:1.35}
#duel .et{font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:800;color:#ffb6dd;margin:14px 0 6px}
#duel button{font:800 16px/1.1 system-ui,-apple-system,'Segoe UI',sans-serif;color:#fff;border:2px solid rgba(255,255,255,.55);border-radius:999px;padding:11px 22px;margin:4px;cursor:pointer;background:linear-gradient(180deg,#5be37a,#26a94a);box-shadow:0 5px 0 #157a33,0 0 18px rgba(80,230,120,.4);touch-action:manipulation}
#duel button:active{transform:translateY(3px)}
#duel button.b2{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.35);box-shadow:none;font-size:14px;padding:9px 18px}
#duel button:disabled{filter:grayscale(.8);opacity:.6;cursor:default}
#duel input{font:800 20px system-ui,sans-serif;color:#fff;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,140,210,.5);border-radius:14px;padding:9px 12px;text-align:center;width:100%;max-width:240px;outline:none;user-select:text;-webkit-user-select:text}
#duel input:disabled{opacity:.6}
#dCodIn{text-transform:uppercase;letter-spacing:.2em;width:8ch!important}
#duel .fila{display:flex;gap:6px;justify-content:center;align-items:center;flex-wrap:wrap}
#duel .cod{font-size:clamp(40px,13vw,58px);font-weight:900;letter-spacing:.2em;color:#ffd23f;text-shadow:0 0 20px rgba(255,210,63,.6);line-height:1.05}
#duel .jl{display:flex;flex-direction:column;gap:6px;margin:8px 0;text-align:left}
#duel .jl div{display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.18);border-radius:14px;padding:7px 12px}
#duel .jl div.yo{border-color:#ffd23f}
#duel .jl b{flex:1;font-size:16px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#duel .jl em{font-style:normal;font-weight:700;font-size:12.5px;color:#ffb6dd;white-space:nowrap}
#duel .jl div.vacio{justify-content:center;border-style:dashed;color:#cdbdf0;font-size:13.5px}
#duel .canc{display:flex;flex-direction:column;gap:5px;max-height:34vh;overflow-y:auto;text-align:left;padding:2px}
#duel .canc button{display:flex;justify-content:space-between;gap:8px;text-align:left;margin:0;border-radius:12px;padding:9px 12px;font-size:14.5px;background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.18);box-shadow:none}
#duel .canc button small{font-weight:600;opacity:.75;white-space:nowrap}
#duel .canc button.sel{background:linear-gradient(180deg,#ff5fa8,#c02a7a);border-color:#fff}
#duel .canc.solo button{pointer-events:none}
#duel .difs{display:flex;gap:6px;justify-content:center}
#duel .difs button{margin:0;font-size:14px;padding:8px 14px;background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.25);box-shadow:none}
#duel .difs button.sel{background:linear-gradient(180deg,#ffd23f,#e09a00);color:#2a1700;border-color:#fff}
#duel .difs.solo button{pointer-events:none}
#duel table{width:100%;border-collapse:collapse;margin:10px 0;font-size:15px}
#duel td,#duel th{padding:6px 4px;border-bottom:1px solid rgba(255,255,255,.12)}
#duel th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#ffb6dd}
#duel td:first-child{font-size:20px}
#duel tr.yo td{color:#ffd23f;font-weight:800}
#dHud{position:fixed;left:10px;top:calc(76px + env(safe-area-inset-top));z-index:30;display:flex;flex-direction:column;gap:4px;pointer-events:none;font:800 13px/1 system-ui,sans-serif;color:#fff}
#dHud[hidden]{display:none}
#dHud div{display:flex;gap:8px;align-items:center;background:rgba(10,6,30,.66);border:1.5px solid rgba(255,255,255,.22);border-radius:999px;padding:5px 10px;min-width:118px;transition:transform .3s}
#dHud div.yo{border-color:#ffd23f}
#dHud div.fuera{opacity:.45;text-decoration:line-through}
#dHud i{font-style:normal;width:14px;text-align:center;color:#ffd23f}
#dHud b{flex:1;max-width:84px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#dHud span{font-variant-numeric:tabular-nums;color:#ffd9ef}
#dCuenta{position:fixed;inset:0;z-index:61;display:flex;flex-direction:column;align-items:center;justify-content:center;pointer-events:none;font-family:system-ui,sans-serif;color:#fff;background:rgba(8,6,24,.55)}
#dCuenta[hidden]{display:none}
#dCuenta b{font-size:min(38vw,180px);font-weight:900;color:#ffd23f;text-shadow:0 0 40px rgba(255,210,63,.7);line-height:1}
#dCuenta span{font-size:18px;font-weight:800;letter-spacing:.06em}
`;document.head.appendChild(css);

/* ---------- interfaz ---------- */
const ui=document.createElement('div');ui.id='duel';ui.hidden=true;ui.innerHTML=`
<div class="dc" id="dIni"><h2>⚔️ Duelo de guitarras</h2>
  <p>De 2 a 4 jugadores, cada uno en su móvil: la misma canción a la vez y el marcador de los rivales en directo. Vale con wifi distintos o datos móviles.</p>
  <button id="dCrea">Crear sala</button><div class="et">— o únete con un código —</div>
  <div class="fila"><input id="dCodIn" maxlength="4" placeholder="CÓDIGO" autocomplete="off" autocapitalize="characters" spellcheck="false"><button id="dUne" class="b2" style="font-size:16px">Unirme</button></div>
  <p id="dInfo" style="min-height:20px;margin-bottom:4px"></p><button class="b2" id="dSalir1">Volver</button></div>
<div class="dc" id="dSala" hidden><div class="et" style="margin-top:0">Código de la sala</div><div class="cod" id="dCod">----</div>
  <div class="jl" id="dJug"></div>
  <div class="et">Tu nombre</div><input id="dNom" maxlength="12" autocomplete="off" spellcheck="false" placeholder="Nombre">
  <div class="et">Canción</div><div class="canc" id="dCanc"></div>
  <div class="et">Dificultad</div><div class="difs" id="dDif"></div>
  <p id="dInfoS"></p><button id="dListo">¡Listo!</button><button id="dEmp">Empezar</button><br><button class="b2" id="dSalir2">Salir</button></div>
<div class="dc" id="dRes" hidden><h2 id="dResT">Resultado</h2><p id="dResS"></p>
  <table><thead><tr><th></th><th style="text-align:left">Jugador</th><th>Puntos</th><th>Acierto</th><th>Racha</th></tr></thead><tbody id="dResL"></tbody></table>
  <button id="dRev">Revancha</button><br><button class="b2" id="dSalir3">Salir del duelo</button></div>`;
document.body.appendChild(ui);
const hud=document.createElement('div');hud.id='dHud';hud.hidden=true;document.body.appendChild(hud);
const cuenta=document.createElement('div');cuenta.id='dCuenta';cuenta.hidden=true;cuenta.innerHTML='<span id="dCuT">¡Preparados!</span><b id="dCuN">3</b>';document.body.appendChild(cuenta);
const tarj=k=>['dIni','dSala','dRes'].forEach(id=>$d(id).hidden=id!==k);
function abre(k){ui.hidden=false;tarj(k);}
function cierra(){ui.hidden=true;}
function info(id,t){$d(id).textContent=t;}

// botón en el menú del juego
(function(){const m=document.getElementById('menu');if(!m)return;const dif=m.querySelector('.diff');const b=document.createElement('button');b.id='dBtn';b.type='button';
  b.innerHTML='⚔️ Duelo con amigos<small>2 a 4 móviles · la misma canción a la vez</small>';
  if(dif&&dif.parentNode)dif.parentNode.insertBefore(b,dif.nextSibling);else (m.querySelector('.panel')||m).appendChild(b);
  b.addEventListener('click',()=>{try{G.initAudio();}catch(e){}abre('dIni');info('dInfo','');});})();

/* ---------- canciones ---------- */
function canciones(){
  const out=[];
  G.slots().forEach(sl=>{let sg=null;const M=G.META;try{
    if(M&&M[sl.id]){const m=M[sl.id];delete M[sl.id];sg=G.slotSong(sl);M[sl.id]=m;}else sg=G.slotSong(sl);}catch(e){}
    if(sg&&!(G.BUILTIN&&!G.BUILTIN[sl.id]))out.push(sg);});
  return out;
}
const cancion=id=>canciones().find(s=>s.id===id)||null;
function precarga(id){const s=cancion(id);if(!s||!s.mp3)return Promise.resolve();try{G.initAudio();}catch(e){}if(!G.ac)return Promise.resolve();
  if(G.DEC[s.id])return Promise.resolve();return G.loadMp3(s).then(()=>{if(D.fase==='sala'){pintaSala();elige();}}).catch(()=>{});}
const cargada=id=>{const s=cancion(id);return !s||!s.mp3||!!G.DEC[s.id];};

/* ---------- red ---------- */
function envia(o){o.from=D.me;
  if(D.host)D.jug.forEach(j=>{if(j.conn&&j.conn.open){try{j.conn.send(o);}catch(e){}}});
  else{try{if(D.conn&&D.conn.open)D.conn.send(o);}catch(e){}}}
function reenvia(m,menos){D.jug.forEach(j=>{if(j.conn&&j.conn!==menos&&j.conn.open){try{j.conn.send(m);}catch(e){}}});}
function cargaPeer(cb){if(window.Peer)return cb(true);
  const urls=['https://cdn.jsdelivr.net/npm/peerjs@1.5.4/dist/peerjs.min.js','https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js','https://cdnjs.cloudflare.com/ajax/libs/peerjs/1.5.4/peerjs.min.js'];
  let i=0;(function sig(){if(i>=urls.length)return cb(false);const s=document.createElement('script');s.src=urls[i++];s.onload=()=>cb(!!window.Peer);s.onerror=sig;document.head.appendChild(s);})();}

/* ---------- sala ---------- */
function datosSala(){return D.jug.map(j=>({nom:j.nom,listo:!!j.listo,ok:!!j.ok}));}
function difunde(){D.jug.forEach((j,i)=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'sala',tu:i,cod:D.code,song:D.song,dif:D.dif,jug:datosSala()});}catch(e){}}});pintaSala();}
function abreSala(){D.fase='sala';D.listo=false;D.res={};hud.hidden=true;clearInterval(D.vigila);clearTimeout(D.tiempo);
  if(!$d('dNom').value)$d('dNom').value=miNom||'Jugador';abre('dSala');if(D.song)precarga(D.song);pintaSala();}
function elige(){const nom=($d('dNom').value||'').trim().slice(0,12)||'Jugador';miNom=nom;try{localStorage.setItem('guitarduel-nom',nom);}catch(e){}
  const ok=cargada(D.song);
  if(D.host){const j=D.jug[0];j.nom=nom;j.ok=ok;difunde();}else envia({t:'elige',nom,listo:D.listo,ok});}
function pintaSala(){
  if(D.fase!=='sala')return;
  $d('dCod').textContent=D.code||'----';
  $d('dJug').innerHTML=D.jug.map((j,i)=>'<div class="'+(i===D.me?'yo':'')+'"><span>🎸</span><b>'+esc(j.nom)+(i===D.me?' (tú)':'')+'</b><em>'+(i===0?'Anfitrión':j.listo?(j.ok?'✅ ¡Listo!':'⏳ Cargando…'):'Eligiendo…')+'</em></div>').join('')
    +(D.jug.length<MAXP?'<div class="vacio">'+(D.jug.length<2?'Esperando jugadores… comparte el código':'Puede entrar alguien más (máx. '+MAXP+')')+'</div>':'');
  $d('dNom').disabled=D.listo;
  const cs=canciones(),cl=$d('dCanc');
  if(!D.song&&cs[0])D.song=cs[0].id;
  if(D.host){cl.classList.remove('solo');cl.innerHTML=cs.map(s=>'<button data-s="'+esc(s.id)+'" class="'+(s.id===D.song?'sel':'')+'"><span>'+esc(s.title)+'</span><small>'+esc(s.note||'')+'</small></button>').join('');
    cl.querySelectorAll('button').forEach(b=>b.onclick=()=>{D.song=b.dataset.s;precarga(D.song);elige();});
    const sel=cl.querySelector('.sel');if(sel&&!pintaSala.scrolled){pintaSala.scrolled=1;sel.scrollIntoView({block:'nearest'});}
  }else{const s=cs.find(x=>x.id===D.song);cl.classList.add('solo');cl.innerHTML=s?'<button class="sel"><span>'+esc(s.title)+'</span><small>'+esc(s.note||'')+'</small></button>':'';}
  const dd=$d('dDif');dd.classList.toggle('solo',!D.host);dd.innerHTML=DIFS.map(d=>'<button data-d="'+d[0]+'" class="'+(d[0]===D.dif?'sel':'')+'">'+d[1]+'</button>').join('');
  if(D.host)dd.querySelectorAll('button').forEach(b=>b.onclick=()=>{D.dif=b.dataset.d;difunde();});
  const bl=$d('dListo'),be=$d('dEmp');
  if(D.host){bl.hidden=true;be.hidden=false;const otros=D.jug.slice(1),todos=otros.length>=1&&otros.every(j=>j.listo&&j.ok)&&cargada(D.song);
    be.disabled=!todos;be.textContent=otros.length<1?'Esperando jugadores…':!otros.every(j=>j.listo)?'Esperando a que estén listos…':!todos?'Cargando la canción…':'¡Empezar el duelo! ('+D.jug.length+')';
    info('dInfoS','Tú eliges canción y dificultad. Cada jugador pone su nombre y pulsa «¡Listo!».');
  }else{be.hidden=true;bl.hidden=false;bl.textContent=D.listo?'✓ ¡Listo! (cambiar)':'¡Listo!';
    info('dInfoS',D.listo?(cargada(D.song)?'Esperando a que el anfitrión empiece…':'Cargando la canción…'):'Pon tu nombre y pulsa «¡Listo!».');}
}
/* ---------- partida ---------- */
function empieza(){
  if(!D.host||$d('dEmp').disabled)return;elige();
  const jug=D.jug.map(j=>({nom:j.nom}));
  D.jug.forEach((j,i)=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'sala',tu:i,cod:D.code,song:D.song,dif:D.dif,jug:datosSala()});j.conn.send({t:'va',song:D.song,dif:D.dif,jug});}catch(e){}}});
  arranca(D.song,D.dif,jug);
}
function arranca(song,dif,jug){
  jug.forEach((q,i)=>{const j=D.jug[i]||(D.jug[i]={});j.nom=q.nom;j.fuera=false;j.sc=0;});D.jug.length=jug.length;
  D.song=song;D.dif=dif;D.res={};D.fase='cuenta';cierra();
  try{G.endSession();G.show('menu');}catch(e){}
  cuenta.hidden=false;let n=3;$d('dCuN').textContent=n;$d('dCuT').textContent=(cancion(song)||{}).title||'¡Preparados!';
  const t=setInterval(()=>{n--;if(n>0)$d('dCuN').textContent=n;else{clearInterval(t);cuenta.hidden=true;toca();}},1000);
}
function toca(){
  const s=cancion(D.song);if(!s){abreSala();return;}
  try{G.setDiff(D.dif);}catch(e){}
  D.fase='juego';G.startSong(s);pintaHud();
  clearInterval(D.vigila);D.vigila=setInterval(vigila,250);
}
function vigila(){
  if(D.fase!=='juego')return;
  const yo=D.jug[D.me];
  const S=G.S;if(S&&!S.free){yo.sc=Math.floor(S.score+(S.sus||0));
    D.envT++;if(D.envT%2===0)envia({t:'sc',s:yo.sc});
    if(S.finished&&!D.res[D.me])termino(false);}
  else if(!D.res[D.me]&&!$d('menu').hidden)termino(true); // ha salido con ✕
  pintaHud();
}
function termino(aband){
  const st=G.S||null,tot=st?Math.max(1,st.total||1):1;
  const r={s:D.jug[D.me].sc|0,a:st?Math.round((st.perfect+st.good)/tot*100):0,c:st?st.maxCombo|0:0,x:aband?1:0};
  D.res[D.me]=r;envia(Object.assign({t:'fin'},r));revisaFin();
}
function revisaFin(){
  const act=D.jug.map((j,i)=>i).filter(i=>!D.jug[i].fuera);
  if(!D.res[D.me])return;
  if(act.every(i=>D.res[i])){clearInterval(D.vigila);clearTimeout(D.tiempo);D.fase='fin';hud.hidden=true;setTimeout(resultado,D.res[D.me].x?200:1600);}
  else{pintaHud();clearTimeout(D.tiempo);D.tiempo=setTimeout(()=>{if(D.fase==='juego'){act.forEach(i=>{if(!D.res[i])D.res[i]={s:D.jug[i].sc|0,a:0,c:0,x:1};});revisaFin();}},120000);}
}
function pintaHud(){
  if(D.fase!=='juego'){hud.hidden=true;return;}hud.hidden=false;
  const ord=D.jug.map((j,i)=>({j,i,s:D.res[i]?D.res[i].s:j.sc|0})).sort((a,b)=>b.s-a.s);
  hud.innerHTML=ord.map((o,k)=>'<div class="'+(o.i===D.me?'yo':'')+(o.j.fuera?' fuera':'')+'"><i>'+(D.res[o.i]?'✓':(k+1))+'</i><b>'+esc(o.i===D.me?'Tú':o.j.nom)+'</b><span>'+o.s.toLocaleString('es')+'</span></div>').join('');
}
function resultado(){
  const ord=D.jug.map((j,i)=>({j,i,r:D.res[i]||{s:j.sc|0,a:0,c:0,x:1}})).sort((a,b)=>b.r.s-a.r.s);
  const pos=o=>ord.filter(x=>x.r.s>o.r.s).length,med=['🥇','🥈','🥉','4º'],yo=ord.find(o=>o.i===D.me),top=ord.filter(o=>pos(o)===0);
  $d('dResT').textContent=top.length>1&&top.some(o=>o.i===D.me)?'¡Empate!':pos(yo)===0?'🏆 ¡Has ganado el duelo!':'¡Gana '+top[0].j.nom+'!';
  $d('dResS').textContent=((cancion(D.song)||{}).title||'')+' · '+((DIFS.find(d=>d[0]===D.dif)||[,''])[1]);
  $d('dResL').innerHTML=ord.map(o=>'<tr class="'+(o.i===D.me?'yo':'')+'"><td>'+med[pos(o)]+'</td><td style="text-align:left">'+esc(o.i===D.me?'Tú':o.j.nom)+(o.j.fuera?' <small>(se fue)</small>':o.r.x?' <small>(no acabó)</small>':'')+'</td><td>'+o.r.s.toLocaleString('es')+'</td><td>'+o.r.a+'%</td><td>'+o.r.c+'</td></tr>').join('');
  $d('dRev').textContent=D.host?'Revancha':'Revancha';abre('dRes');
}
/* ---------- mensajes ---------- */
function recibe(m){
  if(!m||!m.t)return;
  if(m.t==='sala'){D.me=m.tu;D.code=m.cod||D.code;const cambia=m.song!==D.song;D.song=m.song;D.dif=m.dif;
    const ant=D.jug;D.jug=m.jug.map((q,i)=>Object.assign(ant[i]||{},{nom:q.nom,listo:q.listo,ok:q.ok}));
    if(D.fase!=='sala'&&D.fase!=='juego'&&D.fase!=='cuenta')abreSala();else{if(cambia){precarga(D.song);setTimeout(elige,50);}pintaSala();}return;}
  if(m.t==='abresala'){try{G.endSession();G.show('menu');}catch(e){}abreSala();return;}
  if(m.t==='lleno'){D.on=false;info('dInfo',m.por||'La sala está llena.');return;}
  if(m.t==='va'){arranca(m.song,m.dif,m.jug);return;}
  const j=D.jug[m.from];if(!j)return;
  if(m.t==='sc'){j.sc=m.s|0;if(D.fase==='juego')pintaHud();}
  else if(m.t==='fin'){D.res[m.from]={s:m.s|0,a:m.a|0,c:m.c|0,x:m.x|0};j.sc=m.s|0;if(D.fase==='juego'||D.fase==='fin')revisaFin();}
  else if(m.t==='fuera')seVa(m.asiento);
}
function anfRecibe(conn,m){
  const i=D.jug.findIndex(j=>j.conn===conn);if(i<0||!m||!m.t)return;m.from=i;
  if(m.t==='elige'){const j=D.jug[i];j.nom=String(m.nom||'').slice(0,12)||'Jugador';j.listo=!!m.listo;j.ok=!!m.ok;difunde();return;}
  if(m.t==='revancha'){if(D.fase==='fin'||D.fase==='juego')volverSala();return;}
  reenvia(m,conn);recibe(m);
}
function volverSala(){
  if(!D.host){envia({t:'revancha'});$d('dRev').textContent='Volviendo…';return;}
  D.jug=D.jug.filter((j,i)=>i===0||(!j.fuera&&j.conn&&j.conn.open));D.jug.forEach(j=>{j.listo=false;});D.me=0;
  D.jug.forEach(j=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'abresala'});}catch(e){}}});
  try{G.endSession();G.show('menu');}catch(e){}abreSala();difunde();
}
function seVa(i){const j=D.jug[i];if(!j||j.fuera)return;j.fuera=true;
  if(D.fase==='sala'&&D.host){D.jug.splice(i,1);difunde();return;}
  if(D.host)reenvia({t:'fuera',asiento:i,from:0},j.conn);
  if(D.fase==='juego'||D.fase==='fin')revisaFin();pintaHud();}
function creaSala(intento){
  info('dInfo','Conectando…');
  cargaPeer(ok=>{
    if(!ok){info('dInfo','No se ha podido cargar el modo online. Revisa la conexión.');return;}
    const L='ABCDEFGHJKLMNPQRSTUVWXYZ',code=[0,1,2,3].map(()=>L[Math.floor(Math.random()*L.length)]).join('');
    let peer;try{peer=new Peer(PREFIX+code,window.DUEL_PEER_OPTS||{});}catch(e){info('dInfo','Error al crear la sala.');return;}
    D.peer=peer;
    peer.on('open',()=>{D.on=true;D.host=true;D.me=0;D.code=code;D.jug=[{nom:miNom||'Jugador',listo:true,ok:true,conn:null}];abreSala();elige();});
    peer.on('error',e=>{if(e&&e.type==='unavailable-id'&&(intento||0)<4){try{peer.destroy();}catch(_){}creaSala((intento||0)+1);}else if(D.fase==='off')info('dInfo','Error de conexión ('+(e&&e.type||'?')+'). Inténtalo de nuevo.');});
    peer.on('connection',conn=>{
      conn.on('open',()=>{if(D.fase!=='sala'||D.jug.length>=MAXP){try{conn.send({t:'lleno',por:D.fase!=='sala'?'El duelo ya ha empezado. Espera al siguiente.':'La sala está llena (máximo '+MAXP+').'});}catch(e){}setTimeout(()=>{try{conn.close();}catch(e){}},400);return;}
        D.jug.push({nom:'Jugador '+(D.jug.length+1),listo:false,ok:false,conn});difunde();});
      conn.on('data',m=>anfRecibe(conn,m));
      conn.on('close',()=>{const i=D.jug.findIndex(j=>j.conn===conn);if(i>=0)seVa(i);});
    });
  });
}
function unirse(){
  const code=($d('dCodIn').value||'').trim().toUpperCase();if(code.length!==4){info('dInfo','Escribe el código de 4 letras.');return;}
  info('dInfo','Conectando…');
  cargaPeer(ok=>{
    if(!ok){info('dInfo','No se ha podido cargar el modo online. Revisa la conexión.');return;}
    let peer;try{peer=new Peer(window.DUEL_PEER_OPTS||{});}catch(e){info('dInfo','Error de conexión.');return;}
    D.peer=peer;let hecho=false;const falla=t=>{if(hecho)return;hecho=true;info('dInfo',t);try{peer.destroy();}catch(_){}};
    const to=setTimeout(()=>falla('No se encuentra la sala. Revisa el código (o puede que tu red bloquee la conexión).'),22000);
    peer.on('error',e=>{if(!D.on)falla(e&&e.type==='peer-unavailable'?'No existe esa sala. Revisa el código.':'Error de conexión ('+(e&&e.type||'?')+').');});
    peer.on('open',()=>{const conn=peer.connect(PREFIX+code,{reliable:true});D.conn=conn;D.code=code;
      conn.on('data',recibe);conn.on('close',pierdeAnf);
      conn.on('open',()=>{clearTimeout(to);hecho=true;D.on=true;D.host=false;info('dInfo','¡Conectado! Entrando en la sala…');setTimeout(()=>{D.listo=false;elige();},300);});});
  });
}
function pierdeAnf(){if(!D.on)return;const jugando=D.fase==='juego';D.on=false;D.fase='off';clearInterval(D.vigila);hud.hidden=true;
  if(jugando)return; // sigue tocando la canción en solitario
  abre('dIni');info('dInfo','Se ha cerrado la sala. Crea una nueva o únete con otro código.');}
function sal(){D.on=false;D.host=false;D.fase='off';clearInterval(D.vigila);clearTimeout(D.tiempo);hud.hidden=true;
  try{if(D.conn)D.conn.close();}catch(e){}D.jug.forEach(j=>{try{if(j.conn)j.conn.close();}catch(e){}});try{if(D.peer)D.peer.destroy();}catch(e){}
  D.conn=null;D.peer=null;D.jug=[];cierra();}

$d('dCrea').onclick=()=>creaSala(0);
$d('dUne').onclick=unirse;
$d('dCodIn').addEventListener('keydown',e=>{e.stopPropagation();if(e.key==='Enter')unirse();});
$d('dNom').addEventListener('keydown',e=>e.stopPropagation());
$d('dNom').addEventListener('change',()=>{if(D.fase==='sala')elige();});
$d('dListo').onclick=()=>{try{G.initAudio();}catch(e){}D.listo=!D.listo;if(D.song)precarga(D.song);elige();pintaSala();};
$d('dEmp').onclick=empieza;
$d('dRev').onclick=volverSala;
$d('dSalir1').onclick=()=>{sal();};
$d('dSalir2').onclick=()=>{sal();};
$d('dSalir3').onclick=()=>{sal();try{G.endSession();G.show('menu');}catch(e){}};
conInvita(()=>{const nom=(document.title||'Guitarra').split(/ [—|·-] /)[0].trim();SalaInvita.monta($d('dCod'),()=>D.code,nom,'es');SalaInvita.alEntrar(c=>{try{G.initAudio();}catch(e){}abre('dIni');$d('dCodIn').value=c;unirse();},1500);});
window.__duelo=D;
})();
