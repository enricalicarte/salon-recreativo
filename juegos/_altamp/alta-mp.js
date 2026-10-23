/* © 2026 Enric Alicarte · Alica Games Studio · Salón Recreativo. Todos los derechos reservados. Prohibida la copia, redistribución o publicación de este código en otros sitios sin permiso escrito. */
/* Alta Temporada · multijugador de 2 a 4 móviles (WebRTC / PeerJS)
   Lo usan El Gran Salto, La Gran Pirueta y El Gran Descenso. Los rivales del campeonato pasan a ser tus amigos:
   sala de espera (nombre y «¡Listo!»; el anfitrión elige el campeonato), cada uno hace su salto o bajada
   en su móvil y, al acabar cada ronda, la clasificación espera a que todos hayan terminado.
   El juego expone window.__alta (puente) y llama a window.__altaMP en initTour, showResult, nextRound y showFinal. */
(function(){
'use strict';
const __invSrc=(document.currentScript&&document.currentScript.src)||'';function conInvita(cb){if(window.SalaInvita)return cb();const s=document.createElement('script');s.src=new URL('../_sala/invita.js',__invSrc||location.href).href;s.onload=cb;document.head.appendChild(s);}
const A=()=>window.__alta;
const MAXP=4;
const $m=id=>document.getElementById(id);
const esc=t=>String(t==null?'':t).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const M={on:false,host:false,me:0,peer:null,conn:null,code:'',fase:'off',jug:[],listo:false,ti:0,riv:[]};
let miNom='';try{miNom=(localStorage.getItem('altatemp-nom')||'').slice(0,12);}catch(e){}
const PALABRA={salto:['salto','saltos'],pirueta:['salto','saltos'],descenso:['bajada','bajadas']};

/* ---------- estilos e interfaz ---------- */
const css=document.createElement('style');css.textContent=`
#mpov{z-index:45;background:radial-gradient(ellipse at 50% 20%,#1d3a66 0%,#0d1b33 60%,#08111f 100%)}
#mpBtnHome{position:relative;z-index:3;background:rgba(10,24,48,.88)!important;margin-top:10px!important;font-size:clamp(15px,4.2vw,19px)!important;padding:10px 26px!important}
#mpov .mpc{position:relative;z-index:2;width:min(440px,100%);max-height:100%;overflow-y:auto;color:var(--ivory,#f7f2e4);padding:6px 4px}
#mpov h2{font-family:var(--disp,serif);font-style:italic;font-weight:700;font-size:clamp(26px,7vw,34px);margin:0 0 6px}
#mpov p{margin:6px 0 10px;font-size:15px;opacity:.85;line-height:1.35}
#mpov .et{font-size:11px;letter-spacing:.18em;text-transform:uppercase;opacity:.7;margin:14px 0 6px}
#mpov input{font:700 20px system-ui,sans-serif;color:inherit;background:rgba(255,255,255,.08);border:1.5px solid currentColor;border-radius:999px;padding:9px 16px;text-align:center;width:100%;max-width:240px;outline:none;user-select:text;-webkit-user-select:text}
#mpov input:disabled{opacity:.55}
#mpCodIn{text-transform:uppercase;letter-spacing:.2em;width:8ch!important}
#mpov .fila{display:flex;gap:8px;justify-content:center;align-items:center;flex-wrap:wrap}
#mpov .fila .btn{margin-top:0}
#mpov .cod{font-family:var(--disp,serif);font-weight:700;font-size:clamp(42px,13vw,60px);letter-spacing:.18em;line-height:1.05}
#mpov .jl{display:flex;flex-direction:column;gap:6px;margin:8px 0;text-align:left}
#mpov .jl div{display:flex;align-items:center;gap:10px;border:1.5px solid rgba(247,242,228,.35);border-radius:14px;padding:7px 12px}
#mpov .jl div.yo{border-color:currentColor;background:rgba(255,255,255,.07)}
#mpov .jl b{flex:1;font-size:16px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#mpov .jl em{font-style:normal;font-size:12.5px;opacity:.75;white-space:nowrap}
#mpov .jl div.vacio{justify-content:center;border-style:dashed;opacity:.7;font-size:13.5px}
#mpov .tl{display:flex;flex-direction:column;gap:5px;text-align:left}
#mpov .tl button{display:flex;justify-content:space-between;gap:8px;font:600 14.5px system-ui,sans-serif;color:inherit;background:transparent;border:1.5px solid rgba(247,242,228,.3);border-radius:12px;padding:8px 12px;cursor:pointer}
#mpov .tl button small{opacity:.7;font-weight:500;white-space:nowrap}
#mpov .tl button.sel{border-color:currentColor;background:rgba(255,255,255,.12)}
#mpov .tl.solo button{pointer-events:none}
#mpov .btn:disabled{opacity:.5;cursor:default}
#mpWaitTag{display:block;margin-top:6px;font-size:13px;opacity:.85}
`;document.head.appendChild(css);
const ov=document.createElement('div');ov.id='mpov';ov.className='ov';ov.innerHTML=`<div class="frame"></div><div class="stripes"><i></i><i></i><i></i></div>
<div class="mpc" id="mpIni"><h2>Multijugador</h2><p>De 2 a 4 amigos, cada uno en su móvil: el mismo campeonato, ronda a ronda, con la clasificación de verdad. Vale con wifi distintos o datos móviles.</p>
  <button class="btn" id="mpCrea">Crear sala</button><div class="et">— o únete con un código —</div>
  <div class="fila"><input id="mpCodIn" maxlength="4" placeholder="CÓDIGO" autocomplete="off" autocapitalize="characters" spellcheck="false"><button class="btn alt" id="mpUne">Unirme</button></div>
  <p id="mpInfo" style="min-height:20px"></p><button class="btn alt sm" id="mpSal1">Volver</button></div>
<div class="mpc" id="mpSala" hidden><div class="et" style="margin-top:0">Código de la sala</div><div class="cod" id="mpCod">----</div>
  <div class="jl" id="mpJug"></div>
  <div class="et">Tu nombre</div><input id="mpNom" maxlength="12" autocomplete="off" spellcheck="false" placeholder="Nombre">
  <div class="et">Campeonato</div><div class="tl" id="mpTl"></div>
  <p id="mpInfoS"></p><button class="btn" id="mpListo">¡Listo!</button><button class="btn" id="mpEmp">Empezar</button><br><button class="btn alt sm" id="mpSal2">Salir</button></div>`;
document.body.appendChild(ov);
function abre(k){ov.classList.add('show');['mpIni','mpSala'].forEach(id=>$m(id).hidden=id!==k);}
function cierra(){ov.classList.remove('show');}
function info(id,t){$m(id).textContent=t;}
(function(){const pb=$m('playBtn');if(!pb)return;const b=document.createElement('button');b.className='btn alt';b.id='mpBtnHome';b.textContent='👥 Multijugador';
  pb.parentNode.insertBefore(b,pb.nextSibling);b.addEventListener('click',()=>{info('mpInfo','');abre('mpIni');});})();

/* ---------- red ---------- */
const PREFIX=()=>'altatemp-'+((A()&&A().kind)||'x')+'-';
function envia(o){o.from=M.me;
  if(M.host)M.jug.forEach(j=>{if(j.conn&&j.conn.open){try{j.conn.send(o);}catch(e){}}});
  else{try{if(M.conn&&M.conn.open)M.conn.send(o);}catch(e){}}}
function reenvia(m,menos){M.jug.forEach(j=>{if(j.conn&&j.conn!==menos&&j.conn.open){try{j.conn.send(m);}catch(e){}}});}
function cargaPeer(cb){if(window.Peer)return cb(true);
  const urls=['https://cdn.jsdelivr.net/npm/peerjs@1.5.4/dist/peerjs.min.js','https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js','https://cdnjs.cloudflare.com/ajax/libs/peerjs/1.5.4/peerjs.min.js'];
  let i=0;(function sig(){if(i>=urls.length)return cb(false);const s=document.createElement('script');s.src=urls[i++];s.onload=()=>cb(!!window.Peer);s.onerror=sig;document.head.appendChild(s);})();}

/* ---------- sala ---------- */
const datosSala=()=>M.jug.map(j=>({nom:j.nom,listo:!!j.listo}));
function difunde(){M.jug.forEach((j,i)=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'sala',tu:i,cod:M.code,ti:M.ti,jug:datosSala()});}catch(e){}}});pinta();}
function abreSala(){M.fase='sala';M.listo=false;if(!$m('mpNom').value)$m('mpNom').value=miNom||'Jugador';abre('mpSala');pinta();}
function elige(){const nom=($m('mpNom').value||'').trim().slice(0,12)||'Jugador';miNom=nom;try{localStorage.setItem('altatemp-nom',nom);}catch(e){}
  if(M.host){M.jug[0].nom=nom;difunde();}else envia({t:'elige',nom,listo:M.listo});}
