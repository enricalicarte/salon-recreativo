#!/usr/bin/env python3
"""Copia els jocs de CatQuiz (repo enricalicarte/catquiz) a juegos/catquiz/.
Uso: python3 tools/catquiz_sync.py /ruta/al/repo/catquiz"""
import os, sys, shutil, glob
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1]; dst = os.path.join(root, 'juegos', 'catquiz')
os.makedirs(os.path.join(dst, 'jocs'), exist_ok=True)
nous = {os.path.basename(f) for f in glob.glob(os.path.join(src, 'jocs', '*.html'))}
for f in glob.glob(os.path.join(dst, 'jocs', '*.html')):
    if os.path.basename(f) not in nous: os.remove(f); print('fora', os.path.basename(f))
for f in sorted(nous): shutil.copy(os.path.join(src, 'jocs', f), os.path.join(dst, 'jocs', f))
shutil.copy(os.path.join(src, 'comu.js'), os.path.join(dst, 'comu.js'))
os.makedirs(os.path.join(dst, 'img'), exist_ok=True); shutil.copy(os.path.join(src, 'img', 'favicon.svg'), os.path.join(dst, 'img', 'favicon.svg'))
for f in ('index.html', 'demo.html', 'video.html'):  # la portada de CatQuiz no es fa servir aquí: els jocs tornen al Salón
    p = os.path.join(dst, f)
    if os.path.exists(p): os.remove(p)
open(os.path.join(dst, 'index.html'), 'w').write('<!DOCTYPE html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../../#sec-catquiz"><link rel="canonical" href="https://www.catquiz.cat/"><title>CatQuiz</title><a href="../../#sec-catquiz">CatQuiz</a>')
print(len(nous), 'jocs copiats')
