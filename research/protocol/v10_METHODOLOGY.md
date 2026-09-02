# Evaluating the Evaluators — Full Methodology (Dataset v10)

> **This document describes the v10 build (456 findings, 2026-07-30 cutoff) and is kept as the
> historical record of how that corpus was constructed. It is not the current dataset.** The live
> corpus is `dataset/AISIEVAL_V13.xlsx`, sheet `AISIEVAL_V13`, read only through
> `scripts/dataset_source.py`: **1,169 findings · 484 reports · 47 institutions · 39 columns ·
> window 2020-05-29 – 2026-08-27 · Tier A 231 · B 607 · C 331 · headline 113/188 = 60.1%.**
> Counts in the body below are v10-era and are correct only for that snapshot.

**Dataset this document describes:** `v10.csv` — 456 findings · 211 reports · 40 columns *(superseded)*
**Corpus window described here:** each organisation's first publication → **2026-07-30** (the v10 frozen cutoff; the live corpus now runs to 2026-08-29)
**Screening ledger:** `sweep_state/master_ledger.csv` — 6,579 rows; **active corpus 4,463** after the
2026-08-14 roster corrections (2,116 rows belong to retired venues and are retained as documented zeros)
**Document status:** consolidated reference. Supersedes nothing — it merges `v10_RULEBOOK.md`
(the normative rules), `SEARCH_PROTOCOL.md` (the search/screening SOP) and
`run_severity_ensemble.py` (the frozen severity prompt) into one narrative, and adds the
observed funnel numbers. **Where this document and the rulebook disagree, the rulebook wins.**
**Last updated:** 2026-08-14

---

## 0. What the dataset measures

The dataset measures the **public-channel accountability pipeline**:

> When a government AI Safety Institute (or comparable evaluator) publishes a finding about a
> specific model or company, does a documented response follow?

Every design decision below follows from that question. The unit of analysis is the **finding**,
not the report and not the organisation, because a response is owed to a claim, not to a PDF.

### 0.1 A structural note on ordering

The dataset was built **before** the census. v9 → v10 was assembled by targeted research; the
6,712-item sweep is a **retrospective completeness audit** run in August 2026 to demonstrate that
nothing qualifying was missed. This is why reconciliation (§10) runs in *both* directions: every
Report ID already in the sheet must reappear as `INCLUDED`, and every `INCLUDED` item absent from
the sheet is a candidate miss. The ledger is evidence of recall, not the source of the dataset.

### 0.2 Canonical artifacts

| Artifact | Role |
|---|---|
| `v10.csv` | The v10 dataset, 456 findings × 40 columns. **Superseded** — the live dataset is `dataset/AISIEVAL_V13.xlsx` |
| `v10_RULEBOOK.md` | Normative rules. Living document; every change gets a changelog entry |
| `SEARCH_PROTOCOL.md` | Search & screening SOP (Step 1) |
| `run_severity_ensemble.py` | The frozen severity prompt + 3-model runner |
| `sweep_state/master_ledger.csv` | The screening ledger — one decision per enumerated item |
| `sweep_state/cached_enumerations.json` | All 6,712 enumerated items, by venue |
| `sweep_state/known_reports.json` | Reconciliation key. **Must be rebuilt from `v10.csv` each sweep** |
| `sweep_state/company_self_reports_excluded.json` | Audit trail for the §7.3 hard drop |

---

## 1. The pipeline at a glance

```
STAGE 0   Roster derivation ................ 33 active organisations (derived, never hand-picked)
STAGE 1   Enumeration ...................... 6,712 items enumerated → 4,463 in the active corpus
STAGE 2   Screening ........................ 4,463 active rows → 219 INCLUDED · 597 unresolved
STAGE 3   Finding extraction ............... 211 reports → 456 findings (split & club)
STAGE 4   Identity assignment .............. Finding ID (unique, immutable) + Report ID
STAGE 5   Severity coding .................. 3-model ensemble, majority vote → C1 / C2
STAGE 6   Tier assignment .................. A=111 · B=240 · C=105
STAGE 7   Scope assignment ................. government-AISI=291 · third-party=165
STAGE 8   Response search (Tier A only) .... Channel A / B / C fixed batteries
STAGE 9   Proportionality .................. derived by formula, no discretion
STAGE 10  Reconciliation ................... bidirectional; gaps re-swept
```

**The governing design decision:** *enumerate exhaustively and exclude explicitly, rather than
search selectively.* Every one of the 6,579 ledger rows carries exactly one decision and a
one-line reason, so the PRISMA diagram for the paper is a database query rather than a
reconstruction.

---

## 2. Stage 0 — Roster derivation (who gets searched)

**Rule: the roster is derived, never hand-picked.** This is Stage 0 of *every* sweep, and the
derivation is logged with its date. It is the anti-cherry-picking guarantee: membership comes
from external authorities, not from the researcher's judgement.

Three sources, plus company artifacts:

1. **Government institutes** = the current membership of the **International Network of AI Safety
   Institutes** — as of last check: UK, US, Japan, Singapore, Korea, France, EU AI Office, Canada,
   Australia, **Kenya** — plus any newly announced national institute (verified at sweep time).
2. **Third-party evaluators** = current membership of the **AI Evaluators Forum**, plus every
   evaluator organisation already present in the dataset: METR, Apollo Research, SecureBio,
   Transluce, Holistic AI, Princeton HAL, Shanghai AI Lab, LatticeFlow, Robust Intelligence/Cisco,
   UL DSRI, Scale AI, CIP/Weval, Palisade, Dreadnode, FAR.AI, RAND, Redwood, CAIS, Citadel AI,
   Tsinghua CoAI, AVERI.
3. **Grandfathered orgs** — any organisation already in the dataset that appears on neither list
   stays on the roster **permanently**.
4. **Company release artifacts** — OpenAI (incl. `deploymentsafety.openai.com`), Anthropic,
   Google DeepMind, Meta. Swept under the narrowed test of §7.3.

**→ 46 organisations derived; 33 active after the 2026-08-14 retirements (§2.2).**

**Zero-yield organisations are swept anyway and logged as zeros.** "We enumerated Germany AISI and
found 0 items" is itself a census result and must appear in the ledger. Members with no rows in
the sheet (EU AI Office, Canada, Kenya) are swept on the same terms as UK AISI.

