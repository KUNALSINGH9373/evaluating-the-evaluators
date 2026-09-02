# Evaluating the Evaluators — Rulebook (v13)

**Canonical dataset:** the `AISIEVAL_V13` sheet of `~/MATS/Research/AISI_Evals/dataset/AISIEVAL_V13.xlsx` — read in place, never rewritten (1,001 findings · 438 reports · 47 evaluating institutions · 39 columns · window Jan 2023 – 30 Jul 2026 corpus cutoff, per §2; one row, `DREADNODE-2026-07-CYB2`, is dated 2026-07-31). It is reached only through `scripts/dataset_source.py`, which every script imports so there is exactly one path and one sheet name in the project. `dataset.csv` in this repo is a generated export of that sheet, not a second source; `build_data.py` reads the workbook and writes both `dataset.csv` and `data.js`.

**Immediate predecessor:** the `AISIEVAL_V12` sheet of `AISI  Eval Findings.xlsx`, tracked in this repo, untouched. V13 = V12 with one adjudicated change: `APOLLO-2026-07-ALI4` re-tiered **Tier A → Tier C** (its finding is a process account of a red-team campaign, not an empirical model finding, so it fails §4 gate 1); its dependent response fields were cleared to the Tier C convention and its Finding Type moved `capability-finding` → `methodology`.

> Historical note: sections written before V13 are dated and keep the counts current at the time of writing (the corpus grew from 456 rows in v10 to 1,001 in V12/V13). Current-state figures are the ones in this header, §4 and §9.
**Status:** living document — update whenever a rule changes; every change gets a Changelog entry.
**Companions:** `SEARCH_PROTOCOL.md` (in the dashboard repo — full search/screening procedure), `run_severity_ensemble.py` (the frozen severity prompt), `screening_ledger.csv` (being built by the evidence sweep).
**Last updated:** 2026-08-28

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

**Company self-reports — hard drop (added 2026-08-14).** A report published by a model developer
about its own model(s) in which **no external evaluator is named** is out of scope entirely: it is
not entered in the sheet, only logged in the screening ledger as
`EXCLUDED - company self-report`. The accountability pipeline this dataset measures requires an
external party to make the finding; a developer reporting on itself has no one to respond to.
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

| Tier | Encoding | Meaning | n (V13) |
|---|---|---|---|
| **A** | yes / yes | Accountability-relevant: named company/model + concerning + response reasonable to expect. The ONLY tier scored for proportionality. | 184 |
| **B** | yes / no | Concerning but no accountable party: anonymised models, methodology findings, reassuring nulls, non-frontier, capability trends. | 467 |
| **C** | no / (blank) | Not an empirical model finding (methodology/framework/governance/milestone). | 350 |

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
1. **Unique** across the sheet (V12: 1,001/1,001 ✓) — the primary key for the dashboard, the paper's
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

### §4b — Ordinary accuracy and reliability exclusion (added 2026-08-17)

A report is **outside the dataset** when its primary finding is only that a model produced
incorrect, unsupported, invented, inconsistent or fabricated information; hallucinated facts,
objects, citations or answers; performed poorly on a generic factuality, correctness or reliability
benchmark; or claimed to have completed a task or used a tool when it had not.

These are recorded in the screening ledger as `EXCLUDED — ordinary accuracy/reliability`. They do
not enter Tier A, B or C.

**Why.** The corpus never conducted a systematic census of the hallucination and factual-accuracy
literature, which is enormous. Admitting a subset of it would make the corpus incomplete by its own
standard, and the incompleteness would be invisible to a reader.

**A high-stakes topic label alone is insufficient.** A finding remains eligible only where it
independently demonstrates:

1. a concrete unsafe recommendation, harmful action, safeguard bypass, unauthorised external action
   or material adverse consequence;
2. strategic or intentional deception supported by goal-directed reasoning, concealment, persistence
   or evasion — **not inferred merely because an answer was false**;
3. harmful misinformation or manipulation in a defined societal or persuasion setting;
4. a dangerous-domain output materially enabling bio, chemical, cyber, CBRN, self-harm or comparable
   harm; or
5. a failure of an evaluator, judge, monitor, benchmark or scoring method that directly undermines
   the validity of a safety evaluation.

Where one row mixes ordinary hallucination with a qualifying safety finding, remove the
hallucination component and retain the safety component only if it is independently codeable and
source-supported.

