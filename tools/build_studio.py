"""Alica Studio: portada (index.html) y Alica Play (play/), la plataforma de series.

Se ejecuta desde build_seo.py (usa sus funciones head(), e(), play, BASE...).
El catálogo de series está en tools/series.json. Las ilustraciones de las series se generan con
tools/series_art.py (salen en play/img/).
"""
import json, os, re

SER = json.load(open(os.path.join(root, 'tools/series.json'), encoding='utf-8'))
SERIES = SER['series']
SERIES_SLUGS[:] = [s['slug'] for s in SERIES]
_src = open(os.path.join(root, 'tools/source.html'), encoding='utf-8').read()
_feat = re.findall(r"'([a-z_0-9]+)'", re.search(r"const FEAT=\[(.*?)\]", _src).group(1))
_byid = {g['id']: g for g in play}
LATEST = [_byid[i] for i in _feat if i in _byid][:12]


def studio_head(title, desc, url, p, img, extra=''):
    h = head('es', title, desc, url, p, img, extra=extra)
    return h.replace('<meta property="og:site_name" content="Salón Recreativo">', '<meta property="og:site_name" content="Alica Studio">').replace(
        '<meta name="apple-mobile-web-app-title" content="Salón">', '<meta name="apple-mobile-web-app-title" content="Alica">')


