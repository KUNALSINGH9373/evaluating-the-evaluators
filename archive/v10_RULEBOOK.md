# Evaluating the Evaluators — Rulebook (v10)

**Canonical dataset:** `~/Desktop/v10.csv` (456 findings · 211 reports · 40 columns · window Sep 2023 – 30 Jul 2026 corpus cutoff, per §2)
**Status:** living document — update whenever a rule changes; every change gets a Changelog entry.
**Companions:** `SEARCH_PROTOCOL.md` (in the dashboard repo — full search/screening procedure), `run_severity_ensemble.py` (the frozen severity prompt), `screening_ledger.csv` (being built by the evidence sweep).
**Last updated:** 2026-08-14

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
  co-author, e.g. METR alone).
- **Hard drop (not in the sheet; logged in the screening ledger):** reports naming no evaluating
  agency at all ("external evaluators"); **company self-reports** (see below); never-published
  MOU findings; non-English-only output; rows failing source verification.

**Company-published reports — hard drop (added 2026-08-14; clarified 2026-08-14).** A report
published by a model developer with **no government AISI and no independent (non-developer)
evaluator associated** is out of scope entirely: it is not entered in the sheet, only logged in the
screening ledger as `EXCLUDED - company self-report`. The accountability pipeline this dataset
measures requires an independent party to make the finding.

> **The test is the evaluator's independence, not whose model was evaluated.** The drop applies
> even when a developer evaluates *someone else's* model — Google DeepMind publishing on GPT-4,
> or a cross-lab exercise between two developers — because a competing developer is an interested
> party, not an independent evaluator. **The four model developers (OpenAI, Anthropic, Google
> DeepMind, Meta) can never satisfy the named-evaluator test for one another.** Only a government
> AISI or a non-developer third-party evaluator (METR, Apollo, SecureBio, Gray Swan, Irregular,
> Deloitte, Faculty, Transluce, Redwood, CAIS, …) qualifies.
>
> **Facilitation is not contribution:** an acknowledgement thanking an evaluator for *facilitating* an
> exercise does not make it a named evaluator of findings.
>
> **Using an evaluator's benchmark, dataset, scaffold or framework is not contribution either**
> (added 2026-08-14). If the developer ran the evaluation itself, the finding is the developer's,
> whoever built the instrument. The test is *who ran the evaluation and asserts the result*, not
> whose questions were used.
>
> | Pattern | Verdict |
> |---|---|
> | "we evaluate models on 350 virology troubleshooting questions **from SecureBio**" | ✗ benchmark usage — developer ran it |
> | "we adopt the **METR** modular scaffold" | ✗ tool usage |
> | "our CTF suite can be run with **UK AISI's** evaluation framework" | ✗ framework usage |
> | "**Apollo Research** evaluated o3 and o4-mini for in-context scheming" | ✓ evaluator ran it |
> | "**UK AISI** was given access to an early snapshot … their findings are:" | ✓ evaluator ran it, results reproduced |
> | "in a joint study **with the UK AI Security Institute**" | ✓ joint authorship |
>
> This is the same rule already applied to Google DeepMind, whose model cards cite METR scaffolds
> and SecureBio benchmarks but contain no externally-run evaluation.

This codifies existing practice — v10 has never contained a `Scope = company-self-report` row.

> **Carve-out (load-bearing — do not collapse this rule into "drop anything a company published").**
> Many company system cards contain a section contributed by a named external evaluator. That
> section is **in scope**. Its findings enter under the **evaluator's** Institution and the
> evaluator's Scope (`government-AISI` if a government AISI contributed, else
> `third-party-evaluator`), with `company-published` on Finding Type — never under the company.
> The company's own surrounding self-assessment in the same document remains a hard drop.
> Worked examples already in v10: `JOINT-2026-07-*` (GPT-5.6 System Card → *Joint UK AISI +
> OpenAI (company-published)*, `government-AISI`); `OPENAI-2025-08-SELF` (GPT-5 System Card →
> *Apollo Research*, `third-party-evaluator`); `ANTHROPIC-2026-06-SELF` (Claude Fable 5 &
> Mythos 5 System Card → *UK AISI*, `government-AISI`); `JOINT-2025-05-ALI2..ALI5` (Claude Opus 4
> & Sonnet 4 System Card → *Apollo Research + Anthropic*, `third-party-evaluator`).
>
> The screening test for any item on a company venue is therefore **not** "does it contain a
> finding?" but the far cheaper **"is an external evaluator named as contributing findings?"** —
> no → `EXCLUDED - company self-report`; yes → `INCLUDED`, filed under that evaluator.

