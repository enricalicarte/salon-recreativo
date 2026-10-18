#!/usr/bin/env python3
"""Genera la web publicable a partir de tools/source.html y tools/games.json:
index.html, jugar/<slug>/ (una ficha por juego),
páginas temáticas, Sobre el estudio, páginas legales, sitemap.xml, robots.txt, 404.html,
manifest.webmanifest y sw.js (app instalable).
Uso: python3 tools/build_seo.py   (desde la raíz del repo)."""
import json, re, html, os, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n import CA_G, ES_CQ, CA_CATS, CA_CATD, CA_UI

# ================= CONFIGURACIÓN =================
BASE = 'https://enricalicarte.github.io/salon-recreativo/'
# Mientras sea False, ninguna página se indexa. Al lanzar en el dominio definitivo: cambiar BASE, poner True y regenerar.
INDEXABLE = False
# Titular de la web (aviso legal y privacidad). Lo que quede vacío aparece como [pendiente].
OWNER = dict(name='', nif='', addr='', email='')
# Analítica sin cookies: código de GoatCounter (p. ej. 'alicagames' para alicagames.goatcounter.com). Vacío = apagada.
GOATCOUNTER = ''
# =================================================

ROBOTS = 'index,follow,max-image-preview:large' if INDEXABLE else 'noindex,nofollow'
TODAY = datetime.date.today().isoformat()
UPDATED = '16 de octubre de 2026'
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(root, 'tools/games.json'), encoding='utf-8'))
G, CATS, CATD = D['GAMES'], D['CATS'], D['CATD']
e = lambda x: html.escape(str(x), quote=True)
play = [g for g in G if g.get('play')]
ORDER = ['accion', 'puzles', 'deporte', 'ritmo', 'motor', 'historias', 'marca', 'relax', 'catquiz']
EMAIL = OWNER['email']
PEND = '<mark class="pend">[pendiente]</mark>'
AGE = {'olimpiadas': 3, 'aventura': 3, 'towerstack': 3, 'miramar': 16}
age = lambda g: AGE.get(g['id'], 3 if g['cat'] == 'relax' else 7)
has_media = lambda g: os.path.exists(os.path.join(root, 'media', g['slug'] + '.mp4'))

def short(t, n):
    t = t.strip()
    return t if len(t) <= n else t[:n - 1].rsplit(' ', 1)[0].rstrip('.,;:') + '…'
