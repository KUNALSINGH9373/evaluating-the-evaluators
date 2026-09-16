#!/usr/bin/env python3
"""Final site pass: de-version everything, cut the prose hard, refresh the figure set.

Requirements: current data only, all new charts, very little text, and no reference anywhere to a
previous dataset version. The dataset file is therefore named for what it is rather than for its
lineage, and the methodology is cut to only what a reader needs in order to read the numbers.
"""
import os, re, csv, json, shutil, subprocess, collections, html

REPO = os.path.expanduser("~/evaluating-the-evaluators")
D = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(D, "web_figs")
IX = os.path.join(REPO, "index.html")
APP = os.path.join(REPO, "app.js")

# ---- 0. drop the superseded bar chart, keep it gone -----------------------------------
sup = os.path.expanduser("~/Desktop/AISIEVAL_charts/13_institution_type.png")
if os.path.exists(sup):
    os.remove(sup)
    print("removed superseded 13_institution_type.png (the tree replaces it)")
tp = os.path.join(D, "tree.py")
t = open(tp).read()
if "13_institution_type.png" not in t:
    t += ('\n# The old bar version of this chart is superseded by the tree; keep it from reappearing.\n'
          'old = os.path.join(OUT, "13_institution_type.png")\n'
          'if os.path.exists(old):\n    os.remove(old)\n    print("  removed superseded 13_institution_type.png")\n')
    open(tp, "w").write(t)
    print("tree.py: now removes the superseded bar chart")
subprocess.run(["python3", os.path.join(D, "site_images.py")], capture_output=True, cwd=D)

# ---- 1. version-neutral dataset + codebook filenames ---------------------------------
if os.path.exists(os.path.join(REPO, "v11.csv")):
    shutil.move(os.path.join(REPO, "v11.csv"), os.path.join(REPO, "dataset.csv"))
    print("v11.csv -> dataset.csv")
rb = os.path.join(REPO, "v10_RULEBOOK.md")
if os.path.exists(rb):
    shutil.copy2(rb, os.path.join(REPO, "codebook.md"))
    print("v10_RULEBOOK.md -> copied to codebook.md")
bd = os.path.join(REPO, "build_data.py")
t = open(bd).read()
t = t.replace('HERE / "v11.csv" if (HERE / "v11.csv").exists() else HERE / "v10.csv"',
              'HERE / "dataset.csv"')
t = t.replace('# Dataset CSV, derived from AISIEVAL.xlsx. Pass a path to override; v11 is the current\n'
              '# merged corpus and v10 is kept so older builds stay reproducible.',
              '# Dataset CSV, derived from the master workbook. Pass a path to override.')
open(bd, "w").write(t)
r = subprocess.run(["python3", "build_data.py"], cwd=REPO, capture_output=True, text=True)
print("  " + (r.stdout.strip() or r.stderr.strip()))

# ---- 2. refresh figures ---------------------------------------------------------------
CH = os.path.join(REPO, "charts")
shutil.rmtree(CH, ignore_errors=True)
os.makedirs(CH)
FMT = json.load(open(os.path.join(WEB, "_fmt.json")))
for f in sorted(os.listdir(WEB)):
    if not f.startswith("_") and f.lower().endswith((".png", ".jpg")):
        shutil.copy2(os.path.join(WEB, f), os.path.join(CH, f))
for stem, dst in (("13_institution_type_tree", "institution_type_tree.png"),
                  ("17_severity_classification", "severity_classification.png")):
    ext = FMT[stem + ".png"]
    shutil.copy2(os.path.join(WEB, f"{stem}.{ext}"), os.path.join(REPO, dst))
print(f"charts/: {len(os.listdir(CH))} figures refreshed")

