# Evaluating the Evaluators — Rulebook (v11 audited additions)

**Project question:** Do third-party AI evaluations matter?

**Corpus cutoff:** 2026-08-29 (moved from 2026-07-30 by the window-extension sweep). **Eligible
publication period:** no lower-date boundary is applied. A report is eligible if it was publicly
available on or before the cutoff. The earliest publication actually held is 2023-03-17 and the
latest 2026-08-27; that range describes the corpus, not an eligibility rule.

**Current file — there is exactly one.** `dataset/AISIEVAL_V13.xlsx`, sheet `AISIEVAL_V13`, read
only through `scripts/dataset_source.py`. **1,146 findings · 457 reports · 46 institutions ·
39 columns · Tier A 233 · B 599 · C 314 · headline 152/190 = 80.0% falling short, of which
114/190 = 60.0% with no located response.**

The merge this section used to describe is done. `v10 revised.xlsx` (455-finding base) and
`v11_FINAL.xlsx` (558-finding audited additions) were reconciled into V12 and then V13; both source
files are **dead paths and must not be read**. The reconciliation preserved every v10 finding —
`scripts/diff_v12_v13.py` asserts 0 missing rows — and the report-identity issues in §12 were
resolved under §6.2, which the validator now enforces at 0 violations.

Both workbooks now use one row-level sheet and the same 39-column core schema. The v10 sheet is
named `v10 revised`; its 455 rows incorporate the atomic tier reclassification in `Eval?
(trackable)` and `Action Trackable?`, with the underlying rationale preserved in `Notes`. Obsolete
response fields on revised Tier B/C rows are blank in the active schema; their prior contents are
preserved in `Notes` as legacy audit data.

**Schema:** one sheet named `v11 final`; 39 named columns; rows sorted Tier A, Tier B, Tier C and
then newest-to-oldest within each tier.

**Last updated:** 2026-09-07.

---

## 1. Scope and accountable unit

The dataset measures the public accountability pipeline after an external evaluator publishes a
finding about a frontier AI model or developer.

**The frontier condition is a scope gate, not a tiering condition.** A finding must concern a
frontier AI lab, company or model to be in the dataset at all. If it does not, it is excluded to
the screening ledger and receives no tier. Three consequences follow, and they are frequently
confused:

- **Anonymised is not non-frontier.** A finding that evaluates frontier systems without naming
  which ones satisfies this gate. It fails Tier A on the *named* requirement and is Tier B — a
  frontier-related adverse finding that cannot be traced to an accountable company.
- **Model size does not decide it.** Any model from a frontier developer is in scope at any scale;
  an 8B open-weight release from a frontier lab qualifies, and NVIDIA, Meta, Alibaba, DeepSeek,
  Moonshot and Zhipu are frontier developers for this purpose.
- **The evaluator's own constructs are out.** A model the evaluator built, fine-tuned or
  backdoored for the study has no accountable developer and fails the gate, as does a finding whose
  subject is a benchmark, a software library, an evaluation apparatus, or human baseliners rather
  than a model.

- `government-AISI`: government AI safety/security institutes and joint exercises containing one.
- `third-party-evaluator`: independent non-government evaluators, retained as a separate stratum.
- Company-published system cards qualify only for a finding explicitly attributed to a named
  external evaluator. The Institution is that evaluator, not the model developer.
- Company self-reports with no named external evaluator are excluded to the screening ledger.
- A named organisation must genuinely have evaluated or asserted the finding. Merely developing a
  benchmark, hosting a report, or being cited by another evaluator is insufficient.
- A secondary summary of another evaluator's result is excluded when the primary evaluator finding
  is already represented.

## 2. Finding eligibility

A finding is one discrete, independently codeable claim that satisfies all three conditions:

1. **Evaluator assertion:** the in-scope evaluator asserts it; it is not a passing comparator or a
   summary of somebody else's finding.
2. **Evidence in the source:** the report documents a measured result, observed behaviour, or
   process fact. Opinions, recommendations, announcements, and plans are not findings.
3. **Atomicity:** it could reasonably receive its own response. Findings that would receive one
   common response are clubbed; findings needing distinct responses are split.

Every included row must have a primary Source URL, a concise Finding paraphrase, and a verbatim
Finding Quote from the correct source. If the source is bilingual, the source-language quotation
is authoritative; an analyst translation must be clearly identified and must not be represented as
verbatim source text.

