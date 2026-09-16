# Tier A publication table

`TierA_paper_table.xlsx` / `.csv` — 231 Tier A findings × 34 columns. Built by
`scripts/build_paper_table.py` from `dataset/AISIEVAL_V13.xlsx`. Re-run the script to rebuild;
never hand-edit these files.

**V13 remains the audit copy.** It keeps the search logs, dated re-run markers and coding rulings
that make the dataset checkable. This table is the same rows with that apparatus removed.

## Columns dropped (5)

| Column | Why |
|---|---|
| `Sources Checked (channel A)` | Internal search log — five-source battery, dated re-runs, coding rulings. |
| `Human` | Mirrors the ensemble on every row. Publishing it would imply a human validation that has not been done. |
| `Eval? (trackable)` | Constant `yes` on Tier A — no information. |
| `Action Trackable?` | Constant `yes` on Tier A — no information. |
| `Tags` | Internal keywording, applied to 168 of 231 rows. |

## Cells cleaned (360)

Whitelisted columns only. Three removals and nothing else:

1. **Process notes** — bracketed coder logs (`[ADDED …]`, `[CHANNEL A BATTERY RE-RUN …]`,
   `[Moved from …]`, `[Tier justification …]`). Editorial insertions inside quotations —
   `[Claude Mythos 5]`, `[Anthropic, 2025b]` — are **kept**: deleting them would alter a verbatim.
2. **Search apparatus** — query strings, API names, HTTP statuses, provenance stamps.
3. **"Nothing found"** — normalised from five spellings to `None located`.

Distinguish `None located` (searched, nothing there) from an **empty cell** (not searched, or not
applicable). They are not the same claim.

## Columns never touched

Anything holding a quotation, code, date or number is byte-identical to V13, verified on every
build: all IDs, titles, dates, `Finding`, `Finding Quote`, `Channel A Verbatim`,
`Channel C Verbatim`, the severity majority and three votes, `Attribution`, `Lag (days)`,
`Action Level`, `Policy Level`, `Proportionality`, `Finding Type`, `Scope`.

An earlier pass trimmed trailing punctuation across all columns and silently turned 11 negative
`Lag (days)` values from `-27` into `27`, and cut an em-dash off the end of a Channel C quote. Hence
the whitelist, and hence the byte-identity assertion on every build.

## Still needs a human pass

`manual_pass_needed.csv` lists cells where search apparatus is interleaved mid-sentence with real
content — "Semantic Scholar, checked 2026-08-31: paperId 4a63c…, 'Testing…'". No pattern separates
those safely, so they were left intact rather than risk cutting the citation with the apparatus.

## One coding change made while building this

`UKAISI-2025-02-JAI1` was held at `Action Level = None` with a note reading "ONE CANDIDATE FOUND AND
NOT ADMITTED PENDING A RULING". The candidate — OpenAI's self-serve fine-tuning wind-down — is
already admitted as `Partial` on five other C1 fine-tuning-API rows (`FARAI-2024-08-JAI1`,
`FARAI-2024-10-ALI1`, `FARAI-2024-10-JAI1`, `FARAI-2025-02a-JAI2`, `PALISADE-2024-12-JAI1`). Identical
evidence was being coded two different ways. Resolved to `Partial` for consistency; `Attribution`
follows to `No explicit attribution` and `Proportionality` to `Under-response (gap)`.

**This moves the headline: 113/188 = 60.1% → 112/188 = 59.6%.** The prior values are recorded in
that row's `Sources Checked` in V13.
