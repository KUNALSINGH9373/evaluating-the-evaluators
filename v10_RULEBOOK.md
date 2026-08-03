# Evaluating the Evaluators — Rulebook (v10)

**Canonical dataset:** `~/Desktop/v10.csv` (456 findings · 211 reports · 40 columns · window Sep 2023 – 31 Jul 2026)
**Status:** living document — update whenever a rule changes; every change gets a Changelog entry.
**Companions:** `SEARCH_PROTOCOL.md` (in the dashboard repo — full search/screening procedure), `run_severity_ensemble.py` (the frozen severity prompt), `screening_ledger.csv` (being built by the evidence sweep).
**Last updated:** 2026-08-03

---

## 1. What the dataset measures & scope

The dataset measures the **public-channel accountability pipeline**: when a government AI Safety
Institute (or comparable evaluator) publishes a finding about a specific model/company, does a
documented response follow?

- **In scope, headline stats** (`Scope = government-AISI`): UK AISI, US CAISI/NIST, the national
  AISIs affiliated via the International Network (Japan, Singapore, Korea, France PEReN/INESIA,
  EU AI Office, Canada, Australia, Kenya), and any joint exercise that includes a government AISI
  (even with a non-government co-author).
- **Kept, stratified, excluded from headline stats:** `third-party-evaluator` (no government
  co-author, e.g. METR alone) and `company-self-report` (a company evaluating its own model).
- **Hard drop (not in the sheet; logged in the screening ledger):** reports naming no evaluating
  agency at all ("external evaluators"); never-published MOU findings; non-English-only output;
  rows failing source verification.

## 2. What qualifies as a FINDING (the unit of analysis)

A **finding** is a discrete, evidence-backed claim asserted by an in-scope evaluator in a public
report, codeable independently of the report's other claims. All three must hold:

1. **Asserted by the evaluator** — not a summary of someone else's work; not a comparator score
   cited in passing (comparators → Notes as `[Report tested: …]`).
2. **Evidence-backed in that report** — a measured result, observed behaviour, or documented
   process fact. Opinions, recommendations, and forward-looking plans are not findings.
3. **Independently codeable** — it would warrant its own response (the club test, §5).

Three kinds qualify: **empirical model findings** (a specific system's capability/behaviour/
safeguard — including reassuring nulls), **methodology/tooling findings**, and
**governance/process findings**. Announcements, partnership news, opinion pieces, and plans
contain no findings.

## 3. Search & screening rules (summary — full procedure in SEARCH_PROTOCOL.md)

- **Roster is derived, never hand-picked** (Stage 0 of every sweep): current membership of the
  International Network of AI Safety Institutes + current members of the AI Evaluators Forum +
  every org already in the dataset (grandfathered) + four company-artifact sources (OpenAI,
  Anthropic, Google DeepMind, Meta — swept only for named-evaluator findings). Zero-yield orgs
  are swept anyway and logged as zeros.
- **Venue = the org's own publication surfaces**: research/blog/publications index pages
  (paginated to the end; sitemap fallback), plus arXiv via the org's own publication list and
  citation-chasing — never open keyword search.
- **Window:** each org's first publication → the frozen corpus cutoff (**2026-07-30**). Later
  qualifying items are logged `POST-CUTOFF` for the next version.
- **Every enumerated item gets exactly one decision** (with a one-line reason, in the ledger):
  `INCLUDED` · `EXCLUDED — no findings` · `EXCLUDED — no named evaluator` ·
  `EXCLUDED — non-English` · `EXCLUDED — out-of-scope org` · `EXCLUDED — duplicate/secondary` ·
  `POST-CUTOFF`.
- **Dedup:** the primary (earliest, fullest) source wins. Progress reports / annual summaries are
  duplicate/secondary unless a finding appears nowhere else.
- **Reconciliation after every sweep:** (a) every Report ID in the canonical CSV must appear as
  INCLUDED — a gap means re-sweep that org; (b) INCLUDED items absent from the sheet are
  candidate misses → triage; (c) zero-yield venues reported explicitly.

