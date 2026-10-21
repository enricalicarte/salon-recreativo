/* ===== Poses, formas del hueco y puntuación ===== */
/* Coordenadas en unidades S (altura nariz→tobillo), origen en el centro de las caderas, y hacia abajo */
const NEUTRAL=[[0,-.55],[-.13,-.40],[.13,-.40],[-.16,-.17],[.16,-.17],[-.17,.04],[.17,.04],[-.07,0],[.07,0],[-.08,.22],[.08,.22],[-.09,.45],[.09,.45]];
const mk=o=>{const p=NEUTRAL.map(a=>a.slice());for(const k in o)p[k]=o[k];return p;};
const POSES=[
  {n:'¡ESTRELLA!',t:1,c:['#3b1fa8','#8a2cff'],j:mk({3:[-.33,-.50],4:[.33,-.50],5:[-.55,-.64],6:[.55,-.64],9:[-.17,.22],10:[.17,.22],11:[-.30,.45],12:[.30,.45]})},
  {n:'AVIÓN',t:1,c:['#0b5a7a','#1fc8e8'],j:mk({3:[-.34,-.40],4:[.34,-.40],5:[-.60,-.40],6:[.60,-.40]})},
  {n:'MANOS ARRIBA',t:1,c:['#7a1f4a','#ff3d8b'],j:mk({3:[-.17,-.62],4:[.17,-.62],5:[-.17,-.88],6:[.17,-.88]})},
  {n:'LA Y',t:1,c:['#1f6a3a','#3ddc84'],j:mk({3:[-.25,-.55],4:[.25,-.55],5:[-.40,-.78],6:[.40,-.78]})},
  {n:'MANOS A LA CABEZA',t:2,c:['#7a4a0b','#ffb300'],j:mk({3:[-.24,-.52],4:[.24,-.52],5:[-.07,-.63],6:[.07,-.63]})},
  {n:'GALLINA',t:2,c:['#4a1f7a','#b05cff'],j:mk({3:[-.36,-.28],4:[.36,-.28],5:[-.21,-.42],6:[.21,-.42]})},
  {n:'BRAZO IZQ. ARRIBA',t:2,c:['#0b3a7a','#3d8bff'],j:mk({3:[-.17,-.62],5:[-.17,-.88]})},
  {n:'BRAZO DER. ARRIBA',t:2,c:['#7a0b2a','#ff5c6c'],j:mk({4:[.17,-.62],6:[.17,-.88]})},
  {n:'GUERRERO',t:2,c:['#5a2a0b','#ff7a1f'],j:mk({3:[-.22,-.56],4:[.22,-.56],5:[-.30,-.80],6:[.30,-.80],9:[-.20,.22],10:[.20,.22],11:[-.34,.45],12:[.34,.45]})},
  {n:'FLAMENCO',t:3,c:['#0b6a6a','#1fe8c8'],j:mk({3:[-.34,-.40],4:[.34,-.40],5:[-.60,-.40],6:[.60,-.40],9:[-.09,.04],11:[-.09,.21]})},
  {n:'SENTADILLA',t:3,c:['#3a3a0b','#d4e81f'],j:mk({0:[0,-.34],1:[-.13,-.20],2:[.13,-.20],3:[-.25,-.02],4:[.25,-.02],5:[-.13,-.14],6:[.13,-.14],7:[-.08,.20],8:[.08,.20],9:[-.27,.33],10:[.27,.33],11:[-.23,.45],12:[.23,.45]})},
  {n:'DIAGONAL',t:3,c:['#6a0b5a','#e81fc8'],j:mk({3:[-.17,-.62],5:[-.17,-.88],4:[.34,-.36],6:[.60,-.30],10:[.17,.22],12:[.30,.45]})}
];
/* hueco con forma de cuerpo: cápsulas para cabeza y extremidades + torso como polígono redondeado.
   pieza: [x1,y1,x2,y2,radio] ; el torso va aparte en .poly */