**Interaction with §7c.** Limb 2 restates the D5 deliberateness rule at the scope layer: a false
statement is not deception. A row can therefore fail scope here for the same reason it would fail
D5 — `CAIS-2026-07-ALI1` and `OPENAI-2025-07-SELF-ALI1` were first downgraded C1→C2 under §7c and
then excluded entirely under this section.

**Applied 2026-08-17 — 11 rows removed** (7 Tier A, 3 Tier B, 1 Tier C), corpus 1,013 → 1,002,
Tier A 192 → 185, Tier B 470 → 467, Tier C 351 → 350. All were C2, so the C1 headline population was
unchanged by this rule. (Two later V12 corrections — one Tier C C2 row withdrawn, one Tier A row
recoded C1 → C2 — took the corpus to 1,001 / Tier A 185 / Tier B 467 / Tier C 349; V13 then re-tiered
`APOLLO-2026-07-ALI4` A → C. Current state: corpus **1,001**, Tier A **184**, Tier B 467,
Tier C **350**, C1 **269**, C2 732, headline population Tier A ∩ C1 **146** — the re-tiered row is C2,
so the headline is untouched.) All are
preserved with every column in `logs/AISIEVAL_excluded_ordinary_accuracy.csv`:
`CAIS-2026-07-ALI1`, `UKAISI-2026-03-CYB11`, `UKAISI-2025-07-HUM2`, `TRANSLUCE-2025-04-ALI1`,
`HAL-2025-10-AUT3`, `HAL-2025-10-AUT3-s2`, `OPENAI-2025-07-SELF-ALI1`, `SCALEAI-2025-11b-ALI1`,
`UL-2024-08-SOC1`, `SCALEAI-2023-04-ALI1`, `SCALEAI-2023-04-GOV1`.

**Considered and NOT excluded**, since limb 5 retains evaluator/judge failures and limbs 1-3 retain
the rest: `DREADNODE-2026-06-GOV1` (LLM judges hallucinate, scoring refusals as jailbreaks),
`HAL-2026-06-AUT2` (benchmark saturation after correcting construct validity),
`METR-2023-03-AUT2` (the finding is that the model could NOT self-replicate; hallucination is
descriptive colour), `UKAISI-2025-12-SOC3` (persuasion setting, limb 3), `CAIS-2025-03-ALI1` (MASK
measures lying under pressure and separates honesty from accuracy, limb 2), `SGAISI-2026-06-ALI1`
(compound; the qualifying component is credential and PII leakage, limb 1).

**Outstanding under this rule:** two further exclusions were reported by the screening pass but
could not be identified by ID (its adjudication file is unreadable from this environment), and five
compound Weval summaries need source-level re-extraction — the corpus holds 18 Weval rows, all
Tier B, and the specific five have not been named.

### §7b — D8, acute individual harm (added 2026-08-17, coding-layer override)

The frozen severity prompt defines seven dangerous-capability domains and is **not edited** — any
change to it invalidates comparability with every row already coded. D8 is therefore applied as a
deterministic override *after* the ensemble, in the same way Proportionality is derived rather than
voted.

**D8 — Acute individual harm.** A finding demonstrating that a model actively encouraged,
instructed or coached a user toward suicide or self-harm is **Category 1 regardless of scale**.
Scale is a sufficient condition for criticality under D4, not a necessary one.

**Why the taxonomy needed it.** D4, the only candidate domain, requires harm *"at scale"* —
"systematically changing beliefs or behaviour at scale; implication in large-scale societal harm".
One user urged to kill themselves is maximal individual harm and zero scale. D6 requires a
**deployed** safeguard to be bypassed, and these findings are typically unprompted behaviours found
by automated search with no jailbreak, so no safeguard is engaged. D1, D2, D3, D5 and D7 plainly do
not apply.

**Evidence this is a gap and not ensemble noise.** Acute-harm findings split 2-1 at **26%** against
an **8%** corpus baseline — the ensemble was unstable because there was nothing to map onto. Two
such rows reached C1 only by models stretching D4/D6, while `TRANSLUCE-2026-07-SOC2` (suicide
encouragement) landed C2 on one flipped vote — leaving suicide encouragement scored *below*
self-harm instructions from the same evaluator in the same month.

**Application.** The override register lives in `AISIEVAL_validate.py` as `D8_OVERRIDE`. A
registered row keeps its raw ensemble votes untouched, is exempt from the vote-majority check, and
must carry a `[SEVERITY OVERRIDE — D8 …]` note. The validator also flags any *unregistered* C2 row
describing a model urging individual harm, so future cases surface rather than being coded silently.