def jd(o): return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(',', ':')) + '</script>'
def W(path, txt):
    p = os.path.join(root, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(txt)

def loc(g, lang):
    """Textos de un juego en el idioma pedido."""
    x = dict(g)
    if lang == 'ca':
        x.update(CA_G.get(g['id'], {}))
    elif g['cat'] == 'catquiz':
        x.update(ES_CQ.get(g['id'], {}))
    return x

def gc(prefix=''):
    return f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>' if GOATCOUNTER else ''

def pwa(p):
    return (f'<link rel="manifest" href="{p}manifest.webmanifest"><link rel="icon" href="{p}icons/favicon.svg" type="image/svg+xml"><link rel="icon" href="{p}icons/favicon-32.png" sizes="32x32" type="image/png">'
            f'<link rel="apple-touch-icon" href="{p}icons/apple-touch-icon.png"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">'
            '<meta name="apple-mobile-web-app-title" content="Salón"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">')

GENRE = {'entrenos': 'sesión de entrenamiento de fútbol', 'invierno': 'juego de deportes de invierno', 'accion': 'juego de acción', 'puzles': 'juego de puzles', 'deporte': 'juego de deporte', 'ritmo': 'juego de ritmo musical', 'motor': 'juego de motor', 'historias': 'juego narrativo', 'marca': 'juego con marca', 'relax': 'juego relajante', 'cosmico': 'juego cósmico', 'catquiz': 'juego de palabras en catalán'}
GENRE_CA = {'entrenos': "sessió d'entrenament de futbol", 'invierno': "joc d'esports d'hivern", 'accion': "joc d'acció", 'puzles': 'joc de trencaclosques', 'deporte': "joc d'esport", 'ritmo': 'joc de ritme musical', 'motor': 'joc de motor', 'historias': 'joc narratiu', 'marca': 'joc amb marca', 'relax': 'joc relaxant', 'cosmico': 'joc còsmic', 'catquiz': 'joc de paraules en català'}

# ---------- estilos de las páginas interiores ----------
CSS = """*{box-sizing:border-box}html{color-scheme:dark}body{margin:0;background:#07060f;color:#f5f2ff;font:16px/1.65 'Onest',system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased}a{color:#ffd23f}
.w{max-width:1000px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left)) 0 max(16px,env(safe-area-inset-right))}
header.t{position:sticky;top:0;z-index:5;background:rgba(7,6,15,.82);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,.1)}
header.t .w{display:flex;align-items:center;justify-content:space-between;gap:12px;height:60px}
header.t .br{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font:700 .8rem/1 'Unbounded',system-ui,sans-serif;letter-spacing:.06em;white-space:nowrap}
header.t .br i{width:12px;height:12px;border-radius:50%;background:conic-gradient(#ffd23f,#ff4fa3,#38e5ff,#ffd23f)}
header.t nav{display:flex;gap:8px;align-items:center}
header.t nav a{color:#a79fcb;text-decoration:none;font-size:.88rem;padding:8px 12px;border-radius:999px;border:1px solid rgba(255,255,255,.12);white-space:nowrap}
header.t nav a:hover{color:#fff;border-color:#ffd23f}
@media (max-width:520px){header.t nav a.hide{display:none}}
nav.bc{font-size:.85rem;color:#a79fcb;margin:22px 0 8px}nav.bc a{color:#a79fcb}
h1,h2,h3{font-family:'Unbounded',system-ui,sans-serif;font-weight:700;letter-spacing:-.01em}
h1{font-size:clamp(1.9rem,6vw,3.1rem);line-height:1.08;margin:.2em 0 .35em}
h2{margin:1.8em 0 .5em;font-size:clamp(1.15rem,3vw,1.45rem);line-height:1.2}
h3{font-size:1.02rem;margin:1.4em 0 .3em}
.lead{font-size:1.15rem;color:#e2ddf7}
p,li{color:#d6d1ee}
.stage{position:relative;width:100%;aspect-ratio:16/10;max-height:78vh;border-radius:20px;overflow:hidden;background:#000;border:1px solid rgba(255,255,255,.14)}
.stage iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.stage .bgv{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
video::-webkit-media-controls,video::-webkit-media-controls-start-playback-button,video::-webkit-media-controls-overlay-play-button{display:none!important;-webkit-appearance:none}
.stage .go{position:absolute;inset:0;display:grid;place-items:center;border:0;cursor:pointer;color:#07060f;background:center/cover}
.go span{background:#ffd23f;font:700 1.1rem 'Unbounded',system-ui;padding:16px 34px;border-radius:99px;box-shadow:0 8px 30px rgba(0,0,0,.5)}
.tags{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0}.tags li{border:1px solid rgba(255,255,255,.22);border-radius:99px;padding:3px 12px;font-size:.85rem;color:#a79fcb}
.tags li.age{color:#fff;border-color:#ffd23f}
.acts{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:18px 0}
.sh{display:inline-flex;align-items:center;gap:8px;font:600 .88rem 'Onest',system-ui;color:#fff;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:9px 15px;text-decoration:none;cursor:pointer}
.sh:hover{border-color:#ffd23f}.sh i{width:9px;height:9px;border-radius:50%;background:var(--c,#ffd23f)}
.rel{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(46%,210px),1fr));gap:16px;list-style:none;padding:0}
.rel a{display:block;text-decoration:none;color:#fff;background:#171232;border:1px solid rgba(255,255,255,.1);border-radius:16px;overflow:hidden}.rel a:hover{border-color:#ffd23f}
.rel img{width:100%;display:block;aspect-ratio:1.6;object-fit:cover}.rel b{display:block;padding:10px 12px;font-weight:600}
footer.f{margin:70px 0 0;padding:30px 0 calc(40px + env(safe-area-inset-bottom,0px));border-top:1px solid rgba(255,255,255,.1);background:#110d22;color:#a79fcb;font-size:.9rem}
footer.f p{margin:0 0 10px;color:#a79fcb}footer.f a{color:#a79fcb}footer.f a:hover{color:#fff}
footer.f .fl{display:flex;flex-wrap:wrap;gap:6px 18px}
.toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#fff;color:#07060f;padding:10px 16px;border-radius:12px;font-weight:600;opacity:0;transition:opacity .3s}.toast.on{opacity:1}
mark.pend{background:#ffd23f;color:#07060f;padding:0 4px;border-radius:4px}
.card{background:#171232;border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:22px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:16px}.card h3{margin-top:0}
.btn{display:inline-flex;align-items:center;gap:10px;font:600 1rem 'Onest',system-ui;text-decoration:none;border-radius:999px;padding:14px 24px;cursor:pointer;border:1px solid transparent;background:#ffd23f;color:#07060f}
.btn.g{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.18);color:#fff}
.legal h2{font-size:1.1rem}.legal p,.legal li{font-size:.98rem}"""

SHARE_JS = """<script>(function(){var u=location.href.split('#')[0],t=document.title.split(' | ')[0];var b=document.getElementById('shN');if(b&&navigator.share)b.hidden=false;
document.addEventListener('click',function(e){var a=e.target.closest('[data-sh]');if(!a)return;var k=a.getAttribute('data-sh');
if(k==='n'){navigator.share({title:t,url:u}).catch(function(){});return;}
if(k==='c'){e.preventDefault();var ok=function(){var d=document.createElement('div');d.className='toast';d.textContent=a.getAttribute('data-ok');document.body.appendChild(d);requestAnimationFrame(function(){d.classList.add('on')});setTimeout(function(){d.remove()},2000)};try{navigator.clipboard.writeText(u).then(ok,function(){prompt('',u)})}catch(x){prompt('',u)}return;}
var m={w:'https://wa.me/?text='+encodeURIComponent(t+' '+u),t:'https://t.me/share/url?url='+encodeURIComponent(u)+'&text='+encodeURIComponent(t),x:'https://twitter.com/intent/tweet?url='+encodeURIComponent(u)+'&text='+encodeURIComponent(t)};
if(m[k]){e.preventDefault();window.open(m[k],'_blank','noopener');}});})();</script>"""

def share_bar(ca):
    return ('<div class="acts" aria-label="' + ('Comparteix' if ca else 'Compartir') + '">'
            f'<button class="sh" type="button" id="shN" data-sh="n" hidden><i></i>{"Comparteix" if ca else "Compartir"}</button>'
            '<a class="sh" href="#" data-sh="w" style="--c:#25d366"><i></i>WhatsApp</a>'
            '<a class="sh" href="#" data-sh="t" style="--c:#2aabee"><i></i>Telegram</a>'
            '<a class="sh" href="#" data-sh="x" style="--c:#fff"><i></i>X</a>'
            f'<a class="sh" href="#" data-sh="c" data-ok="{"Enllaç copiat" if ca else "Enlace copiado"}"><i></i>{"Copia l’enllaç" if ca else "Copiar enlace"}</a></div>')

def header(p, ca, alt=None):
    """p: prefijo hasta la raíz. alt: enlace a la otra versión de idioma."""
    home = p
    lng = f'<a href="{alt}" hreflang="{"es" if ca else "ca"}" lang="{"es" if ca else "ca"}">{"ES" if ca else "CA"}</a>' if alt else ''
    return (f'<header class="t"><div class="w"><a class="br" href="{home}"><i></i>SALÓN RECREATIVO</a><nav>'
            f'<a href="{home}">{"Tots els jocs" if ca else "Todos los juegos"}</a>{lng}</nav></div></header>')

def footer(p, ca):
    return (f'<footer class="f"><div class="w"><p>© 2026 <b>Alica Games Studio</b> · Salón Recreativo · {"Minijocs en línia gratuïts" if ca else "Minijuegos online gratis"}</p>'
            f'<p class="fl"><a href="{p}estudio/">{"Sobre l’estudi" if ca else "Sobre el estudio"}</a>'
            f'<a href="{p}aviso-legal/">{"Avís legal" if ca else "Aviso legal"}</a><a href="{p}privacidad/">{"Privacitat" if ca else "Privacidad"}</a><a href="{p}cookies/">Cookies</a></p></div></footer>')

def head(lang, title, desc, url, p, img=None, alts=None, robots=None, extra=''):
    al = ''.join(f'<link rel="alternate" hreflang="{k}" href="{v}">' for k, v in (alts or {}).items())
    img = img or BASE + 'img/og-home.jpg'
    return (f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            f'<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">{al}\n'
            f'<meta name="robots" content="{robots or ROBOTS}"><meta name="theme-color" content="#07060f"><meta name="author" content="Alica Games Studio">\n'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Salón Recreativo"><meta property="og:locale" content="{"ca_ES" if lang == "ca" else "es_ES"}">'
            f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img}">\n'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{img}">\n'
            f'<link rel="stylesheet" href="{p}assets/fonts.css">{pwa(p)}{gc()}{extra}')

