(()=>{const cv=document.getElementById('c');let ph=0,tt=0,lt=performance.now(),down=false,tap=0;
function ev(type,x,y){cv.dispatchEvent(new PointerEvent(type,{clientX:x,clientY:y,isPrimary:true,pointerId:1,bubbles:true,pointerType:'mouse'}));}
function g2s(x,y){const r=cv.getBoundingClientRect(),sc=Math.min(innerWidth/540,innerHeight/1200),ox=(innerWidth-540*sc)/2,oy=(innerHeight-1200*sc)/2;return [ox+x*sc,oy+y*sc];}
function tick(now){const dt=Math.min(.05,(now-lt)/1000);lt=now;tt+=dt;ph+=dt;
 try{const cyc=ph%2.2;
  if(cyc<1.6){const [x,y]=g2s(270+230*Math.sin(tt*7),480+190*(.5+.5*Math.sin(tt*1.7)));if(!down){ev('pointerdown',x,y);down=true}else ev('pointermove',x,y);}
  else{if(down){const [x,y]=g2s(270,560);ev('pointerup',x,y);down=false}tap-=dt;if(tap<=0){tap=.1;const [x,y]=g2s(470,700);ev('pointerdown',x,y);ev('pointerup',x,y);}}
 }catch(e){window.__crerr=String(e)}requestAnimationFrame(tick);}requestAnimationFrame(tick);})()