### 2.1 Roster discoveries banked 2026-08-01 (act on in the paper)

- The Network was **renamed** (Dec 2025) to *"International Network for Advanced AI Measurement,
  Evaluation and Science"* — update §2.1 terminology throughout the paper.
- **AI Evaluator Forum** founding members (Dec 2025): Transluce, METR, RAND, Princeton HAL,
  SecureBio, CIP, Meridian Labs, AVERI.
- **Germany AISI** approved 2026-06-09 (pre-launch, 0 items). **IndiaAI Safety Institute** has
  existed since Jan 2025. **Kenya** is a network member; its ministry site is nearly all PR with
  near-zero evaluations.
- **Meridian Labs** and **Gray Swan** are roster organisations with no dataset presence yet.

### 2.2 Roster corrections and retirements (2026-08-14)

**Grandfathering attaches to the PUBLISHER, never to a co-author.** An organisation named inside a
joint `Institution` string is not thereby a roster org — the report is already captured under
whoever published it.

> **The failure this fixes.** The single string
> `"UK AISI; University of Oxford; EPFL; Yale; UC Berkeley; Stanford; Allen Institute for AI"` on
> `UKAISI-2025-11a` placed six universities on the roster as standalone venues; `"UK AISI + Thorn"`
> added a seventh. Together: **1,405 enumerated items, 1,400 screened rows, 0 inclusions.** The rule
> was also applied inconsistently — CMU appears in `"Gray Swan AI, with Center for AI Safety, CMU,
> EPFL"` and was never added.

| Retired | Basis | Enumerated | Included |
|---|---|---:|---:|
| Ai2, UC Berkeley, Thorn, EPFL, Yale, Stanford, Oxford | Co-author affiliation only, never a publisher | 1,405 | 0 |
| EU AI Office, Kenya, Canada, Australia, India, Germany | Network members with zero qualifying reports; retired by explicit scope decision | 896 | 0 |

**Roster 46 → 33 active organisations.** Retired venues keep their ledger rows — the zero stays
documented and the PRISMA counts stay reconstructable — but leave the active queue and the corpus
denominator.

> ⚠ **Cost of the second retirement, to be stated in the paper.** Dropping Network members means
> the dataset can no longer claim to have swept *every* member of the International Network. This
> must be disclosed wherever coverage is described.

### 2.3 The RAND filter

RAND is an AI Evaluators Forum member and therefore cannot be retired, but it publishes ~756 items
in the window, the overwhelming majority unrelated to AI evaluation. Two gates apply before an item
enters the queue:

1. **Format gate** → `EXCLUDED - out-of-scope format`. Drops `/pubs/commentary`,
   `/pubs/testimonies`, `/pubs/podcasts`, `/pubs/presentations`, `/pubs/visualizations`,
   `/pubs/corporate_pubs`, `/pubs/commercial_books`, `/pubs/rgs_dissertations`, `/multimedia/`,
   `/news/`, `/events/`. Research output only. **253 dropped.**
2. **Topic gate** → `EXCLUDED - off-topic`. The title must carry at least one of: AI · AGI ·
   artificial (general) intelligence · superintelligence · LLM · large language model · machine
   learning · model(s) · agent(s)/agentic · chatbot · generative · foundation/frontier model ·
   neural · algorithmic · autonomous · deepfake · red-team · jailbreak · benchmark · fine-tuning ·
   alignment · compute · or a frontier-developer name. **144 dropped.**

**RAND 756 → 359 in scope.** Verified in both directions: the filter drops "Unlocking the Tax Code
with RAND's Tax Code Analysis Tool" and keeps "A Structured Approach to Identifying and
Characterizing AI Vulnerabilities".

---

## 3. Stage 1 — Enumeration (how 6,712 items appeared)

This stage is **not a search. It is an exhaustive listing.**

### 3.1 What counts as a venue

A **venue** is any publication surface of an in-scope organisation — primarily the org's **own
website** (research / blog / publications index pages, **paginated to the very end**, with a
sitemap fallback). Company release artifacts and arXiv are supplements, never the primary surface.

### 3.2 The arXiv rule

arXiv is reached **only** via each roster organisation's own publication list and by
**citation-chasing** from already-included reports — **never by open keyword search.** A keyword
search is unreproducible and its recall is unknowable; a publication index is neither.

### 3.3 Window

Each venue's first publication → **2026-07-30**, the frozen corpus cutoff. Qualifying items after
the cutoff are logged `POST-CUTOFF` (ledger only, not corpus) so the next dataset version ingests
them rather than re-discovering them.

### 3.4 Why the number is 6,712 and not 300

Because listing everything an organisation ever published — rather than searching for likely
hits — is the only way to make recall auditable. Most of what is enumerated is knowingly
irrelevant, and that is the point.

| Venue | Items | Venue | Items |
|---|---:|---|---:|
| RAND Corporation | 756 | Redwood Research | 137 |
| Kenya Ministry of ICT | 628 | OpenAI | 124 |
| Allen Institute for AI (Ai2) | 548 | FAR.AI | 116 |
| Holistic AI | 427 | Korea AISI (K-AISI) | 106 |
| Google DeepMind | 355 | Japan AISI (J-AISI) | 100 |
| Scale AI | 309 | METR | 90 |
| Anthropic | 284 | UL DSRI | 89 |
| UC Berkeley | 273 | Citadel AI | 86 |
| Thorn | 270 | SecureBio | 79 |
| Cisco (Robust Intelligence) | 256 | Yale University | 71 |
| Tsinghua CoAI | 230 | Stanford University | 65 |
| EU AI Office | 182 | Shanghai AI Lab (AI45) | 59 |
| EPFL | 155 | CIP (Weval) | 57 |
| Center for AI Safety (CAIS) | 155 | Apollo Research | 57 |
| UK AISI | 152 | Gray Swan AI | 54 |
| France INESIA | 54 | LatticeFlow AI | 49 |
| Canada AISI | 46 | US CAISI (NIST) | 42 |
| Dreadnode | 41 | Meta | 38 |
| Princeton HAL | 28 | IndiaAI Safety Institute | 28 |
| Transluce | 27 | University of Oxford | 23 |
| Palisade Research | 22 | Singapore AISI | 18 |
| Australian AISI | 12 | Meridian Labs | 7 |
| AVERI | 7 | Germany AISI (pre-launch) | 0 |