## 4. Tier assignment (who is accountable)

Every finding sits in exactly one tier, encoded by `Eval? (trackable)` + `Action Trackable?`:

| Tier | Encoding | Meaning | n (v10) |
|---|---|---|---|
| **A** | yes / yes | Accountability-relevant: named company/model + concerning + response reasonable to expect. The ONLY tier scored for proportionality. | 111 |
| **B** | yes / no | Concerning but no accountable party: anonymised models, methodology findings, reassuring nulls, non-frontier, capability trends. | 240 |
| **C** | no / (blank) | Not an empirical model finding (methodology/framework/governance/milestone). | 105 |

**Tier A test — ALL must hold:** (1) empirical model finding; (2) names a specific company or
model (company-level suffices; "anonymised" fails); (3) demonstrates a concerning result for which
a specific company response is reasonable to expect. Condition (3) **excludes**: reassuring nulls;
benchmark-score/relative-uplift results with no dangerous threshold crossed; inconclusive results;
comparative rankings; capability trends/forecasts; findings where named models are instruments of
a methodology study, not its subject; company self-classifications ("we treat this as High
capability"); non-frontier models; too-recent findings.

> ⚠ **Known gap (to close):** 65 solo capability-findings are outside Tier A on condition (3) or
> frontier/scope judgments whose per-row justification is not yet written into `Sources Checked`.
> Backfill required; the paper carries a government-AISI-only sensitivity line as the guard.

## 5. One finding per row (split & club rules)

- **Different companies never share a row.**
- **Club** findings that warrant the *same* response — decisive test: *did (or would) the company
  respond to them as one thing?* (e.g. four Constitutional-Classifiers bypasses → one
  restructuring → one row).
- **Split** findings that warrant *distinct* responses (capability vs safeguard-failure; different
  domains of the same model).
- **Comparators/baselines are never rows** → `Notes: [Report tested: …]`.
- On a split, part 1 keeps the base Finding ID; parts 2+ get `-s2`, `-s3` suffixes. Both remain
  live rows.

## 6. Identifier rules

### 6.1 Finding ID — the primary key

**Format:** `PREFIX-YYYY-MM[m]-DDDn[-sN]`
- `PREFIX` — institution prefix (registry below). New orgs get a prefix assigned once, here.
- `YYYY-MM` — the report's publication year-month. `[m]` = optional lowercase letter (`a`, `b`)
  distinguishing multiple same-month reports from one org.
- `DDD` — three-letter domain code (registry below) reflecting the finding's domain **at initial
  assignment**.
- `n` — sequence number within report+domain. `[-sN]` — split suffix (§5).

**Rules:**
1. **Unique** across the sheet (v10: 456/456 ✓) — the primary key for the dashboard, the paper's
   appendices, and the ledger.
2. **Immutable.** IDs are keys, not semantics: if a row's Domain is later recoded, or a date is
   corrected, the ID does NOT change. (23 IDs carry domain codes that no longer match the revised
   Domain column — this is expected, not an error.)
3. Legacy variants are grandfathered, never retro-fixed: trailing `b` on the sequence
   (`…-ALI1b`), uppercase month letter (`2026-05B`), hyphenated prefix (`AISI-JP-…`). New IDs
   follow the format above strictly.

**Institution prefix registry:** UKAISI · USCAISI · JOINT (any multi-org exercise) · SECUREBIO ·
METR · APOLLO · NETWORK · SGAISI · FRANCE · UL · CISCO · SHANGHAIAILAB · TSINGHUACOAI · HAL ·
LATTICEFLOW · TRANSLUCE · SCALEAI · CIP · PALISADE · DREADNODE · FARAI · RAND · OPENAI ·
ANTHROPIC · AISI-JP (legacy) · *(new orgs: add here before first use)*

**Domain code registry:** JAI Jailbreaks · CYB Cyber · BIO Bio-Chem · ALI Alignment ·
AUT Autonomy · SOC Societal · HUM Human Influence · GOV Governance/process.

### 6.2 Report ID — the grouping key

- Groups all findings extracted from one report; **must be unique per report** (two different
  reports must never share an ID — split collisions with a letter suffix: `UKAISI-2026-03` /
  `UKAISI-2026-03b`).
- **Format going forward:** `PREFIX-YYYY-MM[-slug]` — slug only when needed to disambiguate.
- Legacy Report IDs use three coexisting conventions (bare month, finding-style, descriptive slug
  like `OPENAI-2025-08-SELF`) — grandfathered, never renamed.
- All rows sharing a Report ID must share the same Report Title, Source URL, **and Publication
  Date** (⚠ 8 reports currently violate the same-date rule — flagged for repair; see Open Items).

## 7. Severity (C1/C2) — the ensemble rule

- Coded by **three independently queried models** (Claude Sonnet 5, GPT-5.5, Gemini 3.1) applying
  the frozen prompt in `run_severity_ensemble.py` (D1–D7 dangerous-capability domains, each with a
  fixed decision boundary). **Majority vote wins; all three votes stay on the record.**
- C1 requires a **demonstrated** threshold (working universal jailbreak, full attack chain,
  expert-surpassing bio capability, …) — not alarming wording, not model-vs-model uplift, not a
  trend, not a negation.
- Non-unanimous rows (34 in v10: 29 true 2–1 splits + 5 single-model errors decided 2–0) are
  published in the paper's Appendix D. A unanimous vote that conflicts with the written rule is a
  re-vote candidate, not an authority.

## 8. Response attribution rules (Channel A)

A company action counts as a response **only if causally attributable to the finding**:
- **Pre-existing/standing policy is NOT a response** (a framework clause or product decision that
  predates the finding does not count, even on the same topic).
- **Company self-reports are not third-party responses.**
- **Negative lag is allowed** for pre-deployment evaluations (the company had the findings before
  publication); lag 0 = coordinated disclosure; never use 0 as a placeholder.
- Response dates are the **actual dates of the source documents**, verified.
- A "None" coding should record where we searched (Sources Checked) with the search date.

## 8b. Response-search protocol (Channels A, B, C) — how to search, per Tier A finding

The mirror of the finding-search protocol: a fixed battery, executed in order, each source
logged with its check date in `Sources Checked`. **Search window: finding publication date →
corpus cutoff** (re-swept quarterly for open None/Partial rows).

### Channel A — company response (determines Action Level)
Battery (all five checked before a `None` may be coded):
1. **Company newsroom/blog** — site search for the evaluator's name and the finding's model/topic.
2. **The next model/system card(s)** for that model family published after the finding — and for
   pre-deployment evaluations, the launch card itself (the canonical response location).
3. **Company safety/deployment hubs** (e.g. deploymentsafety.openai.com, Anthropic
   safeguards/RSP pages, transparency reports).
4. **Official company accounts/newsroom posts** (e.g. an OpenAI Newsroom statement).
5. **Open web search**: `<company> response <evaluator> <finding topic>` — used only to *locate*
   company primary sources; news articles themselves are never Channel A evidence.

Rules: admissible evidence = the company's own primary document only. Any candidate response
**dated before the finding** is invalid unless it is a documented pre-deployment coordinated
disclosure (§8 negative-lag rule) — record invalidations in Sources Checked. Stop condition:
battery exhausted → `Action Level = None` + dated search log. Classification (Substantive /
Partial / Acknowledged) per §9 col 17.

### Channel B — policy uptake (determines Policy Level)
Battery: 1. **UK**: Hansard (Commons + Lords) + committee reports + gov.uk ministerial
statements + regulator advisories (NCSC, BoE/FCA, ICO). 2. **US**: Congress.gov, Federal
Register, agency announcements (Commerce/NIST), committee records. 3. **EU/other**: Commission
statements, national regulator publications matching the finding's jurisdiction. Search terms:
evaluator name, report title, and the finding's specific claim. Admissible = official government
sources only. Classification: Binding policy action / Non-binding policy uptake / No policy
uptake identified (Tier A rows only; the last is coded only after the battery is exhausted).

### Channel C — coverage log (no score; feeds the obscurity check)
Log, with URL and date: independent press coverage (news search on evaluator + finding),
academic citations (Semantic Scholar / Google Scholar count, dated), notable public discussion
threads. The finding's own paper and the company's own posts are circular → excluded. This
channel is evidence, not measurement: nothing is computed from it except the documented-coverage
share of no-response findings.

## 9. Column reference (all 40 columns)

Legend: 🔑 identifier · 📋 descriptive · 📊 analysis input · 🧾 evidence/audit · ⚙️ derived (never hand-edit).

| # | Column | Type | Meaning, allowed values, and what matters |
|---|---|---|---|
| 1 | Finding ID | 🔑 | Primary key. Rules in §6.1. Unique, immutable. |
| 2 | Report ID | 🔑 | Groups findings of one report. Rules in §6.2. |
| 3 | Institution | 📋 | The **evaluating** body, canonical spelling; must match what the source names. Joint variants spell out all parties. |
| 4 | Report Title | 📋 | Verbatim title of the source report. Same for all rows of a Report ID. |
| 5 | Publication Date | 📊 | The report's real release date, source-verified. `YYYY-MM-DD` (or `YYYY-MM` if that's all the source gives). **Date only, never a time.** Feeds Lag and per-year stats. Same for all rows of a Report ID. |
| 6 | Domain | 📊 | Finding-level, multi-select (semicolon), controlled vocabulary: Cyber, Bio-Chem, Alignment, Jailbreaks, Autonomy, Societal, Human Influence + governance sub-types (Institutional, Eval-methodology, Eval-tooling, Transparency/Disclosure, International-coordination, Policy/Standards, Frontier-forecasting). Never blank, never bare "Governance". |
| 7 | Tags | 📋 | Internal search aid only (lowercase-hyphenated, semicolons): models, companies, techniques, benchmarks. Not analytical. |
| 8 | Models / Systems | 📋 | The finding's **subject** model(s) only; comparators → Notes. "anonymised" when the source doesn't name it (⚠ 37 blanks pending this fix). |
| 9 | Access Type | 📊 | Pre-deployment / Post-deployment / Mixed / Aggregate / N/A. Drives the paper's most policy-relevant split. |
| 10 | Source URL | 🧾 | Primary source **of the finding** — the evaluator's own report where one exists; a company document only if it is the sole publisher (then Finding Type gets `company-published`). |
| 11 | Finding | 📋 | 1–2 sentence paraphrase; every number verified against the source; no overstatement. |
| 12 | Finding Quote | 🧾 | Verbatim quote supporting the finding. *(Currently byte-identical to Key Quote in all rows — kept deliberately; treat Key Quote as authoritative.)* |
| 13 | Severity (C1/C2) majority | 📊 | Majority of the three ensemble votes. §7. |
| 14–16 | Sonnet5 / GPT-5.5 / Gemini3.1 vote | 🧾 | The three raw ensemble votes (C1/C2/ERR). Never overwritten. |
| 17 | Action Level | 📊 | Tier A only. **Substantive** (specific, documented, attributed change) / **Partial** (claimed but unverifiable, or incomplete) / **Acknowledged** (referenced, no action) / **None** (nothing located). Coherence: response fields filled ⇔ level ≠ None. |
| 18 | Attribution | 📊 | Tier A only, two categories: **Explicit attribution** (company names the evaluator/finding) / **No explicit attribution** (everything else, incl. no response). |
| 19 | Company Response | 📋 | Concise factual clause from the company's own primary source. No URLs in text. |
| 20 | Channel A Verbatim | 🧾 | Character-exact quote of the response from the company source. |
| 21 | Response Date | 📊 | Actual date of the company source document. |
| 22 | Lag (days) | ⚙️ | = Response Date − Publication Date. Negative allowed (pre-deployment); 0 = coordinated disclosure. Exists ⇔ Response Date exists (⚠ 3 violations pending fix). |
| 23 | Channel A Evidence | 🧾 | Company primary-source URL. Exists ⇔ a response exists (⚠ 6 violations pending fix). |
| 24 | Sources Checked | 🧾 | The audit-trail cell, four uses: dated search logs behind None codings; negative-lag invalidation records; verification pointers behind confirmed responses; tier-assignment justifications. |
| 25 | Policy Level | 📊 | Three categories: **Binding policy action** / **Non-binding policy uptake** / **No policy uptake identified** (Tier A rows that were searched with nothing found). Non-Tier-A rows may be blank (not systematically searched). Official government sources only. |
| 26 | Policy Response | 📋 | What the policy action was, from the official source. |
| 27 | Channel B Verbatim | 🧾 | Exact quote from the government source. |
| 28 | Channel B Evidence | 🧾 | Official government URL. |
| 29 | Media Outlets | 🧾 | Independent press coverage, each item with its URL. Powers the obscurity check. |
| 30 | Academic Citations | 🧾 | Verified citations/counts with sources (e.g. Semantic Scholar, dated). |
| 31 | Social Highlights | 🧾 | Notable public discussion, with links. Log only. |
| 32 | Channel C Verbatim | 🧾 | Quotes from third-party coverage. Log only. |
| 33 | Proportionality | ⚙️ | **Formula, no discretion, severity-dependent (v10, revised 2026-08-03):** C1+Substantive → Proportionate · C1+Partial/Acknowledged → Under-response (gap) · C1+None → Accountability gap (no action) · C2+Substantive/Partial → Proportionate · C2+Acknowledged → Under-response (gap) · C2+None → Accountability gap (no action). Equivalently: C1 requires a Substantive response to pass; C2 requires at least a Partial response. No too-recent exception (the 3 rows carrying a `too-recent` Finding Type modifier are already excluded upstream at Action Trackable = no, so they never reach this formula). Computed on Channel A only, Tier A rows only (Action Trackable = yes ⇔ Action Level populated); policy uptake never substitutes. |
| 34 | Notes | 🧾 | Audit trail: `[CLUBBED …]` `[SPLIT …]` `[RECLASSIFIED …]` `[Report tested: …]`, caveats. |
| 35 | Key Quote | 🧾 | Short exact verbatim from the source report supporting the finding. Authoritative quote cell. |
| 36 | Traceability Tag | 📋 | Legacy column (mixed vocabulary, overlaps Finding Type). Retained; do not extend — new rows may leave blank. |
| 37 | Eval? (trackable) | 📊 | yes = empirical model finding; no = Tier C (§4). |
| 38 | Action Trackable? | 📊 | yes ⇔ full Tier A test (§4). Blank on Tier C rows. |
| 39 | Finding Type | 📊 | Nature (exactly one): `capability-finding` / `methodology` / `capability-trend` / `governance` + modifiers (0+): `anonymised-model`, `reassuring-null`, `company-self-report`, `too-recent`, `non-frontier`, `company-published`. |
| 40 | Scope | 📊 | `government-AISI` / `third-party-evaluator` / `company-self-report`. Headline stats use government-AISI only. |

