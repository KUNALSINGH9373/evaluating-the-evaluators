# Figure captions — ICLR set

The ICLR PDFs carry no title and no explanatory text inside the image. Both live here,
ready to paste into `\caption{}`. Every figure is a vector PDF with live text, so it
stays searchable and selectable in the compiled paper.

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{figures/04_headline_outcome_distribution.pdf}
  \caption{\textbf{Outcome distribution.} Tier A $\cap$ C1, $n = 190$.}
  \label{fig:outcomes}
\end{figure}
```

### `00_title_hero.pdf`

**From published finding to documented response.** Boxes are schematic (not to scale); the outcome bar is proportional. A finding falls short when the named company shows no located public response (red) or only a partial or acknowledged one (orange).

### `01_findings_per_institution.pdf`

**Findings by evaluating institution.** Top 18 of 46 institutions.

### `02_findings_per_model_developer.pdf`

**Findings by model developer.** n = 1,146. A finding naming several developers counts once per developer, so the bars sum to more than the corpus total. Red marks the Tier A share.

### `03_findings_per_access_type.pdf`

**Findings by model access type.** n = 1,146.

### `04_headline_outcome_distribution.pdf`

**Outcome distribution.** Tier A \cap C1, n = 190.

### `05_pre_vs_post_deployment_response_rate.pdf`

**Substantive response rate by deployment stage.** Tier A \cap C1.

### `06_findings_per_year.pdf`

**Findings by publication year.** n = 1,146. 2026 is partial: the corpus cutoff is 29 August 2026.

### `07_tier_distribution.pdf`

**Tier distribution.** n = 1,146 findings.

### `08_action_level_distribution.pdf`

**Channel A: company response strength.** Tier A, n = 233.

### `09_policy_level_distribution.pdf`

**Channel B: policy uptake.** Tier A, n = 233.

### `10_proportionality_by_severity.pdf`

**Proportionality outcome by severity.** Tier A.

### `11_domain_distribution.pdf`

**Findings by risk domain.** Domains are multi-label, so the total exceeds the number of findings.

### `12_evaluator_scope.pdf`

**Outcome by evaluator type.** Significant-risk findings that name a company, n = 190. Bars are 100\% stacked because the two groups are of very unequal size; counts are printed inside.

### `13_institution_type_tree.pdf`

**Findings by institution type.** Bar length is the finding count on one scale shared across all four branches, showing the top five institutions per type. Compound Institution Type values (e.g. "Government;Lab") fold into their primary type, so the four branches sum to 1,146.

### `14_response_lag_distribution.pdf`

**Response lag distribution.** Tier A, n = 88. Days between publication and company response on a symlog scale; a negative lag means the company documented its response before the finding was published, which happens under coordinated pre-deployment disclosure.

### `15_gap_rate_by_year.pdf`

**Accountability gap rate by publication year.** Tier A \cap C1.

### `15b_shortfall_rate_by_year.pdf`

**Shortfall rate by publication year.** Tier A \cap C1, n = 190. 2023 and 2024 are small samples and 2026 is partial (cutoff 29 August 2026). The two metrics trend in opposite directions: part of the decline in shortfall reflects composition, since later years hold more pre-deployment evaluations, which are answered in the launch card by construction.

### `16_gap_rate_by_access_type.pdf`

**Accountability gap rate by model access type.** Tier A \cap C1.

### `17_severity_classification.pdf`

**Severity classification.** n = 1,146, three-model ensemble majority. C1 + C2 + unresolved sums to the corpus.

### `18_attribution_distribution.pdf`

**Attribution of company responses.** Tier A, n = 233.

### `20_accountability_pipeline_funnel.pdf`

**The accountability pipeline.** Tier A \cap C1. Attrition at each stage of the pipeline.

### `21_severity_x_action_heatmap.pdf`

**Severity \times company response.** Tier A.

### `22_domain_x_outcome_heatmap.pdf`

**Outcome by risk domain.** Tier A.

### `23_corpus_growth_by_tier.pdf`

**Corpus growth by publication year.** By tier.

### `24_evaluator_volume_vs_gap.pdf`

**Accountability gap rate by evaluator.** Tier A \cap C1, evaluators with n \geq 4. Marker area is proportional to the number of findings published; the dashed line is the corpus average.

### `25_what_is_a_finding.pdf`

**Finding eligibility criteria.** The three conditions of \S2, with what qualifies and what does not.

### `26_action_level_scale.pdf`

**The Action Level scale.** The strength of the located company response, with a Tier A example of each level.

### `27_three_outcomes.pdf`

**Three findings, three outcomes.** One worked example of each proportionality outcome.

### `28_three_findings_provenance.pdf`

**Three findings, by source.** The same three 2026 findings traced to their primary sources.

### `neurips/fig1_pipeline.pdf`

**From published finding to documented response.** 114 of 190 significant-risk findings about named frontier systems drew no documented company response. Boxes are schematic, not to scale; the outcome bar is proportional. A finding falls short when the company response is absent, or weaker than the finding's severity warrants.

### `neurips/fig2_severity_x_action.pdf`

**The proportionality matrix.** Proportionality is a function of these two columns and nothing else. The bar is severity-relative: C1 needs a substantive response, C2 needs at least a partial one.

### `neurips/figA2_access_type.pdf`

**Corpus and shortfall by access type.** (a) the corpus by access type, n = 1,146; (b) significant-risk findings with no located response, by access type.