**Total: 6,712 items across 46 venues** — 4,463 of them in the active corpus after the roster
corrections in §2.2.

> ⚠ **Enumeration is NOT complete.** The earlier "COMPLETE" claim is withdrawn (2026-08-14).
> **24 reports already in `v10.csv` were never enumerated at all** — 4 UK AISI, 4 Holistic AI,
> 5 Shanghai AI Lab, 2 CIP/Weval and others. UK AISI is recorded as fully screened with 152 items
> enumerated, yet four of its own reports in the dataset never appeared. A further 81 enumerated
> items had never been written to the ledger and have since been backfilled. Diagnose the 24
> before further screening: each reveals a *class* of enumeration failure, and re-enumeration may
> change the corpus base.

---

## 4. Stage 2 — Screening (6,712 → 219 included)

**Every enumerated item receives exactly one decision and a one-line reason**, written to the
ledger. No item is silently dropped.

### 4.1 The decision vocabulary

| Decision | Meaning |
|---|---|
| `INCLUDED` | Contains ≥1 qualifying finding (§5) by an in-scope, **named** evaluator |
| `EXCLUDED - not an evaluation` | Announcement, product post, PR, opinion piece, plan. Resolved by **title triage**, no fetch |
| `EXCLUDED - no findings` | Fetched, but contains only promises, recommendations, or methodology intentions |
| `EXCLUDED - no named evaluator` | "External evaluators" / "specialist groups" with no agency named (hard drop) |
| `EXCLUDED - company self-report` | Model developer's report on its own model(s) with no external evaluator named (hard drop; added 2026-08-14, §7.3) |
| `EXCLUDED - non-English` | Non-English-only output |
| `EXCLUDED - out-of-scope org` | Publisher not on the roster and no roster co-author |
| `EXCLUDED - duplicate/secondary` | Restates findings whose primary source is already `INCLUDED` (§4.3) |
| `POST-CUTOFF` | Qualifying but published after 2026-07-30 |
| `EXCLUDED - not a roster org` | Venue was on the roster only via a co-author affiliation, never as a publisher (§2.2) |
| `EXCLUDED - venue retired` | Venue retired by scope decision; rows kept as a documented zero (§2.2) |
| `EXCLUDED - out-of-scope format` | Non-research publication format (§2.3 format gate) |
| `EXCLUDED - off-topic` | No AI / LLM / model / agent / developer term in the title (§2.3 topic gate) |

Two **operational, non-terminal** states also appear:

| State | Meaning |
|---|---|
| `PENDING-FETCH` | Eval-candidate awaiting full-text screening |
| `PENDING-EVALUATOR-CHECK` | Company-venue item awaiting the §7.3 narrowed test only — one question, no finding extraction |

### 4.2 Title triage: what makes the census affordable

4,894 of 6,712 items are resolved to `EXCLUDED - not an evaluation` **from the title alone, at
zero fetch cost.** This is the single economic decision that makes an exhaustive census possible;
without it the sweep would require ~6,700 full-text fetches instead of ~1,300.

### 4.3 Dedup rule

**The primary — earliest, fullest — source wins.** Progress reports and annual summaries are
`EXCLUDED - duplicate/secondary` **unless** they contain a finding published nowhere else, in
which case only that finding enters, with the summary as its source.

Dedup across venues collapsed 6,712 enumerated items into 6,498 ledger rows (214 collapsed).

### 4.4 Ledger schema

`venue, item_title, url, publication_date, decision, reason (1 line), report_id (if INCLUDED),
sweep_date, sweeper`

### 4.5 Evidence standard for the ledger itself

Item lists come from the venue's own publication index, paginated fully. URLs recorded as found;
an archive (web.archive.org) capture is requested for every `INCLUDED` item.

### 4.6 Current ledger state (2026-08-14, post roster correction)

**Active corpus — 4,463 rows.** These are the numbers the PRISMA diagram is built from.

| Decision | Count |
|---|---:|
| `EXCLUDED - not an evaluation` | 2,601 |
| `EXCLUDED - no findings` | 523 |
| `PENDING-FETCH` | 364 |
| `EXCLUDED - out-of-scope format` | 253 |
| `PENDING-EVALUATOR-CHECK` | 233 |
| `INCLUDED` | 219 |
| `EXCLUDED - off-topic` | 144 |
| `EXCLUDED - duplicate/secondary` | 79 |
| `POST-CUTOFF` | 16 |
| `EXCLUDED - no named evaluator` | 15 |
| `EXCLUDED - out-of-scope org` | 15 |
| `EXCLUDED - company self-report` | 1 |
| **Active total** | **4,463** |

**Retained but out of corpus — 2,116 rows** (`EXCLUDED - not a roster org` 1,400 ·
`EXCLUDED - venue retired` 716). Ledger file total: **6,579 rows.**

**597 rows remain unresolved** — 364 pending fetch + 233 pending the company evaluator check.
**86.6% of the active corpus is resolved.**

## 5. Stage 3 — What qualifies as a FINDING

A **finding** is a discrete, evidence-backed claim asserted by an in-scope evaluator in a public
report, codeable independently of the report's other claims. **All three tests must hold:**

1. **Asserted by the evaluator** — not a summary of someone else's work; not a comparator score
   cited in passing (comparators → `Notes` as `[Report tested: …]`).
2. **Evidence-backed in that report** — a measured result, an observed behaviour, or a documented
   process fact. **Opinions, recommendations, and forward-looking plans are not findings.**
3. **Independently codeable** — it would warrant its own response (the club test, §6).

### 5.1 Three kinds qualify

- **Empirical model findings** — a specific system's capability, behaviour, or safeguard,
  **including reassuring nulls**
- **Methodology / tooling findings**
- **Governance / process findings**

Announcements, partnership news, opinion pieces, and plans contain **no** findings.

---

## 6. Stage 3b — One finding per row: split & club

- **Different companies never share a row.**
- **Club** findings that warrant the *same* response. Decisive test: *did (or would) the company
  respond to them as one thing?* Example: four Constitutional-Classifiers bypasses → one
  restructuring → **one row**.
- **Split** findings that warrant *distinct* responses — capability vs safeguard-failure, or
  different domains of the same model.
