#!/usr/bin/env python3
"""Add the figure-set gallery to the site.

Reuses the existing .grid / .card CSS so it inherits the dashboard's look and its dark theme.
One short caption per figure and nothing else -- the section adds 26 images and ~180 words.
Inserted after #charts so the interactive charts stay the primary view.
"""
import os, csv, collections, json, html

REPO = os.path.expanduser("~/evaluating-the-evaluators")
IX = os.path.join(REPO, "index.html")
FMT = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_figs", "_fmt.json")))

rows = list(csv.DictReader(open(os.path.join(REPO, "v11.csv"), encoding="utf-8")))
tier = lambda r: ("A" if r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")
A = [r for r in rows if tier(r) == "A"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]
p = collections.Counter(r["Proportionality"] for r in H)
short = p["Accountability gap (no action)"] + p["Under-response (gap)"]
n = len(H)

# (file stem, wide?, caption). Captions are one line each; no paragraphs.
FIGS = [
 ("00_title_hero", 1, "The pipeline end to end. A finding <b>falls short</b> when the response is weaker than its severity warrants."),
 ("04_headline_outcome_distribution", 0, "Outcome distribution across the headline population."),
 ("10_proportionality_by_severity", 0, "Outcome composition by severity. The bar is severity-relative."),
 ("20_accountability_pipeline_funnel", 1, "Attrition from all findings through to policy uptake."),
 ("07_tier_distribution", 0, "Accountability-relevant, evaluation-only, and out-of-scope splits."),
 ("17_severity_classification", 0, "Severity from the three-model ensemble majority."),
 ("13_institution_type_tree", 1, "Who reports findings, by institution type."),
 ("01_findings_per_institution", 0, "Findings per institution, top 18."),
 ("12_evaluator_scope", 0, "Government institute versus third-party evaluator."),
 ("11_domain_distribution", 0, "Findings per risk domain. Multi-label, so bars sum above n."),
 ("02_findings_per_model_developer", 0, "Accountability-relevant findings per model developer."),
 ("03_findings_per_access_type", 0, "Access the evaluator had: pre-deployment, post, or mixed."),
 ("23_corpus_growth_by_tier", 0, "Corpus growth by year and tier."),
 ("06_findings_per_year", 0, "Findings per year. 2026 is partial — cutoff 31 July."),
 ("08_action_level_distribution", 0, "Strength of the documented company response."),
 ("18_attribution_distribution", 0, "Whether the company referenced the finding or its evaluator."),
 ("14_response_lag_distribution", 0, "Days from publication to response. Negative = pre-deployment."),
 ("05_pre_vs_post_deployment_response_rate", 0, "Substantive response rate, pre- versus post-deployment."),
 ("09_policy_level_distribution", 1, "Policy uptake. Official government sources only; one binding action in the corpus."),
 ("19_gap_rate_by_developer", 0, "By developer, n≥5. The smallest bars are fragile."),
 ("16_gap_rate_by_access_type", 0, "By access type, against the corpus average."),
 ("22_domain_x_outcome_heatmap", 0, "Outcome composition by domain. Colour encodes magnitude only."),
 ("21_severity_x_action_heatmap", 0, "Severity against response strength."),
 ("15b_shortfall_rate_by_year", 0, "Shortfall by year versus the no-response-at-all rate — the two diverge."),
 ("15_gap_rate_by_year", 0, "No-response-at-all rate by year."),
 ("24_evaluator_volume_vs_gap", 0, "Evaluator volume against shortfall, n≥4."),
]
missing = [s for s, _, _ in FIGS if f"{s}.png" not in FMT]
if missing:
    raise SystemExit(f"figures not in the web set: {missing}")

cards = []
for stem, wide, cap in FIGS:
    ext = FMT[f"{stem}.png"]
    cls = "card wide" if wide else "card"
    alt = html.escape(__import__("re").sub(r"<[^>]+>", "", cap))
    cards.append(
        f'        <figure class="{cls}" style="margin:0">\n'
        f'          <img loading="lazy" src="charts/{stem}.{ext}" alt="{alt}"\n'
        f'               style="width:100%;height:auto;border-radius:8px;display:block;background:#fff">\n'
        f'          <figcaption class="sub" style="margin:8px 0 0">{cap}</figcaption>\n'
        f'        </figure>')

SECTION = (
 '\n    <section id="figures">\n'
 '      <h2>The figure set</h2>\n'
 f'      <p class="sectionlede">All 26 figures from the paper, regenerated 2026-08-17 from the merged '
 f'corpus. Headline: {short} of {n} significant-risk findings ({short/n*100:.0f}%) drew no proportionate '
 'response.</p>\n'
 '      <div class="grid">\n' + "\n".join(cards) + '\n      </div>\n'
 '    </section>\n')

t = open(IX).read()
if 'id="figures"' in t:
    import re
    t = re.sub(r'\n    <section id="figures">.*?\n    </section>\n', SECTION, t, flags=re.S)
    print("replaced the existing figures section")
else:
    anchor = '    <section id="explorer">'
    if anchor not in t:
        raise SystemExit("could not find the explorer section to insert before")
    t = t.replace(anchor, SECTION + anchor, 1)
    print("inserted the figures section before #explorer")
open(IX, "w").write(t)

# add it to the nav if there is one
navm = __import__("re").search(r'<nav[^>]*>(.*?)</nav>', t, __import__("re").S)
if navm and 'href="#figures"' not in navm.group(1) and 'href="#charts"' in navm.group(1):
    seg = navm.group(1)
    m2 = __import__("re").search(r'(<a[^>]*href="#charts"[^>]*>.*?</a>)', seg, __import__("re").S)
    if m2:
        new = seg.replace(m2.group(1), m2.group(1) + m2.group(1)
                          .replace('#charts', '#figures')
                          .replace('>' + __import__("re").sub(r'<[^>]+>', '', m2.group(1)) + '<',
                                   '>Figures<'), 1)
        t = t.replace(seg, new, 1)
        open(IX, "w").write(t)
        print("nav: added a Figures link")

import re as _re
words = len(_re.sub(r'<[^>]+>', ' ', SECTION).split())
print(f"section adds {len(cards)} figures and ~{words} words of caption text")
print(f"index.html now {os.path.getsize(IX)/1024:.0f} KB")
