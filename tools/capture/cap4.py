"""Captura con tiempo virtual: los menús se recorren en tiempo real y la partida se graba
fotograma a fotograma (24 fps reales aunque el render por software sea lento).
Uso: python3 cap3.py slug ...  (sin argumentos: todos)"""
import sys, json, os, time, subprocess, shutil, base64
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from harness import route, launch
from steps import STEPS
from playwright.sync_api import sync_playwright

OUT = HERE + '/p5/'
LEN = int(os.environ.get('LEN','240')); os.makedirs(OUT, exist_ok=True)
G = {g['slug']: g for g in json.load(open('/home/claude/salon-recreativo/tools/games.json'))['GAMES'] if g.get('play')}
FMS = 1000 / 24
VF_PORTRAIT = 'split[a][b];[a]scale=640:-2,crop=640:400,boxblur=18:2,eq=brightness=-0.12:saturation=1.1[bg];[b]scale=-2:400[fg];[bg][fg]overlay=(W-w)/2:0'
VCLICK = open(HERE + '/vclick.js').read()

class Rec:
    def __init__(s, pg, cdp, d):
        s.pg, s.cdp, s.d, s.n, s.capture = pg, cdp, d, 0, True
        vp = pg.viewport_size; cdp.send('Emulation.setDeviceMetricsOverride', {'width': vp['width'], 'height': vp['height'], 'deviceScaleFactor': 1, 'mobile': False})
    def frame(s):
        s.pg.evaluate(f'__vt.step({FMS})')
        if s.capture:
            r = s.cdp.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 88})
            open(f'{s.d}/{s.n:04d}.jpg', 'wb').write(base64.b64decode(r['data'])); s.n += 1
    def advance(s, ms):
        for _ in range(max(1, round(ms / FMS))): s.frame()

def do(pg, st, rec=None):
    k = st[0]
    wait = (lambda ms: rec.advance(ms)) if rec else (lambda ms: pg.wait_for_timeout(ms))
    try:
        if k == 'wait': wait(st[1])
        elif k == 'skip':  # avanzar sin grabar (cuentas atrás)
            if rec: rec.capture = False; rec.advance(st[1]); rec.capture = True
            else: pg.wait_for_timeout(st[1])
        elif k == 'click': pg.locator(st[1]).first.click(timeout=3000, force=True)
        elif k == 'text':
            r = pg.evaluate(VCLICK, st[1])
            if r: pg.mouse.click(r[0], r[1])
            else: print('   no visible:', st[1], flush=True)
        elif k == 'tap': pg.mouse.click(st[1], st[2]); wait(80)
        elif k == 'press': pg.keyboard.down(st[1]); wait(90); pg.keyboard.up(st[1])
        elif k == 'type':
            for ch in st[1]: pg.keyboard.press(ch); wait(90)
        elif k == 'js': pg.evaluate(st[1])
        elif k == 'down': pg.keyboard.down(st[1])
        elif k == 'up': pg.keyboard.up(st[1])
        elif k == 'hold':
            for kk in st[1]: pg.keyboard.down(kk)
            wait(st[2])
            for kk in st[1]: pg.keyboard.up(kk)
        elif k == 'mousehold':
            pg.mouse.move(st[1], st[2]); pg.mouse.down(); wait(st[3]); pg.mouse.up()
        elif k == 'spell':  # ('spell', 'PALABRA'): arrastrar por las letras de la rueda (#wheel .letter)
            pts = pg.evaluate('''w=>{const ls=[...document.querySelectorAll('#wheel .letter')],used=new Set(),out=[];
              for(const ch of w){const e=ls.find((l,i)=>!used.has(i)&&l.textContent.trim()===ch);if(!e)return null;used.add(ls.indexOf(e));
                const r=e.getBoundingClientRect();out.push([r.left+r.width/2,r.top+r.height/2]);}return out;}''', st[1])
            if pts:
                pg.mouse.move(*pts[0]); pg.mouse.down(); wait(FMS * 2)
                for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                    for i in range(1, 6): pg.mouse.move(x0 + (x1 - x0) * i / 5, y0 + (y1 - y0) * i / 5); wait(FMS)
                wait(FMS * 2); pg.mouse.up()
            else: print('   no se puede deletrear', st[1], flush=True)
        elif k == 'zig':  # ('zig', x0, y0, x1, y1, ms): frotar en zigzag
            x0, y0, x1, y1, ms = st[1:]; import math
            pg.mouse.move(x0, y0); pg.mouse.down(); n = max(2, round(ms / FMS))
            for i in range(n):
                f = i * FMS / 1000
                pg.mouse.move((x0 + x1) / 2 + (x1 - x0) / 2 * math.sin(f * 9), (y0 + y1) / 2 + (y1 - y0) / 2 * math.sin(f * 2.1)); wait(FMS)
            pg.mouse.up()
        elif k == 'drag':
            x1, y1, x2, y2, ms = st[1:]
            pg.mouse.move(x1, y1); pg.mouse.down(); n = max(2, round(ms / FMS))
            for i in range(1, n + 1):
                pg.mouse.move(x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n); wait(FMS)
            pg.mouse.up()
        elif k == 'taps':
            for i in range(st[3]): pg.mouse.click(st[1], st[2]); wait(st[4])
    except Exception as e:
        print('   step fail', st[:2], str(e)[:70], flush=True)