function pinta(){
  if(M.fase!=='sala')return;const a=A();
  $m('mpCod').textContent=M.code||'----';
  $m('mpJug').innerHTML=M.jug.map((j,i)=>'<div class="'+(i===M.me?'yo':'')+'"><span>⛷️</span><b>'+esc(j.nom)+(i===M.me?' (tú)':'')+'</b><em>'+(i===0?'Anfitrión':j.listo?'✅ ¡Listo!':'Eligiendo…')+'</em></div>').join('')
    +(M.jug.length<MAXP?'<div class="vacio">'+(M.jug.length<2?'Esperando jugadores… comparte el código':'Puede entrar alguien más (máx. '+MAXP+')')+'</div>':'');
  $m('mpNom').disabled=M.listo;
  const tl=$m('mpTl'),pal=PALABRA[a.kind]||['ronda','rondas'];
  const fila=(t,i)=>'<button data-i="'+i+'" class="'+(i===M.ti?'sel':'')+'"><span>'+esc(t.name)+'</span><small>'+esc(t.sub||'')+' · '+t.rounds+' '+pal[1]+'</small></button>';
  if(M.host){tl.classList.remove('solo');tl.innerHTML=a.TOURS.map(fila).join('');tl.querySelectorAll('button').forEach(b=>b.onclick=()=>{M.ti=+b.dataset.i;difunde();});}
  else{tl.classList.add('solo');tl.innerHTML=fila(a.TOURS[M.ti]||a.TOURS[0],M.ti);}
  const bl=$m('mpListo'),be=$m('mpEmp');
  if(M.host){bl.hidden=true;be.hidden=false;const otros=M.jug.slice(1),todos=otros.length>=1&&otros.every(j=>j.listo);be.disabled=!todos;
    be.textContent=otros.length<1?'Esperando jugadores…':todos?'¡Empezar! ('+M.jug.length+')':'Esperando a que estén listos…';
    info('mpInfoS','Tú eliges el campeonato. Cada jugador pone su nombre y pulsa «¡Listo!».');}
  else{be.hidden=true;bl.hidden=false;bl.textContent=M.listo?'✓ ¡Listo! (cambiar)':'¡Listo!';info('mpInfoS',M.listo?'Esperando a que el anfitrión empiece…':'Pon tu nombre y pulsa «¡Listo!».');}
}
/* ---------- partida ---------- */
function empieza(){if(!M.host||$m('mpEmp').disabled)return;elige();const jug=M.jug.map(j=>({nom:j.nom}));
  M.jug.forEach((j,i)=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'sala',tu:i,cod:M.code,ti:M.ti,jug:datosSala()});j.conn.send({t:'va',ti:M.ti,jug});}catch(e){}}});arranca(M.ti,jug);}
