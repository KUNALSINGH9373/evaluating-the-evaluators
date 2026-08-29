# Evaluating the Evaluators — AISI Accountability Tracker

**Live site:** https://kunalsingh9373.github.io/evaluating-the-evaluators/

When government AI Safety Institutes (UK AISI, US CAISI and the International
Network) and independent third-party evaluators publish findings about frontier
AI models, do companies respond? This dashboard visualises a source-verified
dataset of **1,001 findings from 438 reports by 47 evaluating institutions**
(Jan 2023 – Jul 2026) tracking the public-channel accountability pipeline. The
dataset itself is a screened subset of a systematic census — 6,712 publications
enumerated across 46 evaluator organisations, of which 6,684 have been screened
for evaluation-relevance to date.

Headline: of the 146 significant-risk (Tier A ∩ C1) findings, **90 (61.6%) drew
no documented company response at all** and **116 (79.5%) drew a response that
fell short of what the severity warranted**.

## Structure

| File | Purpose |
|---|---|
| `AISI  Eval Findings.xlsx`, sheet `AISIEVAL_V12` | **The single source of truth.** Read in place; never rewritten, moved or renamed. |
| `dataset.csv` | Generated export of `AISIEVAL_V12` — all 1,001 rows, all 39 columns, header verbatim. Do not edit by hand. |
| `data.js` | Generated — `window.AISI = {meta, findings}` consumed by `app.js`. Do not edit by hand. |
| `build_data.py` | Reads the workbook through `dataset_source.py` and writes `dataset.csv` + `data.js` |
| `codebook.md` | Full coding rulebook: inclusion rules, tier test, column definitions, evidentiary standard |
| `aisi_v6_CODEBOOK.md` | Older codebook (v6) — superseded by `codebook.md`, kept for history |
| `SEARCH_PROTOCOL.md` | Full search / screening procedure |
| `sweep_state/` | Discovery-sweep checkpoint: census enumeration, screening ledger, in-progress reconciliation |
| `charts/` | Web-sized copies of the paper figures shown in the gallery |
| `index.html` / `app.js` | The dashboard (static, no dependencies, no build step) |

## Updating the data

1. Edit the `AISIEVAL_V12` sheet in `AISI  Eval Findings.xlsx` — it is the only place data changes
2. Run `python3 build_data.py` (regenerates `dataset.csv` and `data.js` from the sheet)
3. Commit and push — GitHub Pages redeploys automatically

`build_data.py` imports the shared accessor `dataset_source.py`; set `AISI_SCRIPTS` if it does not
live at `~/MATS/Research/AISI_Evals/scripts`.

## Method (short version)

Every cell in the dataset is **verified-real or deliberately empty**. A company
action counts as a response only if it is causally attributable to the finding,
sourced from the company's own primary document. Severity is ensemble-coded by
three cross-provider model votes. See the codebook for the full rules.

Built by [Kunal Singh](https://kunalsingh9373.github.io).