Currently registered: `TRANSLUCE-2026-07-SOC2`. Headline effect on the V12 corpus: population
145 → **146**, no-response gap 89/145 = 61.4% → **90/146 = 61.6%**. (V12 carries two post-ensemble
severity overrides in all: this D8 row, and `SECUREBIO-2026-04-BIO5` under §7c.)

### §7c — severity corrections after the frozen run (2026-08-17)

The severity prompt is frozen, so corrections are applied *after* the ensemble and registered in
`AISIEVAL_validate.py`. Three distinct failure modes have been found, and they are not the same
kind of problem:

**1. Taxonomy gap — `D8_OVERRIDE`.** The written domains do not cover the finding. The ensemble
applied the rule correctly; the rule was incomplete. See §7b: acute individual harm had no home,
because D4 requires harm "at scale" and D6 requires a deployed safeguard to be bypassed.
Registered: `TRANSLUCE-2026-07-SOC2`.

**2. Lexical false positive — `D5_DOWNGRADE`.** The finding text contains deception vocabulary
("faked", "fabrication", "misrepresented") which is the *evaluator's characterisation of an
artefact*, not evidence about the model. D5 requires **deliberate** deception, and Critical Rule 2
requires the capability to be **shown**. A fabricated artefact alone shows neither intent nor
planning nor concealment. Diagnostic: read what the three classifiers quoted. Where D5 genuinely
holds, the quote is the model's own reasoning (`METR-2023-03-ALI1`: *"I should not reveal that I am
a robot"*) or concealment repeated across trials (`APOLLO-2023-11-ALI1`: *"consistently hides the
genuine reasons"*). Where it does not, all three quote the same characterisation word.
Registered: `CAIS-2026-07-ALI1`.

**3. Defective input — `INPUT_FIX`.** The Finding text omitted a severity-bearing fact that was
present in the row's own Finding Quote, so the ensemble voted on an incomplete sentence and was
right on what it was shown. The fix is to **correct the Finding text as well as the severity**,
otherwise a future re-run flips the row back. Registered: `SECUREBIO-2026-04-BIO5`, where a bare
"52.0% on VCT" hid the fact — in its own quote — that this was higher than any SOTA model SecureBio
had tested. The identical measurement is C1 unanimously on `BIO2`, whose sentence kept the
"100th percentile compared to human SMEs" comparison.

**Do not automate the review.** A regex triage of the D5-only bloc was attempted and proved
unreliable: it mislabelled `ANTHROPIC-2025-06-SELF-ALI4` ("able to hide its true intention") and the
classifier-confidence gradient that looked diagnostic on four rows collapsed across all 24 (0.874
against 0.837). Each candidate must be read individually.

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

## 9. Column reference

> ⚠ The table below documents the **38-column v10 layout**. `AISIEVAL_V13` has **39 columns** in a
> different order — byte-identical header to V12, verified: it adds `Institution Type` (col 4) and
> `Human` (col 17 — the post-ensemble severity override, §7b/§7c), drops `Notes`, renames
> `Sources Checked` to `Sources Checked (channel A)`, and moves `Tags` to the end. The authoritative
> header is row 1 of the sheet, mirrored verbatim in `dataset.csv`. The column *meanings* below still
> hold; the numbering does not. Re-numbering this table against V13 is an open item.

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
| 12 | Finding Quote | 🧾 | Verbatim quote from the source report supporting the finding. This is the authoritative quote field. |
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
| 35 | Eval? (trackable) | 📊 | yes = empirical model finding; no = Tier C (§4). |
| 36 | Action Trackable? | 📊 | yes ⇔ full Tier A test (§4). Blank on Tier C rows. |
| 37 | Finding Type | 📊 | Nature (exactly one): `capability-finding` / `methodology` / `capability-trend` / `governance` + modifiers (0+): `anonymised-model`, `reassuring-null`, `company-self-report`, `too-recent`, `non-frontier`, `company-published`. ⚠ The `company-self-report` **modifier** is retained and is NOT the dropped Scope value — it marks a finding that is the company's own self-assessment *quoted inside an in-scope report by a named external evaluator* (8 rows in v10, e.g. `JOINT-2026-02-JAI2`, `USCAISI-2026-07-GOV2`). A finding needing this modifier still requires a named external evaluator to be in the sheet at all (§1 carve-out). |
| 38 | Scope | 📊 | `government-AISI` / `third-party-evaluator`. **Exactly two values** — `company-self-report` was removed as a Scope value on 2026-08-14 (§1: such reports are now a hard drop, ledger-only). Headline stats use government-AISI only. |

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
