#!/usr/bin/env python3
"""Fitxes dels jocs de CatQuiz al Salón (català + castellà). Actualitza tools/games.json, tools/source.html (const GAMES i NEW),
tools/i18n.py (ES_CQ) i tools/seo_copy.py. Uso: python3 tools/catquiz_fitxes.py"""
import os, json, re
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda c, e: ["#1b1448", "#3b2a8f", c, e]
# id, slug, joc, nom, kw (ca), descripció (ca), etiquetes, color, emoji, kw (es), descripció (es)
CQ = [
 ('cq_motle', 'catquiz-motle', 'motle', 'Motle', "Wordle en català",
  "El Wordle en català: endevina la paraula de cinc lletres en sis intents. Verd, al lloc correcte; groc, hi és però en un altre lloc. Amb paraula del dia i partides aleatòries.",
  ['Wordle', 'Paraula del dia', 'Català'], '#4ee06a', '🟩', "Wordle en catalán",
  "El Wordle en catalán: adivina la palabra de cinco letras en seis intentos. Verde, en su sitio; amarillo, está pero en otro lugar. Con palabra del día y partidas aleatorias."),
 ('cq_roda', 'catquiz-roda-de-paraules', 'roda', 'Roda de paraules', "joc de paraules en català",
  "Joc de paraules en català tipus mots encreuats: uneix les lletres de la roda amb el dit per formar les paraules que falten. 300 nivells, cada cop amb paraules més llargues.",
  ['Mots encreuats', 'Paraules', 'Català'], '#4ee06a', '🔤', "juego de palabras en catalán",
  "Juego de palabras en catalán tipo crucigrama: une las letras de la rueda con el dedo para formar las palabras que faltan. 300 niveles, cada vez con palabras más largas."),
 ('cq_pronoms', 'catquiz-pronoms-febles', 'pronoms', 'Pronoms febles', "joc de pronoms febles",
  "Joc de pronoms febles en català: el, la, ho, en, hi, li i les combinacions més traïdores. Tria el pronom correcte en cada frase, en deu nivells de fàcil a difícil.",
  ['Pronoms febles', 'Gramàtica', 'Català'], '#38e5ff', '🧩', "juego de pronombres débiles en catalán",
  "Juego de pronombres débiles en catalán: el, la, ho, en, hi, li y las combinaciones más traicioneras. Elige el pronombre correcto en cada frase, en diez niveles de fácil a difícil."),
 ('cq_barbarismes', 'catquiz-barbarismes', 'barbarismes', 'Barbarismes', "joc de barbarismes en català",
  "Joc de barbarismes en català: completa la frase amb la forma correcta. Calcs, formes deformades i expressions que sonen bé però no ho són, en deu nivells de dificultat creixent.",
  ['Barbarismes', 'Frases', 'Català'], '#ff4fa3', '🚫', "juego de barbarismos en catalán",
  "Juego de barbarismos en catalán: completa la frase con la forma correcta. Calcos, formas deformadas y expresiones que suenan bien pero no lo son, en diez niveles de dificultad creciente."),
 ('cq_catala', 'catquiz-com-es-diu-en-catala', 'catala', 'Com es diu en català?', "joc de castellanismes",
  "Joc de castellanismes en català: et diem una paraula que es diu malament i tries la catalana correcta entre tres. Més de 700 paraules en deu nivells.",
  ['Castellanismes', 'Vocabulari', 'Català'], '#ff4fa3', '💬', "juego de castellanismos en catalán",
  "Juego de castellanismos en catalán: te damos una palabra mal dicha y eliges la catalana correcta entre tres. Más de 700 palabras en diez niveles."),
 ('cq_accents', 'catquiz-accents', 'accents', 'Accents!', "joc d'accents en català",
  "Joc d'accents en català: una paraula, tres maneres d'escriure-la i només una és correcta. Posa l'accent on toca, o no en posis, en deu nivells de fàcil a difícil.",
  ['Accents', 'Ortografia', 'Català'], '#38e5ff', '✍️', "juego de acentos en catalán",
  "Juego de acentos en catalán: una palabra, tres formas de escribirla y solo una es correcta. Pon el acento donde toca, o no lo pongas, en diez niveles de fácil a difícil."),
 ('cq_penjat', 'catquiz-penjat-3d', 'penjat', 'Penjat 3D', "penjat en català",
  "El joc del penjat en català i en 3D: tria una categoria i endevina la paraula abans que es munti el ninot. Vuit errors i s'acaba; la pista et dona una lletra.",
  ['Penjat', 'Categories', 'Català'], '#4ee06a', '🪢', "ahorcado en catalán",
  "El juego del ahorcado en catalán y en 3D: elige una categoría y adivina la palabra antes de que se monte el muñeco. Ocho errores y se acaba; la pista te da una letra."),
 ('cq_anagrama', 'catquiz-anagrama', 'anagrama', 'Anagrama', "anagrames en català",
  "Joc d'anagrames en català: les lletres cauen barrejades i les has d'ordenar per formar la paraula. 60 segons, 5 més per encert, i paraules cada cop més llargues.",
  ['Anagrames', 'Contrarellotge', 'Català'], '#4ee06a', '🔀', "anagramas en catalán",
  "Juego de anagramas en catalán: las letras caen desordenadas y tienes que ordenarlas para formar la palabra. 60 segundos, 5 más por acierto, y palabras cada vez más largas."),
 ('cq_intrus', 'catquiz-l-intrus', 'intrus', "L'intrús", "joc de l'intrús en català",
  "Joc de l'intrús en català: quatre paraules, tres de la mateixa categoria i una que no hi encaixa. Troba-la abans que s'acabi el temps i suma punts dobles amb la ratxa.",
  ['Categories', 'Vocabulari', 'Català'], '#ff4fa3', '🕵️', "juego del intruso en catalán",
  "Juego del intruso en catalán: cuatro palabras, tres de la misma categoría y una que no encaja. Encuéntrala antes de que se acabe el tiempo y suma puntos dobles con la racha."),
 ('cq_perdudes', 'catquiz-lletres-perdudes', 'perdudes', 'Lletres perdudes', "joc de lletres en català",
  "Joc de lletres en català: a la paraula li falten lletres i les has d'escriure en ordre. Tres errors i es revela; deu nivells, cada cop amb més forats.",
  ['Ortografia', 'Lletres', 'Català'], '#38e5ff', '❓', "juego de letras en catalán",
  "Juego de letras en catalán: a la palabra le faltan letras y tienes que escribirlas en orden. Tres errores y se revela; diez niveles, cada vez con más huecos."),
 ('cq_sopa', 'catquiz-sopa-de-lletres', 'sopa', 'Sopa de lletres', "sopa de lletres en català",
  "Sopa de lletres en català: sis paraules d'una categoria amagades en una graella de 8×8, en horitzontal, vertical o diagonal. Arrossega el dit i troba-les totes.",
  ['Sopa de lletres', 'Categories', 'Català'], '#4ee06a', '🔎', "sopa de letras en catalán",
  "Sopa de letras en catalán: seis palabras de una categoría escondidas en una cuadrícula de 8×8, en horizontal, vertical o diagonal. Arrastra el dedo y encuéntralas todas."),
 ('cq_futbol', 'catquiz-quiz-de-futbol', 'futbol', 'Quiz de futbol', "quiz de futbol català",
  "Quant saps de futbol català? Deu nivells de preguntes sobre el Barça, l'Espanyol i el Girona: trivia, «qui és?» per pistes, verdader o fals i «qui va néixer abans?».",
  ['Futbol', 'Trivia', 'Català'], '#ffd23f', '⚽', "quiz de fútbol catalán",
  "¿Cuánto sabes de fútbol catalán? Diez niveles de preguntas sobre el Barça, el Espanyol y el Girona: trivia, «¿quién es?» por pistas, verdadero o falso y «¿quién nació antes?». En catalán."),
 ('cq_esportistes', 'catquiz-quiz-d-esportistes', 'esportistes', "Quiz d'esportistes", "quiz d'esportistes catalans",
  "Quant saps dels esportistes catalans? Setanta campions de vint-i-tres esports: endevina qui és per les pistes, de quin esport és i qui va néixer abans, en deu nivells.",
  ['Esport', 'Trivia', 'Català'], '#ffd23f', '🏅', "quiz de deportistas catalanes",
  "¿Cuánto sabes de los deportistas catalanes? Setenta campeones de veintitrés deportes: adivina quién es por las pistas, de qué deporte es y quién nació antes, en diez niveles. En catalán."),
]
NOUS = ['cq_roda', 'cq_pronoms', 'cq_esportistes']
FORA = ['cq_esquiva', 'cq_estrelles']