### 1.1 The evaluation-vs-benchmark decision procedure (added 2026-08-15)

§1 states the principle; this is the operational procedure. It was applied to all 67 v11 rows
sourced from a developer domain and resolved 65 of them from source text alone.

**Do not classify from the Institution field, the Source URL, or the reason a row was previously
excluded.** Go to the source document and find *the sentence that asserts the result*. The
grammatical subject of that sentence is the evaluator. Everything follows from that one reading.

| What the document says | Verdict | Why |
|---|---|---|
| "**Irregular evaluated** GPT-5.6 Sol across three suites … **Irregular found** that…" | ✓ KEEP | Evaluator ran it and asserts it |
| "**Pattern Labs … evaluated** o3 and o4-mini's ability to solve three types of challenge" | ✓ KEEP | Evaluator ran it |
| "They shared with us the following findings, **reproduced verbatim**: UK AISI tested…" | ✓ KEEP | Evaluator's own words, developer is only the host |
| "**GraySwan additionally ran** prompt injection attacks using their private ART benchmark" | ✓ KEEP | Evaluator ran it |
| "**we** also evaluate the model in agentic contexts" *(on Agentic Misalignment)* | ✗ DROP | Developer ran another party's benchmark |
| "Select machine learning engineering tasks **from METR**: 0/10 trials" | ✗ DROP | Developer ran the evaluator's task set |
| "a benchmark **built in partnership with** Gray Swan, UK AISI, US CAISI … **we organized** a competition" | ✗ DROP | Co-construction, then developer-run |
| "**we** identified three incidents … within the evaluation environment of Irregular" | ✗ DROP | Developer reviewing its own infrastructure; the evaluator is the venue, not the asserter |
| "we shared a pre-release snapshot with **additional external partners**" | ✗ DROP | No named evaluator (see below) |

**Three sub-rules that the principle implies but which were being applied inconsistently:**

1. **Benchmark co-authorship is not contribution — and it is not co-attribution either.** Gray Swan
   developed the ART benchmark *in collaboration with UK AISI*. When Gray Swan then runs ART against
   a model, the finding is **Gray Swan's alone**. UK AISI does not become a co-author of every
   finding produced by an instrument it helped build, and such a row is **not** `government-AISI`
   scope. Corrected in v11: `ANTHROPIC-2026-03-SONNET46-JAI1`.
2. **"External partners", unnamed, fails the named-evaluator test.** A developer that reports
   external testing without naming the tester has not produced an attributable finding, however
   substantive the result. Dropped in v11: `ANTHROPIC-2026-XX-MYTHOS-AUT1` and `-AUT2` — the Mythos
   Preview card names METR and Epoch AI in §2.3.7 but attributes the reported block to "additional
   external partners", and never names UK AISI anywhere. `-CYB1` has the same defect (§3.4, unnamed
   partners) but was already out as a v10 duplicate of `UKAISI-2026-04-CYB3`; per the order-of-tests
   rule below, the duplicate reason stands as recorded.
3. **A stated collaboration carries every named party.** SHADE-Arena — *"a collaboration between
   researchers at Anthropic, Scale AI (Xiang Deng and Chen Bo Calvin Zhang) and Redwood Research
   (Tyler Tracy and Buck Shlegeris)"* — is filed under **Redwood Research + Scale AI**. Omitting a
   named co-author because it was not the one that came to mind is an attribution error.

**Thin-authorship cases.** SLEIGHT-Bench is 4:1 Anthropic:Redwood (Tyler Tracy is the sole external
author) and was produced inside the Anthropic Fellows Program. **Ruled 2026-08-15: retain.** A named
independent co-author who ran the work satisfies §1; author-count ratios are not a scope criterion.
SHADE-Arena is the stronger case on the same rule and both are in. Record the ratio in `Notes` so
the boundary is visible to a reader rather than silently applied.

