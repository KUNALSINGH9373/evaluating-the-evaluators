# AISIEVAL — figure set

Generated, never edited. `bash scripts/build_charts.sh` from the project root rebuilds all 28
top-level figures plus the ICML set in `neurips/`; `scripts/verify_charts.py` then recomputes every
plotted quantity from the workbook and must print **PASS**. If a figure disagrees with the paper,
change the generator and rebuild — do not touch a `.png`.

Source of truth is `dataset/AISIEVAL_V13.xlsx`, sheet `AISIEVAL_V13`, read only through
`scripts/dataset_source.py`. Set `AISIEVAL_WORKBOOK` to point the whole pipeline at another copy.

## Current corpus (2026-09-07)

**1,140 findings · 458 reports · 458 source URLs · 46 institutions · 2023-03-17 to 2026-08-27**
Tier A 231 · Tier B 597 · Tier C 312 · Tier A ∩ C1 (headline population) 188

**HEADLINE: 150/188 = 79.8%** (Wilson 73–85%) of significant-risk findings drew a response falling
short of one proportionate to their severity. **112/188 = 59.6%** (52–66%) drew no documented
response at all — the stricter subset, not an alternative headline. Both figures appear in the
paper and on the dashboard, the shortfall figure leading in each.

"Falls short" is the complement of `Proportionate` under the §9 severity × Action Level matrix, and
the bar is severity-relative: for C1 only `Substantive` qualifies, whereas for C2 `Partial` also
counts. It is a reporting label, not a rulebook term — define it once on first use.

Clustering: the 188 findings sit in 102 reports, ICC 0.62, design effect 1.52, effective n ≈ 124.

## Layout

- `*.png` — the 28 numbered figures, the working set the website draws from.
- `neurips/` — the ICML submission set: paper-numbered figures plus the two hand-written `.tex`
  tables. See `neurips/README.md`; `table2_institutions.tex` holds no corpus statistics, so its
  file date is expected to lag the workbook.