- **Comparators and baselines are never rows** → `Notes: [Report tested: …]`.
- On a split, part 1 keeps the base Finding ID; parts 2+ take `-s2`, `-s3` suffixes. **Both remain
  live rows.**

**→ 211 reports produce 456 findings.**

---

## 7. Stage 7 — Scope (stated here because it gates ingestion)

### 7.1 In scope, headline stats — `Scope = government-AISI` (291 rows)

UK AISI, US CAISI/NIST, and the national AISIs affiliated via the International Network (Japan,
Singapore, Korea, France PEReN/INESIA, EU AI Office, Canada, Australia, Kenya) — **and any joint
exercise that includes a government AISI, even with a non-government co-author.**

### 7.2 Kept, stratified, excluded from headline stats — `Scope = third-party-evaluator` (165 rows)

No government co-author (e.g. METR alone).

`Scope` has **exactly two values.** A third, `company-self-report`, was defined in v10 but never
populated (0 of 456 rows) and was removed on 2026-08-14.

### 7.3 Hard drop — not in the sheet, logged in the ledger

- Reports naming **no evaluating agency at all** ("external evaluators", "specialist groups")
- **Company self-reports** — see below
- Never-published MOU findings
- Non-English-only output
- Rows failing source verification

**Company self-reports (hard drop, added 2026-08-14).** A report published by a model developer
about its own model(s) in which **no external evaluator is named** is out of scope entirely. The
accountability pipeline this dataset measures requires an external party to make the finding; a
developer reporting on itself has no one to respond to.

> **Carve-out — load-bearing. Do not collapse this rule into "drop anything a company published."**
>
> Many company system cards contain a section contributed by a **named external evaluator**. That
> section is **in scope**. Its findings enter under the **evaluator's** Institution and the
> evaluator's Scope (`government-AISI` if a government AISI contributed, else
> `third-party-evaluator`), with `company-published` on Finding Type — **never under the company**.
> The company's own surrounding self-assessment in the same document remains a hard drop.
>
> Worked examples already in v10:
>
> | Report ID | Source document | Filed under | Scope |
> |---|---|---|---|
> | `JOINT-2026-07-*` | GPT-5.6 System Card | Joint UK AISI + OpenAI (company-published) | government-AISI |
> | `OPENAI-2025-08-SELF` | GPT-5 System Card | Apollo Research / Joint UK AISI + US CAISI | both |
> | `ANTHROPIC-2026-06-SELF` | Claude Fable 5 & Mythos 5 System Card | UK AISI | government-AISI |
> | `JOINT-2025-05-ALI2..5` | Claude Opus 4 & Sonnet 4 System Card | Apollo Research + Anthropic | third-party-evaluator |
>
> These documents exist **only** on the company's own site. Dropping the four company venues from
> the roster would silently delete 16 existing rows.

**The narrowed screening test.** For any item on a company venue the question is **not** "does it
contain a finding?" but the far cheaper:

> **"Is an external evaluator named as contributing findings?"**

- **No** → `EXCLUDED - company self-report`. Stop. Do not read further, do not extract.
- **Yes** → `INCLUDED`, but only that evaluator's section, filed under that evaluator.

This drop applies **wherever the report is published**, not only on company venues — a developer's
solo self-evaluation posted to arXiv is the same drop.

> ⚠ **Open edge case.** "Model developer" is not limited to the four company venues. Four roster
> organisations both build and evaluate models: **Allen Institute for AI (Ai2)** (OLMo/Molmo; 548
> items, 21 pending, 0 included), **Shanghai AI Lab** (InternLM; 11 included — all verified as
> third-party work on *other* models, clean), **Tsinghua CoAI** (10 pending) and **Scale AI**
> (34 pending). §7.3 covers them in principle ("a model developer's report about its own models"),
> but the protocol names only the four company venues, so a screener may miss it. **The test is
> whose model is under evaluation, not who published.**

---

## 8. Stage 4 — Identity

### 8.1 Finding ID — the primary key

**Format:** `PREFIX-YYYY-MM[m]-DDDn[-sN]`

- `PREFIX` — institution prefix (registry below). New orgs get a prefix assigned once, in the rulebook.
- `YYYY-MM` — the report's publication year-month. `[m]` = optional lowercase letter (`a`, `b`)
  distinguishing multiple same-month reports from one org.
- `DDD` — three-letter domain code reflecting the finding's domain **at initial assignment**.
- `n` — sequence number within report + domain. `[-sN]` — split suffix (§6).

**Rules:**

1. **Unique** across the sheet — v10: 456/456 ✓. Primary key for the dashboard, the paper's
   appendices, and the ledger.
2. **Immutable.** IDs are keys, not semantics. If a row's Domain is later recoded or a date is
   corrected, the ID does **not** change. 23 IDs carry domain codes that no longer match the
   revised Domain column — **this is expected, not an error.**
3. **Legacy variants are grandfathered, never retro-fixed:** trailing `b` on the sequence
   (`…-ALI1b`), uppercase month letter (`2026-05B`), hyphenated prefix (`AISI-JP-…`). New IDs
   follow the format strictly.

**Institution prefix registry:** UKAISI · USCAISI · JOINT (any multi-org exercise) · SECUREBIO ·
METR · APOLLO · NETWORK · SGAISI · FRANCE · UL · CISCO · SHANGHAIAILAB · TSINGHUACOAI · HAL ·
LATTICEFLOW · TRANSLUCE · SCALEAI · CIP · PALISADE · DREADNODE · FARAI · RAND · OPENAI ·
ANTHROPIC · AISI-JP (legacy) · *(new orgs: add to the rulebook before first use)*

**Domain code registry:** `JAI` Jailbreaks · `CYB` Cyber · `BIO` Bio-Chem · `ALI` Alignment ·
`AUT` Autonomy · `SOC` Societal · `HUM` Human Influence · `GOV` Governance/process

### 8.2 Report ID — the grouping key

- Groups all findings extracted from one report; **must be unique per report.** Two different
  reports must never share an ID — split collisions with a letter suffix (`UKAISI-2026-03` /
  `UKAISI-2026-03b`).
- **Format going forward:** `PREFIX-YYYY-MM[-slug]`, slug only when needed to disambiguate.
- Legacy Report IDs use three coexisting conventions (bare month, finding-style, descriptive slug
  such as `OPENAI-2025-08-SELF`) — grandfathered, never renamed.