function arranca(ti,jug){
  jug.forEach((q,i)=>{const j=M.jug[i]||(M.jug[i]={});j.nom=q.nom;j.fuera=false;j.v=[];});M.jug.length=jug.length;
  M.ti=ti;M.fase='juego';cierra();
  const a=A(),des=a.kind==='descenso',R=a.TOURS[ti].rounds;
  // rivales = los demás jugadores; sus puntos (o tiempos) se rellenan cuando llegan
  M.riv=M.jug.map((j,i)=>i===M.me?null:{name:j.nom,cc:'',idx:i,[des?'times':'scores']:Array.from({length:R},()=>0)}).filter(Boolean);
  a.startTour(ti);
  if(a.kind==='descenso')iniciaFantasmas();
}
const valor=r=>A().kind==='descenso'?r.time:r.total;
function ronda(n,r){
  if(!activo())return;const v=Math.round(valor(r)*1000)/1000;
  M.jug[M.me].v[n-1]=v;envia({t:'r',n,v});refresca();
}
function faltan(n){return M.jug.map((j,i)=>i).filter(i=>i!==M.me&&!M.jug[i].fuera&&M.jug[i].v[n-1]==null);}
function aplica(i){const j=M.jug[i],r=M.riv.find(x=>x.idx===i);if(!r)return;const arr=r.scores||r.times,des=!!r.times;
  for(let k=0;k<arr.length;k++){const v=j.v[k];arr[k]=v!=null?v:(j.fuera?(des?999:0):0);}}
