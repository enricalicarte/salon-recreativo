#!/usr/bin/env python3
"""Reel cinematográfico Salón Recreativo · 1080x1920 @24fps, 120 BPM (12 frames/beat)."""
import json, math, os, random, sys
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np

R = os.path.dirname(os.path.abspath(__file__))
FR = f'{R}/fr'; OUT = f'{R}/out'; os.makedirs(OUT, exist_ok=True)
W, H, FPS, BEAT = 1080, 1920, 24, 12
G = {g['slug']: g for g in json.load(open('/home/claude/salon-recreativo/tools/games.json'))['GAMES']}
NAME = lambda s: G[s]['name'] if s in G else s
F = lambda n, sz: ImageFont.truetype(f'{R}/fonts/{n}.ttf', sz)
BG = (7, 6, 15)
YEL, PINK, CYAN, VIO, LIME, ORA = (255, 210, 63), (255, 79, 163), (56, 229, 255), (168, 120, 255), (120, 255, 150), (255, 140, 60)

# ---------- timeline (duración en beats) ----------
CH = [  # (título, subtítulo, color, [(slug, beats)...])
    ('SAGA CÓSMICA', 'Naves, jefes y música', VIO, [('ruta-cosmica', 3), ('tiradora-cosmica', 3), ('constructor-cosmico', 3), ('cosmic-guitar', 3)]),
    ('ALTA TEMPORADA', 'Nieve, saltos y piruetas', CYAN, [('el-gran-salto', 3), ('la-gran-pirueta', 3), ('el-gran-descenso', 3)]),
    ('ENTRENAMIENTOS', 'Muévete delante de la cámara', LIME, [('fifa-11-kids', 3), ('boxeo-kids', 3)]),
    ('JUEGA CON TU CÁMARA', 'Tu cuerpo es el mando', PINK, [('lluvia-loca', 4), ('muro-loco', 4), ('portero-loco', 4), ('balon-loco', 4)]),
    ('PUZLES', 'Piensa rápido', YEL, [('crucigiro', 2), ('bloques-neon', 2), ('tower-stack', 2)]),
    ('MOTOR Y ACCIÓN', 'A toda velocidad', ORA, [('moto-fury', 2), ('turbo-kart-rally', 2), ('looping-loco', 2), ('halfpipe', 2), ('alas-de-acero', 2), ('monster-smash', 2)]),
    ('RELAX', 'Respira y mira', CYAN, [('relax-estanque-de-koi', 3), ('relax-aurora-boreal', 3)]),
    ('CATQUIZ', 'Juegos en català', YEL, [('catquiz-motle', 2), ('catquiz-penjat-3d', 2), ('l-ultim-estiu', 2)]),
]
GRID = ['paradon-cosmico', 'la-gran-pirueta', 'yoga-kids', 'muro-loco', 'drop-in', 'ola-perfecta', 'ciudadela-de-arena', 'stu-el-especialista',
        'relax-farolillos-del-lago', 'catquiz-quiz-de-futbol', 'hotel-miramar', 'porrazo-party', 'aventura-porc', 'bloques-neon', 'portero-loco', 'moto-fury']
INTRO, TITLE, GRIDB, OUTRO = 7, 1.5, 6, 8

def build():
    seq = []; t = 0
    def add(kind, beats, **kw):
        nonlocal t; n = int(round(beats * BEAT)); seq.append(dict(kind=kind, start=t, n=n, **kw)); t += n
    add('intro', INTRO)
    for i, (ti, su, col, clips) in enumerate(CH):
        add('title', TITLE, title=ti, sub=su, col=col, idx=i + 1)
        for slug, b in clips: add('clip', b, slug=slug, col=col, chap=ti)
    add('grid', GRIDB)
    add('outro', OUTRO)
    return seq, t
SEQ, TOTAL = build()