## 10. Cross-cutting evidentiary standard

- **Real-or-empty:** every cell is verified-real or deliberately blank/None — never inferred,
  never fabricated.
- **Admissible sources:** Channel A = the company's own primary document; Channel B = official
  government source; coverage logs = independent third parties. **News quoting a company is
  not Channel A.**
- **Coherence:** evidence links exist only where a response/coverage exists; "where we looked"
  lives in Sources Checked.
- Every number and quote verified against the *correct* cited source.

## 11. Open items (tracked here until resolved)

1. **Too-recent rule** — pending decision: drop category (73%→75%) / 30-day censoring (78%) /
   60-day (77%) / keep with footnote. Currently one hand-judged row.
2. **8 reports with internally inconsistent Publication Dates** (RepliBench, STACK, RealityTest,
   OpenClaw + 4) — resolve each to the true release date.
3. **Coherence repairs:** 3 Lag-without-Response-Date rows; 6 Channel-A-evidence-without-Action
   rows; 11 Policy-Response-without-uptake rows; 37 blank Models/Systems → "anonymised".
4. **5 ensemble ERR votes** — re-run the errored model (needs API keys).
5. **Tier A justification backfill** for the 65 excluded solo capability-findings (§4 note).
6. **Screening ledger** — sweep PARTIALLY complete (2026-08-01, halted by org spend limit):
   roster of 46 orgs derived and cached; 17 of ~40 venues fully screened → 885 ledger rows
   (182 INCLUDED; 90/153 known Report IDs re-found; 86 unmapped candidates awaiting triage) in
   `screening_ledger_PARTIAL.csv`. Enumerations for most remaining venues are cached in the
   workflow (run wf_dd0ca140-5d6) — resume when budget allows; only failed screening chunks
   re-run. Roster discoveries to act on: the Network was RENAMED (Dec 2025) to "International
   Network for Advanced AI Measurement, Evaluation and Science" (update paper terminology);
   AI Evaluator Forum founding members (Dec 2025): Transluce, METR, RAND, Princeton HAL,
   SecureBio, CIP, Meridian Labs, AVERI; Germany AISI approved 2026-06-09 (pre-launch);
   IndiaAI Safety Institute exists since Jan 2025; Meridian Labs + Gray Swan are Forum/roster
   orgs with no dataset presence yet.