def deglitch(fd, n):
    # quita fotogramas con fallos de render (un fotograma muy distinto de sus vecinos)
    from PIL import Image, ImageChops, ImageStat
    sm = lambda i: Image.open(f'{fd}/{i:04d}.jpg').convert('L').resize((96, 60))
    prev = sm(0); ims = [prev] + [None] * (n - 1)
    for i in range(1, n): ims[i] = sm(i)
    d = lambda a, b: ImageStat.Stat(ImageChops.difference(a, b)).mean[0]
    fixed = 0
    for i in range(1, n - 1):
        a, c = d(ims[i], ims[i - 1]), d(ims[i + 1], ims[i - 1])
        if a > 12 and c < a * .5:
            shutil.copy(f'{fd}/{i-1:04d}.jpg', f'{fd}/{i:04d}.jpg'); ims[i] = ims[i - 1]; fixed += 1
    if fixed: print('   fotogramas corregidos:', fixed, flush=True)

def capture(b, slug):
    cfg = STEPS[slug]; g = G[slug]; url = cfg.get('url', g['play'])
    fd = OUT + slug + '_fr'; shutil.rmtree(fd, ignore_errors=True); os.makedirs(fd)
    ctx = b.new_context(viewport=cfg.get('vp', {'width': 960, 'height': 600}), locale='es-ES', has_touch=cfg.get('touch', False))
    ctx.add_init_script(path=HERE + '/vt.js')
    pg = ctx.new_page(); pg.route('**/*', route)
    pg.goto('http://localhost:8765/' + url, timeout=30000)
    for st in cfg.get('setup', []): do(pg, st)
    cdp = ctx.new_cdp_session(pg)
    pg.evaluate('__vt.start()')
    cdp.send('Page.captureScreenshot', {'format': 'jpeg', 'quality': 10})  # un fotograma real para que el bucle rAF pase al tiempo virtual (si no, los 'skip' no avanzan)
    rec = Rec(pg, cdp, fd)
    for st in cfg.get('intro', []):
        if st[0] == 'press': rec.capture = False; do(pg, st, rec); rec.capture = True
        else: do(pg, st, rec)
    for rep in range(6):                      # repetir la partida hasta tener un clip largo
        for st in cfg.get('play', [('wait', 3500)]):
            do(pg, st, rec)
            if rec.n >= LEN + cfg.get('extra', 40): break
        if rec.n >= LEN + cfg.get('extra', 40): break
    if rec.n < LEN: rec.advance((LEN - rec.n) * FMS)
    ctx.close()
    n = rec.n
    pick = cfg.get('poster', 0.62)
    shutil.copy(f'{fd}/{int(n * pick):04d}.jpg', OUT + slug + '.jpg')
    deglitch(fd, n)
    start = 0 if cfg.get('clip','start')=='start' else max(0, n - LEN)
    n = min(n, start + LEN)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', '24', '-start_number', str(start), '-i', f'{fd}/%04d.jpg',
                    '-frames:v', str(n - start), '-vf', (VF_PORTRAIT if cfg.get('portrait') else 'scale=640:400'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '29',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT + slug + '.mp4'], check=False)
    if cfg.get('portrait'):  # portada también compuesta (juego vertical centrado sobre fondo difuminado)
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(LEN / 24 * pick), '-i', OUT + slug + '.mp4', '-frames:v', '1', '-vf', 'scale=960:600', '-q:v', '3', OUT + slug + '.jpg'], check=False)
    if not os.environ.get('KEEP'): shutil.rmtree(fd, ignore_errors=True)
    print(slug, 'ok', n, 'frames', flush=True)

if __name__ == '__main__':
    only = sys.argv[1:] or list(STEPS)
    with sync_playwright() as p:
        b = launch(p)
        for s in only:
            t = time.time()
            try: capture(b, s)
            except Exception as e: print(s, 'ERR', str(e)[:160], flush=True)
            print('   ', round(time.time() - t), 's', flush=True)
