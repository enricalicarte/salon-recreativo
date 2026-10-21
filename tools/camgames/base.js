/* ===== Base común de los juegos con cámara: lienzo, audio, música, cámara, MediaPipe, recorte del jugador y efectos ===== */
const $=s=>document.querySelector(s);
const cv=$('#stage'),ctx=cv.getContext('2d'),video=$('#cam');
let W=0,H=0,DPR=1;
const onResize=[];
function resize(){
  W=innerWidth;H=innerHeight;
  DPR=Math.min(window.devicePixelRatio||1,W*H>1000000?1.25:2);
  cv.width=Math.round(W*DPR);cv.height=Math.round(H*DPR);cv.style.width=W+'px';cv.style.height=H+'px';
  ctx.setTransform(DPR,0,0,DPR,0,0);
  for(const f of onResize)f();
}
addEventListener('resize',resize);
/* calidad adaptativa: si el dispositivo no llega a ~35 fps se apagan los efectos más caros (?hq la fuerza alta) */
const lerp=(a,b,t)=>a+(b-a)*t;
const HQ=new URLSearchParams(location.search).has('hq');
let lowFx=false,fpsAvg=60,fpsT=0;
function perf(dt,active){if(HQ||lowFx||!active||dt<=0)return;fpsAvg=lerp(fpsAvg,1/dt,.05);fpsT+=dt;if(fpsT>3&&fpsAvg<35){lowFx=true;console.info('Efectos reducidos para ir fluido');}}
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
function rnd(i){const x=Math.sin(i*127.1+311.7)*43758.5453;return x-Math.floor(x);}
function mkCanvas(w,h){const c=document.createElement('canvas');c.width=Math.max(1,Math.round(w));c.height=Math.max(1,Math.round(h));return c;}