## 3. Search, dates, and deduplication

- Enumerate each eligible organisation's own publication surfaces through the cutoff; use sitemaps,
  archive copies, and citation-chasing only to complete or freeze that enumeration.
- Every screened publication receives one ledger decision: included, excluded with reason,
  duplicate/secondary, or post-cutoff.
- Publication age is not an exclusion criterion. A qualifying pre-September-2023 report is retained
  under the same evaluator, finding, source, duplication, and tier rules as every later report.
- Publication Date is the source-verified release date in `YYYY-MM-DD`, or `YYYY-MM` only when the
  source supplies no day. A live-page rebuild timestamp is not publication evidence.
- Mutable leaderboards and model cards require a dated frozen snapshot or an explicit, documented
  observation-date policy. An “Updated” date must not silently be treated as “Published.”
- The earliest, fullest primary source wins. Deduplication uses Finding ID, Report ID, normalized
  title, Source URL, publication date, evaluator, models, quoted text, paraphrase similarity, and
  semantic review. Same-report atomic findings are not duplicates merely because they share a quote.
- All rows sharing a Report ID must share Report Title, Publication Date, and Source URL.

## 4. Tier classification

Each row belongs to exactly one tier:

| Tier | Encoding | Rule | Use |
|---|---|---|---|
| A | `Eval? = yes`; `Action Trackable? = yes` | Empirical finding about a named frontier company/model, concerning, and a company response is reasonable to assess. | Channel A/B/C and proportionality analysis. |
| B | `Eval? = yes`; `Action Trackable? = no` | Empirical and in scope under §1, but fails at least one Tier-A condition: anonymised model, reassuring/null result, bare score or ranking without a concerning threshold, capability trend, inconclusive result, or company response is not reasonably assessable. | Descriptive analysis only. |
| C | `Eval? = no`; `Action Trackable? = blank` | Methodology, framework, governance/process, tooling, milestone, or other non-empirical-model finding. | Descriptive analysis only. |

Tier A requires **all** of the following:

1. empirical model behaviour/capability/safeguard result;
2. a named frontier model or accountable developer;
3. an adverse or concerning result, not a reassuring null or bare performance number; and
4. a concrete company response could reasonably be assessed.

Only Tier A receives response classifications. Tier B and C response fields are blank.

After the 2026-08-16 additions audit and removal of the lower-date boundary, the additions file
contains 74 Tier A, 301 Tier B, and 183 Tier C rows. These are not combined-master or manuscript
headline counts.

## 5. One finding and one accountable company per row

- Different accountable companies never share a row.
- Club results that warrant the same response; split results that warrant different responses.
- Comparators and tested baselines belong in Notes, not separate rows, unless independently asserted
  as an eligible finding.
- Split rows keep a common report identity and receive unique Finding IDs.

## 6. Identifiers

- Finding ID is unique and immutable once published. Correcting a classification does not rewrite
  the key. Placeholder IDs may be regenerated before release when the date was unresolved.
- Report ID groups exactly one source report. Different reports must never share a Report ID.
- Known cross-version identities must be reconciled before a combined release (§12).

## 7. Severity

- Three independent model votes apply the frozen severity prompt; majority vote sets
  `Severity (C1/C2) majority`; all votes remain visible.
- `C1` means a demonstrated significant-risk threshold under the frozen domain rubric.
- `C2` means a lower-risk result that does not cross a C1 boundary.
- `ERR` is not a severity. If the ensemble has no majority, severity and Proportionality remain
  unresolved until re-run or documented human adjudication. A human override must be identified in
  Notes, state its rationale, and preserve all raw votes; it must not be described as a model
  majority.

## 8. Channel A — company response

Channel A searches the company newsroom/blog, later system cards in the same model family,
deployment-safety pages, official company statements, and open-web results used only to locate
company primary sources. A no-response classification requires a dated search log through the
cutoff.

A qualifying response must be documented in a company primary source and directly address the
identified problem through recognition, mitigation, model change, safeguard, access restriction,
or deployment decision. A standing policy that predates the finding is not a post-finding response,
except that a documented coordinated pre-deployment response may have a negative lag.

### Attribution

Attribution records whether an identified response was publicly connected to the relevant finding.

- **Explicit attribution:** the responding company directly referenced the finding, report,
  evaluation result, or evaluating institution, or stated that its response was informed by that
  evidence.
- **No explicit attribution:** a qualifying response was identified, but the company did not
  publicly state a connection to the finding.
