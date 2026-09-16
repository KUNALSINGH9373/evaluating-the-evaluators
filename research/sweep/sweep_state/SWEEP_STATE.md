# Evidence Sweep — State Snapshot (2026-08-01, revised 2026-08-14)

Durable checkpoint of the census sweep so it survives session loss / usage limits.
All files in this folder are the recoverable state.

## ⚠ 2026-08-14 revisions — read before resuming

**0. Roster corrections applied — 46 → 33 organisations. Ledger is now 6,579 rows,
of which 2,116 belong to retired venues; the ACTIVE CORPUS is 4,463 and 597 rows are unresolved
(86.6% resolved). `INCLUDED` unchanged at 219.**

| | Retired / filtered | Effect |
|---|---|---|
| **A** | Ai2, UC Berkeley, Thorn, EPFL, Yale, Stanford, Oxford | Co-author affiliations mis-read as evaluators. 1,400 rows → `EXCLUDED - not a roster org` |
| **B** | EU AI Office, Kenya, Canada, Australia, India, Germany | Zero-yield Network members. 716 rows → `EXCLUDED - venue retired` |
| **C** | RAND format + topic gates | 397 rows → `EXCLUDED - out-of-scope format` (253) / `EXCLUDED - off-topic` (144). RAND 756 → 359 |
| **D** | Backfill | 81 enumerated-but-never-ledgered items added as `PENDING-FETCH` |

**Enumeration is NOT complete** — the earlier claim is withdrawn. 24 reports already in v10.csv were
never enumerated (4 UK AISI, 4 Holistic AI, 5 Shanghai, 2 CIP/Weval…). Diagnose these *before*
further screening; re-enumeration may change the corpus base.


1. **Company self-reports are now a HARD DROP** (rulebook §1). A model developer's report on its
   own model(s) with no external evaluator named is out of scope. Company venues stay on the
   roster but use a **narrowed test**: "is an external evaluator named?" — not "does it contain a
   finding?". 233 rows are now `PENDING-EVALUATOR-CHECK` (213 ex-`PENDING-FETCH`, 20
   ex-`INCLUDED`); 1 confirmed solo self-eval is `EXCLUDED - company self-report`; 7 company-venue
   items keep `INCLUDED` under the §1 carve-out with their Report IDs backfilled. This removes
   226 rows from `eval_candidates_to_fetch.csv` (673 → 447) and makes the rest much cheaper.
2. **The reconciliation key is STALE — rebuild it first.** `known_reports.json` holds 153 Report
   IDs; v10.csv has **211**. The 59-ID gap made the dedup pass mislabel **34 already-present
   reports as "genuinely new"**, and 31 of the 139 "candidate misses" are likewise already in v10.
   Regenerate `known_reports.json` from v10.csv before any triage, and match by URL **and**
   normalised title (Report IDs are absent on candidate-miss rows by definition).
3. **Corrected new-material count:** of the 58 originally flagged "genuinely new" — 34 already in
   v10, 16 removed as company self-reports (logged in `company_self_reports_excluded.json`),
   leaving **8 third-party candidates** in `genuinely_new_dedup.json` (42 entries total after the
   company removals; the remaining surplus over 8 is the already-in-v10 set still to be pruned
   once the key is rebuilt).

The decision counts in "Where things stand" below are the 2026-08-01 originals and are now
superseded by `master_ledger.csv` (6,498 rows: 4,894 not-an-evaluation · 598 no-findings ·
424 PENDING-FETCH · 233 PENDING-EVALUATOR-CHECK · 219 INCLUDED · 83 duplicate/secondary ·
16 POST-CUTOFF · 15 no-named-evaluator · 15 out-of-scope · 1 company self-report).

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
| Fetch-screen the remaining 424 PENDING-FETCH eval-candidates | 🔄 in progress (workflow wef3k70ua; ~30 done) |
| — the 4 COMPANY sources (OpenAI, Anthropic, GDM, Meta) | ♻️ **rescoped 2026-08-14** — 233 rows now `PENDING-EVALUATOR-CHECK`, needing only the named-evaluator question, not a full screen. Cheap; do these first |
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
