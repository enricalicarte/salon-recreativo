/* © 2026 Enric Alicarte · Alica Games Studio · Salón Recreativo. Todos los derechos reservados. Prohibida la copia, redistribución o publicación de este código en otros sitios sin permiso escrito. */
/* Looping Loco · carrera multijugador de 2 a 4 móviles (WebRTC / PeerJS)
   Mismo nivel para todos (la pista sale de la misma semilla), cada uno con su vehículo, salida a la vez y los
   demás como fantasmas en la pista. Cada piloto tiene 3 intentos; gana quien más puntos hace al llegar a la meta.
   El juego expone window.__loop y llama a window.__loopMP.fin()/fuera()/sal()/boton(). */
(function(){
'use strict';
const __invSrc=(document.currentScript&&document.currentScript.src)||'';
function conInvita(cb){if(window.SalaInvita)return cb();const s=document.createElement('script');s.src=new URL('../_sala/invita.js',__invSrc||location.href).href;s.onload=cb;document.head.appendChild(s);}
const A=()=>window.__loop;
const MAXP=4;
const $q=id=>document.getElementById(id);
const esc=t=>String(t==null?'':t).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const M={on:false,host:false,me:0,peer:null,conn:null,code:'',fase:'off',jug:[],listo:false,lv:1,veh:'rayo',res:{},envT:null,raf:0,maxS:0};
let miNom='';try{miNom=(localStorage.getItem('looprace-nom')||'').slice(0,12);}catch(e){}
const COLS=['#ff4fd8','#38e8ff','#ffd23f','#6dff8a'];

const css=document.createElement('style');css.textContent=`
#lmpBtn{font-size:.82em!important}
#lmp{position:fixed;inset:0;z-index:60;display:flex;align-items:center;justify-content:center;background:rgba(15,10,40,.8);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);padding:12px}
#lmp.hide{display:none}
#lmp .mc{width:min(440px,94vw);max-height:92vh;overflow-y:auto;background:linear-gradient(180deg,#2b1f63,#140c36);border:3px solid #ffe14a;border-radius:22px;padding:18px 16px;color:#fff;font-family:system-ui,-apple-system,'Segoe UI',sans-serif;text-align:center;box-shadow:0 8px 0 rgba(0,0,0,.35)}
#lmp h2{margin:0 0 6px;font:400 28px/1.1 'Lilita One',system-ui,sans-serif;letter-spacing:.02em;color:#ffe14a}
#lmp p{margin:6px 0 10px;font-size:14.5px;opacity:.9;line-height:1.35}
#lmp .et{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:800;opacity:.7;margin:12px 0 6px}
#lmp button.b{font:800 16px system-ui,sans-serif;color:#1a1300;background:#ffe14a;border:0;border-radius:999px;padding:11px 22px;margin:4px;cursor:pointer;box-shadow:0 4px 0 #b88a00}
#lmp button.b2{font:700 14px system-ui,sans-serif;color:#fff;background:rgba(255,255,255,.1);border:1.5px solid rgba(255,255,255,.4);border-radius:999px;padding:9px 18px;margin:4px;cursor:pointer}
#lmp button:disabled{opacity:.5;cursor:default}
#lmp input{font:800 20px system-ui,sans-serif;color:#fff;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.45);border-radius:14px;padding:9px 12px;text-align:center;width:100%;max-width:240px;outline:none;user-select:text;-webkit-user-select:text}
#lmp input:disabled{opacity:.55}
#lmpCodIn{text-transform:uppercase;letter-spacing:.2em;width:8ch!important}
#lmp .fila{display:flex;gap:6px;justify-content:center;align-items:center;flex-wrap:wrap}
#lmp .cod{font-size:clamp(42px,13vw,58px);font-weight:900;letter-spacing:.2em;color:#ffe14a;line-height:1.05}
#lmp .jl{display:flex;flex-direction:column;gap:6px;margin:8px 0;text-align:left}
#lmp .jl div{display:flex;align-items:center;gap:10px;background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.18);border-radius:14px;padding:7px 12px}
#lmp .jl div.yo{border-color:#ffe14a}
#lmp .jl b{flex:1;font-size:16px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#lmp .jl em{font-style:normal;font-weight:700;font-size:12.5px;opacity:.8;white-space:nowrap}
#lmp .jl small{display:block;font-size:11.5px;font-weight:600;opacity:.7}
#lmp .jl div.vacio{justify-content:center;border-style:dashed;opacity:.7;font-size:13.5px}
#lmp .ops{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
#lmp .ops button{font:700 13.5px system-ui,sans-serif;color:#fff;background:rgba(255,255,255,.08);border:1.5px solid rgba(255,255,255,.25);border-radius:12px;padding:8px 11px;cursor:pointer}
#lmp .ops button.sel{background:#ffe14a;border-color:#ffe14a;color:#1a1300}
#lmp .ops button.lock{opacity:.4}
#lmp .ops.solo button{pointer-events:none}
#lmp table{width:100%;border-collapse:collapse;margin:10px 0;font-size:15px}
#lmp td,#lmp th{padding:6px 4px;border-bottom:1px solid rgba(255,255,255,.12)}
#lmp th{font-size:11px;letter-spacing:.1em;text-transform:uppercase;opacity:.7}
#lmp tr.yo td{color:#ffe14a;font-weight:800}
#lmpHud{position:fixed;right:10px;top:34%;z-index:8;display:flex;flex-direction:column;gap:4px;pointer-events:none;font:800 13px/1 system-ui,sans-serif;color:#fff}
#lmpHud[hidden]{display:none}
#lmpHud div{display:flex;gap:7px;align-items:center;background:rgba(15,10,40,.7);border:1.5px solid rgba(255,255,255,.25);border-radius:999px;padding:5px 10px;min-width:124px}
#lmpHud div.yo{border-color:#ffe14a}
#lmpHud div.fuera{opacity:.45;text-decoration:line-through}
#lmpHud i{font-style:normal;width:16px;text-align:center;color:#ffe14a}
#lmpHud b{flex:1;max-width:78px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#lmpHud span{font-variant-numeric:tabular-nums}
`;document.head.appendChild(css);
const ov=document.createElement('div');ov.id='lmp';ov.className='hide';ov.innerHTML=`
<div class="mc" id="lmpIni"><h2>🏁 Carrera con amigos</h2><p>De 2 a 4 jugadores, cada uno en su móvil: el mismo nivel, salida a la vez y los demás como fantasmas en la pista. Tres intentos cada uno; gana quien más puntos haga al llegar a la meta. Vale con wifi distintos o datos móviles.</p>
  <button class="b" id="lmpCrea">Crear sala</button><div class="et">— o únete con un código —</div>
  <div class="fila"><input id="lmpCodIn" maxlength="4" placeholder="CÓDIGO" autocomplete="off" autocapitalize="characters" spellcheck="false"><button class="b2" id="lmpUne" style="font-size:16px">Unirme</button></div>
  <p id="lmpInfo" style="min-height:20px;margin-bottom:4px"></p><button class="b2" id="lmpSal1">Volver</button></div>
<div class="mc" id="lmpSala" hidden><div class="et" style="margin-top:0">Código de la sala</div><div class="cod" id="lmpCod">----</div>
  <div class="jl" id="lmpJug"></div>
  <div class="et">Tu nombre</div><input id="lmpNom" maxlength="12" autocomplete="off" spellcheck="false" placeholder="Nombre">
  <div class="et">Tu vehículo</div><div class="ops" id="lmpV"></div>
  <div class="et">Nivel</div><div class="ops" id="lmpL"></div>
  <p id="lmpInfoS"></p><button class="b" id="lmpListo">¡Listo!</button><button class="b" id="lmpEmp">Empezar</button><br><button class="b2" id="lmpSal2">Salir</button></div>
<div class="mc" id="lmpRes" hidden><h2 id="lmpResT">Resultado</h2><p id="lmpResS"></p>
  <table><thead><tr><th></th><th style="text-align:left">Piloto</th><th>Puntos</th><th>★</th><th>Intento</th></tr></thead><tbody id="lmpResL"></tbody></table>
  <button class="b" id="lmpRev">Revancha</button><br><button class="b2" id="lmpSal3">Salir del multijugador</button></div>`;
document.body.appendChild(ov);
const hud=document.createElement('div');hud.id='lmpHud';hud.hidden=true;document.body.appendChild(hud);
function abre(k){ov.classList.remove('hide');['lmpIni','lmpSala','lmpRes'].forEach(id=>$q(id).hidden=id!==k);}
function cierra(){ov.classList.add('hide');}
function info(id,t){$q(id).textContent=t;}
['pointerdown','touchstart','mousedown','keydown','keyup'].forEach(ev=>ov.addEventListener(ev,e=>e.stopPropagation()));
function boton(p){const b=document.createElement('button');b.className='ybtn alt';b.id='lmpBtn';b.type='button';b.textContent='👥 CON AMIGOS · 2 A 4';
  b.addEventListener('click',e=>{e.stopPropagation();try{A().initAudio();}catch(_){}info('lmpInfo','');abre('lmpIni');});p.appendChild(b);}

/* ---------- red ---------- */
const PREFIX='looprace-';
function envia(o){o.from=M.me;
  if(M.host)M.jug.forEach(j=>{if(j.conn&&j.conn.open){try{j.conn.send(o);}catch(e){}}});
  else{try{if(M.conn&&M.conn.open)M.conn.send(o);}catch(e){}}}
function reenvia(m,menos){M.jug.forEach(j=>{if(j.conn&&j.conn!==menos&&j.conn.open){try{j.conn.send(m);}catch(e){}}});}
function cargaPeer(cb){if(window.Peer)return cb(true);
  const urls=['https://cdn.jsdelivr.net/npm/peerjs@1.5.4/dist/peerjs.min.js','https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js','https://cdnjs.cloudflare.com/ajax/libs/peerjs/1.5.4/peerjs.min.js'];
  let i=0;(function sig(){if(i>=urls.length)return cb(false);const s=document.createElement('script');s.src=urls[i++];s.onload=()=>cb(!!window.Peer);s.onerror=sig;document.head.appendChild(s);})();}

/* ---------- sala ---------- */
const vehNom=id=>{const v=A().VEH.find(x=>x.id===id);return v?v.name:'';};
const datosSala=()=>M.jug.map(j=>({nom:j.nom,listo:!!j.listo,veh:j.veh||'rayo'}));
function difunde(){M.jug.forEach((j,i)=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'sala',tu:i,cod:M.code,lv:M.lv,jug:datosSala()});}catch(e){}}});pinta();}
function abreSala(){M.fase='sala';M.listo=false;M.res={};hud.hidden=true;paraFantasmas();
  const a=A();if(a.VEH.findIndex(v=>v.id===M.veh)<0||a.totalStars()<a.VEH.find(v=>v.id===M.veh).need)M.veh=a.SV.veh;
  if(!$q('lmpNom').value)$q('lmpNom').value=miNom||'Piloto';abre('lmpSala');pinta();}
