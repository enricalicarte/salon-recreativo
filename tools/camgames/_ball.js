/* ---------- balón de fútbol (sprite con pentágonos, cacheado por tamaño) ---------- */
const ballCache={};
function ballSprite(R,gold){
  R=Math.max(6,Math.round(R/2)*2);const k=R+(gold?'g':'')+'|'+DPR;if(ballCache[k])return ballCache[k];
  const D=R*2+8,c=mkCanvas(D*DPR,D*DPR),g=c.getContext('2d');g.scale(DPR,DPR);g.translate(D/2,D/2);
  const bg=g.createRadialGradient(-R*.35,-R*.4,R*.1,0,0,R);
  if(gold){bg.addColorStop(0,'#fffbe0');bg.addColorStop(.6,'#ffd84a');bg.addColorStop(1,'#d18a00');}else{bg.addColorStop(0,'#ffffff');bg.addColorStop(.7,'#e9edf5');bg.addColorStop(1,'#a9b2c4');}
  g.beginPath();g.arc(0,0,R,0,7);g.fillStyle=bg;g.fill();
  g.save();g.clip();
  const pent=(cx,cy,r,rot)=>{g.beginPath();for(let i=0;i<5;i++){const a=rot+i*Math.PI*2/5;g.lineTo(cx+Math.cos(a)*r,cy+Math.sin(a)*r);}g.closePath();g.fill();};
  g.fillStyle=gold?'#7a4a00':'#1d1f2b';pent(0,0,R*.36,-Math.PI/2);
  for(let i=0;i<5;i++){const a=-Math.PI/2+i*Math.PI*2/5+Math.PI/5;pent(Math.cos(a)*R*.92,Math.sin(a)*R*.92,R*.33,a);}
  g.strokeStyle=gold?'rgba(122,74,0,.6)':'rgba(29,31,43,.55)';g.lineWidth=Math.max(1,R*.05);
  for(let i=0;i<5;i++){const a=-Math.PI/2+i*Math.PI*2/5;g.beginPath();g.moveTo(Math.cos(a)*R*.36,Math.sin(a)*R*.36);g.lineTo(Math.cos(a)*R*.62,Math.sin(a)*R*.62);g.stroke();}
  g.restore();
  g.lineWidth=Math.max(1.5,R*.06);g.strokeStyle='rgba(20,10,40,.7)';g.beginPath();g.arc(0,0,R,0,7);g.stroke();
  g.fillStyle='rgba(255,255,255,.6)';g.beginPath();g.ellipse(-R*.38,-R*.45,R*.32,R*.15,-.6,0,7);g.fill();
  return ballCache[k]={c,D};
}
function drawBall(x,y,R,rot,gold){
  const s=ballSprite(R,gold),f=R/(Math.max(6,Math.round(R/2)*2));
  ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.scale(f,f);ctx.drawImage(s.c,-s.D/2,-s.D/2,s.D,s.D);ctx.restore();
}
/* guantes de portero sobre las manos */
function drawGlove(x,y,r,ang,col){
  ctx.save();ctx.translate(x,y);ctx.rotate(ang);const s=r/40;ctx.scale(s,s);
  ctx.lineJoin='round';ctx.lineWidth=4;ctx.strokeStyle='#120a30';
  const fing=[[-21,-30,11,30],[-7,-36,11,34],[7,-35,11,33],[20,-29,10,28]];
  for(const[fx,fy,fw,fh]of fing){ctx.fillStyle=col;ctx.beginPath();ctx.roundRect?ctx.roundRect(fx-fw/2,fy-fh/2,fw,fh,fw/2):ctx.rect(fx-fw/2,fy-fh/2,fw,fh);ctx.fill();ctx.stroke();}
  ctx.fillStyle=col;ctx.beginPath();ctx.roundRect?ctx.roundRect(-28,-22,56,48,16):ctx.rect(-28,-22,56,48);ctx.fill();ctx.stroke();
  ctx.save();ctx.translate(-30,6);ctx.rotate(-.7);ctx.beginPath();ctx.roundRect?ctx.roundRect(-7,-16,14,30,7):ctx.rect(-7,-16,14,30);ctx.fill();ctx.stroke();ctx.restore();
  ctx.fillStyle='#120a30';ctx.fillRect(-26,20,52,12);ctx.fillStyle='#fff';ctx.fillRect(-26,22,52,4);
  ctx.fillStyle='rgba(255,255,255,.35)';ctx.beginPath();ctx.ellipse(-8,-8,14,6,-.4,0,7);ctx.fill();
  ctx.restore();
}
