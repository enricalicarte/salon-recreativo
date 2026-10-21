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
 'paradon-cosmico': {'setup': [w(2500), ('text', 'Saltar'), w(800), ('text', 'A jugar'), w(1200), ('text', 'Saltar'), w(800), ('text', 'Entendido'), ('js', 'window.__auto=true'), w(200)],
                     'intro': [('skip', 6000), ('text', 'Jugar otra vez'), ('js', 'window.__auto=true'), ('skip', 2500)], 'play': [('wait', 3000)]},
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
 'turbo-kart-rally': {'setup': [w(2500), ('click', '#startBtn'), w(1500)], 'play': [('down', 'ArrowUp'), w(3500), w(3300), ('up', 'ArrowUp')], 'clip': 'end', 'poster': 0.85},
 'neon-coast': {'setup': [w(2500), ('text', 'empezar a conducir'), w(1500)], 'play': [('skip', 2500)]+wiggle(n=10, ms=400)},
 'aventura-porc': {'setup': [w(2500), ('text', 'Jugar! Nivel 1'), w(9000)], 'play': [('press', 'ArrowLeft'), w(1200), ('press', 'ArrowUp'), w(1200), ('press', 'ArrowRight'), w(1100), ('press', 'ArrowRight'), w(1200), ('press', 'ArrowDown'), w(1200), ('press', 'ArrowLeft'), w(1200), ('press', 'ArrowUp'), w(1200), ('press', 'ArrowLeft'), w(1200), ('press', 'ArrowRight'), w(1200), ('press', 'ArrowUp'), w(1200)], 'clip': 'end', 'poster': 0.92},
 'aura-battle': {'setup': [w(2500), ('text', 'Solo lo necesario'), w(500), ('text', 'Partida rápida'), w(2500), ('click', '#btnFight'), w(3500)], 'play': [('press', 'Digit1'), w(500), ('press', 'Digit3'), w(500), ('press', 'Digit2'), w(500), ('press', 'Digit5'), w(500), ('press', 'Space'), w(1500)]},
 'porrazo-party': {'setup': [w(2000), ('click', 'input'), ('type', 'Sasha'), ('click', '#userAdd'), w(1200), ('click', '#closeUser'), w(1200), ('click', '#goPlay'), w(1500), ('click', '#goFight'), w(1500), ('click', '#goRound'), w(3000)],
                   'play': [('hold', ['ArrowRight'], 700), ('press', 'KeyJ'), w(250), ('press', 'KeyK'), w(250), ('press', 'KeyJ'), w(400), ('hold', ['ArrowLeft'], 500), ('press', 'KeyK'), w(1200)]},
 'tiro-limpio': {'setup': [w(2500), ('text', 'Jugar'), w(1500), ('text', 'A por ellos'), w(2500)], 'play': [('drag', 480, 300, 600, 280, 800), ('tap', 600, 280), w(600), ('drag', 600, 280, 380, 320, 800), ('tap', 380, 320), w(1200)]},
 'cube-runner': {'setup': [w(2500), ('text', 'Empezar'), w(800)], 'play': wiggle(n=6, ms=380), 'poster': 0.5},
 'tower-stack': {'setup': [w(2500)], 'play': [('tap', 480, 400), w(2503), ('tap', 480, 400), w(2378), ('tap', 480, 400), w(2253), ('tap', 480, 400), w(2170), ('tap', 480, 400), w(2045), ('tap', 480, 400), w(900)], 'clip': 'end', 'poster': 0.97},
 # ---------- deporte ----------
 'anguera-superstars': {'setup': [w(3000), ('tap', 480, 300), w(1500), ('click', '#btnStart'), w(1500), ('click', '#btnLuPlay'), w(4000)], 'play': [('hold', ['ArrowRight'], 1200), ('hold', ['ArrowRight', 'ArrowUp'], 900), ('press', 'Space'), w(1500)]},
 'olimpiadas-de-la-granja': {'setup': [w(2500), ('text', 'Jugar'), w(1200), ('text', 'Rosa'), w(1500), ('text', 'Verano'), w(1500), ('text', 'Correr'), w(4500)], 'play': [('taps', 480, 400, 16, 180)]},
 'ola-perfecta': {'setup': [w(2500), ('js', 'window.__surf.start(4);window.__surf.god=true')], 'intro': [('skip', 11000), ('press', 'Space'), ('skip', 3000)], 'play': [('hold', ['ArrowUp'], 900), ('press', 'Space'), ('hold', ['ArrowRight'], 560), w(1000), ('hold', ['ArrowDown'], 1100), w(500), ('press', 'Space'), ('hold', ['ArrowLeft'], 560), w(1000), ('hold', ['ArrowLeft'], 900), ('hold', ['ArrowUp'], 700), w(400)], 'poster': 0.8, 'clip': 'end'},
 'el-gran-salto': {'setup': [w(2500), ('click', '#playBtn'), w(800), ('click', '#sagaGo'), w(800), ('click', '.tc'), w(600), ('js', "(function(){\n const $=id=>document.getElementById(id),K=(t,c)=>window.dispatchEvent(new KeyboardEvent(t,{code:c,key:c===' '?' ':c,bubbles:true}));\n const tap=c=>{K('keydown',c);setTimeout(()=>K('keyup',c),60);};\n let flipOn=false,twOn=false,last=0;\n setInterval(()=>{\n  const now=performance.now();\n  if($('result').classList.contains('show')){if(now-last>900){last=now;$('nextBtn').click();}return;}\n  if($('final').classList.contains('show')){if(now-last>900){last=now;$('againBtn').click();}return;}\n  const pr=$('prompt').textContent||'';\n  if(/lanzarte/.test(pr)&&now-last>500){last=now;tap('Space');return;}\n  const tm=$('timing');\n  if(tm&&tm.style.opacity=='1'){const l=parseFloat($('tmark').style.left)||0;if(l>=83&&now-last>300){last=now;tap('Space');}}\n  if(/AHORA/.test(pr)&&now-last>300){last=now;tap('Space');}\n  const cF=$('cF');\n  if(cF&&cF.style.opacity=='1'){\n    const v=parseFloat((cF.querySelector('b')||{}).textContent?.replace(',','.')||'0'),tg=parseFloat((cF.querySelector('b').textContent.split('/')[1]||'1'));\n    const want=v<tg-0.12;\n    if(want&&!flipOn){flipOn=true;K('keydown','KeyZ');}\n    if(!want&&flipOn){flipOn=false;K('keyup','KeyZ');}\n    const cT=$('cT'),b2=cT&&cT.querySelector('b');\n    if(b2){const v2=parseFloat(b2.textContent.replace(',','.'))||0,t2=parseFloat(b2.textContent.split('/')[1]||'0');const w2=v2<t2-0.12;\n      if(w2&&!twOn){twOn=true;K('keydown','KeyX');} if(!w2&&twOn){twOn=false;K('keyup','KeyX');}}\n  } else if(flipOn||twOn){flipOn=twOn=false;K('keyup','KeyZ');K('keyup','KeyX');}\n },20);\n})();\n")], 'play': [('wait', 4000)], 'poster': 0.45},
 'la-gran-pirueta': {'setup': [w(2500), ('click', '#playBtn'), w(800), ('click', '#sagaGo'), w(800), ('click', '.tc'), w(600), ('js', "(function(){\n const $=id=>document.getElementById(id),K=(t,c)=>window.dispatchEvent(new KeyboardEvent(t,{code:c,key:c===' '?' ':c,bubbles:true}));\n const tap=c=>{K('keydown',c);setTimeout(()=>K('keyup',c),60);};\n let flipOn=false,twOn=false,last=0;\n setInterval(()=>{\n  const now=performance.now();\n  if($('result').classList.contains('show')){if(now-last>900){last=now;$('nextBtn').click();}return;}\n  if($('final').classList.contains('show')){if(now-last>900){last=now;$('againBtn').click();}return;}\n  const pr=$('prompt').textContent||'';\n  if(/lanzarte/.test(pr)&&now-last>500){last=now;tap('Space');return;}\n  const tm=$('timing');\n  if(tm&&tm.style.opacity=='1'){const l=parseFloat($('tmark').style.left)||0;if(l>=83&&now-last>300){last=now;tap('Space');}}\n  if(/AHORA/.test(pr)&&now-last>300){last=now;tap('Space');}\n  const cF=$('cF');\n  if(cF&&cF.style.opacity=='1'){\n    const v=parseFloat((cF.querySelector('b')||{}).textContent?.replace(',','.')||'0'),tg=parseFloat((cF.querySelector('b').textContent.split('/')[1]||'1'));\n    const want=v<tg-0.12;\n    if(want&&!flipOn){flipOn=true;K('keydown','KeyZ');}\n    if(!want&&flipOn){flipOn=false;K('keyup','KeyZ');}\n    const cT=$('cT'),b2=cT&&cT.querySelector('b');\n    if(b2){const v2=parseFloat(b2.textContent.replace(',','.'))||0,t2=parseFloat(b2.textContent.split('/')[1]||'0');const w2=v2<t2-0.12;\n      if(w2&&!twOn){twOn=true;K('keydown','KeyX');} if(!w2&&twOn){twOn=false;K('keyup','KeyX');}}\n  } else if(flipOn||twOn){flipOn=twOn=false;K('keyup','KeyZ');K('keyup','KeyX');}\n },20);\n})();\n")], 'play': [('wait', 4000)], 'poster': 0.45},
 'el-gran-descenso': {'setup': [w(2500), ('click', '#playBtn'), w(800), ('click', '#sagaGo'), w(800), ('click', '.tc'), w(1500), ('js', "(function(){\n const $=id=>document.getElementById(id),K=(t,c)=>window.dispatchEvent(new KeyboardEvent(t,{code:c,key:c,bubbles:true}));\n let side=0,last=0,hold='';\n const setHold=h=>{if(h===hold)return;if(hold)K('keyup',hold);hold=h;if(h)K('keydown',h);};\n setInterval(()=>{\n  const now=performance.now();\n  if($('result').classList.contains('show')){setHold('');if(now-last>900){last=now;$('nextBtn').click();}return;}\n  if($('final').classList.contains('show')){setHold('');if(now-last>900){last=now;$('againBtn').click();}return;}\n  if($('pushw').style.opacity=='1'){ if(now-last>70){last=now;const c=side?'ArrowRight':'ArrowLeft';side^=1;K('keydown',c);setTimeout(()=>K('keyup',c),30);} return;}\n  if($('lane').classList.contains('on')){\n    const r=parseFloat($('lref').style.left)||50,m=parseFloat($('lme').style.left)||50;\n    setHold(m<r-4?'ArrowRight':m>r+4?'ArrowLeft':'');\n  } else setHold('');\n },20);\n})();\n")], 'intro': [('skip', 3500)], 'play': [('wait', 4000)], 'poster': 0.5},
 'alas-de-acero': {'setup': [w(3000), ('click', '#bStart'), w(800), ('click', '#bGo'), w(600)], 'intro': [('skip', 2500)], 'play': [('hold', ['Space'], 1800), ('hold', ['Space', 'ArrowLeft'], 900), ('hold', ['Space'], 1600), ('press', 'KeyE'), w(900), ('hold', ['Space', 'ArrowRight'], 900), ('hold', ['Space'], 1800)], 'poster': 0.5},
 'fifa-11-kids': {'setup': [w(3000), ('click', '#go'), w(1500), ('click', '#mainBtn'), w(300)], 'intro': [('skip', 1500)], 'play': [('wait', 3000)], 'poster': 0.5},
 'tecnica-individual': {'setup': [w(3000), ('click', '#go'), w(1500), ('click', '#mainBtn'), w(300)], 'intro': [('skip', 1500)], 'play': [('wait', 3000)], 'poster': 0.5},
 'plan-de-fuerza': {'setup': [w(3000), ('click', '#go'), w(1500), ('click', '#mainBtn'), w(300)], 'intro': [('skip', 1500)], 'play': [('wait', 3000)], 'poster': 0.5},
 'stu-el-especialista': {'setup': [w(3000), ('click', '#lvRow > :nth-child(6)'), w(300), ('click', '#vehRow > :nth-child(3)'), w(300), ('click', '#play'), w(500)], 'intro': [('skip', 300)], 'play': [('hold', ['Space'], 3200), ('press', 'KeyX'), ('hold', ['Space'], 1500), ('hold', ['Space','KeyD'], 1200), ('hold', ['Space','KeyA'], 1000), ('hold', ['Space'], 1500), w(1500)], 'poster': 0.45},
 'looping-loco': {'setup': [w(3000), ('text', 'JUGAR'), w(1200), ('text', 'PARQUE NEÓN'), w(800)], 'intro': [('skip', 1000)], 'play': [('hold', ['Space'], 2500), w(600), ('hold', ['Space'], 2500), w(600), ('hold', ['Space'], 2500)], 'extra': 120, 'clip': 'end', 'poster': 0.7},
 'lluvia-loca': {'url': 'tools/capture/lluvia-loca_cap.html?demo&hq&np=2&modo=duelo', 'setup': [w(1500), ('click', '#btn'), w(200)], 'intro': [('skip', 12000)], 'play': [('wait', 3000)], 'poster': 0.55},
 'muro-loco': {'url': 'juegos/muro-loco/index.html?demo&hq&np=2&modo=doble', 'setup': [w(1500), ('click', '#btn'), w(200)], 'intro': [('skip', 3600)], 'play': [('wait', 3000)], 'extra': 140, 'clip': 'end', 'poster': 0.5},
 'portero-loco': {'url': 'juegos/portero-loco/index.html?demo&hq', 'setup': [w(1500), ('click', '#btn'), w(200)], 'intro': [('skip', 4500)], 'play': [('wait', 3000)], 'extra': 60, 'clip': 'end', 'poster': 0.5},
 'balon-loco': {'url': 'juegos/balon-loco/index.html?demo&hq&modo=toques', 'setup': [w(1500), ('click', '#btn'), w(200)], 'intro': [('skip', 4200)], 'play': [('wait', 3000)], 'poster': 0.5},
 'crucigiro': {'vp': {'width': 396, 'height': 704}, 'portrait': True, 'setup': [w(2500), ('text', 'JUGAR'), w(1500)], 'intro': [('skip', 300)], 'play': [('spell','ALGO'), w(700), ('spell','OLA'), w(700), ('spell','LAGO'), w(700), ('spell','GOL'), w(2200), ('text','SIGUIENTE'), w(1500), ('spell','AYER'), w(700), ('spell','REY'), w(700), ('spell','ERA'), w(2000)], 'poster': 0.35},
 'car-revamp': {'setup': [w(2500), ('tap', 480, 480), w(300), ('js', open(__import__('os').path.dirname(__file__)+'/cr_auto.js').read())], 'intro': [('skip', 44500)], 'play': [('wait', 3000)], 'poster': 0.75},
 'bloques-neon': {'setup': [w(2000), ('js', 'startLevel(7);closeModal()'), w(300), ('js', open(__import__('os').path.dirname(__file__)+'/bn_auto.js').read())], 'intro': [('skip', 300)], 'play': [('wait', 3000)], 'poster': 0.5},
 'ciudadela-de-arena': {'url': 'juegos/ciudadela-de-arena/index.html?debug', 'setup': [w(3500), ('js', '__t.start(4)'), w(500), ('js', '(()=>{const g=__t.LV.guards.find(g=>g.type==="B");__t.tp(g.x-3.5,g.y);})()'), w(200)], 'intro': [('skip', 600)], 'play': [('press','KeyJ'), w(500), ('press','KeyK'), w(500), ('press','KeyK'), w(450), ('press','KeyJ'), w(600), ('hold',['ArrowRight'],120), ('press','KeyK'), w(500), ('press','KeyJ'), w(550)], 'poster': 0.3},
 'halfpipe': {'setup': [w(3000), ('click', '#bStart'), w(800), ('js', '__hp.SAVE.unlocked=8;__hp.startLevel(4)'), w(600), ('js', open(__import__('os').path.dirname(__file__)+'/hp_auto.js').read())], 'intro': [('skip', 2000)], 'play': [('wait', 3000)], 'extra': 110, 'clip': 'end', 'poster': 0.6},
 'drop-in': {'setup': [w(3000), ('click', '#bPlay'), w(300)], 'play': [('hold', ['KeyW'], 1600), ('press', 'Space'), w(250), ('press', 'Space'), w(900), ('hold', ['KeyW', 'KeyD'], 700), ('hold', ['KeyW'], 900), ('down', 'Space'), w(300), ('up', 'Space'), ('hold', ['KeyA', 'KeyG'], 700), w(500), ('hold', ['KeyW', 'KeyA'], 800), ('press', 'Space'), w(200), ('press', 'KeyL'), w(900)], 'poster': 0.45},
 # ---------- marca ----------
 'suo-shop-rush': {'setup': [w(2500), ('click', '#play'), w(3000)], 'play': [('tap', 640, 420), w(1500), ('tap', 330, 380), w(1500), ('tap', 600, 230), w(1500), ('tap', 420, 460), w(1500), ('tap', 700, 300), w(1400)], 'clip': 'end', 'poster': 0.7},
 'mnac-rush': {'setup': [w(2500), ('text', 'Comença'), w(3000)], 'play': [('tap', 640, 420), w(1500), ('tap', 330, 380), w(1500), ('tap', 600, 230), w(1500), ('tap', 420, 460), w(1500), ('tap', 700, 300), w(1400)], 'clip': 'end', 'poster': 0.7},
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
    ('catquiz-motle', 'aleatòria', [('type', 'CASAL'), ('press', 'Enter'), w(1200), ('type', 'TERRA'), ('press', 'Enter'), w(1200), ('type', 'MOTOR'), ('press', 'Enter'), w(1200), ('type', 'PLATA'), ('press', 'Enter'), w(2000)]),
    ('catquiz-esquiva', 'Comença', wiggle(n=8, ms=380)),
    ('catquiz-accents', 'Juga', [w(1200), ('click', '.opt, .option, button.ans'), w(1800)]),
    ('catquiz-penjat-3d', 'Animals', [('type', 'AEOSR'), w(1800)]),
    ('catquiz-anagrama', 'Comença', [w(800), ('type', 'A'), w(500), ('type', 'E'), w(1800)]),
    ('catquiz-caca-estrelles', 'Comença', wiggle(n=8, ms=400)),
    ('catquiz-sopa-de-lletres', 'Juga', [('drag', 450, 520, 560, 520, 900), w(1500)]),
    ('catquiz-lletres-perdudes', 'Juga', [w(1000), ('type', 'A'), w(1500)]),
]:
    STEPS[k] = {'setup': [w(2500), ('text', start), w(1200)], 'play': play}
