# Research artifact — Evaluating the Evaluators

Everything behind the site at the repo root: the dataset, the rules that govern it, the scripts
that read it, and the provenance of every change. See the top-level `README.md` for the project,
the scope and the commands.

**Corpus** — 1,146 findings · 457 reports · 46 institutions · 39 columns · 2023-03-17 to
2026-08-27. Tier A 233 · B 599 · C 314. Cutoff 2026-08-29.

**Headline** — of the 190 significant-risk (Tier A ∩ C1) findings that name a company:
**114 (60.0%)** drew no documented response, and **152 (80.0%)** drew none proportionate to the
finding's severity. Policy uptake across the whole corpus: **1 binding action**, 46 non-binding.

The bar is severity-relative: a significant-risk finding needs a substantive response, a lesser one
only a partial. The measure scores the *content* of the public response, not whether it was
implemented or whether it reduced risk.

## Layout

| Folder | Contents |
|---|---|
| **`dataset/`** | **`AISIEVAL_V13.xlsx`, sheet `AISIEVAL_V13` — the source of truth, and the only current copy.** Plus `AISIEVAL_validate.py`, a 29-check integrity validator that finds the workbook beside itself. Currently **PASS, 0 violations** |
| `rulebook/` | `v11_RULEBOOK.md` — **normative**. Scope gate, finding eligibility, one-company-per-row, report identity, severity, the evidentiary standard, and the changelog. `v10_RULEBOOK.md` is its superseded predecessor |
| `protocol/` | `SEARCH_PROTOCOL.md` (discovery and screening), `RESPONSE_SEARCH_PROTOCOL.md` (the Channel A/B/C response battery), `codebook.md`, and the superseded v6 codebook and v10 methodology |
| `scripts/` | Every program that touches the workbook: chart generators, `all_stats.py`, `verify_charts.py`, `fetch.py`, and the merge, sort, repair and diff tools. All reach the data through `dataset_source.py` and nothing else |
| `charts/` | The 29 figures at full resolution, plus `neurips/` — three paper-specific renderings and two hand-written LaTeX tables |
| `severity/` | `severity_prompt_v1.0_FROZEN.txt` and the active v1.1 prompt, `run_severity_ensemble.py`, and the raw per-finding votes: 846 records over 843 findings, plus a 60-record calibration set |
| `sweep/` | The discovery census — `master_ledger.csv`, cached enumerations, 56 per-evaluator screening slices under `eval_slices/`, 49 ledger slices and the 106-file `sweep_state/` checkpoint |
| `paper/` | `DRAFT_6.2.md`, the LaTeX source under `latex/`, the submission bundles under `submission/`, and the Tier A table exports |
| `logs/` | Provenance: correction, restoration and deletion logs, audit reports, reconciliation ledgers, and the exclusion records. **See the warning below** |
| `archive/`, `working/` | Superseded workbooks, CSVs and intermediate files, kept because each has a distinct hash |
| `deck/` | `AISIEVAL_10min.pptx` — a 10-minute presentation of the project |

`dataset.csv`, `data.js` and `charts/` at the repo root are all **derived** from this folder.
Regenerate them; never edit them directly.

## Do not delete from logs/

- `AISIEVAL_notes_archive.csv` is the **sole surviving copy** of 7 pre-merge Finding IDs (immutable
  by §6), 47 pre-merge Report IDs, 55 prior Institution values, and the cleared values for two rows.
- `AISIEVAL_excluded_ordinary_accuracy.csv` holds the 11 rows removed under rulebook §4b, with all
  columns intact. It is the only record of them.

`logs/fetch_cache/` is **not** published here: 158 MB of raw HTTP responses that `fetch.py`
regenerates on demand. Everything else in `logs/` is.

## Standing caveats

- **The paper is not anonymized.** `paper/DRAFT_6.2.md` and `paper/latex/paper.tex` carry the
  author block, and the appendices link to a personal domain.
- **The authorship audit covers 15 of 59 institutions.** The rest are attributed by cluster, not
  checked paper by paper; roughly 20 Shanghai AI Lab papers are the largest unchecked group.
- **Severity votes cover 843 of 1,146 findings.** The remainder carry a majority label without the
  per-model vote record, so a vote-level audit cannot be run on them.
- **Reachability is not an eligibility test.** A URL that fails to load is never grounds for
  removing a row; link checking goes through the `fetch.py` retrieval ladder, which distinguishes
  a blocked request from an absent document.
