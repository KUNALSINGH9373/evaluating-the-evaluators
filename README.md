# Evaluating the Evaluators — AISI Accountability Tracker

**Live site:** https://kunalsingh9373.github.io/evaluating-the-evaluators/

When government AI Safety Institutes (UK AISI, US CAISI and the International
Network) publish findings about frontier AI models, do companies respond? This
dashboard visualises a source-verified dataset of **345 findings from 157
reports** (Sep 2023 – Jul 2026) tracking the public-channel accountability
pipeline.

## Structure

| File | Purpose |
|---|---|
| `aisi_v9.csv` | The dataset (v9) — single source of truth |
| `aisi_v6_CODEBOOK.md` | Codebook: inclusion rules, column definitions, evidentiary standard (last updated for v6; rules still apply, some column vocabulary has since evolved — due for a refresh) |
| `build_data.py` | Converts the CSV into `data.js` consumed by the site |
| `data.js` | Generated — do not edit by hand |
| `index.html` / `app.js` | The dashboard (static, no dependencies, no build step) |

## Updating the data

1. Replace `aisi_v9.csv` with the new sheet
2. Run `python3 build_data.py`
3. Commit and push — GitHub Pages redeploys automatically

## Method (short version)

Every cell in the dataset is **verified-real or deliberately empty**. A company
action counts as a response only if it is causally attributable to the finding,
sourced from the company's own primary document. Severity is ensemble-coded by
three cross-provider model votes. See the codebook for the full rules.

Built by [Kunal Singh](https://kunalsingh9373.github.io).
