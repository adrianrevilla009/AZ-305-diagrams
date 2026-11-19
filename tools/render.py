#!/usr/bin/env python3
"""Render pages of a .drawio file to PNG using draw.io's own viewer (headless Chrome).
usage: render.py WEBAPP_DIR FILE.drawio OUT_DIR [page_index ...]   (no pages = all)"""
import sys, os, json, html, shutil, re
from playwright.sync_api import sync_playwright

webapp, drawio, outdir, *pages = sys.argv[1:]
os.makedirs(outdir, exist_ok=True)
xml = open(drawio, encoding="utf-8").read()
n = len(re.findall(r"<diagram ", xml))
idx = [int(p) for p in pages] if pages else list(range(n))
tmp = os.path.join(webapp, "_render.html")
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
    for i in idx:
        cfg = {"highlight": "#0000ff", "nav": False, "resize": False, "toolbar": "", "page": i, "xml": xml}
        with open(tmp, "w", encoding="utf-8") as f:
            f.write('<html><body style="margin:0;background:white"><div id="g" class="mxgraph" style="width:100%%;min-height:400px" data-mxgraph="%s"></div>'
                    '<script src="js/viewer-static.min.js"></script></body></html>' % html.escape(json.dumps(cfg), quote=True))
        pg = b.new_page(viewport={"width": 1500, "height": 1000})
        def serve(route, request, webapp=webapp):
            path = request.url.split("app.diagrams.net/", 1)[1].split("?")[0]
            fp = os.path.join(webapp, path)
            if os.path.isfile(fp):
                ct = "image/svg+xml" if fp.endswith(".svg") else "application/octet-stream"
                route.fulfill(path=fp, content_type=ct)
            else:
                route.abort()
        pg.route("https://app.diagrams.net/**", serve)
        pg.goto("file://" + tmp)
        pg.wait_for_timeout(2500)
        box = pg.evaluate("(()=>{const s=document.querySelector('#g svg');if(!s)return null;const r=s.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
        out = os.path.join(outdir, f"{os.path.splitext(os.path.basename(drawio))[0]}_p{i}.png")
        if box:
            pg.set_viewport_size({"width": int(box[0]+box[2])+40, "height": int(box[1]+box[3])+40})
            pg.wait_for_timeout(300)
        pg.screenshot(path=out, full_page=True)
        pg.close()
        print(out)
    b.close()
os.remove(tmp)