- **Not applicable:** no company response was identified.

Attribution is assessed only where a company response exists. It measures the company's public
explanation and does not independently establish causation.

### Action Level

Action Level records the strength of the publicly documented Channel-A response.

- **None:** no public response was identified through the completed search by the cutoff date.
- **Acknowledged:** the company recognised the finding or underlying problem but specified no
  action.
- **Partial:** the company documented an action addressing only part of the problem or expressly
  described as interim, limited, or incomplete.
- **Substantive:** the company documented a specific mitigation, model change, safeguard, access
  restriction, or deployment decision directly addressing the identified problem.

Action Level measures the content of the public response. It does not establish implementation or
effectiveness.

## 9. Channel B — policy uptake

Channel B searches official parliamentary, congressional, agency, legislative, regulatory, and
government sources. General policy activity on the same topic does not qualify without an explicit
link to the finding, report, evaluation, or result.

- **No policy uptake identified:** a completed search found no official source explicitly linking
  the finding/report/result to policy activity.
- **Non-binding policy-related uptake:** an official source explicitly cited or discussed it but
  created no enforceable obligation, including statements, legislative records, consultations,
  recommendations, and guidance.
- **Binding policy action:** a law, regulation, regulatory order, or other enforceable instrument
  explicitly referenced it and imposed a mandatory requirement.

Rows without a completed Channel-B search are missing, not negative. Policy Level measures
documented uptake, not whether the finding caused the policy response.

## 10. Channel C — public and academic coverage

Channel C logs independent media, academic citations, and notable public discussion. It does not
score company action or proportionality. Record the retrieval date for citation status/counts;
counts retrieved after the corpus cutoff are present-day retrieval measures, not historical counts
as of the cutoff. The evaluator's source and company self-promotion are not independent coverage.

## 11. Proportionality

Proportionality is a deterministic combination of independently assigned Severity and Action Level
for Tier A only:

| Severity | Action Level | Proportionality |
|---|---|---|
| C1 | Substantive | Proportionate |
| C1 | Partial or Acknowledged | Under-response (gap) |
| C1 | None | Accountability gap (no action) |
| C2 | Substantive or Partial | Proportionate |
| C2 | Acknowledged | Under-response (gap) |
| C2 | None | Accountability gap (no action) |

C1 requires a Substantive response; C2 requires at least a Partial response. Acknowledgment alone
never passes, and no response always yields a no-action gap. Missing/errored severity produces a
blank Proportionality value, never an inferred outcome.

## 12. Version continuity and release controls

The audited v11 workbook is an additions corpus. Before publishing a single v11 master:

1. concatenate the 455-row revised-v10 base and the 558 retained v11 additions with an internal
   `Version origin` field;
2. do not reintroduce rows already removed as cross-version duplicates;
3. merge shared report identities while retaining distinct findings;
4. unify v11 DrugDiscoveryBench `SCALEAI-2026-06b` with v10
   `SCALEAI-2026-06-DRUGDISCOVERY`;
5. rename the v11 Agent-RLVR Report ID currently colliding with v10 FORTRESS at
   `SCALEAI-2025-06`;
6. resolve whether the exact 2026-07-30 cutoff excludes v10 `DREADNODE-2026-07-CYB2`
   (dated 2026-07-31); and
7. re-run duplicate, report-invariant, tier, channel, and headline-count audits on the merged file.

Until this is complete, do not label the additions workbook a complete successor and do not use its
counts as corpus headline statistics.

## 13. Column reference — 39 named columns