function elige(){const nom=($q('lmpNom').value||'').trim().slice(0,12)||'Piloto';miNom=nom;try{localStorage.setItem('looprace-nom',nom);}catch(e){}
  if(M.host){M.jug[0].nom=nom;M.jug[0].veh=M.veh;difunde();}else envia({t:'elige',nom,listo:M.listo,veh:M.veh});}
function pinta(){
  if(M.fase!=='sala')return;const a=A();
  $q('lmpCod').textContent=M.code||'----';
  $q('lmpJug').innerHTML=M.jug.map((j,i)=>'<div class="'+(i===M.me?'yo':'')+'"><span>🏍️</span><b>'+esc(j.nom)+(i===M.me?' (tú)':'')+'<small>'+esc(vehNom(j.veh||'rayo'))+'</small></b><em>'+(i===0?'Anfitrión':j.listo?'✅ ¡Listo!':'Eligiendo…')+'</em></div>').join('')
    +(M.jug.length<MAXP?'<div class="vacio">'+(M.jug.length<2?'Esperando jugadores… comparte el código':'Puede entrar alguien más (máx. '+MAXP+')')+'</div>':'');
  $q('lmpNom').disabled=M.listo;
  const ts=a.totalStars(),V=$q('lmpV');V.classList.toggle('solo',M.listo);
  V.innerHTML=a.VEH.map(v=>{const ok=ts>=v.need;return '<button data-v="'+v.id+'" class="'+(v.id===M.veh?'sel':'')+(ok?'':' lock')+'"'+(ok?'':' disabled')+'>'+(ok?'':'🔒 ')+esc(v.name.toLowerCase())+'</button>';}).join('');
  V.querySelectorAll('button:not([disabled])').forEach(b=>b.onclick=()=>{M.veh=b.dataset.v;elige();pinta();});
  const L=$q('lmpL');L.classList.toggle('solo',!M.host);
  const lvs=[];for(let i=1;i<=a.MAXL;i++)lvs.push(i);
  L.innerHTML=(M.host?lvs:[M.lv]).map(i=>'<button data-l="'+i+'" class="'+(i===M.lv?'sel':'')+'">'+i+' · '+esc(a.LNAME[i-1].toLowerCase())+'</button>').join('');
  if(M.host)L.querySelectorAll('button').forEach(b=>b.onclick=()=>{M.lv=+b.dataset.l;difunde();});
  const bl=$q('lmpListo'),be=$q('lmpEmp');
  if(M.host){bl.hidden=true;be.hidden=false;const otros=M.jug.slice(1),todos=otros.length>=1&&otros.every(j=>j.listo);be.disabled=!todos;
    be.textContent=otros.length<1?'Esperando jugadores…':todos?'¡Empezar la carrera! ('+M.jug.length+')':'Esperando a que estén listos…';
    info('lmpInfoS','Tú eliges el nivel. Cada piloto elige su vehículo y pulsa «¡Listo!».');}
  else{be.hidden=true;bl.hidden=false;bl.textContent=M.listo?'✓ ¡Listo! (cambiar)':'¡Listo!';info('lmpInfoS',M.listo?'Esperando a que el anfitrión empiece…':'Elige tu vehículo y pulsa «¡Listo!».');}
}
/* ---------- carrera ---------- */
function empieza(){if(!M.host||$q('lmpEmp').disabled)return;elige();const jug=datosSala();
  M.jug.forEach((j,i)=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'sala',tu:i,cod:M.code,lv:M.lv,jug});j.conn.send({t:'va',lv:M.lv,jug});}catch(e){}}});
  arranca(M.lv,jug);}
