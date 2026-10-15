#!/usr/bin/env python3
"""Genera index.html (con SEO), jugar/<slug>/index.html, sitemap.xml, robots.txt y 404.html.
Uso: python3 tools/build_seo.py   (desde la raíz del repo). Datos en tools/games.json, fuente en tools/source.html."""
import json,re,html,os,datetime
BASE='https://enricalicarte.github.io/salon-recreativo/'
TODAY=datetime.date.today().isoformat()
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=json.load(open(os.path.join(root,'tools/games.json'),encoding='utf-8'))
G,CATS,CATD=D['GAMES'],D['CATS'],D['CATD']
e=lambda x:html.escape(str(x),quote=True)
play=[g for g in G if g.get('play')]
ORDER=['accion','deporte','ritmo','motor','historias','marca','relax','catquiz']
def short(t,n):
    t=t.strip()
    return t if len(t)<=n else t[:n-1].rsplit(' ',1)[0].rstrip('.,;:')+'…'
def jd(o):return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False,separators=(',',':'))+'</script>'
def gname(g):return g['name']
GENRE={'accion':'juego de acción','deporte':'juego de deporte','ritmo':'juego de ritmo musical','motor':'juego de motor','historias':'juego narrativo','marca':'juego con marca','relax':'juego relajante','cosmico':'juego cósmico','catquiz':'joc de paraules en català'}
# ---------- páginas de juego ----------
CSS="""*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#0d1230;color:#eef1ff;font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}a{color:#ffc933}
.w{max-width:980px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left))}
header.t{padding:16px 0;border-bottom:1px solid rgba(255,255,255,.13)}header.t a{color:#fff;text-decoration:none;font-weight:800;letter-spacing:.04em}
nav.bc{font-size:.85rem;color:#b3bbea;margin:18px 0 8px}nav.bc a{color:#b3bbea}
h1{font-size:clamp(2rem,6vw,3.2rem);line-height:1.1;margin:.2em 0 .3em}
.cover{width:100%;aspect-ratio:1.6;border-radius:18px;object-fit:cover;border:1px solid rgba(255,255,255,.15);display:block;background:#151b44}
.stage{position:relative;width:100%;aspect-ratio:16/10;max-height:78vh;border-radius:18px;overflow:hidden;background:#000;border:1px solid rgba(255,255,255,.15)}
.stage iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.stage .go{position:absolute;inset:0;display:grid;place-items:center;border:0;cursor:pointer;color:#0d1230;background:center/cover}
.go span{background:#ffc933;font:800 1.2rem system-ui;padding:16px 34px;border-radius:99px;box-shadow:0 8px 30px rgba(0,0,0,.5)}
.lead{font-size:1.15rem;color:#d6dcff}.tags{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0}.tags li{border:1px solid rgba(255,255,255,.25);border-radius:99px;padding:3px 12px;font-size:.85rem;color:#b3bbea}
h2{margin:1.6em 0 .5em;font-size:1.4rem}.rel{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px;list-style:none;padding:0}
.rel a{display:block;text-decoration:none;color:#fff;background:#151b44;border:1px solid rgba(255,255,255,.13);border-radius:14px;overflow:hidden}.rel img{width:100%;display:block;aspect-ratio:1.6;object-fit:cover}.rel b{display:block;padding:10px 12px}
footer{margin:60px 0 0;padding:26px 0 40px;border-top:1px solid rgba(255,255,255,.13);color:#b3bbea;font-size:.9rem}"""
for g in play:
    ca=g['cat']=='catquiz'
    lang='ca' if ca else 'es'
    url=BASE+'jugar/'+g['slug']+'/'
    img=BASE+'img/'+g['slug']+'.jpg'
    cat=CATS[g['cat']]['n'];cd=CATD.get(g['cat'],{})
    title=(g['name']+(' — joc en línia gratuït' if ca else ' — juego online gratis'))+' | Salón Recreativo'
    suf=' Juga gratis al navegador, sense descàrregues.' if ca else ' Juega gratis en el navegador, sin descargas, en móvil y PC.'
    desc=short(g['blurb'].rstrip('.')+'.'+suf,158)
    rel=[x for x in play if x['cat']==g['cat'] and x['slug']!=g['slug']]
    if len(rel)<4: rel+= [x for x in play if x['cat']!=g['cat'] and x['slug']!=g['slug']][:4-len(rel)]
    rel=rel[:6]
    home_lbl='Inicio'
    gtype=GENRE.get(g['cat'],'juego')
    note=(' ('+g['note']+')') if g.get('note') else ''
    if ca:
        p1=f"{g['name']} és un {gtype} que pots jugar en línia i gratis, directament al navegador, des del mòbil o l'ordinador. No cal instal·lar res ni crear cap compte."
        p2="Forma part del Salón Recreativo, una col·lecció de minijocs en línia."
        h2a='Com es juga';ptxt="Prem «Jugar» i comença: el joc carrega aquí mateix. Per a una millor experiència, obre'l a pantalla completa."
        reltitle='Més minijocs'
    else:
        p1=f"{g['name']}{note} es un {gtype} para jugar online y gratis, directamente en el navegador, desde el móvil o el ordenador. No hay que instalar nada ni crear una cuenta."
        p2=("Forma parte del Salón Recreativo, una colección de minijuegos online. "+(cd.get('d','') if cd else ''))
        h2a='Cómo se juega';ptxt="Pulsa «Jugar» y empieza: el juego se carga aquí mismo. Para una mejor experiencia ábrelo a pantalla completa o en una pestaña nueva."
        reltitle='Más minijuegos'
    jgame={"@context":"https://schema.org","@type":"VideoGame","name":g['name'],"description":g['blurb'],"url":url,"image":img,"genre":cat,"gamePlatform":"Web browser","applicationCategory":"Game","operatingSystem":"Any","inLanguage":lang,"isAccessibleForFree":True,"offers":{"@type":"Offer","price":"0","priceCurrency":"EUR"},"author":{"@type":"Person","name":"Enric Alicarte"},"keywords":", ".join(g['tags'])}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Salón Recreativo","item":BASE},{"@type":"ListItem","position":2,"name":cat,"item":BASE+'#sec-'+g['cat']},{"@type":"ListItem","position":3,"name":g['name'],"item":url}]}
    relhtml=''.join(f'<li><a href="../{x["slug"]}/"><img src="../../img/{x["slug"]}.jpg" alt="Portada de {e(x["name"])}" loading="lazy" width="344" height="216"><b>{e(x["name"])}</b></a></li>' for x in rel)
    page=f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0d1230">