/* ---------- audio: efectos y música ---------- */
let ac=null,master=null,noiseBuf=null;
let muted=false;try{muted=localStorage.getItem('camgames-mute')==='1';}catch(e){}
function audio(){
  if(!ac){try{ac=new(window.AudioContext||window.webkitAudioContext)();master=ac.createGain();master.gain.value=muted?0:1;master.connect(ac.destination);
    noiseBuf=ac.createBuffer(1,ac.sampleRate*.5,ac.sampleRate);const d=noiseBuf.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=Math.random()*2-1;}catch(e){}}
  if(ac&&ac.state!=='running'){try{ac.resume();}catch(e){}}
}
/* al volver a la pestaña (o tras una llamada en iOS) se reanudan el audio y el bloqueo de pantalla */
let wakeOn=false;
function wake(){wakeOn=true;try{if(navigator.wakeLock)navigator.wakeLock.request('screen').catch(()=>{});}catch(e){}}
document.addEventListener('visibilitychange',()=>{if(document.visibilityState!=='visible')return;if(ac&&ac.state!=='running'){try{ac.resume();}catch(e){}}if(wakeOn)wake();});
function setMute(m){muted=m;try{localStorage.setItem('camgames-mute',m?'1':'0');}catch(e){}if(master)master.gain.setTargetAtTime(m?0:1,ac.currentTime,.05);const b=$('#snd');if(b)b.innerHTML=m?ICON_OFF:ICON_ON;}
const ICON_ON='<svg viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9z" fill="currentColor"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>';
const ICON_OFF='<svg viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9z" fill="currentColor"/><path d="M16 9l5 6M21 9l-5 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
function tone(f,d=.12,type='sine',vol=.15,slide=0,at=0,dest){
  if(!ac)return;const t=(at||ac.currentTime),o=ac.createOscillator(),g=ac.createGain();
  o.type=type;o.frequency.setValueAtTime(f,t);if(slide)o.frequency.exponentialRampToValueAtTime(Math.max(30,f+slide),t+d);
  g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(vol,t+.005);g.gain.exponentialRampToValueAtTime(.0001,t+d);
  o.connect(g);g.connect(dest||master);o.start(t);o.stop(t+d+.02);
}
function noise(d=.1,vol=.1,hp=4000,at=0,dest){
  if(!ac)return;const t=at||ac.currentTime,s=ac.createBufferSource(),f=ac.createBiquadFilter(),g=ac.createGain();
  s.buffer=noiseBuf;f.type='highpass';f.frequency.value=hp;g.gain.setValueAtTime(vol,t);g.gain.exponentialRampToValueAtTime(.0001,t+d);
  s.connect(f);f.connect(g);g.connect(dest||master);s.start(t);s.stop(t+d+.02);
}
const sfx={
  ok(){tone(660,.1,'triangle',.16);setTimeout(()=>tone(990,.16,'triangle',.16),80);},
  perfect(){[660,880,1320,1760].forEach((f,i)=>setTimeout(()=>tone(f,.18,'triangle',.15),i*70));},
  bad(){tone(160,.5,'sawtooth',.22,-110);noise(.35,.25,300);},
  boom(){tone(90,.6,'sine',.5,-60);noise(.5,.35,150);},
  tick(){tone(1200,.04,'square',.05);},
  whoosh(){if(!ac)return;const t=ac.currentTime,s=ac.createBufferSource(),f=ac.createBiquadFilter(),g=ac.createGain();s.buffer=noiseBuf;f.type='bandpass';f.Q.value=1.2;
    f.frequency.setValueAtTime(400,t);f.frequency.exponentialRampToValueAtTime(3000,t+.35);g.gain.setValueAtTime(.0001,t);g.gain.linearRampToValueAtTime(.3,t+.12);g.gain.exponentialRampToValueAtTime(.0001,t+.45);
    s.connect(f);f.connect(g);g.connect(master);s.start(t);s.stop(t+.5);},
  calib(){tone(520,.1,'triangle');setTimeout(()=>tone(780,.14,'triangle'),80);},
  count(n){tone(n?660:1320,n?.15:.4,'square',.08);}
};
/* música: secuenciador sencillo (bombo, charles, bajo y arpegio) */
const music={g:null,next:0,step:0,bpm:116,prog:[[110,130.8,164.8],[87.3,110,130.8],[130.8,164.8,196],[98,123.5,146.8]],lead:true,
  start(){if(!ac||this.g)return;this.g=ac.createGain();this.g.gain.value=0;this.g.gain.linearRampToValueAtTime(.55,ac.currentTime+1);this.g.connect(master);this.next=ac.currentTime+.1;this.step=0;},
  stop(){if(!this.g)return;const g=this.g;g.gain.setTargetAtTime(0,ac.currentTime,.2);setTimeout(()=>{try{g.disconnect();}catch(e){}},800);this.g=null;},
  tick(){if(!this.g)return;const spb=60/this.bpm/4;if(this.next<ac.currentTime-.5)this.next=ac.currentTime;while(this.next<ac.currentTime+.15){this.play(this.step,this.next);this.next+=spb;this.step++;}},
  play(s,t){const b=s%16,ch=this.prog[Math.floor(s/16)%4],d=this.g;
    if(b%4===0){tone(150,.22,'sine',.5,-110,t,d);}
    if(b%2===1)noise(.04,.06,7000,t,d);
    if(b===4||b===12)noise(.12,.12,1800,t,d);
    if(b%2===0)tone(ch[0]/2,.18,'sawtooth',.09,0,t,d);
    if(this.lead&&b%2===0)tone(ch[(b/2)%3]*4,.12,'triangle',.035,0,t,d);
  }
};

