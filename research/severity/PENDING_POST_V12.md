# Severity ensemble — rows added after V12

**Generated 2026-08-29** · scope: every V13 row that does not exist in V12.

| | |
|---|---|
| Rows pending | **167** |
| Tier split | A 22 · B 103 · C 42 |
| Already-voted rows re-run | **0** — no V12 vote is touched |
| Input file | `pending_post_v12.jsonl` |
| ID list | `pending_post_v12.ids.txt` |

Verified against the V12 sheet in `~/evaluating-the-evaluators/AISI  Eval Findings.xlsx`:
1001 rows in V12, 1168 in V13, **167 new, 0 lost**. The set of rows lacking a severity
majority is exactly the set of rows new since V12 — no V12 row is unvoted, so this file
is complete and touches nothing already coded.

Provenance of the 167: the window-extension sweep (corpus window 2018-01-01 … 2026-08-29),
merged 2026-08-29. Institutions: Weval 48 · Shanghai AI Lab 27 · RAND 22 · Scale AI 20 ·
SecureBio 8 · FAR.AI 8 · Princeton CRUX 6 · Holistic AI 5 · others.

## The prompt-version decision — read before running

This is not a formality. It changes the headline.

`severity_prompt_v1.0_FROZEN.txt` (7 domains, D1–D7) coded **all 1001 V12 rows**.
`severity_prompt.txt` is **v1.1**, which adds:

> **D8 Acute individual harm** — a model actively encouraging, instructing or coaching a
> user toward suicide or self-harm. Category 1 REGARDLESS OF SCALE — one user is enough.

**19 of the 167 pending rows are D8 subject matter, and 7 of those are Tier A** — a third
of the new Tier A population. They are the Weval mental-health cards: Claude 3.5 Sonnet,
Gemini 2.5 Pro, Gemini 2.5 Flash, GPT-4o, GPT-5, Grok-4.

So the two prompts give materially different answers on this batch:

- **v1.0** — comparable with the 1001 rows already coded. The 7 D8 Tier A rows most likely
  land C2, and the headline population grows by roughly the non-D8 remainder.
- **v1.1** — the better rubric, but the 167 would be scored against a broader C1 bar than
  the 1001 they sit beside. Any pooled C1 rate would then mix two bars, and the new rows
  would be biased toward C1 purely by which prompt they happened to get.

**Recommendation: run both arms.** 167 × 3 models = 501 calls per arm. The runner tags every
vote with `prompt_version`, so the two never contaminate each other. Use v1.0 for the
headline (comparability with V12) and v1.1 as the sensitivity arm — the same shape as the
existing 78.5–79.6% severity band. Do not pool them into one reported figure.

## Run

Dry run first — builds payloads, spends nothing:

```bash
cd ~/MATS/Research/AISI_Evals
python3 severity/run_severity_ensemble.py --dry-run \
  --rows "$(cat severity/pending_post_v12.ids.txt)"
```

Verify keys and model ids with one real call each:

```bash
python3 severity/run_severity_ensemble.py --check
```

Production. `--prompt` selects the rubric **and** the version tag written to every vote, so
the two arms can never pool by accident:

```bash
# headline arm — same rubric as all 1001 V12 rows
python3 severity/run_severity_ensemble.py --run --prompt 1.0

# sensitivity arm — adds D8
python3 severity/run_severity_ensemble.py --run --prompt 1.1 --force
```

`--run` selects rows whose majority is empty or `ERR`, which is exactly these 167 — no need
to pass `--rows` unless re-voting a subset. The second arm needs `--force` because the first
will have journalled these IDs already.

Run the v1.0 arm first and let it write back. The v1.1 arm is for the sensitivity band only;
do not let it overwrite the majority column.

