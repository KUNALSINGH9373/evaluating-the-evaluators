# Negative-lag / mis-dated-response sweep — results (2026-07-15)

Swept 22 candidate rows for the row-5 failure mode: a company action credited as a "response"
that actually predates the finding or has no causal link. **8 errors, 1 uncertain, 13 legit.**

## 8 ERRORS — corrected in v5 (Action Level → None, Channel A stripped, Proportionality recomputed)
| Row | Finding | The mis-dated "response" | Why it fails |
|---|---|---|---|
| 9 | UKAISI-2026-03-CYB1 | Mythos Preview / Project Glasswing restriction | Anthropic attributes restriction to its OWN internal red-teaming; never names UK AISI; different/later model than the Opus 4.6 finding. **NCSC policy citation KEPT (legit).** |
| 10 | UKAISI-2026-03-CYB2 | Mythos benchmark restriction | Same mis-attribution; wrong model. **NCSC policy citation KEPT.** |
| 11 | UKAISI-2026-04-CYB1 | Mythos restriction (2026-04-07) | Predates finding (2026-04-13); driven by internal red-teaming, not the AISI finding |
| 12 | UKAISI-2026-04-CYB2 | Mythos restriction (2026-04-07) | Same as row 11 |
| 34 | NEW-070 (sycophancy) | GPT-4o rollback (2025-04-29) | Predates finding (2026-04-28) by ~12 months; OpenAI's own reaction to user feedback |
| 45 | ADD-03 | Mythos restriction (2026-04-07) | Predates finding (2026-04-30) |
| 50 | ADD-08 | Mythos restriction (2026-04-07) | Predates finding (2026-05-13) by ~5 weeks |
| 53 | ADD-11 | Gemini 3.1 Pro FSF below-CCL (2026-02-19) | Predates SecureBio finding (2026-04-23) by ~2 months; Google's own assessment |

**Dominant pattern:** six rows (9,10,11,12,45,50) all recycled the *same* Anthropic Mythos-Preview /
Project Glasswing restriction as a "response" — a single company decision (its own internal red-teaming)
mis-applied across multiple distinct findings and multiple model versions. This is the row-5 error at scale.

## 1 UNCERTAIN — needs your check
- **Row 42 (NEW-116)** — Opus 4.5 Preview, pre-deployment context is real (response predates finding by only
  2 days, consistent with pre-deployment), but the AISI source doesn't credit Anthropic and eval-awareness
  data removal is Anthropic's own practice. Verify system-card wording; if no explicit tie, downgrade
  Attribution Explicit → Topical+Temporal.

## 13 LEGIT — kept as-is (verified causal link)
- Genuine pre-deployment (AISI/CAISI named in the system card, so a pre-publication response is real):
  rows 19, 22, 31, 32, 49, 56, 21.
- Post-publication collaboration-remediation (same-day "we patched these"): rows 39, 65, 67.
- No-response rows (correct): 2, 5.

## Secondary flags for pending review
- **Row 49**: causally legit but Source URL points to a later 2026-05-13 longitudinal blog → set
  Access = Pre-deployment and align the finding date.
- **Rows 52 & 53**: cite SecureBio (independent org), not UK AISI/CAISI — scope question: do they belong
  in an AISI-response dataset?

## Impact on the accountability set (63 rows)
- Action Level after sweep: None 32, Substantive 18, Acknowledged 8, Partial 5.
- The corrections moved ~7 rows from "Substantive response" to "no response" — i.e. the pre-sweep
  responsiveness rate was **overstated**. This is exactly the direction that protects the paper from a
  reviewer: the errors were inflating apparent company responsiveness, and they are now removed.