function arranca(lv,jug){
  jug.forEach((q,i)=>{const j=M.jug[i]||(M.jug[i]={});j.nom=q.nom;j.veh=q.veh||'rayo';j.fuera=false;j.g=null;j.p=0;j.at=1;});M.jug.length=jug.length;
  M.lv=lv;M.res={};M.maxS=0;M.fase='juego';cierra();
  try{A().run(lv,M.veh);}catch(e){console.error(e);}
  hud.hidden=false;clearInterval(M.envT);M.envT=setInterval(tic,120);iniciaFantasmas();pintaHud();
}
function tic(){
  if(M.fase!=='juego')return;const a=A(),B=a.B,yo=M.jug[M.me];
  if(!M.res[M.me]&&a.LV){if(B.s>M.maxS&&a.st.mode==='run')M.maxS=B.s;yo.p=a.pct(B.s);yo.at=a.st.attempt;
    envia({t:'g',s:+B.s.toFixed(2),x:+B.x.toFixed(2),v:+B.v.toFixed(1),m:a.st.mode,at:a.st.attempt});}
  pintaHud();
}
function fin(r){if(M.fase!=='juego'||M.res[M.me])return;const x={sc:r.sc|0,f:1,st:r.st|0,tot:r.tot|0,at:r.at|0,p:100};M.res[M.me]=x;envia(Object.assign({t:'fin'},x));revisa();}
function fuera(){if(M.fase!=='juego'||M.res[M.me])return;const x={sc:0,f:0,st:0,tot:0,at:3,p:A().pct(M.maxS)};M.res[M.me]=x;envia(Object.assign({t:'fin'},x));revisa();}
function revisa(){
  const act=M.jug.map((j,i)=>i).filter(i=>!M.jug[i].fuera);pintaHud();
  if(!M.res[M.me])return;
  if(act.every(i=>M.res[i])){M.fase='fin';clearInterval(M.envT);hud.hidden=true;paraFantasmas();setTimeout(resultado,1500);}
}
function orden(){return M.jug.map((j,i)=>({j,i,r:M.res[i]||{sc:0,f:0,st:0,tot:0,at:j.at||1,p:j.p||0}})).sort((a,b)=>{
  if(a.r.f&&b.r.f)return b.r.sc-a.r.sc;if(a.r.f)return -1;if(b.r.f)return 1;return (b.r.p||0)-(a.r.p||0);});}
