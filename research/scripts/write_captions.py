#!/usr/bin/env python3
"""CAPTIONS.md — the text the ICLR build strips out of the artwork.

Every title and every explanatory sentence that the default figures draw inside the image is
removed from the ICLR PDFs, because a conference figure carries that text in its LaTeX
\\caption: there it is styled by the document, sized by the document, and searchable as part of
the caption rather than as a stray text run inside a graphic.

Removing it and then losing it would be worse than leaving it in, so this file writes the
removed text back out, one entry per figure, ready to paste into \\caption{}.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palette import CHARTS_OUT

# (stem, title, caption body). The body is the sentence the ICLR build suppresses, rewritten
# only where the figure's own wording referred to itself ("the figure above", "this chart").
FIGS = [
 ("00_title_hero", "From published finding to documented response",
  "Boxes are schematic (not to scale); the outcome bar is proportional. A finding falls short "
  "when the named company shows no located public response (red) or only a partial or "
  "acknowledged one (orange)."),
 ("01_findings_per_institution", "Findings by evaluating institution", "Top 18 of 46 institutions."),
 ("02_findings_per_model_developer", "Findings by model developer",
  "n = 1,146. A finding naming several developers counts once per developer, so the bars sum to "
  "more than the corpus total. Red marks the Tier A share."),
 ("03_findings_per_access_type", "Findings by model access type", "n = 1,146."),
 ("04_headline_outcome_distribution", "Outcome distribution", "Tier A \\cap C1, n = 190."),
 ("05_pre_vs_post_deployment_response_rate", "Substantive response rate by deployment stage",
  "Tier A \\cap C1."),
 ("06_findings_per_year", "Findings by publication year",
  "n = 1,146. 2026 is partial: the corpus cutoff is 29 August 2026."),
 ("07_tier_distribution", "Tier distribution", "n = 1,146 findings."),
 ("08_action_level_distribution", "Channel A: company response strength", "Tier A, n = 233."),
 ("09_policy_level_distribution", "Channel B: policy uptake", "Tier A, n = 233."),
 ("10_proportionality_by_severity", "Proportionality outcome by severity", "Tier A."),
 ("11_domain_distribution", "Findings by risk domain",
  "Domains are multi-label, so the total exceeds the number of findings."),
 ("12_evaluator_scope", "Outcome by evaluator type",
  "Significant-risk findings that name a company, n = 190. Bars are 100\\% stacked because the "
  "two groups are of very unequal size; counts are printed inside."),
 ("13_institution_type_tree", "Findings by institution type",
  "Bar length is the finding count on one scale shared across all four branches, showing the "
  "top five institutions per type. Compound Institution Type values (e.g. \"Government;Lab\") "
  "fold into their primary type, so the four branches sum to 1,146."),
 ("14_response_lag_distribution", "Response lag distribution",
  "Tier A, n = 88. Days between publication and company response on a symlog scale; a negative "
  "lag means the company documented its response before the finding was published, which "
  "happens under coordinated pre-deployment disclosure."),
 ("15_gap_rate_by_year", "Accountability gap rate by publication year", "Tier A \\cap C1."),
 ("15b_shortfall_rate_by_year", "Shortfall rate by publication year",
  "Tier A \\cap C1, n = 190. 2023 and 2024 are small samples and 2026 is partial (cutoff 29 "
  "August 2026). The two metrics trend in opposite directions: part of the decline in shortfall "
  "reflects composition, since later years hold more pre-deployment evaluations, which are "
  "answered in the launch card by construction."),
 ("16_gap_rate_by_access_type", "Accountability gap rate by model access type", "Tier A \\cap C1."),
 ("17_severity_classification", "Severity classification",
  "n = 1,146, three-model ensemble majority. C1 + C2 + unresolved sums to the corpus."),
 ("18_attribution_distribution", "Attribution of company responses", "Tier A, n = 233."),
 ("20_accountability_pipeline_funnel", "The accountability pipeline",
  "Tier A \\cap C1. Attrition at each stage of the pipeline."),
 ("21_severity_x_action_heatmap", "Severity \\times company response", "Tier A."),
 ("22_domain_x_outcome_heatmap", "Outcome by risk domain", "Tier A."),
 ("23_corpus_growth_by_tier", "Corpus growth by publication year", "By tier."),
 ("24_evaluator_volume_vs_gap", "Accountability gap rate by evaluator",
  "Tier A \\cap C1, evaluators with n \\geq 4. Marker area is proportional to the number of "
  "findings published; the dashed line is the corpus average."),
 ("25_what_is_a_finding", "Finding eligibility criteria",
  "The three conditions of \\S2, with what qualifies and what does not."),
 ("26_action_level_scale", "The Action Level scale",
  "The strength of the located company response, with a Tier A example of each level."),
 ("27_three_outcomes", "Three findings, three outcomes",
  "One worked example of each proportionality outcome."),
 ("28_three_findings_provenance", "Three findings, by source",
  "The same three 2026 findings traced to their primary sources."),
 ("neurips/fig1_pipeline", "From published finding to documented response",
  "114 of 190 significant-risk findings about named frontier systems drew no documented company "
  "response. Boxes are schematic, not to scale; the outcome bar is proportional. A finding falls "
  "short when the company response is absent, or weaker than the finding's severity warrants."),
 ("neurips/fig2_severity_x_action", "The proportionality matrix",
  "Proportionality is a function of these two columns and nothing else. The bar is "
  "severity-relative: C1 needs a substantive response, C2 needs at least a partial one."),
 ("neurips/figA2_access_type", "Corpus and shortfall by access type",
  "(a) the corpus by access type, n = 1,146; (b) significant-risk findings with no located "
  "response, by access type."),
]

present = {os.path.relpath(os.path.join(dp, f), CHARTS_OUT)[:-4]
           for dp, _, fs in os.walk(CHARTS_OUT) for f in fs if f.endswith(".pdf")}

lines = ["# Figure captions — ICLR set", "",
         "The ICLR PDFs carry no title and no explanatory text inside the image. Both live here,",
         "ready to paste into `\\caption{}`. Every figure is a vector PDF with live text, so it",
         "stays searchable and selectable in the compiled paper.", "",
         "```latex",
         "\\begin{figure}[t]",
         "  \\centering",
         "  \\includegraphics[width=\\linewidth]{figures/04_headline_outcome_distribution.pdf}",
         "  \\caption{\\textbf{Outcome distribution.} Tier A $\\cap$ C1, $n = 190$.}",
         "  \\label{fig:outcomes}",
         "\\end{figure}",
         "```", ""]
missing = []
for stem, title, body in FIGS:
    if stem not in present:
        missing.append(stem)
        continue
    lines += [f"### `{stem}.pdf`", "",
              f"**{title}.** {body}", ""]
orphans = sorted(present - {s for s, _, _ in FIGS})
if missing:
    lines += ["---", "", "**No PDF was produced for:** " + ", ".join(f"`{m}`" for m in missing), ""]
if orphans:
    lines += ["---", "", "**PDF with no caption written:** " + ", ".join(f"`{o}`" for o in orphans), ""]

p = os.path.join(CHARTS_OUT, "CAPTIONS.md")
open(p, "w", encoding="utf-8").write("\n".join(lines))
print(f"  wrote {os.path.relpath(p, os.path.dirname(CHARTS_OUT))}"
      f"  ({len(FIGS) - len(missing)} captions"
      + (f", {len(missing)} missing" if missing else "")
      + (f", {len(orphans)} uncaptioned" if orphans else "") + ")")
