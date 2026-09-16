# Phase 3 — Quote & Source Verification of the Finalized 67 (complete)

Run date: 2026-07-15. All 67 trackable rows verified against their primary sources by 11 independent
adversarial passes (one per report group). Full per-row detail: `phase3_consolidated.csv` and `output/*.json`
(each row: publication date check, every number checked, quote verdicts, proposed exact replacements).

## Aggregate results

- **Numbers: 159 numeric claims checked → 138 exact (87%), 13 mismatch, 8 not-found.**
  The quantitative layer is largely sound; errors concentrate in attribution (right number, wrong
  model/evaluator/condition), not invented statistics.
- **Key Quote: only 5 of 67 verbatim-exact.** 34 missing, 13 not in the cited source (fabricated or
  imported from elsewhere), 11 paraphrases labeled as quotes. Exact replacement quotes are proposed
  for every row, copied character-for-character.
- **Channel A Verbatim: 11 exact, ~30 are descriptions/summaries, 1 wrong-purpose quote, 1 not in source.**
  Real company-voice quotes proposed for every non-exact cell.
- **Channel B (government) and Channel C (media) verbatims: almost all exact** — the strongest columns.
- **Publication dates: all verified** (one day-precision caveat: Gemini FSF PDF says only "November 2025").

## Critical triage — decisions needed before fixes are applied

### A. Eligibility / scope (rows that may not belong in the 67 as-is)
- **Row 40 (NEW-151)** — OpenAI Preparedness self-classification, not an AISI finding; response = finding.
- **Rows 54, 64** — Anthropic's own system-card self-reports (whistleblowing §4.1.9; 84% blackmail §4.1.1.2),
  misfiled under the Apollo scheming evaluation. Not third-party findings.
- **Row 5 (RepliBench)** — 15/20, 9/20 attributed to "Claude 3.7 Sonnet" but the blog anonymises all
  seven models. Fails the named-model rule as written.
- **Row 34 (NEW-070, sycophancy)** — OpenAI's rollback (2025-04-29) predates the AISI paper by a year and
  never mentions AISI; "Substantive/Explicit" response is indefensible. Recode Action Level=None or drop.
- **Row 21 (Gemini 3 Pro)** — cited academic review is about Gemini 2.5 Pro (Gemini 3 appears zero times);
  FSF PDF never names Apollo/UK AISI/Vaultis/Dreadnode. Report ID also mislabels a DeepMind publication
  as UK AISI. Needs re-sourcing or reclassification.
- **Rows 20/37/39 (+31)** — finding-source = response-source circularity (OpenAI blog/system card both ways).
  Keep, but the paper must state how pre-deployment/company-published findings are handled.

### B. Fabricated / wrong-source Key Quotes (replace with proposed verbatims)
Rows 58 & 59 (BPJ "credit card" quote — contradicts the blog's "requires significant expertise");
rows 65–68 (identical copy-pasted ASL-3 quote, topically unrelated); row 18 (provenance unknown);
row 17 (Kimi K2 self-reported-benchmarks comparison — not on NIST page); row 26 (synthesized sentence);
rows 9/10 (shared NCSC quote not in cited source); row 11 ("alarm bell... doubling every four months" —
composite from a different blog whose actual estimate is 4.7 months); row 28 (drops "we design",
changing whose monitor was evaded).

### C. Number / attribution corrections
- Row 24: 0.778 pass@200 is UK AISI's jailbreak success vs safeguards, not a model capability score.
- Row 48: "internal" red team unsupported; jailbreaks found against GPT-5.2-checkpoint configs;
  exact wording "not blocking and will be remediated".
- Row 58: 25.5% avg paired with wrong condition's 80.4% max (base-BPJ max = 39.9%).
- Row 53 (ADD-11): inversion — Gemini 3.1 Pro was FIRST to 100th-pct VCT, GPT-5.5 Ckpt2 second;
  response date 2026-02-19 not 02-01.
- Row 33 (NEW-161): 22.1%/54%/"held-out wet-lab" not in cited article (imported from VCT paper).
- Row 51 (ADD-09): "safeguard regression" contradicts source's "no clear conclusion can be drawn".
- Row 26: "11% for baseline defences" inverts source (11% = strongest baseline ATTACK success).
- Row 11: "first model to solve expert-level CTFs" contradicts source (threshold crossed ~Apr 2025);
  38%, 70x, 476% are author-derived, not in source.
- Row 20: "not credited in GPT-5 system card" contradicted by live card §5.3.3.5.
- Rows 57, 19: cherry-picked favorable cyber numbers; same reports show underperformance on the
  other institute's tasks — add balancing clause.
- Row 27: "+ 2 unnamed frontier models" outdated — full paper names all four models; and
  "Sources Checked: no company statement found" is FALSE (Opus 4.5 System Card §6.13 responds
  to AISI) → Action Level upgrade from None.
- Row 16: Anthropic page dated 2026-06-02 (not 05-15); lag ~20d not 2.
- Row 49: Channel A (Apr 23) and Channel B (May 1) predate the AISI blog (May 13) — recheck coding.
- Rows 11/12: EP question E-001575/2026 cites Anthropic and CeSIA, never AISI; submitted 16 Apr not 7 Apr.

### D. Merge candidates within the 67 (same source sentence)
23+24 (one system-card sentence); 61+62 (one blog sentence); 12+45 (same TLO-first sentence);
16+50; NEW-116 (row 42) → club into rows 6/7 group as the response channel.
(Verified-justified splits: 58/59; 65–68 map to distinct vulnerability bullets.)

## Systematic fixes ready to apply mechanically
1. Insert/replace Key Quote for all 67 rows from `proposed_key_quote`.
2. Replace ~30 Channel A Verbatim descriptions with `proposed_channelA_verbatim`.
3. Date/Lag corrections (rows 16, 21, 25, 37, 53, 59, 63, 64, 65 + Phase 1 lag list).
4. Metadata fills from Phase 1 (Report IDs, Institutions, Access Types, canonical spellings).
