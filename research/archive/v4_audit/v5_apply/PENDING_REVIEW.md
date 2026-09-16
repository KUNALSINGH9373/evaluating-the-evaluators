# v5 — status & remaining decisions (updated 2026-07-15)

## Accountability set: 67 → 58
Removed since v4:
- 40, 54, 64 → company-self-report stratum (re-filed)
- 24 → merged into 23 (tombstone)
- 6, 7, 27, 42 → methodology/null-result cluster (UKAISI-2025-11b "Investigating Models for Misalignment")
- 8 → monitoring-methodology stress-test with reassuring result (UKAISI-2025-12-16)

## RESOLVED this session
- Row 5 (RepliBench): RepliBench-response claim retracted — ARA→checkpoint change was RSP v2.0 (2024-10-15),
  6 months before the finding; RSP v2.1/v2.2 unchanged on autonomy. Action Level → None, Accountability gap.
  (Row stays trackable; the "no response" is the honest result.)
- Neg-lag sweep: 8 mis-dated "responses" corrected to None (rows 9,10,11,12,34,45,50,53); NCSC policy
  citations on 9/10 preserved. Overstated responsiveness removed.
- Row 42: Attribution Explicit → Topical+Temporal (card credits AISI only as observer; mitigation predates
  finding by 2 days). Then reclassified out of accountability set as methodology.
- Rows 6/7: NOT errors — Key Quotes verbatim in the cited blog, models match the blog. The "paper has
  different models" was a blog-vs-paper version gap (paper arXiv:2604.00788 adds GPT-5). Then reclassified
  as methodology/null.
- v3 row 96 (Claude Mythos 65% discrepancy) is NOT an accidental loss — it is present as row 13. Restore
  recommendation withdrawn.

## STILL OPEN — need your decision
1. **Row 21 (GDM-2025-11, Gemini 3 Pro FSF)** — cited academic review is about Gemini **2.5** Pro (Gemini 3
   appears zero times); FSF PDF never names Apollo/UK AISI/Vaultis/Dreadnode. Re-source or drop. Also it's a
   Google DeepMind (company) FSF report — scope question like the self-report rows.
2. **Rows 52 & 53 (USCAISI-2026-04)** — cite **SecureBio**, an independent org, not UK AISI/CAISI. Scope: do
   SecureBio-led evals belong in an AISI-response dataset? (Row 53 already corrected for the Gemini-first
   inversion + neg-lag.)
3. **Severity re-vote (deferred)** — test cases where unanimous C1 looks wrong under codebook
   "negation → Cat 2 / demonstrated-not-domain":
   - Row 5 (RepliBench): pass@10 partial capability, "not yet capable of full replication".
   - Row 19 (o1 cyber): 45% vs 35% baseline uplift, fails 55%, UNDERperforms on the parallel UK AISI
     suite (36% vs 46%) — a benchmark-score uplift, not a demonstrated threshold breach → likely C2.
   RULE to add: C1 = a qualitative dangerous-capability THRESHOLD demonstrated (e.g. "first to complete
   the full attack chain"); C2 = relative/benchmark uplift where the model still fails most tasks.
   Recommend re-voting all C1 rows with a sharpened prompt + a domain-vs-severity correlation check
   (tests Stephen's K199 concern that the ensemble over-reads scary domains).
4. **15 v3-drop dispositions** — confirm reasons in phase2_disposition_ledger.csv (row 96 now resolved →
   14 remaining). Superseded set 151–154 to be marked, not just dropped.
5. **Unapplied merges** — 61+62, 12+45, 16+50 (same-source-sentence pairs).
6. **Codebook edits** — (a) negative-lag clause; (b) company-published-findings clause; (c) new strata
   `company-self-report`, `methodology-null`; (d) "response = action attributable to the finding, not
   pre-existing standing policy" (from the RSP row-5 lesson).

## Finding Type column — added & populated (multi-select), 6 consistency flags to resolve
Column added: nature (capability-finding / methodology / capability-trend / governance) + modifiers
(anonymised-model / reassuring-null / company-self-report / too-recent / non-frontier). Rule:
solo `capability-finding` ⟺ Action Trackable? = yes. Full-corpus distribution (nature): capability-finding
133, methodology 81, governance 59, capability-trend 20.
The column surfaced 6 rows where trackable and nature disagree — resolve each:
- **Row 22** (GPT-5.3-Codex "first High cybersecurity"): trackable=yes but classified governance
  (it's OpenAI's precautionary self-classification, not an empirical AISI verdict). Decide: keep in
  accountability set as capability-finding, or reclassify governance + drop trackable.
- **Row 24**: capability-finding but trackable=no — expected (it's the 23+24 merge tombstone; delete row).
- **Rows 134 (Llama 3.1 405B), 143 (bio tool-augmentation), 150 (DeepSeek cyber), 180 (open-weight
  finetuning defences undone)**: clean named-model results marked trackable=no with no fitting modifier —
  likely MISLABELS. Review whether they should be trackable=yes (would grow the accountability set).

## Mythos/Fable — reviewed, resolved (2026-07-15)
Anthropic's gate-Mythos / release-Fable architecture was announced 2026-04-07, BEFORE the first AISI
Mythos finding (2026-04-13); Anthropic attributes it to pre-planned tiered strategy + internal
red-teaming, never to AISI. Therefore NOT a response (row-5 principle). All 6 Mythos cyber-capability
rows (11,12,16,45,50,191) harmonized to company response None; rows 16 & 191 downgraded from
Substantive/Explicit. Row 191's government Channel B responses (BoE/FCA/Treasury, NCSC, UK AI Minister)
PRESERVED. Row 165 mis-filed evaluator quote removed. OPEN CHOICE: rows 16/191 company channel is coded
strict None; softer alternative is Topical+Temporal (same cyber issue, same window) — never Explicit.

## Channel-A coherence — 5 fixed, 22 flagged (2026-07-15)
- FIXED: Attribution → None on rows 2, 3, 6, 7, 18, 13 (had an Attribution value but no company response;
  Attribution describes a response, so it must be None when Company Response = None).
- FLAGGED (need per-row decision — fill a real Company Response, or downgrade Action Level → None):
  22 rows have Action Level = Acknowledged/Partial/Substantive but Company Response = None:
  70, 71, 72, 80, 81, 82, 83, 84, 87, 88, 89, 96, 174, 175, 177, 179, 183, 184, 192, 211, 212.
  NOTE: ~10 are governance/GOV rows where the "action" may legitimately live in the POLICY channel
  (Channel B), not the company channel — for those, Action Level may be mis-applied to Channel A and
  should either move to a policy-level field or be blanked. The capability rows (70,71,72,80,81,82,83,
  84,87,88,89,96) are true incoherences: either a company response exists and must be filled, or Action
  Level should be None. Row 96 also: Action Level=Acknowledged on a reassuring-null — likely None.

## Deliverables on Desktop
aisi_v5.csv · aisi_v5_changelog.csv (all cell changes, DECISION-tagged where a judgment call) ·
aisi_v5_neglag_sweep.md · aisi_v5_PENDING_REVIEW.md
