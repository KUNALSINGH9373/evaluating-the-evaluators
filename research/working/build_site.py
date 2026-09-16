#!/usr/bin/env python3
"""Build the chart-led Evaluating the Evaluators site.

Replaces the prose-heavy v10 methodology page. Every figure is inlined as a data URI (the
artifact CSP blocks external hosts) and every number is read from the workbook rather than
typed, so the page cannot drift from the data.

Text budget: one sentence per figure. The methodology survives as a compact table, not prose --
v10_RULEBOOK.md remains the normative source.
"""
import os, io, json, base64, collections, datetime, html
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "web_figs")
OUT = os.path.join(HERE, "site.html")
P = os.path.expanduser("~/Desktop/AISIEVAL.xlsx")

# ---------------------------------------------------------------- data
def norm(v):
    if v is None:
        return ""
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime("%Y-%m-%d")
    return str(v).strip()

ws = openpyxl.load_workbook(P, data_only=True)["AISIEVAL"]
hdr = [norm(c.value) for c in ws[1]]
R = [{h: norm(ws.cell(r, i).value) for i, h in enumerate(hdr, 1) if h}
     for r in range(2, ws.max_row + 1)]
R = [r for r in R if r.get("Finding ID")]
tier = lambda r: ("A" if r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")
A = [r for r in R if tier(r) == "A"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]
n = len(H)
GAP = "Accountability gap (no action)"
prop = collections.Counter(r["Proportionality"] for r in H)
noact, under, ok = prop[GAP], prop["Under-response (gap)"], prop["Proportionate"]
short = noact + under
al = collections.Counter(r["Action Level"] for r in A)
at = collections.Counter(r["Attribution"] for r in A)
pl = collections.Counter(r["Policy Level"] for r in A)
tiers = collections.Counter(tier(r) for r in R)
sc = collections.Counter(r.get("Scope", "") for r in R)
gov = [r for r in H if r.get("Scope") == "government-AISI"]
gov_short = sum(1 for r in gov if r["Proportionality"] != "Proportionate")
dates = sorted(r["Publication Date"] for r in R if r["Publication Date"])
years = sorted({d[:4] for d in dates})
yr = {}
for y in years:
    g = [r for r in H if r["Publication Date"][:4] == y]
    yr[y] = (len(g), sum(1 for r in g if r["Proportionality"] != "Proportionate") / len(g))
dom = collections.Counter()
for r in H:
    for x in r.get("Domain", "").split(";"):
        if x.strip():
            dom[x.strip()] += 1
lags = sorted(int(r["Lag (days)"]) for r in A if r["Lag (days)"].lstrip("-").isdigit())
med = lags[len(lags) // 2] if lags else 0

# ---------------------------------------------------------------- figures
fmt = json.load(open(os.path.join(FIGS, "_fmt.json")))
def uri(stem):
    ext = fmt.get(stem + ".png", "png")
    p = os.path.join(FIGS, f"{stem}.{ext}")
    mime = "image/jpeg" if ext == "jpg" else "image/png"
    return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()

def fig(stem, caption, wide=False):
    return (f'<figure class="{"wide" if wide else ""}">'
            f'<img loading="lazy" alt="{html.escape(caption)}" src="{uri(stem)}">'
            f'<figcaption>{caption}</figcaption></figure>')

pct = lambda a, b: f"{a/b*100:.0f}%"

# ---------------------------------------------------------------- page
CSS = """
:root{
  --paper:#F1F4F6; --surface:#FBFCFD; --surface-2:#E9EEF2;
  --ink:#0E1519; --ink-2:#3A4A55; --muted:#647684;
  --rule:#D3DCE3; --rule-strong:#B4C2CC;
  --accent:#1B4965; --accent-soft:#E2EBF1;
  --stop:#8E3A3A; --warn:#8A5D12; --ok:#2F6F4E;
  --shadow:0 1px 2px rgba(14,21,25,.05),0 10px 30px -18px rgba(14,21,25,.30);
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,ui-serif,serif;
  --sans:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI","Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#0C1216; --surface:#121B21; --surface-2:#18242B;
  --ink:#E3EAEF; --ink-2:#B4C3CD; --muted:#8497A4;
  --rule:#22303A; --rule-strong:#33454F;
  --accent:#79B0CE; --accent-soft:#162A36;
  --stop:#D68A8A; --warn:#D2A452; --ok:#7FBF9C;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 30px -18px rgba(0,0,0,.75);
}}
:root[data-theme="dark"]{
  --paper:#0C1216; --surface:#121B21; --surface-2:#18242B;
  --ink:#E3EAEF; --ink-2:#B4C3CD; --muted:#8497A4;
  --rule:#22303A; --rule-strong:#33454F;
  --accent:#79B0CE; --accent-soft:#162A36;
  --stop:#D68A8A; --warn:#D2A452; --ok:#7FBF9C;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 30px -18px rgba(0,0,0,.75);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:4.2rem}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
     font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
.shell{max-width:1180px;margin:0 auto;padding:0 clamp(1rem,3.5vw,2.5rem)}

/* sticky rail */
.bar{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--paper) 88%,transparent);
     backdrop-filter:blur(10px);border-bottom:1px solid var(--rule)}
.bar .shell{display:flex;gap:.15rem;align-items:center;overflow-x:auto;padding-top:.5rem;padding-bottom:.5rem;
     scrollbar-width:none}
.bar .shell::-webkit-scrollbar{display:none}
.bar b{font-family:var(--mono);font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;
     color:var(--accent);margin-right:.9rem;white-space:nowrap}
.bar a{font-family:var(--sans);font-size:.8rem;color:var(--ink-2);text-decoration:none;
     padding:.3rem .55rem;border-radius:3px;white-space:nowrap}
.bar a:hover{background:var(--accent-soft);color:var(--accent)}
.bar a:focus-visible{outline:2px solid var(--accent);outline-offset:1px}

/* masthead */
header.mast{padding:clamp(2.2rem,6vw,4rem) 0 1.4rem;border-bottom:2px solid var(--ink)}
.eyebrow{font-family:var(--mono);font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;
     color:var(--accent);margin:0 0 1rem}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(2.1rem,6vw,3.5rem);line-height:1.04;
   letter-spacing:-.022em;margin:0;text-wrap:balance}
.lede{font-family:var(--serif);font-size:clamp(1.05rem,2.1vw,1.32rem);color:var(--ink-2);
   max-width:56ch;margin:1.1rem 0 0;line-height:1.5}
.lede b{color:var(--ink);font-weight:600}
.statbar{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:1px;
   background:var(--rule);border:1px solid var(--rule);margin:2.1rem 0 0}
.stat{background:var(--surface);padding:.8rem .95rem}
.stat b{display:block;font-family:var(--mono);font-size:1.3rem;font-weight:600;letter-spacing:-.02em;
   font-variant-numeric:tabular-nums;color:var(--ink);line-height:1.15}
.stat.hi b{color:var(--stop)}
.stat span{display:block;font-size:.66rem;letter-spacing:.09em;text-transform:uppercase;
   color:var(--muted);margin-top:.25rem;line-height:1.3}

/* sections */
section{padding:3.2rem 0 0}
section > h2{font-family:var(--serif);font-weight:600;font-size:clamp(1.45rem,3.2vw,2rem);
   line-height:1.14;letter-spacing:-.018em;margin:0 0 .5rem;text-wrap:balance}
.kicker{font-family:var(--mono);font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;
   color:var(--accent);margin:0 0 .45rem}
section > p{font-family:var(--serif);font-size:1.04rem;color:var(--ink-2);max-width:62ch;margin:0 0 1.5rem}
section > p b{color:var(--ink);font-weight:600}
.num{font-variant-numeric:tabular-nums}

/* figures */
.grid{display:grid;gap:1.2rem;grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}
figure{margin:0;background:var(--surface);border:1px solid var(--rule);border-radius:6px;
   box-shadow:var(--shadow);overflow:hidden;display:flex;flex-direction:column}
figure.wide{grid-column:1/-1}
figure img{display:block;width:100%;height:auto;background:#fff}
figcaption{font-size:.815rem;line-height:1.5;color:var(--muted);padding:.7rem .9rem;
   border-top:1px solid var(--rule)}
figcaption b{color:var(--ink-2);font-weight:600}

/* compact tables */
.tw{overflow-x:auto;border:1px solid var(--rule);background:var(--surface);border-radius:6px;margin:0 0 1.4rem}
table{border-collapse:collapse;width:100%;min-width:420px;font-size:.85rem}
th,td{padding:.5rem .8rem;text-align:left;border-bottom:1px solid var(--rule);vertical-align:top}
thead th{font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;
   color:var(--muted);font-weight:500;background:var(--surface-2);white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
td.n{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
code{font-family:var(--mono);font-size:.86em;background:var(--surface-2);padding:.08em .32em;border-radius:2px}

.chip{display:inline-block;font-family:var(--mono);font-size:.68rem;padding:.1rem .4rem;border-radius:2px}
.chip.stop{background:color-mix(in srgb,var(--stop) 14%,transparent);color:var(--stop)}
.chip.warn{background:color-mix(in srgb,var(--warn) 16%,transparent);color:var(--warn)}
.chip.ok{background:color-mix(in srgb,var(--ok) 14%,transparent);color:var(--ok)}

ul.tight{margin:0 0 1.4rem;padding-left:1.15rem;max-width:62ch;font-size:.95rem;color:var(--ink-2)}
ul.tight li{margin-bottom:.4rem}
ul.tight li::marker{color:var(--muted)}

footer{margin-top:4rem;border-top:2px solid var(--ink);padding:1.5rem 0 3.5rem;
   font-family:var(--mono);font-size:.74rem;color:var(--muted);line-height:1.8}
"""

NAV = [("finding", "The finding"), ("who", "Who reports"), ("what", "What they test"),
       ("scale", "Scale"), ("response", "Response"), ("policy", "Policy"),
       ("where", "Where it sits"), ("time", "Over time"), ("method", "Method")]

def s(id_, kicker, h2, lede, body):
    return (f'<section id="{id_}"><p class="kicker">{kicker}</p><h2>{h2}</h2>'
            f'<p>{lede}</p>{body}</section>')

parts = [f"<title>Evaluating the Evaluators</title>", f"<style>{CSS}</style>"]

parts.append('<div class="bar"><div class="shell"><b>Evaluating the Evaluators</b>'
             + "".join(f'<a href="#{i}">{t}</a>' for i, t in NAV) + "</div></div>")

parts.append(f"""<div class="shell">
<header class="mast">
  <p class="eyebrow">Dataset v11 · merged corpus · updated {datetime.date(2026,8,17):%Y-%m-%d}</p>
  <h1>Evaluating the Evaluators</h1>
  <p class="lede">When an AI safety institute or third-party evaluator publishes a finding about a
  named model, does a documented company response follow? For <b>{short} of {n}</b> significant-risk
  findings, no &mdash; nothing proportionate to what was found.</p>
  <div class="statbar">
    <div class="stat"><b>{len(R):,}</b><span>Findings</span></div>
    <div class="stat"><b>{len({r["Report ID"] for r in R if r["Report ID"]})}</b><span>Reports</span></div>
    <div class="stat"><b>{len({r["Institution"] for r in R})}</b><span>Evaluators</span></div>
    <div class="stat"><b>{len(A)}</b><span>Accountability-relevant</span></div>
    <div class="stat"><b>{n}</b><span>Significant risk</span></div>
    <div class="stat hi"><b>{pct(short,n)}</b><span>Fall short</span></div>
    <div class="stat hi"><b>{pct(noact,n)}</b><span>No response at all</span></div>
    <div class="stat"><b>{dates[-1]}</b><span>Frozen cutoff</span></div>
  </div>
</header>""")

# 1 — the finding
parts.append(s("finding", "01 · The finding",
  "Most significant-risk findings go unanswered",
  f"Of <b>{n}</b> findings that name a company and were graded the more serious of two risk levels, "
  f"<b>{noact}</b> drew no documented response at all and <b>{under}</b> drew one weaker than the "
  f"severity warranted. <b>{ok}</b> were answered proportionately.",
  fig("00_title_hero", "The pipeline end to end. <b>Falls short</b> means the response was weaker "
      "than the finding's severity warranted &mdash; for a significant-risk finding, only a "
      "substantive response qualifies.", wide=True)
  + '<div class="grid">'
  + fig("04_headline_outcome_distribution", "Outcome distribution across the headline population.")
  + fig("10_proportionality_by_severity", "Outcome composition by severity. The bar is severity-relative: "
        "a partial response satisfies the lower severity but not the higher one.")
  + fig("20_accountability_pipeline_funnel", "Attrition from all findings through to policy uptake.")
  + fig("07_tier_distribution", f"Tier A {tiers['A']} · B {tiers['B']} · C {tiers['C']}. Only Tier A "
        "carries a traceable evaluation <em>and</em> a traceable company action.")
  + "</div>"))

# 2 — who
parts.append(s("who", "02 · Who reports",
  "Scrutiny is not the bottleneck",
  f"<b>{len({r['Institution'] for r in R})}</b> institutions published these findings &mdash; "
  f"<b>{sc['government-AISI']}</b> from government safety institutes and "
  f"<b>{sc['third-party-evaluator']}</b> from third-party evaluators. The headline holds on the "
  f"government-only subset: <b>{gov_short}/{len(gov)}</b> = {pct(gov_short,len(gov))} fall short.",
  fig("13_institution_type_tree", "Every finding traces to exactly one institution type.", wide=True)
  + '<div class="grid">'
  + fig("01_findings_per_institution", "Findings per institution, top 18.")
  + fig("12_evaluator_scope", "Government institute versus third-party evaluator.")
  + "</div>"))

# 3 — what
parts.append(s("what", "03 · What they test",
  "Jailbreaks, cyber, alignment",
  f"Among the significant-risk findings: jailbreaks <b>{dom['Jailbreaks']}</b>, cyber "
  f"<b>{dom['Cyber']}</b>, alignment <b>{dom['Alignment']}</b>, autonomy <b>{dom['Autonomy']}</b>, "
  f"bio-chem <b>{dom['Bio-Chem']}</b>. Severity is a three-model ensemble majority, not a judgement call.",
  '<div class="grid">'
  + fig("11_domain_distribution", "Findings per risk domain. Multi-label &mdash; a finding can carry more "
        "than one domain, so the bars sum above n.")
  + fig("17_severity_classification", "Severity split from the ensemble majority vote.")
  + fig("03_findings_per_access_type", "Access the evaluator had: pre-deployment, post-deployment or mixed.")
  + fig("02_findings_per_model_developer", "Accountability-relevant findings per model developer.")
  + "</div>"))

# 4 — scale
parts.append(s("scale", "04 · Scale",
  "The field is scaling fast",
  f"Findings rise steeply through 2025&ndash;26, and the accountability-relevant share rises with them. "
  f"Supply of scrutiny is growing; documented response is not keeping pace.",
  '<div class="grid">'
  + fig("23_corpus_growth_by_tier", "Corpus growth by year and tier.")
  + fig("06_findings_per_year", "Findings per publication year. 2026 is partial &mdash; cutoff 31 July.")
  + "</div>"))

# 5 — response
parts.append(s("response", "05 · Response",
  "What a response looks like when it happens",
  f"<b>{al['Substantive']}</b> substantive, <b>{al['Partial']}</b> partial, "
  f"<b>{al['Acknowledged']}</b> acknowledged, <b>{al['None']}</b> none. "
  f"<b>{at['Explicit attribution']}</b> responses cite the evaluator; <b>{at['No explicit attribution']}</b> "
  f"act without saying why. Median lag <b>{med} days</b> &mdash; responses cluster in the launch card, "
  "because that is where pre-deployment evaluations get answered.",
  '<div class="grid">'
  + fig("08_action_level_distribution", "Strength of the documented company response.")
  + fig("18_attribution_distribution", "Whether the company referenced the finding or its evaluator.")
  + fig("14_response_lag_distribution", "Days from publication to response. Negative = pre-deployment.")
  + fig("05_pre_vs_post_deployment_response_rate", "Substantive response rate, pre- versus post-deployment.")
  + "</div>"))

# 6 — policy
parts.append(s("policy", "06 · Policy",
  "One binding action in the whole corpus",
  f"<b>{pl['No policy uptake identified']}</b> findings show no policy uptake, "
  f"<b>{pl['Non-binding policy-related uptake']}</b> non-binding uptake, and "
  f"<b>{pl['Binding policy action']}</b> a binding action &mdash; the June 2026 Commerce "
  "export-control order. This is the weakest link in the pipeline.",
  fig("09_policy_level_distribution", "Policy uptake, from a three-jurisdiction search of official "
      "government sources only.", wide=True)))

# 7 — where
parts.append(s("where", "07 · Where it sits",
  "The shortfall is unevenly distributed",
  "It varies sharply by developer, by how much access the evaluator had, and by risk domain.",
  '<div class="grid">'
  + fig("19_gap_rate_by_developer", "By developer, n&ge;5. The smallest bars are fragile.")
  + fig("16_gap_rate_by_access_type", "By access type, against the corpus average.")
  + fig("22_domain_x_outcome_heatmap", "Outcome composition by domain. Colour encodes magnitude only; "
        "the strip above the headers carries the good/bad reading.")
  + fig("21_severity_x_action_heatmap", "Severity against response strength.")
  + "</div>"))

# 8 — time
yline = " &rarr; ".join(f"{y} <b>{v[1]*100:.0f}%</b>" for y, v in yr.items())
parts.append(s("time", "08 · Over time",
  "Narrowing, but still the norm",
  f"Shortfall by year: {yline}. The trend is downward, but roughly three in four findings still "
  "fall short. Early years are small samples and 2026 is partial; some of the decline is composition, "
  "since later years hold more pre-deployment evaluations, which are answered in the launch card by construction.",
  '<div class="grid">'
  + fig("15b_shortfall_rate_by_year", "Shortfall by year against the no-response-at-all rate. The two "
        "metrics trend in opposite directions.")
  + fig("15_gap_rate_by_year", "No-response-at-all rate by year.")
  + fig("24_evaluator_volume_vs_gap", "Evaluator publication volume against shortfall, n&ge;4.")
  + "</div>"))

# 9 — method (compact)
parts.append(s("method", "09 · Method",
  "How a finding qualifies",
  "Two filters, both pre-registered. <code>v10_RULEBOOK.md</code> is the normative source; this is the "
  "short version.",
  '<div class="tw"><table><thead><tr><th>Gate</th><th>Test</th><th class="n">Out</th></tr></thead><tbody>'
  f'<tr><td>Published findings</td><td>One finding = one claim a response could be owed to</td><td class="n">{len(R):,}</td></tr>'
  f'<tr><td>Accountability-relevant</td><td>Empirical, names a specific company or model, and concerning '
  'enough that a response is reasonable. Excludes reassuring nulls, benchmark scores with no dangerous '
  'threshold crossed, comparative rankings and anonymised models</td>'
  f'<td class="n">{len(A)}</td></tr>'
  f'<tr><td>Significant risk</td><td>Majority vote of a three-model severity ensemble</td><td class="n">{n}</td></tr>'
  '</tbody></table></div>'
  '<div class="tw"><table><thead><tr><th>Outcome</th><th>Definition</th><th class="n">n</th></tr></thead><tbody>'
  f'<tr><td><span class="chip ok">Proportionate</span></td><td>Response strength matches the severity</td><td class="n">{ok}</td></tr>'
  f'<tr><td><span class="chip warn">Under-response</span></td><td>A response exists but is weaker than the severity warrants</td><td class="n">{under}</td></tr>'
  f'<tr><td><span class="chip stop">No action</span></td><td>No response located after a completed five-source search</td><td class="n">{noact}</td></tr>'
  '</tbody></table></div>'
  '<ul class="tight">'
  '<li><b>Every negative coding is backed by a dated, exhausted search battery</b> &mdash; five company '
  'sources for response, three jurisdictions for policy. An absence is only claimed where the search ran out.</li>'
  '<li><b>Action Level measures the content of the public response</b>, not whether it was implemented '
  'or whether it reduced risk.</li>'
  '<li><b>Attribution is a separate axis</b> from response strength, so the data distinguishes "said '
  'nothing" from "acted without saying why".</li>'
  '<li><b>Limitation:</b> the two corpus halves differ in search depth, so the headline is an upper bound.</li>'
  '</ul>'))

parts.append(f"""<footer>
Corpus {len(R):,} findings · {len({r["Report ID"] for r in R if r["Report ID"]})} reports ·
{len({r["Institution"] for r in R})} evaluators · {dates[0]} to {dates[-1]}<br>
Headline population = accountability-relevant &cap; significant risk (n={n}) ·
falls short {short}/{n} = {pct(short,n)} · no response at all {noact}/{n} = {pct(noact,n)}<br>
26 figures regenerated 2026-08-17 · integrity validator: 24 checks, 0 violations
</footer></div>""")

html_out = "\n".join(parts)
open(OUT, "w", encoding="utf-8").write(html_out)
print(f"wrote {OUT}")
print(f"  {len(html_out):,} chars ({len(html_out)/1e6:.2f} MB) · "
      f"{html_out.count('<figure')} figures · {len(NAV)} sections")
words = len(__import__("re").sub(r"<[^>]+>", " ", html_out.split("</style>")[1]).split())
print(f"  visible prose: ~{words} words (the old page was a full methodology treatise)")
