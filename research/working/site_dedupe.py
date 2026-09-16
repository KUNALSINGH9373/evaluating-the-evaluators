#!/usr/bin/env python3
"""Cut the figure gallery down to what the interactive charts do not already show.

The page was rendering the same topics twice. The interactive #charts section already covers the
funnel, severity x response, outcomes, response lag, findings per year, most-evaluated models,
domain, institution, the severity diagram and the institution tree -- the last two as the very
same PNGs. Those duplicates come out; what stays is the headline image plus the views that exist
nowhere else, in three labelled groups so it reads as structured rather than scattered.
"""
import os, re, csv, json, collections

REPO = os.path.expanduser("~/evaluating-the-evaluators")
IX = os.path.join(REPO, "index.html")
CH = os.path.join(REPO, "charts")
FMT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_figs", "_fmt.json")))

# Dropped because an interactive chart already shows it (its title in brackets):
DROP = {
 "20_accountability_pipeline_funnel": "The accountability funnel",
 "21_severity_x_action_heatmap":      "Severity vs. company response",
 "04_headline_outcome_distribution":  "Outcomes in the accountability set",
 "14_response_lag_distribution":      "Response lag",
 "06_findings_per_year":              "Reports released per year",
 "02_findings_per_model_developer":   "Most-evaluated models",
 "11_domain_distribution":            "Findings by domain",
 "01_findings_per_institution":       "Findings by institution",
 "17_severity_classification":        "How severity is classified (same image, already embedded)",
 "13_institution_type_tree":          "Institution tree (same image, already embedded)",
 # dropped as redundant against another kept figure, or too thin to earn space
 "15_gap_rate_by_year":               "superseded by the shortfall chart, which plots both series",
 "08_action_level_distribution":      "covered by outcomes + severity-vs-response",
 "10_proportionality_by_severity":    "covered by severity-vs-response",
 "23_corpus_growth_by_tier":          "covered by reports-per-year",
 "24_evaluator_volume_vs_gap":        "small-n scatter, little signal",
}

GROUPS = [
 ("The headline", [
   ("00_title_hero", 1, "Every significant-risk finding, and whether the response matched its severity."),
   ("15b_shortfall_rate_by_year", 0, "Shortfall by year, against the no-response-at-all rate — the two diverge."),
   ("09_policy_level_distribution", 0, "Policy uptake. One binding action in the whole corpus."),
 ]),
 ("Where the shortfall sits", [
   ("19_gap_rate_by_developer", 0, "By developer, n≥5. The smallest bars are fragile."),
   ("16_gap_rate_by_access_type", 0, "By how much access the evaluator had."),
   ("22_domain_x_outcome_heatmap", 1, "By risk domain. Colour encodes magnitude only."),
 ]),
 ("The corpus", [
   ("07_tier_distribution", 0, "Accountability-relevant, evaluation-only, and out-of-scope splits."),
   ("12_evaluator_scope", 0, "Safety institute versus third-party evaluator."),
   ("03_findings_per_access_type", 0, "Pre-deployment, post-deployment, or mixed access."),
   ("18_attribution_distribution", 0, "Whether the company referenced the finding or its evaluator."),
   ("05_pre_vs_post_deployment_response_rate", 0, "Substantive response rate, pre- versus post-deployment."),
 ]),
]
keep = [s for _, figs in GROUPS for s, _, _ in figs]
assert not (set(keep) & set(DROP)), set(keep) & set(DROP)

rows = list(csv.DictReader(open(os.path.join(REPO, "dataset.csv"), encoding="utf-8")))
tier = lambda r: ("A" if r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")
H = [r for r in rows if tier(r) == "A" and r["Severity (C1/C2) majority"] == "C1"]
p = collections.Counter(r["Proportionality"] for r in H)
short = p["Accountability gap (no action)"] + p["Under-response (gap)"]
n = len(H)

blocks = []
for label, figs in GROUPS:
    cards = []
    for stem, wide, cap in figs:
        ext = FMT[stem + ".png"]
        alt = re.sub(r"<[^>]+>", "", cap)
        cards.append(
          f'        <figure class="card{" wide" if wide else ""}" style="margin:0">\n'
          f'          <img loading="lazy" src="charts/{stem}.{ext}" alt="{alt}"\n'
          f'               style="width:100%;height:auto;border-radius:8px;display:block;background:#fff">\n'
          f'          <figcaption class="sub" style="margin:8px 0 0">{cap}</figcaption>\n'
          f'        </figure>')
    blocks.append(f'      <h3 class="figgroup">{label}</h3>\n      <div class="grid">\n'
                  + "\n".join(cards) + "\n      </div>")

SECTION = ('\n    <section id="figures">\n      <h2>Key figures</h2>\n'
           f'      <p class="sectionlede">{short} of {n} significant-risk findings — '
           f'{short/n*100:.0f}% — drew no proportionate response.</p>\n'
           + "\n".join(blocks) + "\n    </section>\n")

t = open(IX).read()
t = re.sub(r'\n    <section id="figures">.*?\n    </section>\n', SECTION, t, flags=re.S)
if ".figgroup" not in t:
    t = t.replace("</style>", """h3.figgroup { font-size: 13px; font-weight: 650; letter-spacing: .06em;
  text-transform: uppercase; color: var(--muted); margin: 26px 0 12px; }
h3.figgroup:first-of-type { margin-top: 6px; }
</style>""", 1)
open(IX, "w").write(t)

# delete the now-unused figures from the repo
used = {m.group(1) for m in re.finditer(r'src="charts/([^"]+)"', t)}
removed = []
for f in sorted(os.listdir(CH)):
    if f not in used:
        os.remove(os.path.join(CH, f))
        removed.append(f)

print(f"kept {len(keep)} figures in {len(GROUPS)} groups; dropped {len(DROP)}\n")
print("dropped, and why:")
for s, why in DROP.items():
    print(f"  {s:<42} {why}")
print(f"\ndeleted {len(removed)} files from charts/ · {len(os.listdir(CH))} remain")
vis = len(re.sub(r"<[^>]+>", " ", t[t.find("<body"):]).split())
print(f"figures on the page: {len(used)} · total visible words: {vis}")
miss = [r for r in re.findall(r'(?:src|href)="(?!https?:|#|mailto:)([^"]+)"', t)
        if not os.path.exists(os.path.join(REPO, r.split("?")[0]))]
print("missing refs:", miss or "none")