- All rows sharing a Report ID must share the same **Report Title, Source URL, and Publication
  Date**. ⚠ 8 reports currently violate the same-date rule (§14).

---

## 9. Stage 5 — Severity: the C1/C2 ensemble

### 9.1 The mechanism

Severity is coded by **three independently queried models** — Claude Sonnet 5, GPT-5.5, and
Gemini 3.1 Pro — each applying the **frozen prompt** in `run_severity_ensemble.py`.
**Majority vote wins. All three votes stay on the record** (columns 14–16) and are never
overwritten. The script also computes Fleiss' κ.

Each model returns JSON only: seven boolean domain flags, a supporting verbatim quote, the
category, a confidence, and a one-line reason. `category = 1 if ANY d* is true, else 2`.

### 9.2 Why these thresholds

The Category 1 domains deliberately mirror the dangerous-capability thresholds **the frontier
developers themselves publish** — Anthropic's RSP (ASL / Capability Thresholds), OpenAI's
Preparedness Framework, and Google DeepMind's Frontier Safety Framework (Critical Capability
Levels). The severity bar is therefore the industry's own, not the researcher's.

### 9.3 Category 1 (Critical) — any ONE demonstrated

| | Domain | Trigger |
|---|---|---|
| **D1** | CBRN / Bio-Chem uplift | Meaningful uplift toward chemical/biological/radiological/nuclear weapons; expert-surpassing bio/chem capability; crossing a stated CBRN threshold |
| **D2** | Cyber operations | Offensive cyber capability; expert-level or novel-uplift hacking; completing realistic multi-stage attack chains; high CTF/exploit success; "High"+ cyber designation |
| **D3** | Autonomy / AI R&D / self-replication | Autonomous replication, self-propagation, or automating AI R&D / accelerating scaling |
| **D4** | Persuasion / manipulation / societal harm at scale | Systematically changing beliefs or behaviour at scale; implication in large-scale societal harm (mass CSAM, election-scale persuasion exceeding a real benchmark) |
| **D5** | Deceptive alignment / misalignment | Deliberate deception, scheming, sabotage, sandbagging, blackmail, or hiding of abilities/intentions |
| **D6** | Safeguard failure | A **deployed** safety mechanism (jailbreak defence, classifier, guardrail, refusal training, content filter) bypassed, defeated, or shown to fail, allowing harmful output on a frontier system |
| **D7** | Evaluation integrity compromised | The evaluation itself undermined — model detected it was being evaluated, gamed the benchmark, was trained on eval data (contamination), or defeated/de-anonymised the eval environment |

### 9.4 Category 2 (Non-critical)

Reassuring / null results (capability **below** expert threshold, "no uplift", "did not degrade",
"zero instances"); capability-**gap** findings (the model *fails* a task); positive
methodology/tool contributions; pure process/governance observations; findings about
non-frontier or small research models where no frontier system is implicated.

### 9.5 The four critical rules (verbatim from the frozen prompt)

1. **NEGATION** — "did NOT", "below expert", "zero instances", "no uplift", "remained below" →
   **Cat 2**, even with alarming vocabulary.
2. **DEMONSTRATED, not mentioned** — the capability or failure must be *shown in the evaluation*,
   not merely discussed or proposed.
3. **TRAJECTORY** — a rising trend is Cat 1 **only if a dangerous capability was reached NOW**. A
   pure future projection with no current dangerous level is Cat 2. If a dangerous capability *is*
   demonstrated at present, code Cat 1 even if the sentence also describes a trend.
4. **SOCIETAL HARM** — documented real-world harm at scale **is** Cat 1 under D4, even without a
   "safeguard".

Restated in the rulebook: **C1 requires a demonstrated threshold** — a working universal
jailbreak, a full attack chain, expert-surpassing bio capability. Not alarming wording, not
model-vs-model uplift, not a trend, not a negation.

### 9.6 Disagreement handling

34 non-unanimous rows in v10 — **29 true 2–1 splits plus 5 single-model errors decided 2–0** — are
published in the paper's **Appendix D**. A unanimous vote that conflicts with the written rule is
a **re-vote candidate, not an authority**.

---

## 10. Stage 6 — Tier assignment (who is accountable)

Every finding sits in exactly one tier, encoded by `Eval? (trackable)` + `Action Trackable?`:

| Tier | Encoding | Meaning | n (v10) |
|---|---|---|---:|
| **A** | yes / yes | Accountability-relevant: named company/model + concerning + response reasonable to expect. **The ONLY tier scored for proportionality** | 111 |
| **B** | yes / no | Concerning but no accountable party: anonymised models, methodology findings, reassuring nulls, non-frontier, capability trends | 240 |
| **C** | no / (blank) | Not an empirical model finding (methodology / framework / governance / milestone) | 105 |

### 10.1 The Tier A test — ALL must hold

1. It is an **empirical model finding**
2. It **names a specific company or model** — company-level suffices; "anonymised" fails
3. It **demonstrates a concerning result for which a specific company response is reasonable to
   expect**

### 10.2 What condition (3) excludes

Reassuring nulls · benchmark-score or relative-uplift results with **no dangerous threshold
crossed** · inconclusive results · comparative rankings · capability trends and forecasts ·
findings where named models are **instruments of a methodology study, not its subject** · company
self-classifications ("we treat this as High capability") · non-frontier models · too-recent
findings.

> ⚠ **Known gap (to close):** 65 solo capability-findings sit outside Tier A on condition (3) or
> on frontier/scope judgments whose **per-row justification is not yet written into
> `Sources Checked`**. Backfill required. The paper currently carries a government-AISI-only
> sensitivity line as the guard.

---

## 11. Stage 8 — The response search (Tier A findings only)

The mirror of the finding search: **a fixed battery, executed in order, each source logged with
its check date in `Sources Checked`.** Search window: finding publication date → corpus cutoff,
**re-swept quarterly** for open `None`/`Partial` rows.

### 11.1 Channel A — company response (determines Action Level)

**All five must be checked before a `None` may be coded:**

1. **Company newsroom / blog** — site search for the evaluator's name and the finding's model or topic
2. **The next model/system card(s)** for that model family published after the finding — and, for
   pre-deployment evaluations, **the launch card itself, which is the canonical response location**
