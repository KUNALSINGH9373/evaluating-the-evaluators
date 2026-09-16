#!/usr/bin/env python3
"""Finish the site data refresh: the tree card's alt text, and web-sized embedded PNGs.

The alt text is the accessible description of the tree image, so it has to state the same
numbers the picture does -- it is generated from the CSV here rather than typed.
"""
import os, re, csv, shutil, collections

REPO = os.path.expanduser("~/evaluating-the-evaluators")
WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_figs")

rows = list(csv.DictReader(open(os.path.join(REPO, "v11.csv"), encoding="utf-8")))
PRIM = ["Government", "Non-Profit (AIEF)", "Non-Profit (Independent)", "For-Profit"]


def prim(r):
    p = [x.strip() for x in r.get("Institution Type", "").split(";") if x.strip()]
    for k in PRIM:
        if k in p:
            return k
    return p[0] if p else "Other"


grp = collections.defaultdict(list)
for r in rows:
    grp[prim(r)].append(r)
order = sorted(PRIM, key=lambda k: -len(grp[k]))
bits = []
for k in order:
    top = collections.Counter(r["Institution"] for r in grp[k]).most_common(5)
    other = len(grp[k]) - sum(v for _, v in top)
    inner = ", ".join(f"{nm} {v}" for nm, v in top) + (f", Other {other}" if other > 0 else "")
    bits.append(f"{k} {len(grp[k])} ({inner})")
alt = (f"Left-to-right tree diagram: {len(rows):,} findings by Institution Type - "
       + "; ".join(bits) + ".")

ap = os.path.join(REPO, "app.js")
t = open(ap).read()
m = re.search(r'alt: "Tree diagram: 456 findings by Institution Type[^"]*"', t)
if m:
    t = t[:m.start()] + 'alt: ' + repr(alt).replace("'", '"', 1)[:0] + f'"{alt}"' + t[m.end():]
    open(ap, "w").write(t)
    print("app.js: tree alt text regenerated from the CSV")
    print("   " + alt[:150] + " ...")
else:
    print("app.js !! tree alt text not matched")

# the dashboard should serve the web-sized figures, not the 200 dpi originals
for stem, dst in (("13_institution_type_tree", "institution_type_tree.png"),
                  ("17_severity_classification", "severity_classification.png")):
    for ext in ("png", "jpg"):
        p = os.path.join(WEB, f"{stem}.{ext}")
        if os.path.exists(p):
            before = os.path.getsize(os.path.join(REPO, dst))
            shutil.copy2(p, os.path.join(REPO, dst))
            print(f"   {dst}: {before/1024:.0f} KB -> {os.path.getsize(os.path.join(REPO,dst))/1024:.0f} KB")
            break

left = [x for x in ("456", " 211", " 155", " 301", " 415")
        if x in open(os.path.join(REPO, "index.html")).read() or x in open(ap).read()]
print(f"\nstale v10 figures remaining: {left or 'none'}")