# ================= FICHAS DE JUEGO =================
def landing(g0, lang):
    ca = lang == 'ca'
    g = loc(g0, lang)
    p = '../../../' if ca else '../../'
    path = ('ca/' if ca else '') + 'jugar/' + g['slug'] + '/'
    url = BASE + path
    alts = None
    img = BASE + 'img/' + g['slug'] + '.jpg'
    cat = (CA_CATS if ca else {k: v['n'] for k, v in CATS.items()})[g['cat']]
    cd = (CA_CATD if ca else CATD).get(g['cat'], {})
    kw = g.get('kw')
    if kw:
        K = kw[0].upper() + kw[1:]
        if ca: suf = ' gratis' if (g['cat'] == 'catquiz' or 'línia' in kw) else ' en línia gratis'
        else: suf = ' gratis' if 'online' in kw else ' online gratis'
        title = f"{K}{suf}" if g['name'].lower() in kw.lower() else f"{K}{suf}: {g['name']}"
        if len(title) <= 44: title += ' | Salón Recreativo'
    else:
        title = g['name'] + (' — joc en línia gratuït' if ca else ' — juego online gratis') + ' | Salón Recreativo'
    suf = ' Juga gratis al navegador, sense descàrregues.' if ca else ' Juega gratis en el navegador, sin descargas, en móvil y PC.'
    desc = short(g['blurb'].rstrip('.') + '.' + suf, 158)
    rel = [x for x in play if x['cat'] == g['cat'] and x['slug'] != g['slug']]
    if len(rel) < 4: rel += [x for x in play if x['cat'] != g['cat'] and x['slug'] != g['slug']][:4 - len(rel)]
    rel = [loc(x, lang) for x in rel[:6]]
    note = (' (' + g['note'] + ')') if g.get('note') else ''
    if ca:
        p1 = f"{g['name']} és un {kw or GENRE_CA.get(g['cat'], 'joc')} que pots jugar {'' if 'línia' in (kw or '') else 'en línia i '}gratis, directament al navegador, des del mòbil o l'ordinador. No cal instal·lar res ni crear cap compte."
        p2 = "Forma part del Salón Recreativo, una col·lecció de minijocs en línia d'Alica Games Studio. " + cd.get('d', '')
        h2a, ptxt, reltitle = 'Com es juga', "Prem «Juga» i comença: el joc es carrega aquí mateix. Al mòbil s'obre a pantalla completa.", 'Més minijocs'
        agel = f'Edat recomanada: +{age(g)}'
    else:
        p1 = f"{g['name']}{note} es un {kw or GENRE.get(g['cat'], 'juego')} para jugar {'' if 'online' in (kw or '') else 'online y '}gratis, directamente en el navegador, desde el móvil o el ordenador. No hay que instalar nada ni crear una cuenta."
        p2 = "Forma parte del Salón Recreativo, una colección de minijuegos online de Alica Games Studio. " + cd.get('d', '')
        h2a, ptxt, reltitle = 'Cómo se juega', "Pulsa «Jugar» y empieza: el juego se carga aquí mismo. En el móvil se abre a pantalla completa.", 'Más minijuegos'
        agel = f'Edad recomendada: +{age(g)}'
    jgame = {"@context": "https://schema.org", "@type": "VideoGame", "name": g['name'], "description": g['blurb'], "url": url, "image": img, "genre": cat, "gamePlatform": "Web browser", "applicationCategory": "Game", "operatingSystem": "Any", "inLanguage": 'ca' if (ca or g['cat'] == 'catquiz' or g['id'] == 'verano') else 'es', "isAccessibleForFree": True, "typicalAgeRange": f"{age(g)}-", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "author": {"@type": "Organization", "name": "Alica Games Studio", "url": BASE + 'estudio/'}, "keywords": ", ".join(([kw] if kw else []) + g['tags'])}
    home = BASE + ('ca/' if ca else '')
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Salón Recreativo", "item": home}, {"@type": "ListItem", "position": 2, "name": cat, "item": home + '#sec-' + g['cat']}, {"@type": "ListItem", "position": 3, "name": g['name'], "item": url}]}
    relhtml = ''.join(f'<li><a href="../{x["slug"]}/"><img src="{p}img/{x["slug"]}.jpg" alt="{"Portada de" if not ca else "Portada de"} {e(x["name"])}" loading="lazy" width="344" height="216"><b>{e(x["name"])}</b></a></li>' for x in rel)
    hm = has_media(g)
    vid = (f'<video class="bgv" autoplay muted loop playsinline disablepictureinpicture disableremoteplayback preload="metadata" poster="{p}media/{g["slug"]}.jpg"><source src="{p}media/{g["slug"]}.webm" type="video/webm"><source src="{p}media/{g["slug"]}.mp4" type="video/mp4"></video>') if hm else ''
    other = (BASE + 'jugar/' + g['slug'] + '/') if ca else (BASE + 'ca/jugar/' + g['slug'] + '/')
    other_rel = (p + 'jugar/' + g['slug'] + '/') if ca else (p + 'ca/jugar/' + g['slug'] + '/')
    page = head(lang, title, desc, url, p, img, alts) + jd(jgame) + jd(bc) + f"""
<style>{CSS}</style></head>
<body>{header(p, ca)}
<main class="w">
<nav class="bc" aria-label="{'Molles de pa' if ca else 'Migas de pan'}"><a href="{p}{'ca/' if ca else ''}">{'Inici' if ca else 'Inicio'}</a> › <a href="{p}{'ca/' if ca else ''}#{ {'cosmico': 'trilogia', 'invierno': 'saga-invierno', 'entrenos': 'saga-entrenos'}.get(g['cat'], 'sec-' + g['cat']) }">{e(cat)}</a> › {e(g['name'])}</nav>
<h1>{e(g['name'])}</h1>
<p class="lead">{e(g['blurb'])}</p>
<div class="stage" id="stage">{vid}<button class="go" id="go" type="button" style="background-image:linear-gradient(rgba(7,6,15,.25),rgba(7,6,15,.25)){'' if hm else ',url(' + p + 'img/' + g['slug'] + '.jpg)'}" aria-label="{'Juga a' if ca else 'Jugar a'} {e(g['name'])}"><span>▶ {'Juga' if ca else 'Jugar'}</span></button></div>
<noscript><p><a href="{p}{g['play']}">{'Obre' if ca else 'Abrir'} {e(g['name'])}</a></p></noscript>
{share_bar(ca)}
<p><a href="{p}{g['play']}" target="_blank" rel="noopener">{'Obrir en una pestanya nova' if ca else 'Abrir en una pestaña nueva'} ↗</a></p>
<ul class="tags"><li class="age">{agel}</li>{''.join('<li>' + e(t) + '</li>' for t in g['tags'])}</ul>
<h2>Sobre {e(g['name'])}</h2>
<p>{e(p1)}</p><p>{e(p2)}</p>
<h2>{h2a}</h2><p>{e(ptxt)}</p>
<h2>{reltitle}</h2>
<ul class="rel">{relhtml}</ul>
</main>
{footer(p, ca)}
<script>document.getElementById('go').addEventListener('click',function(){{var f=document.createElement('iframe');f.src='{p}{g['play']}';f.title={json.dumps(g['name'], ensure_ascii=False)};f.allow='fullscreen; autoplay; gamepad; accelerometer; gyroscope';f.allowFullscreen=true;var s=document.getElementById('stage');s.innerHTML='';s.appendChild(f);try{{if(window.goatcounter&&goatcounter.count)goatcounter.count({{path:'jugar/{g['slug']}',title:{json.dumps(g['name'], ensure_ascii=False)},event:true}})}}catch(x){{}}if(matchMedia('(pointer:coarse)').matches){{try{{var fs=s.requestFullscreen||s.webkitRequestFullscreen;if(fs){{var pr=fs.call(s);if(pr&&pr.catch)pr.catch(function(){{}});}}}}catch(e){{}}}}}});</script>
{SHARE_JS}
</body></html>"""
    W(path + 'index.html', page)