# ---------- helpers ----------
_cache = {}
def frame_of(slug, i):
    k = (slug, i)
    if k not in _cache:
        n = len(os.listdir(f'{FR}/{slug}'))
        _cache[k] = Image.open(f'{FR}/{slug}/{min(i, n - 1) + 1:03d}.jpg').convert('RGB')
    return _cache[k]

def ease(x, k=3):  # ease-out
    x = max(0, min(1, x)); return 1 - (1 - x) ** k

def glow_text(img, xy, text, font, fill, glow, rad=18, anchor='mm', strength=2):
    layer = Image.new('RGB', img.size, (0, 0, 0)); d = ImageDraw.Draw(layer)
    d.text(xy, text, font=font, fill=glow, anchor=anchor)
    layer = layer.filter(ImageFilter.GaussianBlur(rad))
    for _ in range(strength): img = ImageChops.add(img, layer)
    ImageDraw.Draw(img).text(xy, text, font=font, fill=fill, anchor=anchor)
    return img

def radial(col, cx, cy, r, alpha=1.0):
    y, x = np.mgrid[0:H, 0:W]
    d = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / r
    a = np.clip(1 - d, 0, 1) ** 2 * alpha
    arr = np.zeros((H, W, 3), np.float32)
    for c in range(3): arr[..., c] = col[c] * a
    return arr

def base_bg(cols, t, seed=0):
    """fondo oscuro con 2 nebulosas de color que respiran"""
    arr = np.zeros((H, W, 3), np.float32); arr[...] = BG
    for i, c in enumerate(cols):
        cx = W * (0.25 + 0.5 * ((i + seed) % 2)) + 120 * math.sin(t * 0.7 + i * 2)
        cy = H * (0.3 + 0.4 * (i % 2)) + 150 * math.cos(t * 0.5 + i)
        arr += radial(c, cx, cy, 900, 0.35)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

def logo(size):
    s = size; im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    y, x = np.mgrid[0:s, 0:s]; u = (x + y) / (2 * s)
    g = np.zeros((s, s, 4), np.float32)
    c0, c1, c2 = np.array(YEL), np.array(PINK), np.array(CYAN)
    for c in range(3):
        g[..., c] = np.where(u < .5, c0[c] + (c1[c] - c0[c]) * u * 2, c1[c] + (c2[c] - c1[c]) * (u - .5) * 2)
    r = np.sqrt((x - s / 2) ** 2 + (y - s / 2) ** 2)
    g[..., 3] = np.clip((s * .5 - r) * 2, 0, 255)
    im = Image.fromarray(g.astype(np.uint8), 'RGBA')
    d = ImageDraw.Draw(im); k = s / 64
    d.polygon([(25 * k, 20 * k), (25 * k, 44 * k), (44 * k, 32 * k)], fill=BG + (255,))
    return im

def rounded_mask(w, h, r):
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255); return m

def particles(img, t, col, n=40, seed=1):
    rnd = random.Random(seed); d = ImageDraw.Draw(img)
    for i in range(n):
        x0, y0, sp, sz = rnd.random() * W, rnd.random() * H, .3 + rnd.random(), 2 + rnd.random() * 5
        y = (y0 - t * 60 * sp) % H; x = x0 + 30 * math.sin(t * sp + i)
        a = .4 + .6 * abs(math.sin(t * 2 + i))
        c = tuple(int(v * a) for v in col)
        d.ellipse((x - sz, y - sz, x + sz, y + sz), fill=c)
    return img

def wordmark(img, alpha=1.0):
    lg = logo(64); ov = Image.new('RGB', img.size, (0, 0, 0))
    ov.paste(lg, (64, 96), lg)
    ImageDraw.Draw(ov).text((148, 128), 'SALÓN RECREATIVO', font=F('lilita', 40), fill=(255, 255, 255), anchor='lm')
    return ImageChops.add(img, ov.point(lambda v: int(v * alpha)))

