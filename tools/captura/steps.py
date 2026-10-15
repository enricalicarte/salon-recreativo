W = ('wait',)
def w(ms): return ('wait', ms)
def wiggle(keys=('ArrowLeft', 'ArrowRight'), n=6, ms=450):
    out = []
    for i in range(n): out.append(('hold', [keys[i % len(keys)]], ms))
    return out
def mouse_tour(n=8, ms=350):
    pts = [(300, 250), (650, 220), (700, 400), (260, 420), (480, 300), (620, 260), (330, 330), (560, 420)]
    out = []
    for i in range(n):
        x, y = pts[i % len(pts)]; out += [('js', f'void 0'), ('drag', x, y, pts[(i + 1) % len(pts)][0], pts[(i + 1) % len(pts)][1], ms)]
    return out
HIDE_RELAX = ('js', "(()=>{const s=document.createElement('style');s.textContent='#back,#gtitle,#hint,#extra,#mute,#langBtn,#breathBtn,.topbar,header,.hud,.chip,button{opacity:0!important}';document.head.appendChild(s)})()")

STEPS = {
 # ---------- saga cósmica ----------
 'ruta-cosmica': {'setup': [w(2500), ('text', 'a volar'), w(1500), ('text', 'saltar'), w(1000), ('text', 'entendido'), w(800), ('text', 'despegar'), w(800), ('text', 'a volar'), w(1500), ('text', 'despegar'), w(3000)],
                  'play': mouse_tour(10, 380)},
 'tiradora-cosmica': {'setup': [w(2500), ('click', '#stSkip'), w(800), ('click', '#playTxt'), w(1800), ('click', '#stSkip'), w(800), ('click', '#startBtn'), w(1500), ('click', '#stSkip'), w(600), ('click', '#startBtn'), w(3000)],
                      'play': [('drag', 300, 300, 520, 260, 600), ('tap', 520, 260), w(400), ('drag', 520, 260, 640, 330, 500), ('tap', 640, 330), w(400), ('drag', 640, 330, 420, 300, 500), ('tap', 420, 300), w(800)]},
 'constructor-cosmico': {'setup': [w(2500), ('click', '#btnPlay'), w(1800), ('click', '#stSkip'), w(1200), ('click', '#btnPlay'), w(1800), ('click', '#cineSkip'), w(1200), ('click', '#arGo'), w(1500), ('click', '#howBack'), w(800), ('click', '#cineSkip'), w(800), ('click', '#arGo'), w(1500)],
                         'play': [('drag', 330, 380, 480, 380, 500), ('drag', 480, 380, 630, 380, 500), w(500), ('click', '#btnTest'), w(3500)]},
 'paradon-cosmico': {'setup': [w(2500), ('text', 'Saltar'), w(800), ('text', 'A jugar'), w(1200), ('text', 'Saltar'), w(800), ('text', 'Entendido'), w(2500)],
                     'play': wiggle(n=7, ms=360)},
 'cosmic-guitar': {'setup': [w(2500), ('click', '#songs button, .song, li button'), w(4000)],
                   'play': [('taps', 480, 520, 12, 250)]},
 # ---------- ritmo ----------
 'martin-leyenda-del-rock': {'setup': [w(2500), ('click', '.song, #list li, .track'), w(4500)], 'play': [('press', 'KeyD'), w(300), ('press', 'KeyF'), w(300), ('press', 'KeyJ'), w(300), ('press', 'KeyK'), w(2500)]},
 'supernova-guitar': {'setup': [w(2500), ('click', '.song, #list li, .track'), w(4500)], 'play': [('press', 'KeyD'), w(300), ('press', 'KeyF'), w(300), ('press', 'KeyJ'), w(2800)]},
 # ---------- historias ----------
 'l-ultim-estiu': {'setup': [w(2500), ('text', 'Començar'), w(5000)], 'play': [w(400), ('hold', ['ArrowRight'], 900), ('hold', ['ArrowDown'], 700), ('hold', ['ArrowLeft'], 900), w(600)], 'poster': 0.15},
 # ---------- motor ----------
 'monster-smash': {'setup': [w(2500)], 'play': [('hold', ['ArrowRight'], 200), ('skip', 3500), ('hold', ['ArrowRight'], 3200), ('hold', ['ArrowRight', 'Space'], 900), ('hold', ['ArrowRight'], 1200)]},
 'moto-fury': {'setup': [w(2500), ('text', 'correr'), w(1500), ('text', 'entendido'), w(800), ('text', 'correr'), w(1000)], 'play': [('hold', ['ArrowRight'], 200), ('skip', 3500), ('hold', ['ArrowRight'], 2500), ('hold', ['ArrowRight', 'Space'], 700), ('hold', ['ArrowRight', 'KeyZ'], 1200), ('hold', ['ArrowRight'], 900)]},
 'turbo-kart-rally': {'setup': [w(2500), ('click', '#startBtn'), w(1500)], 'play': [('down', 'ArrowUp'), ('skip', 3000), ('hold', ['ArrowUp'], 900), ('hold', ['ArrowUp', 'ArrowLeft'], 900), ('hold', ['ArrowUp', 'ArrowRight'], 1200), ('hold', ['ArrowUp'], 900)], 'clip': 'end', 'poster': 0.8},
 'neon-coast': {'setup': [w(2500), ('text', 'empezar a conducir'), w(1500)], 'play': [('skip', 2500)]+wiggle(n=10, ms=400)},
 'aventura-porc': {'setup': [w(2500), ('text', 'Jugar! Nivel 1'), w(3500)], 'play': [('press', 'ArrowLeft'), w(900), ('press', 'ArrowUp'), w(900), ('press', 'ArrowRight'), w(900), ('press', 'ArrowRight'), w(900), ('press', 'ArrowDown'), w(900)]},
 # ---------- acción ----------
 'aura-battle': {'setup': [w(2500), ('text', 'Solo lo necesario'), w(500), ('text', 'Partida rápida'), w(2500), ('click', '#btnFight'), w(3500)], 'play': [('press', 'Digit1'), w(500), ('press', 'Digit3'), w(500), ('press', 'Digit2'), w(500), ('press', 'Digit5'), w(500), ('press', 'Space'), w(1500)]},
 'porrazo-party': {'setup': [w(2000), ('click', 'input'), ('type', 'Sasha'), ('click', '#userAdd'), w(1200), ('click', '#closeUser'), w(1200), ('click', '#goPlay'), w(1500), ('click', '#goFight'), w(1500), ('click', '#goRound'), w(3000)],
                   'play': [('hold', ['ArrowRight'], 700), ('press', 'KeyJ'), w(250), ('press', 'KeyK'), w(250), ('press', 'KeyJ'), w(400), ('hold', ['ArrowLeft'], 500), ('press', 'KeyK'), w(1200)]},
 'tiro-limpio': {'setup': [w(2500), ('text', 'Jugar'), w(1500), ('text', 'A por ellos'), w(2500)], 'play': [('drag', 480, 300, 600, 280, 800), ('tap', 600, 280), w(600), ('drag', 600, 280, 380, 320, 800), ('tap', 380, 320), w(1200)]},
 'cube-runner': {'setup': [w(2500), ('text', 'Empezar'), w(800)], 'play': wiggle(n=6, ms=380), 'poster': 0.5},
 'tower-stack': {'setup': [w(2500)], 'play': [('tap', 480, 400), w(2503), ('tap', 480, 400), w(2378), ('tap', 480, 400), w(2253), ('tap', 480, 400), w(2170), ('tap', 480, 400), w(2045), ('tap', 480, 400), w(900)], 'clip': 'end', 'poster': 0.97},
 # ---------- deporte ----------
 'anguera-superstars': {'setup': [w(3000), ('tap', 480, 300), w(1500), ('click', '#btnStart'), w(1500), ('click', '#btnLuPlay'), w(4000)], 'play': [('hold', ['ArrowRight'], 1200), ('hold', ['ArrowRight', 'ArrowUp'], 900), ('press', 'Space'), w(1500)]},
 'olimpiadas-de-la-granja': {'setup': [w(2500), ('text', 'Jugar'), w(1200), ('text', 'Rosa'), w(1500), ('text', 'Verano'), w(1500), ('text', 'Correr'), w(4500)], 'play': [('taps', 480, 400, 16, 180)]},
 # ---------- marca ----------
 'suo-shop-rush': {'setup': [w(2500), ('click', '#play'), w(3000)], 'play': [('mousehold', 600, 400, 1500), ('mousehold', 350, 300, 1500), w(800)]},
 'mnac-rush': {'setup': [w(2500), ('text', 'Comença'), w(3000)], 'play': [('mousehold', 600, 380, 1500), ('mousehold', 360, 300, 1500), w(800)]},
}
# ---------- relax: sin interfaz, solo la escena ----------
RELAX = {'relax-estanque-de-koi': [('taps', 480, 300, 3, 700)], 'relax-farolillos-del-lago': [('taps', 400, 400, 4, 500)],
         'relax-pompas-musicales': [('taps', 480, 300, 4, 500)], 'relax-isla-jardin': [('taps', 480, 330, 5, 400)],
         'relax-jardin-zen': [('drag', 250, 250, 700, 380, 1500)], 'relax-cristal-de-lluvia': [('drag', 300, 250, 650, 350, 1500)],
         'relax-hoguera-nocturna': [('tap', 480, 350), w(1500)], 'relax-bola-de-nieve': [('tap', 480, 300), w(2000)],
         'relax-pesca-al-atardecer': [('tap', 480, 380), w(2500)], 'relax-arrecife-de-coral': [('drag', 400, 300, 600, 320, 1500)],
         'relax-velero-entre-islas': [('mousehold', 700, 300, 1500)], 'relax-orilla-y-marea': [w(2500)],
         'relax-vuelo-del-amanecer': [('drag', 480, 300, 560, 260, 1500)], 'relax-aurora-boreal': [('taps', 480, 200, 3, 600)],
         'relax-orbitas-musicales': [('taps', 560, 300, 3, 600), w(1000)], 'relax-constelaciones': [('drag', 300, 200, 600, 260, 1200)],
         'relax-cometa-al-viento': [('drag', 400, 300, 600, 250, 1500)], 'relax-rana-y-luciernagas': [('taps', 560, 360, 3, 800)]}