const SEG=[[1,3,.078],[3,5,.066],[2,4,.078],[4,6,.066],[7,9,.098],[9,11,.078],[8,10,.098],[10,12,.078]];
const WT=[1.5,1,1,1,1,1.5,1.5,1,1,1,1,1.5,1.5];       /* peso por articulación */
const STRICT=[3,4,5,6,9,10,11,12];                       /* además de caber, deben acercarse a su sitio */
const PASS=.88,PERFECT=.97;                              /* umbrales de acierto */
const mid=(a,b)=>({x:(a.x+b.x)/2,y:(a.y+b.y)/2});
const ext=(a,b,k)=>({x:a.x+(a.x-b.x)*k,y:a.y+(a.y-b.y)*k});
function shapes(pts,S){
  const sm=mid(pts[1],pts[2]),hm=mid(pts[7],pts[8]);
  const caps=[[pts[0],pts[0],.125],[pts[0],sm,.06]];
  for(const[a,b,r]of SEG)caps.push([pts[a],pts[b],r]);
  caps.push([pts[5],ext(pts[5],pts[3],.32),.075],[pts[6],ext(pts[6],pts[4],.32),.075]);          /* manos */
  for(const[k,kn]of[[11,9],[12,10]]){const f=pts[k],sgn=f.x<hm.x?-1:1;caps.push([f,{x:f.x+sgn*.06*S,y:f.y+.035*S},.065]);}  /* pies */
  const L=caps.map(([a,b,r])=>[a.x,a.y,b.x,b.y,r*S]);
  /* torso: hombros algo más anchos, cintura y caderas */
  const sL=ext(pts[1],sm,.45),sR=ext(pts[2],sm,.45),hL=ext(pts[7],hm,1.0),hR=ext(pts[8],hm,1.0);
  const wL={x:(sL.x+hL.x)/2+(hm.x-sm.x)*.0+(sm.x-sL.x)*.08,y:(sL.y+hL.y)/2},wR={x:(sR.x+hR.x)/2-(sR.x-sm.x)*.08,y:(sR.y+hR.y)/2};
  L.poly=[sL,sR,wR,hR,hL,wL].map(p=>[p.x,p.y]);L.pr=.045*S;
  return L;
}
function dSeg(px,py,x1,y1,x2,y2){const dx=x2-x1,dy=y2-y1,l=dx*dx+dy*dy;let t=l?((px-x1)*dx+(py-y1)*dy)/l:0;t=Math.max(0,Math.min(1,t));return Math.hypot(px-(x1+t*dx),py-(y1+t*dy));}
function inPoly(px,py,P){let c=false;for(let i=0,j=P.length-1;i<P.length;j=i++){const[xi,yi]=P[i],[xj,yj]=P[j];if((yi>py)!==(yj>py)&&px<(xj-xi)*(py-yi)/(yj-yi)+xi)c=!c;}return c;}
function inShape(px,py,sh,m){
  for(const s of sh)if(dSeg(px,py,s[0],s[1],s[2],s[3])<=s[4]+m)return true;
  const P=sh.poly;if(inPoly(px,py,P))return true;
  for(let i=0,j=P.length-1;i<P.length;j=i++)if(dSeg(px,py,P[i][0],P[i][1],P[j][0],P[j][1])<=sh.pr+m)return true;
  return false;
}
function strokeCap(g,s,w){g.lineWidth=w;g.beginPath();if(s[0]===s[2]&&s[1]===s[3])g.arc(s[0],s[1],w/2,0,7);else{g.moveTo(s[0],s[1]);g.lineTo(s[2],s[3]);}g.stroke();}
function polyPath(g,P){g.beginPath();g.moveTo(P[0][0],P[0][1]);for(let i=1;i<P.length;i++)g.lineTo(P[i][0],P[i][1]);g.closePath();}
/* pinta el cuerpo entero engordado "extra" píxeles (para brillo, borde y recorte) */
function paintBody(g,sh,extra){
  for(const s of sh)strokeCap(g,s,s[4]*2+extra);
  polyPath(g,sh.poly);g.lineWidth=sh.pr*2+extra;g.stroke();g.fill();
}

/* puntuación 0..1 del cuerpo j frente al muro w; rellena w.ok con el acierto por articulación */
function scoreBody(j,w){
  const S=w.S;let got=0,tot=0;w.ok=[];
  for(let i=0;i<13;i++){
    const p=j[i],t=w.pts[i];
    let ok=p.v>.3&&inShape(p.x,p.y,w.sh,.03*S);
    if(ok&&STRICT.includes(i))ok=Math.hypot(p.x-t.x,p.y-t.y)<=.25*S;
    w.ok[i]=ok;tot+=WT[i];if(ok)got+=WT[i];
  }
  return got/tot;
}
/* cuerpo virtual para el modo demo: parte de la postura neutra y va hacia la pose objetivo (blend 0..1) */
function demoBodyAt(now,c,target,blend,bad,seed){
  seed=seed||0;
  return NEUTRAL.map((nj,i)=>{
    let x=nj[0],y=nj[1];
    if(target){x+=(target[i][0]-x)*blend;y+=(target[i][1]-y)*blend;if(bad&&STRICT.includes(i)){x+=.25*blend*(i%2?1:-1);y-=.1*blend;}}
    x+=Math.sin(now/310+i*1.7+seed)*.012;y+=Math.cos(now/270+i*2.3+seed)*.012;
    return{x:c.cx+x*c.S,y:c.cy+y*c.S,v:1};
  });
}
/* poses en pareja: [cuerpo izquierdo, cuerpo derecho] y separación entre caderas (en unidades S) */
const PAIRS=[
  {n:'¡CORAZÓN!',c:['#7a1f4a','#ff3d8b'],gap:1.1,j:[mk({3:[-.06,-.82],5:[.42,-1.0],4:[.3,-.15],6:[.5,.1]}),mk({4:[.06,-.82],6:[-.42,-1.0],3:[-.3,-.15],5:[-.5,.1]})]},
  {n:'PUENTE',c:['#0b5a7a','#1fc8e8'],gap:1.1,j:[mk({4:[.3,-.75],6:[.55,-1.0],3:[-.2,-.2],5:[-.25,.02]}),mk({3:[-.3,-.75],5:[-.55,-1.0],4:[.2,-.2],6:[.25,.02]})]},
  {n:'¡CHOCA ESOS CINCO!',c:['#1f6a3a','#3ddc84'],gap:1.15,j:[mk({4:[.32,-.42],6:[.57,-.44],3:[-.2,-.3],5:[-.12,-.12]}),mk({3:[-.32,-.42],5:[-.57,-.44],4:[.2,-.3],6:[.12,-.12]})]},
  {n:'ESTRELLA DOBLE',c:['#3b1fa8','#8a2cff'],gap:1.35,j:[POSES[0].j,POSES[0].j]},
  {n:'LA Y A DÚO',c:['#7a4a0b','#ffb300'],gap:1.0,j:[POSES[3].j,POSES[3].j]},
  {n:'TECHITO',c:['#4a1f7a','#b05cff'],gap:1.0,j:[mk({4:[.3,-.7],6:[.5,-.95],3:[-.3,-.7],5:[-.5,-.95]}),mk({4:[.3,-.7],6:[.5,-.95],3:[-.3,-.7],5:[-.5,-.95]})]}
];
