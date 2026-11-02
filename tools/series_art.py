"""Genera las ilustraciones de las series de Alica Play (play/img/). Uso: python3 tools/series_art.py"""
import sys, os
from playwright.sync_api import sync_playwright
out=sys.argv[1] if len(sys.argv)>1 else None
here=os.path.dirname(os.path.abspath(__file__)); out=out or os.path.join(os.path.dirname(here),'play','img')
jobs=[]
for m,slug,n in [('lloguer','lloguer',3),('tico','tico',5),('pronto','nueva-serie-infantil',1)]:
    jobs.append((m,0,f'{slug}.jpg',1600,900,False))
    jobs.append((m,0,f'{slug}-v.jpg',675,900,True))
    for v in range(n): jobs.append((m,v,f'{slug}-{v+1}.jpg',640,360,False))
os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch()
    for m,v,f,w,h,vert in jobs:
        pg=b.new_page(viewport={'width':w,'height':h})
        pg.goto(f'file://{here}/series_art.html?m={m}&v={v}'+('&vert=1' if vert else ''))
        pg.wait_for_timeout(200)
        pg.screenshot(path=os.path.join(out,f),type='jpeg',quality=84)
        pg.close()
    b.close()
print('ok',len(jobs))