**Order of tests when a row fails more than one.** A row can fail the §1 scope test *and* be a v10
duplicate *and* lack a measured result. Record the reason that is **independent of the others**,
because a later rule change may reverse one without reversing the rest. In v11 this mattered:
five rows read as company self-reports were actually excluded as v10 duplicates or for having no
result, so the §1 amendment did not reinstate them. Only `OPENAI-2025-04-SELF-CYB1` came back, and
because its stated reason ("reports no outcome") was simply wrong — the Pattern Labs conclusion sits
later in §3.9.3 than the original extraction read.

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
- **Grandfathering attaches to the publisher, never to a co-author** (2026-08-14). An org named
  inside a joint `Institution` string is not thereby a roster org; the report is already captured
  under its publisher. Seven orgs added this way — Ai2, UC Berkeley, Thorn, EPFL, Yale, Stanford,
  Oxford — are retired (1,405 enumerated items, 0 inclusions). See `SEARCH_PROTOCOL.md` §2.
- **Retired venues** (2026-08-14, `SEARCH_PROTOCOL.md` §2.1): the seven above, plus six Network
  members with zero qualifying reports across full enumeration — EU AI Office, Kenya, Canada,
  Australia, India, Germany. Rows stay in the ledger as documented zeros; the venues leave the
  active queue and the corpus denominator. **Roster 46 → 33.** ⚠ The paper can no longer claim to
  have swept every Network member — state the exclusion wherever coverage is described.
- **RAND filter** (`SEARCH_PROTOCOL.md` §2.2): RAND is a Forum member and cannot be retired, so its
  756 items pass a format gate (research output only) and a topic gate (title must name AI/LLM/
  model/agent/a frontier developer) before entering the queue. 756 → 359 in scope.
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

### 5.1 Multiple models, and evaluation series (added 2026-08-14)

**Separate models with different findings are separate entries.** Club only when the *same*
finding or threat is asserted about models **within one report and one company**; otherwise split.

| Situation | Rows |
|---|---|
| One report · one company · same finding across its models | **1** (club) |
| One report · **different companies** · same finding | **1 per company** — the company-split rule above always wins; two companies cannot respond as one thing |
| One report · genuinely different findings | 1 per finding |
| **Separate reports** — even same evaluator, same benchmark family, same threat | **1 per report** |

**Evaluation series and leaderboards.** A platform that publishes one page per model
(`weval.org/cards/<model>`) is publishing **separate reports**, not one report with many models —
each card is its own Report ID. Precedent in v10: `CIP-2025-08-OPUS41` and `CIP-2025-08-GPT5` are
distinct. The same holds for a leaderboard suite where each board is a distinct benchmark
(Scale AI's Humanity's Last Exam vs MASK vs SWE-Bench Pro vs PropensityBench): different
benchmarks are different findings by construction, not one threat repeated.

*Within* a single leaderboard, a ranking across many models is a **comparative ranking**, which
§4 condition (3) excludes from Tier A — such rows sit in Tier B/C.

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

**C1 = significant risk. C2 = low risk.** Use these names in prose; use C1/C2 in the data.
A finding is C1 if **any one** of the seven dangerous-capability domains D1–D7 is *demonstrated*,
and C2 otherwise. The two categories are exhaustive and mutually exclusive.

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

### §9 col 17 — scope of "directly addressed the identified problem" (added 2026-08-17)

Col 17 measures the **content** of the documented company response. It expressly does **not**
establish causation, and it lists *access restriction* among qualifying actions. Two consequences,
both settled by working through the 11 hardest rows in the corpus:

**1. A missing link to the finding is not grounds to downgrade Action Level.** Where a company acts
after a finding without referencing it or the evaluator, the action still counts; the silence is
recorded in col 18 as `No explicit attribution`. Downgrading col 17 as well would count the same
absence twice and would empty the very cell the 2026-08-15 Attribution revision was created to hold.
A bulk reclassification of 11 such rows to `None` was applied on 2026-08-17 and **withdrawn the same
day** for this reason. Motive is likewise outside col 17: OpenAI's fine-tuning wind-down states a
capability rather than a safety rationale, and still counts as an access restriction.

