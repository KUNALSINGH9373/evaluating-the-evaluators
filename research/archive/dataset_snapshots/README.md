# Historical dataset snapshots

Rescued from the orphaned `site/` directory before it was deleted (2026-09-05).

- `aisi_v9.csv` — the v9 corpus, 351 findings. This was the only copy anywhere.
- `v10_backup_before_prop_fix.csv` — the v10 CSV as it stood immediately before the
  proportionality correction. Cited by name in `protocol/codebook.md` (changelog,
  "Pre-edit CSV backed up to `v10_backup_before_prop_fix.csv`"), so the reference would
  have dangled if this file were lost. Only copy anywhere.

`v10.csv` was not moved here: an identical copy already exists at `archive/v10.csv`.

None of these is readable through `scripts/dataset_source.py` and none is an input to any
analysis. The live dataset is `dataset/AISIEVAL_V13.xlsx` and nothing else.