/* ---------- cámara y modelo ---------- */
const MP_BASE='https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.14';
const MODEL='https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task';
let landmarker=null,camOK=false,demo=new URLSearchParams(location.search).has('demo');
async function initCamera(){
  /* en móvil se pide menos resolución: la máscara de recorte se calcula píxel a píxel y así va fluido */
  const small=Math.min(innerWidth,innerHeight)<700||matchMedia('(pointer:coarse)').matches;
  const stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:'user',width:{ideal:small?640:960},height:{ideal:small?360:540}},audio:false});
  video.srcObject=stream;video.muted=true;video.playsInline=true;
  await video.play();
  if(!video.videoWidth)await new Promise(r=>{video.onloadedmetadata=r;if(video.readyState>=1)r();setTimeout(r,3000);});
  camOK=true;
}
async function initModel(){
  const {PoseLandmarker,FilesetResolver}=await import(MP_BASE+'/vision_bundle.mjs');
  const fileset=await FilesetResolver.forVisionTasks(MP_BASE+'/wasm');
  const mk=delegate=>PoseLandmarker.createFromOptions(fileset,{baseOptions:{modelAssetPath:MODEL,delegate},runningMode:'VIDEO',outputSegmentationMasks:true,numPoses:players,minPoseDetectionConfidence:.5,minPosePresenceConfidence:.5,minTrackingConfidence:.5});
  try{landmarker=await mk('GPU');}catch(e){console.warn('GPU no disponible, uso CPU',e);landmarker=await mk('CPU');}
  try{await landmarker.setOptions({numPoses:players});}catch(e){}   /* por si se eligió 2 jugadores mientras cargaba */
}
/* número de jugadores (1 o 2): con dos, el detector busca dos personas y cada una se recorta por su lado */
let players=1;
function setPlayers(n){players=n;bodies=[null,null];body=null;if(landmarker){try{const r=landmarker.setOptions({numPoses:n});if(r&&r.catch)r.catch(()=>{});}catch(e){}}}

/* ---------- recorte de los jugadores y auras de neón ---------- */
const mCvs=[mkCanvas(2,2),mkCanvas(2,2)],mCxs=mCvs.map(c=>c.getContext('2d')),mImgs=[null,null];
const mCv=mkCanvas(2,2),mCx=mCv.getContext('2d');          /* máscara combinada */
const pCv=mkCanvas(2,2),pCx=pCv.getContext('2d');          /* vídeo recortado */
const aCvs=[mkCanvas(2,2),mkCanvas(2,2)],aCxs=aCvs.map(c=>c.getContext('2d'));   /* aura por jugador */
let segOK=false,segAt=0,auraCol='#35f0ff',auraCol2='#ff3d8b',maskSlot=[0,1],auraOn=[false,false];
function useMask(res){
  const ms=res&&res.segmentationMasks;
  if(!ms||!ms.length)return;
  try{
    const vw=video.videoWidth,vh=video.videoHeight;
    if(pCv.width!==vw||pCv.height!==vh){pCv.width=vw;pCv.height=vh;}
    let w=0,h=0;auraOn=[false,false];
    ms.forEach((m,i)=>{
      const slot=maskSlot[i];if(slot==null||slot<0||slot>1)return;
      w=m.width;h=m.height;const f=m.getAsFloat32Array(),c=mCvs[slot],x=mCxs[slot];
      if(c.width!==w||c.height!==h){c.width=w;c.height=h;mImgs[slot]=x.createImageData(w,h);}
      const u=new Uint32Array(mImgs[slot].data.buffer);
      for(let k=0;k<f.length;k++){const v=f[k];const a=v<.3?0:v>.7?255:((v-.3)*637)|0;u[k]=(a<<24)|0xffffff;}
      x.putImageData(mImgs[slot],0,0);auraOn[slot]=true;
      const ac2=aCvs[slot],ax=aCxs[slot],aw=Math.max(32,w>>2),ah=Math.max(18,h>>2);
      if(ac2.width!==aw||ac2.height!==ah){ac2.width=aw;ac2.height=ah;}
      ax.globalCompositeOperation='copy';ax.filter='blur(3px)';ax.drawImage(c,0,0,aw,ah);ax.filter='none';
      ax.globalCompositeOperation='source-in';ax.fillStyle=slot?auraCol2:auraCol;ax.fillRect(0,0,aw,ah);ax.globalCompositeOperation='source-over';
    });
    if(!w)return;
    if(mCv.width!==w||mCv.height!==h){mCv.width=w;mCv.height=h;}
    mCx.globalCompositeOperation='copy';let first=true;
    for(let k=0;k<2;k++){if(!auraOn[k])continue;mCx.globalCompositeOperation=first?'copy':'lighter';mCx.drawImage(mCvs[k],0,0);first=false;}
    mCx.globalCompositeOperation='source-over';
    pCx.globalCompositeOperation='copy';pCx.drawImage(video,0,0,vw,vh);
    pCx.globalCompositeOperation='destination-in';if(!lowFx)pCx.filter='blur(1.5px)';pCx.drawImage(mCv,0,0,vw,vh);pCx.filter='none';
    pCx.globalCompositeOperation='source-over';
    segOK=true;segAt=performance.now();
  }catch(e){}
  finally{for(const m of ms){try{m.close();}catch(e){}}}
}
function coverMap(){const vw=video.videoWidth||16,vh=video.videoHeight||9,s=Math.max(W/vw,H/vh);return{vw,vh,s,ox:(W-vw*s)/2,oy:(H-vh*s)/2};}
/* dibuja a los jugadores recortados (espejados) con su aura; si no hay máscara, la cámara entera atenuada */
function drawPlayer(now,dim){
  if(!camOK||video.readyState<2)return false;
  const m=coverMap(),cut=segOK&&now-segAt<1500;
  ctx.save();ctx.translate(W,0);ctx.scale(-1,1);
  if(cut){
    ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.75+.2*Math.sin(now/220);
    const g=1.035,cx=m.ox+m.vw*m.s/2,cy=m.oy+m.vh*m.s/2;
    for(let k=0;k<2;k++)if(auraOn[k])ctx.drawImage(aCvs[k],cx-(m.vw*m.s*g)/2,cy-(m.vh*m.s*g)/2,m.vw*m.s*g,m.vh*m.s*g);
    ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;
    ctx.drawImage(pCv,m.ox,m.oy,m.vw*m.s,m.vh*m.s);
  }else ctx.drawImage(video,m.ox,m.oy,m.vw*m.s,m.vh*m.s);
  ctx.restore();
  if(!cut){ctx.fillStyle='rgba(6,6,24,'+dim+')';ctx.fillRect(0,0,W,H);}
  return true;
}