**2. Substantive vs Partial turns on whether the action reaches the model tested.** This is the
distinction that survived, and it is a col 17 question:

* **Substantive** — the action lands on the tested model, the tested surface, or the exact broken
  component. Examples: `CISCO-2024-07-JAI1` (Prompt Guard 2 is the successor to the very classifier
  the finding broke); `CIP-2025-08-ALI1` (same model, same behaviour, 68 days, 65–80% measured
  reduction); `SCALEAI-2024-10-JAI1` (a GPT-4o browser agent shipped with proactive refusals for the
  exact harmful-task class).
* **Partial** — the action addresses the identified problem class but reaches only **successor**
  systems, or removes the venue rather than the behaviour, or is expressly interim. Examples:
  `CAIS-2023-07-JAI1` (deliberative alignment on o-series, not the tested GPT-3.5/GPT-4);
  `SCALEAI-2025-02b-JAI3` (Safety Reasoner across successor systems); `APOLLO-2023-11-ALI1`
  (restricting stock trading removes the scenario, not the deception); `CAIS-2023-07-JAI3`
  (prototype, never deployed); the four `FARAI` fine-tuning rows (phased, and inference on existing
  fine-tuned models continues).

Attribution and response strength are **independent axes**. Of the 12 Tier A rows with
`No explicit attribution`, 11 are the rows above and 1 is `METR-2025-04-ALI1`, where Anthropic
documents the exact reward-hacking pattern and partial pre-launch mitigations while crediting its own
monitoring — `Partial` + `No explicit attribution`, undisturbed. Proportionality inputs are unchanged:
Severity × Action Level only.

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
| 17 | Action Level | 📊 | Tier A only. Records the **strength of the publicly documented company response** found through Channel A. **None** — no public response identifiable through the battery by the corpus cutoff. **Acknowledged** — the company recognised the finding or the underlying problem but specified no action. **Partial** — the company documented an action that addressed only part of the identified problem, or expressly described it as interim, limited or incomplete. **Substantive** — the company documented a specific mitigation, model change, safeguard, access restriction or deployment decision that directly addressed the identified problem. Action Level measures the **content** of the public response; it does **not** establish that the action was implemented or that it reduced the risk. Coherence: response fields filled ⇔ level ≠ None. |
| 18 | Attribution | 📊 | Tier A only, **assessed only where a company response exists**. **Explicit attribution** — the responding company directly referenced the finding, report, evaluation result or evaluating institution, or stated that its response was informed by that evidence. **No explicit attribution** — a qualifying response was identified but the company did not publicly state a connection to the finding. **No response located** — no response was identified through the Channel A battery (Action Level = None), so there is nothing to attribute. Attribution measures the company's **public explanation**; it does not independently establish causation. Coherence: Attribution = No response located ⇔ Action Level = None. |
| 19 | Company Response | 📋 | Concise factual clause from the company's own primary source. No URLs in text. |
| 20 | Channel A Verbatim | 🧾 | Character-exact quote of the response from the company source. |
| 21 | Response Date | 📊 | Actual date of the company source document. |
| 22 | Lag (days) | ⚙️ | = Response Date − Publication Date. Negative allowed (pre-deployment); 0 = coordinated disclosure. Exists ⇔ Response Date exists (⚠ 3 violations pending fix). |
| 23 | Channel A Evidence | 🧾 | Company primary-source URL. Exists ⇔ a response exists (⚠ 6 violations pending fix). |
| 24 | Sources Checked | 🧾 | The audit-trail cell, four uses: dated search logs behind None codings; negative-lag invalidation records; verification pointers behind confirmed responses; tier-assignment justifications. |
| 25 | Policy Level | 📊 | Tier A only. Records whether the finding received documented uptake through Channel B and whether that uptake created an **enforceable requirement**. **No policy uptake identified** — no official government, legislative or regulatory source explicitly referencing the finding, report, evaluation or specific result was found by the cutoff. **Non-binding policy uptake** — an official source explicitly cited or discussed the finding but created no enforceable obligation; includes official statements, legislative records, consultations, recommendations and guidance. **Binding policy action** — a law, regulation, regulatory order or other enforceable instrument explicitly referenced the finding and imposed a mandatory requirement. Official government sources only. Non-Tier-A rows may be blank. |
| 26 | Policy Response | 📋 | What the policy action was, from the official source. |
| 27 | Channel B Verbatim | 🧾 | Exact quote from the government source. |
| 28 | Channel B Evidence | 🧾 | Official government URL. |
| 29 | Media Outlets | 🧾 | Independent press coverage, each item with its URL. Powers the obscurity check. |
| 30 | Academic Citations | 🧾 | Verified citations/counts with sources (e.g. Semantic Scholar, dated). |
| 31 | Social Highlights | 🧾 | Notable public discussion, with links. Log only. |
| 32 | Channel C Verbatim | 🧾 | Quotes from third-party coverage. Log only. |
| 33 | Proportionality | ⚙️ | **Formula, no discretion, severity-dependent. Restated 2026-08-15; matrix unchanged from the 2026-08-03 revision.** Two inputs only — Severity and Action Level — on Tier A rows only. **C1 (significant risk)** + Substantive → Proportionate · C1 + Partial *or* Acknowledged → Under-response (gap) · C1 + None → Accountability gap (no action). **C2 (low risk)** + Substantive *or* Partial → Proportionate · C2 + Acknowledged → Under-response (gap) · C2 + None → Accountability gap (no action). Equivalently: **C1 needs a Substantive response to pass; C2 needs at least a Partial one.** Never hand-edited — `compute_proportionality.py` is the only writer. Computed on Channel A only; **policy uptake (Channel B) never substitutes**, and Attribution, Lag and Channel C do not enter the formula. No too-recent exception: those rows are excluded upstream at Action Trackable = no and never reach it. |
| 34 | Notes | 🧾 | Audit trail: `[CLUBBED …]` `[SPLIT …]` `[RECLASSIFIED …]` `[Report tested: …]`, caveats. |
| 35 | Key Quote | 🧾 | Short exact verbatim from the source report supporting the finding. Authoritative quote cell. |
| 36 | Traceability Tag | 📋 | Legacy column (mixed vocabulary, overlaps Finding Type). Retained; do not extend — new rows may leave blank. |
| 37 | Eval? (trackable) | 📊 | yes = empirical model finding; no = Tier C (§4). |
| 38 | Action Trackable? | 📊 | yes ⇔ full Tier A test (§4). Blank on Tier C rows. |
| 39 | Finding Type | 📊 | Nature (exactly one): `capability-finding` / `methodology` / `capability-trend` / `governance` + modifiers (0+): `anonymised-model`, `reassuring-null`, `company-self-report`, `too-recent`, `non-frontier`, `company-published`. ⚠ The `company-self-report` **modifier** is retained and is NOT the dropped Scope value — it marks a finding that is the company's own self-assessment *quoted inside an in-scope report by a named external evaluator* (8 rows in v10, e.g. `JOINT-2026-02-JAI2`, `USCAISI-2026-07-GOV2`). A finding needing this modifier still requires a named external evaluator to be in the sheet at all (§1 carve-out). |
| 40 | Scope | 📊 | `government-AISI` / `third-party-evaluator`. **Exactly two values** — `company-self-report` was removed as a Scope value on 2026-08-14 (§1: such reports are now a hard drop, ledger-only). Headline stats use government-AISI only. |

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
6. **Screening ledger** — sweep PARTIALLY complete (2026-08-01, halted by org spend limit).
   Authoritative artifact is `sweep_state/master_ledger.csv` (6,579 rows, of which 2,116 belong to
   retired venues and 4,463 are the active corpus). **597 rows unresolved; 86.6% resolved.**
   ⚠ **Enumeration is NOT complete, contrary to the earlier claim.** Two gaps found 2026-08-14:
   (a) 24 reports already in v10.csv were never enumerated at all — 4 UK AISI, 4 Holistic AI,
   5 Shanghai AI Lab, 2 CIP/Weval and others — so the venue enumerations have real misses;
   (b) 81 enumerated items had never been written to the ledger (SecureBio, CAIS, HAL, Korea
   worst) and have now been backfilled as `PENDING-FETCH`. Diagnose (a) before further screening:
   each miss reveals a class of enumeration failure, and re-enumeration may change the corpus base.
   **⚠ Reconciliation key is stale — fix before resuming.** `sweep_state/known_reports.json`
   holds 153 Report IDs but v10 has **211**; the 59 missing IDs made the dedup pass mislabel
   34 already-present reports as "genuinely new" (verified 2026-08-14). Rebuild the key from
   v10.csv and re-run the dedup before triaging. Post-correction counts: of the 58 flagged
   "genuinely new", 34 were already in v10 and 16 more are company self-reports now hard-dropped
   under §1 — leaving ~8 real third-party additions. Of the 139 INCLUDED-without-Report-ID rows,
   31 are already in v10, so ≤108 are true candidate misses.
   Enumerations for most remaining venues are cached in the
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

