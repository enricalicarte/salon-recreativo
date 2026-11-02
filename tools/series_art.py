"""Genera las ilustraciones de LLOGUER para Alica Play (play/img/). Uso: python3 tools/series_art.py

- lloguer.jpg (1600x900) y lloguer-v.jpg (vertical): cartel completo.
- lloguer-bg.jpg, lloguer-mid.png, lloguer-fg.png: las tres capas del collage, para el movimiento en paralaje.
- lloguer-1/2/3.jpg: miniaturas de episodios y extras, con encuadres distintos.
"""
import os
from playwright.sync_api import sync_playwright
here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(os.path.dirname(here), 'play', 'img')
os.makedirs(out, exist_ok=True)
J = [  # (archivo, ancho, alto, parámetros, png transparente)
    ('lloguer.jpg', 1600, 900, '', False),
    ('lloguer-v.jpg', 675, 900, '&vert=1', False),
    ('lloguer-bg.jpg', 1600, 900, '&layer=bg', False),
    ('lloguer-mid.png', 1600, 900, '&layer=mid', True),
    ('lloguer-fg.png', 1600, 900, '&layer=fg', True),
    ('lloguer-1.jpg', 640, 360, '&vb=880,150,720,405', False),
    ('lloguer-2.jpg', 640, 360, '&vb=1180,90,520,292', False),
    ('lloguer-3.jpg', 640, 360, '&vb=60,140,800,450', False),
]
with sync_playwright() as p:
    b = p.chromium.launch()
    for f, w, h, q, png in J:
        pg = b.new_page(viewport={'width': w, 'height': h})
        pg.goto(f'file://{here}/series_art.html?m=lloguer' + q)
        pg.wait_for_timeout(250)
        pg.screenshot(path=os.path.join(out, f), type='png' if png else 'jpeg', omit_background=png, **({} if png else {'quality': 84}))
        pg.close()
    b.close()
print('ok', len(J))
