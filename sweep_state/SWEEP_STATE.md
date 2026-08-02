# Evidence Sweep — State Snapshot (2026-08-01)

Durable checkpoint of the census sweep so it survives session loss / usage limits.
All files in this folder are the recoverable state.

## Where things stand

- **Roster:** 46 organisations derived (Int'l Network members + AI Evaluator Forum members +
  every org already in the dataset + 4 company-artifact sources). Frozen in
  `cached_enumerations.json` keys.
- **Enumeration:** COMPLETE. All 46 venues' full publication lists captured = **6,712 items**,
  cached in `cached_enumerations.json`. Nothing un-listed.
- **Screening:** partial — see `master_ledger.csv` (6,377 rows; the rest are the ~335 within
  already-screened venues that dedup collapsed). Decision breakdown:
  - INCLUDED **187** (92 of the 153 existing Report IDs re-found)
  - EXCLUDED – not an evaluation **4,834** (title-triage, budget-free)
  - EXCLUDED – no findings **592**, duplicate/secondary **81**, no named evaluator **15**,
    out-of-scope **15**, POST-CUTOFF **16**
  - **PENDING-FETCH 651** ← the only work left: eval-candidates from the 29 un-fetched venues
    that need full-text confirmation.

## What's done vs. pending

| Component | State |
|---|---|
| 17 venues fully fetch-screened (UK AISI, CAISI, J-AISI, Korea, Singapore, France, METR, SecureBio, Apollo, CAIS, Canada, Australia, India, Transluce, CIP, HAL, AVERI) | ✅ done (885 rows) |
| Title-exclusion of 4,834 non-evaluations across the other 29 venues | ✅ done, logged |
| Fetch-screen the ~651 PENDING eval-candidates | 🔄 in progress (workflow wef3k70ua; ~30 done) |
| — of which the 4 COMPANY sources (OpenAI, Anthropic, GDM, Meta ≈ 226 items) | ⛔ highest-value, not yet confirmed screened |
| Reconciliation (all 153 Report IDs) + candidate-miss triage | ⛔ waits on fetch-screen |
| PRISMA numbers for paper §3.1 | ⛔ waits on reconciliation |

## How to resume (cheapest path)

The expensive part (enumeration) is done and cached. Remaining = fetch-screen the PENDING-FETCH
rows only, headline (gov + company) first.

1. The prepared, headline-first chunk files are `chunks_headline.json` (253 items) and
   `chunks_thirdparty.json` (420) in the session scratchpad; the candidate list is
   `eval_candidates_to_fetch.csv` here.
2. Lean workflow script: `.../workflows/scripts/eval-sweep-lean-wf_4f71502b-684.js` —
   resume with `resumeFromRunId: "wf_4f71502b-684"` (done chunks replay from cache).
3. On completion: merge `eval_slices/*.csv` into `master_ledger.csv`, flip matching PENDING rows,
   then run reconciliation: every one of the 153 known Report IDs must be INCLUDED; INCLUDED
   items with no report_id = candidate misses → triage.

## Roster discoveries already banked (act on in the paper)

- Int'l Network **renamed** (Dec 2025) → "International Network for Advanced AI Measurement,
  Evaluation and Science" — update §2.1 terminology.
- **AI Evaluator Forum** founding members (Dec 2025): Transluce, METR, RAND, Princeton HAL,
  SecureBio, CIP, Meridian Labs, AVERI.
- **Germany AISI** approved 2026-06-09 (pre-launch); **IndiaAI Safety Institute** since Jan 2025;
  **Kenya** is a network member (its ministry site is ~all PR, near-zero evals).
- **Meridian Labs** and **Gray Swan** are roster orgs with no dataset presence yet.

## Files here

- `master_ledger.csv` — the consolidated 6,377-row screening ledger (authoritative).
- `cached_enumerations.json` — all 6,712 enumerated items (the free, complete listing).
- `eval_candidates_to_fetch.csv` — the 673 eval-candidates, tier-prioritised.
- `known_reports.json` / `known_orgs.json` — the 153-report + 51-org reconciliation keys.
- `eval_slices_backup/` — raw lean-sweep fetch decisions so far.
- `triage_pass.csv`, `screening_ledger_PARTIAL.csv` — intermediate artifacts.
