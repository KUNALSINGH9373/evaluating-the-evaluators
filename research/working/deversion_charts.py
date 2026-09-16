#!/usr/bin/env python3
"""Strip dataset-version references from the figure captions, then regenerate every figure.

The strings live inside the PNGs, so editing the site is not enough -- the charts themselves say
"merged v10+v11". The site should describe one current dataset with no lineage on display.
"""
import os, re, subprocess

D = os.path.dirname(os.path.abspath(__file__))
SUBS = [
    # hero.py
    ('"shows no located public response (red) or only a partial / acknowledged one (orange). Data: merged v10+v11, "\n        "cutoff 31 July 2026."',
     '"shows no located public response (red) or only a partial / acknowledged one (orange). "\n        "Corpus cutoff 31 July 2026."'),
    ('"Data: merged v10+v11 (1,013 findings), Institution Type field. Compound values (e.g. \\"Government;Lab\\") folded into their primary type."',
     '"Institution Type field. Compound values (e.g. \\"Government;Lab\\") fold into their primary type."'),
    # tree.py
    ('"Data: merged v10+v11 (1,013 findings), Institution Type field. Compound values "\n        "(e.g. \\"Government;Lab\\") fold into their primary type.",',
     '"Institution Type field. Compound values (e.g. \\"Government;Lab\\") fold into their "\n        "primary type.",'),
    # charts.py global footer
    ('"Corpus: 1,013 findings · 441 reports · 2023-01-23 to 2026-07-31 · merged v10+v11"',
     '"Corpus: 1,013 findings · 441 reports · 2023-01-23 to 2026-07-31"'),
]
for f in ("hero.py", "tree.py", "charts.py", "charts2.py", "fig15b.py"):
    p = os.path.join(D, f)
    if not os.path.exists(p):
        continue
    t = open(p).read()
    orig = t
    for a, b in SUBS:
        t = t.replace(a, b)
    # any straggler in a user-visible string
    t = re.sub(r'merged v10\+v11[,\s]*', '', t)
    if t != orig:
        open(p, "w").write(t)
        print(f"de-versioned {f}")

print()
for s in ("charts.py", "charts2.py", "hero.py", "tree.py", "fig15b.py"):
    p = os.path.join(D, s)
    if not os.path.exists(p):
        continue
    r = subprocess.run(["python3", p], capture_output=True, text=True, cwd=D)
    print(("ok   " if r.returncode == 0 else "FAIL ") + s + ("" if r.returncode == 0 else "\n" + r.stderr[-400:]))

# confirm nothing version-ish survives in a visible caption
left = []
for s in ("charts.py", "charts2.py", "hero.py", "tree.py", "fig15b.py"):
    p = os.path.join(D, s)
    if os.path.exists(p):
        for m in re.finditer(r'"[^"\n]*\bv1[01]\b[^"\n]*"', open(p).read()):
            left.append((s, m.group(0)[:70]))
print("\nversion strings left in quoted captions:", left or "none")