for g in play:
    landing(g, 'es')

# ================= PÁGINAS TEMÁTICAS =================
HUBS = [
 dict(slug='jocs-en-catala', lang='ca', title='Jocs en català online i gratis | Salón Recreativo', h1='Jocs en català online i gratis',
  desc='Jocs de paraules en català per jugar al navegador: Wordle en català, penjat, sopa de lletres, anagrames, accents i castellanismes. Gratis i sense anuncis.',
  intro=["Una col·lecció de jocs en català per jugar online, al mòbil o a l'ordinador, sense instal·lar res ni registrar-se. Hi ha jocs de paraules per a tota la família: el Wordle en català (Motle), el penjat, la sopa de lletres, anagrames, un joc d'accents i un de castellanismes.",
         "Són partides curtes, d'un o dos minuts, pensades per practicar l'ortografia i el vocabulari mentre jugues. També hi trobaràs L'últim estiu, un joc narratiu en català."],
  pick=lambda g: g['cat'] == 'catquiz' or g['id'] == 'verano'),
 dict(slug='juegos-relajantes', lang='es', title='Juegos relajantes online gratis y sin anuncios | Salón Recreativo', h1='Juegos relajantes online',
  desc='18 juegos relajantes online y gratis con música tranquila: jardín zen, estanque de koi, hoguera, lluvia, aurora boreal y más. Sin puntos, sin prisa y sin anuncios.',
  intro=['Dieciocho juegos relajantes para jugar en el navegador cuando necesitas desconectar unos minutos. No hay puntos, ni tiempo límite, ni forma de perder: solo tocar, mirar y escuchar.',
         'Cada juego tiene su propia música generativa, que nunca suena igual: rastrilla un jardín zen, da de comer a los koi, suelta farolillos sobre un lago o despierta una aurora boreal. Funcionan en móvil y ordenador, sin descargas.'],
  pick=lambda g: g['cat'] == 'relax'),
 dict(slug='juegos-de-ritmo', lang='es', title='Juegos de ritmo y música online gratis | Salón Recreativo', h1='Juegos de ritmo online',
  desc='Juegos de ritmo y música online gratis: juegos tipo Guitar Hero, de guitarra, un portero al ritmo de la música y más. Para móvil y PC, sin descargas.',
  intro=['Juegos de ritmo musical para jugar en el navegador: pulsa las notas a tiempo en juegos tipo Guitar Hero, toca la guitarra en el año 3000 o para balones al compás de la canción.',
         'Todas las canciones son originales. Se juegan en móvil y ordenador, gratis y sin anuncios.'],
  pick=lambda g: g['id'] in ('martin', 'supernova', 'cosmicguitar', 'cabina', 'paradon', 'tiradora', 'constructora', 'rutacosmica')),
 dict(slug='juegos-de-motor', lang='es', title='Juegos de motos, coches y karts online gratis | Salón Recreativo', h1='Juegos de motos, coches y karts',
  desc='Juegos de motor online gratis: motos con trucos y loopings, monster trucks, karts con turbo, coches por la costa y montañas rusas. Para móvil y PC, sin descargas ni anuncios.',
  intro=['Juegos de motor para jugar en el navegador: haz trucos en el aire con una moto de motocross, salta con un monster truck, derrapa con un kart para cargar el turbo o conduce por una carretera de neón.',
         'Todos funcionan en móvil y ordenador, gratis y sin anuncios. Partidas rápidas para batir tu récord una y otra vez.'],
  pick=lambda g: g['cat'] == 'motor'),
 dict(slug='juegos-de-puzles', lang='es', title='Juegos de puzles online gratis | Salón Recreativo', h1='Juegos de puzles online',
  desc='Juegos de puzles online gratis: crucigrama con rueda de letras, puzle de bloques de neón y torres para apilar. Para móvil y PC, sin descargas ni anuncios.',
  intro=['Juegos de puzles para jugar en el navegador: forma palabras girando una rueda de letras, encaja bloques para completar filas y columnas o apila una torre lo más alta posible.',
         'Partidas cortas para pensar un poco y batir tu récord. Funcionan en móvil y ordenador, gratis y sin anuncios.'],
  pick=lambda g: g['cat'] == 'puzles'),
]
HUB_CSS = """.hub{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px;list-style:none;padding:0;margin:26px 0}
.hub a{display:flex;flex-direction:column;height:100%;text-decoration:none;color:#fff;background:#171232;border:1px solid rgba(255,255,255,.1);border-radius:18px;overflow:hidden}.hub a:hover{border-color:#ffd23f}
.hub img{width:100%;aspect-ratio:1.6;object-fit:cover}.hub b{padding:12px 14px 4px}.hub span{padding:0 14px 14px;color:#a79fcb;font-size:.92rem}
.more a{display:inline-block;margin:0 10px 10px 0}"""
for H in HUBS:
    ca = H['lang'] == 'ca'
    url = BASE + H['slug'] + '/'
    sel = [loc(g, H['lang']) for g in play if H['pick'](g)]
    lp = lambda g: '../jugar/' + g['slug'] + '/'
    items = [{"@type": "ListItem", "position": k + 1, "url": BASE + lp(g)[3:], "name": g['name']} for k, g in enumerate(sel)]
    cards = ''.join(f'<li><a href="{lp(g)}"><img src="../img/{g["slug"]}.jpg" alt="{e(g["name"])}" loading="lazy" width="344" height="216"><b>{e(g["name"])}</b><span>{e(short(g["blurb"], 120))}</span></a></li>' for g in sel)
    others = ''.join(f'<a href="../{h["slug"]}/">{e(h["h1"])}</a>' for h in HUBS if h is not H)
    page = head(H['lang'], H['title'], H['desc'], url, '../', BASE + 'img/' + sel[0]['slug'] + '.jpg') + jd({"@context": "https://schema.org", "@type": "CollectionPage", "name": H['h1'], "url": url, "inLanguage": H['lang'], "description": H['desc'], "mainEntity": {"@type": "ItemList", "itemListElement": items}}) + f"""
<style>{CSS}
{HUB_CSS}</style></head>
<body>{header('../', ca)}
<main class="w"><nav class="bc" aria-label="{'Molles de pa' if ca else 'Migas de pan'}"><a href="../">{'Inici' if ca else 'Inicio'}</a> › {e(H['h1'])}</nav>
<h1>{e(H['h1'])}</h1>{''.join('<p class="lead">' + e(t) + '</p>' if i == 0 else '<p>' + e(t) + '</p>' for i, t in enumerate(H['intro']))}
<ul class="hub">{cards}</ul>
<h2>{'Més col·leccions' if ca else 'Más colecciones'}</h2><p class="more">{others} <a href="../">{'Tots els jocs' if ca else 'Todos los juegos'}</a></p>
</main>{footer('../', ca)}</body></html>"""
    W(H['slug'] + '/index.html', page)