function pintaHud(){
  if(M.fase!=='juego'){hud.hidden=true;return;}hud.hidden=false;
  hud.innerHTML=orden().map((o,k)=>'<div class="'+(o.i===M.me?'yo':'')+(o.j.fuera?' fuera':'')+'"><i>'+(o.r.f?'🏁':M.res[o.i]?'✕':(k+1))+'</i><b>'+esc(o.i===M.me?'Tú':o.j.nom)+'</b><span>'+(o.r.f?o.r.sc:Math.max(0,Math.min(99,o.r.p|0))+'%'+(M.res[o.i]?'':' · '+(o.j.at||1)+'/3'))+'</span></div>').join('');
}
function resultado(){
  const ord=orden(),med=['🥇','🥈','🥉','4º'],yo=ord.findIndex(o=>o.i===M.me);
  $q('lmpResT').textContent=yo===0?'🏆 ¡Has ganado la carrera!':'¡Gana '+ord[0].j.nom+'!';
  const a=A();$q('lmpResS').textContent='Nivel '+M.lv+' · '+a.LNAME[M.lv-1].toLowerCase();
  $q('lmpResL').innerHTML=ord.map((o,k)=>'<tr class="'+(o.i===M.me?'yo':'')+'"><td>'+(o.r.f?med[k]:'')+'</td><td style="text-align:left">'+esc(o.i===M.me?'Tú':o.j.nom)+(o.j.fuera?' <small>(se fue)</small>':'')+'</td><td>'+(o.r.f?o.r.sc:'✕ '+(o.r.p|0)+'%')+'</td><td>'+(o.r.f?o.r.st+'/'+o.r.tot:'–')+'</td><td>'+(o.r.f?o.r.at+'/3':'–')+'</td></tr>').join('');
  $q('lmpRev').textContent='Revancha';abre('lmpRes');
}
function volver(){if(M.host)volverSala();else{envia({t:'revancha'});$q('lmpRev').textContent='Volviendo…';}}
function volverSala(){
  M.jug=M.jug.filter((j,i)=>i===0||(!j.fuera&&j.conn&&j.conn.open));M.jug.forEach(j=>j.listo=false);M.me=0;
  M.jug.forEach(j=>{if(j.conn&&j.conn.open){try{j.conn.send({t:'abresala'});}catch(e){}}});
  try{A().toMenu();}catch(e){}abreSala();difunde();
}