# ---------- scenes ----------
def sc_intro(k, n):
    t = k / FPS; p = k / n
    img = base_bg([VIO, PINK], t); img = particles(img, t, CYAN, 60)
    # logo
    s = int(300 * ease(p * 3.5));
    if s > 2:
        lg = logo(s); glow = lg.filter(ImageFilter.GaussianBlur(30))
        img.paste(glow, (W // 2 - s // 2, 560 - s // 2), glow); img.paste(lg, (W // 2 - s // 2, 560 - s // 2), lg)
    if k > BEAT * 1.5:
        q = ease((k - BEAT * 1.5) / (BEAT * 1.5)); sz = int(150 + 30 * (1 - q))
        img = glow_text(img, (W // 2, 900), 'SALÓN', F('lilita', sz), (255, 255, 255), YEL, 24)
        img = glow_text(img, (W // 2, 1070), 'RECREATIVO', F('lilita', int(sz * .78)), (255, 255, 255), PINK, 24)
    if k > BEAT * 3:
        q = ease((k - BEAT * 3) / BEAT)
        d = ImageDraw.Draw(img)
        d.text((W // 2, 1220), 'ALICA GAMES STUDIO', font=F('nunito800', 44), fill=tuple(int(v * q) for v in CYAN), anchor='mm')
    if k > BEAT * 4.5:
        q = ease((k - BEAT * 4.5) / BEAT)
        d = ImageDraw.Draw(img)
        d.text((W // 2, 1420), 'Juegos gratis para jugar', font=F('nunito700', 54), fill=tuple(int(230 * q) for _ in range(3)), anchor='mm')
        d.text((W // 2, 1490), 'en el navegador · móvil y PC', font=F('nunito700', 54), fill=tuple(int(230 * q) for _ in range(3)), anchor='mm')
    # fade in
    if k < 8: img = img.point(lambda v: int(v * k / 8))
    return img

def sc_title(k, n, title, sub, col, idx):
    t = k / FPS
    img = base_bg([col, VIO], t, idx); img = particles(img, t + idx * 7, col, 30, idx)
    q = ease(k / (BEAT * .8), 4); sz = int(120 + 50 * (1 - q))
    d = ImageDraw.Draw(img)
    d.text((W // 2, 760), f'CAPÍTULO {idx:02d}', font=F('nunito800', 40), fill=col, anchor='mm')
    fnt = F('lilita', sz)
    # dos líneas si es largo
    if d.textlength(title, font=fnt) < W - 120 or ' ' not in title:
        while d.textlength(title, font=fnt) > W - 120: sz -= 4; fnt = F('lilita', sz)
        lines = [title]
    else: lines = title.rsplit(' ', 1)
    y = 920 - (len(lines) - 1) * 70
    for ln in lines:
        img = glow_text(img, (W // 2, y), ln, fnt, (255, 255, 255), col, 26); y += int(sz * 1.05)
    d = ImageDraw.Draw(img)
    d.text((W // 2, y + 40), sub, font=F('nunito700', 52), fill=(235, 235, 245), anchor='mm')
    # barra decorativa
    bw = int(ease(k / BEAT) * 300); d.rounded_rectangle((W // 2 - bw // 2, 700, W // 2 + bw // 2, 708), 4, fill=col)
    # flash inicial
    if k < 4: img = ImageChops.add(img, Image.new('RGB', img.size, tuple(int(v * (1 - k / 4) * .8) for v in col)))
    return wordmark(img, .6)

def sc_clip(k, n, slug, col, chap):
    fr = frame_of(slug, k); p = k / n
    # fondo: clip desenfocado y oscurecido
    bg = fr.resize((W // 8, int(W // 8 * fr.height / fr.width))).resize((W, int(W * fr.height / fr.width)))
    bg = bg.filter(ImageFilter.GaussianBlur(14)).resize((W, int(W * fr.height / fr.width)))
    full = Image.new('RGB', (W, H), BG)
    # llena verticalmente ampliando
    bh = H; bw = int(bh * fr.width / fr.height); bgf = fr.resize((bw // 10, bh // 10)).filter(ImageFilter.GaussianBlur(6)).resize((bw, bh))
    full.paste(bgf, ((W - bw) // 2, 0)); full = full.point(lambda v: int(v * .42))
    # tinte de capítulo
    full = ImageChops.add(full, Image.fromarray(np.clip(radial(col, W // 2, H, 1100, .25), 0, 255).astype(np.uint8)))
    # clip principal con punch-in
    sc = 1.0 + 0.06 * (1 - ease(k / 6)) + 0.03 * p
    cw = int(1030 * sc); ch = int(cw * fr.height / fr.width)
    card = fr.resize((cw, ch), Image.LANCZOS)
    # glow del borde
    r = 40; x, y = (W - cw) // 2, 790 - ch // 2
    gl = Image.new('RGB', (W, H), (0, 0, 0)); ImageDraw.Draw(gl).rounded_rectangle((x - 6, y - 6, x + cw + 6, y + ch + 6), r + 6, fill=col)
    gl = gl.filter(ImageFilter.GaussianBlur(28)); full = ImageChops.add(full, gl.point(lambda v: int(v * .7)))
    full.paste(card, (x, y), rounded_mask(cw, ch, r))
    ImageDraw.Draw(full).rounded_rectangle((x, y, x + cw - 1, y + ch - 1), r, outline=tuple(int(v * .9) for v in col), width=4)
    # textos (capa RGBA con alpha = q para que no aparezcan en negro)
    q = ease((k - 2) / 8)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    pill = chap; pf = F('nunito800', 34); pw = d.textlength(pill, font=pf) + 50
    py = y + ch + 90
    d.rounded_rectangle((W // 2 - pw / 2, py - 30, W // 2 + pw / 2, py + 30), 30, fill=col + (255,))
    d.text((W // 2, py), pill, font=pf, fill=BG + (255,), anchor='mm')
    nm = NAME(slug); nf = F('lilita', 92 if len(nm) < 16 else 72)
    ty = py + 60 + int(30 * (1 - q))
    # sombra + glow del nombre
    gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((W // 2, ty + 70), nm, font=nf, fill=col + (255,), anchor='mm')
    gl = gl.filter(ImageFilter.GaussianBlur(18)); lay = Image.alpha_composite(lay, gl); lay = Image.alpha_composite(lay, gl)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W // 2 + 4, ty + 76), nm, font=nf, fill=(0, 0, 0, 160), anchor='mm')
    lay = Image.alpha_composite(lay, sh.filter(ImageFilter.GaussianBlur(4)))
    ImageDraw.Draw(lay).text((W // 2, ty + 70), nm, font=nf, fill=(255, 255, 255, 255), anchor='mm')
    if q < 1: lay.putalpha(lay.getchannel('A').point(lambda v: int(v * q)))
    full = Image.alpha_composite(full.convert('RGBA'), lay).convert('RGB')
    full = wordmark(full, .8)
    # fundido corto al salir del clip (3 frames)
    if n - k <= 3: full = full.point(lambda v: int(v * (n - k) / 4 + .25 * v / 255 * 0))
    return full

def sc_grid(k, n):
    t = k / FPS; p = k / n
    img = base_bg([PINK, CYAN], t, 3)
    cols, rows = 4, 4; tw, th = 250, 156; gap = 16
    gw = cols * tw + (cols - 1) * gap; gh = rows * th + (rows - 1) * gap
    sc = 1.35 - 0.35 * ease(p * 1.6);
    layer = Image.new('RGB', (gw, gh), BG)
    for i, s in enumerate(GRID):
        fr = frame_of(s, k).resize((tw, th)); c, r = i % cols, i // cols
        layer.paste(fr, (c * (tw + gap), r * (th + gap)), rounded_mask(tw, th, 18))
    lw, lh = int(gw * sc), int(gh * sc); layer = layer.resize((lw, lh), Image.BILINEAR)
    img.paste(layer, ((W - lw) // 2, 820 - lh // 2))
    q = ease((k - BEAT) / BEAT)
    img = glow_text(img, (W // 2, 1560), 'Y MUCHOS MÁS', F('lilita', int(110 * (0.8 + 0.2 * q))), tuple(int(255 * q) for _ in range(3)), tuple(int(v * q) for v in YEL), 24)
    d = ImageDraw.Draw(img)
    d.text((W // 2, 1660), 'Nuevos juegos muy pronto', font=F('nunito700', 48), fill=tuple(int(230 * q) for _ in range(3)), anchor='mm')
    return wordmark(img, .8)

def sc_outro(k, n):
    t = k / FPS; p = k / n
    img = base_bg([YEL, PINK], t + 9, 1); img = particles(img, t + 20, YEL, 60, 5)
    s = 260; lg = logo(s); glow = lg.filter(ImageFilter.GaussianBlur(30))
    q0 = ease(k / BEAT); s2 = int(s * q0)
    if s2 > 2:
        l2 = lg.resize((s2, s2)); g2 = glow.resize((s2, s2))
        img.paste(g2, (W // 2 - s2 // 2, 520 - s2 // 2), g2); img.paste(l2, (W // 2 - s2 // 2, 520 - s2 // 2), l2)
    img = glow_text(img, (W // 2, 800), 'SALÓN', F('lilita', 150), (255, 255, 255), YEL, 24)
    img = glow_text(img, (W // 2, 960), 'RECREATIVO', F('lilita', 117), (255, 255, 255), PINK, 24)
    d = ImageDraw.Draw(img)
    if k > BEAT * 1.5:
        q = ease((k - BEAT * 1.5) / BEAT)
        d.text((W // 2, 1120), 'Juega gratis · sin descargas', font=F('nunito700', 52), fill=tuple(int(235 * q) for _ in range(3)), anchor='mm')
    if k > BEAT * 2.5:
        q = ease((k - BEAT * 2.5) / BEAT)
        pf = F('nunito800', 40); url = 'enricalicarte.github.io/salon-recreativo'; pw = d.textlength(url, font=pf) + 70
        d.rounded_rectangle((W // 2 - pw / 2, 1240, W // 2 + pw / 2, 1330), 45, fill=tuple(int(v * q) for v in CYAN))
        d.text((W // 2, 1285), url, font=pf, fill=tuple(int(v * q) for v in BG), anchor='mm')
    if k > BEAT * 3.5:
        q = ease((k - BEAT * 3.5) / BEAT)
        d.text((W // 2, 1480), 'ALICA GAMES STUDIO', font=F('nunito800', 44), fill=tuple(int(v * q) for v in YEL), anchor='mm')
    if n - k < 18: img = img.point(lambda v: int(v * (n - k) / 18))
    return img

def render(i):
    out = f'{OUT}/{i:05d}.jpg'
    if os.path.exists(out): return
    for s in SEQ:
        if s['start'] <= i < s['start'] + s['n']:
            k = i - s['start']; kind = s['kind']
            if kind == 'intro': img = sc_intro(k, s['n'])
            elif kind == 'title': img = sc_title(k, s['n'], s['title'], s['sub'], s['col'], s['idx'])
            elif kind == 'clip': img = sc_clip(k, s['n'], s['slug'], s['col'], s['chap'])
            elif kind == 'grid': img = sc_grid(k, s['n'])
            else: img = sc_outro(k, s['n'])
            img.save(out, quality=92); return

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'info':
        print(TOTAL, TOTAL / FPS); [print(s['start'], s['kind'], s.get('slug', s.get('title', ''))) for s in SEQ]; sys.exit()
    frames = [int(a) for a in sys.argv[1:]] if len(sys.argv) > 1 else range(TOTAL)
    with Pool(2) as p: p.map(render, frames, chunksize=8)
    print('done', TOTAL)