# ================= PÁGINAS DEL ESTUDIO =================
def simple(slug, title, desc, h1, body, robots=None, extra_css='', extra_js=''):
    url = BASE + slug + '/'
    page = head('es', title, desc, url, '../', robots=robots) + f"""
<style>{CSS}{extra_css}</style></head>
<body>{header('../', False)}
<main class="w"><nav class="bc" aria-label="Migas de pan"><a href="../">Inicio</a> › {e(h1)}</nav>
{body}
</main>{footer('../', False)}{extra_js}</body></html>"""
    W(slug + '/index.html', page)

V = lambda x: e(x) if x else PEND
MAIL = (f'<a href="mailto:{e(EMAIL)}">{e(EMAIL)}</a>' if EMAIL else PEND)

# --- Sobre el estudio ---
simple('estudio', 'Sobre Alica Games Studio | Salón Recreativo',
       'Alica Games Studio hace minijuegos para el navegador: gratis, sin anuncios, sin registro y en catalán y castellano. Conoce el estudio detrás del Salón Recreativo.',
       'Sobre el estudio', f"""<h1>Alica Games Studio</h1>
<p class="lead">Somos el estudio detrás del Salón Recreativo: hacemos minijuegos que se juegan en el navegador, al momento, en el móvil o en el ordenador.</p>
<h2>Cómo son nuestros juegos</h2>
<div class="grid2">
<div class="card"><h3>Gratis y sin anuncios</h3><p>Ni anuncios, ni compras dentro del juego, ni registro. Abres y juegas.</p></div>
<div class="card"><h3>Sin descargas</h3><p>Todo funciona en el navegador. Si quieres, puedes instalar el Salón como una app en el móvil.</p></div>
<div class="card"><h3>Para toda la familia</h3><p>Cada juego indica una edad recomendada. Hay juegos para peques a partir de 3 años y juegos relajantes para desconectar.</p></div>
<div class="card"><h3>En catalán y castellano</h3><p>Juegos de palabras en catalán, historias en catalán y una web en los dos idiomas.</p></div>
</div>
<h2>Qué hacemos</h2>
<p>Juegos propios, como la saga cósmica de Lyra y la Patrulla Nova, los juegos de ritmo o los Relax Games, y también juegos hechos para clientes, como SÛO Shop Rush, MNAC Rush o Anguera Superstars.</p>
<h2>Contacto</h2>
<p>Escríbenos a {MAIL}.</p>""")

