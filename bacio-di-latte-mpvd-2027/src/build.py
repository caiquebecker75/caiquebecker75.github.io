import json, re, sys, os
deck = sys.argv[1]; out = sys.argv[2]
base = os.path.join(deck, "project") if os.path.isdir(os.path.join(deck, "project")) else deck
d = json.load(open(os.path.join(base, "deck.json")))
arrow = '<svg class="arrow" viewBox="0 0 64 32" width="64" height="32" style="flex:none;align-self:center" aria-hidden="true"><path d="M0 10h38V0l26 16-26 16V22H0z" fill="#8BA65A"/></svg>'
slides = []
for i, sid in enumerate(d["order"], 1):
    h = open(os.path.join(base, "slides", f"{sid}.html"), encoding="utf-8").read().strip()
    h = re.sub(r'<x-shape kind="arrow-right"[^>]*></x-shape>', arrow, h)
    h = re.sub(r'<aside>(.*?)</aside>', r'<aside class="notes">\1</aside>', h, flags=re.S)
    h = h.replace('<section id="%s"' % sid, '<section class="slide" data-n="%d" id="%s"' % (i, sid), 1)
    slides.append(h)
html = open(os.path.join(os.path.dirname(__file__), "shell.html"), encoding="utf-8").read()
html = html.replace("{{TITLE}}", d["title"]).replace("{{SLIDES}}", "\n".join(slides)).replace("{{COUNT}}", str(len(slides)))
open(out, "w", encoding="utf-8").write(html)
print(len(slides), "slides")