3. **Company safety / deployment hubs** — e.g. `deploymentsafety.openai.com`, Anthropic
   safeguards/RSP pages, transparency reports
4. **Official company accounts / newsroom posts**
5. **Open web search** — `<company> response <evaluator> <finding topic>`, used **only to locate
   company primary sources**. News articles are never Channel A evidence.

**Rules.** Admissible evidence is the company's own primary document **only**. Any candidate
response **dated before the finding** is invalid unless it is a documented pre-deployment
coordinated disclosure (§11.4) — record invalidations in `Sources Checked`. **Stop condition:**
battery exhausted → `Action Level = None` **plus a dated search log**.

**Classification:** `Substantive` (specific, documented, attributed change) · `Partial` (claimed
but unverifiable, or incomplete) · `Acknowledged` (referenced, no action) · `None` (nothing located).

### 11.2 Channel B — policy uptake (determines Policy Level)

1. **UK** — Hansard (Commons + Lords), committee reports, gov.uk ministerial statements,
   regulator advisories (NCSC, BoE/FCA, ICO)
2. **US** — Congress.gov, Federal Register, agency announcements (Commerce/NIST), committee records
3. **EU / other** — Commission statements, national regulator publications matching the finding's
   jurisdiction

Search terms: evaluator name, report title, and the finding's specific claim. **Admissible =
official government sources only.** Classification: `Binding policy action` / `Non-binding policy
uptake` / `No policy uptake identified` — the last coded only after the battery is exhausted, on
Tier A rows.

### 11.3 Channel C — coverage log (no score)

Log, with URL and date: independent press coverage, academic citations (Semantic Scholar / Google
Scholar count, dated), notable public discussion threads. **The finding's own paper and the
company's own posts are circular → excluded.** This channel is **evidence, not measurement**:
nothing is computed from it except the documented-coverage share of no-response findings (the
obscurity check).

### 11.4 Attribution rules (Channel A)

A company action counts as a response **only if causally attributable to the finding**:

- **Pre-existing or standing policy is NOT a response** — a framework clause or product decision
  that predates the finding does not count, even on the same topic.
- **Company self-reports are not third-party responses.**
- **Negative lag is allowed** for pre-deployment evaluations (the company had the findings before
  publication). **Lag 0 = coordinated disclosure. Never use 0 as a placeholder.**
- Response dates are the **actual dates of the source documents**, verified.
- A `None` coding **must** record where we searched, in `Sources Checked`, with the search date.

`Attribution` has two categories: **Explicit attribution** (the company names the evaluator or
finding) / **No explicit attribution** (everything else, including no response).

---

## 12. Stage 9 — Proportionality (derived; never hand-edited)

**Formula, no discretion, severity-dependent** (revised 2026-08-03). Computed on **Channel A
only**, **Tier A rows only** (`Action Trackable = yes` ⇔ `Action Level` populated). **Policy uptake
never substitutes for a company response.**

| | Substantive | Partial | Acknowledged | None |
|---|---|---|---|---|
| **C1** | Proportionate | Under-response (gap) | Under-response (gap) | Accountability gap (no action) |
| **C2** | Proportionate | Proportionate | Under-response (gap) | Accountability gap (no action) |

Equivalently: **C1 requires a Substantive response to pass; C2 requires at least a Partial
response.**

**No too-recent exception.** The 3 rows carrying a `too-recent` Finding Type modifier are already
excluded upstream at `Action Trackable = no`, so they never reach this formula.

---

## 13. Stage 10 — Reconciliation (end of every sweep)

**Step 0 — Rebuild the reconciliation key from the canonical CSV first.** `known_reports.json`
must be regenerated from the live `v10.csv` Report ID column at the start of every reconciliation,
**never reused from a prior sweep.**

> **2026-08-01 failure mode, recorded so it is not repeated.** The key held 153 Report IDs against
> a 211-ID sheet. The 59-ID gap caused **34 already-present reports to be mislabelled "genuinely
> new"** and **31 already-present items to be counted as candidate misses**. Detected 2026-08-14.

1. **Every Report ID in the canonical CSV must appear as `INCLUDED`** — any missing = sweep gap,
   re-check that venue.
2. **Any `INCLUDED` item with no Report ID = a candidate miss** → triage for extraction into the
   next dataset version. Before triage, match candidates against the canonical CSV by **URL and
   normalised title**, not by Report ID alone — Report IDs are absent on these rows by definition,
   and title variants will otherwise read as new:
   - "System Card: Claude Opus 4 & Claude Sonnet 4" vs "Claude Opus 4 and Claude Sonnet 4 System Card"
   - "GPT-5.6 System Card (Sol/Terra/Luna)" vs "GPT-5.6 System Card"
3. **Zero-yield venues reported explicitly** — "swept N items, 0 included".

---

## 14. The 40-column reference

Legend: 🔑 identifier · 📋 descriptive · 📊 analysis input · 🧾 evidence/audit · ⚙️ derived (never hand-edit)

