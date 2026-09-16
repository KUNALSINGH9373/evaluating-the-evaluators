# V13 full-sheet audit — 2026-08-29

Scope: every row, every column. Deterministic checks plus network verification of all cited
sources. Validator status throughout: **PASS, 0 violations**.

Corpus 1168 · Tier A 206 · headline population 166 · no response 101/166 = 60.8%

---

## 1. Structural — clean

| Check | Result |
|---|---|
| Duplicate Finding IDs | 0 |
| Blank Finding ID / Report ID | 0 |
| Blank Source URL | 0 |
| Blank Finding Quote on Tier A | 0 |
| Publication Date non-ISO | 0 |
| Publication Date outside 2018-01-01…2026-08-29 | 0 |
| Lag ≠ (Response − Publication) | 0 |
| §6.2 Report ID sharing title/URL/date | 0 violations |
| Controlled vocabulary, all 11 coded columns | 0 violations |
| Proportionality vs severity×action formula | 0 violations |
| Tier C carrying Action Trackable? | 0 |
| Leading/trailing whitespace, control chars | 0 |

## 2. Attribution — three values, invariant holds

The sheet uses **three** values, not the two documented in rulebook §9 col 18:

```
                        new Tier A (22)   pre-existing (184)
No response located          19               128
Explicit attribution          3                62
No explicit attribution       0                12
```

`Attribution == "No response located"` ⇔ `Action Level == "None"` — **0 violations** across all
206 Tier A rows. **Action: rulebook §9 col 18 is wrong and must be corrected to three categories.**

## 3. Verbatim verification — the substantive finding

1,300 quote/source pairs across 543 distinct URLs, fetched and substring-tested.

```
740  exact
195  exact after punctuation/hyphenation normalisation
 44  composite-OK (ellipsis-joined; every fragment verifies)
────
979  VERIFIED  (75%)

133  no fragment matched  ← see bands below
 40  partial (some fragments verify)
101  thin fetch (<8k) — inconclusive
 45  source unreachable
```

Longest-common-substring coverage on the 133, measured against full documents:

| Band | n | Tier A | Headline (C1 Tier A) | Meaning |
|---|---|---|---|---|
| paraphrase (<0.30) | **53** | 17 | **15** | the coder's own words in a verbatim column |
| reassembled (0.30–0.70) | **71** | 27 | **22** | real source material, not a contiguous quote |
| near-exact (≥0.70) | 9 | 2 | 1 | one-word/digit drift, repairable |
| partial fragments | 40 | 12 | 11 | mixed |

**All 133 are pre-existing V12 rows. Zero come from the window-extension sweep.**

Confirmed by hand against full PDFs:

- `USCAISI-2026-03-CYB4` — quote asserts "more than 250,000 attack attempts"; the string
  `250,000` does **not** appear in arXiv 2603.15714 (97k chars fetched). A quantitative claim
  in a verbatim column that the source does not contain.
- `METR-2024-11-ALI1` — "violating the rules of the task" absent from the 126k-char METR PDF;
  longest matching run is 26 characters.
- `UKAISI-2026-02-JAI1` — longest matching run 38 characters of a 200-character quote.

Detail: `logs/verbatim_audit.json`, `logs/verbatim_triage.json`, `logs/verbatim_coverage.json`.

### Two corrections to earlier numbers in this audit

1. The first pass reported **378** not-found. **111** of those were the checker fetching arXiv
   `/abs/` landing pages, which contain only the abstract and can never match a body quote.
   Fixed by rewriting `/abs/` → `/pdf/`.
2. "UNSUPPORTED" as a binary verdict overstated the problem: it failed a 663-character quote for
   a single differing word. Coverage banding replaced it.

## 4. Fixed during the audit

- **18 rows lost their provenance and tier reasoning.** Splitting the Channel B log out of
  `Sources Checked` overwrote the cell, destroying the `[ADDED … window-extension sweep]` marker.
  Restored from `pre-channels-20260829`; marker count back to 167.
- **4 Weval report titles** were bare slugs (`Deepseek`, `Grok 3`, `Sonnet`, `Gpt 4 1`) against
  the existing `DEEPSEEK-R1 Model Card` convention. Renamed across 8 rows.

## 5. Cleared — flagged but correct

| Flag | Verdict |
|---|---|
| 2 severity majorities ≠ their votes | registered D8 override + registered input-fix |
| 77 IDs off §6.1 format | legacy, grandfathered under rule 3. **0 from the sweep** |
| 16 Finding-ID/Report-ID prefix mismatches | correct: §1 company-published carve-out |
| 3 positive Policy Level "without a government URL" | URLs present, missing only the scheme |

## 6. Open, needing a decision

1. **124 verbatims** in the paraphrase + reassembled bands need re-extraction from source.
   48 of them are headline rows. This is the largest remaining integrity item.
2. `PALISADE-2025-07-ALI1` cites the **evaluator's own blog** as Channel B evidence for a US
   congressional claim. §8b admits official government sources only.
3. **45 unreachable sources** — link rot; need Wayback snapshots recorded.
4. **101 thin fetches** — inconclusive, mostly JS-rendered pages; need a headless fetch.
5. 8 Tier B/C rows hold prose instead of a URL in `Channel A Evidence` (not scored).
6. 28 Channel B logs don't use the `Not found` prefix convention.
7. Open item #7 — human validation of the severity ensemble. `Human` mirrors the ensemble on
   1168 of 1168 rows, so this is unmet corpus-wide.
8. Rulebook §9 col 18 (Attribution) and codebook §9 (38 vs 39 columns) are stale.
