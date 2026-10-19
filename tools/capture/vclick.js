(t)=>{t=t.toLowerCase();const all=[...document.querySelectorAll('button,a,[role=button],.btn,li,div,span')];
 const ok=all.filter(e=>{const r=e.getBoundingClientRect();if(r.width<8||r.height<8)return false;
  let n=e;while(n&&n.nodeType==1){const s=getComputedStyle(n);if(s.display=='none'||s.visibility=='hidden'||+s.opacity===0)return false;n=n.parentElement;}
  const tx=(e.innerText||e.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();return tx.includes(t)&&tx.length<t.length+40;});
 if(!ok.length)return null;ok.sort((a,b)=>{const pa=a.matches('button,a,[role=button],.btn')?0:1,pb=b.matches('button,a,[role=button],.btn')?0:1;if(pa!=pb)return pa-pb;return (a.innerText||'').length-(b.innerText||'').length});
 const e=ok[0];e.scrollIntoView({block:'center',inline:'center'});const r=e.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2,(e.innerText||'').trim().slice(0,30)]}