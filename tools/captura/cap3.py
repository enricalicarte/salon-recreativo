"""Captura con tiempo virtual: los menús se recorren en tiempo real y la partida se graba
fotograma a fotograma (24 fps reales aunque el render por software sea lento).
Uso: python3 cap3.py slug ...  (sin argumentos: todos)"""
import sys, json, os, time, subprocess, shutil, base64
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from harness import route, launch
from steps import STEPS
from playwright.sync_api import sync_playwright

OUT = HERE + '/p3/'; os.makedirs(OUT, exist_ok=True)
G = {g['slug']: g for g in json.load(open('/home/claude/salon-recreativo/tools/games.json'))['GAMES'] if g.get('play')}
FMS = 1000 / 24
VCLICK = open(HERE + '/vclick.js').read()

class Rec:
    def __init__(s, pg, cdp, d): s.pg, s.cdp, s.d, s.n, s.capture = pg, cdp, d, 0, True
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

def capture(b, slug):
    cfg = STEPS[slug]; g = G[slug]; url = cfg.get('url', g['play'])
    fd = OUT + slug + '_fr'; shutil.rmtree(fd, ignore_errors=True); os.makedirs(fd)
    ctx = b.new_context(viewport={'width': 960, 'height': 600}, locale='es-ES', has_touch=cfg.get('touch', False))
    ctx.add_init_script(path=HERE + '/vt.js')
    pg = ctx.new_page(); pg.route('**/*', route)
    pg.goto('http://localhost:8765/' + url, timeout=30000)
    for st in cfg.get('setup', []): do(pg, st)
    cdp = ctx.new_cdp_session(pg)
    pg.evaluate('__vt.start()')
    rec = Rec(pg, cdp, fd)
    for st in cfg.get('play', [('wait', 3500)]): do(pg, st, rec)
    if rec.n < 60: rec.advance((60 - rec.n) * FMS)
    ctx.close()
    n = rec.n
    pick = cfg.get('poster', 0.62)
    shutil.copy(f'{fd}/{int(n * pick):04d}.jpg', OUT + slug + '.jpg')
    start = 0 if cfg.get('clip','start')=='start' else max(0, n - 96)
    n = min(n, start + 96)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', '24', '-start_number', str(start), '-i', f'{fd}/%04d.jpg',
                    '-frames:v', str(n - start), '-vf', 'scale=640:400', '-c:v', 'libx264', '-preset', 'slow', '-crf', '29',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT + slug + '.mp4'], check=False)
    shutil.rmtree(fd, ignore_errors=True)
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