function refresca(){
  if(M.fase!=='juego')return;const a=A(),P=a.P,n=P.round;
  M.jug.forEach((j,i)=>{if(i!==M.me)aplica(i);});
  const res=$m('result');if(!res||!res.classList.contains('show'))return;
  if(M.jug[M.me].v[n-1]==null)return;
  const w=faltan(n),nb=$m('nextBtn'),rr=$m('rRank');
  if(w.length){rr.innerHTML='⏳ Esperando a '+w.map(i=>esc(M.jug[i].nom)).join(', ')+'…';nb.disabled=true;nb.style.opacity=.5;}
  else{const st=a.standings(n),me=st.findIndex(x=>x.you)+1,l=st[0];
    rr.innerHTML=`<b>${me}.º</b> de ${st.length} · ${l.you?'Lideras con ':'Líder: '+esc(l.name)+' · '}${a.fmtTot(l.total)}`+
      '<span id="mpWaitTag">'+st.map((x,k)=>(k+1)+'. '+esc(x.name)+' '+a.fmtTot(x.total)).join(' · ')+'</span>';
    nb.disabled=false;nb.style.opacity='';}
}
function espera(){if(!activo())return false;const n=A().P.round;return faltan(n).length>0||M.jug[M.me].v[n-1]==null;}
function final(){
  if(!activo())return;
  $m('nextTourBtn').hidden=true;$m('againBtn').textContent='Volver a la sala';$m('toursBtn').textContent='Salir del multijugador';
  const st=A().standings(A().T.rounds),me=st.findIndex(x=>x.you)+1;
  $m('rTitle2').textContent=me===1?'¡Has ganado!':'¡Gana '+st[0].name+'!';$m('fSub').textContent=A().T.name+' · multijugador';
  $m('fList').innerHTML=st.map((r,i)=>`<div class="row${r.you?' me':''}"><i>${i+1}</i><div>${esc(r.name)}</div><em></em><span>${A().fmtTot(r.total)}</span></div>`).join('');
}
function volver(){if(M.host)volverSala();else{envia({t:'revancha'});$m('againBtn').textContent='Volviendo…';}}
function volverSala(){
  paraFantasmas();
  M.jug=M.jug.filter((j,i)=>i===0||(!j.fuera&&j.conn&&j.conn.open));M.jug.forEach(j=>j.listo=false);M.me=0;
  M.jug.forEach(j=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'abresala'});}catch(e){}}});
  try{A().openHome();}catch(e){}abreSala();difunde();
}
// botones del final y de la pausa mientras hay multijugador
function intercepta(id,fn){const b=$m(id);if(b)b.addEventListener('click',e=>{if(activo()){e.stopImmediatePropagation();e.preventDefault();fn();}},true);}
intercepta('againBtn',volver);
intercepta('toursBtn',()=>{sal();A().openTours();});
intercepta('quitBtn',()=>{$m('pause').classList.remove('show');A().P.paused=false;sal();A().openTours();});