| # | Column | Type | Meaning, allowed values, and what matters |
|---|---|---|---|
| 1 | Finding ID | 🔑 | Primary key. §8.1. Unique, immutable |
| 2 | Report ID | 🔑 | Groups findings of one report. §8.2 |
| 3 | Institution | 📋 | The **evaluating** body, canonical spelling; must match what the source names. Joint variants spell out all parties |
| 4 | Report Title | 📋 | Verbatim title of the source report. Same for all rows of a Report ID |
| 5 | Publication Date | 📊 | The report's real release date, source-verified. `YYYY-MM-DD` (or `YYYY-MM` if that is all the source gives). **Date only, never a time.** Feeds Lag and per-year stats |
| 6 | Domain | 📊 | Finding-level, multi-select (semicolon), controlled vocabulary: Cyber, Bio-Chem, Alignment, Jailbreaks, Autonomy, Societal, Human Influence + governance sub-types (Institutional, Eval-methodology, Eval-tooling, Transparency/Disclosure, International-coordination, Policy/Standards, Frontier-forecasting). **Never blank, never bare "Governance"** |
| 7 | Tags | 📋 | Internal search aid only (lowercase-hyphenated, semicolons). **Not analytical** |
| 8 | Models / Systems | 📋 | The finding's **subject** model(s) only; comparators → Notes. "anonymised" when the source does not name it (⚠ 37 blanks pending) |
| 9 | Access Type | 📊 | Pre-deployment / Post-deployment / Mixed / Aggregate / N/A. Drives the paper's most policy-relevant split |
| 10 | Source URL | 🧾 | Primary source **of the finding** — the evaluator's own report where one exists; a company document only if it is the sole publisher (then Finding Type gets `company-published`) |
| 11 | Finding | 📋 | 1–2 sentence paraphrase; every number verified against the source; no overstatement |
| 12 | Finding Quote | 🧾 | Verbatim quote supporting the finding. *(Currently byte-identical to Key Quote in all rows — kept deliberately; treat Key Quote as authoritative)* |
| 13 | Severity (C1/C2) majority | 📊 | Majority of the three ensemble votes. §9 |
| 14–16 | Sonnet5 / GPT-5.5 / Gemini3.1 vote | 🧾 | The three raw ensemble votes (C1/C2/ERR). **Never overwritten** |
| 17 | Action Level | 📊 | Tier A only. **Substantive** / **Partial** / **Acknowledged** / **None**. Coherence: response fields filled ⇔ level ≠ None |
| 18 | Attribution | 📊 | Tier A only, two categories: **Explicit attribution** / **No explicit attribution** |
| 19 | Company Response | 📋 | Concise factual clause from the company's own primary source. No URLs in text |
| 20 | Channel A Verbatim | 🧾 | Character-exact quote of the response from the company source |
| 21 | Response Date | 📊 | Actual date of the company source document |
| 22 | Lag (days) | ⚙️ | = Response Date − Publication Date. Negative allowed (pre-deployment); 0 = coordinated disclosure. Exists ⇔ Response Date exists (⚠ 3 violations) |
| 23 | Channel A Evidence | 🧾 | Company primary-source URL. Exists ⇔ a response exists (⚠ 6 violations) |
| 24 | Sources Checked | 🧾 | The audit-trail cell. **Four uses:** dated search logs behind None codings; negative-lag invalidation records; verification pointers behind confirmed responses; tier-assignment justifications |
| 25 | Policy Level | 📊 | **Binding policy action** / **Non-binding policy uptake** / **No policy uptake identified** (Tier A rows searched with nothing found). Non-Tier-A rows may be blank. Official government sources only |
| 26 | Policy Response | 📋 | What the policy action was, from the official source |
| 27 | Channel B Verbatim | 🧾 | Exact quote from the government source |
| 28 | Channel B Evidence | 🧾 | Official government URL |
| 29 | Media Outlets | 🧾 | Independent press coverage, each item with its URL. Powers the obscurity check |
| 30 | Academic Citations | 🧾 | Verified citations/counts with sources (e.g. Semantic Scholar, dated) |
| 31 | Social Highlights | 🧾 | Notable public discussion, with links. Log only |
| 32 | Channel C Verbatim | 🧾 | Quotes from third-party coverage. Log only |
| 33 | Proportionality | ⚙️ | Formula in §12. Never hand-edit |
| 34 | Notes | 🧾 | Audit trail: `[CLUBBED …]` `[SPLIT …]` `[RECLASSIFIED …]` `[Report tested: …]`, caveats |
| 35 | Key Quote | 🧾 | Short exact verbatim from the source report. **Authoritative quote cell** |
| 36 | Traceability Tag | 📋 | Legacy column (mixed vocabulary, overlaps Finding Type). Retained; **do not extend** |
| 37 | Eval? (trackable) | 📊 | yes = empirical model finding; no = Tier C (§10) |
| 38 | Action Trackable? | 📊 | yes ⇔ full Tier A test (§10.1). Blank on Tier C rows |
| 39 | Finding Type | 📊 | Nature (**exactly one**): `capability-finding` / `methodology` / `capability-trend` / `governance`, plus modifiers (0+): `anonymised-model`, `reassuring-null`, `company-self-report`, `too-recent`, `non-frontier`, `company-published`. ⚠ The `company-self-report` **modifier** is NOT the dropped Scope value — it marks a company self-assessment *quoted inside an in-scope report by a named external evaluator* (8 rows, e.g. `JOINT-2026-02-JAI2`, `USCAISI-2026-07-GOV2`) |
| 40 | Scope | 📊 | `government-AISI` / `third-party-evaluator`. **Exactly two values** (§7). Headline stats use government-AISI only |

---

## 15. Cross-cutting evidentiary standard

- **Real-or-empty** — every cell is verified-real or deliberately blank/None. **Never inferred,
  never fabricated.**
- **Admissible sources** — Channel A = the company's own primary document; Channel B = official
  government source; coverage logs = independent third parties. **News quoting a company is not
  Channel A.**
- **Coherence** — evidence links exist only where a response or coverage exists; "where we looked"
  lives in `Sources Checked`.
- **Every number and quote verified against the *correct* cited source.**

---

## 16. The funnel, end to end

```
46 organisations derived  →  33 active (13 retired, §2.2)
  │
  └─ 6,712 items enumerated across 46 venues
      ├─ 2,116 rows at retired venues (kept in ledger, out of corpus)
      └─ 4,463 ACTIVE CORPUS rows — every one with a decision + reason
          │
          ├─ 2,601  not an evaluation (title triage, no fetch)
          ├─   523  no findings
          ├─   397  RAND gates (253 out-of-scope format · 144 off-topic)
          ├─   597  UNRESOLVED (364 pending fetch + 233 pending evaluator check)
          ├─   110  other exclusions (dup 79 · no named evaluator 15 · out-of-scope org 15 · self-report 1)
          ├─    16  post-cutoff → next version
          │
          └─   219  INCLUDED
              └─ 211 reports in v10.csv
                  └─ 456 findings (split & club applied)
                      │
                      ├─ SEVERITY  3-model ensemble → C1 / C2  (34 non-unanimous → Appendix D)
                      ├─ TIER      A=111 · B=240 · C=105
                      ├─ SCOPE     government-AISI=291 · third-party=165
                      │
                      └─ Tier A (111) → Channel A/B/C batteries → Proportionality (formula)
```

### 16.1 The remaining queue