# CatQuiz (versión Bloques Neón): cada juego se juega solo con ?demo
CQ_FILES = {'catquiz-com-es-diu-en-catala': 'catala', 'catquiz-l-intrus': 'intrus', 'catquiz-motle': 'motle', 'catquiz-esquiva': 'esquiva',
            'catquiz-accents': 'accents', 'catquiz-penjat-3d': 'penjat', 'catquiz-anagrama': 'anagrama', 'catquiz-caca-estrelles': 'estrelles',
            'catquiz-sopa-de-lletres': 'sopa', 'catquiz-lletres-perdudes': 'perdudes', 'catquiz-barbarismes': 'barbarismes', 'catquiz-quiz-de-futbol': 'futbol'}
for k, f in CQ_FILES.items():
    STEPS[k] = {'url': f'juegos/catquiz/jocs/{f}.html?demo', 'setup': [w(1500)], 'intro': [('skip', 1500)], 'play': [('wait', 3000)], 'poster': 0.6}
# ---------- nuevos: Hotel Miramar y Cabina ----------
STEPS['hotel-miramar'] = {'setup': [w(2500), ('click', '#go'), w(2500), ('tap', 480, 300), w(1800)] + [x for _ in range(6) for x in (('tap', 480, 250), w(900), ('tap', 480, 250), w(700))] + [w(1500)],
                          'play': [('tap', 580, 455), w(2200), ('tap', 400, 460), w(2000), ('tap', 480, 432), w(1500)], 'poster': 0.4}
STEPS['cabina'] = {'setup': [w(2500), ('click', '#tourskip'), w(500), ('click', '#tabs button[data-view="cr"]'), w(800), ('click', '#crrand'), w(600), ('click', '#crplay'), w(1500)],
                   'play': [w(4000)], 'poster': 0.5}
