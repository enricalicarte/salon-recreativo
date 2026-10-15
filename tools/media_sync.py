#!/usr/bin/env python3
"""Sincroniza las capturas reales de media/ con la web:
 - escribe la lista de juegos con captura en tools/source.html (const MEDIA)
 - genera img/<slug>.jpg (1200x750) para compartir en redes a partir de media/<slug>.jpg"""
import os,re,json
from PIL import Image
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
md=os.path.join(root,'media')
slugs=sorted(f[:-4] for f in os.listdir(md) if f.endswith('.jpg'))
p=os.path.join(root,'tools/source.html');s=open(p,encoding='utf-8').read()
s=re.sub(r'/\*MEDIA\*/.*?/\*/MEDIA\*/','/*MEDIA*/'+json.dumps(slugs)+'/*/MEDIA*/',s,flags=re.S)
open(p,'w',encoding='utf-8').write(s)
for sl in slugs:
    im=Image.open(os.path.join(md,sl+'.jpg')).convert('RGB')
    w,h=im.size;tw=int(h*1.6)
    if tw<w: im=im.crop(((w-tw)//2,0,(w-tw)//2+tw,h))
    im.resize((1200,750),Image.LANCZOS).save(os.path.join(root,'img',sl+'.jpg'),quality=82,optimize=True)
print(len(slugs),'capturas sincronizadas')