| Venue | Pending | Venue | Pending |
|---|---:|---|---:|
| Google DeepMind | 81 | Meta | 22 |
| Anthropic | 66 | Princeton HAL | 22 |
| OpenAI | 64 | Redwood | 17 |
| RAND *(filtered)* | 48 | Dreadnode | 15 |
| Center for AI Safety | 47 | Shanghai AI Lab | 13 |
| Cisco | 46 | Gray Swan | 12 |
| Holistic AI | 35 | Tsinghua CoAI | 10 |
| Scale AI | 34 | Korea AISI, UL DSRI | 7 each |
| FAR.AI | 27 | Citadel, SecureBio | 6 each |
| | | Palisade 5 · LatticeFlow 3 · Transluce 2 · METR 2 | |

**233 of the 597 are the four company venues** — one-question checks under §7.3, not full screens.
Genuine full-fetch work is **364 items**.

## 17. Known limitations and open items

Tracked in the rulebook §11 until resolved.

| # | Item | Status |
|---|---|---|
| 1 | **Too-recent rule** — drop category (73%→75%) / 30-day censoring (78%) / 60-day (77%) / keep with footnote | Pending decision; currently one hand-judged row |
| 2 | **8 reports with internally inconsistent Publication Dates** (RepliBench, STACK, RealityTest, OpenClaw + 4) | Resolve each to the true release date |
| 3 | **Coherence repairs** — 3 Lag-without-Response-Date · 6 Channel-A-evidence-without-Action · 11 Policy-Response-without-uptake · 37 blank Models/Systems → "anonymised" | Open |
| 4 | **5 ensemble ERR votes** — re-run the errored model | Needs API keys |
| 5 | **Tier A justification backfill** for the 65 excluded solo capability-findings | Open; sensitivity line is the guard |
| 6 | **Screening ledger** — 657 of 6,498 rows unresolved; reconciliation key stale (rebuild first) | Partially complete, halted 2026-08-01 on spend limit |
| 7 | **Human validation of the severity ensemble** — ~20% stratified sample, report κ | Required before submission |
| 8 | **Dual-role organisations** (Ai2, Shanghai AI Lab, Tsinghua CoAI, Scale AI) not named in the protocol's self-report clause | Identified 2026-08-14, §7.3 |

### 17.1 Honest statement of recall

**The "enumeration is COMPLETE" claim is withdrawn** (2026-08-14). Two independent gaps were found:

1. **24 reports already in `v10.csv` were never enumerated at all** — 4 UK AISI, 4 Holistic AI,
   5 Shanghai AI Lab, 2 CIP/Weval and others. UK AISI is recorded as fully screened across 152
   enumerated items, yet four of its own reports in the dataset never appeared. Until each miss is
   explained, the recall of the other 6,712 is unknown.
2. **81 enumerated items had never been written to the ledger** (SecureBio, CAIS, HAL and Korea
   worst) and were invisible in the pending count. They have been backfilled as `PENDING-FETCH`;
   a further 58 candidates were rejected as URL-variant duplicates of rows already present.

Screening is also incomplete: **597 of 4,463 active rows (13.4%)** carry no terminal decision,
including all of Google DeepMind and Meta — 0 included across 421 rows, where the sweep predicted
"expected to screen out" but never verified it.

Any completeness claim in the paper must therefore be stated against the **3,866 resolved active
rows**, must disclose the 24 known enumeration misses, and must disclose that six International
Network members were retired from the roster (§2.2) — so "every Network member was swept" is no
longer available as a claim.

## 18. Changelog (rules only)

- **2026-08-14 · Roster corrections A/B/C; 46 → 33 organisations.** (A) Seven orgs retired as
  `EXCLUDED - not a roster org` after one joint Institution string was parsed as seven evaluators —
  1,405 enumerated, 0 inclusions. (B) Six zero-yield Network members retired as
  `EXCLUDED - venue retired` — 896 enumerated, 0 inclusions. (C) RAND format + topic gates,
  756 → 359. Plus 81 enumerated-but-never-ledgered items backfilled. Active corpus 6,498 → 4,463;
  unresolved 657 → 597; `INCLUDED` unchanged at 219. Grandfathering tightened to publisher-only.
- **2026-08-14 · Company self-reports → HARD DROP** (§7.3). `Scope` reduced to two values; the
  third was never populated (0/456), so no existing row, stratified table, or headline number
  changes. The `company-self-report` *Finding Type modifier* is retained and disambiguated. §7.3
  gains the load-bearing carve-out preserving the 16 rows sourced from company-published documents
  via a named evaluator. Company-venue screening narrows to "is an external evaluator named?".
  `SEARCH_PROTOCOL` §2/§4 updated; sweep artifacts re-decided with rows retained for PRISMA.
- **2026-08-14 · Reconciliation Step 0 added** (§13) — the key must be rebuilt from the canonical
  CSV every sweep, after the 153-vs-211 stale-key failure; candidate-miss matching must use URL
  and normalised title.
- **2026-08-03 · Header cutoff corrected back to 2026-07-30.** An earlier fix had wrongly read the
  max Publication Date present in the sheet rather than the frozen cutoff. `DREADNODE-2026-07-CYB2`
  carries a date one day past the cutoff — a data note, not a reason to move the cutoff.
- **2026-08-03 · Proportionality changed to severity-dependent; one row recoded.**
  `APOLLO-2026-07-ALI2` (C2, Partial) moved from Under-response to Proportionate. Effect: C1-only
  gap unchanged (64/78 = 82.1%); all-Tier-A gap 93/111 (83.8%) → 92/111 (82.9%). Pre-edit CSV
  backed up to `v10_backup_before_prop_fix.csv`.
- **2026-08-03 · Stale headline counts corrected** throughout — 345 findings / 153 reports /
  Tier A=55 / B=185 → 456 / 211 / A=111 / B=240 / C=105.
- **2026-08-01 · §8b added** — the response-search protocol: Channel A five-source battery with
  stop condition, Channel B jurisdiction battery, Channel C logging rules, quarterly re-sweep.
- **2026-08-01 · Too-recent category dropped** — every finding judged by its actual Action Level,
  no recency exception.
- **2026-08-01 · v10 rulebook created** — consolidates codebook v6 + SEARCH_PROTOCOL v1 + the v10
  category changes (Attribution → 2 categories; Policy Level → 3; Traction Score deleted; finding
  definition added; ID rules formalised).