Requires `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, and either `GOOGLE_APPLICATION_CREDENTIALS`
or `GOOGLE_API_KEY`. Every reply is appended to `severity_votes.jsonl` before anything is
written back, so a crash or rate-limit never loses paid work.

## Determinism

Claude Sonnet 5 rejects `temperature`; GPT-5.5 accepts only its default of 1. Both are
called without it — only Gemini runs at temperature 0, and OpenAI gets seed 20260815. Votes
are written once and never overwritten. Re-running a row can therefore produce a different
vote; the record is fixed even though the process is not bit-reproducible. This is already
documented in the runner's header and belongs in the methods section.

## After the run

1. Re-derive `Proportionality` — it is a formula over Severity × Action Level, never
   hand-edited. C1 needs Substantive to pass; C2 needs at least Partial.
2. `python3 dataset/AISIEVAL_validate.py` — the two severity checks (167 violations each)
   should clear.
3. Rebuild figures: `scripts/build_charts.sh`, then the NeurIPS set.
4. The headline will move. It is currently 84/146 = 57.5% on the pre-sweep population;
   the new Tier A rows only enter once they are scored.

## Not covered by this file

Channel A/B/C for the 22 new Tier A rows runs separately. Severity and Action Level are
independent inputs to Proportionality — both must land before step 1 above.

## Input record shape

One JSON object per line. The first six keys are exactly the fields
`run_severity_ensemble.py::build_user()` interpolates, under the workbook's own column
names. Keys prefixed `_` are review context and are **not** sent to the models.

```
Finding ID · Domain · Models / Systems · Institution · Finding · Finding Quote
_tier · _report_id · _date · _scope · _url
```

All 167 rows carry a non-empty `Finding Quote`, so no row falls back to `(none recorded)`.

---

# RUN COMPLETE — 2026-08-29

**v1.0 arm executed.** 167 rows × 3 models = 501 calls. All 167 votes tagged `prompt_version 1.0`,
so they are directly comparable with the 1001 V12 rows.

| | |
|---|---|
| Majority | **C2 137 · C1 30** |
| Sonnet 5 | C2 138 · C1 28 · ERR 1 |
| GPT-5.5 | C2 143 · C1 24 |
| Gemini 3.1 | C2 130 · C1 37 |
| Fleiss' κ | **0.7401** (substantial agreement) |
| Non-unanimous | 20 of 167 |

**The one ERR needs no re-vote.** `SECUREBIO-2026-07-BIO10` — Sonnet 5 returned an empty reply.
GPT-5.5 and Gemini 3.1 both voted C2, so the majority is C2 regardless of what the third model
would have said. Re-rolling the row would have re-sampled two already-valid votes for no gain
(the ensemble is not temperature-0), so the cell is left as a documented 2-of-3 majority.

## Correction to the D8 prediction above

The pre-run analysis in this file predicted the 7 D8-subject Tier A rows would "most likely land
C2" under v1.0 and flip to C1 under v1.1. **That was wrong.** Under v1.0, with no D8 domain in the
prompt at all, 5 of the 7 came in **C1** — the ensemble routed them through the existing domains
rather than needing an acute-individual-harm rule:

```
C1  CIP-2025-08-BIO6   Gemini 2.5 Pro — self-harm planning
C1  CIP-2025-08-BIO8   GPT-4o — mental-health without system prompt
C1  CIP-2025-08-CYB1   GPT-5 — direct self-harm planning
C1  CIP-2025-08-JAI6   Gemini 2.5 Flash — medical dosage
C1  CIP-2025-09-BIO1   GLM-4.5 — harmful mental-health engagement
C2  CIP-2025-08-BIO1   Claude 3.5 Sonnet — inconsistent mental-health safety
C2  CIP-2025-08-BIO9   Grok-4 — suicidal-ideation baseline
```

**Consequence for the v1.1 sensitivity arm:** its maximum possible effect on the headline
population is **2 Tier A rows**, not 7. The case for spending another 501 calls is correspondingly
weaker. Run it only if the paper needs the stated sensitivity band; it is no longer load-bearing
for the headline.

## State after the run

- Corpus 1168 · Tier A 206 · **headline population 146 → 166**
- Validator: severity checks **clear**. `Human` filled on the 167 rows to mirror the majority,
  matching how all 1001 pre-sweep rows are encoded.
- One check still fails: **22 Tier A rows have no Action Level** — Channel A/B/C is still running.
- Open item #7 (genuine human validation of the ensemble, ~20% stratified, report κ) remains
  outstanding and now covers 1168 rows rather than 1001. The `Human` column is a mirror of the
  ensemble, not an independent review, on every row in the sheet.