fitxa = lambda x: {"id": x[0], "slug": x[1], "kw": x[4], "cat": "catquiz", "name": x[3], "blurb": x[5], "tags": x[6], "pal": P(x[7], x[8]), "play": f"juegos/catquiz/jocs/{x[2]}.html"}

# games.json: substitueix el bloc de CatQuiz (mateixa posició)
gp = os.path.join(root, 'tools/games.json'); D = json.load(open(gp, encoding='utf-8'))
i0 = next(i for i, g in enumerate(D['GAMES']) if g['cat'] == 'catquiz')
D['GAMES'] = [g for g in D['GAMES'] if g['cat'] != 'catquiz']; D['GAMES'][i0:i0] = [fitxa(x) for x in CQ]
json.dump(D, open(gp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# source.html: línies {id:"cq_...} de const GAMES
sp = os.path.join(root, 'tools/source.html'); s = open(sp, encoding='utf-8').read()
lin = re.findall(r'^  \{id:"cq_[^\n]*\n', s, re.M); a = s.index(lin[0]); b = s.index(lin[-1]) + len(lin[-1])
js = lambda x: '  {' + f'id:{json.dumps(x[0])},kw:{json.dumps(x[4], ensure_ascii=False)},cat:\'catquiz\',name:{json.dumps(x[3], ensure_ascii=False)},blurb:{json.dumps(x[5], ensure_ascii=False)},tags:{json.dumps(x[6], ensure_ascii=False)},pal:{json.dumps(P(x[7], x[8]), ensure_ascii=False)},play:"juegos/catquiz/jocs/{x[2]}.html"' + '},\n'
s = s[:a] + ''.join(js(x) for x in CQ) + s[b:]
m = re.search(r"const NEW=new Set\(\[([^\]]*)\]\)", s); ids = [i.strip().strip("'") for i in m.group(1).split(',') if i.strip()]
ids = [i for i in ids if i not in FORA and i not in NOUS]; ids = NOUS + ids
s = s[:m.start()] + "const NEW=new Set([" + ','.join(f"'{i}'" for i in ids) + "])" + s[m.end():]
for f in FORA: s = re.sub(r"'" + f + r"',?", '', s)
open(sp, 'w', encoding='utf-8').write(s)

# i18n.py: ES_CQ
ip = os.path.join(root, 'tools/i18n.py'); t = open(ip, encoding='utf-8').read()
a = t.index('ES_CQ = {'); b = t.index('\n}', a) + 2
t = t[:a] + 'ES_CQ = {\n' + ''.join(f" {json.dumps(x[0])}: dict(kw={json.dumps(x[9], ensure_ascii=False)}, blurb={json.dumps(x[10], ensure_ascii=False)}),\n" for x in CQ) + '}' + t[b:]
open(ip, 'w', encoding='utf-8').write(t)

# seo_copy.py: entrades catalanes
cp = os.path.join(root, 'tools/seo_copy.py'); c = open(cp, encoding='utf-8').read()
c = re.sub(r"^'cq_[^\n]*\n", '', c, flags=re.M)
c = c.replace('# CatQuiz (català)\n', '# CatQuiz (català)\n' + ''.join(f"{json.dumps(x[0])}:({json.dumps(x[4], ensure_ascii=False)},{json.dumps(x[5], ensure_ascii=False)},{json.dumps(x[6], ensure_ascii=False)}),\n" for x in CQ))
open(cp, 'w', encoding='utf-8').write(c)
print(len(CQ), 'fitxes de CatQuiz')