/* ---------- articulaciones: 0 nariz, 1/2 hombros, 3/4 codos, 5/6 muñecas, 7/8 caderas, 9/10 rodillas, 11/12 tobillos (I/D) ---------- */
const KJ=[0,11,12,13,14,15,16,23,24,25,26,27,28];
let bodies=[null,null],body=null,lastVT=-1;
function toScreen(lm,m){return KJ.map(i=>{const l=lm[i];return{x:W-(m.ox+l.x*m.vw*m.s),y:m.oy+l.y*m.vh*m.s,v:Math.min(l.visibility??1,l.presence??1)};});}
function feet(lm,m){return[29,30,31,32].map(i=>{const l=lm[i];return l?{x:W-(m.ox+l.x*m.vw*m.s),y:m.oy+l.y*m.vh*m.s,v:Math.min(l.visibility??1,l.presence??1)}:{x:0,y:0,v:0};});}
function smooth(prev,out,fo){
  if(!prev)return{j:out,f:fo,lost:0};
  prev.lost=0;prev.j=prev.j.map((o,i)=>({x:o.x+(out[i].x-o.x)*.55,y:o.y+(out[i].y-o.y)*.55,v:out[i].v}));
  prev.f=(prev.f||fo).map((o,i)=>({x:o.x+(fo[i].x-o.x)*.8,y:o.y+(fo[i].y-o.y)*.8,v:fo[i].v}));return prev;
}
const hipX=j=>(j[7].x+j[8].x)/2;
function detect(now){
  if(demo||!landmarker||!camOK||video.readyState<2||video.currentTime===lastVT)return;
  lastVT=video.currentTime;
  let res;try{res=landmarker.detectForVideo(video,now);}catch(e){return;}
  const m=coverMap(),lms=(res&&res.landmarks)||[];
  const dets=lms.slice(0,2).map(lm=>({j:toScreen(lm,m),f:feet(lm,m)}));
  /* asignación a jugador 1 (izquierda) / 2 (derecha), siguiendo a cada uno por dónde estaba */
  const slotOf=new Array(dets.length).fill(-1);
  if(players===1){if(dets.length)slotOf[0]=0;}
  else if(dets.length===2){
    const x0=hipX(dets[0].j),x1=hipX(dets[1].j);let swap=x0>x1;
    if(bodies[0]&&bodies[1]){const a=Math.abs(x0-hipX(bodies[0].j))+Math.abs(x1-hipX(bodies[1].j)),b=Math.abs(x1-hipX(bodies[0].j))+Math.abs(x0-hipX(bodies[1].j));swap=b<a;}
    slotOf[0]=swap?1:0;slotOf[1]=swap?0:1;
  }else if(dets.length===1){
    const x=hipX(dets[0].j);let best=-1,bd=W*.3;
    for(let k=0;k<2;k++)if(bodies[k]&&bodies[k].lost<30){const d=Math.abs(x-hipX(bodies[k].j));if(d<bd){bd=d;best=k;}}
    slotOf[0]=best>=0?best:(x<W/2?0:1);
  }
  maskSlot=slotOf;
  useMask(res);
  const seen=[false,false];
  dets.forEach((d,i)=>{const k=slotOf[i];if(k<0)return;bodies[k]=smooth(bodies[k],d.j,d.f);seen[k]=true;});
  for(let k=0;k<2;k++)if(!seen[k]&&bodies[k]&&++bodies[k].lost>20)bodies[k]=null;
  body=bodies[0];
}

