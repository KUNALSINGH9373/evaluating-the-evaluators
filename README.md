# Evaluating the Evaluators — AISI Accountability Tracker

**Live site:** https://kunalsingh9373.github.io/evaluating-the-evaluators/

When government AI Safety Institutes (UK AISI, US CAISI and the International
Network) publish findings about frontier AI models, do companies respond? This
dashboard visualises a source-verified dataset of **281 findings from 72
reports** (Jan 2024 – Jun 2026) tracking the public-channel accountability
pipeline.

## Structure

| File | Purpose |
|---|---|
| `aisi_v6.csv` | The dataset (v6, verified 2026-07-16) — single source of truth |
| `aisi_v6_CODEBOOK.md` | Full codebook: inclusion rules, column definitions, evidentiary standard |
| `build_data.py` | Converts the CSV into `data.js` consumed by the site |
| `data.js` | Generated — do not edit by hand |
| `index.html` / `app.js` | The dashboard (static, no dependencies, no build step) |

## Updating the data

1. Replace `aisi_v6.csv` with the new sheet
2. Run `python3 build_data.py`
3. Commit and push — GitHub Pages redeploys automatically

## Method (short version)

Every cell in the dataset is **verified-real or deliberately empty**. A company
action counts as a response only if it is causally attributable to the finding,
sourced from the company's own primary document. Severity is ensemble-coded by
three cross-provider model votes. See the codebook for the full rules.

Built by [Kunal Singh](https://kunalsingh9373.github.io).