# ---- 3. text cuts + de-versioning ----------------------------------------------------
rows = list(csv.DictReader(open(os.path.join(REPO, "dataset.csv"), encoding="utf-8")))
tier = lambda r: ("A" if r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")
A = [r for r in rows if tier(r) == "A"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]
p = collections.Counter(r["Proportionality"] for r in H)
short = p["Accountability gap (no action)"] + p["Under-response (gap)"]
n = len(H)

t = open(IX).read()
CUTS = [
 # section ledes -> gone or one clause
 ('      <p class="sectionlede">Hover any mark for detail. Each chart includes a table view of the plotted values.</p>\n', ''),
 ('      <p class="sectionlede">Search and filter all findings. Click a row for the full finding, key quote, company response and sources.</p>\n',
  '      <p class="sectionlede">Click a row for the full record.</p>\n'),
 # methodology -> the minimum needed to read the numbers
 (re.search(r'      <h3>Scope</h3>.*?Ensemble-coded by three cross-provider model votes with unanimity recorded\.</p>\n',
            t, re.S).group(0) if re.search(r'      <h3>Scope</h3>.*?unanimity recorded\.</p>\n', t, re.S) else '@@nomatch@@',
  """      <dl class="mini">
        <dt>Who</dt><dd>AI safety institutes and third-party evaluators. Company-published reports
          count only where an external evaluator is named, and are filed under that evaluator.</dd>
        <dt>Which findings</dt><dd>Empirical, names a specific company or model, and concerning enough
          that a response is reasonable. Reassuring nulls, benchmark deltas with no threshold crossed,
          comparative rankings and methodology studies are tracked but excluded.</dd>
        <dt>What counts as a response</dt><dd>The company's own primary document, addressing the
          identified problem. Whether it credits the evaluator is recorded separately — acting without
          saying why still counts.</dd>
        <dt>Proportionality</dt><dd>Severity × response strength, severity-relative: a significant-risk
          finding needs a substantive response, a lesser one needs only a partial. Scores the content of
          the response, not its implementation or effect.</dd>
        <dt>Severity</dt><dd>Majority vote of three cross-provider models against seven
          dangerous-capability domains.</dd>
      </dl>
"""),
 # version references
 ('<a href="v11.csv" download>⬇ Download dataset (CSV)</a>', '<a href="dataset.csv" download>⬇ Download dataset (CSV)</a>'),
 ('<a href="v10_RULEBOOK.md">Read the full codebook</a>', '<a href="codebook.md">Read the codebook</a>'),
 ('    Dataset v10, verified 2026-08-02 ·\n', ''),
 (f'      <p class="sectionlede">All 26 figures from the paper, regenerated 2026-08-17 from the merged '
  f'corpus. Headline: {short} of {n} significant-risk findings ({short/n*100:.0f}%) drew no proportionate '
  'response.</p>\n',
  f'      <p class="sectionlede">{short} of {n} significant-risk findings — {short/n*100:.0f}% — drew no '
  'proportionate response.</p>\n'),
]
for a, b in CUTS:
    if a == '@@nomatch@@':
        print("!! methodology block not matched")
        continue
    if a in t:
        t = t.replace(a, b)
    else:
        print("!! not matched:", " ".join(a.split())[:64])
# tiny dl styling for the definition list
if ".mini" not in t:
    t = t.replace("</style>", """dl.mini { margin: 0; font-size: 14px; }
dl.mini dt { font-weight: 650; color: var(--fg); margin-top: 12px; }
dl.mini dd { margin: 2px 0 0; color: var(--muted); }
</style>""", 1)
open(IX, "w").write(t)

a = open(APP).read()
a = a.replace(" · dataset v10, verified 2026-08-02", "")
open(APP, "w").write(a)

# ---- 4. verify ------------------------------------------------------------------------
t = open(IX).read()
refs = set(re.findall(r'(?:src|href)="(?!https?:|#|mailto:)([^"]+)"', t))
missing = [r for r in refs if not os.path.exists(os.path.join(REPO, r.split("?")[0]))]
vis = re.sub(r"<[^>]+>", " ", t[t.find("<body"):])
i = t.find('<section id="methodology"')
meth = len(re.sub(r"<[^>]+>", " ", t[i:t.find("</section>", i)]).split())
verref = sorted(set(re.findall(r"\bv1[01]\b|[Dd]ataset v\d|merged v", t + a)))
print(f"""
missing local refs   {missing or 'none'}
version references   {verref or 'none'}
methodology words    {meth}
total visible words  {len(vis.split())}
figures on the page  {t.count('src="charts/')}
""")