/* ---------- fantasmas ---------- */
const GH={};
function fantasma(i){
  const a=A();if(GH[i])return GH[i];const T3=window.THREE;
  const md=a.BUILD[M.jug[i].veh||'rayo']();const g=new T3.Group();g.add(md.g);md.g.position.y=md.hover||0;
  const vv=a.VEH.find(v=>v.id===(M.jug[i].veh||'rayo'));g.scale.setScalar(vv?vv.size:1);
  g.traverse(o=>{if(o.material){const ms=Array.isArray(o.material)?o.material:[o.material];const nm=ms.map(m=>{const c=m.clone();c.transparent=true;c.opacity=.45;c.depthWrite=false;return c;});o.material=Array.isArray(o.material)?nm:nm[0];}});
  const cv=document.createElement('canvas');cv.width=256;cv.height=64;const x=cv.getContext('2d');x.font='bold 34px system-ui,sans-serif';x.textAlign='center';x.textBaseline='middle';
  x.fillStyle=COLS[i%4];x.beginPath();if(x.roundRect)x.roundRect(8,8,240,48,24);else x.rect(8,8,240,48);x.fill();x.fillStyle='#111';x.fillText(String(M.jug[i].nom||'').slice(0,12),128,34);
  const sp=new T3.Sprite(new T3.SpriteMaterial({map:new T3.CanvasTexture(cv),depthTest:false,transparent:true,fog:false}));sp.scale.set(2.8,.7,1);sp.renderOrder=999;
  a.scene.add(g);a.scene.add(sp);GH[i]={g,sp,s:0,x:0};return GH[i];
}
const _m=()=>new window.THREE.Matrix4();let MB=null;
function iniciaFantasmas(){
  cancelAnimationFrame(M.raf);MB=MB||_m();
  const loop=()=>{M.raf=requestAnimationFrame(loop);if(M.fase!=='juego')return;const a=A();if(!a.LV)return;const now=performance.now();
    M.jug.forEach((j,i)=>{if(i===M.me)return;const g=j.g,vis=!j.fuera&&g&&now-g.t<2000&&(g.m==='run'||g.m==='count'||g.m==='finish');
      const f=GH[i]||(vis?fantasma(i):null);if(!f)return;f.g.visible=f.sp.visible=!!vis;if(!vis)return;
      const es=g.m==='run'?g.s+g.v*Math.min(.25,(now-g.t)/1000):g.s;
      if(Math.abs(es-f.s)>12){f.s=es;f.x=g.x;}else{f.s+=(es-f.s)*.3;f.x+=(g.x-f.x)*.3;}
      const fr=a.frame(f.s);
      f.g.position.copy(fr.p).addScaledVector(fr.r,f.x);MB.makeBasis(fr.r,fr.u,fr.t.clone().negate());f.g.quaternion.setFromRotationMatrix(MB);
      f.sp.position.copy(f.g.position).addScaledVector(fr.u,2.6);
      const d=f.g.position.distanceTo(a.camera.position);f.sp.visible=d>6;});
  };
  loop();
}
function paraFantasmas(){cancelAnimationFrame(M.raf);const a=A();for(const k in GH){try{a.scene.remove(GH[k].g);a.scene.remove(GH[k].sp);}catch(e){}delete GH[k];}}