BASE_CSS = r"""
:root{--bg:#07060f;--ink:#f5f2ff;--mut:#a79fcb;--card:#14102b;--line:rgba(255,255,255,.1);--y:#ffd23f;--p:#ff4fa3;--c:#38e5ff;--hd:'Unbounded',system-ui,sans-serif;--tx:'Onest',system-ui,sans-serif}
*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.5 var(--tx);overflow-x:hidden;-webkit-font-smoothing:antialiased}
a{color:inherit}img{display:block;max-width:100%}button{font:inherit;color:inherit}
.dot{display:inline-block;width:.9em;height:.9em;border-radius:50%;background:conic-gradient(#ffd23f,#ff4fa3,#38e5ff,#ffd23f);position:relative;flex:none}
.dot::after{content:"";position:absolute;inset:28%;border-radius:50%;background:var(--bg)}
.btn{display:inline-flex;align-items:center;gap:.55em;border:0;border-radius:999px;padding:.82em 1.5em;font:700 1rem/1 var(--tx);text-decoration:none;cursor:pointer;transition:transform .2s,background .2s,opacity .2s;white-space:nowrap}
.btn:active{transform:scale(.97)}.btn.w{background:#fff;color:#07060f}.btn.w:hover{background:#e9e6f5}
.btn.g{background:rgba(160,150,200,.28);color:#fff;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}.btn.g:hover{background:rgba(160,150,200,.42)}
.btn.y{background:var(--y);color:#1a1300}
.btn svg{width:1.15em;height:1.15em;fill:currentColor}
.ft{border-top:1px solid var(--line);margin-top:60px;padding:34px 4vw 50px;color:var(--mut);font-size:.9rem}
.ft .in{max-width:1400px;margin:0 auto;display:flex;flex-wrap:wrap;gap:14px 28px;justify-content:space-between;align-items:center}
.ft nav{display:flex;flex-wrap:wrap;gap:8px 20px}.ft a{text-decoration:none}.ft a:hover{color:#fff}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

# ============================ ALICA PLAY ============================
PLAY_CSS = r"""
/* ---- intro ---- */
.intro{position:fixed;inset:0;z-index:100;background:#000;display:grid;place-items:center;transition:opacity .6s .1s,visibility .7s}
.intro.out{opacity:0;visibility:hidden}
.intro .w{display:flex;align-items:center;gap:.35em;font:900 clamp(2.4rem,8vw,5.6rem)/1 var(--hd);letter-spacing:-.03em}
.intro svg{width:1em;height:1em;transform:rotate(-90deg)}
.intro circle{fill:none;stroke-width:9;stroke-linecap:round;stroke-dasharray:252;stroke-dashoffset:252;animation:draw 1s cubic-bezier(.6,0,.2,1) forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.intro .w span{display:inline-block;opacity:0;transform:translateY(.4em);animation:up .5s cubic-bezier(.2,.8,.2,1) forwards}
.intro .w span:nth-child(2){animation-delay:.55s}.intro .w span:nth-child(3){animation-delay:.68s;color:var(--y)}
@keyframes up{to{opacity:1;transform:none}}
/* ---- billboard en capas ---- */
.bb .lay{max-width:none;position:absolute;left:-4%;top:-4%;width:108%;height:108%;object-fit:cover;object-position:70% 45%;will-change:transform;pointer-events:none}
.bb .lay.l0{animation:dr0 22s ease-in-out infinite alternate}.bb .lay.l1{animation:dr1 18s ease-in-out infinite alternate}.bb .lay.l2{animation:dr2 14s ease-in-out infinite alternate}
@keyframes dr0{from{translate:0 0}to{translate:-.8% .4%}}@keyframes dr1{from{translate:0 0}to{translate:-1.4% -.6%}}@keyframes dr2{from{translate:0 0}to{translate:-2.1% .7%}}
.bb .par{position:absolute;inset:0;transition:transform .5s cubic-bezier(.2,.8,.2,1)}
.bb .grn{position:absolute;inset:0;opacity:.22;mix-blend-mode:multiply;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E");pointer-events:none}
.bb .agb{position:absolute;right:0;bottom:max(140px,20vh);z-index:3;background:rgba(40,36,60,.55);border-left:3px solid #ddd;padding:7px 34px 7px 12px;font:600 1rem/1 var(--tx);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)}
.bb .q{font:italic 400 clamp(1.1rem,1.8vw,1.5rem)/1.3 Georgia,'Times New Roman',serif;margin:18px 0 0;color:#fff;text-shadow:0 2px 14px rgba(0,0,0,.7)}
.bb .chip{display:inline-flex;align-items:center;gap:8px;margin-top:14px;font:700 .8rem/1 var(--tx);letter-spacing:.06em;color:#fff;background:#e50914;padding:7px 11px;border-radius:4px;text-transform:uppercase}
/* ---- secciones de la serie ---- */
.shw{max-width:1500px;margin:0 auto;padding:0 4vw}
.shw .hdr{display:flex;align-items:end;justify-content:space-between;gap:16px;margin:0 0 18px}
.shw h2.s{font:900 clamp(1.5rem,2.6vw,2.3rem)/1 var(--hd);letter-spacing:-.02em;margin:0}
.shw .hdr small{color:var(--mut)}
.eps{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:22px;margin-bottom:70px}
.ec{border:0;padding:0;background:none;text-align:left;cursor:pointer;color:#fff;display:flex;flex-direction:column;justify-content:flex-start;align-self:start;font:inherit}
.ec .th{position:relative;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:#000;box-shadow:0 16px 40px rgba(0,0,0,.45);transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s}
.ec:hover .th{transform:translateY(-5px);box-shadow:0 26px 60px rgba(0,0,0,.6)}
.ec .th img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s cubic-bezier(.2,.8,.2,1)}.ec:hover .th img{transform:scale(1.05)}
.ec .th::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.55),rgba(0,0,0,0) 50%)}
.ec .num{position:absolute;left:16px;bottom:8px;z-index:2;font:900 3.4rem/1 var(--hd);color:#fff;-webkit-text-stroke:0;text-shadow:0 4px 20px rgba(0,0,0,.5)}
.ec .pl{position:absolute;inset:0;margin:auto;z-index:2;width:62px;height:62px;border-radius:50%;background:rgba(255,255,255,.92);display:grid;place-items:center;transform:scale(.85);opacity:0;transition:.3s}
.ec .pl svg{width:24px;fill:#07060f;margin-left:4px}.ec:hover .pl,.ec:focus-visible .pl{opacity:1;transform:none}
.ec .bdg{position:absolute;top:12px;left:12px;z-index:2;font:800 .68rem/1 var(--tx);letter-spacing:.08em;text-transform:uppercase;padding:7px 10px;border-radius:999px;background:var(--y);color:#1a1300}
.ec .bdg.r{background:#e50914;color:#fff}
.ec .pb{position:absolute;left:0;right:0;bottom:0;height:4px;background:rgba(255,255,255,.25);z-index:3}.ec .pb i{display:block;height:100%;background:#e50914}
.ec .ti{display:flex;justify-content:space-between;gap:12px;margin:14px 2px 4px;font:700 1.1rem/1.25 var(--tx)}.ec .ti span{color:var(--mut);font-weight:500;white-space:nowrap}
.ec p{margin:0 2px;color:#bdb6d9;font-size:.95rem;line-height:1.5}
.ec.soon .th img{filter:grayscale(.6) brightness(.6)}
.abt{display:grid;grid-template-columns:1.05fr 1fr;gap:6vw;align-items:center;margin:20px 0 40px;padding:70px 0;border-top:1px solid var(--line)}
.col{position:relative;aspect-ratio:1.1}
.col .pc{position:absolute;border-radius:4px;overflow:hidden;box-shadow:0 18px 40px rgba(0,0,0,.55);background:#000}
.col .pc img{width:100%;height:100%;object-fit:cover}
.col .pc:nth-child(1){left:0;top:4%;width:72%;aspect-ratio:16/9;transform:rotate(-4deg)}
.col .pc:nth-child(2){right:0;top:34%;width:58%;aspect-ratio:16/9;transform:rotate(3.5deg)}
.col .pc:nth-child(3){left:10%;bottom:0;width:50%;aspect-ratio:16/9;transform:rotate(-1.5deg)}
.col .tp{position:absolute;width:90px;height:26px;background:rgba(243,230,168,.82);z-index:2}
.abt .ey{font:800 .76rem/1 var(--tx);letter-spacing:.28em;text-transform:uppercase;color:var(--mut);margin:0 0 18px}
.abt blockquote{margin:0 0 22px;font:italic 400 clamp(1.6rem,3vw,2.5rem)/1.2 Georgia,'Times New Roman',serif;color:#f4ecd8}
.abt p{color:#d0c9e6;line-height:1.65;margin:0 0 26px}
.abt dl{display:grid;grid-template-columns:auto 1fr;gap:10px 22px;margin:0;font-size:.95rem}.abt dt{color:var(--mut)}.abt dd{margin:0}
.nokids .kt,.nokids [data-v=peques]{display:none!important}
@media (max-width:800px){
 .bb .lay{object-position:73% 45%}
 .bb .art{overflow:hidden}
 .bb .agb{display:none}.bb .tl{margin-bottom:12px}.shw .hdr small{display:none}.mnav{overflow-x:auto;scrollbar-width:none}.mnav::-webkit-scrollbar{display:none}.bb .q{display:none}.bb .chip{margin-top:10px}
 .eps{grid-template-columns:1fr;gap:26px}
 .abt{grid-template-columns:1fr;padding:50px 0;gap:40px}
 .ec .num{font-size:2.6rem}
}

body.kids{--bg:#110d33;--card:#1d1850}
.hd{position:fixed;inset:0 0 auto;z-index:40;display:flex;align-items:center;gap:26px;padding:calc(10px + env(safe-area-inset-top)) 4vw 10px;background:linear-gradient(rgba(7,6,15,.85),rgba(7,6,15,0));transition:background .3s}
.hd.solid{background:rgba(7,6,15,.96)}body.kids .hd.solid{background:rgba(17,13,51,.97)}
.logo{display:flex;align-items:center;gap:.4em;font:900 1.35rem/1 var(--hd);letter-spacing:-.02em;text-decoration:none;white-space:nowrap}
.logo b{color:var(--y)}.logo small{font:700 .55rem/1 var(--tx);letter-spacing:.2em;color:var(--mut);margin-left:.2em;align-self:flex-end;margin-bottom:.15em}
.nv{display:flex;gap:20px;font-size:.95rem}.nv a{text-decoration:none;color:#d8d3ef;cursor:pointer}.nv a:hover,.nv a.on{color:#fff;font-weight:600}
.hd .sp{flex:1}
.ic{width:40px;height:40px;border-radius:50%;border:0;background:transparent;display:grid;place-items:center;cursor:pointer}.ic:hover{background:rgba(255,255,255,.1)}
.ic svg{width:22px;height:22px;stroke:#fff;fill:none;stroke-width:2;stroke-linecap:round}
.kt{display:flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:999px;padding:5px 12px 5px 6px;background:rgba(0,0,0,.25);cursor:pointer;font:600 .85rem/1 var(--tx)}
.kt i{width:30px;height:18px;border-radius:9px;background:#3a345c;position:relative;transition:background .25s}.kt i::after{content:"";position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;background:#fff;transition:transform .25s}
body.kids .kt i{background:#7cf0c8}body.kids .kt i::after{transform:translateX(12px)}
.out{font-size:.85rem;color:var(--mut);text-decoration:none;white-space:nowrap}.out:hover{color:#fff}
/* billboard */
.bb{position:relative;height:min(92vh,56.25vw + 120px);min-height:560px;overflow:hidden}
.bb .art{position:absolute;inset:0;background-size:cover;background-position:center right;animation:kb 26s ease-in-out infinite alternate;transform-origin:70% 40%}
@keyframes kb{from{transform:scale(1)}to{transform:scale(1.08)}}
.bb::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,6,15,.92) 0,rgba(7,6,15,.55) 32%,rgba(7,6,15,0) 62%),linear-gradient(0deg,var(--bg) 0,rgba(7,6,15,0) 34%);pointer-events:none}
body.kids .bb::after{background:linear-gradient(90deg,rgba(17,13,51,.9) 0,rgba(17,13,51,.5) 32%,rgba(17,13,51,0) 62%),linear-gradient(0deg,var(--bg) 0,rgba(17,13,51,0) 34%)}
.bb .tx{position:absolute;z-index:2;left:4vw;bottom:max(120px,18vh);width:min(560px,44vw)}
.bb .tag{display:inline-flex;align-items:center;gap:.45em;font:800 .78rem/1 var(--tx);letter-spacing:.24em;text-transform:uppercase;color:#fff;margin-bottom:14px}
.bb .tag .dot{width:1.2em;height:1.2em}
.bb .sum{font-size:1.12rem;line-height:1.45;margin:14px 0 22px;text-shadow:0 2px 12px rgba(0,0,0,.6);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.bb .acts{display:flex;gap:12px;flex-wrap:wrap}
.meta{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;font-size:.92rem;color:#ddd8f2}
.meta .nw{color:#7cf0c8;font-weight:800}.meta .age{border:1px solid rgba(255,255,255,.55);padding:1px 7px;border-radius:4px;font-size:.8rem}
.meta .hdq{border:1px solid rgba(255,255,255,.4);border-radius:3px;padding:0 4px;font-size:.7rem;font-weight:700}
/* logotipos de las series (texto) */
.tl{white-space:nowrap;margin:0;font-weight:900;line-height:.92;color:#fff;text-shadow:0 4px 30px rgba(0,0,0,.45)}
.tl.lloguer{padding-bottom:.14em;font:900 clamp(2.6rem,6.2vw,6rem)/.9 Georgia,'Times New Roman',serif;letter-spacing:.02em}
.tl.lloguer span{display:inline-block;background:#f4ecd8;color:#1d1712;padding:.02em .1em .06em;margin:0 .02em;box-shadow:3px 5px 0 rgba(0,0,0,.35);text-shadow:none}
.tl.lloguer span:nth-child(odd){transform:rotate(-3deg)}.tl.lloguer span:nth-child(even){transform:rotate(2.5deg) translateY(.04em)}.tl.lloguer span:nth-child(3){background:#c8452f;color:#f4ecd8}.tl.lloguer span:nth-child(6){background:#2f5b4c;color:#f4ecd8}
.tl.tico{font:900 clamp(3.6rem,9vw,8rem)/.9 var(--hd);letter-spacing:-.03em;color:#ffe27a;text-shadow:0 6px 0 #7c6cff,0 12px 30px rgba(0,0,0,.4)}
.tl.pronto{font:900 clamp(2.2rem,5.4vw,4.6rem)/.95 var(--hd);letter-spacing:-.03em;color:#fff;text-shadow:0 5px 0 #ff4fa3,0 10px 30px rgba(0,0,0,.35)}
.tl.sm.lloguer{font-size:1.05rem}.tl.sm.lloguer span{box-shadow:2px 3px 0 rgba(0,0,0,.35)}.tl.sm.tico{font-size:1.7rem;text-shadow:0 3px 0 #7c6cff}.tl.sm.pronto{font-size:1rem;white-space:normal;text-shadow:0 2px 0 #ff4fa3}
.tl.mid.lloguer{font-size:clamp(2rem,5.4vw,3.4rem)}.tl.mid.tico{font-size:clamp(2.8rem,7vw,4rem)}.tl.mid.pronto{font-size:clamp(1.8rem,4.6vw,2.6rem)}
/* filas */
main{position:relative;z-index:3;margin-top:-90px}
.row{margin:0 0 3.2vw}
.row h2{font:700 clamp(1.05rem,1.6vw,1.45rem)/1.2 var(--tx);margin:0 4vw 10px;display:flex;align-items:baseline;gap:12px}
.row h2 small{font-size:.78rem;color:var(--mut);font-weight:500}
.rail{position:relative}
.trk{display:flex;gap:.55vw;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding:0 4vw;padding:6px 4vw 18px;scrollbar-width:none;overscroll-behavior-x:contain}
.trk::-webkit-scrollbar{display:none}
.cd{flex:0 0 calc((100vw - 8vw - 4*.55vw)/5);scroll-snap-align:start;position:relative;border-radius:8px;overflow:hidden;background:var(--card);cursor:pointer;aspect-ratio:16/9;border:0;padding:0;text-align:left;transition:transform .25s,box-shadow .25s;outline-offset:3px}
.cd img{width:100%;height:100%;object-fit:cover}
.cd .lb{position:absolute;left:10px;right:10px;bottom:9px;z-index:2}
.cd::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.72),rgba(0,0,0,0) 55%)}
.cd .rb{position:absolute;top:0;left:0;z-index:2;font:800 .64rem/1 var(--tx);letter-spacing:.08em;text-transform:uppercase;padding:6px 9px;border-radius:0 0 8px 0;background:#e50914;color:#fff}
.cd .rb.p{background:var(--y);color:#1a1300}.cd .rb.k{background:#7cf0c8;color:#08201a}
.cd .et{font:700 .92rem/1.2 var(--tx);color:#fff;text-shadow:0 1px 6px #000}.cd .et small{display:block;font-weight:500;color:#d6d0ee;font-size:.78rem;margin-top:2px}
.cd .pb{position:absolute;left:0;right:0;bottom:0;height:4px;background:rgba(255,255,255,.25);z-index:3}.cd .pb i{display:block;height:100%;background:#e50914}
.cd.dim img{filter:grayscale(.5) brightness(.65)}
.cd .pl{position:absolute;inset:0;margin:auto;width:46px;height:46px;border-radius:50%;border:2px solid #fff;background:rgba(0,0,0,.45);display:grid;place-items:center;z-index:2;opacity:0;transition:opacity .2s}
.cd .pl svg{width:20px;fill:#fff;margin-left:3px}
.cd:hover .pl,.cd:focus-visible .pl{opacity:1}
.arr{position:absolute;top:6px;bottom:18px;width:4vw;border:0;background:rgba(7,6,15,.55);z-index:4;cursor:pointer;opacity:0;transition:opacity .2s;display:grid;place-items:center}
.arr svg{width:28px;stroke:#fff;stroke-width:3;fill:none}.arr.l{left:0}.arr.r{right:0}
.rail:hover .arr{opacity:1}.arr[hidden]{display:none}
@media (hover:hover) and (pointer:fine){.cd:hover{transform:scale(1.06);box-shadow:0 14px 40px rgba(0,0,0,.6);z-index:5}}
/* vista previa al pasar el ratón */
.pv{position:fixed;z-index:30;width:340px;border-radius:10px;overflow:hidden;background:#181433;box-shadow:0 20px 60px rgba(0,0,0,.75);transform-origin:center top;transform:scale(.7);opacity:0;transition:transform .22s,opacity .22s;pointer-events:none}
body.kids .pv{background:#241e5c}
.pv.on{transform:scale(1);opacity:1;pointer-events:auto}
.pv .im{position:relative;aspect-ratio:16/9}.pv .im img{width:100%;height:100%;object-fit:cover}.pv .im .lb{position:absolute;left:12px;bottom:10px}
.pv .bd{padding:12px 14px 16px}.pv .bt{display:flex;gap:8px;margin-bottom:10px}
.cb{width:38px;height:38px;border-radius:50%;border:2px solid rgba(255,255,255,.55);background:rgba(0,0,0,.2);display:grid;place-items:center;cursor:pointer;flex:none}
.cb:hover{border-color:#fff}.cb svg{width:18px;height:18px;stroke:#fff;fill:none;stroke-width:2.4;stroke-linecap:round}.cb.w{background:#fff;border-color:#fff}.cb.w svg{fill:#07060f;stroke:none;margin-left:2px}
.pv .bt .sp{flex:1}.pv .gn{font-size:.82rem;color:#e6e1f7}.pv .gn i{color:#6d6690;font-style:normal;margin:0 5px}
.pv .meta{font-size:.82rem;margin-bottom:6px}
/* ficha */
.md{position:fixed;inset:0;z-index:50;background:rgba(0,0,0,.72);overflow-y:auto;opacity:0;pointer-events:none;transition:opacity .25s;overscroll-behavior:contain}
.md.on{opacity:1;pointer-events:auto}
.md .bx{position:relative;width:min(920px,100%);margin:4vh auto;background:#141029;border-radius:12px;overflow:hidden;transform:translateY(30px) scale(.97);transition:transform .3s;box-shadow:0 30px 90px rgba(0,0,0,.8)}
body.kids .md .bx{background:#1c174a}
.md.on .bx{transform:none}
.md .hero{position:relative;aspect-ratio:16/9;max-height:62vh;width:100%}
.md .hero img{width:100%;height:100%;object-fit:cover}
.md .hero::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,#141029 0,rgba(20,16,41,0) 50%)}
body.kids .md .hero::after{background:linear-gradient(0deg,#1c174a 0,rgba(28,23,74,0) 50%)}
.md .hero .tx{position:absolute;left:5%;bottom:8%;z-index:2;right:5%}
.md .hero .acts{display:flex;gap:10px;margin-top:18px;align-items:center}
.md .x{position:absolute;top:14px;right:14px;z-index:5;width:40px;height:40px;border-radius:50%;border:0;background:#141029;cursor:pointer;display:grid;place-items:center}
.md .x svg{width:20px;stroke:#fff;stroke-width:2.5}
.md .bd{padding:4px 5% 36px}
.md .two{display:grid;grid-template-columns:2fr 1fr;gap:30px;margin-bottom:26px}
.md .two p{margin:10px 0 0;line-height:1.55}.md .side{font-size:.88rem;color:var(--mut)}.md .side p{margin:0 0 10px}.md .side b{color:#ddd7f3;font-weight:500}
.md h3{font:700 1.3rem/1.2 var(--tx);margin:28px 0 12px;display:flex;justify-content:space-between;align-items:center}
.md h3 small{font-size:.9rem;font-weight:500;color:var(--mut)}
.ep{display:grid;grid-template-columns:28px 150px 1fr;gap:16px;align-items:center;padding:16px 14px;border-bottom:1px solid var(--line);border-radius:6px;cursor:pointer}
.ep:first-of-type{background:rgba(255,255,255,.06)}.ep:hover{background:rgba(255,255,255,.09)}
.ep .n{font-size:1.4rem;color:var(--mut);text-align:center}
.ep .th{position:relative;aspect-ratio:16/9;border-radius:5px;overflow:hidden;background:#000}.ep .th img{width:100%;height:100%;object-fit:cover}
.ep .th .pl{position:absolute;inset:0;margin:auto;width:36px;height:36px;border-radius:50%;border:2px solid #fff;background:rgba(0,0,0,.4);display:grid;place-items:center;opacity:0;transition:opacity .2s}.ep:hover .th .pl{opacity:1}.ep .th .pl svg{width:15px;fill:#fff;margin-left:2px}
.ep .th .pb{position:absolute;left:0;right:0;bottom:0;height:3px;background:rgba(255,255,255,.3)}.ep .th .pb i{display:block;height:100%;background:#e50914}
.ep .t{display:flex;justify-content:space-between;gap:10px;font-weight:700}.ep .t span{font-weight:500;color:#ddd;white-space:nowrap}
.ep p{margin:6px 0 0;font-size:.9rem;color:#bdb6d9;line-height:1.45}
.ep .t .soonb{color:#1a1300;white-space:nowrap;align-self:flex-start;font-weight:800}.ep.soon{opacity:.62}.ep .soonb{display:inline-block;font:800 .66rem/1 var(--tx);letter-spacing:.08em;text-transform:uppercase;background:var(--y);color:#1a1300;padding:4px 7px;border-radius:4px;margin-left:8px;vertical-align:middle}
.sim{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.sim .cd{flex:none;width:auto}
/* buscador */
.sr{position:fixed;inset:0;z-index:45;background:var(--bg);overflow-y:auto;padding:calc(84px + env(safe-area-inset-top)) 4vw 40px;display:none}
.sr.on{display:block}
.sr input{width:100%;font:600 1.5rem/1.2 var(--tx);color:#fff;background:transparent;border:0;border-bottom:2px solid var(--line);padding:10px 0;outline:0}
.sr input:focus{border-color:var(--y)}
.sr .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:24px}.sr .grid .cd{flex:none;width:auto}
.sr .emp{color:var(--mut);margin-top:24px}
/* reproductor */
.pl-o{position:fixed;inset:0;z-index:80;background:#000;display:none;align-items:center;justify-content:center}
.pl-o.on{display:flex}
.pl-o .fr{position:relative;width:100%;height:100%}
.pl-o.vert .fr{height:100%;width:auto;aspect-ratio:9/16;max-width:100%}
.pl-o .fr>div,.pl-o iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.pl-o .bar{position:absolute;top:0;left:0;right:0;z-index:3;display:flex;align-items:center;gap:14px;padding:calc(10px + env(safe-area-inset-top)) 16px 30px 0;background:linear-gradient(rgba(0,0,0,.7),rgba(0,0,0,0));pointer-events:none;transition:opacity .4s}
.pl-o .bar .ti{font:600 1rem/1.25 var(--tx);text-shadow:0 1px 6px #000}.pl-o .bar .ti small{display:block;color:#ccc;font-weight:500;font-size:.82rem}
.pl-o.idle .bar{opacity:0}
.xb{pointer-events:auto;display:flex;align-items:center;gap:6px;padding:8px 14px 8px 10px;border:0;border-radius:0 22px 22px 0;background:#fff;color:#07060f;box-shadow:0 8px 24px rgba(0,0,0,.45);cursor:pointer;font:700 1.3rem/1 var(--tx);transition:transform .35s cubic-bezier(.2,.8,.2,1),opacity .35s}
.xb i{width:30px;height:30px;border-radius:50%;background:conic-gradient(#ffd23f,#ff4fa3,#38e5ff,#ffd23f);display:grid;place-items:center}.xb i::after{content:"";width:13px;height:13px;border-radius:50%;background:#07060f}
.xb.tuck{transform:translateX(calc(-100% + 9px));opacity:.6}
.nx{position:absolute;right:24px;bottom:84px;z-index:3;display:none}.nx.on{display:inline-flex}
.soonbox{position:absolute;inset:0;display:none;place-items:center;text-align:center;padding:24px;background:center/cover no-repeat}
.soonbox::before{content:"";position:absolute;inset:0;background:rgba(7,6,15,.72)}
.soonbox div{position:relative}.soonbox h2{font:900 clamp(1.6rem,4vw,2.6rem)/1.1 var(--hd);margin:0 0 10px}.soonbox p{color:#d8d2ee;max-width:30em;margin:0 auto 20px}
.pl-o.soon .soonbox{display:grid}
.toast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom));transform:translate(-50%,20px);background:#fff;color:#07060f;font-weight:700;padding:12px 20px;border-radius:999px;z-index:90;opacity:0;transition:.3s;pointer-events:none;max-width:90vw;text-align:center}
.toast.on{opacity:1;transform:translate(-50%,0)}
.mnav{display:none}
@media (max-width:1100px){.cd{flex-basis:calc((100vw - 8vw - 3*.55vw)/4)}}
@media (max-width:800px){
 .nv,.out.d{display:none}.hd{gap:10px}.kt span{display:none}.kt{padding:5px}
 .mnav{display:flex;gap:8px;padding:0 4vw 4px;position:fixed;top:calc(58px + env(safe-area-inset-top));left:0;right:0;z-index:39;transition:transform .3s,opacity .3s}
 .mnav a{border:1px solid rgba(255,255,255,.5);border-radius:999px;padding:6px 14px;font-size:.85rem;text-decoration:none;white-space:nowrap;background:rgba(7,6,15,.3);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
 .mnav a.on{background:#fff;color:#07060f;border-color:#fff}
 .mnav.hide{transform:translateY(-70px);opacity:0}
 .bb{height:auto;min-height:0;padding:calc(118px + env(safe-area-inset-top)) 6vw 0}
 .bb .art{position:relative;inset:auto;aspect-ratio:3/4;border-radius:12px;background-image:var(--v)!important;background-position:center;animation:none;box-shadow:0 16px 50px rgba(0,0,0,.6);border:1px solid rgba(255,255,255,.14)}
 .bb::before{content:"";position:absolute;inset:0;background:var(--v) center/cover;filter:blur(40px) brightness(.45);transform:scale(1.2);z-index:-1}
 .bb{z-index:0;isolation:isolate}
 .bb::after{display:none}
 .bb .tx{left:6vw;right:6vw;bottom:0;width:auto;padding:0 18px 22px;text-align:center;position:absolute;background:linear-gradient(0deg,rgba(7,6,15,.95) 0,rgba(7,6,15,.6) 60%,rgba(7,6,15,0));border-radius:0 0 12px 12px;padding-top:90px}
 .tl.lloguer{font-size:2.3rem}.tl.tico{font-size:3.4rem}.tl.pronto{font-size:1.9rem;white-space:normal}
 .bb .tag{justify-content:center}.bb .meta{justify-content:center}.bb .sum{display:none}.bb .acts{justify-content:center}.bb .acts .btn{flex:1;justify-content:center;padding:.8em 1em}
 main{margin-top:26px}
 .cd{flex-basis:42vw;border-radius:6px}.trk{gap:8px}.arr{display:none}
 .row{margin-bottom:22px}
 .md .bx{margin:0;min-height:100%;border-radius:0}.md .two{grid-template-columns:1fr;gap:6px}
 .ep{grid-template-columns:120px 1fr;gap:12px;padding:12px 4px;align-items:start}.tl.sm.lloguer{font-size:.78rem}.tl.sm.tico{font-size:1.35rem}.ep .n{display:none}.ep .t{flex-direction:column;gap:2px}
 .sim{grid-template-columns:repeat(2,1fr)}
 .pl-o .nx{right:14px;bottom:70px}
}
"""

ICO = {
    'play': '<svg viewBox="0 0 24 24"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12.5-7.5a1 1 0 0 0 0-1.72L8.5 3.64A1 1 0 0 0 7 4.5z"/></svg>',
    'info': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9.5"/><path d="M12 11v6M12 7.2v.1" stroke-linecap="round"/></svg>',
}

PLAY_HTML = r"""<div class="intro" id="intro" aria-hidden="true"><div class="w"><svg viewBox="0 0 100 100"><defs><linearGradient id="ig" x1="0" x2="1"><stop offset="0" stop-color="#ffd23f"/><stop offset=".5" stop-color="#ff4fa3"/><stop offset="1" stop-color="#38e5ff"/></linearGradient></defs><circle cx="50" cy="50" r="40" stroke="url(#ig)"/></svg><span>ALICA</span><span>PLAY</span></div></div>
<a class="skip" href="#cont" style="position:absolute;left:-999px">Saltar al contenido</a>
<header class="hd" id="hd">
 <a class="logo" href="__P__" aria-label="Alica Play, inicio"><span class="dot"></span>ALICA<b>PLAY</b></a>
 <nav class="nv" id="nv"><a data-v="inicio" class="on">Inicio</a><a data-v="series">Series</a><a data-v="peques">Peques</a><a data-v="lista">Mi lista</a></nav>
 <span class="sp"></span>
 <a class="out d" href="__R__salon/">Salón Recreativo ↗</a>
 <button class="ic" id="bSearch" type="button" aria-label="Buscar"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg></button>
 <button class="kt" id="bKids" type="button" aria-pressed="false" title="Modo Peques: solo series infantiles"><i></i><span>Peques</span></button>
</header>
<nav class="mnav" id="mnav"><a data-v="inicio" class="on">Inicio</a><a data-v="series">Series</a><a data-v="peques">Peques</a><a data-v="lista">Mi lista</a></nav>
<section class="bb" id="bb" aria-label="Serie destacada"></section>
<main id="cont"></main>
<footer class="ft"><div class="in"><span><span class="dot" style="vertical-align:-2px"></span> © 2026 <b style="color:#fff">Alica Studio</b> · Series creadas por Enric Alicarte</span>
<nav><a href="__R__">Alica Studio</a><a href="__R__salon/">Salón Recreativo</a><a href="__R__estudio/">El estudio</a><a href="__R__aviso-legal/">Aviso legal</a><a href="__R__privacidad/">Privacidad</a></nav></div></footer>
<div class="pv" id="pv"></div>
<div class="md" id="md" role="dialog" aria-modal="true" aria-label="Ficha de la serie"><div class="bx" id="mdb"></div></div>
<div class="sr" id="sr" role="dialog" aria-label="Buscar"><input id="q" type="search" placeholder="Series, episodios, géneros…" autocomplete="off"><div id="sres"></div></div>
<div class="pl-o" id="plo" aria-label="Reproductor">
 <div class="fr" id="fr"><div id="yt"></div></div>
 <div class="bar"><button class="xb" id="xb" type="button" aria-label="Volver">‹<i></i></button><div class="ti" id="pti"></div></div>
 <button class="btn w nx" id="nx" type="button"></button>
 <div class="soonbox" id="soon"><div><h2>Muy pronto</h2><p id="soonp">Este episodio todavía no está disponible.</p><button class="btn w" type="button" id="soonx">Volver</button></div></div>
</div>
<div class="toast" id="toast"></div>
"""

PLAY_JS = r"""
const D=window.__SER,P=window.__P,OPEN=window.__OPEN||'';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const st={get(k,d){try{const v=localStorage.getItem('ap_'+k);return v?JSON.parse(v):d}catch(e){return d}},set(k,v){try{localStorage.setItem('ap_'+k,JSON.stringify(v))}catch(e){}}};
const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
const IP='<svg viewBox="0 0 24 24"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12.5-7.5a1 1 0 0 0 0-1.72L8.5 3.64A1 1 0 0 0 7 4.5z"/></svg>';
const IINFO='<svg viewBox="0 0 24 24" style="fill:none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9.5"/><path d="M12 11v6M12 7.2v.1" stroke-linecap="round"/></svg>';
const S=D.series,BY={};S.forEach(s=>BY[s.slug]=s);
let kids=st.get('kids',false),view='inicio',list=st.get('list',[]),prog=st.get('prog',{});
const img=(s,k)=>P+'img/'+s.slug+(k?'-'+k:'')+'.jpg';
const eps=s=>{const o=[];(s.temporadas||[]).forEach(t=>t.episodios.forEach(e=>o.push(Object.assign({s:s.slug,t:t.n},e))));return o};
const ekey=e=>e.s+'-'+e.t+'-'+e.n;
const ready=e=>e&&!!e.yt&&e.estado!=='pronto';
const logo=(s,c)=>{if(s.logo==='lloguer')return '<h2 class="tl lloguer '+(c||'')+'">'+[...s.titulo].map(ch=>'<span>'+esc(ch)+'</span>').join('')+'</h2>';
  if(s.logo==='pronto')return '<h2 class="tl pronto '+(c||'')+'">'+esc(s.titulo)+'</h2>';return '<h2 class="tl '+esc(s.logo)+' '+(c||'')+'">'+esc(s.titulo)+'</h2>'};
const ntemp=s=>(s.temporadas||[]).length;
const metaH=(s,full)=>{const n=eps(s).filter(ready).length,m=[];
  if(s.estado==='pronto')m.push('<span class="nw">Próximamente</span>');else m.push('<span class="nw">Nuevo</span>');
  m.push('<span>'+s.anio+'</span>','<span class="age">'+esc(s.edad)+'</span>');
  if(ntemp(s))m.push('<span>'+ntemp(s)+' temporada'+(ntemp(s)>1?'s':'')+'</span>');
  if(full)m.push('<span class="hdq">HD</span>','<span>'+esc(s.idiomas)+'</span>');
  return '<div class="meta">'+m.join('')+'</div>'};
const visible=()=>S.filter(s=>!kids||s.peques);
function toast(t){const x=$('#toast');x.textContent=t;x.classList.add('on');clearTimeout(toast.t);toast.t=setTimeout(()=>x.classList.remove('on'),2600)}

/* ---------- billboard ---------- */
function billboard(){
  const s=BY[kids?D.destacada_peques:D.destacada]||visible()[0],bb=$('#bb');
  bb.style.setProperty('--v','url("'+img(s,'v')+'")');
  const E=eps(s),f=E.find(ready)||E[0],pr=f&&prog[ekey(f)];
  const art=s.capas?'<div class="art" role="img" aria-label="'+esc(s.titulo)+'"><div class="par" id="par">'+s.capas.map((c,i)=>'<img class="lay l'+i+'" data-d="'+(i+1)+'" src="'+P+'img/'+c+'" alt="" '+(i?'':'fetchpriority="high"')+'>').join('')+'<div class="grn"></div></div></div>':'<div class="art" style="background-image:url(\''+img(s)+'\')" role="img" aria-label="'+esc(s.titulo)+'"></div>';
  bb.innerHTML=art+'<div class="tx"><div class="tag"><span class="dot"></span>Serie original</div>'+logo(s)+'<p class="q">'+esc(s.gancho)+'</p><p class="sum">'+esc(s.sinopsis)+'</p>'+metaH(s)+(f?'<span class="chip">'+(f.n===1?'Piloto':'Episodio '+f.n)+(f.dur?' · '+esc(f.dur):'')+'</span>':'')+'<div class="acts" style="margin-top:20px"><button class="btn w" data-play="'+s.slug+'" type="button">'+IP+' '+(pr&&pr.t>20?'Reanudar':'Ver')+(f?' T'+f.t+':E'+f.n:'')+'</button><button class="btn g" data-info="'+s.slug+'" type="button">'+IINFO+' Más información</button></div></div><div class="agb">'+esc(s.edad)+'</div>';
  if(!PAR.on)PAR();
}

/* ---------- tarjetas ---------- */
function cardS(s){const p=s.estado==='pronto',n=eps(s).filter(ready).length;
  return '<button class="cd" type="button" data-info="'+s.slug+'" data-pv="s:'+s.slug+'"><img src="'+img(s)+'" alt="" loading="lazy">'+(p?'<span class="rb p">Próximamente</span>':(n?'<span class="rb">Nuevo</span>':'<span class="rb p">Estreno pronto</span>'))+'<div class="lb">'+logo(s,'sm')+'</div></button>'}
function cardE(e,i){const s=BY[e.s],pr=prog[ekey(e)],r=ready(e),soon=e.estado==='pronto';
  return '<button class="cd'+(soon?' dim':'')+'" type="button" data-ep="'+ekey(e)+'" data-pv="e:'+ekey(e)+'">'+thumb(e,s,img(s,(e.n-1)%(s.slug==='lloguer'?3:5)+1))+''+(soon?'<span class="rb p">Próximamente</span>':(!r?'<span class="rb p">Muy pronto</span>':''))+(r?'<span class="pl">'+IP+'</span>':'')+'<div class="lb"><div class="et">'+(e.n?'E'+e.n+' · ':'')+esc(e.titulo)+'<small>'+esc(s.titulo)+(e.dur?' · '+esc(e.dur):'')+'</small></div></div>'+(pr&&pr.d?'<div class="pb"><i style="width:'+Math.min(100,pr.t/pr.d*100).toFixed(1)+'%"></i></div>':'')+'</button>'}
function row(t,inner,sub){if(!inner)return '';return '<section class="row"><h2>'+esc(t)+(sub?' <small>'+esc(sub)+'</small>':'')+'</h2><div class="rail"><button class="arr l" type="button" aria-label="Anterior" hidden><svg viewBox="0 0 24 24"><path d="m15 5-7 7 7 7"/></svg></button><div class="trk">'+inner+'</div><button class="arr r" type="button" aria-label="Siguiente"><svg viewBox="0 0 24 24"><path d="m9 5 7 7-7 7"/></svg></button></div></section>'}
const ICL=on=>'<svg viewBox="0 0 24 24"><path d="'+(on?'M5 12l5 5 9-11':'M12 5v14M5 12h14')+'"/></svg>';
const findE=k=>{for(const s of S)for(const e of eps(s))if(ekey(e)===k)return e;return null};

function render(){
  document.body.classList.toggle('kids',kids);$('#bKids').setAttribute('aria-pressed',kids);
  $$('[data-v]').forEach(a=>a.classList.toggle('on',a.dataset.v===view));
  const vis=visible(),m=$('#cont');let h='';
  const cont=Object.entries(prog).filter(([k,v])=>v.d&&v.t>20&&v.t<v.d*.93).sort((a,b)=>b[1].ts-a[1].ts).map(([k])=>findE(k)).filter(e=>e&&(!kids||BY[e.s].peques));
  if(view==='inicio'&&vis.length===1){h+=showcase(vis[0]);}
  else if(view==='inicio'){
    h+=row('Seguir viendo',cont.map(cardE).join(''));
    h+=row(kids?'Para los peques':'Novedades en Alica Play',vis.map(cardS).join(''));
    vis.filter(s=>eps(s).length).forEach(s=>{h+=row('Episodios de '+s.titulo,eps(s).map(cardE).join(''),'Temporada 1')});
    if(!kids)h+=row('Para los peques',S.filter(s=>s.peques).map(cardS).join(''));
    const pr=vis.filter(s=>s.estado==='pronto');h+=row('Próximamente',pr.map(cardS).join(''));
    const ex=[];vis.forEach(s=>(s.extras||[]).forEach((x,i)=>ex.push(Object.assign({s:s.slug,t:0,n:0,x:i},x))));
    h+=row('Detrás de las cámaras',ex.map(x=>cardX(x)).join(''));
    h+=row('Mi lista',list.filter(k=>BY[k]&&(!kids||BY[k].peques)).map(k=>cardS(BY[k])).join(''));
  }else if(view==='series'){h+=row('Todas las series',vis.map(cardS).join(''));vis.filter(s=>eps(s).length).forEach(s=>{h+=row(s.titulo,eps(s).map(cardE).join(''))})}
  else if(view==='peques'){h+=row('Series para los peques',S.filter(s=>s.peques).map(cardS).join(''));S.filter(s=>s.peques&&eps(s).length).forEach(s=>{h+=row('Episodios de '+s.titulo,eps(s).map(cardE).join(''))})}
  else if(view==='lista'){const l=list.filter(k=>BY[k]&&(!kids||BY[k].peques)).map(k=>cardS(BY[k])).join('');h+=l?row('Mi lista',l):'<section class="row"><h2>Mi lista</h2><p style="margin:0 4vw;color:var(--mut)">Todavía no has añadido nada. Pulsa <b>+</b> en una serie para guardarla aquí.</p></section>';h+=row('Seguir viendo',cont.map(cardE).join(''))}
  m.innerHTML=h;billboard();rails();
}
/* miniatura: fotograma de YouTube si el episodio está publicado; si no, la ilustración */
function thumb(e,s,art){return e.yt?'<img src="https://i.ytimg.com/vi/'+e.yt+'/hqdefault.jpg" alt="" loading="lazy" onerror="this.onerror=null;this.src=\''+art+'\'">':'<img src="'+art+'" alt="" loading="lazy">'}
function ecard(e,s,i){const pr=prog[ekey(e)],r=ready(e),soon=e.estado==='pronto';
  return '<button class="ec'+(soon?' soon':'')+'" type="button" data-ep="'+ekey(e)+'"><div class="th">'+thumb(e,s,img(s,(i%3)+1))+''+(soon?'<span class="bdg">En producción</span>':(r?'<span class="bdg r">Nuevo</span>':'<span class="bdg">Muy pronto</span>'))+'<span class="num">'+e.n+'</span>'+(r?'<span class="pl">'+IP+'</span>':'')+(pr&&pr.d?'<div class="pb"><i style="width:'+Math.min(100,pr.t/pr.d*100).toFixed(1)+'%"></i></div>':'')+'</div><div class="ti">'+esc(e.titulo)+'<span>'+esc(e.dur||'')+'</span></div><p>'+esc(e.sinopsis||'')+'</p></button>'}
function showcase(s){const E=eps(s);let h='<div class="shw">';
  h+='<section id="sec-ep"><div class="hdr"><h2 class="s">Episodios</h2><small>Temporada 1 · '+esc(s.idiomas)+'</small></div><div class="eps">'+E.map((e,i)=>ecard(e,s,i)).join('')+'</div></section>';
  if((s.extras||[]).length)h+='<section id="sec-ex"><div class="hdr"><h2 class="s">Detrás de las cámaras</h2></div><div class="eps">'+s.extras.map((x,i)=>'<button class="ec" type="button" data-ex="'+s.slug+':'+i+'"><div class="th"><img src="'+img(s,3)+'" alt="" loading="lazy">'+(x.yt?'<span class="pl">'+IP+'</span>':'<span class="bdg">Muy pronto</span>')+'</div><div class="ti">'+esc(x.titulo)+'<span>'+esc(x.dur||'')+'</span></div><p>'+esc(x.sinopsis||'')+'</p></button>').join('')+'</div></section>';
  h+='<section class="abt" id="sec-ab"><div class="col" aria-hidden="true"><div class="pc"><img src="'+img(s,1)+'" alt="" loading="lazy"></div><div class="pc"><img src="'+img(s,2)+'" alt="" loading="lazy"></div><div class="pc"><img src="'+img(s,3)+'" alt="" loading="lazy"></div><span class="tp" style="left:30%;top:1%;transform:rotate(-8deg)"></span><span class="tp" style="right:12%;top:31%;transform:rotate(10deg)"></span></div><div><p class="ey">Sobre la serie</p>'+logo(s,'mid')+'<blockquote style="margin-top:22px">«'+esc(s.gancho)+'»</blockquote><p>'+esc(s.sinopsis)+'</p><dl><dt>Creada por</dt><dd>'+esc(s.creador)+'</dd><dt>Estilo</dt><dd>'+esc(s.estilo)+'</dd><dt>Géneros</dt><dd>'+s.generos.map(esc).join(' · ')+'</dd><dt>Idiomas</dt><dd>'+esc(s.idiomas)+'</dd><dt>Edad</dt><dd>'+esc(s.edad_txt||s.edad)+'</dd><dt>Año</dt><dd>'+s.anio+'</dd></dl><div style="display:flex;gap:12px;margin-top:30px;flex-wrap:wrap"><button class="btn w" type="button" data-play="'+s.slug+'">'+IP+' Ver la serie</button><button class="btn g" type="button" data-list="'+s.slug+'">'+(inList(s.slug)?'✓ En Mi lista':'+ Mi lista')+'</button></div></div></section>';
  return h+'</div>'}
/* paralaje del cartel */
function PAR(){PAR.on=1;if(!fine||matchMedia('(prefers-reduced-motion:reduce)').matches)return;let tx=0,ty=0,cx=0,cy=0,raf=0;
  addEventListener('pointermove',e=>{tx=(e.clientX/innerWidth-.5);ty=(e.clientY/innerHeight-.5);if(!raf)raf=requestAnimationFrame(step)},{passive:true});
  function step(){raf=0;cx+=(tx-cx)*.12;cy+=(ty-cy)*.12;document.querySelectorAll('#bb .lay').forEach(l=>{const d=+l.dataset.d;l.style.transform='translate('+(-cx*d*9).toFixed(2)+'px,'+(-cy*d*6).toFixed(2)+'px)'});if(Math.abs(tx-cx)+Math.abs(ty-cy)>.002)raf=requestAnimationFrame(step)}}
function cardX(x){const s=BY[x.s];return '<button class="cd" type="button" data-ex="'+x.s+':'+x.x+'"><img src="'+img(s,((x.x+1)%3)+1)+'" alt="" loading="lazy">'+(x.yt?'<span class="pl">'+IP+'</span>':'<span class="rb p">Muy pronto</span>')+'<div class="lb"><div class="et">'+esc(x.titulo)+'<small>'+esc(s.titulo)+(x.dur?' · '+esc(x.dur):'')+'</small></div></div></button>'}
function rails(){$$('.rail').forEach(r=>{const t=r.querySelector('.trk'),l=r.querySelector('.arr.l'),rr=r.querySelector('.arr.r');
  const up=()=>{l.hidden=t.scrollLeft<8;rr.hidden=t.scrollLeft+t.clientWidth>=t.scrollWidth-8};t.addEventListener('scroll',up,{passive:true});up();
  l.onclick=()=>t.scrollBy({left:-t.clientWidth*.9,behavior:'smooth'});rr.onclick=()=>t.scrollBy({left:t.clientWidth*.9,behavior:'smooth'})})}

/* ---------- vista previa (ratón) ---------- */
let pvT=0,pvFor=null;const pv=$('#pv');
function inList(slug){return list.includes(slug)}
function showPV(card){const [k,id]=card.dataset.pv.split(':');let s,e;
  if(k==='s')s=BY[id];else{e=findE(id);s=BY[e.s]}
  const r=card.getBoundingClientRect(),w=Math.max(300,r.width*1.45);
  let x=r.left+r.width/2-w/2;x=Math.max(12,Math.min(innerWidth-w-12,x));
  pv.style.width=w+'px';pv.style.left=x+'px';pv.style.top=Math.max(70,r.top-r.height*.25)+'px';
  const pi=e?img(s,(e.n-1)%(s.slug==='lloguer'?3:5)+1):img(s);
  pv.innerHTML='<div class="im"><img src="'+pi+'" alt=""><div class="lb">'+logo(s,'sm')+'</div></div><div class="bd"><div class="bt"><button class="cb w" type="button" '+(e?'data-ep="'+ekey(e)+'"':'data-play="'+s.slug+'"')+' aria-label="Ver"><svg viewBox="0 0 24 24"><path d="M7 4.5v15a1 1 0 0 0 1.5.86l12.5-7.5a1 1 0 0 0 0-1.72L8.5 3.64A1 1 0 0 0 7 4.5z"/></svg></button><button class="cb'+(inList(s.slug)?' on':'')+'" type="button" data-list="'+s.slug+'" aria-label="Mi lista">'+ICL(inList(s.slug))+'</button><span class="sp"></span><button class="cb" type="button" data-info="'+s.slug+'" aria-label="Más información"><svg viewBox="0 0 24 24"><path d="m6 9 6 6 6-6"/></svg></button></div>'+(e?'<div class="et" style="font-weight:700;margin-bottom:6px">E'+e.n+' · '+esc(e.titulo)+'</div>':'')+metaH(s)+'<div class="gn">'+s.generos.map(esc).join('<i>•</i>')+'</div></div>';
  pv.classList.add('on');pvFor=card;const ph=pv.offsetHeight;if(parseFloat(pv.style.top)+ph>innerHeight-12)pv.style.top=Math.max(70,innerHeight-ph-12)+'px'}
function hidePV(){pv.classList.remove('on');pvFor=null}
if(fine){document.addEventListener('mouseover',ev=>{const c=ev.target.closest('[data-pv]');if(c&&c!==pvFor&&!c.closest('.md,.sr')){clearTimeout(pvT);pvT=setTimeout(()=>showPV(c),420)}});
  document.addEventListener('mouseout',ev=>{const c=ev.target.closest('[data-pv]');if(c&&!(ev.relatedTarget&&(c.contains(ev.relatedTarget)||pv.contains(ev.relatedTarget))))clearTimeout(pvT)});
  pv.addEventListener('mouseleave',hidePV);addEventListener('scroll',hidePV,{passive:true});
  document.addEventListener('mousemove',ev=>{if(pvFor&&!pv.contains(ev.target)&&!pvFor.contains(ev.target))hidePV()},{passive:true})}

/* ---------- ficha ---------- */
const md=$('#md');let mdSlug=null;
function openInfo(slug,push=true){const s=BY[slug];if(!s)return;hidePV();mdSlug=slug;
  const E=eps(s),first=E.find(ready);
  let h='<button class="x" type="button" data-close aria-label="Cerrar"><svg viewBox="0 0 24 24"><path d="M5 5l14 14M19 5 5 19"/></svg></button><div class="hero"><img src="'+img(s)+'" alt=""><div class="tx">'+logo(s,'mid')+'<div class="acts">'+(s.estado!=='pronto'?'<button class="btn w" type="button" data-play="'+s.slug+'">'+IP+' '+(first&&prog[ekey(first)]&&prog[ekey(first)].t>20?'Reanudar':'Ver')+'</button>':'<span class="btn y" style="cursor:default">Próximamente</span>')+'<button class="cb'+(inList(s.slug)?' on':'')+'" type="button" data-list="'+s.slug+'" aria-label="Añadir a Mi lista">'+ICL(inList(s.slug))+'</button></div></div></div>';
  h+='<div class="bd"><div class="two"><div>'+metaH(s,true)+'<p style="font-size:1.08rem"><b>'+esc(s.gancho)+'</b></p><p>'+esc(s.sinopsis)+'</p></div><div class="side"><p><b>Creada por:</b> '+esc(s.creador)+'</p><p><b>Géneros:</b> '+s.generos.map(esc).join(', ')+'</p><p><b>Estilo:</b> '+esc(s.estilo)+'</p><p><b>Edad:</b> '+esc(s.edad_txt||s.edad)+'</p><p><b>Idiomas:</b> '+esc(s.idiomas)+'</p></div></div>';
  if(E.length){h+='<h3>Episodios <small>Temporada 1</small></h3>'+E.map(e=>{const pr=prog[ekey(e)],soon=e.estado==='pronto';
    return '<div class="ep'+(soon?' soon':'')+'" role="button" tabindex="0" data-ep="'+ekey(e)+'"><div class="n">'+e.n+'</div><div class="th">'+thumb(e,s,img(s,(e.n-1)%(s.slug==='lloguer'?3:5)+1))+''+(ready(e)?'<span class="pl">'+IP+'</span>':'')+(pr&&pr.d?'<div class="pb"><i style="width:'+Math.min(100,pr.t/pr.d*100).toFixed(1)+'%"></i></div>':'')+'</div><div><div class="t">'+esc(e.titulo)+(soon?'<span class="soonb">Próximamente</span>':(!ready(e)?'<span class="soonb">Muy pronto</span>':''))+'<span>'+esc(e.dur||'')+'</span></div><p>'+esc(e.sinopsis||'')+'</p></div></div>'}).join('')}
  else h+='<h3>Episodios</h3><p style="color:var(--mut)">Los episodios se anunciarán aquí muy pronto.</p>';
  if((s.extras||[]).length)h+='<h3>Tráiler y más</h3><div class="sim">'+s.extras.map((x,i)=>cardX(Object.assign({s:s.slug,x:i},x))).join('')+'</div>';
  const sim=visible().filter(x=>x.slug!==s.slug);if(sim.length)h+='<h3>Más títulos</h3><div class="sim">'+sim.map(cardS).join('')+'</div>';
  h+='</div>';$('#mdb').innerHTML=h;md.classList.add('on');md.scrollTop=0;document.documentElement.style.overflow='hidden';
  if(push)try{history.pushState({md:slug},'',location.pathname.replace(/[^/]*$/,'')+'?s='+slug)}catch(e){}
}
let skipPop=0;
function closeInfo(back=true){if(!md.classList.contains('on'))return;md.classList.remove('on');document.documentElement.style.overflow='';mdSlug=null;
  if(back&&history.state&&history.state.md){skipPop++;history.back()}else try{history.replaceState(null,'',location.pathname)}catch(e){}}
md.addEventListener('click',e=>{if(e.target===md||e.target.closest('[data-close]'))closeInfo()});

/* ---------- reproductor ---------- */
const plo=$('#plo');let yt=null,ytReady=null,cur=null,saveI=0,idleT=0;
function loadYT(){if(ytReady)return ytReady;ytReady=new Promise(res=>{window.onYouTubeIframeAPIReady=()=>res();const s=document.createElement('script');s.src='https://www.youtube.com/iframe_api';s.onerror=()=>res('err');document.head.appendChild(s)});return ytReady}
function nextOf(e){const E=eps(BY[e.s]);const i=E.findIndex(x=>ekey(x)===ekey(e));return E.slice(i+1).find(ready)||null}
function tuck(ms){const b=$('#xb');b.classList.remove('tuck');clearTimeout(tuck.t);tuck.t=setTimeout(()=>b.classList.add('tuck'),ms)}
function poke(){plo.classList.remove('idle');clearTimeout(idleT);idleT=setTimeout(()=>plo.classList.add('idle'),3200)}
async function playItem(item,label){hidePV();const s=BY[item.s];cur=item;
  plo.classList.add('on');plo.classList.toggle('vert',!!s.vertical);document.documentElement.style.overflow='hidden';
  $('#pti').innerHTML=esc(s.titulo)+'<small>'+esc(label)+'</small>';$('#nx').classList.remove('on');tuck(2500);poke();
  try{history.pushState({pl:1},'')}catch(e){}
  try{if(plo.requestFullscreen&&!document.fullscreenElement)await plo.requestFullscreen();if(!s.vertical&&screen.orientation&&screen.orientation.lock)screen.orientation.lock('landscape').catch(()=>{})}catch(e){}
  if(!item.yt){plo.classList.add('soon');$('#soon').style.backgroundImage='url("'+img(s)+'")';$('#soonp').textContent=(item.estado==='pronto'?'Este episodio está en producción.':'Lo estamos preparando: muy pronto podrás verlo aquí.');return}
  plo.classList.remove('soon');
  const r=await loadYT();if(r==='err'){toast('No se ha podido cargar el vídeo. Revisa la conexión.');return}
  const k=item.x!=null?null:ekey(item),start=k&&prog[k]&&prog[k].t<prog[k].d*.93?Math.floor(prog[k].t):0;
  const vars={autoplay:1,playsinline:1,rel:0,modestbranding:1,iv_load_policy:3,start,fs:0,cc_lang_pref:'es',hl:'es'};
  if(yt){yt.loadVideoById({videoId:item.yt,startSeconds:start})}
  else{$('#fr').innerHTML='<div id="yt"></div>';yt=new YT.Player('yt',{host:'https://www.youtube-nocookie.com',videoId:item.yt,playerVars:vars,events:{onStateChange:ev=>{
    if(ev.data===YT.PlayerState.ENDED)ended();}}})}
  clearInterval(saveI);saveI=setInterval(()=>{if(!yt||!yt.getCurrentTime||!cur||cur.x!=null)return;const t=yt.getCurrentTime(),d=yt.getDuration();if(d>0){prog[ekey(cur)]={t,d,ts:Date.now()};st.set('prog',prog);
    const n=nextOf(cur);if(n&&d-t<25)showNext(n);}},3000);
}
function showNext(n){const b=$('#nx');if(b.classList.contains('on'))return;b.innerHTML=IP+' Siguiente episodio';b.onclick=()=>playEp(n);b.classList.add('on')}
function ended(){if(!cur||cur.x!=null)return;const n=nextOf(cur);if(!n){toast('¡Has visto todos los episodios disponibles!');return}let c=5;const b=$('#nx');b.classList.add('on');b.onclick=()=>{clearInterval(ended.i);playEp(n)};
  b.innerHTML=IP+' Siguiente episodio en '+c;clearInterval(ended.i);ended.i=setInterval(()=>{c--;if(c<=0){clearInterval(ended.i);playEp(n)}else b.innerHTML=IP+' Siguiente episodio en '+c},1000)}
function playEp(e){if(!e)return;playItem(e,'T'+e.t+':E'+e.n+' · '+e.titulo)}
function playSeries(slug){const s=BY[slug],E=eps(s);
  const started=E.filter(e=>prog[ekey(e)]).sort((a,b)=>prog[ekey(b)].ts-prog[ekey(a)].ts)[0];
  let e=started&&prog[ekey(started)].t<prog[ekey(started)].d*.93?started:(started?nextOf(started):null)||E.find(ready)||E[0];
  if(!e){openInfo(slug);return}playEp(e)}
function closePlayer(back=true){if(!plo.classList.contains('on'))return;clearInterval(saveI);clearInterval(ended.i);try{if(yt&&yt.stopVideo)yt.stopVideo()}catch(e){}
  if(yt&&cur&&cur.x==null&&yt.getCurrentTime){const t=yt.getCurrentTime(),d=yt.getDuration();if(d>0){prog[ekey(cur)]={t,d,ts:Date.now()};st.set('prog',prog)}}
  plo.classList.remove('on','soon');cur=null;document.documentElement.style.overflow=md.classList.contains('on')?'hidden':'';
  try{if(document.fullscreenElement)document.exitFullscreen()}catch(e){}
  if(back&&history.state&&history.state.pl){skipPop++;history.back()}render();if(mdSlug)openInfo(mdSlug,false)}
$('#xb').addEventListener('click',()=>{const b=$('#xb');if(b.classList.contains('tuck')){b.classList.remove('tuck');tuck(2500);return}closePlayer()});
$('#soonx').addEventListener('click',()=>closePlayer());
plo.addEventListener('pointermove',poke);plo.addEventListener('pointerdown',poke);
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement&&plo.classList.contains('on'))tuck(2500)});

/* ---------- buscador ---------- */
const sr=$('#sr');
function search(){const q=$('#q').value.trim().toLowerCase();const out=$('#sres');
  const pool=visible();if(!q){out.innerHTML='<div class="row" style="margin-top:24px"><h2 style="margin:0 0 10px">Todas las series</h2><div class="grid">'+pool.map(cardS).join('')+'</div></div>';return}
  const hs=pool.filter(s=>(s.titulo+' '+s.generos.join(' ')+' '+s.sinopsis+' '+s.gancho).toLowerCase().includes(q));
  const he=[];pool.forEach(s=>eps(s).forEach(e=>{if((e.titulo+' '+(e.sinopsis||'')).toLowerCase().includes(q))he.push(e)}));
  out.innerHTML=(hs.length||he.length)?'<div class="grid">'+hs.map(cardS).join('')+he.map(cardE).join('')+'</div>':'<p class="emp">No hay nada con «'+esc(q)+'». Prueba con otra palabra.</p>'}
function openSearch(){sr.classList.add('on');search();setTimeout(()=>$('#q').focus(),30)}
function closeSearch(){sr.classList.remove('on');$('#q').value=''}
$('#bSearch').addEventListener('click',()=>sr.classList.contains('on')?closeSearch():openSearch());$('#q').addEventListener('input',search);

/* ---------- clics ---------- */
document.addEventListener('click',ev=>{const t=ev.target;
  const pl=t.closest('[data-play]');if(pl){ev.preventDefault();closeSearch();playSeries(pl.dataset.play);return}
  const ep=t.closest('[data-ep]');if(ep){ev.preventDefault();const e=findE(ep.dataset.ep);if(!e)return;if(e.estado==='pronto'){toast('Este episodio está en producción.');return}closeSearch();playEp(e);return}
  const ex=t.closest('[data-ex]');if(ex){const [sl,i]=ex.dataset.ex.split(':');const x=BY[sl].extras[+i];closeSearch();playItem(Object.assign({s:sl,x:+i},x),x.titulo);return}
  const li=t.closest('[data-list]');if(li){const k=li.dataset.list;list=inList(k)?list.filter(x=>x!==k):[...list,k];st.set('list',list);$$('[data-list="'+k+'"]').forEach(b=>{b.classList.toggle('on',inList(k));b.innerHTML=b.classList.contains('btn')?(inList(k)?'✓ En Mi lista':'+ Mi lista'):ICL(inList(k))});toast(inList(k)?'Añadida a Mi lista':'Quitada de Mi lista');if(view==='lista'||view==='inicio')setTimeout(render,0);return}
  const inf=t.closest('[data-info]');if(inf){ev.preventDefault();closeSearch();openInfo(inf.dataset.info);return}
  const go=t.closest('[data-go]');if(go){ev.preventDefault();if(view!=='inicio'){view='inicio';render()}const el=document.getElementById(go.dataset.go);if(el)scrollTo({top:el.getBoundingClientRect().top+scrollY-90,behavior:'smooth'});return}
  const v=t.closest('[data-v]');if(v){view=v.dataset.v;if(view==='peques'&&!kids){}closeSearch();render();scrollTo({top:0,behavior:'smooth'});return}
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(plo.classList.contains('on'))closePlayer();else if(sr.classList.contains('on'))closeSearch();else closeInfo()}
  if((e.key==='Enter'||e.key===' ')&&e.target.matches('.ep[role=button]')){e.preventDefault();e.target.click()}});
$('#bKids').addEventListener('click',()=>{kids=!kids;st.set('kids',kids);if(kids&&view==='series')view='inicio';render();toast(kids?'Modo Peques: solo series infantiles':'Modo Peques desactivado')});
addEventListener('popstate',()=>{if(skipPop){skipPop--;return}if(plo.classList.contains('on'))closePlayer(false);else if(md.classList.contains('on'))closeInfo(false)});
let lastY=0;addEventListener('scroll',()=>{const y=scrollY;$('#hd').classList.toggle('solid',y>40);$('#mnav').classList.toggle('hide',y>lastY&&y>120);lastY=y},{passive:true});

if(!S.some(s=>s.peques)){kids=false;document.body.classList.add('nokids')}
if(S.length===1){const nv='<a data-v="inicio" class="on">Inicio</a><a data-go="sec-ep">Episodios</a>'+((S[0].extras||[]).length?'<a data-go="sec-ex">Detrás de las cámaras</a>':'')+'<a data-go="sec-ab">Sobre la serie</a><a data-v="lista">Mi lista</a>';$('#nv').innerHTML=nv;$('#mnav').innerHTML=nv}
/* intro (una vez por sesión) */
(function(){const it=$('#intro');let seen=0;try{seen=sessionStorage.getItem('ap_intro')}catch(e){}
  if(seen||OPEN||location.search||matchMedia('(prefers-reduced-motion:reduce)').matches){it.remove();return}
  try{sessionStorage.setItem('ap_intro','1')}catch(e){}const end=()=>{it.classList.add('out');setTimeout(()=>it.remove(),800)};it.addEventListener('click',end);setTimeout(end,2000)})();
render();
const q=new URLSearchParams(location.search),qs=q.get('s')||OPEN,qv=q.get('v');
if(qv){const e=findE(qv);if(e)setTimeout(()=>playEp(e),300)}else if(qs&&BY[qs])openInfo(qs,false);
"""


def play_page(slug=None):
    s = next((x for x in SERIES if x['slug'] == slug), None)
    p = '../../' if s else '../'          # hasta la raíz
    pp = '../' if s else ''               # hasta play/
    url = BASE + 'play/' + (s['slug'] + '/' if s else '')
    title = (f"{s['titulo']} · Serie de animación | Alica Play" if s else 'Alica Play · Series de animación originales de Alica Studio')
    desc = (s['gancho'] + ' ' + s['sinopsis'])[:158] if s else 'Alica Play es la plataforma de series de Alica Studio: animación original para adultos y para los peques, creada por Enric Alicarte. Gratis y en el navegador.'
    ogimg = BASE + 'play/img/' + (s['slug'] if s else SER['destacada']) + '.jpg'
    jl = {"@context": "https://schema.org", "@type": "TVSeries", "name": s['titulo'], "description": s['sinopsis'], "url": url, "image": ogimg, "genre": s['generos'],
          "creator": {"@type": "Person", "name": s['creador']}, "productionCompany": {"@type": "Organization", "name": "Alica Studio"}, "inLanguage": "es"} if s else \
         {"@context": "https://schema.org", "@type": "WebSite", "name": "Alica Play", "url": url, "publisher": {"@type": "Organization", "name": "Alica Studio", "url": BASE}}
    h = studio_head(title, desc, url, p, ogimg, extra='<link rel="preload" href="' + p + 'assets/fonts/unbounded-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>') + jd(jl)
    data = json.dumps({k: v for k, v in SER.items() if not k.startswith('_')}, ensure_ascii=False, separators=(',', ':'))
    body = PLAY_HTML.replace('__P__', pp or './').replace('__R__', p)
    js = 'window.__SER=' + data + ';window.__P=' + json.dumps(pp) + ';' + (f'window.__OPEN={json.dumps(s["slug"])};' if s else '') + PLAY_JS
    out = h + '<style>' + BASE_CSS + PLAY_CSS + '</style></head><body>' + body + '<script>' + js + '</script></body></html>'
    W('play/' + (s['slug'] + '/' if s else '') + 'index.html', out)


# ============================ PORTADA ALICA STUDIO ============================
HOME_CSS = r"""
.sh{position:fixed;inset:0 0 auto;z-index:40;display:flex;align-items:center;gap:24px;padding:calc(14px + env(safe-area-inset-top)) 4vw 14px;transition:background .3s,backdrop-filter .3s}
.sh.solid{background:rgba(7,6,15,.8);backdrop-filter:blur(14px) saturate(1.4);-webkit-backdrop-filter:blur(14px) saturate(1.4)}
.sh .logo{display:flex;align-items:center;gap:.45em;font:900 1.2rem/1 var(--hd);letter-spacing:-.01em;text-decoration:none;white-space:nowrap}
.sh nav{display:flex;gap:26px;margin-left:auto;align-items:center}.sh nav a{text-decoration:none;color:#d8d3ef;font-weight:500;white-space:nowrap}.sh nav a:hover{color:#fff}
.sh nav .pill{background:#fff;color:#07060f;padding:9px 16px;border-radius:999px;font-weight:700}.sh nav .pill:hover{color:#07060f;background:var(--y)}
/* hero con muro de juegos */
.hero{position:relative;min-height:100svh;display:grid;place-items:center;text-align:center;padding:130px 5vw 120px;overflow:hidden;isolation:isolate}
.wall{position:absolute;inset:-30% -20%;z-index:-3;display:flex;gap:18px;justify-content:center;transform:perspective(1600px) rotateX(32deg) rotateZ(-16deg) scale(1.08);transform-origin:50% 40%;opacity:.55}
.wall .cl{display:flex;flex-direction:column;gap:18px;width:300px;flex:none;animation:colU 70s linear infinite}
.wall .cl:nth-child(even){animation-name:colD;animation-duration:85s}
.wall img{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.5)}
@keyframes colU{from{transform:translateY(0)}to{transform:translateY(-50%)}}@keyframes colD{from{transform:translateY(-50%)}to{transform:translateY(0)}}
.hero::before{content:"";position:absolute;inset:0;z-index:-2;background:radial-gradient(ellipse 60% 55% at 50% 50%,rgba(7,6,15,.94) 0,rgba(7,6,15,.78) 45%,rgba(7,6,15,.25) 100%),linear-gradient(0deg,var(--bg) 0,rgba(7,6,15,0) 25%),linear-gradient(180deg,var(--bg) 0,rgba(7,6,15,0) 18%)}
.orb{position:absolute;width:min(80vw,900px);aspect-ratio:1;border-radius:50%;background:conic-gradient(from 0deg,#ffd23f,#ff4fa3,#7c6cff,#38e5ff,#ffd23f);filter:blur(110px);opacity:.28;z-index:-1;animation:spin 26s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.hero .ey{display:inline-flex;align-items:center;gap:10px;font:700 .78rem/1 var(--tx);letter-spacing:.3em;text-transform:uppercase;color:#cfc8ea;margin:0 0 26px;padding:9px 16px;border:1px solid rgba(255,255,255,.16);border-radius:999px;background:rgba(7,6,15,.45);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.hero h1{font:900 clamp(3.4rem,13vw,11.5rem)/.84 var(--hd);letter-spacing:-.055em;margin:0}
.hero h1 .a{display:block;color:#fff}
.hero h1 .b{display:block;background:linear-gradient(90deg,#ffd23f,#ff4fa3 45%,#7c6cff 70%,#38e5ff);background-size:200% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;padding-bottom:.06em;animation:sh 8s ease-in-out infinite alternate}
@keyframes sh{to{background-position:100% 0}}
.hero .lead{font-size:clamp(1.05rem,2vw,1.35rem);max-width:34em;margin:30px auto 36px;color:#e2dcf5}
.hero .ctas{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.hero .btn{padding:1em 1.7em}
.rv{opacity:0;transform:translateY(26px);animation:rv .9s cubic-bezier(.2,.8,.2,1) forwards}
.rv.d1{animation-delay:.12s}.rv.d2{animation-delay:.24s}.rv.d3{animation-delay:.36s}
@keyframes rv{to{opacity:1;transform:none}}
/* cinta */
.mq{overflow:hidden;border-block:1px solid var(--line);padding:16px 0;background:#0b0918}
.mq div{display:flex;gap:48px;width:max-content;animation:mq 38s linear infinite;font:900 clamp(1.1rem,2vw,1.6rem)/1 var(--hd);letter-spacing:-.01em;text-transform:uppercase;color:#4d4672}
.mq span{display:flex;align-items:center;gap:48px}.mq span::after{content:"";width:.6em;height:.6em;border-radius:50%;background:conic-gradient(#ffd23f,#ff4fa3,#38e5ff,#ffd23f)}
.mq b{color:#f5f2ff}
@keyframes mq{to{transform:translateX(-50%)}}
.wrap{max-width:1440px;margin:0 auto;padding:0 4vw}
.sec{margin-top:110px}
.lbl{display:inline-flex;align-items:center;gap:10px;font:800 .74rem/1 var(--tx);letter-spacing:.28em;text-transform:uppercase;color:var(--mut);margin:0 0 16px}
.lbl .dot{width:1.1em;height:1.1em}
.sec h2.t{font:900 clamp(2rem,4.4vw,3.6rem)/.98 var(--hd);letter-spacing:-.04em;margin:0 0 14px}
.sec .st{color:var(--mut);margin:0 0 30px;max-width:40em;font-size:1.05rem}
/* puertas */
.doors{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.door{position:relative;display:block;min-height:min(76vh,660px);border-radius:28px;overflow:hidden;text-decoration:none;isolation:isolate;transition:transform .5s cubic-bezier(.2,.8,.2,1)}
.door::before{content:"";position:absolute;inset:0;border-radius:inherit;padding:1.5px;background:linear-gradient(140deg,rgba(255,255,255,.3),rgba(255,255,255,.04) 40%,rgba(255,255,255,.04) 60%,rgba(255,255,255,.25));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;z-index:3;pointer-events:none;transition:background .4s}
.door.sal:hover::before{background:linear-gradient(140deg,#ffd23f,rgba(255,210,63,.1) 50%,#ff4fa3)}
.door.ply:hover::before{background:linear-gradient(140deg,#ff4fa3,rgba(255,79,163,.1) 50%,#38e5ff)}
.door:hover{transform:translateY(-8px)}
.door .bg{position:absolute;inset:0;z-index:-2;overflow:hidden}
.door .bg video,.door .bg img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity 1.2s,transform 6s cubic-bezier(.2,.8,.2,1)}
.door.ply .bg img{max-width:none;object-position:72% 50%;inset:-3%;width:106%;height:106%}
.door:hover .bg video{transform:scale(1.06)}
.door.ply .bg .l0{animation:dr0 22s ease-in-out infinite alternate}.door.ply .bg .l1{animation:dr1 18s ease-in-out infinite alternate}.door.ply .bg .l2{animation:dr2 14s ease-in-out infinite alternate}
@keyframes dr0{to{translate:-1.5% .8%}}@keyframes dr1{to{translate:-2.6% -1%}}@keyframes dr2{to{translate:-4% 1.2%}}
.door::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(7,6,15,.96) 6%,rgba(7,6,15,.5) 48%,rgba(7,6,15,.05))}
.door .in{position:absolute;left:0;right:0;bottom:0;padding:38px}
.door .k{display:inline-flex;align-items:center;gap:.5em;font:800 .72rem/1 var(--tx);letter-spacing:.26em;text-transform:uppercase;color:#fff;background:rgba(0,0,0,.4);padding:9px 13px;border-radius:999px;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);margin-bottom:18px}
.door h2{font:900 clamp(2.4rem,5vw,4.8rem)/.9 var(--hd);letter-spacing:-.045em;margin:0 0 14px}
.door p{margin:0 0 24px;color:#ddd7f3;max-width:28em;font-size:1.05rem}
.door .go{display:inline-flex;align-items:center;gap:12px;font-weight:700}.door .go i{width:48px;height:48px;border-radius:50%;background:#fff;color:#07060f;display:grid;place-items:center;font-style:normal;font-size:1.3rem;transition:transform .35s,background .35s}
.door:hover .go i{transform:translateX(8px)}.door.sal:hover .go i{background:var(--y)}.door.ply:hover .go i{background:var(--p);color:#fff}
.door.sal h2{color:var(--y)}.door.ply h2 b{color:var(--p)}
.door .now{position:absolute;top:22px;right:22px;z-index:2;font:700 .78rem/1 var(--tx);background:rgba(7,6,15,.6);padding:8px 12px;border-radius:999px;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);display:flex;align-items:center;gap:8px}
.door .now::before{content:"";width:8px;height:8px;border-radius:50%;background:#e50914;box-shadow:0 0 0 0 rgba(229,9,20,.7);animation:pulse 1.8s infinite}
@keyframes pulse{70%{box-shadow:0 0 0 10px rgba(229,9,20,0)}100%{box-shadow:0 0 0 0 rgba(229,9,20,0)}}
/* estreno */
.prem{position:relative;border-radius:28px;overflow:hidden;min-height:540px;display:flex;align-items:center;isolation:isolate}
.prem .bg{position:absolute;inset:0;z-index:-2}.prem .bg img{max-width:none;position:absolute;inset:-3%;width:106%;height:106%;object-fit:cover;object-position:75% 50%}
.prem::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(7,6,15,.96) 0,rgba(7,6,15,.75) 38%,rgba(7,6,15,0) 72%)}
.prem .in{padding:56px;max-width:600px}
.prem .tl{font:900 clamp(2.6rem,6vw,5.2rem)/.9 Georgia,'Times New Roman',serif;letter-spacing:.02em;margin:6px 0 22px;white-space:nowrap}
.prem .tl span{display:inline-block;background:#f4ecd8;color:#1d1712;padding:.02em .1em .06em;margin:0 .02em;box-shadow:3px 5px 0 rgba(0,0,0,.35)}
.prem .tl span:nth-child(odd){transform:rotate(-3deg)}.prem .tl span:nth-child(even){transform:rotate(2.5deg) translateY(.04em)}.prem .tl span:nth-child(3){background:#c8452f;color:#f4ecd8}.prem .tl span:nth-child(6){background:#2f5b4c;color:#f4ecd8}
.prem blockquote{margin:0 0 14px;font:italic 400 clamp(1.3rem,2.2vw,1.8rem)/1.25 Georgia,'Times New Roman',serif;color:#f4ecd8}
.prem p{color:#d7d0ec;margin:0 0 22px;line-height:1.6}
.prem .mt{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;color:#ddd8f2;font-size:.92rem;margin-bottom:26px}.prem .mt .age{border:1px solid rgba(255,255,255,.55);padding:1px 7px;border-radius:4px;font-size:.8rem}.prem .mt b{color:#7cf0c8}
/* bento */
.bento{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:clamp(150px,13vw,210px);gap:16px}
.bento a{position:relative;display:block;border-radius:18px;overflow:hidden;text-decoration:none;background:var(--card);isolation:isolate;transition:transform .4s cubic-bezier(.2,.8,.2,1)}
.bento a:hover{transform:translateY(-5px)}
.bento a:first-child{grid-column:span 2;grid-row:span 2}
.bento img,.bento video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transition:transform 1.2s cubic-bezier(.2,.8,.2,1)}
.bento a:hover img{transform:scale(1.06)}
.bento a::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(7,6,15,.9),rgba(7,6,15,0) 60%)}
.bento .tx{position:absolute;left:16px;right:16px;bottom:14px}.bento b{display:block;font:700 1.05rem/1.2 var(--tx)}.bento small{color:#cfc8ea;font-size:.85rem}
.bento a:first-child b{font:900 clamp(1.6rem,2.6vw,2.4rem)/1 var(--hd);letter-spacing:-.03em;margin-bottom:6px}.bento a:first-child .tx{left:26px;bottom:24px}
.bento .ch{position:absolute;top:12px;left:12px;font:800 .64rem/1 var(--tx);letter-spacing:.08em;text-transform:uppercase;padding:6px 9px;border-radius:999px;background:var(--y);color:#1a1300}
.more{display:flex;justify-content:flex-end;margin-top:18px}.more a{color:#fff;font-weight:700;text-decoration:none;display:inline-flex;gap:8px;align-items:center}.more a:hover{color:var(--y)}
/* qué hacemos */
.what{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.what div{position:relative;border:1px solid var(--line);border-radius:22px;padding:30px;background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,0));overflow:hidden}
.what h3{font:700 1.25rem/1.2 var(--hd);margin:0 0 12px;letter-spacing:-.01em}.what p{margin:0;color:#cfc9e8;line-height:1.6}
.what .n{font:900 3rem/1 var(--hd);background:conic-gradient(#ffd23f,#ff4fa3,#38e5ff,#ffd23f);-webkit-background-clip:text;background-clip:text;color:transparent;display:block;margin-bottom:18px}
/* pie */
.big{margin-top:120px;border-top:1px solid var(--line);overflow:hidden}
.big .wm{font:900 clamp(2.6rem,11.4vw,13rem)/.8 var(--hd);letter-spacing:-.06em;text-align:center;white-space:nowrap;margin:40px 0 -0.12em;background:linear-gradient(180deg,#2a2450 0,#07060f 92%);-webkit-background-clip:text;background-clip:text;color:transparent;user-select:none}
.big .ft{margin-top:0;border-top:0}
.io{opacity:0;transform:translateY(40px);transition:opacity .9s cubic-bezier(.2,.8,.2,1),transform .9s cubic-bezier(.2,.8,.2,1)}.io.on{opacity:1;transform:none}
@media (max-width:860px){
 .sh nav{gap:12px;font-size:.9rem}.sh nav .x{display:none}.sh .logo{font-size:1.02rem}.sh .lg{display:none}.sh nav .pill{padding:7px 12px}
 .hero .ey{font-size:.62rem;letter-spacing:.2em;white-space:nowrap}.wall .cl{width:180px}.wall{gap:12px}.wall .cl{gap:12px}.wall{opacity:.5}
 .hero{padding-top:110px}
 .doors{grid-template-columns:1fr}.door{min-height:460px}.door .in{padding:26px}
 .prem{min-height:0;flex-direction:column;align-items:stretch}.prem .bg{position:relative;aspect-ratio:16/10;inset:auto}.prem::after{background:linear-gradient(0deg,rgba(7,6,15,1) 30%,rgba(7,6,15,0) 62%)}.prem .in{padding:0 22px 30px;margin-top:-6px;position:relative;z-index:2}.prem .tl{font-size:2.4rem}
 .bento{grid-template-columns:repeat(2,1fr);grid-auto-rows:150px;gap:12px}
 .what{grid-template-columns:1fr}.sec{margin-top:80px}
}
@media (prefers-reduced-motion:reduce){.rv,.io{opacity:1!important;transform:none!important}}
"""


def home_page():
    url = BASE
    title = 'Alica Studio · Juegos y series de animación de Enric Alicarte'
    desc = 'Alica Studio es el estudio de Enric Alicarte: minijuegos para el navegador en el Salón Recreativo y series de animación originales en Alica Play.'
    h = studio_head(title, desc, url, '', BASE + 'img/og-home.jpg', extra='<link rel="preload" href="assets/fonts/unbounded-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>')
    h += jd({"@context": "https://schema.org", "@type": "Organization", "name": "Alica Studio", "url": BASE, "founder": {"@type": "Person", "name": "Enric Alicarte"},
             "subOrganization": [{"@type": "Organization", "name": "Salón Recreativo", "url": BASE + 'salon/'}, {"@type": "Organization", "name": "Alica Play", "url": BASE + 'play/'}]})
    s0 = next(x for x in SERIES if x['slug'] == SER['destacada'])
    # muro de juegos: columnas con las portadas (duplicadas para el bucle infinito)
    order = LATEST + [g for g in play if g not in LATEST]
    ncol, per = 7, 7
    cols = ''
    for c in range(ncol):
        pick = [order[(c * per + k) % len(order)] for k in range(per)]
        imgs = ''.join(f'<img src="img/{g["slug"]}.jpg" alt="" width="344" height="216" decoding="async"{" loading=\"lazy\"" if k > 3 else ""}>' for k, g in enumerate(pick))
        cols += f'<div class="cl">{imgs}{imgs}</div>'
    vids = [g for g in LATEST if has_media(g)][:4]
    vhtml = ''.join(f'<video muted loop playsinline preload="none" poster="media/{g["slug"]}.jpg" style="opacity:{1 if k == 0 else 0}"><source src="media/{g["slug"]}.webm" type="video/webm"><source src="media/{g["slug"]}.mp4" type="video/mp4"></video>' for k, g in enumerate(vids))
    lay = ''.join(f'<img class="l{i}" src="play/img/{c}" alt="" loading="lazy">' for i, c in enumerate(s0.get('capas', [s0['slug'] + '.jpg'])))
    ep1 = (s0['temporadas'][0]['episodios'][0] if s0.get('temporadas') else None)
    tl = ''.join(f'<span>{e(ch)}</span>' for ch in s0['titulo'])
    b = LATEST[:9]
    bento = ''
    for k, g in enumerate(b):
        med = (f'<video muted loop playsinline preload="none" poster="img/{g["slug"]}.jpg" data-hv><source src="media/{g["slug"]}.webm" type="video/webm"><source src="media/{g["slug"]}.mp4" type="video/mp4"></video>' if k == 0 and has_media(g) else f'<img src="img/{g["slug"]}.jpg" alt="" loading="lazy" width="344" height="216">')
        bento += f'<a href="jugar/{g["slug"]}/">{med}{"<span class=ch>Nuevo</span>" if k < 3 else ""}<div class="tx"><b>{e(g["name"])}</b><small>{e(g.get("note", ""))}</small></div></a>'
    marq = ''.join(f'<span><b>{w}</b></span>' if i % 2 == 0 else f'<span>{w}</span>' for i, w in enumerate(['Juegos', 'Series', 'Animación', 'Hecho en Barcelona', 'Sin descargas', 'Móvil y PC'] * 2))
    body = f"""<header class="sh" id="sh"><a class="logo" href="./"><span class="dot"></span>ALICA STUDIO</a><nav><a href="salon/">Salón<span class="lg"> Recreativo</span></a><a href="play/"><span class="lg">Alica </span>Play</a><a class="x" href="estudio/">El estudio</a><a class="pill x" href="play/{s0['slug']}/">Ver {e(s0['titulo'])}</a></nav></header>
<section class="hero"><div class="wall" aria-hidden="true">{cols}</div><div class="orb" aria-hidden="true"></div><div>
<p class="ey rv"><span class="dot"></span>Estudio de juegos y animación</p>
<h1 class="rv d1"><span class="a">ALICA</span><span class="b">STUDIO</span></h1>
<p class="lead rv d2">Juegos que se juegan al momento en el navegador y series de animación originales. Todo creado por Enric Alicarte.</p>
<div class="ctas rv d3"><a class="btn y" href="salon/">Jugar en el Salón</a><a class="btn g" href="play/">{ICO['play']} Ver Alica Play</a></div></div></section>
<div class="mq" aria-hidden="true"><div>{marq}{marq}</div></div>
<div class="wrap">
<section class="sec io"><p class="lbl"><span class="dot"></span>Dos puertas</p><h2 class="t">Elige por dónde entrar</h2><p class="st">El Salón Recreativo para jugar. Alica Play para ver nuestras series.</p>
<div class="doors">
<a class="door sal" href="salon/"><div class="bg" id="vbg">{vhtml}</div><span class="now">Nuevos juegos</span><div class="in"><span class="k"><span class="dot"></span>Juegos</span><h2>Salón<br>Recreativo</h2><p>Minijuegos gratis y sin anuncios: carreras, fútbol, ritmo, juegos con cámara y mucho más. En el móvil y en el ordenador.</p><span class="go">Entrar al Salón <i>→</i></span></div></a>
<a class="door ply" href="play/"><div class="bg">{lay}</div><span class="now">Estreno: {e(s0['titulo'])}</span><div class="in"><span class="k"><span class="dot"></span>Series</span><h2>Alica<br><b>Play</b></h2><p>Series de animación originales, creadas en el estudio. Empezamos con {e(s0['titulo'])}.</p><span class="go">Ver series <i>→</i></span></div></a>
</div></section>
<section class="sec io"><div class="prem"><div class="bg"><img src="play/img/{s0['slug']}.jpg" alt="" loading="lazy"></div><div class="in"><p class="lbl"><span class="dot"></span>Estreno en Alica Play</p><h2 class="tl" aria-label="{e(s0['titulo'])}">{tl}</h2><blockquote>«{e(s0['gancho'])}»</blockquote><p>{e(s0['sinopsis'])}</p><div class="mt"><b>Nuevo</b><span>{s0['anio']}</span><span class="age">{e(s0['edad'])}</span>{f"<span>Piloto · {e(ep1['dur'])}</span>" if ep1 and ep1.get('dur') else ''}<span>{e(s0['idiomas'])}</span></div><a class="btn w" href="play/{s0['slug']}/">{ICO['play']} Ver {e(s0['titulo'])}</a></div></div></section>
<section class="sec io"><p class="lbl"><span class="dot"></span>Salón Recreativo</p><h2 class="t">Recién llegados al Salón</h2><p class="st">Los últimos juegos que hemos estrenado o mejorado.</p><div class="bento">{bento}</div><div class="more"><a href="salon/">Ver todos los juegos →</a></div></section>
<section class="sec io"><p class="lbl"><span class="dot"></span>El estudio</p><h2 class="t">Qué hacemos</h2><p class="st">Un estudio pequeño con dos líneas de trabajo.</p><div class="what">
<div><span class="n">01</span><h3>Juegos para el navegador</h3><p>Se abren y se juegan al momento, sin descargas ni registro. Pantalla completa en móvil y PC.</p></div>
<div><span class="n">02</span><h3>Series de animación</h3><p>Historias originales con estilo propio, como el collage de papel de {e(s0['titulo'])}.</p></div>
<div><span class="n">03</span><h3>Hecho en Barcelona</h3><p>Ideas, guiones, música y animación creados en el estudio de Enric Alicarte.</p></div>
</div></section>
</div>
<div class="big"><div class="wm" aria-hidden="true">ALICA STUDIO</div>
<footer class="ft"><div class="in"><span><span class="dot" style="vertical-align:-2px"></span> © 2026 <b style="color:#fff">Alica Studio</b> · Enric Alicarte</span><nav><a href="salon/">Salón Recreativo</a><a href="play/">Alica Play</a><a href="estudio/">El estudio</a><a href="aviso-legal/">Aviso legal</a><a href="privacidad/">Privacidad</a><a href="cookies/">Cookies</a></nav></div></footer></div>
<script>
(function(){{const h=document.getElementById('sh');addEventListener('scroll',()=>h.classList.toggle('solid',scrollY>30),{{passive:true}});
const red=matchMedia('(prefers-reduced-motion:reduce)').matches;
const io2=new IntersectionObserver(es=>es.forEach(x=>{{if(x.isIntersecting){{x.target.classList.add('on');io2.unobserve(x.target)}}}}),{{threshold:.12}});document.querySelectorAll('.io').forEach(el=>io2.observe(el));
const hv=document.querySelector('[data-hv]');if(hv){{const o=new IntersectionObserver(es=>es.forEach(x=>{{if(x.isIntersecting){{hv.preload='auto';hv.play().catch(()=>{{}})}}else hv.pause()}}),{{threshold:.3}});o.observe(hv)}}
const vs=[...document.querySelectorAll('#vbg video')];if(!vs.length)return;let i=0,on=false;
const io=new IntersectionObserver(es=>{{es.forEach(x=>{{on=x.isIntersecting;if(on){{const v=vs[i];v.preload='auto';v.play().catch(()=>{{}})}}else vs.forEach(v=>v.pause())}})}},{{threshold:.25}});io.observe(document.getElementById('vbg'));
if(red||vs.length<2)return;setInterval(()=>{{if(!on)return;const a=vs[i];i=(i+1)%vs.length;const b=vs[i];b.preload='auto';b.currentTime=0;b.play().catch(()=>{{}});b.style.opacity=1;a.style.opacity=0;setTimeout(()=>a.pause(),1300)}},6000)}})();
</script>"""
    out = h + '<style>' + BASE_CSS + HOME_CSS + '</style></head><body>' + body + '</body></html>'
    W('index.html', out)


home_page()
play_page()
for _s in SERIES:
    play_page(_s['slug'])
print('Alica Studio OK ·', len(SERIES), 'series')