for k, v in RELAX.items():
    STEPS[k] = {'setup': [w(3500), HIDE_RELAX, w(300)], 'play': v + [w(1200)], 'skip': 0.2}
# ---------- CatQuiz: empezar y jugar un poco ----------
for k, start, play in [
    ('catquiz-com-es-diu-en-catala', 'Juga', [w(1200), ('click', '.opt, .option, button.ans'), w(1800)]),
    ('catquiz-l-intrus', 'Juga', [w(1200), ('click', '.opt, .option, button.ans'), w(1800)]),
    ('catquiz-motle', 'aleatòria', [('type', 'CASAL'), ('press', 'Enter'), w(900), ('type', 'TERRA'), ('press', 'Enter'), w(1500)]),
    ('catquiz-esquiva', 'Comença', wiggle(n=8, ms=380)),
    ('catquiz-accents', 'Juga', [w(1200), ('click', '.opt, .option, button.ans'), w(1800)]),
    ('catquiz-penjat-3d', 'Animals', [('type', 'AEOSR'), w(1800)]),
    ('catquiz-anagrama', 'Comença', [w(800), ('type', 'A'), w(500), ('type', 'E'), w(1800)]),
    ('catquiz-caca-estrelles', 'Comença', wiggle(n=8, ms=400)),
    ('catquiz-sopa-de-lletres', 'Juga', [('drag', 450, 520, 560, 520, 900), w(1500)]),
    ('catquiz-lletres-perdudes', 'Juga', [w(1000), ('type', 'A'), w(1500)]),
]:
    STEPS[k] = {'setup': [w(2500), ('text', start), w(1200)], 'play': play}
