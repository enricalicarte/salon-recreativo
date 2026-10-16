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
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512"><defs>' + ''.join(s.defs) + '</defs>' + ''.join(s.body) + '</svg>')

def st(fill, w=SW, extra=''):
    return f'fill="{fill}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" {extra}'

def bg(I, c1, c2, rays=None, ra=.12):
    I.add(f'<rect width="512" height="512" fill="{I.rg(c1, c2, .5, .42, .75)}"/>')
    if rays:
        p = ''
        for k in range(16):
            a0 = k * math.pi / 8; a1 = a0 + math.pi / 16
            p += f'M256 230L{256+700*math.cos(a0):.0f} {230+700*math.sin(a0):.0f}L{256+700*math.cos(a1):.0f} {230+700*math.sin(a1):.0f}Z'
        I.add(f'<path d="{p}" fill="{rays}" opacity="{ra}"/>')

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

@icon('catquiz-esquiva')
def _(I):
    cq_bg(I, '#ff9ad5', '#9a3cff')
    I.add(f'<path d="M256 180 L-40 522 H552Z" fill="{I.lg("#8de06a", "#3a9a3a")}"/>')
    for (x, y, s) in ((150, 230, 60), (360, 260, 74)): I.add(f'<rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" rx="10" {st("#ff5a3c", 7)}/>')
    I.add(f'<circle cx="256" cy="360" r="70" {st(I.lg("#ffe680", "#ffb11f"))}/><circle cx="234" cy="350" r="10" fill="{INK}"/><circle cx="278" cy="350" r="10" fill="{INK}"/><path d="M236 384 q20 14 40 0" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    I.add(f'<circle cx="390" cy="410" r="28" {st("#ffd23f", 6)}/><text x="390" y="422" text-anchor="middle" font-size="32" {FONT} fill="{INK}">€</text>')
    for i in range(3): I.add(f'<path d="M{150-i*24} {330+i*20} h-40" stroke="#fff" stroke-width="9" stroke-linecap="round"/>')

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

@icon('catquiz-caca-estrelles')
def _(I):
    bg(I, '#8de06a', '#2a9a3a', '#ffffff', .18)
    for (x, y, r, rot) in ((130, 140, 44, -10), (380, 110, 36, 15), (400, 330, 48, 5), (150, 380, 32, -20)): I.add(f'<path d="{star5(x, y, r, rot=rot-90)}" {st("#ffd23f", 7)}/>')
    I.add(f'<circle cx="256" cy="256" r="70" {st(I.lg("#ff7ad9", "#d12a8a"))}/>'); shine(I, 230, 225, 22, 12, -30, .6)
    I.add(f'<circle cx="300" cy="420" r="34" {st("#2b2440", 7)}/><path d="M318 392 Q330 370 350 372" stroke="{INK}" stroke-width="6" fill="none"/><circle cx="352" cy="370" r="7" fill="#ff9a3c"/>')

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
