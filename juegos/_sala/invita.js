/* Invitar a una sala multijugador: WhatsApp con el código y un enlace que entra directo en la sala.
   SalaInvita.monta(elemento, ()=>código, 'Nombre del juego', 'es'|'ca') pone los botones debajo del código.
   SalaInvita.alEntrar(fn) llama a fn(código) si la página se abrió con ?sala=XXXX. */
(function(){
'use strict';
if(window.SalaInvita)return;
const css=document.createElement('style');css.textContent=
'.sinv{display:flex!important;gap:8px!important;justify-content:center!important;flex-wrap:wrap!important;margin:6px 0 10px!important}'+
'.sinv button{font:700 14px/1.1 system-ui,-apple-system,"Segoe UI",sans-serif!important;letter-spacing:0!important;text-transform:none!important;border-radius:999px!important;padding:9px 16px!important;margin:0!important;cursor:pointer!important;box-shadow:0 3px 0 rgba(0,0,0,.25)!important;text-shadow:none!important;-webkit-text-stroke:0!important;min-height:0!important;width:auto!important;height:auto!important;flex:0 0 auto!important;transform:none!important}'+
'.sinv .sinv-wa{background:#25D366!important;color:#fff!important;border:2px solid rgba(255,255,255,.6)!important}'+
'.sinv .sinv-cp{background:rgba(255,255,255,.14)!important;color:#fff!important;border:1.5px solid rgba(255,255,255,.45)!important}'+
'.sinv[hidden]{display:none!important}';
document.head.appendChild(css);
function url(code){const u=new URL(location.href);u.hash='';u.search='';u.searchParams.set('sala',code);return u.toString();}
function texto(code,juego,ca){return (ca?'Uneix-te a la meva sala de '+juego+'! Codi: '+code:'¡Únete a mi sala de '+juego+'! Código: '+code)+'\n'+url(code);}
function abre(href){try{const w=window.open(href,'_blank');if(!w)location.href=href;}catch(e){location.href=href;}}
window.SalaInvita={
  url,
  codigo(){const q=new URLSearchParams(location.search).get('sala');return q&&/^[A-Za-z]{4}$/.test(q)?q.toUpperCase():null;},
  monta(el,getCode,juego,lang){
    if(!el||el.parentNode.querySelector('.sinv'))return;const ca=lang==='ca';
    const d=document.createElement('div');d.className='sinv';
    d.innerHTML='<button type="button" class="sinv-wa">'+(ca?'📲 Convida per WhatsApp':'📲 Invitar por WhatsApp')+'</button><button type="button" class="sinv-cp">'+(ca?'🔗 Copia l\'enllaç':'🔗 Copiar enlace')+'</button>';
    el.parentNode.insertBefore(d,el.nextSibling);
    const sync=()=>{const c=getCode();d.hidden=!c||!/^[A-Z]{4}$/.test(c);};sync();setInterval(sync,700);
    d.querySelector('.sinv-wa').addEventListener('click',e=>{e.stopPropagation();const c=getCode();if(c)abre('https://wa.me/?text='+encodeURIComponent(texto(c,juego,ca)));});
    d.querySelector('.sinv-cp').addEventListener('click',e=>{e.stopPropagation();const c=getCode();if(!c)return;const b=e.currentTarget,t=b.textContent,ok=()=>{b.textContent=ca?'✓ Copiat!':'✓ ¡Copiado!';setTimeout(()=>b.textContent=t,1600);};
      const txt=texto(c,juego,ca);
      if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(txt).then(ok,()=>{prompt('',txt);});else{prompt('',txt);}});
  },
  alEntrar(fn,espera){const c=this.codigo();if(c)setTimeout(()=>fn(c),espera||1200);}
};
})();