- **2026-08-15 · §9 cols 17, 18, 25 — definitions tightened for Action Level, Attribution and
  Policy Level.** Action Level and Policy Level are clarifications only: no coded value changes.
  Two real changes. (a) **Substantive no longer requires attribution** — the old wording said
  "specific, documented, *attributed* change", which double-counted attribution, an independent
  axis in col 18. Substantive now turns purely on whether a mitigation, model change, safeguard,
  access restriction or deployment decision is documented. (b) **Attribution is now assessed only
  where a response exists.** The old rule folded "no response" into *No explicit attribution*; a
  third value, **No response located**, now covers it, so the column stops conflating "the company said
  nothing" with "the company acted but did not say why". Applied to v11: 53 rows moved from
  *No explicit attribution* to *No response located*. New coherence invariant: Attribution = No response
  located ⇔ Action Level = None. v10's 80 rows on the old convention were migrated during the merge,
  so the column now means the same thing across both halves. **Label revised 2026-08-17:** the third
  value was originally worded *Not applicable*, which asserted that the attribution question did not
  apply; it now reads **No response located**, which states the fact — no response was found, so
  there is nothing to attribute. Meaning and invariant are unchanged; 126 cells were relabelled.
  Also records that both columns measure the *content of the public record*, not implementation,
  effectiveness or causation.
