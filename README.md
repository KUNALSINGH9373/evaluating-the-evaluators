# Evaluating the Evaluators — AISI Accountability Tracker

**Live site:** https://kunalsingh9373.github.io/evaluating-the-evaluators/

When government AI Safety Institutes (UK AISI, US CAISI and the International
Network) publish findings about frontier AI models, do companies respond? This
dashboard visualises a source-verified dataset of **456 findings from 211
reports** (Sep 2023 – Jul 2026) tracking the public-channel accountability
pipeline. The dataset itself is a screened subset of a systematic census —
6,712 publications enumerated across 46 evaluator organisations, of which
6,498 have been screened for evaluation-relevance to date.

## Structure

| File | Purpose |
|---|---|
| `v10.csv` | The dataset (v10) — single source of truth |
| `v10_RULEBOOK.md` | Full coding rulebook: inclusion rules, column definitions, evidentiary standard |
| `aisi_v6_CODEBOOK.md` | Older codebook (v6) — superseded by `v10_RULEBOOK.md`, kept for history |
| `sweep_state/` | Discovery-sweep checkpoint: census enumeration, screening ledger, in-progress reconciliation |
| `build_data.py` | Converts the CSV into `data.js` consumed by the site |
| `data.js` | Generated — do not edit by hand |
| `index.html` / `app.js` | The dashboard (static, no dependencies, no build step) |

## Updating the data

1. Replace `v10.csv` with the new sheet
2. Run `python3 build_data.py`
3. Commit and push — GitHub Pages redeploys automatically

## Method (short version)

Every cell in the dataset is **verified-real or deliberately empty**. A company
action counts as a response only if it is causally attributable to the finding,
sourced from the company's own primary document. Severity is ensemble-coded by
three cross-provider model votes. See the codebook for the full rules.

Built by [Kunal Singh](https://kunalsingh9373.github.io).
