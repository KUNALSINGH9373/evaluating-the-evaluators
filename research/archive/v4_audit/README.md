# v4-era audit working directory

Moved here from `~/aisi-v4-audit/` on 2026-09-05, when the project was tidied so that nothing
related to it sat loose in the home folder. Content dates from 2026-07-15 to 2026-07-23.

**Nothing here was deleted, because 109 of the 110 files had no copy anywhere inside the
project.** It is unique working material from the v4 stage, superseded by V13 but not
reproducible from it.

- `PROJECT_CONTEXT_AND_6MONTH_PLAN.md` — a self-contained strategic brief written 2026-07-19,
  including a six-month extension plan. **This one is not history.** A copy has been placed at
  the project root; this is the original.
- `phase1_report.md` — mechanical integrity audit of the 293-row v4 sheet, 495 flags. Superseded
  by `dataset/AISIEVAL_validate.py`, which enforces the same class of rule automatically.
- `phase2_disposition_ledger.csv`, `phase1_fixlist.csv`, `phase1_flags.json` — the fix ledger from
  that audit.
- `chanA_batch*.json`, `chanA_validate.json` — Channel A search batches from the v4 stage.
- `neglag_sweep_*` — the negative-lag investigation.
- `v8_apply/`, `domtag/`, `findtype/` — intermediate staging from later stages.

None of it is read by any current script. The live dataset is `dataset/AISIEVAL_V13.xlsx`.
