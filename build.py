"""Builds TechVestVentures Market Economy Graphs from /workspace/risk-watcher/focus/market-economy (charts.py -> index.json + PNGs). Numbers come only from the linked primary data."""
import os,sys,json,shutil
sys.path.insert(0,'/workspace/risk-watcher/graphs-site');os.chdir(os.path.dirname(os.path.abspath(__file__)))
import common
from common import *
T="TechVestVentures Market Economy Graphs";F="/workspace/risk-watcher/focus/market-economy"
C=json.load(open(F+"/index.json"))
TABS=[("Q1","USA Markets","USA"),("Q2","China Credit","China"),("Q3","Europe Bonds","Europe"),("Q4","Russia Ruble","Russia"),("Q5","Japan Rates","Japan"),("Q6","International","International"),("Q7","Recessions","Recessions"),("Q8","Depressions","Depressions"),("Q9","Boom Peaks","Booms"),("Q10","Bubble Watch","Bubbles"),("Q11","Debt Burdens","Debt"),("Q12","Cycle Counts","Cycles")]
VIEW='<div class="view"><b>Michael Hentschel\'s view:</b> Pattern repetition is easy to show. But unless a cycle, such as a Kondratieff wave, has repeated more than 3 times in the record, short-term pattern analysis is a stab in the dark. Where a chart implies a repeat, its caption says how many past cycles support it. These charts illustrate risk; they do not call stocks or bonds.</div>'
common.CSS+="""
figure.g{display:grid;grid-template-columns:minmax(0,7fr) minmax(260px,3fr);gap:22px;align-items:start;margin:0 0 40px}
figure.g img{width:100%;height:auto;max-width:none}
figure.g figcaption{font-size:18px;line-height:1.5;margin:0}figure.g figcaption p{margin:0 0 12px}
figure.g figcaption .t{font-weight:700;display:block;margin-bottom:8px}
.view{border-left:4px solid #8B0000;background:#faf3f3;padding:10px 14px;margin:0 0 24px;font-size:17px;line-height:1.5}
@media(max-width:1100px){figure.g{grid-template-columns:1fr}}"""
shutil.rmtree("issues",ignore_errors=True);os.makedirs("issues/img")
tabs=[];counts={}
def w(k,lab,body): open(f"issues/{k}.html","w").write(page(T,k,body));tabs.append((k,lab))
for c in C: save_img(F+"/"+c["file"],"issues/img/"+c["file"].replace(".png",".webp"))
def fig(c):
    s=" ".join(f'<a href="{E(u)}">{E(l)}</a>' for l,u in c["sources"])
    return f'<figure class="g"><img src="img/{c["file"].replace(".png",".webp")}" alt="{E(c["title"])}" loading="lazy"><figcaption><span class="t">Chart M{c["n"]:02d}. {E(c["title"])}</span><p>{E(c["caption"])}</p><p>Sources: {s}</p></figcaption></figure>'
for q,lab,tag in TABS:
    cs=[c for c in C if tag in c["tabs"]];counts[f"{q} {lab}"]=len(cs)
    w(q,f"{q} {lab}",f'<h2 class="desk">{q}. {E(lab)}</h2>'+VIEW+"\n".join(fig(c) for c in cs))
src={}
for c in C:
    for l,u in c["sources"]: src.setdefault(u,l)
w("sources","Sources",f'<h2 class="desk">Sources ({len(src)} links)</h2><p>All charts were drawn by TechVestVentures from primary data downloaded on Oct 23, 2026 (M01-M25) and Oct 25, 2026 (M26-M28), mostly via FRED (Federal Reserve Bank of St. Louis), which redistributes Fed, BEA, BLS, OECD, BIS and IMF series. No numbers were copied from third-party chart images.</p><ul class="src">'+"".join(f'<li>{E(l)}: <a href="{E(u)}">{E(u)}</a></li>' for u,l in src.items())+"</ul>")
index(T,tabs,"Sections",cur="market");print(json.dumps(counts),len(src))
