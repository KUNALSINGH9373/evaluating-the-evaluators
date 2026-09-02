# Evaluating the Evaluators — research artifact

Everything needed to reproduce the paper. No figure or statistic is transcribed by hand;
all of them regenerate from one workbook by the scripts here.

## Reproduce

    python3 -m pip install -r requirements.txt

Then, from this directory, in order:

    python3 dataset/AISIEVAL_validate.py     # structural validation      -> PASS, 0 violations
    python3 scripts/all_stats.py             # every reported quantity
    bash    scripts/build_charts.sh          # all 28 figures -> charts/
    python3 scripts/verify_charts.py         # figures vs workbook        -> PASS
    python3 scripts/find_duplicates.py       # six duplicate tests        -> 0

Note `python3`, not `python`. Expected headline from the validator:

    1169 records · Tier A 231 · headline population 188 · gap 112/188 = 59.6%

## Layout

    dataset/AISIEVAL_V13.xlsx      The dataset. 1,169 findings x 39 columns, sheet AISIEVAL_V13.
                                   The single source of truth; everything else derives from it.
    dataset/AISIEVAL_validate.py   Structural validator: identifiers, controlled vocabularies,
                                   date coherence, the proportionality formula, the Attribution
                                   invariant.

    scripts/dataset_source.py      The one accessor. Every reader imports this, so there is
                                   exactly one path and one sheet name in the project. Override
                                   the workbook location with AISIEVAL_WORKBOOK.
    scripts/all_stats.py           Recomputes all reported quantities.
    scripts/build_charts.sh        Builds every figure, in the one order that is correct.
    scripts/verify_charts.py       Re-derives each plotted quantity and fails on disagreement.
    scripts/find_duplicates.py     Duplicate detection across IDs, text, quotes, near-duplicates.
    scripts/reconcile.py           Two-way reconciliation of the sheet against the ledger.
    scripts/sort_by_rulebook.py    Enforces the documented row order (tier, then newest first).
    scripts/charts*.py fig*.py
      nfig*.py tree.py hero.py
      palette.py tablefig.py       Figure generators, invoked by build_charts.sh.
    scripts/fetch.py               Source retrieval used by verification tooling.

    severity/severity_prompt.txt   Severity annotation prompt, version 1.1 (eight domains).
    severity/severity_prompt_v1.0_FROZEN.txt
                                   Version 1.0, verbatim. Rows coded under it are tagged with
                                   their prompt version and were not re-run.
    severity/run_severity_ensemble.py
                                   Three-model ensemble runner.

    sweep/master_ledger.csv        The screening ledger. 6,684 publications examined across 46
                                   organisations, each with its decision and reason. Exclusions
                                   are recorded, not only inclusions, so coverage can be
                                   reconciled in both directions.
    sweep/cached_enumerations.json Per-organisation enumeration used to build the ledger.

    protocol/v11_RULEBOOK.md       The coding manual. Every rule applied to every row: finding
                                   eligibility, tier assignment, the split-and-club rule, the
                                   identifier scheme, severity, the three channel protocols,
                                   proportionality, and the evidentiary standard. The paper's
                                   Section 3 summarises this; the rulebook is authoritative for
                                   borderline cases.
    protocol/codebook.md           Column-by-column reference for all 39 columns.
    protocol/v10_METHODOLOGY.md    Historical record of the v10 corpus build. Superseded.

## Two conventions that matter when reading the data

A recorded **"not found"** means the search ran and returned nothing. An **empty cell** means
the field was not searched or does not apply. These are different claims and the analysis
depends on the distinction.

`Sources Checked (channel A)` logs where each search looked, including where nothing was
found, and carries dated coding markers (`[ADDED ...]`, `[CHANNEL A BATTERY RE-RUN ...]`)
recording when a row was added or re-verified. That is the audit trail, kept deliberately.

## Known limitations of this artifact

- The `Human` column mirrors the three-model ensemble majority on every row. It records no
  independent human adjudication and is not validation of the ensemble.
- 28 Tier A rows have a `Finding Quote` that could not be matched to its cited source by
  automated check — a mixture of citation-wrapper artefacts, wrong-URL cases and genuine
  paraphrase. Flagged rather than silently corrected.
- Licence terms for the quoted source reports have not been individually audited. Every
  finding carries its source URL and publishing institution, so attribution is complete.