| # | Column | Rule |
|---:|---|---|
| 1 | Finding ID | Unique immutable primary key. |
| 2 | Report ID | One report-level grouping key. |
| 3 | Institution | Source-named external evaluator; finding-level for company system cards. |
| 4 | Institution Type | Government, non-profit, for-profit, academic, or joint classification. |
| 5 | Report Title | Complete source-visible title; invariant within Report ID. |
| 6 | Publication Date | Source-verified `YYYY-MM-DD`, or `YYYY-MM` if no day is available. |
| 7 | Domain | Controlled vocabulary, semicolon-separated when multi-domain. |
| 8 | Models / Systems | Subject systems only; comparators go in Notes. |
| 9 | Access Type | Pre-deployment, Post-deployment, Mixed, Aggregate, or N/A. |
| 10 | Source URL | Primary finding source; stable/frozen where possible. |
| 11 | Finding | Accurate 1–2 sentence paraphrase; every number supported. |
| 12 | Finding Quote | Verbatim supporting source text. |
| 13 | Severity (C1/C2) majority | Ensemble majority, documented C1/C2 human adjudication after no majority, or unresolved ERR. |
| 14–16 | Sonnet5 vote; GPT-5.5 vote; Gemini3.1 vote | Raw frozen votes. |
| 17 | Attribution | Explicit attribution, No explicit attribution, or Not applicable. |
| 18 | Company Response | Concise factual description from company primary evidence. |
| 19 | Channel A Verbatim | Exact response quote. |
| 20 | Response Date | Actual source-document date. |
| 21 | Lag (days) | Response Date minus Publication Date; negative allowed for coordinated pre-deployment disclosure. |
| 22 | Channel A Evidence | Company primary-source URL. |
| 23 | Action Level | None, Acknowledged, Partial, or Substantive. |
| 24 | Sources Checked (channel A) | Dated search log and adjudication notes. |
| 25 | Policy Level | No uptake, non-binding uptake, binding action, or blank if not searched. |
| 26 | Policy Response | Concise official-policy description. |
| 27 | Channel B Verbatim | Exact official-source quote. |
| 28 | Channel B Evidence | Official government URL. |
| 29 | Media Outlets | Independent coverage with URLs. |
| 30 | Academic Citations | Citation evidence and retrieval date. |
| 31 | Social Highlights | Notable public discussion with URLs. |
| 32 | Channel C Verbatim | Exact third-party coverage quote. |
| 33 | Proportionality | Deterministic §11 output. |
| 34 | Eval? (trackable) | `yes` for Tier A/B, `no` for Tier C. |
| 35 | Action Trackable? | `yes` Tier A, `no` Tier B, blank Tier C. |
| 36 | Finding Type | Canonical nature plus allowed semicolon modifiers. |
| 37 | Tags | Lowercase hyphenated semicolon-separated search terms. |
| 38 | Scope | `government-AISI` or `third-party-evaluator`. |
| 39 | Notes | Audit trail, split/club details, limitations, and tested comparators. |

## 14. Evidentiary and sign-off standard

- **Real or empty:** never fill a cell merely to make the table complete.
- Channel A uses company primary evidence; Channel B uses official government evidence; Channel C
  uses independent third-party evidence.
- A quote's presence in a source is necessary but not sufficient: it must be the evaluator's own
  assertion and materially support the Finding sentence.
- Automated checks establish consistency and locate evidence; they do not replace independent human
  verification of substantive meaning. All correction-ready and blocked source/finding judgments,
  all Tier-A response recodes, and the severity sample require documented human sign-off before
  manuscript submission.
- Do not claim “100% verified” while unresolved source-date, quote-provenance, finding-support,
  severity, or combined-version blockers remain.

## Changelog

- **2026-08-16:** reconstructed `v10 revised.xlsx` as one sheet (`v10 revised`) using the complete
  39-column data schema; retained 455 findings; incorporated the revised A/B/C encoding; sorted by
  tier and descending date; preserved tier rationale and displaced legacy response data in Notes;
  standardized full-report URLs within shared Report IDs; and removed all auxiliary workbook
  sheets. `APOLLO-2026-07-ALI4` was changed from Substantive to missing Channel A because the
  recorded evidence is Apollo's statement about Anthropic, not a public Anthropic primary-source
  response; the prior values remain in Notes. Twenty Tier-A rows still have missing Channel-A
  classification and 26 have missing Channel-B classification, so these are missing-data tasks
  rather than negative outcomes.
- **2026-08-16:** removed the September-2023 lower-date boundary and restored 25 qualifying older
  findings (A 4, B 12, C 9). Three older rows were not restored because they independently fail
  evaluator scope/attribution: `TSINGHUACOAI-2022-01-SOC1`,
  `TSINGHUACOAI-2021-05-GOV1`, and `SECUREBIO-2023-06-BIO1`. The additions corpus now has 558
  findings, and the unreconciled v10-plus-v11 total is 1,013.
- **2026-08-16:** removed `TSINGHUACOAI-2023-09-SOC1` from both active v10 data sheets because
  Tsinghua University CoAI Group is an academic research group/benchmark producer rather than a
  qualifying external evaluator organisation under §1. The record remains only in the v10 Change
  Log and the untouched raw-source archive. Revised v10 now contains 455 findings (A 123, B 161,
  C 171); at that release stage the unreconciled v10-plus-v11 total was 988.