/* ---------- efectos: partículas, ondas, textos, destello, temblor ---------- */
let parts=[],rings=[],pops=[],shake=0,flashT=0,flashC='255,255,255';
const glowDot=(()=>{const c=mkCanvas(64,64),g=c.getContext('2d'),r=g.createRadialGradient(32,32,0,32,32,32);r.addColorStop(0,'rgba(255,255,255,1)');r.addColorStop(.25,'rgba(255,255,255,.8)');r.addColorStop(1,'rgba(255,255,255,0)');g.fillStyle=r;g.fillRect(0,0,64,64);return c;})();
const tinted={};
function tintDot(col){if(tinted[col])return tinted[col];const c=mkCanvas(64,64),g=c.getContext('2d');g.drawImage(glowDot,0,0);g.globalCompositeOperation='source-in';g.fillStyle=col;g.fillRect(0,0,64,64);g.globalCompositeOperation='lighter';g.globalAlpha=.6;g.drawImage(glowDot,16,16,32,32);return tinted[col]=c;}
function burst(x,y,cols,n,spd=1,grav=900,size=1){for(let i=0;i<n;i++){const a=Math.random()*6.283,v=(80+Math.random()*360)*spd;parts.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v-120*spd,life:1,dec:1.1+Math.random()*.9,c:cols[i%cols.length],r:(3+Math.random()*6)*size,g:grav,k:Math.random()<.3?'star':'dot',rot:Math.random()*6});}}
function confetti(x,y,n){const C=['#ff3d8b','#35f0ff','#ffd93d','#5dff9a','#b05cff','#ff7a1f'];for(let i=0;i<n;i++){const a=-Math.PI/2+(Math.random()-.5)*2.2,v=300+Math.random()*700;parts.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:1,dec:.35+Math.random()*.3,c:C[i%C.length],r:5+Math.random()*6,g:700,k:'conf',rot:Math.random()*6,vr:(Math.random()-.5)*14});}}
function ring(x,y,col,max,w=8,dur=.5){rings.push({x,y,col,max,w,t:0,dur});}
function pop(x,y,text,col,size=1){pops.push({x:clamp(x,70,W-70),y,t:0,text,col,size});}
function star4(g,r){g.beginPath();for(let i=0;i<8;i++){const a=i*Math.PI/4,d=i%2?r*.32:r;g.lineTo(Math.cos(a)*d,Math.sin(a)*d);}g.closePath();g.fill();}
function drawFx(dt){
  for(const p of parts){p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=p.g*dt;p.vx*=1-dt*.6;p.life-=dt*p.dec;p.rot+=(p.vr||4)*dt;}
  parts=parts.filter(p=>p.life>0&&p.y<H+40);
  ctx.save();
  for(const p of parts){
    const a=Math.min(1,p.life*1.4);ctx.globalAlpha=a;
    if(p.k==='conf'){ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot);ctx.scale(1,Math.cos(p.rot*1.7));ctx.fillStyle=p.c;ctx.fillRect(-p.r,-p.r*.45,p.r*2,p.r*.9);ctx.restore();}
    else if(p.k==='star'){ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot);ctx.fillStyle='#fff';star4(ctx,p.r*1.6);ctx.restore();}
    else{ctx.globalCompositeOperation='lighter';const s=p.r*3*(.5+p.life*.5);ctx.drawImage(tintDot(p.c),p.x-s,p.y-s,s*2,s*2);ctx.globalCompositeOperation='source-over';}
  }
  ctx.globalAlpha=1;
  for(const r of rings){r.t+=dt;}rings=rings.filter(r=>r.t<r.dur);
  for(const r of rings){const k=r.t/r.dur,e=1-Math.pow(1-k,3),w=r.w*(1-k)+1;ctx.strokeStyle=r.col;ctx.beginPath();ctx.arc(r.x,r.y,r.max*e,0,7);
    ctx.globalAlpha=(1-k)*.3;ctx.lineWidth=w*3;ctx.stroke();ctx.globalAlpha=1-k;ctx.lineWidth=w;ctx.stroke();}
  ctx.globalAlpha=1;
  for(const p of pops){p.t+=dt;p.y-=60*dt;}pops=pops.filter(p=>p.t<1);
  ctx.textAlign='center';ctx.textBaseline='middle';
  for(const p of pops){
    const sc=p.t<.12?p.t/.12*1.35:p.t<.25?1.35-(p.t-.12)/.13*.35:1;
    const fs=Math.round(clamp(Math.min(W,H)*.07,26,54)*p.size);
    ctx.save();ctx.translate(p.x,p.y);ctx.scale(sc,sc);ctx.globalAlpha=p.t>.7?1-(p.t-.7)/.3:1;
    ctx.font=fs+'px "Lilita One",system-ui,sans-serif';ctx.lineJoin='round';ctx.lineWidth=fs*.18;ctx.strokeStyle='rgba(20,8,50,.85)';ctx.strokeText(p.text,0,0);
    ctx.fillStyle=p.col;ctx.fillText(p.text,0,0);ctx.restore();
  }
  ctx.restore();
}
let vig=null,vigKey='';
function drawVignette(alpha=1){
  const k=W+'x'+H;if(k!==vigKey){vigKey=k;vig=ctx.createRadialGradient(W/2,H/2,Math.min(W,H)*.35,W/2,H/2,Math.hypot(W,H)*.6);vig.addColorStop(0,'rgba(0,0,10,0)');vig.addColorStop(1,'rgba(0,0,15,.6)');}
  ctx.globalAlpha=alpha;ctx.fillStyle=vig;ctx.fillRect(0,0,W,H);ctx.globalAlpha=1;
}
function drawFlash(dt){if(flashT>0){ctx.fillStyle='rgba('+flashC+','+(flashT*.45)+')';ctx.fillRect(0,0,W,H);flashT=Math.max(0,flashT-dt*2.4);}}
function bigText(t){const b=$('#big');if(b.textContent===t)return;b.textContent=t;b.classList.remove('pop');void b.offsetWidth;if(t)b.classList.add('pop');}
let toastTO=0;
function toast(t,cls){const e=$('#toast');e.textContent=t;e.className='on '+(cls||'');clearTimeout(toastTO);toastTO=setTimeout(()=>e.className='',1300);}
function goFS(){const e=document.documentElement,f=e.requestFullscreen||e.webkitRequestFullscreen;if(f&&!document.fullscreenElement){try{const p=f.call(e);if(p&&p.catch)p.catch(()=>{});}catch(x){}}}
