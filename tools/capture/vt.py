import sys,time,os,base64;sys.path.insert(0,'.')
from harness import route,launch
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=launch(p);ctx=b.new_context(viewport={'width':960,'height':600});ctx.add_init_script(path='vt.js');pg=ctx.new_page();pg.route('**/*',route)
    pg.goto('http://localhost:8765/juegos/monster/index.html');pg.wait_for_timeout(2500)
    cdp=ctx.new_cdp_session(pg)
    pg.evaluate('__vt.start()')
    pg.keyboard.down('ArrowRight')
    os.makedirs('fr',exist_ok=True)
    t=time.time()
    for i in range(48):
        pg.evaluate('__vt.step(42)')
        d=cdp.send('Page.captureScreenshot',{'format':'jpeg','quality':85})
        open(f'fr/{i:03d}.jpg','wb').write(base64.b64decode(d['data']))
    print('s/frame',(time.time()-t)/48)
