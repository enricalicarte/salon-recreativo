#!/usr/bin/env python3
"""Ilustraciones cuadradas (512×512) de cada juego para la vista Mosaico.
Estilo pegatina: fondo con degradado y rayos, objeto protagonista con contorno grueso y brillos.
Uso: python3 tools/icons.py   → icons/games/<slug>.svg"""
import os, json, math
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(root, 'icons', 'games'); os.makedirs(OUT, exist_ok=True)
INK = '#1d1442'
SW = 9
FONT = "font-family=\"'Arial Black','Arial Rounded MT Bold',Arial,Helvetica,sans-serif\" font-weight=\"900\""

class Icon:
    def __init__(s): s.defs = []; s.body = []; s.n = 0
    def gid(s): s.n += 1; return 'g%d' % s.n
    def lg(s, c1, c2, x1=0, y1=0, x2=0, y2=1):
        i = s.gid(); s.defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>'); return f'url(#{i})'
    def rg(s, c1, c2, cx=.5, cy=.45, r=.7):
        i = s.gid(); s.defs.append(f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient>'); return f'url(#{i})'
    def add(s, x): s.body.append(x); return s
    def svg(s):
        base = ('<filter id="ds" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="7" stdDeviation="5" flood-color="#140c33" flood-opacity=".38"/></filter>'
                '<filter id="bk" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>'
                '<radialGradient id="vig" cx=".5" cy=".46" r=".75"><stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#0a0620" stop-opacity=".42"/></radialGradient>'
                '<linearGradient id="gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/></linearGradient>')
        over = '<rect width="512" height="512" fill="url(#vig)"/><rect width="512" height="512" fill="url(#gl)"/>'
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512"><defs>' + base + ''.join(s.defs) + '</defs>' + ''.join(s.body) + over + '</svg>')

def st(fill, w=SW, extra=''):
    sh = ' filter="url(#ds)"' if w >= 7 else ''
    return f'fill="{fill}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{sh} {extra}'

def bg(I, c1, c2, rays=None, ra=.12):
    I.add(f'<rect width="512" height="512" fill="{I.rg(c1, c2, .5, .42, .75)}"/>')
    if rays:
        p = ''
        for k in range(16):
            a0 = k * math.pi / 8; a1 = a0 + math.pi / 16
            p += f'M256 230L{256+700*math.cos(a0):.0f} {230+700*math.sin(a0):.0f}L{256+700*math.cos(a1):.0f} {230+700*math.sin(a1):.0f}Z'
        I.add(f'<path d="{p}" fill="{rays}" opacity="{ra}"/>')
    import random; rnd = random.Random(len(c1) * 31 + ord(c1[1]))
    for _ in range(6):
        I.add(f'<circle cx="{rnd.uniform(0,512):.0f}" cy="{rnd.uniform(0,512):.0f}" r="{rnd.uniform(18,46):.0f}" fill="#fff" opacity="{rnd.uniform(.08,.18):.2f}" filter="url(#bk)"/>')

def sparkle(I, x, y, r, c='#fff', o=1):
    I.add(f'<path d="M{x} {y-r}Q{x+r*.18} {y-r*.18} {x+r} {y}Q{x+r*.18} {y+r*.18} {x} {y+r}Q{x-r*.18} {y+r*.18} {x-r} {y}Q{x-r*.18} {y-r*.18} {x} {y-r}Z" fill="{c}" opacity="{o}"/>')

def star5(x, y, R, r=None, rot=-90):
    r = r or R * .48; pts = []
    for i in range(10):
        a = math.radians(rot + i * 36); d = R if i % 2 == 0 else r
        pts.append(f'{x+d*math.cos(a):.1f},{y+d*math.sin(a):.1f}')
    return 'M' + 'L'.join(pts) + 'Z'

def shine(I, x, y, rx, ry, rot=-25, o=.45):
    I.add(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#fff" opacity="{o}" transform="rotate({rot} {x} {y})"/>')

def wheel(I, x, y, r, rim='#d9dcef', tire='#2b2440'):
    I.add(f'<circle cx="{x}" cy="{y}" r="{r}" {st(tire)}/>')
    I.add(f'<circle cx="{x}" cy="{y}" r="{r*.52}" {st(rim, 6)}/>')
    I.add(f'<circle cx="{x}" cy="{y}" r="{r*.16}" fill="{INK}"/>')

def note(I, x, y, s=1, c='#ffd23f'):
    I.add(f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0V-70L42 -82V-14" fill="none" stroke="{INK}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<ellipse cx="-12" cy="2" rx="20" ry="15" {st(c, 8)} transform="rotate(-20 -12 2)"/><ellipse cx="30" cy="-10" rx="20" ry="15" {st(c, 8)} transform="rotate(-20 30 -10)"/></g>')

def tile(I, x, y, w, ch, fill='#fff', tc=INK, fs=None, r=18):
    fs = fs or w * .62
    I.add(f'<rect x="{x}" y="{y}" width="{w}" height="{w}" rx="{r}" {st(fill)}/>')
    I.add(f'<rect x="{x+8}" y="{y+8}" width="{w-16}" height="{w*.28}" rx="{r*.6}" fill="#fff" opacity=".35"/>')
    if ch: I.add(f'<text x="{x+w/2}" y="{y+w/2+fs*.36}" text-anchor="middle" font-size="{fs}" {FONT} fill="{tc}">{ch}</text>')

def planet(I, x, y, r, c1, c2, ring=None):
    I.add(f'<circle cx="{x}" cy="{y}" r="{r}" {st(I.rg(c1, c2, .35, .3, .9))}/>')
    if ring: I.add(f'<ellipse cx="{x}" cy="{y}" rx="{r*1.7}" ry="{r*.45}" fill="none" stroke="{ring}" stroke-width="{max(6,r*.18):.0f}" transform="rotate(-18 {x} {y})" opacity=".95"/>')
    shine(I, x - r * .35, y - r * .4, r * .32, r * .18, -30, .5)

def eyes(I, x, y, s=1, d=24, look=0):
    for k in (-1, 1):
        I.add(f'<ellipse cx="{x+k*d*s}" cy="{y}" rx="{11*s}" ry="{14*s}" fill="#fff" stroke="{INK}" stroke-width="{4*s}"/><circle cx="{x+k*d*s+look*4*s}" cy="{y+2*s}" r="{6.5*s}" fill="{INK}"/><circle cx="{x+k*d*s+look*4*s+2.5*s}" cy="{y-1*s}" r="{2.4*s}" fill="#fff"/>')

def smile(I, x, y, s=1, open_=False):
    if open_: I.add(f'<path d="M{x-16*s} {y} Q{x} {y+26*s} {x+16*s} {y}Z" fill="#7a1530" stroke="{INK}" stroke-width="{4*s}" stroke-linejoin="round"/><path d="M{x-8*s} {y+11*s} Q{x} {y+18*s} {x+8*s} {y+11*s}" fill="#ff7a9a"/>')
    else: I.add(f'<path d="M{x-14*s} {y} Q{x} {y+14*s} {x+14*s} {y}" fill="none" stroke="{INK}" stroke-width="{5*s}" stroke-linecap="round"/>')

def blush(I, x, y, s=1, d=36):
    for k in (-1, 1): I.add(f'<ellipse cx="{x+k*d*s}" cy="{y}" rx="{10*s}" ry="{6*s}" fill="#ff6b8a" opacity=".45"/>')

def cat(I, x, y, s=1, c='#ffb23e'):
    # mascota de CatQuiz: gato que se asoma
    I.add(f'<g transform="translate({x} {y}) scale({s})">'
          f'<path d="M-62 -20 L-58 -92 L-12 -58Z M62 -20 L58 -92 L12 -58Z" {st(c, 8)}/><path d="M-52 -40 L-50 -76 L-26 -58Z M52 -40 L50 -76 L26 -58Z" fill="#ff9ab8"/>'
          f'<ellipse cx="0" cy="0" rx="78" ry="64" {st(I.rg("#ffe2b0", c, .4, .3, .9))}/>'
          f'<path d="M-30 -60 q8 14 0 26 M0 -64 q8 14 0 26 M30 -60 q8 14 0 26" stroke="#d9781a" stroke-width="7" fill="none" stroke-linecap="round"/></g>')
    eyes(I, x, y - 2 * s, s * .95, 26)
    I.add(f'<path d="M{x-7*s} {y+20*s} L{x+7*s} {y+20*s} L{x} {y+28*s}Z" fill="#ff6b8a" stroke="{INK}" stroke-width="{3*s}" stroke-linejoin="round"/>')
    I.add(f'<path d="M{x} {y+28*s} q-10 10 -20 2 M{x} {y+28*s} q10 10 20 2" stroke="{INK}" stroke-width="{4*s}" fill="none" stroke-linecap="round"/>')
    I.add(f'<path d="M{x-40*s} {y+18*s} H{x-80*s} M{x-40*s} {y+28*s} L{x-78*s} {y+36*s} M{x+40*s} {y+18*s} H{x+80*s} M{x+40*s} {y+28*s} L{x+78*s} {y+36*s}" stroke="{INK}" stroke-width="{3*s}" stroke-linecap="round"/>')
    blush(I, x, y + 18 * s, s, 44)

def stars_bg(I, n=22, seed=3, c='#fff'):
    import random; rnd = random.Random(seed)
    for _ in range(n):
        I.add(f'<circle cx="{rnd.uniform(10,502):.0f}" cy="{rnd.uniform(10,502):.0f}" r="{rnd.uniform(1.5,4):.1f}" fill="{c}" opacity="{rnd.uniform(.4,1):.2f}"/>')

def ground(I, y, c, c2=None):
    I.add(f'<path d="M-10 {y} Q128 {y-30} 256 {y} T522 {y} V522 H-10Z" fill="{I.lg(c, c2 or c)}"/>')

ICONS = {}
def icon(*slugs):
    def deco(f):
        for s in slugs: ICONS[s] = f
        return f
    return deco

# ===================== SAGA CÓSMICA =====================
@icon('ruta-cosmica')
def _(I):
    bg(I, '#5b3bd6', '#120a3a', '#9c8cff', .15); stars_bg(I, 30)
    planet(I, 410, 110, 52, '#ff9ad5', '#b03c86', '#ffd23f')
    I.add(f'<path d="M30 420 C150 360 220 470 330 370" fill="none" stroke="#ff7ad9" stroke-width="22" stroke-linecap="round" opacity=".55"/>')
    I.add(f'<path d="M40 450 C160 400 230 500 340 400" fill="none" stroke="#38e5ff" stroke-width="14" stroke-linecap="round" opacity=".55"/>')
    I.add('<g transform="translate(270 270) rotate(-30)">'
          f'<path d="M-40 60 L-70 120 L-10 80Z" {st("#ff5f8f")}/><path d="M40 60 L70 120 L10 80Z" {st("#ff5f8f")}/>'
          f'<path d="M0 -130 C55 -80 55 40 40 80 H-40 C-55 40 -55 -80 0 -130Z" {st(I.lg("#ffffff", "#b9c3ff"))}/>'
          f'<circle cx="0" cy="-30" r="26" {st(I.lg("#7ff3ff", "#2a8fd6"), 8)}/>'
          f'<path d="M-24 80 Q0 160 24 80Z" fill="#ffd23f" stroke="{INK}" stroke-width="7"/><path d="M-12 80 Q0 125 12 80Z" fill="#fff"/></g>')
    shine(I, 255, 200, 14, 40, -30, .6)
    note(I, 120, 200, .9, '#ffd23f'); note(I, 410, 330, .7, '#38e5ff')
    sparkle(I, 90, 90, 18); sparkle(I, 460, 230, 12)

@icon('tiradora-cosmica')
def _(I):
    bg(I, '#2c1c6e', '#0b0724', '#7a5cff', .12); stars_bg(I, 26, 7)
    planet(I, 256, 270, 120, '#7ff3c4', '#1b7a6a', None)
    I.add(f'<path d="M150 230 Q200 210 230 250 T330 240" fill="none" stroke="#0f5a4e" stroke-width="10" opacity=".5"/>')
    I.add(f'<circle cx="256" cy="256" r="170" fill="none" stroke="#ff4fa3" stroke-width="16"/><circle cx="256" cy="256" r="170" fill="none" stroke="{INK}" stroke-width="4" opacity=".6"/>')
    for a in (0, 90, 180, 270):
        x1 = 256 + math.cos(math.radians(a)) * 120; y1 = 256 + math.sin(math.radians(a)) * 120
        x2 = 256 + math.cos(math.radians(a)) * 200; y2 = 256 + math.sin(math.radians(a)) * 200
        I.add(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#ff4fa3" stroke-width="14" stroke-linecap="round"/>')
    I.add(f'<circle cx="256" cy="256" r="14" fill="#ffd23f" stroke="{INK}" stroke-width="5"/>')
    note(I, 300, 290, .65, '#ffd23f'); sparkle(I, 420, 90, 16)

@icon('constructor-cosmico')
def _(I):
    bg(I, '#3a2a8a', '#0d0a2a', '#ffb23e', .1); stars_bg(I, 20, 11)
    planet(I, 420, 100, 40, '#ffd27a', '#d1772a')
    I.add(f'<path d="M-10 330 L120 330 L140 522 H-10Z" {st(I.lg("#b98cff", "#5a3aa6"))}/><path d="M522 330 L392 330 L372 522 H522Z" {st(I.lg("#b98cff", "#5a3aa6"))}/>')
    I.add(f'<rect x="100" y="312" width="312" height="22" rx="6" {st("#ffd23f", 8)}/>')
    xs = [110, 188, 256, 324, 402]
    for i in range(4):
        I.add(f'<path d="M{xs[i]} 312 L{(xs[i]+xs[i+1])/2:.0f} 232 L{xs[i+1]} 312" fill="none" stroke="#ff9a3c" stroke-width="12" stroke-linejoin="round"/>')
    I.add(f'<path d="M149 232 H363" stroke="#ff9a3c" stroke-width="12" stroke-linecap="round"/>')
    for x in xs: I.add(f'<circle cx="{x}" cy="312" r="10" fill="#fff" stroke="{INK}" stroke-width="5"/>')
    I.add(f'<g transform="translate(250 270)"><rect x="-46" y="-10" width="92" height="40" rx="10" {st("#38e5ff", 7)}/><rect x="-28" y="-34" width="48" height="28" rx="8" {st("#bff6ff", 7)}/>'
          f'<circle cx="-26" cy="34" r="14" {st("#2b2440", 6)}/><circle cx="26" cy="34" r="14" {st("#2b2440", 6)}/></g>')
    note(I, 400, 230, .6, '#ffd23f'); sparkle(I, 80, 110, 16)

@icon('paradon-cosmico')
def _(I):
    bg(I, '#1f2f8a', '#090b2c', '#38e5ff', .12); stars_bg(I, 24, 5)
    I.add(f'<path d="M60 470 V170 H452 V470" fill="none" stroke="#fff" stroke-width="18" stroke-linejoin="round"/>')
    for x in range(90, 450, 40): I.add(f'<line x1="{x}" y1="180" x2="{x}" y2="470" stroke="#fff" stroke-width="3" opacity=".25"/>')
    for y in range(200, 470, 40): I.add(f'<line x1="70" y1="{y}" x2="442" y2="{y}" stroke="#fff" stroke-width="3" opacity=".25"/>')
    # balón
    I.add(f'<circle cx="300" cy="230" r="70" {st("#fff")}/><path d="M300 192 L335 215 L322 255 L278 255 L265 215Z" fill="{INK}"/>'
          f'<path d="M300 160 L300 192 M335 215 L367 205 M322 255 L345 285 M278 255 L255 285 M265 215 L233 205" stroke="{INK}" stroke-width="6"/>')
    # guante
    I.add(f'<g transform="translate(190 330) rotate(-20)"><path d="M-60 40 C-70 -20 -60 -80 -40 -90 C-20 -95 -15 -70 -15 -60 C-10 -100 20 -100 22 -70 C30 -95 58 -90 55 -55 C70 -70 90 -55 75 -20 C70 20 40 60 0 70 C-30 75 -55 65 -60 40Z" {st(I.lg("#ffd23f", "#ff8a1f"))}/>'
          f'<rect x="-55" y="60" width="70" height="40" rx="10" {st("#ff4fa3", 8)}/></g>')
    shine(I, 280, 200, 20, 10, -30, .7)
    for x, y in ((380, 120), (420, 300)): sparkle(I, x, y, 18, '#ffd23f')

@icon('cosmic-guitar')
def _(I):
    bg(I, '#b0328f', '#1a0730', '#ff8ad8', .14); stars_bg(I, 20, 9)
    I.add('<g transform="translate(256 270) rotate(35)">'
          f'<rect x="-14" y="-230" width="28" height="200" rx="6" {st("#7a4a2a", 7)}/>'
          + ''.join(f'<line x1="-14" y1="{-200+i*30}" x2="14" y2="{-200+i*30}" stroke="#d9c7a0" stroke-width="4"/>' for i in range(6)) +
          f'<path d="M-24 -262 L24 -262 L18 -222 L-18 -222Z" {st("#2b2440", 7)}/>'
          f'<path d="M0 -40 C70 -60 110 -10 80 40 C110 90 70 150 0 130 C-70 150 -110 90 -80 40 C-110 -10 -70 -60 0 -40Z" {st(I.lg("#38e5ff", "#6a3cff"))}/>'
          f'<path d="M-50 20 L50 -10 L60 20 L-40 50Z" fill="#ff4fa3" stroke="{INK}" stroke-width="5"/>'
          f'<circle cx="0" cy="70" r="20" {st("#1d1442", 5)}/>'
          + ''.join(f'<line x1="{-6+i*4}" y1="-230" x2="{-6+i*4}" y2="80" stroke="#fff" stroke-width="2" opacity=".8"/>' for i in range(4)) + '</g>')
    note(I, 110, 170, .9, '#ffd23f'); note(I, 420, 400, .7, '#38e5ff'); sparkle(I, 410, 110, 20)

# ===================== DEPORTE / VARIOS =====================
@icon('kings-league-mini-game')
def _(I):
    bg(I, '#2c2a3a', '#0c0b14', '#ffd23f', .14)
    ground(I, 400, '#2fbf5c', '#16803a')
    I.add(f'<path d="M136 230 L160 120 L210 180 L256 90 L302 180 L352 120 L376 230Z" {st(I.lg("#ffe680", "#ffb11f"))}/>'
          f'<rect x="130" y="222" width="252" height="40" rx="10" {st("#ffb11f")}/>')
    for x, c in ((256, '#ff4fa3'), (190, '#38e5ff'), (322, '#38e5ff')): I.add(f'<circle cx="{x}" cy="242" r="11" fill="{c}" stroke="{INK}" stroke-width="4"/>')
    I.add(f'<circle cx="256" cy="380" r="66" {st("#fff")}/><path d="M256 344 L290 368 L277 408 L235 408 L222 368Z" fill="{INK}"/>')
    shine(I, 200, 150, 14, 34, -20, .5); sparkle(I, 80, 110, 18, '#ffd23f'); sparkle(I, 440, 150, 14, '#ffd23f')

@icon('anguera-superstars')
def _(I):
    bg(I, '#2bd46a', '#0d6b33', '#ffffff', .14)
    I.add(f'<path d="M-10 330 H522" stroke="#fff" stroke-width="8" opacity=".6"/><circle cx="256" cy="330" r="110" fill="none" stroke="#fff" stroke-width="8" opacity=".6"/>')
    I.add(f'<g transform="translate(220 250) rotate(-12)"><path d="M-110 30 C-110 -30 -60 -40 -20 -30 L40 -60 C60 -70 80 -60 80 -40 L80 0 C130 10 150 40 140 60 L-100 60 C-110 55 -112 45 -110 30Z" {st(I.lg("#ff5a3c", "#c22a1a"))}/>'
          f'<path d="M-100 60 H140" stroke="{INK}" stroke-width="9"/>'
          + ''.join(f'<circle cx="{x}" cy="74" r="9" fill="#fff" stroke="{INK}" stroke-width="4"/>' for x in (-80, -40, 0, 40, 80, 120)) +
          f'<path d="M-30 -10 L60 -40" stroke="#fff" stroke-width="7" stroke-linecap="round"/></g>')
    I.add(f'<circle cx="380" cy="380" r="62" {st("#fff")}/><path d="M380 346 L412 369 L400 406 L360 406 L348 369Z" fill="{INK}"/>')
    sparkle(I, 90, 90, 18); sparkle(I, 440, 120, 14)

@icon('olimpiadas-de-la-granja')
def _(I):
    bg(I, '#7fd6ff', '#3a9fe0', '#ffffff', .2)
    ground(I, 400, '#7ed957', '#3b9a2c')
    I.add(f'<path d="M-10 420 H522" stroke="#fff" stroke-width="6" opacity=".6"/>')
    # cerdito
    I.add(f'<ellipse cx="256" cy="300" rx="120" ry="105" {st(I.rg("#ffd0dc", "#ff8fb0", .4, .35, .8))}/>'
          f'<path d="M160 220 L150 160 L205 200Z M352 220 L362 160 L307 200Z" {st("#ff8fb0", 8)}/>'
          f'<ellipse cx="256" cy="325" rx="46" ry="34" {st("#ff9fbd", 8)}/><ellipse cx="240" cy="325" rx="8" ry="12" fill="{INK}"/><ellipse cx="272" cy="325" rx="8" ry="12" fill="{INK}"/>'
          f'<circle cx="210" cy="270" r="12" fill="{INK}"/><circle cx="302" cy="270" r="12" fill="{INK}"/><circle cx="214" cy="265" r="4" fill="#fff"/><circle cx="306" cy="265" r="4" fill="#fff"/>')
    I.add(f'<path d="M210 395 L256 440 L302 395" fill="none" stroke="#ff4fa3" stroke-width="20" stroke-linejoin="round"/><path d="M210 395 L256 440 L302 395" fill="none" stroke="#38a0ff" stroke-width="7"/>')
    I.add(f'<circle cx="256" cy="458" r="40" {st(I.lg("#ffe680", "#ffb11f"))}/><path d="{star5(256, 460, 22)}" fill="#fff6c2" stroke="{INK}" stroke-width="4"/>')
    sparkle(I, 90, 100, 18); sparkle(I, 430, 130, 16)

# ===================== RITMO =====================
@icon('martin-leyenda-del-rock')
def _(I):
    bg(I, '#ff5a3c', '#5a0f2a', '#ffd23f', .16)
    for x, c in ((110, '#ffd23f'), (256, '#ffffff'), (402, '#38e5ff')):
        I.add(f'<path d="M{x} -20 L{x-70} 520 H{x+70}Z" fill="{c}" opacity=".12"/>')
    I.add('<g transform="translate(256 280) rotate(-35)">'
          f'<rect x="-13" y="-240" width="26" height="190" rx="6" {st("#6b3d1f", 7)}/>'
          f'<path d="M-26 -270 H26 L22 -232 H-22Z" {st("#2b2440", 7)}/>'
          f'<path d="M0 -60 C55 -80 95 -40 70 0 C110 30 95 110 30 120 C10 150 -10 150 -30 120 C-95 110 -110 30 -70 0 C-95 -40 -55 -80 0 -60Z" {st(I.lg("#ffd23f", "#ff8a1f"))}/>'
          f'<path d="M0 -40 C30 -50 55 -30 45 0 C70 20 60 80 20 85 C0 100 -20 85 -20 85 C-60 80 -70 20 -45 0 C-55 -30 -30 -50 0 -40Z" fill="#2b1a0f" opacity=".85"/>'
          f'<rect x="-34" y="40" width="68" height="14" rx="4" fill="#fff" stroke="{INK}" stroke-width="4"/>'
          + ''.join(f'<line x1="{-6+i*4}" y1="-240" x2="{-6+i*4}" y2="48" stroke="#eee" stroke-width="2"/>' for i in range(4)) + '</g>')
    I.add(f'<path d="{star5(420, 110, 40)}" {st("#ffd23f", 7)}/>')
    note(I, 100, 180, .85, '#fff'); sparkle(I, 430, 400, 18)

@icon('supernova-guitar')
def _(I):
    bg(I, '#13d6c8', '#0a1f4a', '#ff4fa3', .14)
    I.add(f'<path d="M-10 380 L522 380" stroke="#ff4fa3" stroke-width="6"/>' + ''.join(f'<path d="M256 380 L{x} 522" stroke="#ff4fa3" stroke-width="4" opacity=".7"/>' for x in range(-200, 720, 90)))
    I.add(f'<circle cx="256" cy="230" r="120" fill="{I.lg("#ffd23f", "#ff4fa3")}"/>' + ''.join(f'<rect x="130" y="{250+i*22}" width="252" height="{6+i*2}" fill="#0a1f4a"/>' for i in range(5)))
    I.add('<g transform="translate(256 300) rotate(-35)">'
          f'<rect x="-12" y="-260" width="24" height="210" rx="5" {st("#1d1442", 7)}/>'
          + ''.join(f'<line x1="-12" y1="{-230+i*30}" x2="12" y2="{-230+i*30}" stroke="#38e5ff" stroke-width="4"/>' for i in range(6)) +
          f'<path d="M-28 -290 L28 -290 L20 -255 L-20 -255Z" {st("#ff4fa3", 7)}/>'
          f'<path d="M0 -60 L80 -110 L60 20 L110 120 L0 70 L-110 120 L-60 20 L-80 -110Z" {st(I.lg("#ffffff", "#9cf7ff"))}/>'
          f'<path d="M-45 10 L45 10 M-50 45 L50 45" stroke="#ff4fa3" stroke-width="10" stroke-linecap="round"/><circle cx="0" cy="-20" r="14" fill="{INK}"/>'
          + ''.join(f'<line x1="{-6+i*4}" y1="-260" x2="{-6+i*4}" y2="60" stroke="#fff" stroke-width="2"/>' for i in range(4)) + '</g>')
    sparkle(I, 90, 100, 18); sparkle(I, 430, 90, 14)

@icon('cabina')
def _(I):
    bg(I, '#ff4fa3', '#3a0f6a', '#ffd23f', .14)
    I.add(f'<rect x="60" y="250" width="392" height="190" rx="30" {st(I.lg("#3a2f7a", "#1d1442"))}/>')
    for x, c in ((165, '#ff9a3c'), (347, '#38e5ff')):
        I.add(f'<circle cx="{x}" cy="335" r="78" {st("#111")}/>' + ''.join(f'<circle cx="{x}" cy="335" r="{r}" fill="none" stroke="#333" stroke-width="3"/>' for r in (40, 55, 68)) +
              f'<circle cx="{x}" cy="335" r="28" fill="{c}" stroke="{INK}" stroke-width="5"/><circle cx="{x}" cy="335" r="6" fill="{INK}"/>')
    I.add(f'<rect x="232" y="290" width="48" height="110" rx="10" fill="#2b2440"/><rect x="238" y="320" width="36" height="22" rx="5" fill="#fff"/>')
    # auriculares
    I.add(f'<path d="M150 210 C150 80 362 80 362 210" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M150 210 C150 80 362 80 362 210" fill="none" stroke="#ffd23f" stroke-width="16" stroke-linecap="round"/>'
          f'<rect x="118" y="170" width="64" height="96" rx="24" {st("#ffd23f")}/><rect x="330" y="170" width="64" height="96" rx="24" {st("#ffd23f")}/>')
    note(I, 440, 120, .6, '#fff'); sparkle(I, 70, 100, 16)

# ===================== HISTORIAS =====================
@icon('l-ultim-estiu')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#ffd9a8", "#ff9e7a")}"/>')
    I.add(f'<circle cx="256" cy="250" r="110" fill="#fff3c4" opacity=".95"/>')
    I.add(f'<path d="M-10 300 Q256 270 522 300 V522 H-10Z" fill="{I.lg("#5aa9d6", "#2a6e9e")}"/>')
    for y, o in ((330, .7), (370, .5), (420, .4)): I.add(f'<path d="M40 {y} q30 -10 60 0 M200 {y+10} q30 -10 60 0 M360 {y} q30 -10 60 0" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round" opacity="{o}"/>')
    I.add(f'<path d="M150 360 Q256 400 362 360 L340 390 Q256 420 172 390Z" {st("#fff", 7)}/><path d="M256 360 V250 L320 345Z" {st("#ff6b5a", 7)}/>')
    I.add(f'<path d="M-10 470 Q140 430 300 470 T522 460 V522 H-10Z" fill="#f2d39a"/>')
    for x, y in ((80, 110), (130, 140), (400, 90)): I.add(f'<path d="M{x} {y} q12 -12 24 0 q12 -12 24 0" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>')

@icon('hotel-miramar')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#1a2350", "#3b4a8a")}"/>'); stars_bg(I, 26, 21, '#f2e9c6')
    I.add(f'<circle cx="420" cy="90" r="36" fill="#f2e9c6"/><circle cx="436" cy="80" r="32" fill="#1f2a5a"/>')
    I.add(f'<rect x="96" y="150" width="320" height="300" {st("#e9d8b4")}/><rect x="84" y="134" width="344" height="26" rx="6" {st("#b5462e")}/>')
    I.add(f'<rect x="150" y="96" width="212" height="44" rx="8" {st("#2b6e9e", 7)}/><text x="256" y="128" text-anchor="middle" font-size="26" font-family="Georgia,serif" font-weight="700" fill="#ffe7a0">MIRAMAR</text>')
    for r in range(3):
        for c in range(4):
            lit = (r, c) in ((0, 1), (1, 3), (2, 0))
            x = 124 + c * 70; y = 180 + r * 80
            I.add(f'<rect x="{x}" y="{y}" width="44" height="54" rx="4" fill="{"#ffd36b" if lit else "#24305f"}" stroke="{INK}" stroke-width="5"/>')
            if lit: I.add(f'<rect x="{x-8}" y="{y-8}" width="60" height="70" rx="10" fill="#ffd36b" opacity=".25"/>')
    I.add(f'<text x="160" y="250" text-anchor="middle" font-size="26" {FONT} fill="#b5462e">7</text>')
    I.add(f'<path d="M-10 452 H522 V522 H-10Z" fill="#0d1a3a"/><path d="M226 450 V400 Q256 370 286 400 V450" {st("#ffd36b", 6)}/>')

# ===================== ACCIÓN =====================
@icon('aura-battle')
def _(I):
    bg(I, '#ffd23f', '#ff4fa3', '#ffffff', .22)
    for r, o in ((190, .25), (150, .35), (115, .45)): I.add(f'<circle cx="256" cy="270" r="{r}" fill="#fff" opacity="{o}"/>')
    I.add(f'<g {st(I.lg("#6a3cff", "#38e5ff"))}><circle cx="256" cy="150" r="44"/>'
          f'<path d="M226 200 H286 L300 320 L330 420 H290 L262 340 L240 420 H200 L222 320Z"/>'
          f'<path d="M232 210 L150 140 L130 160 L220 250Z"/><path d="M280 210 L370 250 L360 275 L276 250Z"/></g>')
    I.add(f'<circle cx="240" cy="146" r="7" fill="{INK}"/><circle cx="272" cy="146" r="7" fill="{INK}"/><path d="M242 168 q14 10 28 0" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    for x, y, r in ((120, 100, 24), (400, 120, 20), (410, 390, 18), (100, 380, 16)): sparkle(I, x, y, r)

@icon('porrazo-party')
def _(I):
    bg(I, '#ff9a1f', '#d4205a', '#ffe680', .2)
    I.add(f'<path d="M330 120 L360 210 L450 190 L380 260 L460 320 L360 310 L340 410 L290 320 L200 380 L240 290 L150 250 L250 240Z" {st("#ffe680", 8)}/>')
    I.add('<g transform="translate(210 270) rotate(-20)">'
          f'<path d="M-30 -110 C60 -130 130 -80 130 0 C130 70 80 110 10 110 C-50 110 -90 80 -90 30 L-90 -40 C-90 -80 -70 -105 -30 -110Z" {st(I.lg("#ff3b3b", "#b0101f"))}/>'
          f'<path d="M-90 -10 C-130 -20 -150 20 -120 50 L-80 60" {st("#e0202f")}/>'
          f'<rect x="-120" y="70" width="110" height="70" rx="16" {st("#fff")}/><path d="M-120 100 H-10" stroke="#e0202f" stroke-width="10"/></g>')
    shine(I, 220, 190, 40, 18, -30, .5)
    I.add(f'<text x="400" y="460" text-anchor="middle" font-size="64" {FONT} fill="#fff" stroke="{INK}" stroke-width="8" paint-order="stroke" transform="rotate(-10 400 460)">POW!</text>')

@icon('tiro-limpio')
def _(I):
    bg(I, '#7fd6ff', '#2b8ad6', '#ffffff', .18)
    for x, h, c in ((40, 220, '#5b6abf'), (130, 300, '#7a86d6'), (230, 180, '#5b6abf'), (330, 260, '#7a86d6'), (420, 210, '#5b6abf')):
        I.add(f'<rect x="{x}" y="{512-h}" width="90" height="{h}" fill="{c}"/>' + ''.join(f'<rect x="{x+15+(i%2)*35}" y="{530-h+(i//2)*40}" width="22" height="22" fill="#ffd36b" opacity=".7"/>' for i in range(min(8, h // 40 * 2))))
    I.add(f'<circle cx="256" cy="240" r="140" fill="#fff" opacity=".25" stroke="{INK}" stroke-width="14"/><circle cx="256" cy="240" r="140" fill="none" stroke="#ff3b3b" stroke-width="6"/>'
          f'<path d="M256 90 V200 M256 280 V390 M106 240 H216 M296 240 H406" stroke="{INK}" stroke-width="10" stroke-linecap="round"/><circle cx="256" cy="240" r="16" {st("#ff3b3b", 6)}/>')
    sparkle(I, 430, 80, 16)

@icon('cube-runner')
def _(I):
    bg(I, '#9a6bff', '#3a1a9a', '#ff9ad5', .15)
    I.add(f'<path d="M256 200 L-60 522 H572Z" fill="{I.lg("#7af0b0", "#2bb36a")}"/><path d="M256 200 L120 522 M256 200 L392 522" stroke="#ff4fa3" stroke-width="10"/>')
    for x, y, s in ((170, 250, 50), (330, 290, 64)):
        I.add(f'<rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" rx="8" {st("#ff5f8f", 7)}/><rect x="{x-s/2+6}" y="{y-s/2+6}" width="{s-12}" height="{s*.25}" rx="4" fill="#fff" opacity=".4"/>')
    I.add(f'<rect x="196" y="320" width="120" height="120" rx="30" {st(I.lg("#ffe680", "#ffb11f"))}/>'
          f'<ellipse cx="236" cy="365" rx="12" ry="18" fill="{INK}"/><ellipse cx="276" cy="365" rx="12" ry="18" fill="{INK}"/><circle cx="240" cy="358" r="5" fill="#fff"/><circle cx="280" cy="358" r="5" fill="#fff"/>')
    for i in range(3): I.add(f'<line x1="{170-i*30}" y1="{350+i*24}" x2="{120-i*30}" y2="{350+i*24}" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".8"/>')
    sparkle(I, 420, 100, 18)

@icon('tower-stack')
def _(I):
    bg(I, '#9cd8ff', '#5a6bff', '#ffffff', .2)
    cols = ['#38e5ff', '#ffd23f', '#ff4fa3', '#7af0b0', '#ff9a3c', '#b98cff']
    for i, c in enumerate(cols):
        y = 440 - i * 52; w = 230 - i * 10; x = 256 - w / 2 + (i % 2) * 8
        I.add(f'<path d="M{x} {y} L{x+w} {y} L{x+w+30} {y-24} L{x+30} {y-24}Z" {st(c, 6)}/><rect x="{x}" y="{y}" width="{w}" height="40" {st(c, 6)}/><rect x="{x}" y="{y}" width="{w}" height="40" fill="#000" opacity=".12"/>')
    I.add(f'<path d="M150 100 L380 100 L410 76 L180 76Z" {st("#fff", 6)}/><rect x="150" y="100" width="230" height="40" {st("#e6eaff", 6)}/>')
    I.add(f'<path d="M256 160 V200" stroke="#fff" stroke-width="8" stroke-dasharray="10 10"/>')
    for x, y, c in ((90, 140, '#ff4fa3'), (430, 180, '#ffd23f'), (420, 70, '#38e5ff')): I.add(f'<rect x="{x}" y="{y}" width="20" height="12" fill="{c}" transform="rotate(30 {x} {y})"/>')

# ===================== MOTOR =====================
@icon('monster-smash')
def _(I):
    bg(I, '#ffd23f', '#ff6a1f', '#ffffff', .2)
    ground(I, 430, '#8a5a3b', '#5c3520')
    I.add(f'<g transform="translate(256 290) rotate(-10)">'
          f'<path d="M-150 10 L-140 -50 L-60 -60 L-30 -120 L70 -120 L100 -60 L160 -50 L165 10Z" {st(I.lg("#ff3b6b", "#b0103a"))}/>'
          f'<path d="M-20 -110 L60 -110 L84 -62 L-40 -62Z" {st("#9cf2ff", 7)}/>'
          f'<rect x="-150" y="0" width="315" height="26" rx="8" {st("#2b2440", 7)}/></g>')
    wheel(I, 150, 380, 78, '#ffd23f'); wheel(I, 380, 340, 78, '#ffd23f')
    shine(I, 200, 230, 50, 12, -10, .45)
    for x, y in ((70, 90), (440, 110)): sparkle(I, x, y, 18)

@icon('moto-fury')
def _(I):
    bg(I, '#38e5ff', '#1b5ad6', '#ffffff', .2)
    I.add(f'<path d="M-10 470 L260 360 L260 522 H-10Z" {st("#c98a4a", 8)}/><path d="M-10 470 L260 360" stroke="#7a4a2a" stroke-width="6"/>')
    I.add('<g transform="translate(256 250) rotate(-24)">')
    wheel(I, -120, 70, 62, '#fff'); wheel(I, 125, 70, 62, '#fff')
    I.add(f'<path d="M-120 70 L-40 0 L60 0 L125 70" fill="none" stroke="{INK}" stroke-width="14" stroke-linejoin="round"/>'
          f'<path d="M-70 -10 L-20 -50 L70 -50 L110 -20 L60 20 L-40 20Z" {st(I.lg("#ffd23f", "#ff8a1f"))}/>'
          f'<path d="M80 -50 L120 -100" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M105 -100 H145" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
          f'<path d="M-30 -50 L10 -120 L50 -110 L40 -50Z" {st("#ff3b6b", 8)}/><path d="M40 -110 L110 -95" stroke="#ff3b6b" stroke-width="20" stroke-linecap="round"/><path d="M40 -110 L110 -95" stroke="{INK}" stroke-width="4" stroke-linecap="round" opacity=".4"/>'
          f'<circle cx="25" cy="-150" r="34" {st(I.lg("#ffffff", "#c9d2ff"), 8)}/><path d="M30 -158 H62 V-140 H30Z" fill="{INK}"/>'
          f'<path d="M-10 -20 L-50 40 L-90 50" fill="none" stroke="#2b2440" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></g>')
    for i in range(3): I.add(f'<line x1="{100-i*22}" y1="{170+i*40}" x2="{30-i*22}" y2="{195+i*40}" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".8"/>')
    sparkle(I, 430, 80, 20, '#ffd23f')

@icon('turbo-kart-rally')
def _(I):
    bg(I, '#7af0b0', '#1b9a6a', '#ffffff', .2)
    I.add(f'<path d="M-10 360 Q256 300 522 360 V522 H-10Z" fill="#5a5f7a"/><path d="M-10 420 Q256 360 522 420" stroke="#fff" stroke-width="10" stroke-dasharray="30 24" fill="none"/>')
    I.add(f'<path d="M90 300 Q40 290 20 320 Q50 330 40 350 Q70 340 90 340Z" fill="#ff9a3c" stroke="{INK}" stroke-width="6"/><path d="M90 310 Q60 310 50 325 Q70 330 90 330Z" fill="#ffd23f"/>')
    I.add(f'<path d="M100 330 L130 250 L330 240 L420 290 L420 340Z" {st(I.lg("#ff3b3b", "#c01020"))}/><path d="M300 250 L330 200 L360 200 L350 250Z" {st("#2b2440", 7)}/>'
          f'<circle cx="250" cy="215" r="40" {st(I.lg("#ffd23f", "#ff9a1f"), 8)}/><rect x="215" y="205" width="70" height="20" rx="8" fill="#9cf2ff" stroke="{INK}" stroke-width="5"/>')
    wheel(I, 150, 350, 48, '#ffd23f'); wheel(I, 370, 350, 48, '#ffd23f')
    I.add(f'<path d="M150 200 L170 160 L200 190" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round"/>')
    sparkle(I, 430, 100, 18)

@icon('neon-coast')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#2a0b5a", "#ff4fa3")}"/>')
    I.add(f'<circle cx="256" cy="230" r="120" fill="{I.lg("#ffe680", "#ff4f8a")}"/>' + ''.join(f'<rect x="130" y="{250+i*22}" width="252" height="{5+i*2}" fill="#5a1a7a"/>' for i in range(5)))
    I.add(f'<path d="M-10 310 L130 250 L200 300 L300 240 L522 310 V330 H-10Z" fill="#3a0f6a"/>')
    I.add(f'<path d="M256 320 L-120 522 H632Z" fill="#1a0533"/>' + ''.join(f'<path d="M256 320 L{x} 522" stroke="#38e5ff" stroke-width="4"/>' for x in (-60, 140, 372, 572)) + ''.join(f'<line x1="-10" y1="{y}" x2="522" y2="{y}" stroke="#38e5ff" stroke-width="3" opacity=".6"/>' for y in (350, 390, 450)))
    I.add(f'<path d="M176 470 L196 400 H316 L336 470Z" {st(I.lg("#ff3b8a", "#b0105a"))}/><rect x="166" y="440" width="180" height="50" rx="12" {st("#ff4f9a")}/><rect x="196" y="410" width="120" height="30" rx="6" fill="#9cf2ff" stroke="{INK}" stroke-width="5"/>'
          f'<rect x="178" y="452" width="40" height="14" rx="5" fill="#fff36b"/><rect x="294" y="452" width="40" height="14" rx="5" fill="#fff36b"/>')

@icon('aventura-porc')
def _(I):
    bg(I, '#9ce8ff', '#4ab0ff', '#ffffff', .22)
    I.add(f'<path d="M-10 380 C100 380 120 160 220 160 C330 160 300 330 420 330 C470 330 500 300 522 280" fill="none" stroke="#c0392b" stroke-width="20"/><path d="M-10 400 C100 400 120 180 220 180 C330 180 300 350 420 350 C470 350 500 320 522 300" fill="none" stroke="#e74c3c" stroke-width="10"/>')
    for x in (40, 110, 330, 420, 480): I.add(f'<line x1="{x}" y1="512" x2="{x}" y2="{400 if x<200 else 350}" stroke="#8a5a3b" stroke-width="10"/>')
    I.add(f'<g transform="translate(250 300) rotate(-8)"><path d="M-110 -10 H110 L95 70 H-95Z" {st(I.lg("#ffd23f", "#ff9a1f"))}/>'
          f'<ellipse cx="0" cy="-50" rx="70" ry="60" {st("#ffb3c8")}/><path d="M-55 -95 L-70 -130 L-30 -105Z M55 -95 L70 -130 L30 -105Z" {st("#ff8fb0", 6)}/>'
          f'<ellipse cx="0" cy="-30" rx="26" ry="18" {st("#ff9fbd", 6)}/><circle cx="-9" cy="-30" r="5" fill="{INK}"/><circle cx="9" cy="-30" r="5" fill="{INK}"/><circle cx="-28" cy="-65" r="8" fill="{INK}"/><circle cx="28" cy="-65" r="8" fill="{INK}"/>'
          f'<path d="M-80 -60 L-130 -110 M80 -60 L130 -110" stroke="#ffb3c8" stroke-width="18" stroke-linecap="round"/></g>')
    sparkle(I, 430, 90, 18)

# ===================== CON MARCA =====================
@icon('suo-shop-rush')
def _(I):
    bg(I, '#ffe7c2', '#f2a65a', '#ffffff', .25)
    I.add(f'<path d="M150 210 L362 210 L392 450 H120Z" {st(I.lg("#ff7a3c", "#d14a1a"))}/><path d="M200 210 C200 140 312 140 312 210" fill="none" stroke="{INK}" stroke-width="14"/>')
    I.add(f'<text x="256" y="350" text-anchor="middle" font-size="76" {FONT} fill="#fff">SÛO</text>')
    I.add(f'<g transform="translate(360 400) rotate(-15)"><path d="M-110 20 C-110 -30 -70 -40 -40 -30 L10 -60 C30 -70 50 -60 50 -40 V-10 C100 0 120 20 110 40 H-100 C-110 35 -112 28 -110 20Z" {st("#fff8ec")}/><path d="M-100 40 H110" stroke="{INK}" stroke-width="9"/><path d="M-20 -30 L40 -48" stroke="#ff7a3c" stroke-width="8" stroke-linecap="round"/></g>')
    sparkle(I, 90, 100, 18, '#ff7a3c')

@icon('mnac-rush')
def _(I):
    bg(I, '#ffe9a8', '#e0a43a', '#ffffff', .25)
    I.add(f'<path d="M110 250 L256 140 L402 250Z" {st("#f2e2c0")}/><rect x="96" y="250" width="320" height="30" {st("#e9d2a5")}/>'
          f'<path d="M206 170 Q256 100 306 170Z" {st("#9cb7c9", 7)}/>')
    for x in range(126, 400, 52): I.add(f'<rect x="{x}" y="280" width="30" height="120" {st("#fff8e6", 6)}/>')
    I.add(f'<rect x="80" y="400" width="352" height="40" {st("#e9d2a5")}/>')
    I.add(f'<g transform="translate(360 150) rotate(8)"><rect x="-60" y="-50" width="120" height="100" {st("#c9962a")}/><rect x="-44" y="-34" width="88" height="68" fill="#2a6e9e"/><circle cx="-10" cy="0" r="18" fill="#ffd36b"/><path d="M-44 34 L-10 0 L20 20 L44 -6 V34Z" fill="#2f7a4a"/></g>')
    sparkle(I, 90, 100, 18)

# ===================== RELAX =====================
@icon('relax-estanque-de-koi')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.rg("#4fd6c4", "#0f5a5e", .5, .5, .8)}"/>')
    for r in (60, 120, 180, 240): I.add(f'<circle cx="256" cy="256" r="{r}" fill="none" stroke="#bff6ec" stroke-width="5" opacity=".35"/>')
    for x, y, rot in ((90, 110, 0), (420, 400, 120), (430, 120, 40)): I.add(f'<path d="M{x} {y} m-46 0 a46 46 0 1 0 92 0 a46 46 0 1 0 -92 0 M{x} {y} L{x+46} {y-10}" {st("#3fbf6a", 6)} transform="rotate({rot} {x} {y})"/>')
    for (x, y, rot, c) in ((230, 230, -30, '#ff7a3c'), (300, 320, 150, '#ffffff')):
        I.add(f'<g transform="translate({x} {y}) rotate({rot})"><path d="M-80 0 C-40 -45 40 -45 70 0 C40 45 -40 45 -80 0Z" {st(c)}/><path d="M60 0 L110 -35 L100 0 L110 35Z" {st(c, 7)}/>'
              f'<circle cx="-50" cy="-8" r="6" fill="{INK}"/><path d="M-10 -25 q15 25 0 50" fill="#ff3b3b" opacity=".7"/></g>')
    sparkle(I, 140, 400, 14)

@icon('relax-farolillos-del-lago')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#1a1650", "#5a3f7a")}"/>'); stars_bg(I, 30, 33)
    I.add(f'<path d="M-10 330 L80 270 L170 320 L260 250 L370 320 L522 270 V340 H-10Z" fill="#2a1f4a"/><rect y="340" width="512" height="172" fill="{I.lg("#2a2560", "#120f30")}"/>')
    for (x, y, s) in ((256, 200, 1.4), (130, 120, .9), (380, 110, 1), (410, 250, .7), (90, 260, .6), (300, 80, .55)):
        I.add(f'<g transform="translate({x} {y}) scale({s})"><circle r="70" fill="#ffb347" opacity=".25"/><path d="M-32 -40 H32 L40 30 Q0 46 -40 30Z" {st(I.lg("#ffe28a", "#ff8a2a"), 7)}/><rect x="-14" y="30" width="28" height="12" rx="4" fill="#ff5a2a" stroke="{INK}" stroke-width="5"/></g>')
        I.add(f'<ellipse cx="{x}" cy="{690-y*1:.0f}" rx="{14*s:.0f}" ry="{5*s:.0f}" fill="#ffb347" opacity=".35"/>')

@icon('relax-pompas-musicales')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#cfb6ff", "#8fe3e0")}"/>')
    for (x, y, r) in ((200, 210, 110), (370, 150, 60), (360, 360, 80), (110, 400, 50), (90, 110, 36)):
        I.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{I.rg("#ffffff", "#c9a6ff", .35, .3, .9)}" fill-opacity=".55" stroke="#fff" stroke-width="6"/>')
        I.add(f'<ellipse cx="{x-r*.4}" cy="{y-r*.45}" rx="{r*.22}" ry="{r*.12}" fill="#fff" transform="rotate(-35 {x-r*.4} {y-r*.45})"/>')
    note(I, 200, 250, .9, '#ff7ad9')

@icon('relax-isla-jardin')
def _(I):
    bg(I, '#bfe6ff', '#7ab8e8', '#ffffff', .2)
    I.add(f'<ellipse cx="120" cy="120" rx="60" ry="22" fill="#fff" opacity=".8"/><ellipse cx="400" cy="90" rx="50" ry="18" fill="#fff" opacity=".8"/>')
    I.add(f'<path d="M100 280 Q256 240 412 280 L330 420 L256 470 L190 420Z" {st(I.lg("#c98a5a", "#7a4a2a"))}/><ellipse cx="256" cy="280" rx="156" ry="40" {st(I.lg("#8de06a", "#4aa63a"))}/>')
    I.add(f'<rect x="300" y="190" width="14" height="80" fill="#7a4a2a" stroke="{INK}" stroke-width="5"/><circle cx="307" cy="180" r="50" {st("#5ac65a")}/>')
    for x, c in ((170, '#ff4fa3'), (215, '#ffd23f'), (370, '#ff7a3c')):
        I.add(f'<line x1="{x}" y1="280" x2="{x}" y2="245" stroke="#2f7a2f" stroke-width="6"/>' + ''.join(f'<circle cx="{x+10*math.cos(a):.0f}" cy="{240+10*math.sin(a):.0f}" r="9" fill="{c}" stroke="{INK}" stroke-width="3"/>' for a in [k * 1.257 for k in range(5)]) + f'<circle cx="{x}" cy="240" r="7" fill="#fff36b"/>')

@icon('relax-jardin-zen')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#efe0bf", "#d5bf92")}"/>')
    for k in range(-6, 14): I.add(f'<path d="M-10 {k*44} C150 {k*44-30} 360 {k*44+30} 522 {k*44}" fill="none" stroke="#c4a873" stroke-width="5"/>')
    for (x, y, r) in ((180, 200, 70), (360, 340, 52)):
        for rr in (r + 26, r + 50, r + 74): I.add(f'<ellipse cx="{x}" cy="{y}" rx="{rr}" ry="{rr*.7:.0f}" fill="none" stroke="#c4a873" stroke-width="5"/>')
        I.add(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.75:.0f}" {st(I.lg("#9a9aa8", "#5a5a6a"))}/>'); shine(I, x - r * .3, y - r * .3, r * .3, r * .15, -20, .5)
    I.add(f'<g transform="translate(400 120) rotate(30)"><rect x="-6" y="-10" width="12" height="150" fill="#9a6a3a" stroke="{INK}" stroke-width="4"/><rect x="-50" y="-20" width="100" height="18" rx="4" {st("#9a6a3a", 5)}/>' + ''.join(f'<rect x="{-44+i*18}" y="-4" width="6" height="22" fill="#7a4a2a"/>' for i in range(6)) + '</g>')

@icon('relax-cristal-de-lluvia')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#16204a", "#0a0f26")}"/>')
    for x, h in ((20, 220), (110, 300), (210, 180), (300, 260), (400, 320)):
        I.add(f'<rect x="{x}" y="{512-h}" width="80" height="{h}" fill="#1f2c5a"/>' + ''.join(f'<rect x="{x+12+(i%3)*22}" y="{530-h+(i//3)*34}" width="12" height="16" fill="#ffd36b" opacity="{.4+(i%2)*.4}"/>' for i in range(9)))
    I.add(f'<rect width="512" height="512" fill="#8fa6d6" opacity=".22"/><path d="M256 0 V512 M0 256 H512" stroke="#2b2440" stroke-width="22"/>')
    I.add(f'<path d="M80 120 Q120 90 160 120 T240 130" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".55"/><path d="M300 330 q40 -40 80 0 q40 40 80 0" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".55"/>')
    import random; rnd = random.Random(4)
    for _ in range(24):
        x, y, r = rnd.uniform(10, 500), rnd.uniform(10, 500), rnd.uniform(5, 13)
        I.add(f'<path d="M{x:.0f} {y-r*1.6:.0f} Q{x+r:.0f} {y:.0f} {x:.0f} {y+r:.0f} Q{x-r:.0f} {y:.0f} {x:.0f} {y-r*1.6:.0f}Z" fill="#cfe0ff" opacity=".85"/>')

@icon('relax-hoguera-nocturna')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#0a1438", "#1c2a4a")}"/>'); stars_bg(I, 34, 41)
    I.add(f'<circle cx="256" cy="330" r="190" fill="#ff9a3c" opacity=".2"/><ellipse cx="256" cy="440" rx="240" ry="60" fill="#13203a"/>')
    I.add(f'<path d="M140 420 L370 380 M150 380 L370 430" stroke="{INK}" stroke-width="40" stroke-linecap="round"/><path d="M140 420 L370 380 M150 380 L370 430" stroke="#8a5a3b" stroke-width="26" stroke-linecap="round"/>')
    I.add(f'<path d="M256 140 C320 220 340 260 320 320 C310 370 280 400 256 400 C220 400 190 370 186 330 C180 280 210 250 220 210 C240 250 250 250 256 140Z" {st(I.lg("#ffd23f", "#ff3b1f"))}/>'
          f'<path d="M256 250 C290 300 290 340 270 370 C260 385 250 385 240 370 C222 345 230 300 256 250Z" fill="#fff3a0"/>')
    for x, y in ((180, 200), (340, 170), (300, 120)): I.add(f'<circle cx="{x}" cy="{y}" r="5" fill="#ffd23f"/>')

@icon('relax-bola-de-nieve')
def _(I):
    bg(I, '#3a2a5a', '#120a24', '#9cc7ff', .1)
    I.add(f'<path d="M150 400 H362 L392 470 H120Z" {st(I.lg("#a0603a", "#5c3520"))}/>')
    I.add(f'<circle cx="256" cy="260" r="160" fill="{I.rg("#e6f3ff", "#7fb0e6", .5, .4, .9)}" stroke="{INK}" stroke-width="{SW}"/>')
    I.add(f'<path d="M110 330 Q256 300 402 330 Q380 400 256 412 Q130 400 110 330Z" fill="#fff"/>')
    I.add(f'<path d="M256 170 L320 280 H192Z" {st("#3faa6a", 7)}/><path d="M256 220 L340 330 H172Z" {st("#2f8a5a", 7)}/><rect x="246" y="330" width="20" height="26" fill="#7a4a2a"/>')
    import random; rnd = random.Random(8)
    for _ in range(26):
        a = rnd.uniform(0, 6.28); d = rnd.uniform(0, 140)
        I.add(f'<circle cx="{256+d*math.cos(a):.0f}" cy="{260+d*math.sin(a)*.85:.0f}" r="{rnd.uniform(3,7):.1f}" fill="#fff"/>')
    shine(I, 180, 160, 40, 18, -40, .6)

@icon('relax-pesca-al-atardecer')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#4a3a8a", "#ff9a6a")}"/>')
    I.add(f'<circle cx="256" cy="290" r="90" fill="#ffd27a"/><path d="M-10 300 L120 230 L210 290 L330 220 L522 300 V320 H-10Z" fill="#5a3a7a"/>')
    I.add(f'<rect y="310" width="512" height="202" fill="{I.lg("#f28c6a", "#3a2a6a")}"/>' + ''.join(f'<rect x="{180+i*14}" y="{330+i*22}" width="{150-i*28}" height="6" rx="3" fill="#ffd27a" opacity=".7"/>' for i in range(5)))
    I.add(f'<path d="M-10 430 H220 V460 H-10Z" {st("#8a5a3b", 7)}/><line x1="60" y1="460" x2="60" y2="522" stroke="{INK}" stroke-width="18"/>')
    I.add(f'<path d="M120 430 L380 140" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M380 140 Q440 260 420 390" stroke="#fff" stroke-width="3" fill="none"/><circle cx="420" cy="392" r="12" {st("#ff3b3b", 5)}/>')

@icon('relax-arrecife-de-coral')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#4fc3e0", "#0a3a5a")}"/>')
    for x in (100, 260, 400): I.add(f'<path d="M{x} 0 L{x-40} 512 H{x+40}Z" fill="#fff" opacity=".08"/>')
    I.add(f'<path d="M-10 430 Q256 380 522 430 V522 H-10Z" fill="#e8d29a"/>')
    I.add(f'<path d="M80 440 C70 360 40 330 50 300 M80 400 C100 360 120 350 130 320 M80 380 C60 360 30 360 20 340" stroke="#ff5f8f" stroke-width="22" fill="none" stroke-linecap="round"/>'
          f'<path d="M400 440 C400 380 380 350 390 310 M400 400 C430 380 450 360 455 330" stroke="#ffb23e" stroke-width="22" fill="none" stroke-linecap="round"/>')
    I.add(f'<g transform="translate(250 230)"><path d="M-70 0 C-30 -50 40 -50 70 0 C40 50 -30 50 -70 0Z" {st(I.lg("#ffd23f", "#ff8a1f"))}/><path d="M60 0 L110 -40 V40Z" {st("#ff8a1f", 7)}/>'
          f'<path d="M-20 -38 V38 M10 -40 V40" stroke="#fff" stroke-width="10"/><circle cx="-45" cy="-6" r="7" fill="{INK}"/></g>')
    I.add(f'<ellipse cx="256" cy="440" rx="44" ry="22" {st("#d9c7ff", 6)}/><circle cx="256" cy="430" r="12" fill="#fff"/>')
    for x, y, r in ((120, 160, 10), (140, 120, 7), (380, 120, 12), (400, 80, 7)): I.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#fff" stroke-width="4" opacity=".8"/>')

@icon('relax-velero-entre-islas')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#9cd2ff", "#e2f1ff")}"/>')
    I.add(f'<path d="M300 300 Q360 200 420 300Z" fill="#6fbf6a"/><rect x="390" y="230" width="18" height="70" fill="#fff" stroke="{INK}" stroke-width="4"/><rect x="386" y="214" width="26" height="18" fill="#ff3b3b" stroke="{INK}" stroke-width="4"/>')
    I.add(f'<rect y="290" width="512" height="222" fill="{I.lg("#4f9be0", "#1f5a9e")}"/>' + ''.join(f'<path d="M{x} {y} q20 -10 40 0" stroke="#fff" stroke-width="6" fill="none" opacity=".6" stroke-linecap="round"/>' for x, y in ((60, 340), (380, 360), (120, 450), (330, 470))))
    I.add(f'<path d="M140 380 H380 L340 430 H180Z" {st(I.lg("#8a5a3b", "#5c3520"))}/><path d="M256 100 V380" stroke="{INK}" stroke-width="10"/>'
          f'<path d="M266 110 Q360 230 266 360Z" {st("#fff")}/><path d="M246 140 Q170 250 246 360Z" {st("#ffd23f")}/><path d="M256 100 L300 115 L256 130Z" fill="#ff4fa3" stroke="{INK}" stroke-width="5"/>')

@icon('relax-orilla-y-marea')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#4d6fb0", "#ffc9a0")}"/>')
    I.add(f'<path d="M-10 230 Q256 200 522 240 V522 H-10Z" fill="#5fb8b4"/><path d="M-10 300 Q140 260 300 300 T522 290 V522 H-10Z" fill="#fff" opacity=".7"/><path d="M-10 320 Q140 280 300 320 T522 310 V522 H-10Z" fill="#f2d39a"/>')
    I.add(f'<g transform="translate(256 390) rotate(-10)"><path d="M0 -90 C60 -90 100 -40 100 20 C100 60 70 70 0 70 C-70 70 -100 60 -100 20 C-100 -40 -60 -90 0 -90Z" {st(I.lg("#ffe6ef", "#ff9ab8"))}/>'
          + ''.join(f'<path d="M0 60 L{math.sin(a)*90:.0f} {-math.cos(a)*80:.0f}" stroke="{INK}" stroke-width="5" opacity=".6"/>' for a in (-1.0, -.5, 0, .5, 1.0)) + f'<rect x="-30" y="60" width="60" height="22" rx="8" {st("#ff9ab8", 6)}/></g>')
    for x, y in ((90, 440), (130, 470), (410, 450), (440, 480)): I.add(f'<ellipse cx="{x}" cy="{y}" rx="12" ry="7" fill="#d9b77a"/>')

@icon('relax-vuelo-del-amanecer')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#6f9fd8", "#ffd9b8")}"/><circle cx="256" cy="330" r="100" fill="#fff1c1"/>')
    I.add(f'<path d="M-10 360 L100 260 L190 340 L300 230 L420 330 L522 270 V522 H-10Z" fill="#7a8fc9"/><path d="M-10 420 L120 340 L250 420 L380 350 L522 420 V522 H-10Z" fill="#5a6fa9"/>')
    I.add(f'<circle cx="256" cy="200" r="70" fill="none" stroke="#ffd23f" stroke-width="12"/>')
    I.add(f'<g transform="translate(256 210) rotate(-8)"><path d="M0 0 C-60 -70 -150 -60 -190 -30 C-130 -30 -70 -10 0 20Z" {st("#fff")}/><path d="M0 0 C60 -70 150 -60 190 -30 C130 -30 70 -10 0 20Z" {st("#fff")}/>'
          f'<ellipse cx="0" cy="10" rx="40" ry="20" {st("#fff")}/><path d="M36 4 L60 10 L36 18Z" fill="#ffb23e" stroke="{INK}" stroke-width="4"/><circle cx="22" cy="6" r="4" fill="{INK}"/></g>')

@icon('relax-aurora-boreal')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#01040f", "#123055")}"/>'); stars_bg(I, 40, 51)
    for (y, c, o) in ((140, '#6ef0b0', .55), (190, '#38e5ff', .4), (110, '#b98cff', .35)):
        I.add(f'<path d="M-20 {y} C100 {y-90} 200 {y+60} 300 {y-30} S480 {y-60} 540 {y-10} L540 {y+120} C420 {y+60} 300 {y+150} 180 {y+90} S20 {y+140} -20 {y+110}Z" fill="{c}" opacity="{o}"/>')
    I.add(f'<path d="M-10 400 L60 300 L130 400 L200 320 L270 400 L360 290 L450 400 L522 330 V522 H-10Z" fill="#0b1830"/>')
    I.add(f'<rect y="420" width="512" height="92" fill="{I.lg("#bfe6ff", "#6aa0d6")}"/><path d="M380 70 L470 40" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="470" cy="40" r="7" fill="#fff"/>')

@icon('relax-orbitas-musicales')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.rg("#2a1f6a", "#05040d", .5, .5, .8)}"/>'); stars_bg(I, 30, 61)
    for r in (110, 170, 225): I.add(f'<ellipse cx="256" cy="256" rx="{r}" ry="{r*.62:.0f}" fill="none" stroke="#b58cff" stroke-width="4" opacity=".5"/>')
    I.add(f'<circle cx="256" cy="256" r="64" fill="#ffd23f" opacity=".3"/><circle cx="256" cy="256" r="48" {st(I.rg("#fff3a0", "#ff9a1f", .4, .35, .8))}/>')
    planet(I, 366, 205, 26, '#7ff3ff', '#2a6ad6'); planet(I, 110, 300, 34, '#ff9ad5', '#b03c86', '#ffd23f'); planet(I, 330, 380, 22, '#9cff8a', '#2a9a4a')
    note(I, 150, 150, .6, '#ffd23f'); note(I, 420, 330, .5, '#38e5ff')

@icon('relax-constelaciones')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#020411", "#1a2b4a")}"/>'); stars_bg(I, 50, 71)
    pts = [(90, 140), (180, 110), (250, 170), (330, 130), (420, 190), (380, 300), (270, 330), (160, 290)]
    I.add('<path d="M' + ' L'.join(f'{x} {y}' for x, y in pts) + f' L250 170" fill="none" stroke="#bfd6ff" stroke-width="5" opacity=".8"/>')
    for x, y in pts: I.add(f'<circle cx="{x}" cy="{y}" r="16" fill="#bfd6ff" opacity=".25"/>'); sparkle(I, x, y, 16)
    I.add(f'<path d="M-10 440 Q256 400 522 440 V522 H-10Z" fill="#0a1226"/>')

@icon('relax-cometa-al-viento')
def _(I):
    bg(I, '#9ad0ff', '#3f86d6', '#ffffff', .2)
    I.add(f'<ellipse cx="110" cy="130" rx="70" ry="24" fill="#fff" opacity=".85"/><ellipse cx="400" cy="420" rx="80" ry="26" fill="#fff" opacity=".8"/>')
    I.add(f'<path d="M256 80 L360 200 L256 340 L152 200Z" {st(I.lg("#ff6b5a", "#d63a2a"))}/><path d="M256 80 V340 M152 200 H360" stroke="{INK}" stroke-width="6"/><path d="M256 80 L360 200 L256 200Z" fill="#ffd23f" opacity=".85"/>')
    I.add(f'<path d="M256 340 C230 380 290 400 260 440 C240 470 280 490 270 520" stroke="{INK}" stroke-width="5" fill="none"/>' + ''.join(f'<path d="M{x} {y} l-16 -10 l0 20Z" fill="{c}" stroke="{INK}" stroke-width="3"/>' for x, y, c in ((248, 380, '#38e5ff'), (276, 430, '#ff4fa3'), (262, 480, '#7af0b0'))))
    for x, y in ((100, 300), (420, 120), (400, 260)): I.add(f'<circle cx="{x}" cy="{y}" r="8" fill="#fff"/>' + ''.join(f'<line x1="{x}" y1="{y}" x2="{x+16*math.cos(a):.0f}" y2="{y+16*math.sin(a):.0f}" stroke="#fff" stroke-width="2"/>' for a in [k * .785 for k in range(8)]))

@icon('relax-rana-y-luciernagas')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#06181c", "#0f3a3e")}"/>')
    for x, y in ((100, 120), (400, 90), (430, 250), (80, 300), (300, 150)): I.add(f'<circle cx="{x}" cy="{y}" r="22" fill="#e8ff6a" opacity=".2"/><circle cx="{x}" cy="{y}" r="7" fill="#f4ff9a"/>')
    I.add(f'<path d="M100 400 m-110 0 a110 40 0 1 0 220 0 a110 40 0 1 0 -220 0" {st("#3faa5a")} transform="translate(160 0)"/>')
    I.add(f'<g transform="translate(256 360)"><ellipse cx="0" cy="0" rx="90" ry="62" {st(I.lg("#8de06a", "#3a9a3a"))}/>'
          f'<circle cx="-42" cy="-56" r="30" {st("#8de06a")}/><circle cx="42" cy="-56" r="30" {st("#8de06a")}/><circle cx="-42" cy="-56" r="14" fill="{INK}"/><circle cx="42" cy="-56" r="14" fill="{INK}"/><circle cx="-37" cy="-61" r="5" fill="#fff"/><circle cx="47" cy="-61" r="5" fill="#fff"/>'
          f'<path d="M-40 10 Q0 40 40 10" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/><ellipse cx="0" cy="24" rx="50" ry="20" fill="#c9f2a0" opacity=".7"/></g>')
    I.add(f'<path d="M270 360 Q340 300 330 180" stroke="#ff6b8a" stroke-width="10" fill="none" stroke-linecap="round"/><circle cx="330" cy="176" r="12" fill="#f4ff9a"/>')

# ===================== CATQUIZ =====================
CQ_BG = ('#7fd0ff', '#4a7dff')
def cq_bg(I, a='#7fd0ff', b='#4a7dff'): bg(I, a, b, '#ffffff', .18)

@icon('catquiz-com-es-diu-en-catala')
def _(I):
    cq_bg(I, '#ffd23f', '#ff8a1f')
    I.add(f'<path d="M90 110 H422 Q452 110 452 140 V330 Q452 360 422 360 H230 L150 430 L170 360 H90 Q60 360 60 330 V140 Q60 110 90 110Z" {st("#fff")}/>')
    I.add(f'<text x="256" y="300" text-anchor="middle" font-size="210" {FONT} fill="#6a3cff">?</text>')
    sparkle(I, 450, 70, 18); sparkle(I, 60, 440, 14)

@icon('catquiz-l-intrus')
def _(I):
    cq_bg(I, '#b98cff', '#5a3ad6')
    for (x, y, c) in ((150, 160, '#ff4fa3'), (360, 160, '#ff4fa3'), (150, 360, '#ff4fa3')): I.add(f'<circle cx="{x}" cy="{y}" r="80" {st(c)}/>'); shine(I, x - 25, y - 30, 22, 12, -30, .5)
    I.add(f'<g transform="rotate(12 360 360)"><rect x="285" y="285" width="150" height="150" rx="24" {st("#ffd23f")}/></g>')
    I.add(f'<text x="360" y="395" text-anchor="middle" font-size="100" {FONT} fill="{INK}" transform="rotate(12 360 360)">!</text>')

@icon('catquiz-motle')
def _(I):
    cq_bg(I, '#7af0b0', '#1b9a6a')
    letters = [('C', '#7a86a6'), ('A', '#ffc93a'), ('S', '#4fc35a'), ('A', '#4fc35a'), ('L', '#7a86a6')]
    for i, (ch, c) in enumerate(letters): tile(I, 26 + i * 94, 140, 84, ch, c, '#fff', 54, 14)
    for i in range(5): tile(I, 26 + i * 94, 240, 84, '', '#ffffff', INK, 54, 14)
    for i, (ch, c) in enumerate([('M', '#4fc35a'), ('O', '#4fc35a'), ('T', '#4fc35a'), ('L', '#4fc35a'), ('E', '#4fc35a')]): tile(I, 26 + i * 94, 340, 84, ch, c, '#fff', 54, 14)
    sparkle(I, 450, 80, 18)

@icon('catquiz-accents')
def _(I):
    cq_bg(I, '#38e5ff', '#2a6ad6')
    tile(I, 120, 150, 272, '', '#fff', INK, 0, 40)
    I.add(f'<text x="256" y="390" text-anchor="middle" font-size="230" {FONT} fill="#6a3cff">e</text>')
    I.add(f'<path d="M230 150 L310 70" stroke="{INK}" stroke-width="44" stroke-linecap="round"/><path d="M230 150 L310 70" stroke="#ff4fa3" stroke-width="26" stroke-linecap="round"/>')
    sparkle(I, 80, 90, 18); sparkle(I, 440, 430, 16)

@icon('catquiz-penjat-3d')
def _(I):
    cq_bg(I, '#ffb23e', '#d14a1a')
    I.add(f'<path d="M100 440 H260 M150 440 V90 H330 V150" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/><path d="M100 440 H260 M150 440 V90 H330" fill="none" stroke="#8a5a3b" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>')
    I.add(f'<circle cx="330" cy="200" r="46" {st("#fff")}/><path d="M330 246 V340 M330 270 L290 310 M330 270 L370 310" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>')
    for i, ch in enumerate('A_E_'): tile(I, 230 + i * 64, 400, 56, ch.replace('_', ''), '#fff', INK, 36, 12)

@icon('catquiz-anagrama')
def _(I):
    cq_bg(I, '#ff7ad9', '#a03cff')
    for (x, y, r, ch, c) in ((90, 120, -14, 'P', '#ffd23f'), (300, 90, 10, 'A', '#38e5ff'), (190, 200, -6, 'R', '#7af0b0'), (360, 230, 16, 'U', '#ff9a3c'), (90, 300, 12, 'A', '#ffffff'), (250, 330, -12, 'L', '#ffd23f')):
        I.add(f'<g transform="rotate({r} {x+50} {y+50})">'); tile(I, x, y, 100, ch, c, INK, 64, 18); I.add('</g>')
    I.add(f'<path d="M380 400 C440 380 450 330 430 300" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M412 300 L432 280 L448 308Z" fill="#fff"/>')

@icon('catquiz-sopa-de-lletres')
def _(I):
    cq_bg(I, '#9cd8ff', '#4a7dff')
    I.add(f'<rect x="56" y="56" width="400" height="400" rx="30" {st("#fff")}/>')
    grid = ['MARXE', 'AQPLU', 'RSOLT', 'ENUVA', 'FIDGH']
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            I.add(f'<text x="{116+c*70}" y="{136+r*72}" text-anchor="middle" font-size="44" {FONT} fill="{INK}" opacity=".85">{ch}</text>')
    I.add(f'<rect x="84" y="88" width="320" height="64" rx="32" fill="none" stroke="#ff4fa3" stroke-width="10"/><rect x="226" y="160" width="64" height="210" rx="32" fill="none" stroke="#38c46a" stroke-width="10"/>')

@icon('catquiz-lletres-perdudes')
def _(I):
    cq_bg(I, '#ffd23f', '#ff8a1f')
    for i, ch in enumerate(['G', '?', 'T', '?']):
        tile(I, 36 + i * 112, 190, 104, ch, '#fff' if ch != '?' else '#b98cff', INK if ch != '?' else '#fff', 68, 18)
    I.add(f'<g transform="translate(390 400) rotate(-30)"><rect x="-90" y="-22" width="160" height="44" rx="8" {st("#ffd23f", 7)}/><path d="M70 -22 L110 0 L70 22Z" {st("#ffc4a0", 7)}/><rect x="-110" y="-22" width="30" height="44" rx="8" {st("#ff7ab0", 7)}/></g>')
    sparkle(I, 90, 100, 18)

@icon('catquiz-roda-de-paraules')
def _(I):
    cq_bg(I, '#7af0b0', '#1b9a6a')
    for i, ch in enumerate('ROSA'): tile(I, 70 + i * 76, 40, 70, ch, '#4ee06a', '#fff', 44, 14)
    for j, ch in enumerate('OCA'): tile(I, 70, 116 + j * 76, 70, ch if j else '', '#4ee06a' if j else '#fff', '#fff', 44, 14)
    I.add(f'<circle cx="320" cy="330" r="150" {st("#fff")}/><circle cx="320" cy="330" r="118" fill="none" stroke="#d9dcef" stroke-width="6"/>')
    pos = [(320, 222), (420, 300), (382, 420), (258, 420), (220, 300)]
    I.add(f'<polyline points="320,222 420,300 382,420" fill="none" stroke="#38e5ff" stroke-width="26" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')
    for (x, y), ch in zip(pos, 'RSOAC'):
        sel = ch in 'RSO'
        I.add(f'<circle cx="{x}" cy="{y}" r="38" {st("#38e5ff" if sel else "#fff", 7)}/><text x="{x}" y="{y+17}" text-anchor="middle" font-size="46" {FONT} fill="{"#fff" if sel else INK}">{ch}</text>')
    sparkle(I, 460, 70, 18)

@icon('catquiz-pronoms-febles')
def _(I):
    cq_bg(I, '#38e5ff', '#2a6ad6')
    I.add(f'<path d="M70 90 H442 Q472 90 472 120 V280 Q472 310 442 310 H230 L160 380 L176 310 H70 Q40 310 40 280 V120 Q40 90 70 90Z" {st("#fff")}/>')
    I.add(f'<text x="256" y="175" text-anchor="middle" font-size="46" {FONT} fill="{INK}">EL LLIBRE,</text>')
    I.add(f'<rect x="96" y="205" width="120" height="66" rx="16" {st("#ff4fa3", 7)}/><text x="156" y="252" text-anchor="middle" font-size="44" {FONT} fill="#fff">L\'</text>')
    I.add(f'<text x="330" y="252" text-anchor="middle" font-size="40" {FONT} fill="{INK}">HE LLEGIT</text>')
    for i, (w, c) in enumerate((('HI', '#ffd23f'), ('EN', '#7af0b0'), ('HO', '#b98cff'))):
        x = 226 + i * 104; I.add(f'<rect x="{x-48}" y="388" width="96" height="70" rx="35" {st(c, 7)}/><text x="{x}" y="436" text-anchor="middle" font-size="40" {FONT} fill="{INK}">{w}</text>')
    sparkle(I, 470, 360, 16); sparkle(I, 50, 60, 14)

@icon('catquiz-quiz-d-esportistes')
def _(I):
    cq_bg(I, '#ffd23f', '#ff8a1f')
    I.add(f'<path d="M190 40 L256 190 L322 40 H284 L256 110 L228 40Z" {st("#3d8eff")}/><path d="M228 40 L256 110 L284 40Z" fill="#ff3355" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
    I.add(f'<circle cx="256" cy="290" r="120" {st(I.lg("#ffe27a", "#ffb11f"))}/><circle cx="256" cy="290" r="86" fill="none" stroke="#fff3b0" stroke-width="10"/>')
    I.add(f'<text x="256" y="335" text-anchor="middle" font-size="130" {FONT} fill="{INK}">1</text>'); shine(I, 210, 230, 34, 16, -30, .55)
    I.add(f'<circle cx="440" cy="300" r="42" {st("#ff8a1f", 7)}/><path d="M398 300 H482 M440 258 V342 M410 270 Q436 300 410 330 M470 270 Q444 300 470 330" stroke="{INK}" stroke-width="5" fill="none"/>')
    I.add(f'<circle cx="432" cy="438" r="36" {st("#d4e600", 7)}/><path d="M404 416 Q432 438 404 460 M460 416 Q432 438 460 460" stroke="#fff" stroke-width="6" fill="none"/>')
    sparkle(I, 80, 110, 20); sparkle(I, 440, 120, 16)

@icon('catquiz-quiz-de-castells')
def _(I):
    cq_bg(I, '#9cd8ff', '#4a7dff')
    I.add(f'<path d="M0 420 H512 V512 H0Z" fill="#e9c9a0"/>')
    def pers(x, y, e, c):
        I.add(f'<rect x="{x-14*e}" y="{y+18*e}" width="{28*e}" height="{30*e}" rx="{6*e}" fill="{c}" stroke="{INK}" stroke-width="5"/><rect x="{x-14*e}" y="{y+36*e}" width="{28*e}" height="{7*e}" fill="{INK}"/><circle cx="{x}" cy="{y+9*e}" r="{10*e}" fill="#f3c9a2" stroke="{INK}" stroke-width="5"/>')
    for i in range(9): pers(120 + i * 34, 410, .95, '#e0533a')
    for f in range(4):
        n = 3; y = 362 - f * 50
        for i in range(n): pers(222 + i * 34, y, 1, '#d7263d')
    pers(239, 162, .85, '#d7263d'); pers(273, 162, .85, '#d7263d'); pers(256, 120, .8, '#d7263d'); pers(256, 80, .75, '#d7263d')
    I.add(f'<path d="M268 92 L298 52" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M268 92 L298 52" stroke="#d7263d" stroke-width="6" stroke-linecap="round"/>')
    sparkle(I, 430, 90, 20); sparkle(I, 90, 140, 14)

# ===================== v2: personajes y escenas más ilustrativas =====================
@icon('aura-battle')
def _(I):
    bg(I, '#ffd23f', '#ff4fa3', '#ffffff', .22)
    for r, o, c in ((205, .3, '#b98cff'), (165, .45, '#ff7ad9'), (128, .55, '#fff3a0')): I.add(f'<ellipse cx="256" cy="300" rx="{r}" ry="{r*1.05:.0f}" fill="{c}" opacity="{o}"/>')
    for a in range(0, 360, 30):
        x = 256 + 175 * math.cos(math.radians(a)); y = 300 + 185 * math.sin(math.radians(a))
        I.add(f'<path d="M{x:.0f} {y:.0f} q8 -30 0 -60 q-8 30 0 60Z" fill="#b98cff" opacity=".7" transform="rotate({a+90} {x:.0f} {y:.0f})"/>')
    I.add(f'<path d="M190 200 L120 120" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M190 200 L120 120" stroke="#6ad0ff" stroke-width="18" stroke-linecap="round"/>'
          f'<path d="M322 230 L400 260" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M322 230 L400 260" stroke="#6ad0ff" stroke-width="18" stroke-linecap="round"/>'
          f'<circle cx="115" cy="114" r="20" {st("#fff", 7)}/><circle cx="404" cy="262" r="20" {st("#fff", 7)}/>'
          f'<path d="M220 410 L200 470 H245 L250 420Z M292 410 L312 470 H267 L262 420Z" {st("#2b2440", 7)}/>'
          f'<path d="M256 150 C330 150 345 230 340 320 C336 400 300 430 256 430 C212 430 176 400 172 320 C167 230 182 150 256 150Z" {st(I.lg("#7ae0ff", "#3a7aff"))}/>'
          f'<path d="M190 330 Q256 360 322 330 L330 380 Q256 410 182 380Z" fill="#ffd23f" stroke="{INK}" stroke-width="6"/>'
          f'<path d="M200 170 Q256 120 312 170 Q300 140 256 132 Q212 140 200 170Z" {st("#ff4fa3", 7)}/>')
    eyes(I, 256, 235, 1.1, 30, 1); smile(I, 256, 280, 1.2, True); blush(I, 256, 270, 1, 52)
    shine(I, 215, 200, 16, 34, -20, .45)
    for x, y, r in ((90, 90, 22), (430, 110, 20), (430, 400, 18), (80, 400, 16)): sparkle(I, x, y, r)

@icon('tiro-limpio')
def _(I):
    bg(I, '#ffb38a', '#ff6a5a', '#fff3c4', .2)
    I.add(f'<circle cx="390" cy="150" r="70" fill="#fff3c4" opacity=".9"/>')
    for x, h, c in ((-10, 230, '#a05a8a'), (90, 300, '#c06a8a'), (200, 190, '#a05a8a'), (300, 260, '#c06a8a'), (410, 220, '#a05a8a')):
        I.add(f'<rect x="{x}" y="{512-h}" width="104" height="{h}" fill="{c}"/>' + ''.join(f'<rect x="{x+16+(i%3)*28}" y="{530-h+(i//3)*36}" width="16" height="20" fill="#ffd36b" opacity=".75"/>' for i in range(min(9, h // 36 * 3))))
    I.add(f'<rect x="-10" y="400" width="532" height="130" fill="#5a3a6a"/><rect x="-10" y="392" width="532" height="18" fill="#7a5a8a"/>')
    I.add(f'<path d="M140 360 L440 300" stroke="{INK}" stroke-width="30" stroke-linecap="round" filter="url(#ds)"/><path d="M140 360 L440 300" stroke="#4a4f6a" stroke-width="16" stroke-linecap="round"/>'
          f'<rect x="250" y="300" width="110" height="34" rx="14" {st("#2b2440", 7)} transform="rotate(-11 305 317)"/><circle cx="356" cy="302" r="18" fill="#9cf2ff" stroke="{INK}" stroke-width="6"/><circle cx="352" cy="298" r="5" fill="#fff"/>'
          f'<path d="M60 410 C60 330 120 300 180 310 L250 330 L240 380 L150 410Z" {st(I.lg("#3fbf8a", "#1f7a5a"))}/>')
    I.add(f'<circle cx="215" cy="300" r="56" {st(I.rg("#ffe0c2", "#f2b48a", .4, .35, .9))}/>'
          f'<path d="M160 296 C160 240 270 230 272 290 Z" {st("#ff3b5a", 7)}/><circle cx="270" cy="270" r="10" fill="#fff" stroke="{INK}" stroke-width="4"/>')
    I.add(f'<ellipse cx="236" cy="312" rx="9" ry="12" fill="{INK}"/><path d="M200 300 q-10 -6 -20 0" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M220 334 q10 6 20 -2" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    sparkle(I, 450, 290, 26); sparkle(I, 90, 100, 16)

@icon('anguera-superstars')
def _(I):
    bg(I, '#2bd46a', '#0d6b33', '#ffffff', .14)
    I.add(f'<path d="M-10 380 H522" stroke="#fff" stroke-width="8" opacity=".55"/><circle cx="256" cy="380" r="120" fill="none" stroke="#fff" stroke-width="8" opacity=".55"/>')
    I.add(f'<path d="M230 330 L180 420 L140 410" fill="none" stroke="{INK}" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/><path d="M230 330 L180 420 L140 410" fill="none" stroke="#f2b48a" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M270 330 L330 380 L380 360" fill="none" stroke="{INK}" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/><path d="M270 330 L330 380 L380 360" fill="none" stroke="#f2b48a" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M118 398 L150 396 L152 426 L112 428Z M372 346 L404 342 L410 372 L374 376Z" {st("#ff5a3c", 7)}/>'
          f'<rect x="210" y="300" width="84" height="50" rx="14" {st("#1d3a8a", 7)}/>'
          f'<path d="M206 214 L150 270 L170 290 L216 250Z M300 214 L360 180 L372 204 L306 250Z" {st("#ffd23f", 7)}/>'
          f'<path d="M206 200 L300 200 L310 310 L196 310Z" {st(I.lg("#ffd23f", "#ff9a1f"))}/><text x="253" y="285" text-anchor="middle" font-size="54" {FONT} fill="{INK}">7</text>')
    I.add(f'<circle cx="253" cy="152" r="54" {st(I.rg("#ffe0c2", "#f2b48a", .4, .35, .9))}/><path d="M200 146 C196 96 310 96 306 146 C290 120 220 120 200 146Z" {st("#5a3a1f", 7)}/>')
    eyes(I, 253, 156, .8, 22, 1); smile(I, 256, 180, .9, True)
    I.add(f'<circle cx="420" cy="320" r="44" {st("#fff")}/><path d="M420 296 L444 313 L435 341 L405 341 L396 313Z" fill="{INK}"/>')
    for i in range(3): I.add(f'<path d="M{440+i*10} {250+i*20} l26 -14" stroke="#fff" stroke-width="8" stroke-linecap="round"/>')
    sparkle(I, 80, 90, 18); sparkle(I, 440, 120, 14)

@icon('martin-leyenda-del-rock')
def _(I):
    bg(I, '#ff5a3c', '#5a0f2a', '#ffd23f', .16)
    for x, c in ((110, '#ffd23f'), (256, '#ffffff'), (402, '#38e5ff')): I.add(f'<path d="M{x} -20 L{x-80} 520 H{x+80}Z" fill="{c}" opacity=".12"/>')
    I.add(f'<path d="M150 512 C150 400 190 360 256 360 C322 360 362 400 362 512Z" {st(I.lg("#2b2440", "#120a24"))}/>'
          f'<path d="M226 362 L256 420 L286 362" fill="none" stroke="#ff4fa3" stroke-width="10"/>')
    I.add(f'<circle cx="256" cy="250" r="92" {st(I.rg("#ffe0c2", "#e8a37a", .4, .35, .9))}/>'
          f'<path d="M168 230 C160 140 352 140 344 230 C330 190 300 176 256 178 C212 176 182 190 168 230Z" {st("#e8e8f0", 7)}/>'
          f'<path d="M180 270 C190 380 322 380 332 270 C310 300 280 296 256 296 C232 296 202 300 180 270Z" {st("#f4f4fa", 7)}/>'
          f'<path d="M226 300 Q256 286 286 300" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    I.add(f'<path d="M188 232 H324 L318 262 Q300 276 276 262 L268 244 H244 L236 262 Q212 276 194 262Z" fill="#141018" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="M200 240 L222 240" stroke="#fff" stroke-width="5" opacity=".6"/>')
    I.add(f'<path d="M252 324 Q256 352 260 324" fill="#7a1530" stroke="{INK}" stroke-width="4"/>')
    I.add('<g transform="translate(400 440) rotate(25) scale(.85)">'
          f'<rect x="-11" y="-230" width="22" height="170" rx="5" {st("#6b3d1f", 7)}/><path d="M-22 -258 H22 L18 -228 H-18Z" {st("#2b2440", 7)}/>'
          f'<path d="M0 -70 C45 -86 80 -52 60 -18 C92 8 80 76 26 84 C10 108 -10 108 -26 84 C-80 76 -92 8 -60 -18 C-80 -52 -45 -86 0 -70Z" {st(I.lg("#ffd23f", "#ff8a1f"))}/>'
          f'<circle cx="0" cy="0" r="16" fill="#2b1a0f"/></g>')
    I.add(f'<path d="{star5(90, 110, 40)}" {st("#ffd23f", 7)}/>'); note(I, 430, 130, .8, '#fff')

@icon('catquiz-l-intrus')
def _(I):
    cq_bg(I, '#b98cff', '#5a3ad6')
    for (x, y) in ((140, 150), (372, 150), (140, 360)):
        I.add(f'<path d="M{x} {y-60} C{x+90} {y-90} {x+100} {y+40} {x+40} {y+76} C{x+20} {y+86} {x-20} {y+86} {x-40} {y+76} C{x-100} {y+40} {x-90} {y-90} {x} {y-60}Z" {st(I.rg("#ff8a8a", "#d42a3a", .35, .3, .9))}/>'
              f'<path d="M{x} {y-60} Q{x+6} {y-90} {x+24} {y-100}" stroke="#7a4a2a" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M{x+10} {y-82} Q{x+50} {y-110} {x+60} {y-80} Q{x+30} {y-70} {x+10} {y-82}Z" {st("#5ac65a", 6)}/>')
        shine(I, x - 30, y - 20, 14, 26, -10, .45)
    I.add(f'<g transform="rotate(10 372 362)"><path d="M290 362 C320 320 410 320 440 362 C410 404 320 404 290 362Z" {st(I.lg("#7ae0ff", "#2a8fd6"))}/><path d="M432 362 L476 330 L470 362 L476 394Z" {st("#2a8fd6", 7)}/><circle cx="320" cy="354" r="9" fill="{INK}"/></g>')
    I.add(f'<circle cx="440" cy="270" r="30" {st("#ffd23f", 7)}/><text x="440" y="284" text-anchor="middle" font-size="40" {FONT} fill="{INK}">!</text>')

@icon('relax-constelaciones')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#020411", "#1a2b5a")}"/>'); stars_bg(I, 60, 71)
    I.add(f'<circle cx="420" cy="90" r="40" fill="#fff6d0"/><circle cx="440" cy="78" r="36" fill="#0a1230"/>')
    pts = [(80, 120), (170, 90), (240, 150), (320, 110), (400, 190), (350, 280), (250, 260), (150, 240)]
    I.add('<path d="M' + ' L'.join(f'{x} {y}' for x, y in pts) + f' L240 150" fill="none" stroke="#bfd6ff" stroke-width="5" opacity=".85"/>')
    for x, y in pts: I.add(f'<circle cx="{x}" cy="{y}" r="18" fill="#bfd6ff" opacity=".25"/>'); sparkle(I, x, y, 16)
    I.add(f'<path d="M-10 420 Q200 340 522 400 V522 H-10Z" fill="#14234a"/>')
    I.add(f'<path d="M300 410 L280 470 M300 410 L320 470 M300 410 L300 470" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
          f'<rect x="230" y="350" width="150" height="40" rx="14" {st(I.lg("#ffd23f", "#ff9a1f"))} transform="rotate(-30 300 370)"/><rect x="350" y="300" width="30" height="54" rx="8" {st("#ff4fa3", 7)} transform="rotate(-30 365 327)"/>')

@icon('relax-jardin-zen')
def _(I):
    I.add(f'<rect width="512" height="512" fill="{I.lg("#f4e8cc", "#d5bf92")}"/>')
    for k in range(-6, 14): I.add(f'<path d="M-10 {k*44} C150 {k*44-30} 360 {k*44+30} 522 {k*44}" fill="none" stroke="#c4a873" stroke-width="5"/>')
    for (x, y, r) in ((190, 300, 70), (380, 400, 50)):
        for rr in (r + 26, r + 50, r + 74): I.add(f'<ellipse cx="{x}" cy="{y}" rx="{rr}" ry="{rr*.7:.0f}" fill="none" stroke="#c4a873" stroke-width="5"/>')
        I.add(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.75:.0f}" {st(I.lg("#a8a8b8", "#5a5a6a"))}/>'); shine(I, x - r * .3, y - r * .3, r * .3, r * .15, -20, .5)
    I.add(f'<path d="M522 40 C420 60 360 120 300 110 M420 70 C400 120 380 150 340 170" fill="none" stroke="{INK}" stroke-width="16" stroke-linecap="round"/><path d="M522 40 C420 60 360 120 300 110 M420 70 C400 120 380 150 340 170" fill="none" stroke="#6b3d1f" stroke-width="8" stroke-linecap="round"/>')
    for (x, y) in ((300, 110), (340, 170), (380, 92), (450, 60), (410, 130), (360, 130)):
        I.add(''.join(f'<circle cx="{x+12*math.cos(a):.0f}" cy="{y+12*math.sin(a):.0f}" r="11" fill="#ffc4d8" stroke="{INK}" stroke-width="3"/>' for a in [k * 1.257 for k in range(5)]) + f'<circle cx="{x}" cy="{y}" r="6" fill="#ff7aa8"/>')
    for x, y in ((150, 160), (250, 200), (110, 230)): I.add(f'<ellipse cx="{x}" cy="{y}" rx="8" ry="5" fill="#ffc4d8" transform="rotate(30 {x} {y})"/>')

@icon('kings-league-mini-game')
def _(I):
    bg(I, '#2c2a5a', '#0c0b24', '#ffd23f', .16)
    for x in (60, 452): I.add(f'<path d="M{x} 0 L{x-60} 300 H{x+60}Z" fill="#fff" opacity=".1"/><circle cx="{x}" cy="20" r="26" fill="#fff6c2"/>')
    ground(I, 410, '#2fbf5c', '#16803a')
    I.add(f'<circle cx="256" cy="330" r="110" {st("#fff")}/>')
    for a in range(5):
        cx = 256 + 72 * math.cos(math.radians(a * 72 - 90)); cy = 330 + 72 * math.sin(math.radians(a * 72 - 90))
        I.add(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="20" fill="{INK}" opacity=".85"/>')
    I.add(f'<path d="M256 300 L284 320 L274 352 L238 352 L228 320Z" fill="{INK}"/>')
    shine(I, 215, 280, 26, 14, -30, .7)
    I.add(f'<g transform="rotate(-8 256 210)"><path d="M166 230 L180 130 L222 178 L256 104 L290 178 L332 130 L346 230Z" {st(I.lg("#ffe680", "#ffb11f"))}/>'
          f'<rect x="160" y="222" width="192" height="34" rx="10" {st("#ffb11f")}/></g>')
    for x, c in ((200, '#38e5ff'), (256, '#ff4fa3'), (312, '#38e5ff')): I.add(f'<circle cx="{x}" cy="{236 - (x-256)*.14:.0f}" r="10" fill="{c}" stroke="{INK}" stroke-width="4"/>')
    sparkle(I, 90, 160, 18, '#ffd23f'); sparkle(I, 430, 170, 16, '#ffd23f')

@icon('olimpiadas-de-la-granja')
def _(I):
    bg(I, '#7fd6ff', '#3a9fe0', '#ffffff', .2)
    ground(I, 380, '#7ed957', '#3b9a2c')
    I.add(f'<path d="M-10 430 C150 400 360 400 522 430" stroke="#fff" stroke-width="8" fill="none" opacity=".7"/><path d="M-10 470 C150 440 360 440 522 470" stroke="#fff" stroke-width="8" fill="none" opacity=".7"/>')
    # podio
    for x, h, n, c in ((110, 70, 2, '#d9dcef'), (256, 110, 1, '#ffd23f'), (402, 50, 3, '#ff9a5a')):
        I.add(f'<rect x="{x-70}" y="{470-h}" width="140" height="{h+60}" rx="8" {st(c)}/><text x="{x}" y="{470-h+48}" text-anchor="middle" font-size="40" {FONT} fill="{INK}">{n}</text>')
    # cerdito campeón
    I.add(f'<ellipse cx="256" cy="250" rx="96" ry="84" {st(I.rg("#ffd0dc", "#ff8fb0", .4, .35, .8))}/>'
          f'<path d="M180 190 L172 140 L218 172Z M332 190 L340 140 L294 172Z" {st("#ff8fb0", 8)}/>'
          f'<ellipse cx="256" cy="272" rx="38" ry="28" {st("#ff9fbd", 7)}/><ellipse cx="243" cy="272" rx="7" ry="10" fill="{INK}"/><ellipse cx="269" cy="272" rx="7" ry="10" fill="{INK}"/>')
    eyes(I, 256, 222, .9, 34); blush(I, 256, 262, 1, 62)
    I.add(f'<path d="M226 320 L256 352 L286 320" fill="none" stroke="#ff4fa3" stroke-width="14" stroke-linejoin="round"/><circle cx="256" cy="362" r="26" {st(I.lg("#ffe680", "#ffb11f"), 7)}/><path d="{star5(256, 364, 14)}" fill="#fff6c2"/>')
    I.add(f'<path d="M150 200 L110 150" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M150 200 L110 150" stroke="#ffb3c8" stroke-width="12" stroke-linecap="round"/><path d="M362 200 L402 150" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M362 200 L402 150" stroke="#ffb3c8" stroke-width="12" stroke-linecap="round"/>')
    for x, y, c in ((90, 90, '#ff4fa3'), (420, 80, '#ffd23f'), (380, 130, '#38e5ff'), (140, 120, '#7af0b0')): I.add(f'<rect x="{x}" y="{y}" width="18" height="10" fill="{c}" transform="rotate(30 {x} {y})"/>')

@icon('cube-runner')
def _(I):
    bg(I, '#9a6bff', '#3a1a9a', '#ff9ad5', .15)
    I.add(f'<path d="M256 170 L-80 522 H592Z" fill="{I.lg("#7af0b0", "#2bb36a")}"/><path d="M256 170 L110 522 M256 170 L402 522" stroke="#ff4fa3" stroke-width="10"/>'
          + ''.join(f'<line x1="-10" y1="{y}" x2="522" y2="{y}" stroke="#fff" stroke-width="3" opacity=".25"/>' for y in (240, 300, 380, 470)))
    for x, y, s in ((180, 230, 44), (310, 210, 34), (350, 300, 66)):
        I.add(f'<path d="M{x-s/2} {y-s/2} l{s*.3:.0f} {-s*.3:.0f} h{s} l{-s*.3:.0f} {s*.3:.0f}Z" {st("#ff8fb0", 5)}/><rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" {st("#ff5f8f", 6)}/>')
    I.add(f'<path d="M200 320 l30 -26 h110 l-30 26Z" {st("#ffe680", 7)}/><path d="M310 320 l30 -26 v110 l-30 26Z" {st("#e09a1f", 7)}/><rect x="200" y="320" width="110" height="110" {st(I.lg("#ffe680", "#ffb11f"))}/>')
    eyes(I, 255, 365, .9, 24, 1); smile(I, 255, 398, .9, True)
    for i in range(3): I.add(f'<line x1="{180-i*30}" y1="{345+i*26}" x2="{110-i*30}" y2="{345+i*26}" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity=".85"/>')
    sparkle(I, 430, 100, 18)


@icon('ola-perfecta')
def _(I):
    bg(I, '#ffc46b', '#ff7a6b', '#fff3c4', .16)
    I.add(f'<circle cx="370" cy="150" r="70" fill="#fff1b8" opacity=".95"/><circle cx="370" cy="150" r="96" fill="#fff1b8" opacity=".25"/>')
    for x, y in ((90, 110), (130, 92)): I.add(f'<path d="M{x-16} {y} q16 -14 32 0 q16 -14 32 0" fill="none" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    # mar de fondo
    I.add(f'<path d="M-10 330 C120 310 260 318 522 300 V522 H-10Z" fill="{I.lg("#2fc4c9", "#0f6f8f")}"/>')
    # la ola que rompe (tubo)
    I.add(f'<path d="M-10 522 V240 C30 120 170 60 270 96 C340 120 360 190 320 226 C292 250 250 238 252 206 C254 184 280 178 292 196 C280 150 220 140 170 176 C110 220 90 330 140 522Z" {st(I.lg("#7af0e0", "#0f7fa0", 0, 0, .3, 1), 9)}/>')
    I.add(f'<path d="M140 522 C90 330 110 220 170 176 C220 140 280 150 292 196" fill="none" stroke="#0b4f6e" stroke-width="10" opacity=".35"/>')
    # espuma del labio
    I.add(f'<path d="M30 160 C80 100 190 60 270 96 C340 120 360 190 320 226" fill="none" stroke="#fff" stroke-width="22" stroke-linecap="round"/>')
    for x, y, r in ((322, 228, 13), (338, 206, 9), (300, 240, 8), (346, 246, 6), (316, 258, 5)): I.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/>')
    for d in ('M40 300 C60 270 70 240 90 220', 'M70 380 C80 340 96 300 116 270'): I.add(f'<path d="{d}" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".55"/>')
    # estela
    I.add(f'<path d="M232 440 C300 450 380 430 470 380" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".8"/>')
    # tabla
    I.add(f'<g transform="rotate(-18 300 410)"><ellipse cx="300" cy="410" rx="120" ry="24" {st(I.lg("#fff6e0", "#ffd38a"), 8)}/><path d="M190 410 H410" stroke="#ff6f4f" stroke-width="9"/></g>')
    # surfista
    I.add(f'<path d="M262 410 L282 340 M336 392 L318 336" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><path d="M262 410 L282 340 M336 392 L318 336" stroke="#e8a77a" stroke-width="14" stroke-linecap="round"/>')
    I.add(f'<path d="M270 350 Q300 330 330 346 L326 300 Q300 290 276 302Z" {st("#1fb6a6", 7)}/>')
    I.add(f'<path d="M282 300 L268 230 Q300 214 330 228 L320 300Z" {st("#ff6f4f", 7)}/>')
    I.add(f'<path d="M276 246 L208 286 M326 240 L392 214" stroke="{INK}" stroke-width="24" stroke-linecap="round"/><path d="M276 246 L208 286 M326 240 L392 214" stroke="#e8a77a" stroke-width="12" stroke-linecap="round"/>')
    I.add(f'<circle cx="300" cy="184" r="42" {st(I.rg("#ffd0aa", "#e8a77a", .4, .35, .8), 8)}/><path d="M258 176 C262 136 340 128 344 172 C330 158 300 150 270 168Z" {st("#5a3a26", 6)}/>')
    eyes(I, 302, 188, .7, 26, 1); smile(I, 302, 206, .7, True)
    sparkle(I, 452, 300, 16); sparkle(I, 200, 70, 12)


def skier(I, x, y, rot=0, s=1, pose='fly'):
    """Esquiador cartoon: casco, gafas, mono naranja y esquís azules."""
    g = f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
    if pose == 'fly':   # estilo V, cuerpo inclinado sobre los esquís
        g += (f'<path d="M-120 34 L150 -6" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-120 34 L150 -6" stroke="#14b8ff" stroke-width="11" stroke-linecap="round"/>'
              f'<path d="M-110 56 L150 40" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-110 56 L150 40" stroke="#14b8ff" stroke-width="11" stroke-linecap="round"/>'
              f'<path d="M-30 30 L-74 4" stroke="{INK}" stroke-width="30" stroke-linecap="round"/><path d="M-30 30 L-74 4" stroke="#1c2233" stroke-width="18" stroke-linecap="round"/>'
              f'<path d="M-78 2 C-40 -40 40 -46 70 -26 L62 4 C30 -8 -20 -2 -60 22Z" {st("#ff5a1f", 8)}/>'
              f'<path d="M10 -26 L-40 -8 M20 -14 L-34 10" stroke="#ffb08a" stroke-width="6" stroke-linecap="round" opacity=".7"/>'
              f'<path d="M-10 -24 L-70 -34" stroke="{INK}" stroke-width="20" stroke-linecap="round"/><path d="M-10 -24 L-70 -34" stroke="#ff5a1f" stroke-width="9" stroke-linecap="round"/>'
              f'<circle cx="92" cy="-36" r="34" {st(I.rg("#ffffff", "#d9dcef", .4, .35, .8), 8)}/>'
              f'<path d="M86 -40 h40 a10 10 0 0 1 0 20 h-40Z" {st("#1b2a4a", 6)}/><path d="M96 -36 h22" stroke="#7fd3ff" stroke-width="5" stroke-linecap="round"/>'
              f'<rect x="-18" y="-20" width="30" height="26" rx="4" fill="#fff" stroke="{INK}" stroke-width="5" transform="rotate(-14)"/><text x="-4" y="1" text-anchor="middle" font-size="20" {FONT} fill="{INK}" transform="rotate(-14)">7</text>')
    else:               # agrupado en voltereta
        g += (f'<path d="M-96 60 L96 60" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-96 60 L96 60" stroke="#14b8ff" stroke-width="11" stroke-linecap="round"/>'
              f'<path d="M-90 80 L100 80" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-90 80 L100 80" stroke="#14b8ff" stroke-width="11" stroke-linecap="round"/>'
              f'<path d="M-6 66 L-40 20 L10 -4" fill="none" stroke="{INK}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/><path d="M-6 66 L-40 20 L10 -4" fill="none" stroke="#1c2233" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>'
              f'<ellipse cx="18" cy="-16" rx="46" ry="40" {st("#ff5a1f", 8)}/>'
              f'<path d="M30 -26 L-30 10" stroke="{INK}" stroke-width="20" stroke-linecap="round"/><path d="M30 -26 L-30 10" stroke="#ff5a1f" stroke-width="9" stroke-linecap="round"/>'
              f'<circle cx="52" cy="-62" r="32" {st(I.rg("#ffffff", "#d9dcef", .4, .35, .8), 8)}/>'
              f'<path d="M50 -66 h36 a10 10 0 0 1 0 20 h-36Z" {st("#1b2a4a", 6)}/><path d="M58 -62 h20" stroke="#7fd3ff" stroke-width="5" stroke-linecap="round"/>')
    I.add(g + '</g>')

def alpine(I):
    """Fondo de cartel alpino: cielo al atardecer, sol marfil con franjas y montañas nevadas."""
    bg(I, '#ffb38a', '#2b4c8f', '#fff3c4', .12)
    I.add(f'<circle cx="256" cy="230" r="150" fill="none" stroke="#c9ab62" stroke-width="4" opacity=".8"/>'
          f'<clipPath id="sunc"><circle cx="256" cy="230" r="132"/></clipPath><circle cx="256" cy="230" r="132" fill="#f7f2e4"/>'
          '<g clip-path="url(#sunc)" fill="#f2c9a4">' + ''.join(f'<rect x="100" y="{270+i*18}" width="320" height="{5+i*2}"/>' for i in range(5)) + '</g>')
    I.add(f'<path d="M-10 522 V360 L70 290 L130 340 L220 250 L300 340 L380 280 L522 380 V522Z" fill="#15496a" stroke="{INK}" stroke-width="7"/>'
          f'<path d="M206 266 L220 250 L236 268 L226 262 L220 274 L212 262Z M58 300 L70 290 L84 304 L76 300 L70 310 L64 300Z M368 290 L380 280 L394 294 L386 290 L380 300 L374 290Z" fill="#f7f2e4"/>'
          f'<path d="M-10 522 V420 L90 370 L180 420 L290 360 L400 420 L522 380 V522Z" fill="#13795b" stroke="{INK}" stroke-width="7"/>')

@icon('el-gran-salto')
def _(I):
    alpine(I)
    # trampolín
    I.add(f'<path d="M-10 250 L120 330 L150 336" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-10 250 L120 330 L150 336" fill="none" stroke="#cfe6ff" stroke-width="12" stroke-linecap="round"/>'
          f'<path d="M20 268 V522 M90 312 V522" stroke="{INK}" stroke-width="10"/>')
    # pista de aterrizaje y marcas
    I.add(f'<path d="M140 522 C260 470 400 440 522 430 V522Z" fill="#f7f2e4" stroke="{INK}" stroke-width="7"/>'
          f'<path d="M330 452 L338 500" stroke="#d8201f" stroke-width="9" stroke-linecap="round"/><path d="M420 440 L426 486" stroke="#2d6bff" stroke-width="7" stroke-linecap="round"/>')
    for i, (x, y) in enumerate(((176, 196), (150, 214), (128, 230))): I.add(f'<path d="M{x} {y} l-46 26" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity="{.9 - i*.25}"/>')
    skier(I, 300, 200, -14, .95, 'fly')
    sparkle(I, 440, 110, 16); sparkle(I, 90, 120, 12)
    for x, y in ((60, 70), (150, 50), (420, 190), (470, 60), (240, 80)): I.add(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" opacity=".85"/>')

@icon('la-gran-pirueta')
def _(I):
    alpine(I)
    I.add(f'<path d="M70 470 Q256 -60 450 470" fill="none" stroke="#fff" stroke-width="7" stroke-dasharray="2 18" stroke-linecap="round" opacity=".9"/>')
    # rotación: flechas curvas alrededor del esquiador
    I.add(f'<path d="M150 150 A120 120 0 0 1 380 160" fill="none" stroke="#ffd23f" stroke-width="12" stroke-linecap="round"/><path d="M380 160 l-30 -10 l20 30Z" fill="#ffd23f" stroke="{INK}" stroke-width="5"/>'
          f'<path d="M380 330 A120 120 0 0 1 150 320" fill="none" stroke="#ffd23f" stroke-width="12" stroke-linecap="round" opacity=".7"/>')
    skier(I, 262, 240, 150, .95, 'tuck')
    # trampolín de salida
    I.add(f'<path d="M-10 420 Q60 470 120 430" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-10 420 Q60 470 120 430" fill="none" stroke="#cfe6ff" stroke-width="12" stroke-linecap="round"/>')
    for x, y, c in ((90, 100, '#ff4fa3'), (430, 90, '#ffd23f'), (400, 380, '#38e5ff'), (120, 330, '#7af0b0')): I.add(f'<rect x="{x}" y="{y}" width="18" height="10" fill="{c}" transform="rotate(30 {x} {y})"/>')
    sparkle(I, 450, 250, 16); sparkle(I, 70, 220, 12)


@icon('el-gran-descenso')
def _(I):
    alpine(I)
    # canal de hielo en curva peraltada
    I.add(f'<path d="M-20 300 C120 280 200 330 260 390 C320 450 420 470 540 440 V560 H-20Z" fill="#cfe6ff" stroke="{INK}" stroke-width="8"/>'
          f'<path d="M-20 340 C110 322 190 372 250 432 C310 492 420 506 540 478" fill="none" stroke="#7cc8ff" stroke-width="10" opacity=".7"/>'
          f'<path d="M-20 300 C120 280 200 330 260 390 C320 450 420 470 540 440" fill="none" stroke="#13795b" stroke-width="10"/>')
    for x, y in ((150, 330), (225, 375), (300, 440)): I.add(f'<path d="M{x-14} {y+10} l14 -16 l14 16" fill="none" stroke="#e7c768" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')
    # trineo
    I.add('<g transform="translate(296 372) rotate(16)">'
          f'<path d="M-120 22 Q-124 -26 -60 -34 L70 -34 Q122 -30 130 6 Q118 34 76 34 L-80 34 Q-120 34 -120 22Z" {st(I.lg("#1d3d6b", "#0b2545"), 8)}/>'
          f'<path d="M-104 6 L118 6" stroke="#13795b" stroke-width="12" stroke-linecap="round"/>'
          f'<path d="M-112 46 H140" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M-112 46 H140" stroke="#c9d3df" stroke-width="5" stroke-linecap="round"/>'
          f'<circle cx="-30" cy="-50" r="26" {st(I.rg("#ffffff", "#e8e1cf", .4, .35, .8), 7)}/><path d="M-12 -56 h22 a8 8 0 0 1 0 16 h-22Z" {st("#1b2a4a", 5)}/>'
          f'<circle cx="34" cy="-48" r="26" {st(I.rg("#f3dc92", "#c9ab62", .4, .35, .8), 7)}/><path d="M52 -54 h22 a8 8 0 0 1 0 16 h-22Z" {st("#1b2a4a", 5)}/>'
          f'<ellipse cx="128" cy="2" rx="16" ry="18" fill="#f7f2e4" stroke="{INK}" stroke-width="6"/>'
          '</g>')
    for i in range(4): I.add(f'<line x1="{170-i*26}" y1="{318+i*20}" x2="{110-i*26}" y2="{300+i*20}" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity="{.9-i*.18}"/>')
    sparkle(I, 440, 110, 16); sparkle(I, 80, 150, 12)


@icon('alas-de-acero')
def _(I):
    bg(I, '#8fd0ff', '#2b6fd0', '#ffffff', .14)
    for x, y, r in ((110, 130, 60), (170, 110, 48), (400, 380, 70), (460, 360, 48), (80, 420, 50)): I.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".85"/>')
    # avión enemigo a lo lejos, humeando
    I.add('<g transform="translate(410 120) rotate(14) scale(.42)">'
          f'<ellipse cx="0" cy="0" rx="110" ry="26" {st("#7a8087", 10)}/><path d="M-20 0 L-60 -90 L-10 -90 L30 0Z M-20 0 L-60 90 L-10 90 L30 0Z" {st("#7a8087", 10)}/>'
          f'<path d="M-10 -12 v24 M-22 0 h24" stroke="{INK}" stroke-width="10"/></g>')
    for i in range(5): I.add(f'<circle cx="{450+i*16}" cy="{108-i*6}" r="{10+i*4}" fill="#5b5f66" opacity="{.5-i*.08}"/>')
    # trazadoras
    for dy in (-18, 18): I.add(f'<path d="M300 {250+dy} L392 {150+dy*.4}" stroke="#ffd23f" stroke-width="7" stroke-linecap="round" stroke-dasharray="20 18"/>')
    # caza aliado
    I.add('<g transform="translate(220 300) rotate(-22)">'
          f'<path d="M-40 -16 L-150 -40 Q-170 -30 -150 -10 L-40 10Z" {st("#55623f", 8)}/>'
          f'<path d="M-40 16 L-150 40 Q-170 30 -150 10 L-40 -10Z" {st("#55623f", 8)}/>'
          f'<ellipse cx="0" cy="0" rx="150" ry="36" {st(I.lg("#7a8a58", "#4a5636"), 9)}/>'
          f'<path d="M-180 -6 L-150 -50 L-120 -6Z" {st("#55623f", 8)}/>'
          f'<path d="M-20 -60 L60 -160 L120 -160 L70 -40Z" {st("#55623f", 9)}/>'
          f'<path d="M-20 60 L60 160 L120 160 L70 40Z" {st("#4a5636", 9)}/>'
          f'<circle cx="80" cy="-110" r="18" fill="#1f3f9a" stroke="#fff" stroke-width="6"/><circle cx="80" cy="-110" r="7" fill="#c81e1e"/>'
          f'<ellipse cx="20" cy="-24" rx="40" ry="18" fill="#9fd4ff" stroke="{INK}" stroke-width="7"/><path d="M8 -34 l24 0" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".8"/>'
          f'<ellipse cx="150" cy="0" rx="22" ry="34" fill="#d9b44a" stroke="{INK}" stroke-width="8"/>'
          f'<ellipse cx="172" cy="0" rx="10" ry="92" fill="#e8eef2" opacity=".55" stroke="{INK}" stroke-width="4"/>'
          '</g>')
    for i in range(3): I.add(f'<line x1="{70-i*10}" y1="{390+i*22}" x2="{10-i*10}" y2="{420+i*22}" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity="{.85-i*.2}"/>')
    sparkle(I, 330, 210, 16)

def kidfb(I, x, y, pose='stand', shirt='#a3e635', s=1):
    """niño futbolista: x,y = cadera"""
    L = {'stand': ('M-14 0 L-18 70', 'M14 0 L18 70'), 'kick': ('M-12 0 L-22 70', 'M12 0 Q50 30 80 20'),
         'squat': ('M-16 0 L-48 26 L-30 70', 'M16 0 L48 26 L30 70'), 'jump': ('M-14 0 L-40 50', 'M14 0 L34 30 L20 64'),
         'punch': ('M-14 0 L-40 34 L-46 70', 'M14 0 L34 36 L42 70'), 'tree': ('M-8 0 L-8 72', 'M10 0 L58 30 L2 42'),
         'quad': ('M-8 0 L-8 72', 'M10 0 L14 50 L44 22')}[pose]
    A = {'stand': ('M-26 -60 L-50 -20', 'M26 -60 L50 -20'), 'kick': ('M-26 -60 L-62 -40', 'M26 -60 L58 -86'),
         'squat': ('M-26 -60 L-6 -36', 'M26 -60 L6 -36'), 'jump': ('M-26 -60 L-60 -96', 'M26 -60 L58 -30'),
         'punch': ('M-26 -60 L-52 -80 L-48 -100', 'M26 -60 L70 -78 L112 -82'), 'tree': ('M-24 -64 L-30 -130 L-6 -160', 'M24 -64 L30 -130 L6 -160'),
         'quad': ('M-26 -60 L-86 -76', 'M26 -60 L46 -8 L44 18')}[pose]
    g = f'<g transform="translate({x} {y}) scale({s})">'
    for d in L: g += f'<path d="{d}" stroke="{INK}" stroke-width="26" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="{d}" stroke="#ffcf9e" stroke-width="14" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    g += f'<rect x="-30" y="-14" width="60" height="30" rx="10" fill="#1f2a44" stroke="{INK}" stroke-width="7"/>'
    for d in A: g += f'<path d="{d}" stroke="{INK}" stroke-width="22" fill="none" stroke-linecap="round"/><path d="{d}" stroke="#ffcf9e" stroke-width="11" fill="none" stroke-linecap="round"/>'
    g += f'<rect x="-32" y="-78" width="64" height="70" rx="20" fill="{shirt}" stroke="{INK}" stroke-width="8"/>'
    g += f'<circle cx="0" cy="-112" r="34" fill="#ffcf9e" stroke="{INK}" stroke-width="8"/><path d="M-34 -116 Q-30 -150 0 -150 Q32 -150 34 -116 Q20 -132 0 -130 Q-20 -132 -34 -116Z" fill="#6b3d1f" stroke="{INK}" stroke-width="6"/>'
    I.add(g + '</g>')
    eyes(I, x, y - 112 * s, .6 * s, 20 * s); smile(I, x, y - 96 * s, .5 * s, True)

def fball(I, x, y, r=34):
    I.add(f'<circle cx="{x}" cy="{y}" r="{r}" {st("#fff")}/><path d="M{x} {y-r*.45} L{x+r*.43} {y-r*.14} L{x+r*.27} {y+r*.36} L{x-r*.27} {y+r*.36} L{x-r*.43} {y-r*.14}Z" fill="{INK}"/>')

def cone(I, x, y, c='#ff8a1c'):
    I.add(f'<path d="M{x-22} {y} L{x} {y-52} L{x+22} {y}Z" fill="{c}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/><path d="M{x-12} {y-24} H{x+12}" stroke="#fff" stroke-width="7"/><rect x="{x-30}" y="{y-4}" width="60" height="10" rx="4" fill="{c}" stroke="{INK}" stroke-width="5"/>')

def pitch(I, c1='#2bd46a', c2='#0d6b33'):
    bg(I, c1, c2, '#ffffff', .12)
    I.add('<path d="M-10 410 H522" stroke="#fff" stroke-width="8" opacity=".55"/><ellipse cx="256" cy="410" rx="170" ry="40" fill="none" stroke="#fff" stroke-width="7" opacity=".5"/>')

@icon('fifa-11-kids')
def _(I):
    pitch(I, '#2bd46a', '#0d6b33')
    for x in (70, 440): cone(I, x, 470)
    # escudo de prevención
    I.add(f'<path d="M400 70 L460 92 V140 Q460 186 400 212 Q340 186 340 140 V92Z" fill="#a3e635" stroke="{INK}" stroke-width="8"/><path d="M372 140 L394 162 L432 118" stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    kidfb(I, 230, 330, 'jump', '#ff5a3c')
    I.add('<path d="M120 250 q30 -20 60 0 M110 290 q30 -20 60 0" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".8"/>')
    fball(I, 330, 440, 30); sparkle(I, 90, 110, 18)

@icon('tecnica-individual')
def _(I):
    pitch(I, '#4fd1ff', '#1b5fae')
    for x in (300, 380, 460): cone(I, x, 470, '#ffd23f')
    kidfb(I, 180, 330, 'kick', '#3c7bff')
    fball(I, 280, 360, 34)
    I.add('<path d="M300 300 Q340 270 360 300 M310 250 Q360 210 390 250" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".85"/>')
    sparkle(I, 420, 110, 20, '#ffe46b'); sparkle(I, 80, 120, 14)

@icon('plan-de-fuerza')
def _(I):
    pitch(I, '#ffb35c', '#c2410c')
    kidfb(I, 256, 330, 'squat', '#a3e635')
    fball(I, 256, 280, 30)
    I.add('<path d="M120 220 v-60 M100 180 l20 -20 l20 20 M392 220 v-60 M372 180 l20 -20 l20 20" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')
    sparkle(I, 90, 100, 18); sparkle(I, 430, 90, 14, '#fff6c0')

@icon('boxeo-kids')
def _(I):
    bg(I, '#ff4d63', '#7a0e22', '#ffd0d6', .14)
    I.add('<path d="M40 470 H472" stroke="#fff" stroke-width="8" opacity=".5"/><path d="M40 430 H472 M40 390 H472" stroke="#fff" stroke-width="5" opacity=".25"/>')
    kidfb(I, 210, 340, 'punch', '#e0293f')
    for gx, gy in ((162, 238), (322, 258)): I.add(f'<circle cx="{gx}" cy="{gy}" r="30" {st("#ffc400")}/><path d="M{gx-14} {gy+18} h28" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
    for i in range(3): I.add(f'<path d="M{372+i*18} {226+i*18} l40 -10" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity="{.9-i*.25}"/>')
    sparkle(I, 430, 110, 20, '#ffe46b'); sparkle(I, 90, 120, 14)

@icon('yoga-kids')
def _(I):
    bg(I, '#b9a2ff', '#3b2385', '#f0e8ff', .12)
    I.add('<rect x="96" y="420" width="320" height="30" rx="15" fill="#ff7a59" stroke="#1d1442" stroke-width="8"/>')
    kidfb(I, 256, 340, 'tree', '#a58bff')
    I.add(f'<circle cx="256" cy="104" r="16" {st("#ffd23f", 6)}/>')
    sparkle(I, 100, 130, 18); sparkle(I, 420, 150, 14, '#fff6c0'); sparkle(I, 410, 330, 10)

@icon('estiramientos-kids')
def _(I):
    bg(I, '#ffd27a', '#b8700c', '#fff3c8', .14)
    I.add('<path d="M-10 452 H522" stroke="#fff" stroke-width="8" opacity=".55"/>')
    kidfb(I, 256, 344, 'quad', '#f2b134')
    I.add('<path d="M330 330 q24 -20 0 -44 M352 340 q36 -32 0 -70" stroke="#8a4dff" stroke-width="8" fill="none" stroke-linecap="round"/>')
    sparkle(I, 100, 110, 18); sparkle(I, 420, 110, 14, '#fff6c0')

@icon('looping-loco')
def _(I):
    bg(I, '#c08cff', '#5a2ab8', '#ffd0f0', .14)
    # looping
    I.add(f'<circle cx="256" cy="230" r="150" fill="none" stroke="{INK}" stroke-width="58"/><circle cx="256" cy="230" r="150" fill="none" stroke="#3a3550" stroke-width="44"/>'
          f'<circle cx="256" cy="230" r="150" fill="none" stroke="#ff4fa3" stroke-width="6" stroke-dasharray="22 18"/>'
          f'<path d="M-10 420 H200 Q256 410 256 380" fill="none" stroke="{INK}" stroke-width="58"/><path d="M-10 420 H200 Q256 410 256 380" fill="none" stroke="#3a3550" stroke-width="44"/>'
          f'<path d="M256 380 Q256 410 312 420 H522" fill="none" stroke="{INK}" stroke-width="58"/><path d="M256 380 Q256 410 312 420 H522" fill="none" stroke="#3a3550" stroke-width="44"/>')
    I.add('<path d="M10 420 H502" stroke="#ffd23f" stroke-width="5" stroke-dasharray="20 16"/>')
    # moto boca abajo arriba del looping
    I.add('<g transform="translate(256 66) rotate(180) scale(1.25)">'
          f'<circle cx="-38" cy="-8" r="20" fill="#22252c" stroke="{INK}" stroke-width="6"/><circle cx="38" cy="-8" r="20" fill="#22252c" stroke="{INK}" stroke-width="6"/>'
          f'<circle cx="-38" cy="-8" r="9" fill="#e8e8f0"/><circle cx="38" cy="-8" r="9" fill="#e8e8f0"/>'
          f'<path d="M-40 -30 L-6 -46 H30 L44 -28 Z" fill="#ffd23f" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
          f'<rect x="-14" y="-82" width="28" height="38" rx="12" fill="#3cc3ff" stroke="{INK}" stroke-width="6"/><circle cx="0" cy="-96" r="18" fill="#ff5a3c" stroke="{INK}" stroke-width="6"/><rect x="-12" y="-100" width="24" height="9" rx="4" fill="#9fdcff"/>'
          '</g>')
    I.add('<path d="M330 84 q30 0 50 20 M340 60 q40 0 66 30" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".85"/>')
    sparkle(I, 96, 96, 18, '#ffe14d'); sparkle(I, 430, 300, 14)

@icon('stu-el-especialista')
def _(I):
    bg(I, '#7fd6ff', '#2f8fe0', '#ffffff', .16)
    ground(I, 420, '#7ed957', '#3b9a2c')
    # rampa
    I.add(f'<path d="M20 430 L190 430 L190 350 Z" fill="#ffb11f" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/><path d="M60 425 L170 365" stroke="#fff" stroke-width="8" stroke-dasharray="14 12"/>')
    # muro de cajas reventando
    for x, y, r in ((330, 330, -18), (395, 300, 22), (430, 370, -8), (360, 395, 12), (300, 260, 30), (450, 250, -26)):
        I.add(f'<g transform="translate({x} {y}) rotate({r})"><rect x="-26" y="-26" width="52" height="52" rx="4" fill="#d98b3a" stroke="{INK}" stroke-width="6"/><path d="M-22 -22 L22 22 M22 -22 L-22 22" stroke="#9c5a20" stroke-width="5"/></g>')
    I.add(f'<g transform="translate(395 300) rotate(22)"><rect x="-26" y="-26" width="52" height="52" rx="4" fill="#e8384f" stroke="{INK}" stroke-width="6"/><text x="0" y="8" text-anchor="middle" font-family="Arial Black,Arial" font-weight="900" font-size="20" fill="#fff">TNT</text></g>')
    I.add('<path d="M380 300 l-40 -60 l50 30 l10 -60 l25 55 l50 -30 l-30 55" fill="#ffe14d" stroke="#ff8a1c" stroke-width="6" stroke-linejoin="round" opacity=".9"/>')
    # Stu volando con los brazos abiertos
    I.add('<g transform="translate(220 170) rotate(-20)">'
          f'<path d="M-18 30 L-46 70 M18 30 L40 74" stroke="{INK}" stroke-width="24" stroke-linecap="round"/><path d="M-18 30 L-46 70 M18 30 L40 74" stroke="#2f6fe0" stroke-width="12" stroke-linecap="round"/>'
          f'<path d="M-28 -24 L-86 -40 M28 -24 L86 -44" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-28 -24 L-86 -40 M28 -24 L86 -44" stroke="#2f6fe0" stroke-width="11" stroke-linecap="round"/>'
          f'<circle cx="-90" cy="-41" r="14" fill="#fff" stroke="{INK}" stroke-width="6"/><circle cx="90" cy="-45" r="14" fill="#fff" stroke="{INK}" stroke-width="6"/>'
          f'<rect x="-32" y="-44" width="64" height="80" rx="22" fill="#2f6fe0" stroke="{INK}" stroke-width="8"/><path d="M-32 -6 H32" stroke="#ffd23f" stroke-width="8"/>'
          f'<circle cx="0" cy="-80" r="36" fill="#fff" stroke="{INK}" stroke-width="8"/><path d="M-36 -86 A36 36 0 0 1 36 -86 Z" fill="#e8384f" stroke="{INK}" stroke-width="7"/><rect x="-26" y="-82" width="52" height="16" rx="8" fill="#9fdcff" stroke="{INK}" stroke-width="5"/>'
          '</g>')
    I.add('<path d="M120 250 q30 -10 50 -40 M90 210 q30 -10 50 -40" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity=".85"/>')
    sparkle(I, 90, 90, 18, '#ffe14d'); sparkle(I, 420, 110, 14)

@icon('car-revamp')
def _(I):
    bg(I, '#2b3142', '#0b0d14', '#6fe3ff', .10)
    # elevador
    I.add(f'<rect x="60" y="372" width="392" height="22" rx="6" fill="#3a3f4c" stroke="{INK}" stroke-width="6"/>'
          + ''.join(f'<rect x="{x}" y="394" width="34" height="90" fill="#9aa3b2" stroke="{INK}" stroke-width="6"/>' for x in (150, 328)))
    # coche: mitad oxidada (izq) y mitad recién pintada (dcha)
    body = 'M70 352 Q70 300 120 292 L170 250 Q190 236 230 236 L310 236 Q345 236 370 262 L398 290 Q448 296 448 336 L448 352 Z'
    I.add(f'<defs><clipPath id="crL"><rect x="0" y="0" width="256" height="512"/></clipPath><clipPath id="crR"><rect x="256" y="0" width="256" height="512"/></clipPath></defs>')
    I.add(f'<path d="{body}" fill="#b5652c" clip-path="url(#crL)"/>'
          + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#7a3a18" clip-path="url(#crL)"/>' for x, y, r in ((110, 320, 14), (160, 300, 10), (200, 330, 16), (230, 270, 9), (140, 342, 8)))
          + f'<path d="{body}" fill="#e8212b" clip-path="url(#crR)"/><path d="M290 250 L340 250 Q356 252 368 268" stroke="#fff" stroke-width="7" fill="none" opacity=".6" stroke-linecap="round" clip-path="url(#crR)"/>'
          f'<path d="{body}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
          f'<path d="M188 256 L230 248 L240 290 L176 292 Z M262 248 L320 248 Q340 250 352 270 L360 290 L262 290 Z" fill="#9fdcff" stroke="{INK}" stroke-width="6"/>'
          f'<path d="M256 226 V362" stroke="#fff" stroke-width="5" stroke-dasharray="10 8" opacity=".8"/>')
    for x in (150, 362):
        I.add(f'<circle cx="{x}" cy="356" r="34" fill="#22252c" stroke="{INK}" stroke-width="7"/><circle cx="{x}" cy="356" r="14" fill="#c9ced8"/>')
    # cepillo y pistola de agua
    I.add(f'<g transform="translate(118 168) rotate(-24)"><rect x="-44" y="-16" width="88" height="34" rx="10" fill="#ffb11f" stroke="{INK}" stroke-width="6"/>'
          + ''.join(f'<path d="M{x} 18 v18" stroke="#f3ead6" stroke-width="6" stroke-linecap="round"/>' for x in range(-34, 40, 12)) + '</g>')
    I.add(f'<path d="M430 170 Q380 190 352 236" stroke="#9fe6ff" stroke-width="10" fill="none" stroke-linecap="round" opacity=".9"/>'
          f'<g transform="translate(440 160) rotate(20)"><rect x="-10" y="-20" width="50" height="30" rx="8" fill="#ffd23f" stroke="{INK}" stroke-width="6"/><rect x="20" y="6" width="16" height="36" rx="5" fill="#ffd23f" stroke="{INK}" stroke-width="6"/></g>')
    sparkle(I, 402, 222, 18, '#fff'); sparkle(I, 330, 196, 12, '#ffe46b'); sparkle(I, 438, 300, 10)

@icon('crucigiro')
def _(I):
    bg(I, '#fff3c4', '#ffb35c', '#ffffff', .2)
    I.add('<path d="M-10 522 V380 Q120 300 256 360 Q390 300 522 370 V522Z" fill="#3b9a4a"/><path d="M-10 522 V420 Q140 360 300 410 Q420 380 522 420 V522Z" fill="#2c7a3a"/>')
    # crucigrama
    cells = [(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2), (1, 3), (3, 0), (3, 2)]
    letters = {(0, 1): 'L', (1, 1): 'A', (2, 1): 'G', (3, 1): 'O', (1, 0): 'C', (1, 2): 'S', (1, 3): 'A'}
    for (c, r) in cells:
        x, y = 150 + c * 54, 52 + r * 54
        ch = letters.get((c, r), '')
        tile(I, x, y, 50, ch, '#3cc3ff' if ch else '#ffffff', '#fff', 30, 10)
    # rueda
    I.add(f'<circle cx="256" cy="380" r="112" fill="#fff8ec" stroke="{INK}" stroke-width="8"/>')
    pts = {'L': (256, 300), 'A': (336, 380), 'G': (256, 460), 'O': (176, 380)}
    I.add('<path d="M256 300 L336 380 L256 460" fill="none" stroke="#4fc35a" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>')
    for ch, (x, y) in pts.items():
        on = ch in 'LAG'
        I.add(f'<circle cx="{x}" cy="{y}" r="32" fill="{"#4fc35a" if on else "#fff8ec"}" stroke="{INK}" stroke-width="6"/>'
              f'<text x="{x}" y="{y+13}" text-anchor="middle" font-size="38" {FONT} fill="{"#fff" if on else INK}">{ch}</text>')
    sparkle(I, 440, 120, 18, '#fff'); sparkle(I, 70, 150, 14, '#ffd23f')

@icon('lluvia-loca')
def _(I):
    bg(I, '#6a4bff', '#1b0f4a', '#35f0ff', .10)
    # niño con los brazos arriba
    I.add(f'<path d="M196 522 Q196 330 256 318 Q316 330 316 522Z" {st("#ff3d8b")}/>')
    arms = 'M214 372 Q196 300 166 250 M298 372 Q316 300 346 250'
    I.add(f'<path d="{arms}" stroke="{INK}" stroke-width="40" fill="none" stroke-linecap="round"/><path d="{arms}" stroke="#ffd2a8" stroke-width="26" fill="none" stroke-linecap="round"/>')
    I.add(f'<circle cx="256" cy="282" r="58" {st("#ffd2a8")}/><path d="M200 270 Q206 214 256 216 Q308 214 312 268 Q290 244 256 246 Q222 244 200 270Z" fill="#5a3214" stroke="{INK}" stroke-width="6"/>')
    eyes(I, 256, 290, .9, 22); smile(I, 256, 312, .8, True)
    # manos de neón
    for x in (160, 352):
        I.add(f'<circle cx="{x}" cy="236" r="58" fill="#35f0ff" opacity=".22"/><circle cx="{x}" cy="236" r="58" fill="none" stroke="#35f0ff" stroke-width="9"/>')
    # manzana atrapada
    I.add(f'<path d="M160 214 Q136 196 124 222 Q114 262 160 270 Q206 262 196 222 Q184 196 160 214Z" {st("#ff3b3b", 7)}/><path d="M160 214 Q162 196 172 186" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M168 196 Q186 180 196 194 Q180 204 168 196Z" fill="#4fc35a" stroke="{INK}" stroke-width="4"/>')
    shine(I, 142, 226, 9, 6, -30, .6)
    # moneda en la otra mano
    I.add(f'<circle cx="352" cy="236" r="34" {st("#ffd23f", 7)}/><circle cx="352" cy="236" r="22" fill="none" stroke="#c98a00" stroke-width="5"/><path d="{star5(352, 236, 13)}" fill="#c98a00"/>')
    # lo que sigue cayendo
    I.add(f'<path d="M84 70 Q120 120 170 104 Q130 128 92 96 Z" {st("#ffe14d", 6)}/>')
    I.add(f'<path d="M262 56 Q228 56 232 84 Q240 112 262 122 Q284 112 292 84 Q296 56 262 56Z" {st("#ff3d5a", 6)}/><circle cx="252" cy="80" r="3" fill="#ffe14d"/><circle cx="272" cy="78" r="3" fill="#ffe14d"/><circle cx="262" cy="98" r="3" fill="#ffe14d"/><path d="M248 58 L262 44 L276 58" stroke="#4fc35a" stroke-width="8" fill="none" stroke-linecap="round"/>')
    I.add(f'<circle cx="420" cy="118" r="40" {st("#2b2440")}/><rect x="410" y="66" width="20" height="16" rx="4" fill="#6b6f80" stroke="{INK}" stroke-width="5"/><path d="M420 66 Q424 46 440 40" stroke="{INK}" stroke-width="5" fill="none"/>')
    sparkle(I, 444, 36, 14, '#ffb300'); shine(I, 406, 104, 10, 6, -30, .5)
    I.add(f'<circle cx="60" cy="300" r="22" {st("#ffd23f", 6)}/>')
    sparkle(I, 470, 300, 14); sparkle(I, 330, 70, 10, '#35f0ff')

@icon('muro-loco')
def _(I):
    bg(I, '#2a1f7a', '#0b0730', '#ff3d8b', .08)
    # muro de ladrillos
    I.add(f'<rect x="34" y="40" width="444" height="432" rx="24" fill="{I.lg("#8a2cff", "#ff3d8b")}" stroke="{INK}" stroke-width="10"/>')
    rows = ''.join(f'<path d="M40 {y} H472" stroke="#fff" stroke-opacity=".18" stroke-width="4"/>' for y in range(94, 472, 54))
    cols = ''.join(f'<path d="M{x + (27 if r % 2 else 0)} {40 + r*54} v54" stroke="#fff" stroke-opacity=".18" stroke-width="4"/>' for r in range(8) for x in range(94, 470, 74))
    I.add(rows + cols)
    # hueco con forma de estrella humana
    seg = [(256, 140, 256, 140), (256, 186, 256, 300), (256, 200, 152, 120), (256, 200, 360, 120), (256, 300, 176, 420), (256, 300, 336, 420)]
    def path(w, c, o=1):
        return ''.join(f'<path d="M{a} {b} L{c2} {d}" stroke="{c}" stroke-width="{w}" stroke-linecap="round" opacity="{o}"/>' for a, b, c2, d in seg)
    I.add(path(92, '#35f0ff', .35) + path(76, '#35f0ff') + path(62, '#0e0a2e'))
    I.add('<circle cx="256" cy="140" r="44" fill="#35f0ff"/><circle cx="256" cy="140" r="37" fill="#0e0a2e"/>')
    # jugador en el hueco
    I.add(path(16, '#5dff9a'))
    I.add('<circle cx="256" cy="140" r="22" fill="none" stroke="#5dff9a" stroke-width="10"/>')
    for x, y in ((152, 120), (360, 120), (176, 420), (336, 420)):
        I.add(f'<circle cx="{x}" cy="{y}" r="11" fill="#fff"/>')
    sparkle(I, 430, 450, 18, '#ffd23f'); sparkle(I, 76, 300, 14); sparkle(I, 452, 220, 10, '#35f0ff')

def fball(I, x, y, r, rot=0):
    I.add(f'<g transform="translate({x} {y}) rotate({rot})"><circle r="{r}" {st("#ffffff", 7)}/>'
          + f'<path d="{star5(0, 0, r*.36, r*.36*.81, -90)}" fill="{INK}" opacity="0"/>'
          + ''.join(f'<path d="M{r*.36*math.cos(math.radians(-90+72*i)):.1f} {r*.36*math.sin(math.radians(-90+72*i)):.1f}" />' for i in range(5))
          + '<path d="' + 'M' + ' L'.join(f'{r*.34*math.cos(math.radians(-90+72*i)):.1f} {r*.34*math.sin(math.radians(-90+72*i)):.1f}' for i in range(5)) + f'Z" fill="{INK}"/>'
          + ''.join('<path d="' + 'M' + ' L'.join(f'{(r*.98*math.cos(math.radians(-54+72*k))+r*.2*math.cos(math.radians(-54+72*k+72*i))):.1f} {(r*.98*math.sin(math.radians(-54+72*k))+r*.2*math.sin(math.radians(-54+72*k+72*i))):.1f}' for i in range(5)) + f'Z" fill="{INK}"/>' for k in range(5))
          + f'<circle r="{r}" fill="none" stroke="{INK}" stroke-width="7"/></g>')
    shine(I, x - r*.35, y - r*.42, r*.3, r*.14, -30, .55)

def glove(I, x, y, s, rot, col):
    I.add(f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
          + ''.join(f'<rect x="{fx-6}" y="{fy}" width="12" height="{fh}" rx="6" {st(col, 5)}/>' for fx, fy, fh in ((-21, -46, 34), (-7, -54, 40), (7, -53, 38), (20, -45, 32)))
          + f'<rect x="-28" y="-24" width="56" height="50" rx="16" {st(col, 5)}/><rect x="-44" y="-10" width="14" height="30" rx="7" transform="rotate(-35 -37 5)" {st(col, 5)}/>'
          + f'<rect x="-27" y="22" width="54" height="14" rx="3" fill="{INK}"/><rect x="-27" y="25" width="54" height="4" fill="#fff"/></g>')

@icon('portero-loco')
def _(I):
    bg(I, '#2a3a9a', '#0a0f3a', '#ffffff', .08)
    I.add('<rect x="0" y="300" width="512" height="212" fill="#24a044"/>' + ''.join(f'<rect x="{x}" y="300" width="60" height="212" fill="#1f8a3a"/>' for x in range(0, 512, 120)))
    # gradas con público
    import random; R = random.Random(7)
    I.add('<rect x="0" y="90" width="512" height="200" fill="#1a1440"/>' + ''.join(f'<rect x="{R.randint(0,510)}" y="{R.randint(96,284)}" width="5" height="6" fill="{R.choice(["#ff3d5a","#fff","#35a0ff","#ffd93d"])}" opacity=".6"/>' for _ in range(260)))
    # portería y red
    I.add('<g opacity=".35" stroke="#fff" stroke-width="2">' + ''.join(f'<path d="M{x} 70 L{x+300} 470"/><path d="M{x+300} 70 L{x} 470"/>' for x in range(-260, 520, 34)) + '</g>')
    I.add(f'<path d="M40 470 V64 H472 V470" fill="none" stroke="{INK}" stroke-width="30" stroke-linejoin="round"/><path d="M40 470 V64 H472 V470" fill="none" stroke="#f4f6fb" stroke-width="18" stroke-linejoin="round"/>')
    glove(I, 170, 300, 2.1, -18, '#2fd67a'); glove(I, 360, 250, 2.1, 22, '#ff7a1f')
    fball(I, 300, 190, 70, 20)
    sparkle(I, 410, 130, 22, '#ffd93d'); sparkle(I, 110, 160, 16); sparkle(I, 230, 120, 12, '#ffd93d')
    I.add('<path d="M330 120 L362 92 M340 150 L384 136 M300 108 L306 70" stroke="#fff" stroke-width="8" stroke-linecap="round"/>')

@icon('balon-loco')
def _(I):
    bg(I, '#7a2a9a', '#1a0b4a', '#ff9500', .1)
    import random; R = random.Random(3)
    x = 0
    while x < 512:
        w = R.randint(40, 80); h = R.randint(90, 200)
        I.add(f'<rect x="{x}" y="{330-h}" width="{w}" height="{h+2}" fill="#140a34"/>' + ''.join(f'<rect x="{x+6+k*12}" y="{330-h+10+m*16}" width="5" height="7" fill="#ffd678" opacity=".8"/>' for k in range((w-8)//12) for m in range((h-14)//16) if R.random() < .3))
        x += w + 4
    I.add('<rect x="0" y="330" width="512" height="182" fill="#3a2a8a"/><ellipse cx="256" cy="430" rx="190" ry="54" fill="none" stroke="#ffd93d" stroke-width="8"/>')
    # pierna que toca el balón
    I.add(f'<path d="M150 512 L210 400 L300 392" fill="none" stroke="{INK}" stroke-width="58" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M150 512 L210 400 L300 392" fill="none" stroke="#ff9500" stroke-width="40" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M272 372 Q330 360 350 388 Q356 410 330 414 L272 414 Z" {st("#35f0ff", 7)}/>')
    fball(I, 300, 230, 80, -15)
    I.add('<path d="M300 330 Q300 340 300 350" stroke="#fff" stroke-width="6" stroke-dasharray="4 10" stroke-linecap="round"/>')
    for k, (x, y) in enumerate(((200, 200), (400, 210), (300, 120))):
        I.add(f'<path d="M{x} {y} Q{(x+300)/2} {y-30} 300 230" fill="none" stroke="#fff" stroke-width="5" stroke-dasharray="2 14" stroke-linecap="round" opacity=".7"/>')
    sparkle(I, 410, 120, 22, '#ffd93d'); sparkle(I, 120, 110, 16, '#35f0ff'); sparkle(I, 440, 300, 12)
    I.add(f'<text x="420" y="90" text-anchor="middle" font-size="64" {FONT} fill="#ffd93d" stroke="{INK}" stroke-width="6" paint-order="stroke">12</text>')

@icon('bloques-neon')
def _(I):
    bg(I, '#3a2fa8', '#14205e', '#ff6ad0', .10)
    PALB = {1: ('#e8384f', '#ff7a8a', '#a3182b'), 3: ('#f3c230', '#ffe46b', '#b8860b'), 4: ('#5bbd3a', '#a0ec7c', '#2f8a1f'),
            5: ('#22c3c3', '#74f5ec', '#0e7a85'), 6: ('#2f6fe0', '#6aa5ff', '#1e3fa8'), 7: ('#9a4fe0', '#c88bff', '#5f26a3')}
    def blk(x, y, s, c):
        m, l, d = PALB[c]
        I.add(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s*.2}" fill="{d}" stroke="{INK}" stroke-width="4"/>'
              f'<rect x="{x+2}" y="{y+2}" width="{s-4}" height="{s*.8}" rx="{s*.18}" fill="{m}"/>'
              f'<rect x="{x+s*.16}" y="{y+s*.1}" width="{s*.68}" height="{s*.1}" rx="3" fill="#fff" opacity=".6"/>')
    # tablero
    X0, Y0, C = 96, 120, 46
    I.add(f'<rect x="{X0-14}" y="{Y0-14}" width="{C*7+28}" height="{C*7+28}" rx="22" fill="#0e1444" stroke="#c88bff" stroke-width="7"/>')
    for r in range(7):
        for c in range(7):
            I.add(f'<rect x="{X0+c*C+3}" y="{Y0+r*C+3}" width="{C-6}" height="{C-6}" rx="7" fill="#18215a"/>')
    fill = {(6, 0): 6, (6, 1): 6, (5, 0): 6, (6, 4): 3, (6, 5): 3, (6, 6): 3, (5, 6): 5, (4, 6): 5, (4, 0): 1, (5, 1): 4, (5, 2): 4, (6, 2): 4, (2, 5): 7, (3, 5): 7, (3, 6): 7, (3, 0): 5, (3, 1): 3, (3, 2): 1, (3, 3): 6, (3, 4): 4}
    for (r, c), col in fill.items(): blk(X0 + c*C + 2, Y0 + r*C + 2, C - 4, col)
    # fila que explota
    I.add(f'<rect x="{X0-10}" y="{Y0+3*C-6}" width="{C*7+20}" height="{C+12}" rx="14" fill="#6fe3ff" opacity=".35"/>'
          f'<rect x="{X0-4}" y="{Y0+3*C+C*.35}" width="{C*7+8}" height="{C*.3}" rx="6" fill="#e8fbff" opacity=".9"/>')
    # pieza en la mano
    for r, c in ((0, 0), (0, 1), (1, 1)): blk(330 + c*52, 34 + r*52, 50, 1)
    sparkle(I, 120, 300, 22, '#ffe46b'); sparkle(I, 420, 250, 16); sparkle(I, 260, 290, 14, '#ff9de0')

@icon('ciudadela-de-arena')
def _(I):
    bg(I, '#ffb35c', '#7a2e3a', '#ffe7a8', .12)
    # luna y cúpulas del palacio
    I.add('<circle cx="390" cy="110" r="46" fill="#fff1c9" opacity=".9"/>')
    for x, r, h in ((90, 46, 230), (250, 70, 190), (420, 40, 250)):
        I.add(f'<path d="M{x-r} {h+60} V{h} Q{x-r} {h-r*1.2} {x} {h-r*1.6} Q{x+r} {h-r*1.2} {x+r} {h} V{h+60}Z" fill="#5a2a45" opacity=".55"/>')
    # muro de piedra y cornisa
    I.add(f'<path d="M-10 522 V330 H340 V522Z" fill="#c98b4e" stroke="{INK}" stroke-width="8"/>'
          + ''.join(f'<path d="M-10 {y} H340" stroke="#9c6534" stroke-width="5"/>' for y in (380, 430, 480))
          + ''.join(f'<path d="M{x} {y} v50" stroke="#9c6534" stroke-width="5"/>' for x, y in ((60, 330), (170, 330), (280, 330), (110, 380), (230, 380), (60, 430), (190, 430), (300, 430)))
          + f'<rect x="-10" y="318" width="360" height="22" rx="6" fill="#e8b170" stroke="{INK}" stroke-width="7"/>')
    # espinas del foso
    I.add(''.join(f'<path d="M{x} 522 l16 -46 l16 46Z" fill="#d9dcef" stroke="{INK}" stroke-width="5"/>' for x in range(350, 522, 34)))
    # prisionero saltando con espada
    I.add('<g transform="translate(380 250) rotate(12)">'
          f'<path d="M-14 40 L-46 86 M14 40 L40 92" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><path d="M-14 40 L-46 86 M14 40 L40 92" stroke="#f3ead6" stroke-width="14" stroke-linecap="round"/>'
          f'<rect x="-28" y="-30" width="56" height="74" rx="20" fill="#2f6fd6" stroke="{INK}" stroke-width="8"/><path d="M-28 22 H28" stroke="#ffd23f" stroke-width="9"/>'
          f'<path d="M-22 -14 Q-60 -30 -74 -64" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M-22 -14 Q-60 -30 -74 -64" stroke="#c98a5e" stroke-width="10" fill="none" stroke-linecap="round"/>'
          f'<path d="M22 -12 Q56 -2 76 -26" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M22 -12 Q56 -2 76 -26" stroke="#c98a5e" stroke-width="10" fill="none" stroke-linecap="round"/>'
          f'<path d="M76 -26 L130 -110" stroke="{INK}" stroke-width="16" stroke-linecap="round"/><path d="M76 -26 L130 -110" stroke="#eef3ff" stroke-width="8" stroke-linecap="round"/><path d="M62 -40 L92 -16" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
          f'<circle cx="0" cy="-62" r="32" fill="#c98a5e" stroke="{INK}" stroke-width="8"/><path d="M-34 -70 Q0 -110 34 -70 Q20 -84 0 -84 Q-20 -84 -34 -70Z" fill="#f3ead6" stroke="{INK}" stroke-width="6"/>'
          '</g>')
    eyes(I, 396, 192, .6, 18); smile(I, 394, 208, .5)
    sparkle(I, 220, 120, 16, '#ffe7a8'); sparkle(I, 470, 300, 12)

@icon('halfpipe')
def _(I):
    bg(I, '#1a2a6c', '#0b1020', '#ffe14d', .10)
    # focos del estadio
    for x in (70, 442):
        I.add(f'<path d="M{x} 40 L{256 if x<256 else 256} 300" stroke="#ffe14d" stroke-width="70" opacity=".08"/><circle cx="{x}" cy="40" r="22" fill="#fff6c0" stroke="{INK}" stroke-width="6"/>')
    stars_bg(I, 14, seed=8)
    # halfpipe en U
    I.add(f'<path d="M-10 522 V250 H40 Q40 450 256 450 Q472 450 472 250 H522 V522Z" fill="#7aa0ff" stroke="{INK}" stroke-width="9"/>'
          f'<path d="M40 250 Q40 450 256 450 Q472 450 472 250" fill="none" stroke="#c9d8ff" stroke-width="10" opacity=".7"/>'
          f'<path d="M-10 250 H44 M468 250 H522" stroke="#ffe14d" stroke-width="12"/>'
          f'<path d="M110 380 Q256 470 402 380" fill="none" stroke="#5a7fe0" stroke-width="5" opacity=".7"/>')
    # estela de vuelo
    I.add('<path d="M460 250 Q420 90 300 120" fill="none" stroke="#ffe14d" stroke-width="8" stroke-dasharray="4 18" stroke-linecap="round" opacity=".9"/>')
    # skater agarrando la tabla en el aire
    I.add('<g transform="translate(250 150) rotate(-18)">'
          f'<path d="M-62 70 Q0 52 62 70" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M-62 70 Q0 52 62 70" stroke="#ff9d1c" stroke-width="10" fill="none" stroke-linecap="round"/>'
          f'<circle cx="-42" cy="82" r="10" fill="#ffe14d" stroke="{INK}" stroke-width="5"/><circle cx="40" cy="80" r="10" fill="#ffe14d" stroke="{INK}" stroke-width="5"/>'
          f'<path d="M-26 52 L-12 6 M26 50 L12 6" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><path d="M-26 52 L-12 6 M26 50 L12 6" stroke="#2d3f5e" stroke-width="14" stroke-linecap="round"/>'
          f'<rect x="-30" y="-56" width="60" height="66" rx="22" fill="#ff4f6d" stroke="{INK}" stroke-width="8"/>'
          f'<path d="M-24 -30 Q-56 10 -40 56" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M-24 -30 Q-56 10 -40 56" stroke="#ffcf9e" stroke-width="10" fill="none" stroke-linecap="round"/>'
          f'<path d="M24 -36 Q60 -60 70 -86" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round"/><path d="M24 -36 Q60 -60 70 -86" stroke="#ffcf9e" stroke-width="10" fill="none" stroke-linecap="round"/>'
          f'<circle cx="0" cy="-86" r="34" fill="#ffcf9e" stroke="{INK}" stroke-width="8"/><path d="M-36 -92 A36 36 0 0 1 36 -92 Z" fill="#ffe14d" stroke="{INK}" stroke-width="7"/>'
          '</g>')
    eyes(I, 226, 72, .7, 20); smile(I, 228, 90, .6, True)
    sparkle(I, 110, 170, 18, '#ffe14d'); sparkle(I, 410, 140, 14)

@icon('drop-in')
def _(I):
    bg(I, '#ffb36b', '#ff5f8f', '#fff3c4', .14)
    I.add(f'<circle cx="256" cy="230" r="110" fill="#ffe680" opacity=".9"/>')
    for x, h in ((40, 150), (90, 110), (420, 140), (470, 100)): I.add(f'<rect x="{x}" y="{380-h}" width="40" height="{h}" fill="#7a5cff" opacity=".45"/>')
    # palmeras
    for x, y, sc in ((70, 300, 1), (450, 290, .9)):
        I.add(f'<g transform="translate({x} {y}) scale({sc})"><path d="M0 120 C6 60 -4 20 6 -20" stroke="{INK}" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M0 120 C6 60 -4 20 6 -20" stroke="#7a5a3a" stroke-width="7" fill="none" stroke-linecap="round"/>'
              + ''.join(f'<path d="M6 -20 q{dx} {dy} {dx*2} {dy*2+30}" stroke="{INK}" stroke-width="13" fill="none" stroke-linecap="round"/><path d="M6 -20 q{dx} {dy} {dx*2} {dy*2+30}" stroke="#2f8a4a" stroke-width="7" fill="none" stroke-linecap="round"/>' for dx, dy in ((-30, -24), (30, -24), (-36, 0), (36, 0))) + '</g>')
    # quarter pipe
    I.add(f'<path d="M-10 522 V420 H260 Q420 420 440 300 H522 V522Z" fill="#b6b3ab" stroke="{INK}" stroke-width="8"/><path d="M440 300 H522" stroke="#d8dde2" stroke-width="12"/>'
          f'<path d="M-10 470 H522" stroke="#9a978f" stroke-width="5" opacity=".6"/>')
    # skater en el aire (kickflip)
    I.add('<g transform="translate(256 250)">'
          f'<path d="M-70 92 Q0 70 70 92" stroke="{INK}" stroke-width="20" fill="none" stroke-linecap="round" transform="rotate(-12)"/><path d="M-70 92 Q0 70 70 92" stroke="#ff4f3a" stroke-width="10" fill="none" stroke-linecap="round" transform="rotate(-12)"/>'
          f'<circle cx="-48" cy="104" r="11" fill="#ffa51f" stroke="{INK}" stroke-width="5"/><circle cx="44" cy="86" r="11" fill="#ffa51f" stroke="{INK}" stroke-width="5"/>'
          f'<path d="M-30 60 L-14 10 M30 54 L14 10" stroke="{INK}" stroke-width="26" stroke-linecap="round"/><path d="M-30 60 L-14 10 M30 54 L14 10" stroke="#2d3f5e" stroke-width="14" stroke-linecap="round"/>'
          f'<path d="M-34 20 Q0 -10 34 20 L30 -50 Q0 -64 -30 -50Z" {st("#e8452c", 8)}/>'
          f'<path d="M-30 -40 L-90 -70 M30 -40 L90 -20" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M-30 -40 L-90 -70 M30 -40 L90 -20" stroke="#e8452c" stroke-width="11" stroke-linecap="round"/>'
          f'<circle cx="0" cy="-92" r="34" {st(I.rg("#ffd0aa", "#dfaa82", .4, .35, .8), 8)}/><path d="M-36 -98 Q0 -140 36 -98 L50 -96 Z" {st("#15151a", 6)}/>'
          '</g>')
    eyes(I, 258, 160, .6, 24); smile(I, 258, 178, .6, True)
    for i, (x, y) in enumerate(((150, 330), (130, 300), (112, 270))): I.add(f'<path d="M{x} {y} q-20 -10 -40 -4" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" opacity="{.9-i*.25}"/>')
    sparkle(I, 360, 120, 16); sparkle(I, 150, 110, 12)

@icon('catquiz-barbarismes')
def _(I):
    cq_bg(I, '#ff9a9a', '#d63a5a')
    # dues targetes de frase: una ratllada, l'altra correcta
    I.add(f'<g transform="rotate(-6 256 180)"><rect x="70" y="120" width="372" height="110" rx="22" {st("#fff")}/>'
          f'<rect x="100" y="150" width="200" height="18" rx="9" fill="#c9c3e6"/><rect x="100" y="184" width="150" height="18" rx="9" fill="#c9c3e6"/>'
          f'<path d="M90 140 L420 210" stroke="#e8384f" stroke-width="16" stroke-linecap="round"/></g>')
    I.add(f'<circle cx="420" cy="132" r="34" {st("#e8384f", 7)}/><path d="M404 116 l32 32 M436 116 l-32 32" stroke="#fff" stroke-width="9" stroke-linecap="round"/>')
    I.add(f'<g transform="rotate(4 256 330)"><rect x="70" y="280" width="372" height="110" rx="22" {st("#fff")}/>'
          f'<rect x="100" y="310" width="230" height="18" rx="9" fill="#c9c3e6"/><rect x="100" y="344" width="170" height="18" rx="9" fill="#c9c3e6"/></g>')
    I.add(f'<circle cx="420" cy="300" r="34" {st("#4fc35a", 7)}/><path d="M404 300 l11 12 l22 -24" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    sparkle(I, 460, 430, 16)

@icon('catquiz-quiz-de-futbol')
def _(I):
    cq_bg(I, '#7fd0ff', '#2f6fe0')
    I.add('<path d="M-10 400 H522" stroke="#fff" stroke-width="8" opacity=".5"/><circle cx="256" cy="400" r="120" fill="none" stroke="#fff" stroke-width="8" opacity=".5"/>')
    I.add(f'<circle cx="256" cy="240" r="118" {st("#fff")}/><path d="M256 182 L311 222 L290 286 L222 286 L201 222Z" fill="{INK}"/>'
          + ''.join(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{INK}" stroke-width="7"/>' for x1, y1, x2, y2 in ((256, 182, 256, 124), (311, 222, 366, 204), (290, 286, 324, 334), (222, 286, 188, 334), (201, 222, 146, 204))))
    shine(I, 215, 180, 30, 16, -30, .5)
    I.add(f'<circle cx="400" cy="120" r="54" {st("#ffd23f")}/><text x="400" y="150" text-anchor="middle" font-size="84" {FONT} fill="{INK}">?</text>')
    sparkle(I, 110, 110, 18)


# ===================== MINIGOLF Y BOLOS =====================
def pin(I, x, y, s=1, rot=0):
    """Bolo blanco con dos franjas rojas."""
    I.add(f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
          f'<path d="M0 -92 C16 -92 20 -76 16 -62 C12 -50 10 -42 14 -30 C30 -6 34 22 26 46 C20 62 12 70 0 70 C-12 70 -20 62 -26 46 C-34 22 -30 -6 -14 -30 C-10 -42 -12 -50 -16 -62 C-20 -76 -16 -92 0 -92Z" {st(I.lg("#ffffff", "#dfe2f2", 0, 0, 1, 0), 7)}/>'
          f'<path d="M-15 -52 Q0 -46 15 -52 M-13 -42 Q0 -36 13 -42" stroke="#ff3d5a" stroke-width="7" fill="none" stroke-linecap="round"/>'
          f'<ellipse cx="-8" cy="-74" rx="4" ry="9" fill="#fff" opacity=".9"/><ellipse cx="-12" cy="14" rx="5" ry="22" fill="#fff" opacity=".8"/></g>')

@icon('strike-party')
def _(I):
    bg(I, '#5b2bd8', '#160a3d', '#ff4fd8', .12)
    stars_bg(I, 12, seed=21)
    # arcos de neón
    for r, c in ((210, '#ff4fd8'), (180, '#3df2ff'), (150, '#ffe14d')):
        I.add(f'<path d="M{256-r} 300 A{r} {r} 0 0 1 {256+r} 300" fill="none" stroke="{c}" stroke-width="12" opacity=".85"/>'
              f'<path d="M{256-r} 300 A{r} {r} 0 0 1 {256+r} 300" fill="none" stroke="{c}" stroke-width="30" opacity=".18"/>')
    # pista en perspectiva
    I.add(f'<path d="M206 270 H306 L470 522 H42Z" fill="{I.lg("#ffe3b8", "#e8a86a")}" stroke="{INK}" stroke-width="9"/>'
          f'<path d="M226 270 L150 522 M286 270 L362 522" stroke="#c98a4e" stroke-width="4" opacity=".6"/>'
          f'<path d="M196 270 L30 522 M316 270 L482 522" stroke="#3df2ff" stroke-width="10"/>')
    # bolos saliendo volando
    pin(I, 256, 236, .55, 0); pin(I, 214, 228, .52, -38); pin(I, 300, 222, .5, 34)
    pin(I, 150, 170, .5, -70); pin(I, 366, 160, .52, 64); pin(I, 268, 120, .46, 160)
    for x, y in ((190, 150), (330, 110), (230, 90), (400, 220), (110, 230)): sparkle(I, x, y, 14, '#ffe14d')
    # bola con brillo y estela
    I.add('<path d="M256 470 Q248 400 254 330" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" opacity=".35"/>')
    I.add(f'<circle cx="256" cy="420" r="70" {st(I.rg("#fff27a", "#ff7a1a", .35, .3, .85))}/>')
    I.add(f'<circle cx="236" cy="398" r="9" fill="{INK}"/><circle cx="262" cy="390" r="9" fill="{INK}"/><circle cx="254" cy="416" r="9" fill="{INK}"/>')
    shine(I, 226, 378, 22, 12, -30, .7)
    sparkle(I, 440, 90, 20); sparkle(I, 80, 110, 14)

@icon('kauai-minigolf')
def _(I):
    bg(I, '#9df2ff', '#1aa7d8', '#ffffff', .12)
    # avioneta con pancarta
    I.add(f'<path d="M290 92 H470 V128 H290Z" {st("#ffffff", 6)}/><text x="380" y="120" text-anchor="middle" font-size="27" {FONT} fill="#1e6bff">kauai.es</text>'
          f'<path d="M290 110 H262" stroke="{INK}" stroke-width="4"/>'
          f'<path d="M188 104 L252 96 Q266 104 252 116 L188 116Z" {st("#ff6b4a", 6)}/><path d="M212 86 L226 100 L212 128 L204 128Z" {st("#ffd23f", 5)}/>')
    # mar e isla
    I.add(f'<path d="M-10 330 C120 300 380 300 522 330 V522 H-10Z" fill="{I.lg("#2fd0e0", "#0f78b8")}"/>')
    I.add(f'<ellipse cx="256" cy="392" rx="232" ry="92" {st(I.lg("#ffe7a8", "#e8b45a"))}/>'
          f'<ellipse cx="256" cy="378" rx="196" ry="70" {st(I.lg("#7ce06a", "#2fa84a"), 7)}/>'
          f'<path d="M110 372 Q256 330 402 372" fill="none" stroke="#a8f090" stroke-width="10" opacity=".6"/>')
    # palmera
    I.add(f'<path d="M96 380 Q84 300 112 230" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/><path d="M96 380 Q84 300 112 230" fill="none" stroke="#b07a42" stroke-width="12" stroke-linecap="round"/>')
    for d in ('M112 230 Q70 200 34 226 Q74 214 112 236Z', 'M112 230 Q150 186 196 210 Q150 206 114 238Z', 'M112 230 Q100 176 128 150 Q118 190 118 232Z', 'M112 230 Q60 240 50 280 Q78 248 112 238Z'):
        I.add(f'<path d="{d}" {st("#3fd06a", 6)}/>')
    # hoyo y bandera
    I.add(f'<ellipse cx="330" cy="382" rx="34" ry="12" fill="#14301c" stroke="{INK}" stroke-width="5"/>')
    I.add(f'<path d="M330 380 V214" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><path d="M330 380 V214" stroke="#fff" stroke-width="5" stroke-linecap="round"/>')
    I.add(f'<path d="M334 218 Q380 226 418 214 Q394 244 420 270 Q380 262 334 268Z" {st("#1e6bff", 7)}/><text x="372" y="256" text-anchor="middle" font-size="34" {FONT} fill="#fff">K</text>')
    # palo y bola
    I.add(f'<path d="M150 470 L236 316" stroke="{INK}" stroke-width="14" stroke-linecap="round"/><path d="M150 470 L236 316" stroke="#c9d1e6" stroke-width="6" stroke-linecap="round"/>')
    I.add(f'<path d="M120 466 h56 a10 10 0 0 1 0 20 h-56Z" {st("#ffd23f", 6)}/>')
    I.add(f'<path d="M206 410 Q260 390 300 394" fill="none" stroke="#fff" stroke-width="7" stroke-dasharray="3 14" stroke-linecap="round"/>')
    I.add(f'<circle cx="200" cy="418" r="24" {st(I.rg("#ffffff", "#d8deef", .35, .3, .85), 7)}/><path d="M178 420 Q200 428 222 420" stroke="#1e6bff" stroke-width="6" fill="none"/>')
    shine(I, 192, 408, 8, 5, -30, .9)
    sparkle(I, 440, 300, 16); sparkle(I, 60, 120, 14)


@icon('catquiz-party')
def _(I):
    cq_bg(I, '#c06bff', '#5b2be0')
    # tres mòbils amb les respostes de colors
    for x, y, r, c in ((128, 300, -12, '#ff4fd8'), (384, 300, 12, '#38e8ff'), (256, 268, 0, '#ffd24a')):
        g = f'<g transform="translate({x} {y}) rotate({r})">'
        g += f'<rect x="-78" y="-140" width="156" height="280" rx="26" {st("#1d1442")}/><rect x="-64" y="-118" width="128" height="232" rx="14" fill="#2e2080"/>'
        g += f'<rect x="-54" y="-104" width="108" height="34" rx="10" fill="{c}"/>'
        for k, (cx, cy, cc) in enumerate(((-28, -40, '#e8357f'), (28, -40, '#e0a800'), (-28, 22, '#1ba8d6'), (28, 22, '#f07a12'))):
            g += f'<rect x="{cx-24}" y="{cy-24}" width="48" height="48" rx="10" fill="{cc}"/>'
        g += '</g>'
        I.add(g)
    I.add(f'<path d="M206 92 L226 132 L256 100 L286 132 L306 92 L298 150 H214Z" {st("#ffd24a", 7)}/>')
    sparkle(I, 70, 120, 18); sparkle(I, 450, 110, 16); sparkle(I, 440, 460, 12)

# CatQuiz: la mascota gata asoma en la esquina
for _s in ['catquiz-party','catquiz-com-es-diu-en-catala','catquiz-motle','catquiz-accents','catquiz-anagrama','catquiz-sopa-de-lletres','catquiz-lletres-perdudes','catquiz-penjat-3d','catquiz-barbarismes','catquiz-quiz-de-futbol','catquiz-roda-de-paraules','catquiz-pronoms-febles','catquiz-quiz-d-esportistes','catquiz-quiz-de-castells']:
    ICONS[_s] = (lambda f: (lambda I: (f(I), cat(I, 78, 466, .82))))(ICONS[_s])


def main():
    D = json.load(open(os.path.join(root, 'tools/games.json'), encoding='utf-8'))
    slugs = [g['slug'] for g in D['GAMES'] if g.get('play') or g.get('url')]
    miss = [s for s in slugs if s not in ICONS]
    for s, f in ICONS.items():
        I = Icon(); f(I)
        open(os.path.join(OUT, s + '.svg'), 'w', encoding='utf-8').write(I.svg())
    print(len(ICONS), 'ilustraciones · sin ilustración:', miss)

if __name__ == '__main__':
    main()
