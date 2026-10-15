#!/usr/bin/env python3
"""Copia capturas (jpg 960x600) y clips (mp4) a media/, recomprimiendo el póster.
Uso: python3 tools/import_media.py <carpeta_con_capturas> [slug ...]"""
import os, sys, shutil
from PIL import Image
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1]; only = set(sys.argv[2:])
md = os.path.join(root, 'media'); os.makedirs(md, exist_ok=True)
n = 0
for f in sorted(os.listdir(src)):
    if not f.endswith('.jpg') or f.endswith('-strip.jpg'): continue
    slug = f[:-4]
    if only and slug not in only: continue
    if not os.path.exists(os.path.join(src, slug + '.mp4')): continue
    Image.open(os.path.join(src, f)).convert('RGB').resize((960, 600), Image.LANCZOS).save(os.path.join(md, slug + '.jpg'), quality=80, optimize=True, progressive=True)
    shutil.copy(os.path.join(src, slug + '.mp4'), os.path.join(md, slug + '.mp4'))
    import subprocess
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', os.path.join(md, slug + '.mp4'), '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '40',
                    '-row-mt', '1', '-deadline', 'good', '-cpu-used', '4', '-an', os.path.join(md, slug + '.webm')], check=False)
    n += 1
print(n, 'juegos importados a media/')
