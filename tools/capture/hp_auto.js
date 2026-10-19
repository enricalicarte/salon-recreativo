(()=>{const H=window.__hp,S=H.S,IN=H.IN;const st={};
function key(c,on){if(!!st[c]===on)return;st[c]=on;dispatchEvent(new KeyboardEvent(on?'keydown':'keyup',{code:c,key:c,bubbles:true}));}
let k=0,lastAir=false,did=false,gr=false;const T=['kick','heel','shuv','tre'];
function tick(){try{
 if(S.state==='ground'){key('ArrowRight',S.u>=0);key('ArrowLeft',S.u<0);key('KeyG',false);lastAir=false;}
 else if(S.state==='air'){key('ArrowRight',false);key('ArrowLeft',false);
  if(!lastAir){lastAir=true;did=false;gr=(k%2==1);k++;}
  if(!did&&S.airT>0.12&&S.vy>0){if(gr)key('KeyG',true);else IN.trick=T[(k>>1)%T.length];did=true;}
  if(gr&&S.vy<-2)key('KeyG',false);}
}catch(e){window.__hperr=String(e);}requestAnimationFrame(tick);}tick();})()