- **2026-08-16:** project lead adjudicated `SECUREBIO-2026-06b-BIO2` as C1 after the ensemble
  returned ERR/C2/C1. Raw votes remain unchanged; Notes identifies the human override; its
  no-response proportionality is therefore Accountability gap (no action).
- **2026-08-16:** adopted the revised Attribution, Action Level, Policy Level, and
  severity-dependent Proportionality definitions; changed no-response Attribution to Not
  applicable; renamed Non-binding policy uptake to Non-binding policy-related uptake; documented
  the 39-column schema; initially enforced the then-stated September 2023 lower bound (superseded
  later the same day); recorded v10/v11 version continuity; and prohibited a 100%-verified claim
  while audit blockers remain.

- **2026-09-05 · frontier scope gate clarified; corpus corrected to 1,144.** §1 now states that the
  frontier condition is a scope gate rather than a tiering condition, and the Tier B row no longer
  lists "non-frontier system" as a Tier B reason. Those two statements contradicted each other: a
  row cannot both fail the scope gate and be admitted as Tier B, and the contradiction is what
  allowed non-frontier rows into earlier versions. §1 also now distinguishes anonymised from
  non-frontier, states that model size does not decide the gate, and excludes the evaluator's own
  constructs.

  Applied to the corpus: 23 rows removed as out of scope — eight where the evaluated model was
  built or fine-tuned by the evaluator (RAND's own A3C/TRPO/PPO agents, Redwood's password-locked
  models, Palisade's constructed backdoors), fourteen whose subject is not a model (human
  baseliners, benchmark reviews, evaluation apparatus, an open-source library audit), and one
  product from a developer that is not a frontier lab. A further 2 rows were removed as duplicates
  found by comparing Models/Systems and Finding semantically rather than by verbatim text: the same
  MultiNRC claim entered through both a paper's PDF and its landing page, and a text-only
  leaderboard that was an 86% subset of the same evaluation.

  Anonymised frontier evaluations were retained. Corpus 1,169 → 1,144 · reports 484 → 474 ·
  institutions 47 → 46 · Tier B 607 → 599 · Tier C 331 → 314. Tier A unchanged at 231 and the
  headline unchanged, since nothing removed was Tier A. Earliest publication now 2022-11-16.

