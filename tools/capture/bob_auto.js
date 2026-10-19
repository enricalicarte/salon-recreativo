(function(){
 const $=id=>document.getElementById(id),K=(t,c)=>window.dispatchEvent(new KeyboardEvent(t,{code:c,key:c,bubbles:true}));
 let side=0,last=0,hold='';
 const setHold=h=>{if(h===hold)return;if(hold)K('keyup',hold);hold=h;if(h)K('keydown',h);};
 setInterval(()=>{
  const now=performance.now();
  if($('result').classList.contains('show')){setHold('');if(now-last>900){last=now;$('nextBtn').click();}return;}
  if($('final').classList.contains('show')){setHold('');if(now-last>900){last=now;$('againBtn').click();}return;}
  if($('pushw').style.opacity=='1'){ if(now-last>70){last=now;const c=side?'ArrowRight':'ArrowLeft';side^=1;K('keydown',c);setTimeout(()=>K('keyup',c),30);} return;}
  if($('lane').classList.contains('on')){
    const r=parseFloat($('lref').style.left)||50,m=parseFloat($('lme').style.left)||50;
    setHold(m<r-4?'ArrowRight':m>r+4?'ArrowLeft':'');
  } else setHold('');
 },20);
})();