- **2026-08-15 · §7 and §9 col 33 — severity names fixed, Proportionality matrix restated.**
  C1 and C2 are now named in the rulebook as **significant risk** and **low risk**; previously they
  were defined only by the D1–D7 mechanism and had no plain-language label, which made the
  Proportionality rows hard to read. The matrix itself is **unchanged** — all eight cells verified
  identical to the 2026-08-03 revision and to the implementation in `compute_proportionality.py`,
  so no row's Proportionality value changes. Col 33 now also states explicitly what the formula
  does *not* depend on (Channel B policy uptake, Attribution, Lag, Channel C), because those were
  only implied before.
- **2026-08-15 · §1.1 added — the evaluation-vs-benchmark decision procedure.** Operationalises
  the §1 principle *who ran the evaluation and asserts the result*. Applied to all 67 v11 rows
  sourced from a developer domain; 65 resolved from source text. Three sub-rules made explicit:
  benchmark co-authorship confers neither contribution nor co-attribution (so a Gray Swan run of
  the UK-AISI-co-developed ART benchmark is Gray Swan's finding alone, and not `government-AISI`
  scope); unnamed "additional external partners" fails the named-evaluator test; a stated
  collaboration carries every named party. Thin-authorship ruled in (SLEIGHT-Bench, 4:1
  Anthropic:Redwood). Also adds the order-of-tests rule for rows that fail more than one check.
  **Effect on the v11 candidate set:** 603 → 568 active rows. 6 newly disqualified (2 Meta-run
  Agentic Misalignment rows misattributed to Apollo; 1 Anthropic-organised IPI competition;
  2 Mythos rows with unnamed evaluators; 1 Anthropic self-review of Irregular incidents);
  1 reinstated (`OPENAI-2025-04-SELF-CYB1`, retiered A→B); the 10-row Irregular / Signature
  Science roster hold cleared after source verification that both ran the evaluations;
  5 attributions and 2 finding texts corrected. All 35 removed rows retained on a `Removed`
  sheet in `v11_FINAL.xlsx`, each with its reason.