<meta property="og:type" content="website"><meta property="og:site_name" content="Salón Recreativo"><meta property="og:locale" content="{'ca_ES' if ca else 'es_ES'}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}"><meta property="og:image:alt" content="Portada de {e(g['name'])}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{img}">
{jd(jgame)}
{jd(bc)}
<style>{CSS}</style></head>
<body><header class="t"><div class="w"><a href="../../">SALÓN RECREATIVO</a></div></header>
<main class="w">
<nav class="bc" aria-label="Migas de pan"><a href="../../">{home_lbl}</a> › <a href="../../#sec-{g['cat']}">{e(cat)}</a> › {e(g['name'])}</nav>
<h1>{e(g['name'])}</h1>
<p class="lead">{e(g['blurb'])}</p>
<div class="stage" id="stage"><button class="go" id="go" type="button" style="background-image:linear-gradient(rgba(13,18,48,.25),rgba(13,18,48,.25)),url(../../img/{g['slug']}.jpg)" aria-label="Jugar a {e(g['name'])}"><span>▶ {'Jugar' if True else ''}</span></button></div>
<noscript><p><a href="../../{g['play']}">Abrir {e(g['name'])}</a></p></noscript>
<p><a href="../../{g['play']}" target="_blank" rel="noopener">{'Obrir en una pestanya nova' if ca else 'Abrir en una pestaña nueva'} ↗</a></p>
<ul class="tags">{''.join('<li>'+e(t)+'</li>' for t in g['tags'])}</ul>
<h2>{'Sobre' if ca else 'Sobre'} {e(g['name'])}</h2>
<p>{e(p1)}</p><p>{e(p2)}</p>
<h2>{h2a}</h2><p>{e(ptxt)}</p>
<h2>{reltitle}</h2>
<ul class="rel">{relhtml}</ul>
</main>
<footer><div class="w"><a href="../../">Salón Recreativo</a> · {'Minijocs en línia gratuïts' if ca else 'Minijuegos online gratis'} · Enric Alicarte</div></footer>
<script>document.getElementById('go').addEventListener('click',function(){{var f=document.createElement('iframe');f.src='../../{g['play']}';f.title={json.dumps(g['name'],ensure_ascii=False)};f.allow='fullscreen; autoplay; gamepad; accelerometer; gyroscope';f.allowFullscreen=true;var s=document.getElementById('stage');s.innerHTML='';s.appendChild(f);}});</script>
</body></html>"""
    d=os.path.join(root,'jugar',g['slug']);os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(page)
# ---------- home ----------
src=open(os.path.join(root,'tools/source.html'),encoding='utf-8').read()
i=src.index('</style>')+8
head_part=src[:i];body=src[i:]
head_part=re.sub(r'<title>.*?</title>\s*','',head_part,flags=re.S)
head_part=re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\s*','',head_part)
HT='Minijuegos online gratis en el navegador | Salón Recreativo'
HD=f'{len(G)} minijuegos online gratis para jugar en el navegador, en móvil y PC: fútbol, ritmo, karts, relax y palabras en catalán. Sin descargas ni registro.'
HD=short(HD,158)
items=[{"@type":"ListItem","position":k+1,"url":BASE+'jugar/'+g['slug']+'/',"name":g['name']} for k,g in enumerate(play)]
site={"@context":"https://schema.org","@type":"WebSite","name":"Salón Recreativo","url":BASE,"inLanguage":"es","description":HD,"publisher":{"@type":"Person","name":"Enric Alicarte"}}
lst={"@context":"https://schema.org","@type":"ItemList","name":"Minijuegos online gratis","itemListElement":items}
meta=f"""<title>{e(HT)}</title>
<meta name="description" content="{e(HD)}">
<link rel="canonical" href="{BASE}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0d1230">
<meta property="og:type" content="website"><meta property="og:site_name" content="Salón Recreativo"><meta property="og:locale" content="es_ES"><meta property="og:title" content="{e(HT)}"><meta property="og:description" content="{e(HD)}"><meta property="og:url" content="{BASE}"><meta property="og:image" content="{BASE}img/og-home.jpg"><meta property="og:image:width" content="2400"><meta property="og:image:height" content="1260"><meta property="og:image:alt" content="Salón Recreativo: colección de minijuegos online">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(HT)}"><meta name="twitter:description" content="{e(HD)}"><meta name="twitter:image" content="{BASE}img/og-home.jpg">
{jd(site)}
{jd(lst)}
"""
# directorio de enlaces en el pie
bycat={}
for g in play:bycat.setdefault(g['cat'],[]).append(g)
cols=''
for k in ['cosmico']+ORDER:
    if k not in bycat:continue
    cols+=f'<div><h2>{e(CATS[k]["n"])}</h2><ul>'+''.join(f'<li><a href="jugar/{g["slug"]}/">{e(g["name"])}</a></li>' for g in bycat[k])+'</ul></div>'
about=f'<p>Salón Recreativo es una colección de {len(G)} minijuegos online y gratis hechos con HTML y Three.js: fútbol, juegos de ritmo musical, karts, montañas rusas, juegos relajantes y juegos de palabras en catalán. Todos se juegan en el navegador, en móvil y ordenador, sin descargas ni registro.</p>'
nav=f'<nav class="dir" aria-label="Todos los juegos">{cols}</nav>'
fa='Juegos para el navegador <a href="#admin"'
assert fa in body
body=body.replace(fa,'Juegos para el navegador <a href="#admin"',1)
fb='</p></div>\n</footer>'
assert body.count(fb)==1
body=body.replace(fb,'</p>'+about+nav+'</div>\n</footer>')
out='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>*,*::before,*::after{box-sizing:border-box}body{margin:0}</style>\n'+meta+head_part+'</head><body>'+body+'</body></html>'
open(os.path.join(root,'index.html'),'w',encoding='utf-8').write(out)
# ---------- sitemap / robots / 404 ----------
urls=[BASE]+[BASE+'jugar/'+g['slug']+'/' for g in play]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{"weekly" if u==BASE else "monthly"}</changefreq><priority>{"1.0" if u==BASE else "0.7"}</priority></url>\n' for u in urls)+'</urlset>\n'
open(os.path.join(root,'sitemap.xml'),'w',encoding='utf-8').write(sm)
open(os.path.join(root,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
open(os.path.join(root,'404.html'),'w',encoding='utf-8').write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Página no encontrada | Salón Recreativo</title><meta name="robots" content="noindex"><style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#0d1230;color:#eef1ff;font:18px system-ui;text-align:center}}a{{color:#ffc933}}</style></head><body><div><h1>Esta página no existe</h1><p><a href="{BASE}">Volver al Salón Recreativo</a></p></div></body></html>')
print('ok',len(play),'paginas')
