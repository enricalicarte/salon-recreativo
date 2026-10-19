(()=>{let mv=null;
function best(){let b=null;
 G.tray.forEach((p,i)=>{if(!p)return;for(let r=0;r<G.s;r++)for(let c=0;c<G.s;c++){if(!canPlace(G.grid,G.s,p.cells,r,c))continue;
  const t=G.grid.map(x=>x.slice());p.cells.forEach(([a,b2])=>t[r+a][c+b2]=9);const f=fullLines(t,G.s);const k=f.rows.length+f.cols.length;
  let adj=0;p.cells.forEach(([a,b2])=>{[[1,0],[-1,0],[0,1],[0,-1]].forEach(([dr,dc])=>{const rr=r+a+dr,cc=c+b2+dc;if(rr<0||cc<0||rr>=G.s||cc>=G.s||t[rr][cc]!==0)adj++})});
  const sc=k*40+adj+p.cells.length*2+Math.random();if(!b||sc>b.sc)b={i,r,c,sc,p};}});return b;}
let wait=0.4,lt=performance.now();
function tick(now){const dt=Math.min(.05,(now-lt)/1000);lt=now;try{
 if(G&&!G.over&&!modalOn){
  if(!mv){wait-=dt;if(wait<=0){const b=best();if(b){const cs=L.cell,p=b.p;
     mv={i:b.i,r:b.r,c:b.c,t:0,x0:W/3*(b.i+.5),y0:L.ty+L.th/2,x1:L.bx+b.c*cs+p.w*cs/2,y1:L.by+b.r*cs+p.h*cs+cs*1.3};drag={i:b.i,x:mv.x0,y:mv.y0};}}}
  else{mv.t+=dt/0.55;const e=mv.t<1?1-Math.pow(1-mv.t,3):1;drag.x=mv.x0+(mv.x1-mv.x0)*e;drag.y=mv.y0+(mv.y1-mv.y0)*e-Math.sin(Math.PI*Math.min(1,mv.t))*40;
   if(mv.t>=1.15){drag=null;place(mv.i,mv.r,mv.c);mv=null;wait=0.25;}}
 }else if(G&&G.over&&modalOn&&!window.__bnR){window.__bnR=1;setTimeout(()=>{window.__bnR=0;startLevel(G.level>=0?G.level:7);closeModal();},300);}
}catch(e){window.__bnerr=String(e)}requestAnimationFrame(tick);}requestAnimationFrame(tick);})()
