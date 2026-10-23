#!/usr/bin/env python3
"""Genera juegos/catquiz/jocs/party-dades.js amb les preguntes de CatQuiz Party,
copiades tal qual dels jocs de CatQuiz (una sola font de veritat: si es corregeix un joc, es torna a generar)."""
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = os.path.join(R, 'juegos/catquiz/jocs')

def lit(src, name):
    m = re.search(r'(?:const|let|var)\s+' + name + r'\s*=\s*(new Set\()?', src) or re.search(r'\b' + name + r'\s*=\s*(new Set\()?', src)
    i = src.index('[' if src[m.end():m.end()+1] == '[' else '{', m.end())
    op = src[i]; cl = ']' if op == '[' else '}'; d = 0; q = None; k = i
    while True:
        c = src[k]
        if q:
            if c == '\\': k += 2; continue
            if c == q: q = None
        elif c in '"\'': q = c
        elif c == op: d += 1
        elif c == cl:
            d -= 1
            if d == 0: break
        k += 1
    return json.loads(src[i:k+1])

rd = lambda f: open(os.path.join(J, f), encoding='utf-8').read()
out = {
    'barb': lit(rd('barbarismes.html'), 'BARB'),
    'pron': lit(rd('pronoms.html'), 'BARB'),
    'par': lit(rd('catala.html'), 'PARELLS'),
    'acc': lit(rd('accents.html'), 'ACCENTS'),
    'val': lit(rd('accents.html'), 'VALIDES'),
    'fut': lit(rd('futbol.html'), 'FUT'),
    'esp': lit(rd('esportistes.html'), 'FUT'),
    'cas': lit(rd('castells.html'), 'FUT'),
}
for k in ('fut', 'esp', 'cas'): out[k].pop('D', None); out[k].pop('C', None)
js = '/* Generat per tools/catquiz_party.py a partir dels jocs de CatQuiz: no editar a mà */\nwindow.PARTY_DADES=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
open(os.path.join(J, 'party-dades.js'), 'w', encoding='utf-8').write(js)
print('party-dades.js', len(js) // 1024, 'KB ·', {k: (len(v) if isinstance(v, list) else {kk: len(vv) for kk, vv in v.items()}) for k, v in out.items()})
