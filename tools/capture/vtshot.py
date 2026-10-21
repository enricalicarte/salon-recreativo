"""Capturas con tiempo virtual: python3 vtshot.py <url> <prefijo> <seg1,seg2,...> [w h]"""
import sys,base64
sys.path.insert(0,'cap');from harness import route,launch
from playwright.sync_api import sync_playwright
url,pre,secs=sys.argv[1],sys.argv[2],[float(x) for x in sys.argv[3].split(',')]
W,H=(int(sys.argv[4]),int(sys.argv[5])) if len(sys.argv)>5 else (960,600)
with sync_playwright() as p:
    b=launch(p);ctx=b.new_context(viewport={'width':W,'height':H});ctx.add_init_script(path='cap/vt.js')
    pg=ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)[:300]));pg.route('**/*',route)
    pg.goto('http://localhost:8765/'+url);pg.wait_for_timeout(1500);pg.click('#btn');pg.wait_for_timeout(300)
    cdp=ctx.new_cdp_session(pg);cdp.send('Emulation.setDeviceMetricsOverride',{'width':W,'height':H,'deviceScaleFactor':1,'mobile':False})
    pg.evaluate('__vt.start()');cdp.send('Page.captureScreenshot',{'format':'jpeg','quality':10})
    t=0
    for s in secs:
        while t<s: pg.evaluate('__vt.step(1000/24)');t+=1/24
        r=cdp.send('Page.captureScreenshot',{'format':'png'});open(f'{pre}_{s:g}.png','wb').write(base64.b64decode(r['data']))
    info=pg.evaluate("[document.querySelector('#score')&&document.querySelector('#score').textContent,document.querySelector('#score2')&&document.querySelector('#score2').textContent,document.querySelector('#tag').textContent,document.querySelector('#toast').textContent]")
    print(pre,info,errs);b.close()