# --- Aviso legal ---
LEG_CSS = ''
simple('aviso-legal', 'Aviso legal | Salón Recreativo', 'Aviso legal del Salón Recreativo de Alica Games Studio.', 'Aviso legal', f"""<div class="legal">
<h1>Aviso legal</h1>
<p>En cumplimiento del artículo 10 de la Ley 34/2002, de servicios de la sociedad de la información y de comercio electrónico (LSSI-CE), se informa de los datos del titular de este sitio web.</p>
<h2>Titular</h2>
<ul><li>Titular: {V(OWNER['name'])}, que opera con el nombre comercial Alica Games Studio</li><li>NIF: {V(OWNER['nif'])}</li><li>Domicilio: {V(OWNER['addr'])}</li><li>Correo electrónico: {MAIL}</li></ul>
<h2>Objeto</h2>
<p>El Salón Recreativo es una colección de minijuegos que se juegan gratis en el navegador. El acceso es libre y no requiere registro.</p>
<h2>Propiedad intelectual</h2>
<p>Los juegos, los textos, los gráficos, la música y el código de este sitio pertenecen a su titular o se usan con permiso, salvo las marcas de terceros que aparecen en los juegos hechos para clientes (como SÛO, MNAC, PB Anguera o Kings League), que pertenecen a sus respectivos dueños. No está permitido copiar, redistribuir ni explotar comercialmente los juegos sin autorización.</p>
<h2>Responsabilidad</h2>
<p>El titular procura que los juegos funcionen correctamente, pero no garantiza la ausencia de errores ni la disponibilidad continua del servicio. Los enlaces a sitios externos se ofrecen como referencia; el titular no responde de su contenido.</p>
<h2>Menores</h2>
<p>Los juegos indican una edad recomendada orientativa. Recomendamos que los menores jueguen con la supervisión de un adulto.</p>
<h2>Legislación aplicable</h2>
<p>Este aviso se rige por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales que correspondan conforme a la ley.</p>
<p class="note">Última actualización: {UPDATED}.</p></div>""", robots='noindex,follow')

