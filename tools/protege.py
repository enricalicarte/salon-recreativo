"""Protección ligera del Salón Recreativo (sin tocar el repositorio ni el alojamiento).

- Bloqueo de dominio: cada página y cada juego solo arranca en los dominios permitidos y solo se deja
  meter en iframes de esos dominios. Si alguien copia un juego a otra web (o lo abre guardado en su
  ordenador), sale un aviso con el enlace al Salón Recreativo en lugar del juego.
- Aviso de autoría (© · todos los derechos reservados) al principio de cada HTML y de cada módulo JS.

Se ejecuta solo al final de build_seo.py (o a mano: python3 tools/protege.py). Es idempotente.
Para el dominio propio: añadirlo en EXTRA (o cambiar BASE en build_seo.py) y regenerar.
"""
import base64, os, re, sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Dominios donde se puede jugar (además del de BASE). Subdominios incluidos.
EXTRA = ['localhost', '127.0.0.1']
# Dominios que pueden mostrar los juegos dentro de un iframe (vista previa privada en claude.ai).
EMBED = ['claude.ai', 'claudeusercontent.com']
AUTOR = 'Enric Alicarte · Alica Games Studio'
SKIP = {'tools', 'media', '.git', 'node_modules', 'icons', 'img'}

COPY_HTML = ('<!-- © 2026 ' + AUTOR + ' · Salón Recreativo. Todos los derechos reservados. '
             'Prohibida la copia, redistribución o publicación de este juego o de su código en otros sitios sin permiso escrito. -->')
COPY_JS = ('/* © 2026 ' + AUTOR + ' · Salón Recreativo. Todos los derechos reservados. '
           'Prohibida la copia, redistribución o publicación de este código en otros sitios sin permiso escrito. */')


def hosts(base):
    h = urlparse(base).hostname or ''
    return [x for x in [h] + EXTRA if x]


def guard(base):
    play = base64.b64encode(','.join(hosts(base)).encode()).decode()
    emb = base64.b64encode(','.join(EMBED).encode()).decode()
    home = base64.b64encode(base.encode()).decode()
    return ('<script data-sr="g">(function(){var d=function(s){return atob(s).split(",")},P=d("' + play + '"),E=P.concat(d("' + emb + '")),'
            'ok=function(x,L){x=String(x||"").toLowerCase().replace(/^www\\./,"");for(var i=0;i<L.length;i++){var a=L[i];if(x===a||x.slice(-a.length-1)==="."+a)return 1}return 0},'
            'hn=function(u){try{return new URL(u).hostname}catch(e){return ""}},bad=!ok(location.hostname,P);'
            'if(!bad&&window.top!==window.self){var an=location.ancestorOrigins;if(an&&an.length){for(var j=0;j<an.length;j++)if(!ok(hn(an[j]),E))bad=1}'
            'else{try{if(!ok(top.location.hostname,E))bad=1}catch(e){var r=document.referrer;if(!r||!ok(hn(r),E))bad=1}}}'
            'if(!bad)return;try{window.stop()}catch(e){}var H=atob("' + home + '");'
            'document.documentElement.innerHTML=(\'<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Salón Recreativo</title></head>'
            '<body style="margin:0;min-height:100vh;display:grid;place-items:center;background:#07060f;color:#f5f2ff;font:18px system-ui,sans-serif;text-align:center;padding:24px">'
            '<div><h1 style="font-size:26px">Este juego es del Salón Recreativo</h1><p style="opacity:.8">Solo se puede jugar en su web oficial.</p>'
            '<p><a target="_top" style="display:inline-block;background:#ffd23f;color:#1a1300;font-weight:800;padding:12px 22px;border-radius:999px;text-decoration:none" href="\'+H+\'">Jugar en el Salón Recreativo</a></p>'
            '<p style="font-size:13px;opacity:.55">© 2026 ' + AUTOR + '</p></div></body>\');throw 0})();</script>')


G_RE = re.compile(r'<script data-sr="g">.*?</script>', re.S)
C_RE = re.compile(r'<!-- © 2026 [^>]*?Todos los derechos reservados\.[^>]*?-->\n?', re.S)
CJ_RE = re.compile(r'/\* © 2026 [^*]*?Todos los derechos reservados\.[^*]*?\*/\n?', re.S)
HEAD_RE = re.compile(r'<head[^>]*>', re.I)
CHARSET_RE = re.compile(r'<meta\s+charset=[^>]*>', re.I)


def protege_html(s, g):
    s = G_RE.sub('', s)
    s = C_RE.sub('', s)
    # el aviso de autoría va justo después del doctype; el bloqueo, lo primero dentro de <head> (tras el charset)
    m = re.match(r'\s*<!doctype[^>]*>\n?', s, re.I)
    s = (s[:m.end()] + COPY_HTML + '\n' + s[m.end():]) if m else (COPY_HTML + '\n' + s)
    m = CHARSET_RE.search(s)
    if m and (not HEAD_RE.search(s) or m.start() < s.lower().find('</head>')):
        return s[:m.end()] + g + s[m.end():]
    m = HEAD_RE.search(s)
    if m:
        return s[:m.end()] + g + s[m.end():]
    m = re.search(r'<html[^>]*>', s, re.I)
    return (s[:m.end()] + g + s[m.end():]) if m else (g + s)


def run(base):
    g = guard(base)
    n_html = n_js = 0
    for dp, dns, fns in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        top = rel.split(os.sep)[0]
        if top in SKIP:
            dns[:] = []
            continue
        dns[:] = [d for d in dns if d not in SKIP]
        for fn in fns:
            p = os.path.join(dp, fn)
            if fn.endswith('.html'):
                s = open(p, encoding='utf-8').read()
                t = protege_html(s, g)
                if t != s:
                    open(p, 'w', encoding='utf-8').write(t)
                n_html += 1
            elif fn.endswith('.js') and top == 'juegos' and not fn.endswith('.min.js') and os.path.getsize(p) < 3_000_000:
                s = open(p, encoding='utf-8').read()
                t = COPY_JS + '\n' + CJ_RE.sub('', s)
                if t != s:
                    open(p, 'w', encoding='utf-8').write(t)
                n_js += 1
    print('protección:', n_html, 'páginas ·', n_js, 'módulos JS · dominios', ', '.join(hosts(base)))


if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    src = open(os.path.join(ROOT, 'tools', 'build_seo.py'), encoding='utf-8').read()
    run(re.search(r"^BASE = '([^']+)'", src, re.M).group(1))
