#!/usr/bin/env python3
"""Update the GitHub Pages site to the merged v11 corpus.

Four things:
  1. point build_data.py at the current CSV (argv, defaulting to v11.csv) and regenerate data.js
  2. refresh the two PNGs the dashboard embeds, from the regenerated figure set
  3. replace the stale hardcoded numbers in index.html and app.js
  4. copy the full figure set into charts/ for the new gallery section

Nothing here invents numbers: every substituted value is read from the workbook by site_export.py.
"""
import os, re, shutil, subprocess, csv, collections, datetime

REPO = os.path.expanduser("~/evaluating-the-evaluators")
CHARTS_SRC = os.path.expanduser("~/Desktop/AISIEVAL_charts")
WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_figs")
CHARTS_DST = os.path.join(REPO, "charts")

# ---------- 1. build_data.py: take the CSV path as an argument ------------------------
bd = os.path.join(REPO, "build_data.py")
t = open(bd).read()
if 'SRC = HERE / "v10.csv"' in t:
    t = t.replace(
        'import csv\nimport json\nimport statistics\nfrom pathlib import Path',
        'import csv\nimport json\nimport statistics\nimport sys\nfrom pathlib import Path')
    t = t.replace(
        'SRC = HERE / "v10.csv"',
        '# Dataset CSV, derived from AISIEVAL.xlsx. Pass a path to override; v11 is the current\n'
        '# merged corpus and v10 is kept so older builds stay reproducible.\n'
        'SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else (\n'
        '    HERE / "v11.csv" if (HERE / "v11.csv").exists() else HERE / "v10.csv")')
    t = t.replace('"""Convert v10.csv into data.js consumed by the dashboard.\n\n'
                  '    Run: python3 build_data.py\n    Reads v10.csv in this directory, writes data.js.\n    """',
                  '"""Convert the dataset CSV into data.js consumed by the dashboard."""')
    open(bd, "w").write(t)
    print("build_data.py: SRC is now argv/v11-aware")
else:
    print("build_data.py: already updated")

r = subprocess.run(["python3", "build_data.py"], cwd=REPO, capture_output=True, text=True)
print("  " + (r.stdout.strip() or r.stderr.strip()))

# ---------- 2. refresh the embedded PNGs ---------------------------------------------
for src, dst in (("13_institution_type_tree.png", "institution_type_tree.png"),
                 ("17_severity_classification.png", "severity_classification.png")):
    s = os.path.join(CHARTS_SRC, src)
    d = os.path.join(REPO, dst)
    before = os.path.getsize(d) if os.path.exists(d) else 0
    shutil.copy2(s, d)
    print(f"  {dst}: {before/1024:.0f} KB -> {os.path.getsize(d)/1024:.0f} KB  (from {src})")

# ---------- 3. the full figure set for the gallery ------------------------------------
os.makedirs(CHARTS_DST, exist_ok=True)
copied = 0
for f in sorted(os.listdir(WEB)):
    if f.startswith("_") or not f.lower().endswith((".png", ".jpg")):
        continue
    shutil.copy2(os.path.join(WEB, f), os.path.join(CHARTS_DST, f))
    copied += 1
tot = sum(os.path.getsize(os.path.join(CHARTS_DST, f)) for f in os.listdir(CHARTS_DST))
print(f"  charts/: {copied} web-sized figures, {tot/1e6:.2f} MB total")

# ---------- 4. stale hardcoded numbers ------------------------------------------------
rows = list(csv.DictReader(open(os.path.join(REPO, "v11.csv"), encoding="utf-8")))
tier = lambda r: ("A" if r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")
A = [r for r in rows if tier(r) == "A"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]
sev = collections.Counter(r["Severity (C1/C2) majority"] for r in rows)
V = ("Sonnet5 vote", "GPT-5.5 vote", "Gemini3.1 vote")
unan = sum(1 for r in rows if len({r[c] for c in V}) == 1)
split = len(rows) - unan
N, NREP = len(rows), len({r["Report ID"] for r in rows if r["Report ID"]})
prop = collections.Counter(r["Proportionality"] for r in H)
short = prop["Accountability gap (no action)"] + prop["Under-response (gap)"]

ix = os.path.join(REPO, "index.html")
t = open(ix).read()
subs = [
  ('A verified dataset of 456 findings from 211 reports.',
   f'A verified dataset of {N:,} findings from {NREP} reports.'),
  ('<h3>From 456 findings to the accountability gap</h3>',
   f'<h3>From {N:,} findings to the accountability gap</h3>'),
]
for a, b in subs:
    if a in t:
        t = t.replace(a, b)
        print(f"  index.html: {b[:62]}")
    else:
        print(f"  index.html !! not matched: {a[:56]}")
open(ix, "w").write(t)

ap = os.path.join(REPO, "app.js")
t = open(ap).read()
asubs = [
  (f'C1 (155 findings, threshold demonstrated) or C2 (301 findings, threshold not demonstrated). '
   f'415 of 456 (91%) were unanimous 3-0; the remaining 41 (9%) were decided 2-1.',
   f'C1 ({sev["C1"]} findings, threshold demonstrated) or C2 ({sev["C2"]} findings, threshold not '
   f'demonstrated). {unan} of {N:,} ({unan/N*100:.0f}%) were unanimous 3-0; the remaining {split} '
   f'({split/N*100:.0f}%) were decided 2-1.'),
  ('["C1", 155, "Demonstrates ≥ 1 of 7 dangerous-capability domains"],',
   f'["C1", {sev["C1"]}, "Demonstrates ≥ 1 of 7 dangerous-capability domains"],'),
  ('["C2", 301, "Threshold not demonstrated (not the same as unimportant)"],',
   f'["C2", {sev["C2"]}, "Threshold not demonstrated (not the same as unimportant)"],'),
  ('["Unanimous 3–0 vote", 415, "91% of all 456 findings"],',
   f'["Unanimous 3–0 vote", {unan}, "{unan/N*100:.0f}% of all {N:,} findings"],'),
  ('["Split 2–1 vote", 41, "9% of all 456 findings"]],',
   f'["Split 2–1 vote", {split}, "{split/N*100:.0f}% of all {N:,} findings"]],'),
]
for a, b in asubs:
    if a in t:
        t = t.replace(a, b)
        print(f"  app.js: {b[:66]}")
    else:
        print(f"  app.js !! not matched: {a[:56]}")
open(ap, "w").write(t)

print(f"\nleftover stale figures in index.html/app.js: "
      f"{[x for x in ('456','211',' 155',' 301',' 415',' 41,') if x in open(ix).read() or x in open(ap).read()] or 'none'}")
print(f"\nheadline for the gallery caption: falls short {short}/{len(H)} = {short/len(H)*100:.1f}%")