# --- Privacidad ---
simple('privacidad', 'Política de privacidad | Salón Recreativo', 'Qué datos trata el Salón Recreativo y para qué: sin registro, sin cookies y con analítica anónima.', 'Privacidad', f"""<div class="legal">
<h1>Política de privacidad</h1>
<p class="lead">Resumen: para jugar no pedimos ningún dato. No hay registro, no usamos cookies y la analítica es anónima.</p>
<h2>Responsable del tratamiento</h2>
<p>{V(OWNER['name'])} (Alica Games Studio), NIF {V(OWNER['nif'])}, con domicilio en {V(OWNER['addr'])}. Contacto: {MAIL}.</p>
<h2>Qué datos tratamos</h2>
<ul>
<li><b>Si nos escribes</b> (por email): tu nombre, tu email y lo que nos cuentes, solo para responderte. Base legal: tu consentimiento al escribirnos. Los conservamos mientras dure la conversación y, como máximo, dos años.</li>
<li><b>Estadísticas de uso</b>: {'usamos GoatCounter, un servicio de analítica que no usa cookies ni guarda tu dirección IP; solo cuenta visitas y partidas de forma agregada y anónima.' if GOATCOUNTER else 'si activamos estadísticas, será con un servicio sin cookies que no guarda tu dirección IP y solo cuenta visitas y partidas de forma agregada y anónima.'}</li>
<li><b>Favoritos, partidas recientes y récords</b>: se guardan en el almacenamiento local de tu navegador, en tu dispositivo. No nos llegan. Puedes borrarlos desde los ajustes del navegador.</li>
</ul>
<h2>Proveedores</h2>
<p>La web está alojada en GitHub Pages (GitHub, Inc.), que registra datos técnicos de las visitas, como la dirección IP, por motivos de seguridad. Algunos juegos cargan librerías desde redes de distribución de contenido públicas (cdnjs, unpkg, jsDelivr), que también reciben la dirección IP técnica necesaria para servir el archivo. Estos proveedores pueden estar fuera del Espacio Económico Europeo y aplican sus propias garantías.</p>
<h2>Tus derechos</h2>
<p>Puedes pedir acceso, rectificación, supresión, oposición, limitación o portabilidad de tus datos escribiendo a {MAIL}. Si crees que no hemos tratado bien tus datos, puedes reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>
<h2>Menores</h2>
<p>No recogemos datos de menores. Los juegos se pueden jugar sin dar ningún dato.</p>
<p class="note">Última actualización: {UPDATED}.</p></div>""", robots='noindex,follow')

# --- Cookies ---
simple('cookies', 'Política de cookies | Salón Recreativo', 'El Salón Recreativo no usa cookies.', 'Cookies', f"""<div class="legal">
<h1>Política de cookies</h1>
<p class="lead">Esta web no usa cookies, ni propias ni de terceros. Por eso no verás ningún aviso de cookies.</p>
<h2>Almacenamiento local</h2>
<p>Para recordar tus favoritos y tus últimas partidas, la web guarda una pequeña lista en el almacenamiento local de tu navegador (localStorage). Algunos juegos guardan del mismo modo tu progreso, tus récords o el volumen. Es información técnica necesaria para la función que pides, se queda en tu dispositivo y no se usa para seguirte ni para publicidad. Puedes borrarla en cualquier momento desde los ajustes de tu navegador.</p>
<h2>Estadísticas</h2>
<p>{'Usamos GoatCounter, que mide visitas sin cookies y sin identificarte.' if GOATCOUNTER else 'Si medimos visitas, lo hacemos sin cookies y sin identificarte.'}</p>
<h2>Enlaces externos</h2>
<p>Si sales de la web por un enlace (por ejemplo, al compartir un juego en WhatsApp o al abrir el juego de la Kings League), el sitio de destino aplica su propia política de cookies.</p>
<p class="note">Última actualización: {UPDATED}.</p></div>""", robots='noindex,follow')

# ================= PORTADA (ES y CA) =================
src = open(os.path.join(root, 'tools/source.html'), encoding='utf-8').read()
src = src.replace("const EMAIL='';", f"const EMAIL={json.dumps(EMAIL)};")
assert f"const EMAIL={json.dumps(EMAIL)};" in src
i = src.index('</style>') + 8
head_part0 = src[:i]; body0 = src[i:]
head_part0 = re.sub(r'<title>.*?</title>\s*', '', head_part0, flags=re.S)
head_part0 = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\s*', '', head_part0)