/* ---------- mensajes ---------- */
function recibe(m){
  if(!m||!m.t)return;
  if(m.t==='sala'){M.me=m.tu;M.code=m.cod||M.code;M.lv=m.lv|0||1;const ant=M.jug;M.jug=m.jug.map((q,i)=>Object.assign(ant[i]||{},{nom:q.nom,listo:q.listo,veh:q.veh}));
    if(M.fase!=='sala'&&M.fase!=='juego')abreSala();else pinta();return;}
  if(m.t==='abresala'){try{A().toMenu();}catch(e){}abreSala();return;}
  if(m.t==='lleno'){M.on=false;info('lmpInfo',m.por||'La sala está llena.');return;}
  if(m.t==='va'){arranca(m.lv|0||1,m.jug);return;}
  const j=M.jug[m.from];if(!j)return;
  if(m.t==='g'){j.g={s:+m.s,x:+m.x,v:+m.v||0,m:m.m,t:performance.now()};j.at=m.at|0||1;if(m.m==='run'||m.m==='crash')j.p=Math.max(j.p||0,A().pct(+m.s));}
  else if(m.t==='fin'){M.res[m.from]={sc:m.sc|0,f:m.f|0,st:m.st|0,tot:m.tot|0,at:m.at|0,p:m.p|0};revisa();}
  else if(m.t==='fuera')seVa(m.asiento);
}
function anfRecibe(conn,m){
  const i=M.jug.findIndex(j=>j.conn===conn);if(i<0||!m||!m.t)return;m.from=i;
  if(m.t==='elige'){const j=M.jug[i];j.nom=String(m.nom||'').slice(0,12)||'Piloto';j.listo=!!m.listo;j.veh=String(m.veh||'rayo').slice(0,10);difunde();return;}
  if(m.t==='revancha'){if(M.fase==='fin'||M.fase==='juego')volverSala();return;}
  reenvia(m,conn);recibe(m);
}
function seVa(i){const j=M.jug[i];if(!j||j.fuera)return;j.fuera=true;
  if(M.fase==='sala'&&M.host){M.jug.splice(i,1);difunde();return;}
  if(M.host)reenvia({t:'fuera',asiento:i,from:0},j.conn);
  if(M.fase==='juego')revisa();}