- **2026-09-07 · attribution and report-identity audit; corpus corrected to 1,140 findings in 458
  reports.** Two failures of the same kind: a check keyed on where a document was *found* rather
  than on who *asserted* it.

  **Attribution.** §1 already said that "merely developing a benchmark, hosting a report, or being
  cited by another evaluator is insufficient", but nothing enforced it, because no column records
  authorship and §3 directs the search to enumerate each organisation's own publication surfaces —
  so a paper hosted on an evaluator's site was credited to that evaluator by construction. Two
  reports removed, logged in full to `logs/deleted_attribution_20260907.csv`:

  - `FARAI-2022-11` (2 rows, Tier B). *Training Language Models with Language Feedback* is by an
    NYU-centred group; neither arXiv nor FAR.AI's own page states any FAR.AI affiliation. FAR AI
    was founded in July 2022 and incorporated in October 2022, while the paper was published in
    April 2022 and presented at an ACL 2022 workshop — it predates the institution credited with
    it. The 2022-11-16 date was the arXiv v4 revision, which §3 excludes as publication evidence.
  - `UKAISI-2024-01` (2 rows, Tier C). A *TIME* article about UK AISI, not a UK AISI publication:
    secondary journalism (§1, §2.1), resting on "sources indicate" rather than a measured result
    (§2.2), and dated 2024-01-01 when its URL places it in the Davos 2025 collection (§3).

  A census of all 55 source domains found no other news, media or social sources; SecureBio's
  Substack is that evaluator's own surface and was retained.

  **Report identity.** Fourteen papers had reached the sheet under two Report IDs each. The
  existing reverse check matched on Source URL, so it caught only a report re-filed under the same
  link; these pairs carried two different links — an arXiv page and the institution's write-up, or
  a blog post and a later research page. Two ingestion passes had produced two ID conventions
  (`INST-YYYY-MM[letter]` and `INST-YYYY-MM-<abbreviated title>`), and the v12→v13 reconciliation
  preserved both because it asserted that no row was *missing* and never that none was
  *duplicated*. `scripts/audit_v13.py` now also matches on normalised Report Title, venue tags
  stripped; the check reports 14 on the pre-fix workbook and 0 after.

  No finding was duplicated — every one of the 14 pairs scored 0 overlapping findings above 0.60
  similarity, so the pairs were single papers whose distinct findings had been split across two
  IDs. The correction therefore removes double-counted *reports*, not findings.

  Corpus 1,144 → 1,140 findings · reports 474 → 458 · Source URLs 473 → 458, now equal to the
  report count · Tier B 599 → 597 · Tier C 314 → 312 · institutions unchanged at 46. Tier A
  unchanged at 231, Tier A C1 unchanged at 188, and the headline unchanged at 150/188 = 79.8%
  (Wilson 73–85%) with 112/188 = 59.6% unanswered. The clustering denominator is unchanged at 102
  C1 reports, so ICC 0.62, design effect 1.52 and effective n ≈ 124 all stand. Earliest
  publication now 2023-03-17 (METR, *Update on ARC's recent eval efforts*), verified against the
  live source for date, authorship and all three verbatim quotes.

  **Open.** 67 reports carry an academic-paper signature on their institution's own surface
  (Shanghai AI Lab 26, Scale AI 18, UK AISI 5, and ten others). Their author lists have not been
  checked against the credited institution; the founding-date sweep and domain census that caught
  the two removals above cannot settle these, only reading affiliations can.

- **2026-09-07 (second pass) · §5 enforced on the accountable-company rule; corpus 1,142.** A
  systematic check of every row naming models from more than one developer: 220 of 1,140 rows do
  so, but most are legitimate under §5 — a comparator or tested baseline may be named in the row,
  and 187 rows are explicitly anonymised and so have no accountable company to separate. Nine were
  Tier A, where the rule actually bites because that is where a response is owed; all nine were read
  by hand.

  Eight were compliant. `TRANSLUCE-2026-08-ALI1/ALI2` name GPT-5.6 Sol only under an explicit
  "Instruments (not subjects)" label. `HOLISTIC-2025-02-JAI1` names o1 as a comparator that scored
  98%/100%, and `SHANGHAIAILAB-2024-02-JAI1` names Claude2/GPT-4/GPT-3.5 as comparators showing
  *less* degradation than the subject, Gemini. `FARAI-2025-02a-JAI1` names one model whose title
  carries two developers' names, DeepSeek R1-Distill-Llama-70B. The two SecureBio rows and
  `SECUREBIO-2025-04-BIO1` each track one accountable company — OpenAI, which responded in both
  cases — over an aggregate the source declines to attribute model-by-model; that aggregation is a
  property of the source, so there is no per-company claim to split. It does mean the other
  developers in those aggregates are never counted, which belongs in Limitations, not here.

  One genuine breach. `TRANSLUCE-2024-10-JAI1` asserted three separate per-company results — a
  95.5% attack success rate against Meta's Llama-3.1 405B, 65.8% against OpenAI's GPT-4o, 22.6%
  against Anthropic's Claude 3.5 Sonnet — in a single row that no one response could address. Split
  into `-s1` (Meta), `-s2` (OpenAI) and `-s3` (Anthropic), keeping the common report identity per
  §5. The 2026-08-16 five-source battery had covered OpenAI alone; Meta and Anthropic rested on a
  2026-08-02 pass its own note recorded as "not fully earned", so both batteries were re-run on
  2026-09-07 and no admissible §8b primary document was found for either. Anthropic's
  Constitutional Classifiers work was considered and rejected — it addresses universal jailbreaks
  generally without referencing this finding — as was Anthropic's use of Transluce's Docent, a
  different product.

  `-s2` and `-s3` are left with **severity unresolved** under §7. The parent's C1 majority was
  justified on the Llama-3.1-405B result, which is now `-s1`; carrying that vote onto the transfer
  results would present a vote taken on the combined claim as a majority on a claim the ensemble
  never saw. Both rows are Tier A with severity unresolved and sit outside the C1 population until a
  fresh ensemble run or documented human adjudication. `verify_charts.py` fails while they stand,
  by design.

  Two checks were wrong in the same way and are fixed: chart 17 titled itself `n=len(ROWS)` while
  its bars only ever summed C1+C2, and the verifier asserted `C1 + C2 = corpus`. Severity may
  legitimately be unresolved, so the identity is now `C1 + C2 + unresolved = corpus` and the figure
  states how many rows await adjudication.

  Corpus 1,140 → **1,142** findings · Tier A 231 → **233** · reports, institutions, Tier B and
  Tier C unchanged. Tier A ∩ C1 unchanged at **188** and the headline unchanged at **150/188 =
  79.8%**, because `-s1` carries the parent's classification and the two new rows are unclassified.

  **Open.** §5 has been enforced by hand on Tier A only. 150 Tier B and 61 Tier C rows name more
  than one developer and have not been read individually. At the Tier A hit rate — one breach in
  nine — perhaps twenty of them are genuine breaches. Splitting those would change Tier B and Tier C
  counts and the corpus total, but not the headline, which is computed on Tier A ∩ C1 alone.

  **Schema note.** §7 requires a human severity override to be recorded "in Notes", but V13's
  39-column schema has no Notes column; the split and adjudication trail is written to
  `Sources Checked (channel A)` instead. §7 should be reworded to name the column that exists.

- **2026-09-07 (third pass) · split-row severity settled; §5 extended to Tier B and C; corpus
  1,147.** Two decisions, both recorded here because both changed published numbers.

  **Severity on split rows.** `TRANSLUCE-2024-10-JAI1-s2` and `-s3` had been left unresolved. They
  now carry the parent's classification — C1, votes C1/C1/C1, Human C1 — on the ground that a §5
  split divides one finding by accountable company without changing what was found, so the parent's
  assessment applies to each part. This is a documented human decision under §7, not a fresh
  ensemble run, and the parent's raw votes are preserved on each row. Proportionality recomputed
  from the §9 matrix: C1 × Action Level None = Accountability gap. The corpus now carries **no
  unresolved severity**, and `verify_charts.py` treats a blank majority as a hard failure anywhere
  in the corpus rather than only on Tier A, so a Tier B or C blank cannot slip past the
  tier-specific checks.

  **§5 on Tier B and C.** 211 Tier B/C rows name models from more than one developer. Screening
  reduced these to 35 needing individual reading; all 35 were read. Three classes emerged.
  Thirteen are **instrument or method findings** — the subject is the evaluator's own technique,
  detector, grader, monitor or scaffold, and the models are substrate or explicitly tagged
  comparators; these are the instrument class the project retains. About fifteen are **comparative
  leaderboards** whose claim is the ranking or the aggregate pattern, with per-model numbers as its
  evidence; §5 clubs results warranting one common response, so these stay in one row. Three were
  genuine per-company adverse breakdowns whose verbatim quote supports a per-company slice, and
  were split: `UKAISI-2024-10-JAI8` into three (OpenAI, Anthropic, Mistral),
  `UKAISI-2024-10-JAI9` into two (OpenAI, Anthropic), and `UKAISI-2025-07-JAI5` into three
  (Google — whose three Gemini variants are one company and so remain one row — Cohere, Meta).

  Four rows that look like the same class were deliberately **not** split, and the reason is the
  quote rather than the finding text. `SHANGHAIAILAB-2025-02-JAI1` is quoted as "Success rates ...
  as high as 96%, 86% and 98% respectively", which does not attribute a figure to a model;
  `SHANGHAIAILAB-2026-01-JAI1` covers 20 models across seven developers under an aggregate claim;
  `CISCO-2025-11-JAI1` asserts that multi-turn attacks beat single-turn across eight models; and
  `SHANGHAIAILAB-2024-02-JAI2` reports a distribution over 36 LLMs. In each the claim is the
  comparison, not a per-company result, so §5 clubs them. Splitting the last would also mint rows
  for Vicuna, TuluV2 and Zephyr, which have no frontier developer and would immediately fail the
  §1 scope gate — the rule would create rows only to delete them.

  Corpus 1,142 → **1,147** findings · Tier B 597 → **599** · Tier C 312 → **315** · reports and
  institutions unchanged at 458 and 46 · Tier A unchanged at **233**. Tier A ∩ C1 **190** and the
  headline **152/190 = 80.0%** (Wilson 74–85%), of which **114/190 = 60.0%** unanswered — both moved
  by the severity decision above, not by the Tier B/C splits, which touched no Tier A row.

- **2026-09-07 (fourth pass) · authorship audit begun; source-URL sweep; corpus 1,146.**

  **Authorship.** 15 of the 59 reports carrying an academic-paper signature on their institution's
  own surface were verified against their author lists. FAR.AI, the institution the earlier pass
  implicated, is now checked in full: all 14 of its reports. One removal —
  `FARAI-2025-02b`, *Universal Sparse Autoencoders* (1 row, Tier C / C2), logged with its reasons
  in `logs/deleted_attribution_20260907.csv`. It fails §1 three ways: the subject is "multiple
  pretrained **vision** models", not a frontier developer's model, so it fails the scope gate; the
  finding is that the authors' own Universal SAE method recovers coherent concepts, which "the
  evaluator's own constructs are out" excludes; and no author is a FAR.AI researcher. **The third
  reason is the weakest of the three and is recorded as uncertain:** Matthew Kowal appears on both
  this paper and FAR.AI's February 2026 persuasion paper, so he may have joined FAR.AI between
  them, exactly the timing question that decided `FARAI-2022-11`. The removal rests on the first
  two grounds, which are independent of authorship.

  A useful discriminator emerged. FAR.AI splits its site into `/blog/`, which carries its own
  writing, and `/research/`, an index that also lists work by affiliated researchers. All 9 `/blog/`
  reports are genuine; 2 of 5 `/research/` reports were not. The same test should be applied to any
  institution that maintains a publications index.

  Verified compliant, with the reason: `ANTHROPIC-2026-05-SELF-SLEIGHT` and
  `ANTHROPIC-2025-06-SELF-SHADE` name Redwood Research (and Scale AI) in their bylines, and §1
  makes the Institution the external evaluator rather than the model developer, so omitting
  Anthropic is the rule working as intended, not a defect. FAR.AI's `FARAI-2024-08`,
  `-2025-04`, `-2026-02`, `-2026-02b` and `-2026-02-PERSUASION` all carry FAR.AI authors (Gleave,
  Pelrine, Garriga-Alonso, Taufeeque, Cundy, Bowen). `CAIS-2026-04` is stamped "© 2026 Center for
  AI Safety". Shanghai AI Laboratory's reports resolve into two verified lab groups — Jing Shao's
  safety group (`SALAD-Bench`, `OASIS`) and Chaochao Lu's causal group (`Beyond Surface
  Structure`) — plus five hosted on the lab's own domain.

  **A caution on method.** A page that does not print affiliations is not evidence of external
  authorship. An automated summary reported FAR.AI's prefill-jailbreak paper as
  "externally-authored, no FAR.AI affiliation" when its authors include Adam Gleave, FAR.AI's
  co-founder. The test is author identity against the institution's roster, never whether the page
  displays an affiliation line.

  **Source-URL sweep.** All 457 distinct Source URLs were probed. 444 return 200 and 6 redirect.
  Three openai.com URLs return 403, which is the documented block behind `fetch.py`'s ladder and
  not a death. Four are genuinely broken and need replacement links, since §2 requires a working
  primary Source URL and these cannot currently be verified by a reader:
  `NETWORK-2025-07` (404, **5 findings**), `SCALEAI-2026-07-FRONTIERBENCH` (404, 2),
  `SCALEAI-2025-11` (404, 1) and `META-2026-07-MUSESPARK` (400).

  The sweep also fixed `FARAI-2026-02`, found because its URL 404'd: the link now resolves, the
  title is the full *The Obfuscation Atlas: Mapping Where Honesty Emerges in RLVR with Deception
  Probes* rather than "Obfuscation atlas", and the date is 2026-02-16 as the page states, not
  2026-02-17.

  Corpus 1,147 → **1,146** findings · reports 458 → **457** · Source URLs 458 → **457**, still
  equal to the report count · Tier C 315 → **314** · C2 807 → **806**. Tier A unchanged at 233,
  Tier A ∩ C1 unchanged at 190, clustering denominator unchanged at 102 C1 reports, and the
  headline unchanged at **152/190 = 80.0%** (Wilson 73.7–85.1%) with **114/190 = 60.0%** unanswered.
  The removal was Tier C, so no analytical quantity moved.

  **Open.** 44 of the 59 reports still need individual author verification: about twenty Shanghai
  AI Laboratory arXiv and venue papers, currently attributed to the two verified lab groups by
  cluster rather than checked one by one; CAIS 2; METR 2; Princeton HAL 2; SecureBio 1; and the
  17-report low-risk block (Scale AI, UK AISI, Dreadnode), whose surfaces are institutional
  publication pages rather than indexes of others' work. The four broken source links above are
  also open.
