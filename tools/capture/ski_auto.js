(function(){
 const $=id=>document.getElementById(id),K=(t,c)=>window.dispatchEvent(new KeyboardEvent(t,{code:c,key:c===' '?' ':c,bubbles:true}));
 const tap=c=>{K('keydown',c);setTimeout(()=>K('keyup',c),60);};
 let flipOn=false,twOn=false,last=0;
 setInterval(()=>{
  const now=performance.now();
  if($('result').classList.contains('show')){if(now-last>900){last=now;$('nextBtn').click();}return;}
  if($('final').classList.contains('show')){if(now-last>900){last=now;$('againBtn').click();}return;}
  const pr=$('prompt').textContent||'';
  if(/lanzarte/.test(pr)&&now-last>500){last=now;tap('Space');return;}
  const tm=$('timing');
  if(tm&&tm.style.opacity=='1'){const l=parseFloat($('tmark').style.left)||0;if(l>=83&&now-last>300){last=now;tap('Space');}}
  if(/AHORA/.test(pr)&&now-last>300){last=now;tap('Space');}
  const cF=$('cF');
  if(cF&&cF.style.opacity=='1'){
    const v=parseFloat((cF.querySelector('b')||{}).textContent?.replace(',','.')||'0'),tg=parseFloat((cF.querySelector('b').textContent.split('/')[1]||'1'));
    const want=v<tg-0.12;
    if(want&&!flipOn){flipOn=true;K('keydown','KeyZ');}
    if(!want&&flipOn){flipOn=false;K('keyup','KeyZ');}
    const cT=$('cT'),b2=cT&&cT.querySelector('b');
    if(b2){const v2=parseFloat(b2.textContent.replace(',','.'))||0,t2=parseFloat(b2.textContent.split('/')[1]||'0');const w2=v2<t2-0.12;
      if(w2&&!twOn){twOn=true;K('keydown','KeyX');} if(!w2&&twOn){twOn=false;K('keyup','KeyX');}}
  } else if(flipOn||twOn){flipOn=twOn=false;K('keyup','KeyZ');K('keyup','KeyX');}
 },20);
})();