- **2026-08-14 · §5.1 added — multiple models and evaluation series.** Separate models with
  different findings are separate entries; club only within one report AND one company. The
  company-split rule always wins over clubbing. A platform publishing one page per model
  (weval.org/cards/<model>) publishes separate reports, one Report ID each — matching the existing
  v10 precedent (`CIP-2025-08-OPUS41`, `CIP-2025-08-GPT5`). A leaderboard suite of distinct
  benchmarks is likewise separate reports; rankings *within* a board are comparative and excluded
  from Tier A by §4(3).
- **2026-08-14 · §7.3 clarified — the test is evaluator independence, not whose model was
  evaluated.** The four model developers can never satisfy the named-evaluator test for one
  another, so a developer publishing alone is out of scope even when evaluating a competitor's
  model, and a cross-developer exercise is not an independent evaluation. Facilitation is not
  contribution. One row corrected (`Findings from a Pilot Anthropic-OpenAI Alignment Evaluation
  Exercise`, previously included).
- **2026-08-14 · Roster corrections A/B/C applied; 46 → 33 organisations.**
  **(A)** Seven orgs retired as `EXCLUDED - not a roster org` — Ai2, UC Berkeley, Thorn, EPFL, Yale,
  Stanford, Oxford — added to the roster by parsing one joint Institution string
  (`UKAISI-2025-11a`) as seven evaluators. 1,405 enumerated / 1,400 screened rows / **0 inclusions**;
  the rule was also applied inconsistently (CMU, in the same kind of string, was never added).
  **(B)** Six zero-yield Network members retired as `EXCLUDED - venue retired` — EU AI Office,
  Kenya, Canada, Australia, India, Germany (896 enumerated, 0 inclusions).
  **(C)** RAND format + topic gates (`EXCLUDED - out-of-scope format` 253, `EXCLUDED - off-topic` 144);
  756 → 359 in scope. Plus 81 enumerated-but-never-ledgered items backfilled as `PENDING-FETCH`
  (58 further candidates rejected as URL-variant duplicates of existing rows).
  **Net:** active corpus 6,498 → **4,463**; unresolved 657 → **597**; `INCLUDED` unchanged at 219 —
  no row that ever qualified was touched. Every retired row is retained in the ledger, so the
  PRISMA exclusion counts remain reconstructable. Grandfathering rule tightened to publisher-only.
- **2026-08-14 · Company self-reports moved from "kept, stratified" to HARD DROP (§1, §9 row 40).**
  A model developer's report on its own model(s) with **no external evaluator named** is now out
  of scope entirely — ledger-only, decision `EXCLUDED - company self-report`. `Scope` drops to two
  values (`government-AISI` / `third-party-evaluator`); the third value was defined in v10 but
  **never populated** (0 of 456 rows), so this codifies existing practice and changes no existing
  row, no stratified table, and no headline number. The `company-self-report` *Finding Type
  modifier* is deliberately RETAINED and now explicitly disambiguated (§9 row 39) — 8 v10 rows use
  it for a company self-assessment quoted inside an in-scope external-evaluator report. §1 gains a
  load-bearing carve-out preserving the 16 v10 rows sourced from company-published documents via a
  named evaluator's section (`JOINT-2026-07-*`, `*-SELF`, `JOINT-2025-05-ALI2..5`). Screening test
  on company venues narrows from "does it contain a finding?" to "is an external evaluator named?"
  `SEARCH_PROTOCOL.md` §2/§4 updated to match; sweep artifacts re-decided (rows retained for PRISMA).
- **2026-08-03 · Header cutoff date corrected back to 2026-07-30.** The 2026-08-03 "stale
  headline counts" fix below wrongly changed this to "31 Jul 2026" by reading the max
  Publication Date actually present in the sheet, rather than the frozen corpus cutoff
  already defined in §2 (2026-07-30). One row, `DREADNODE-2026-07-CYB2`, carries a Publication
  Date one day past that cutoff; that's a data note, not a reason to move the cutoff itself.
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