function creaSala(intento){
  info('lmpInfo','Conectando…');
  cargaPeer(ok=>{
    if(!ok){info('lmpInfo','No se ha podido cargar el modo online. Revisa la conexión.');return;}
    const L='ABCDEFGHJKLMNPQRSTUVWXYZ',code=[0,1,2,3].map(()=>L[Math.floor(Math.random()*L.length)]).join('');
    let peer;try{peer=new Peer(PREFIX+code,window.LOOP_PEER_OPTS||{});}catch(e){info('lmpInfo','Error al crear la sala.');return;}
    M.peer=peer;
    peer.on('open',()=>{M.on=true;M.host=true;M.me=0;M.code=code;M.lv=A().st.level||1;M.veh=A().SV.veh;M.jug=[{nom:miNom||'Piloto',listo:true,conn:null,veh:M.veh}];abreSala();elige();});
    peer.on('error',e=>{if(e&&e.type==='unavailable-id'&&(intento||0)<4){try{peer.destroy();}catch(_){}creaSala((intento||0)+1);}else if(M.fase==='off')info('lmpInfo','Error de conexión ('+(e&&e.type||'?')+'). Inténtalo de nuevo.');});
    peer.on('connection',conn=>{
      conn.on('open',()=>{if(M.fase!=='sala'||M.jug.length>=MAXP){try{conn.send({t:'lleno',por:M.fase!=='sala'?'La carrera ya ha empezado. Espera a la siguiente.':'La sala está llena (máximo '+MAXP+').'});}catch(e){}setTimeout(()=>{try{conn.close();}catch(e){}},400);return;}
        M.jug.push({nom:'Piloto '+(M.jug.length+1),listo:false,conn,veh:'rayo'});difunde();});
      conn.on('data',m=>anfRecibe(conn,m));
      conn.on('close',()=>{const i=M.jug.findIndex(j=>j.conn===conn);if(i>=0)seVa(i);});
    });
  });
}
function unirse(){
  const code=($q('lmpCodIn').value||'').trim().toUpperCase();if(code.length!==4){info('lmpInfo','Escribe el código de 4 letras.');return;}
  info('lmpInfo','Conectando…');
  cargaPeer(ok=>{
    if(!ok){info('lmpInfo','No se ha podido cargar el modo online. Revisa la conexión.');return;}
    let peer;try{peer=new Peer(window.LOOP_PEER_OPTS||{});}catch(e){info('lmpInfo','Error de conexión.');return;}
    M.peer=peer;let hecho=false;const falla=t=>{if(hecho)return;hecho=true;info('lmpInfo',t);try{peer.destroy();}catch(_){}};
    const to=setTimeout(()=>falla('No se encuentra la sala. Revisa el código (o puede que tu red bloquee la conexión).'),22000);
    peer.on('error',e=>{if(!M.on)falla(e&&e.type==='peer-unavailable'?'No existe esa sala. Revisa el código.':'Error de conexión ('+(e&&e.type||'?')+').');});
    peer.on('open',()=>{const conn=peer.connect(PREFIX+code,{reliable:true});M.conn=conn;M.code=code;M.veh=A().SV.veh;
      conn.on('data',recibe);conn.on('close',pierdeAnf);
      conn.on('open',()=>{clearTimeout(to);hecho=true;M.on=true;M.host=false;info('lmpInfo','¡Conectado! Entrando en la sala…');setTimeout(()=>{M.listo=false;elige();},300);});});
  });
}
function pierdeAnf(){if(!M.on)return;const jugando=M.fase==='juego';M.on=false;M.fase='off';clearInterval(M.envT);hud.hidden=true;paraFantasmas();
  if(jugando)return;abre('lmpIni');info('lmpInfo','Se ha cerrado la sala. Crea una nueva o únete con otro código.');}
function sal(){M.on=false;M.host=false;M.fase='off';clearInterval(M.envT);hud.hidden=true;paraFantasmas();
  try{if(M.conn)M.conn.close();}catch(e){}M.jug.forEach(j=>{try{if(j.conn)j.conn.close();}catch(e){}});try{if(M.peer)M.peer.destroy();}catch(e){}
  M.conn=null;M.peer=null;M.jug=[];cierra();}

$q('lmpCrea').onclick=()=>creaSala(0);
$q('lmpUne').onclick=unirse;
$q('lmpCodIn').addEventListener('keydown',e=>{if(e.key==='Enter')unirse();});
$q('lmpNom').addEventListener('change',()=>{if(M.fase==='sala')elige();});
$q('lmpListo').onclick=()=>{M.listo=!M.listo;elige();pinta();};
$q('lmpEmp').onclick=empieza;
$q('lmpRev').onclick=volver;
$q('lmpSal1').onclick=()=>sal();
$q('lmpSal2').onclick=()=>sal();
$q('lmpSal3').onclick=()=>{sal();try{A().toMenu();}catch(e){}};
conInvita(()=>{SalaInvita.monta($q('lmpCod'),()=>M.code,'Looping Loco','es');SalaInvita.alEntrar(c=>{abre('lmpIni');$q('lmpCodIn').value=c;unirse();},1800);});
try{if(A().st.mode==='menu'&&$q('panel')&&!$q('lmpBtn')&&$q('scr').className.indexOf('show')>=0&&$q('panel').querySelector('h1'))boton($q('panel'));}catch(e){}
window.__loopMP={fin,fuera,sal:()=>sal(),boton,activo:()=>M.fase==='juego'||M.fase==='fin',estado:M};
})();
