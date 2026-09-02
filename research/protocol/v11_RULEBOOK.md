# Evaluating the Evaluators — Rulebook (v11 audited additions)

**Project question:** Do third-party AI evaluations matter?

**Corpus cutoff:** 2026-08-29 (moved from 2026-07-30 by the window-extension sweep). **Eligible
publication period:** no lower-date boundary; the report must have been publicly available on or
before the cutoff. The earliest publication actually held is 2020-05-29, the latest 2026-08-27.

**Current file — there is exactly one.** `dataset/AISIEVAL_V13.xlsx`, sheet `AISIEVAL_V13`, read
only through `scripts/dataset_source.py`. **1,169 findings · 484 reports · 47 institutions ·
39 columns · Tier A 231 · B 607 · C 331 · headline 113/188 = 60.1%.**

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

**Last updated:** 2026-08-16.

---

## 1. Scope and accountable unit

The dataset measures the public accountability pipeline after an external evaluator publishes a
finding about a frontier AI model or developer.

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
| B | `Eval? = yes`; `Action Trackable? = no` | Empirical, but fails at least one Tier-A condition: anonymised model, reassuring/null result, bare score or ranking without a concerning threshold, non-frontier system, capability trend, inconclusive result, or company response is not reasonably assessable. | Descriptive analysis only. |
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
