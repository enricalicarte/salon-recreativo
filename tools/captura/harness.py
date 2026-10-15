import re,os
NM='/tmp/claude-0/-home-claude/af2b990b-fbcc-57a3-9b7e-c5746bcaaae9/scratchpad/cap/node_modules'
def route(r):
    u=r.request.url
    if 'cdnjs.cloudflare.com/ajax/libs/three.js' in u:
        return r.fulfill(path=NM+'/three128/build/three.min.js',content_type='application/javascript')
    m=re.search(r'unpkg\.com/three@[\d.]+/(.*)$',u)
    if m:
        f=NM+'/three164/'+m.group(1).split('?')[0]
        if os.path.exists(f): return r.fulfill(path=f,content_type='application/javascript')
        return r.fulfill(status=404,body='')
    if 'fonts.googleapis' in u or 'fonts.gstatic' in u or 'googletagmanager' in u or 'google-analytics' in u:
        return r.fulfill(status=200,body='',content_type='text/css')
    if u.startswith('http://localhost'): return r.continue_()
    return r.fulfill(status=404,body='')
def launch(p):
    return p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--autoplay-policy=no-user-gesture-required'])