def home(lang):
    ca = lang == 'ca'
    url = BASE + ('ca/' if ca else '')
    head_part, body = head_part0, body0
    if ca:
        for a, b in CA_UI:
            assert body.count(a) >= 1, a[:70]
            body = body.replace(a, b)
    HT = 'Minijocs en línia gratis i sense anuncis | Salón Recreativo' if ca else 'Minijuegos online gratis y sin anuncios | Salón Recreativo'
    HD = short('Minijocs en línia gratis i sense anuncis: jocs en català, jocs relaxants, de ritme, karts, motos i futbol. Al navegador, al mòbil i al PC, sense descàrregues.' if ca else
               'Minijuegos online gratis y sin anuncios: juegos relajantes, de ritmo, karts, fútbol y juegos de palabras en catalán. En el navegador, móvil y PC, sin descargas.', 158)
    lp = lambda g: BASE + ('ca/' if ca else '') + 'jugar/' + g['slug'] + '/'
    items = [{"@type": "ListItem", "position": k + 1, "url": lp(g), "name": loc(g, lang)['name']} for k, g in enumerate(play)]
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "Salón Recreativo", "url": url, "inLanguage": lang, "description": HD, "publisher": {"@type": "Organization", "name": "Alica Games Studio", "url": BASE + 'estudio/'}}
    lst = {"@context": "https://schema.org", "@type": "ItemList", "name": 'Minijocs en línia gratis' if ca else 'Minijuegos online gratis', "itemListElement": items}
    alts = None
    pre = ('<base href="../">' if ca else '')
    extra = '<link rel="preload" href="assets/fonts/unbounded-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>'
    if ca:
        CA = {'g': {k: {kk: vv for kk, vv in v.items() if kk in ('name', 'blurb', 'tags', 'note', 'kw')} for k, v in CA_G.items()}, 'cats': CA_CATS, 'catd': CA_CATD}
        extra += '<script>window.__CA=' + json.dumps(CA, ensure_ascii=False, separators=(',', ':')) + '</script>'
    h = head(lang, HT, HD, url, '', BASE + 'img/og-home.jpg', alts, extra=extra)
    h = h.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + pre, 1)
    h += jd(site) + jd(lst)
    # pie: enlaces, texto y directorio
    bycat = {}
    for g in play: bycat.setdefault(g['cat'], []).append(loc(g, lang))
    names = CA_CATS if ca else {k: v['n'] for k, v in CATS.items()}
    cols = ''
    for k in ['cosmico', 'invierno', 'entrenos'] + ORDER:
        if k not in bycat: continue
        cols += f'<div><h2>{e(names[k])}</h2><ul>' + ''.join(f'<li><a href="{"ca/" if ca else ""}jugar/{g["slug"]}/">{e(g["name"])}</a></li>' for g in bycat[k]) + '</ul></div>'
    hubl = ' · '.join(f'<a href="{H["slug"]}/">{e(H["h1"])}</a>' for H in HUBS)
    if ca:
        about = '<p>El Salón Recreativo és una col·lecció de minijocs en línia i gratuïts d\'Alica Games Studio: futbol, jocs de ritme musical, karts, motos, muntanyes russes, jocs relaxants i jocs de paraules en català. Tots es juguen al navegador, al mòbil i a l\'ordinador, sense descàrregues ni registre.</p><p>' + hubl + '</p>'
        fl = '<p class="flinks"><a href="estudio/">Sobre l’estudi</a><a href="aviso-legal/">Avís legal</a><a href="privacidad/">Privacitat</a><a href="cookies/">Cookies</a></p>'
        lng = ''
    else:
        about = '<p>Salón Recreativo es una colección de minijuegos online y gratis de Alica Games Studio: fútbol, juegos de ritmo musical, karts, motos, montañas rusas, juegos relajantes y juegos de palabras en catalán. Todos se juegan en el navegador, en móvil y ordenador, sin descargas ni registro.</p><p>' + hubl + '</p>'
        fl = '<p class="flinks"><a href="estudio/">Sobre el estudio</a><a href="aviso-legal/">Aviso legal</a><a href="privacidad/">Privacidad</a><a href="cookies/">Cookies</a></p>'
        lng = ''
    nav = f'<nav class="dir" aria-label="{"Tots els jocs" if ca else "Todos los juegos"}">{cols}</nav>'
    assert body.count('<!--FLINKS-->') == 1 and body.count('<!--LNG-->') == 1
    body = body.replace('<!--FLINKS-->', fl).replace('</button></div>\n</footer>', '</button>' + about + nav + '</div>\n</footer>').replace('<!--LNG-->', lng)
    assert nav in body
    out = h + '<style>*,*::before,*::after{box-sizing:border-box}body{margin:0}</style>\n' + head_part.replace('<link rel="stylesheet" href="assets/fonts.css">', '') + '</head><body>' + body + '</body></html>'
    W(('ca/' if ca else '') + 'index.html', out)

home('es')

# ================= SITEMAP / ROBOTS / 404 =================
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u, pr, fq in [(BASE, '1.0', 'weekly')] + [(BASE + 'jugar/' + g['slug'] + '/', '0.7', 'monthly') for g in play]:
    sm += f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{fq}</changefreq><priority>{pr}</priority></url>\n'
for u in [BASE + H['slug'] + '/' for H in HUBS] + [BASE + 'estudio/']:
    sm += f'<url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
sm += '</urlset>\n'
W('sitemap.xml', sm)
W('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n' if INDEXABLE else 'User-agent: *\nDisallow: /juegos/\nDisallow: /media/\n')
W('404.html', f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Página no encontrada | Salón Recreativo</title><meta name="robots" content="noindex"><style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#07060f;color:#f5f2ff;font:18px system-ui;text-align:center}}a{{color:#ffd23f}}</style></head><body><div><h1>Esta página no existe</h1><p><a href="{BASE}">Volver al Salón Recreativo</a></p></div></body></html>')

# ================= APP INSTALABLE =================
manifest = {"name": "Salón Recreativo · Alica Games Studio", "short_name": "Salón", "description": "Minijuegos gratis para el navegador, sin anuncios ni descargas.",
            "lang": "es", "start_url": "./?app=1", "scope": "./", "display": "standalone", "orientation": "any", "background_color": "#07060f", "theme_color": "#07060f",
            "icons": [{"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                      {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
            "shortcuts": [{"name": "Juegos relajantes", "url": "./#sec-relax"}, {"name": "CatQuiz", "url": "./#sec-catquiz"}, {"name": "Saga cósmica", "url": "./#trilogia"}]}
W('manifest.webmanifest', json.dumps(manifest, ensure_ascii=False, indent=1))
W('sw.js', """/* Salón Recreativo: service worker. Portada y recursos básicos disponibles sin conexión; los juegos se guardan al jugarlos. */
const V='sr-""" + TODAY + """',CORE=['./','assets/fonts.css','assets/lenis.min.js','manifest.webmanifest','icons/icon-192.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>Promise.all(CORE.map(u=>c.add(u).catch(()=>{})))).then(()=>self.skipWaiting()));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
self.addEventListener('fetch',e=>{
  const r=e.request,u=new URL(r.url);
  if(r.method!=='GET'||u.origin!==location.origin||r.headers.has('range')||/\\/media\\//.test(u.pathname))return;
  const put=res=>{if(res&&res.status===200&&res.type==='basic'){const c=res.clone();caches.open(V).then(x=>x.put(r,c));}return res;};
  if(r.mode==='navigate'||/\\/(juegos)\\//.test(u.pathname)){
    e.respondWith(fetch(r).then(put).catch(()=>caches.match(r).then(m=>m||caches.match('./'))));return;}
  e.respondWith(caches.match(r).then(m=>{const f=fetch(r).then(put).catch(()=>m);return m||f;}));
});
""")
print('ok', len(play), 'juegos')
