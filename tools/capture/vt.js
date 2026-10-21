(()=>{let vt=0;const q=[];let id=1;const realNow=performance.now.bind(performance);const t0=Date.now();
let on=false;const rRAF=window.requestAnimationFrame.bind(window);
window.__vt={start(){on=true;vt=realNow();},step(ms){vt+=ms;const cbs=q.splice(0);for(const [i,cb] of cbs){try{cb(vt)}catch(e){}}return cbs.length;},on(){return on}};
performance.now=()=>on?vt:realNow();
const RD=Date;window.Date=class extends RD{constructor(...a){if(a.length)super(...a);else super(on?t0+vt:RD.now())}static now(){return on?t0+vt:RD.now()}};
window.requestAnimationFrame=cb=>{if(!on)return rRAF(t=>cb(on?vt:t));const i=id++;q.push([i,cb]);return i};
const rC=window.cancelAnimationFrame.bind(window);window.cancelAnimationFrame=i=>{const k=q.findIndex(x=>x[0]===i);if(k>=0)q.splice(k,1);else rC(i)};
})();