/* ---------- El Gran Descenso: trineos de los demás como fantasmas ---------- */
let fT=null,fR=0;
function iniciaFantasmas(){
  clearInterval(fT);cancelAnimationFrame(fR);
  fT=setInterval(()=>{if(!activo())return;const a=A(),P=a.P,r=a.run;
    if(r&&(P.mode==='push'||P.mode==='run'))envia({t:'g',n:P.round,s:+r.s.toFixed(2),y:+r.y.toFixed(3),v:+r.v.toFixed(2),m:P.mode});},150);
  const loop=()=>{fR=requestAnimationFrame(loop);if(!activo())return;const a=A(),P=a.P,now=performance.now();
    M.jug.forEach((j,i)=>{if(i===M.me)return;const g=j.g,vis=!j.fuera&&g&&g.n===P.round&&(g.m==='push'||g.m==='run')&&now-g.t<1500;
      if(!vis){a.ghost(i,0,0,false,j.nom);return;}
      const est=g.s+g.v*Math.min(.4,(now-g.t)/1000);j.gs=j.gs==null||Math.abs(est-j.gs)>25?est:j.gs+(est-j.gs)*.25;
      const mio=a.run&&(P.mode==='push'||P.mode==='run')?a.run.s:null,ds=mio==null?99:j.gs-mio;
      a.ghost(i,j.gs,g.y,!(ds<1.5&&ds>-16),j.nom);});};
  loop();
}
function paraFantasmas(){clearInterval(fT);cancelAnimationFrame(fR);try{if(A().ghostClear)A().ghostClear();}catch(e){}}
/* ---------- mensajes ---------- */
function recibe(m){
  if(!m||!m.t)return;
  if(m.t==='sala'){M.me=m.tu;M.code=m.cod||M.code;M.ti=m.ti|0;const ant=M.jug;M.jug=m.jug.map((q,i)=>Object.assign(ant[i]||{},{nom:q.nom,listo:q.listo}));
    if(M.fase!=='sala'&&M.fase!=='juego')abreSala();else pinta();return;}
  if(m.t==='abresala'){paraFantasmas();try{A().openHome();}catch(e){}abreSala();return;}
  if(m.t==='lleno'){M.on=false;info('mpInfo',m.por||'La sala está llena.');return;}
  if(m.t==='va'){arranca(m.ti|0,m.jug);return;}
  const j=M.jug[m.from];if(!j)return;
  if(m.t==='r'){j.v[m.n-1]=+m.v;refresca();}
  else if(m.t==='g'){j.g={n:m.n,s:+m.s,y:+m.y,v:+m.v,m:m.m,t:performance.now()};}
  else if(m.t==='fuera')seVa(m.asiento);
}
function anfRecibe(conn,m){
  const i=M.jug.findIndex(j=>j.conn===conn);if(i<0||!m||!m.t)return;m.from=i;
  if(m.t==='elige'){const j=M.jug[i];j.nom=String(m.nom||'').slice(0,12)||'Jugador';j.listo=!!m.listo;difunde();return;}
  if(m.t==='revancha'){if(M.fase==='juego')volverSala();return;}
  reenvia(m,conn);recibe(m);
}
function seVa(i){const j=M.jug[i];if(!j||j.fuera)return;j.fuera=true;
  if(M.fase==='sala'&&M.host){M.jug.splice(i,1);difunde();return;}
  if(M.host)reenvia({t:'fuera',asiento:i,from:0},j.conn);
  const r=M.riv.find(x=>x.idx===i);if(r)r.name=j.nom+' (se fue)';refresca();}
