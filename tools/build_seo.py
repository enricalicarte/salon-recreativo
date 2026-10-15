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
.stage .bgv{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
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
    kw=g.get('kw')
    if kw:
        K=kw[0].upper()+kw[1:]
        suf=' gratis' if (ca or 'online' in kw) else ' online gratis'
        title=f"{K}{suf}" if g['name'].lower() in kw.lower() else f"{K}{suf}: {g['name']}"
        if len(title)<=44:title+=' | Salón Recreativo'
    else:
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
        p1=f"{g['name']} és un {kw or gtype} que pots jugar en línia i gratis, directament al navegador, des del mòbil o l'ordinador. No cal instal·lar res ni crear cap compte."
        p2="Forma part del Salón Recreativo, una col·lecció de minijocs en línia."
        h2a='Com es juga';ptxt="Prem «Jugar» i comença: el joc carrega aquí mateix. Per a una millor experiència, obre'l a pantalla completa."
        reltitle='Més minijocs'
    else:
        p1=f"{g['name']}{note} es un {kw or gtype} para jugar online y gratis, directamente en el navegador, desde el móvil o el ordenador. No hay que instalar nada ni crear una cuenta."
        p2=("Forma parte del Salón Recreativo, una colección de minijuegos online. "+(cd.get('d','') if cd else ''))
        h2a='Cómo se juega';ptxt="Pulsa «Jugar» y empieza: el juego se carga aquí mismo. Para una mejor experiencia ábrelo a pantalla completa o en una pestaña nueva."
        reltitle='Más minijuegos'
    jgame={"@context":"https://schema.org","@type":"VideoGame","name":g['name'],"description":g['blurb'],"url":url,"image":img,"genre":cat,"gamePlatform":"Web browser","applicationCategory":"Game","operatingSystem":"Any","inLanguage":lang,"isAccessibleForFree":True,"offers":{"@type":"Offer","price":"0","priceCurrency":"EUR"},"author":{"@type":"Organization","name":"Alica Games Studio","url":BASE},"keywords":", ".join(([kw] if kw else [])+g['tags'])}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Salón Recreativo","item":BASE},{"@type":"ListItem","position":2,"name":cat,"item":BASE+'#sec-'+g['cat']},{"@type":"ListItem","position":3,"name":g['name'],"item":url}]}
    relhtml=''.join(f'<li><a href="../{x["slug"]}/"><img src="../../img/{x["slug"]}.jpg" alt="Portada de {e(x["name"])}" loading="lazy" width="344" height="216"><b>{e(x["name"])}</b></a></li>' for x in rel)
    page=f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0d1230"><meta name="author" content="Alica Games Studio">
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
<div class="stage" id="stage">{('<video class="bgv" autoplay muted loop playsinline preload="metadata" poster="../../media/'+g['slug']+'.jpg"><source src="../../media/'+g['slug']+'.webm" type="video/webm"><source src="../../media/'+g['slug']+'.mp4" type="video/mp4"></video>') if os.path.exists(os.path.join(root,'media',g['slug']+'.mp4')) else ''}<button class="go" id="go" type="button" style="background-image:linear-gradient(rgba(13,18,48,.25),rgba(13,18,48,.25)){'' if os.path.exists(os.path.join(root,'media',g['slug']+'.mp4')) else ',url(../../img/'+g['slug']+'.jpg)'}" aria-label="Jugar a {e(g['name'])}"><span>▶ Jugar</span></button></div>
<noscript><p><a href="../../{g['play']}">Abrir {e(g['name'])}</a></p></noscript>
<p><a href="../../{g['play']}" target="_blank" rel="noopener">{'Obrir en una pestanya nova' if ca else 'Abrir en una pestaña nueva'} ↗</a></p>
<ul class="tags">{''.join('<li>'+e(t)+'</li>' for t in g['tags'])}</ul>
<h2>{'Sobre' if ca else 'Sobre'} {e(g['name'])}</h2>
<p>{e(p1)}</p><p>{e(p2)}</p>
<h2>{h2a}</h2><p>{e(ptxt)}</p>
<h2>{reltitle}</h2>
<ul class="rel">{relhtml}</ul>
</main>
<footer><div class="w"><a href="../../">Salón Recreativo</a> · {'Minijocs en línia gratuïts' if ca else 'Minijuegos online gratis'} · © 2026 <b>Alica Games Studio</b></div></footer>
<script>document.getElementById('go').addEventListener('click',function(){{var f=document.createElement('iframe');f.src='../../{g['play']}';f.title={json.dumps(g['name'],ensure_ascii=False)};f.allow='fullscreen; autoplay; gamepad; accelerometer; gyroscope';f.allowFullscreen=true;var s=document.getElementById('stage');s.innerHTML='';s.appendChild(f);}});</script>
</body></html>"""
    d=os.path.join(root,'jugar',g['slug']);os.makedirs(d,exist_ok=True)
    open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(page)
# ---------- páginas temáticas (hubs) ----------
CA_BLURB={'verano':"Joc narratiu en català amb gràfics d'aquarel·la: un nen passa l'estiu amb el seu avi vora el mar, a Caldes d'Estrac. Trenta dies, minijocs i cançons."}
HUBS=[
 dict(slug='jocs-en-catala',lang='ca',title='Jocs en català online i gratis | Salón Recreativo',h1='Jocs en català online i gratis',
  desc='Jocs de paraules en català per jugar al navegador: Wordle en català, penjat, sopa de lletres, anagrames, accents i castellanismes. Gratis i sense anuncis.',
  intro=['Una col·lecció de jocs en català per jugar online, al mòbil o a l\'ordinador, sense instal·lar res ni registrar-se. Hi ha jocs de paraules per a tota la família: el Wordle en català (Motle), el penjat, la sopa de lletres, anagrames, un joc d\'accents i un de castellanismes.',
         'Són partides curtes, d\'un o dos minuts, pensades per practicar l\'ortografia i el vocabulari mentre jugues. També hi trobaràs L\'últim estiu, un joc narratiu en català.'],
  pick=lambda g:g['cat']=='catquiz' or g['id']=='verano'),
 dict(slug='juegos-relajantes',lang='es',title='Juegos relajantes online gratis y sin anuncios | Salón Recreativo',h1='Juegos relajantes online',
  desc='18 juegos relajantes online y gratis con música tranquila: jardín zen, estanque de koi, hoguera, lluvia, aurora boreal y más. Sin puntos, sin prisa y sin anuncios.',
  intro=['Dieciocho juegos relajantes para jugar en el navegador cuando necesitas desconectar unos minutos. No hay puntos, ni tiempo límite, ni forma de perder: solo tocar, mirar y escuchar.',
         'Cada juego tiene su propia música generativa, que nunca suena igual: rastrilla un jardín zen, da de comer a los koi, suelta farolillos sobre un lago o despierta una aurora boreal. Funcionan en móvil y ordenador, sin descargas.'],
  pick=lambda g:g['cat']=='relax'),
 dict(slug='juegos-de-ritmo',lang='es',title='Juegos de ritmo y música online gratis | Salón Recreativo',h1='Juegos de ritmo online',
  desc='Juegos de ritmo y música online gratis: juegos tipo Guitar Hero, de guitarra, un portero al ritmo de la música y más. Para móvil y PC, sin descargas.',
  intro=['Juegos de ritmo musical para jugar en el navegador: pulsa las notas a tiempo en juegos tipo Guitar Hero, toca la guitarra en el año 3000 o para balones al compás de la canción.',
         'Todas las canciones son originales. Se juegan en móvil y ordenador, gratis y sin anuncios.'],
  pick=lambda g:g['id'] in ('martin','supernova','cosmicguitar','paradon','tiradora','constructora','rutacosmica')),

 dict(slug='juegos-de-motor',lang='es',title='Juegos de motos, coches y karts online gratis | Salón Recreativo',h1='Juegos de motos, coches y karts',
  desc='Juegos de motor online gratis: motos con trucos y loopings, monster trucks, karts con turbo, coches por la costa y montañas rusas. Para móvil y PC, sin descargas ni anuncios.',
  intro=['Juegos de motor para jugar en el navegador: haz trucos en el aire con una moto de motocross, salta con un monster truck, derrapa con un kart para cargar el turbo o conduce por una carretera de neón.',
         'Todos funcionan en móvil y ordenador, gratis y sin anuncios. Partidas rápidas para batir tu récord una y otra vez.'],
  pick=lambda g:g['cat']=='motor'),
]
for H in HUBS:
    ca=H['lang']=='ca'
    url=BASE+H['slug']+'/'
    sel=[g for g in play if H['pick'](g)]
    items=[{"@type":"ListItem","position":k+1,"url":BASE+'jugar/'+g['slug']+'/',"name":g['name']} for k,g in enumerate(sel)]
    cards=''.join(f'<li><a href="../jugar/{g["slug"]}/"><img src="../img/{g["slug"]}.jpg" alt="{e(g["name"])}" loading="lazy" width="344" height="216"><b>{e(g["name"])}</b><span>{e(short(CA_BLURB.get(g["id"],g["blurb"]) if ca else g["blurb"],120))}</span></a></li>' for g in sel)
    others=''.join(f'<a href="../{h["slug"]}/">{e(h["h1"])}</a>' for h in HUBS if h is not H)
    page=f"""<!doctype html>
<html lang="{H['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(H['title'])}</title><meta name="description" content="{e(H['desc'])}"><link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#0d1230"><meta name="author" content="Alica Games Studio">
<meta property="og:type" content="website"><meta property="og:site_name" content="Salón Recreativo"><meta property="og:title" content="{e(H['title'])}"><meta property="og:description" content="{e(H['desc'])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}img/{sel[0]['slug']}.jpg">
<meta name="twitter:card" content="summary_large_image">
{jd({"@context":"https://schema.org","@type":"CollectionPage","name":H['h1'],"url":url,"inLanguage":H['lang'],"description":H['desc'],"mainEntity":{"@type":"ItemList","itemListElement":items}})}
<style>{CSS}
.hub{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px;list-style:none;padding:0;margin:26px 0}}
.hub a{{display:flex;flex-direction:column;height:100%;text-decoration:none;color:#fff;background:#151b44;border:1px solid rgba(255,255,255,.13);border-radius:16px;overflow:hidden}}
.hub img{{width:100%;aspect-ratio:1.6;object-fit:cover}}.hub b{{padding:12px 14px 4px}}.hub span{{padding:0 14px 14px;color:#b3bbea;font-size:.92rem}}
.more a{{display:inline-block;margin:0 10px 10px 0}}</style></head>
<body><header class="t"><div class="w"><a href="../">SALÓN RECREATIVO</a></div></header>
<main class="w"><nav class="bc" aria-label="Migas de pan"><a href="../">Inicio</a> › {e(H['h1'])}</nav>
<h1>{e(H['h1'])}</h1>{''.join('<p class="lead">'+e(t)+'</p>' if i==0 else '<p>'+e(t)+'</p>' for i,t in enumerate(H['intro']))}
<ul class="hub">{cards}</ul>
<h2>{'Més col·leccions' if ca else 'Más colecciones'}</h2><p class="more">{others} <a href="../">{'Tots els jocs' if ca else 'Todos los juegos'}</a></p>
</main><footer><div class="w"><a href="../">Salón Recreativo</a> · © 2026 <b>Alica Games Studio</b></div></footer></body></html>"""
    os.makedirs(os.path.join(root,H['slug']),exist_ok=True)
    open(os.path.join(root,H['slug'],'index.html'),'w',encoding='utf-8').write(page)
# ---------- home ----------
src=open(os.path.join(root,'tools/source.html'),encoding='utf-8').read()
i=src.index('</style>')+8
head_part=src[:i];body=src[i:]
head_part=re.sub(r'<title>.*?</title>\s*','',head_part,flags=re.S)
head_part=re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\s*','',head_part)
HT='Minijuegos online gratis y sin anuncios | Salón Recreativo'
HD=f'{len(G)} minijuegos online gratis y sin anuncios: juegos relajantes, de ritmo, karts, fútbol y juegos de palabras en catalán. En el navegador, móvil y PC, sin descargas.'
HD=short(HD,158)
items=[{"@type":"ListItem","position":k+1,"url":BASE+'jugar/'+g['slug']+'/',"name":g['name']} for k,g in enumerate(play)]
site={"@context":"https://schema.org","@type":"WebSite","name":"Salón Recreativo","url":BASE,"inLanguage":"es","description":HD,"publisher":{"@type":"Organization","name":"Alica Games Studio","url":BASE}}
lst={"@context":"https://schema.org","@type":"ItemList","name":"Minijuegos online gratis","itemListElement":items}
meta=f"""<title>{e(HT)}</title>
<meta name="description" content="{e(HD)}">
<link rel="canonical" href="{BASE}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0d1230"><meta name="author" content="Alica Games Studio">
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
hubl=' · '.join(f'<a href="{H["slug"]}/">{e(H["h1"])}</a>' for H in HUBS)
about=f'<p>Salón Recreativo es una colección de {len(G)} minijuegos online y gratis hechos con HTML y Three.js: fútbol, juegos de ritmo musical, karts, montañas rusas, juegos relajantes y juegos de palabras en catalán. Todos se juegan en el navegador, en móvil y ordenador, sin descargas ni registro.</p><p>'+hubl+'</p>'
nav=f'<nav class="dir" aria-label="Todos los juegos">{cols}</nav>'
fb='</p></div>\n</footer>'
assert body.count(fb)==1
body=body.replace(fb,'</p>'+about+nav+'</div>\n</footer>')
out='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>*,*::before,*::after{box-sizing:border-box}body{margin:0}</style>\n'+meta+head_part+'</head><body>'+body+'</body></html>'
open(os.path.join(root,'index.html'),'w',encoding='utf-8').write(out)
# ---------- sitemap / robots / 404 ----------
urls=[BASE]+[BASE+H['slug']+'/' for H in HUBS]+[BASE+'jugar/'+g['slug']+'/' for g in play]
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{"weekly" if u==BASE else "monthly"}</changefreq><priority>{"1.0" if u==BASE else "0.7"}</priority></url>\n' for u in urls)+'</urlset>\n'
open(os.path.join(root,'sitemap.xml'),'w',encoding='utf-8').write(sm)
open(os.path.join(root,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
open(os.path.join(root,'404.html'),'w',encoding='utf-8').write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Página no encontrada | Salón Recreativo</title><meta name="robots" content="noindex"><style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#0d1230;color:#eef1ff;font:18px system-ui;text-align:center}}a{{color:#ffc933}}</style></head><body><div><h1>Esta página no existe</h1><p><a href="{BASE}">Volver al Salón Recreativo</a></p></div></body></html>')
print('ok',len(play),'paginas')
