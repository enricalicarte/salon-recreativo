#!/usr/bin/env python3
"""Monta los juegos con cámara (un solo HTML cada uno) a partir de las plantillas de esta carpeta:
base.js y common.css se insertan en <slug>.html  →  juegos/<slug>/index.html"""
import os, re
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(D))
base = open(os.path.join(D, 'base.js'), encoding='utf-8').read()
css = open(os.path.join(D, 'common.css'), encoding='utf-8').read()
for slug in ('lluvia-loca', 'muro-loco', 'portero-loco', 'balon-loco'):
    p = os.path.join(D, slug + '.html')
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read().replace('/*CSS*/', css).replace('/*BASE*/', base)
    s = re.sub(r'/\*INC:([\w.-]+)\*/', lambda m: open(os.path.join(D, m.group(1)), encoding='utf-8').read(), s)
    os.makedirs(os.path.join(R, 'juegos', slug), exist_ok=True)
    open(os.path.join(R, 'juegos', slug, 'index.html'), 'w', encoding='utf-8').write(s)
    print(slug, 'ok', len(s))
