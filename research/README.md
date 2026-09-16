# AISI Evals — Evaluating the Evaluators

Measures the **public-channel accountability pipeline**: when an AI safety institute or
third-party evaluator publishes a finding about a named model, does a documented company
response follow?

This folder is the research artifact behind the site at the repo root; see the top-level
`README.md` for the project, the scope and how to run everything.

## Layout

| Folder | Contents |
|---|---|
| **`dataset/`** | **`AISIEVAL.xlsx` — the dataset, and the only current copy.** 1,146 findings × 41 columns. Plus `AISIEVAL_validate.py`, a 31-check integrity validator that finds the workbook beside itself. Currently **PASS, 0 violations** |
| `charts/` | The 29 figures. Regenerate with the scripts in `scripts/`; every count derives from the workbook, so none can go stale |
| `deck/` | `AISIEVAL_10min.pptx` — 9 slides, editable in Keynote, timings in the presenter notes |
| `paper/` | Paper drafts and the findings-calculations workbook |
| `rulebook/` | `v10_RULEBOOK.md` (normative) and `v11_RULEBOOK.md` |
| `logs/` | Provenance, revision logs and the exclusion ledger. **See the warning below** |
| `scripts/` | Chart generators, `run_severity_ensemble.py`, and the severity prompt — v1.0 frozen, v1.1 active |
| `archive/` | Superseded workbooks and CSVs, kept only because each has a distinct hash |

The site that consumes this folder lives at the root of this repo, published to
<https://kunalsingh9373.github.io/evaluating-the-evaluators/>. Its `dataset.csv`, `data.js` and
`charts/` are all **derived** from this folder — regenerate them, never edit them directly.

## Headline

- **114 of 190** significant-risk findings — **60.0%** — drew no documented company response.
- **152 of 190** — **80.0%** — drew none proportionate to the finding's severity.
- Corpus: 1,146 findings · 457 reports · 46 institutions · Mar 2023 – Aug 2026.
- Tiers: A 233 · B 599 · C 314.
- Policy uptake: 1 binding action in the whole corpus.

The bar is severity-relative: a significant-risk finding needs a substantive response, a lesser one
needs only a partial. The measure scores the *content* of the public response, not whether it was
implemented or whether it reduced risk.

## Do not delete from logs/

- `AISIEVAL_notes_archive.csv` is the **sole surviving copy** of 7 pre-merge Finding IDs (immutable
  by §6), 47 pre-merge Report IDs, 55 prior Institution values, and the cleared values for two rows.
- `AISIEVAL_excluded_ordinary_accuracy.csv` holds the 11 rows removed under rulebook §4b, with all
  columns intact. It is the only record of them.

## Rules added 2026-08-17

- **§4b** ordinary accuracy and reliability exclusion — hallucination and generic factuality
  findings are out of scope, because the corpus never censused that literature.
- **§7b** D8, acute individual harm — a model urging a user toward suicide or self-harm is C1
  regardless of scale.
- **§7c** the three severity failure modes and how to tell them apart: taxonomy gap, lexical false
  positive, defective input. Includes a warning not to automate the review.

Severity prompt **v1.1** is now active (adds D8 and a deliberateness requirement to D5). v1.0 is
preserved frozen; existing votes are tagged `prompt_version 1.0` and were not re-run.

## Outstanding

- Dated Channel A batteries for 53 pre-2026 significant-risk rows coded "no response" — bookkeeping
  only, changes no values, but until it is done the headline is an upper bound.
- Two further §4b exclusions reported by the screening pass but not identified by ID.
- Five compound Weval rows needing source-level re-extraction; the corpus holds 18, all Tier B.
- Severity provenance (classifier quotes and reasons) covers 554 of the rows; the rest have vote
  labels only, so the audit that found today's four corrections cannot be run on them.