function creaSala(intento){
  info('mpInfo','Conectando…');
  cargaPeer(ok=>{
    if(!ok){info('mpInfo','No se ha podido cargar el modo online. Revisa la conexión.');return;}
    const L='ABCDEFGHJKLMNPQRSTUVWXYZ',code=[0,1,2,3].map(()=>L[Math.floor(Math.random()*L.length)]).join('');
    let peer;try{peer=new Peer(PREFIX()+code,window.ALTA_PEER_OPTS||{});}catch(e){info('mpInfo','Error al crear la sala.');return;}
    M.peer=peer;
    peer.on('open',()=>{M.on=true;M.host=true;M.me=0;M.code=code;M.jug=[{nom:miNom||'Jugador',listo:true,conn:null}];abreSala();elige();});
    peer.on('error',e=>{if(e&&e.type==='unavailable-id'&&(intento||0)<4){try{peer.destroy();}catch(_){}creaSala((intento||0)+1);}else if(M.fase==='off')info('mpInfo','Error de conexión ('+(e&&e.type||'?')+'). Inténtalo de nuevo.');});
    peer.on('connection',conn=>{
      conn.on('open',()=>{if(M.fase!=='sala'||M.jug.length>=MAXP){try{conn.send({t:'lleno',por:M.fase!=='sala'?'El campeonato ya ha empezado. Espera al siguiente.':'La sala está llena (máximo '+MAXP+').'});}catch(e){}setTimeout(()=>{try{conn.close();}catch(e){}},400);return;}
        M.jug.push({nom:'Jugador '+(M.jug.length+1),listo:false,conn});difunde();});
      conn.on('data',m=>anfRecibe(conn,m));
      conn.on('close',()=>{const i=M.jug.findIndex(j=>j.conn===conn);if(i>=0)seVa(i);});
    });
  });
}
function unirse(){
  const code=($m('mpCodIn').value||'').trim().toUpperCase();if(code.length!==4){info('mpInfo','Escribe el código de 4 letras.');return;}
  info('mpInfo','Conectando…');
  cargaPeer(ok=>{
    if(!ok){info('mpInfo','No se ha podido cargar el modo online. Revisa la conexión.');return;}
    let peer;try{peer=new Peer(window.ALTA_PEER_OPTS||{});}catch(e){info('mpInfo','Error de conexión.');return;}
    M.peer=peer;let hecho=false;const falla=t=>{if(hecho)return;hecho=true;info('mpInfo',t);try{peer.destroy();}catch(_){}};
    const to=setTimeout(()=>falla('No se encuentra la sala. Revisa el código (o puede que tu red bloquee la conexión).'),22000);
    peer.on('error',e=>{if(!M.on)falla(e&&e.type==='peer-unavailable'?'No existe esa sala. Revisa el código.':'Error de conexión ('+(e&&e.type||'?')+').');});
    peer.on('open',()=>{const conn=peer.connect(PREFIX()+code,{reliable:true});M.conn=conn;M.code=code;
      conn.on('data',recibe);conn.on('close',pierdeAnf);
      conn.on('open',()=>{clearTimeout(to);hecho=true;M.on=true;M.host=false;info('mpInfo','¡Conectado! Entrando en la sala…');setTimeout(()=>{M.listo=false;elige();},300);});});
  });
}
function pierdeAnf(){if(!M.on)return;const jugando=M.fase==='juego';M.on=false;M.fase='off';
  if(jugando){M.jug.forEach((j,i)=>{if(i!==M.me){j.fuera=true;}});refresca();return;}
  abre('mpIni');info('mpInfo','Se ha cerrado la sala. Crea una nueva o únete con otro código.');}
function sal(){paraFantasmas();M.on=false;M.host=false;M.fase='off';try{if(M.conn)M.conn.close();}catch(e){}M.jug.forEach(j=>{try{if(j.conn)j.conn.close();}catch(e){}});try{if(M.peer)M.peer.destroy();}catch(e){}
  M.conn=null;M.peer=null;M.jug=[];M.riv=[];cierra();}
function activo(){return M.fase==='juego';}

$m('mpCrea').onclick=()=>creaSala(0);
$m('mpUne').onclick=unirse;
['mpCodIn','mpNom'].forEach(id=>$m(id).addEventListener('keydown',e=>{e.stopPropagation();if(e.key==='Enter'&&id==='mpCodIn')unirse();}));
$m('mpNom').addEventListener('change',()=>{if(M.fase==='sala')elige();});
$m('mpListo').onclick=()=>{M.listo=!M.listo;elige();pinta();};
$m('mpEmp').onclick=empieza;
$m('mpSal1').onclick=()=>{sal();};
$m('mpSal2').onclick=()=>{sal();};
conInvita(()=>{const nom=(document.title||'Alta Temporada').split(/ [—|·-] /)[0].trim();SalaInvita.monta($m('mpCod'),()=>M.code,nom,'es');SalaInvita.alEntrar(c=>{abre('mpIni');$m('mpCodIn').value=c;unirse();},2500);});
window.__altaMP={activo,rivales:()=>M.riv,ronda,espera:()=>{const e=espera();if(e){refresca();}return e;},final,volver,estado:M};
})();