7. **Human validation** of the severity ensemble (~20% stratified sample, report κ) before
   submission.

## Changelog

- **2026-08-03 · Proportionality rule changed to severity-dependent; one row recoded.**
  `APOLLO-2026-07-ALI2` (C2, Action Level=Partial) recoded from `Under-response (gap)` to
  `Proportionate`, so that C2 findings require only a Partial response (not Substantive) to
  pass — matching the rule: C1+Substantive / C2+Substantive-or-Partial → Proportionate;
  C1+Partial-or-Acknowledged / C2+Acknowledged → Under-response (gap); None → Accountability
  gap (no action) for both severities. This reverses the same-day "uniform across severity"
  correction below — that entry now describes the *prior* state, kept for the audit trail.
  Pre-edit CSV backed up to `v10_backup_before_prop_fix.csv`. Effect on headline stats: C1-only
  gap unchanged (64/78 = 82.1%, the row is C2); all-Tier-A gap moves from 93/111 (83.8%) to
  92/111 (82.9%).
- **2026-08-03 · Stale headline counts corrected.** Header dataset stats, ID-uniqueness check
  (§6), and Tier table (§4) still read 345 findings / 153 reports / Tier A=55 / Tier B=185 from
  an earlier growth stage of the sheet; corrected throughout to the actual current `v10.csv`
  state (456 findings / 211 reports / Tier A=111 / Tier B=240 / Tier C=105). §9 row 33
  (Proportionality) also corrected: the documented formula still had the retired v9 rule
  (C2 auto-pass to Proportionate regardless of Action Level; a "too-recent" carve-out) — the
  actual sheet applies one uniform mapping (Substantive→Proportionate, Partial/Acknowledged→
  Under-response, None→Accountability gap) identically to C1 and C2, and no row ever hits the
  too-recent path because those rows are excluded upstream at Action Trackable=no.
- **2026-08-01 · §8b added** — response-search protocol: fixed Channel A five-source battery
  with stop condition, Channel B jurisdiction battery, Channel C logging rules; quarterly
  re-sweep cadence for open rows.
- **2026-08-01 · v10 rulebook created.** Consolidates codebook v6 + SEARCH_PROTOCOL v1 + v10
  category changes: Attribution → 2 categories; Policy Level → 3 categories; Traction Score
  column deleted (coverage logs retained); finding definition added (§2); ID rules formalized
  incl. immutability, prefix/domain registries, Report ID format (§6); Sources Checked's four
  uses documented; column reference updated to the 40 v10 columns.
