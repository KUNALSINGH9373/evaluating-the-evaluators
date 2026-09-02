# Search & Screening Protocol (SOP Step 1) — v1.1, 2026-08-14

Governs the identification and screening of candidate evaluation reports for the
"Evaluating the Evaluators" dataset. Every sweep (initial ledger reconstruction and all
future update cycles) follows this protocol and appends to `screening_ledger.csv`.

## 1.0 Definition of a finding (the unit of analysis)

A **finding** is a discrete, evidence-backed claim asserted by an in-scope evaluator in a
public report, codeable independently of the report's other claims. It must be:

1. **Asserted by the evaluator** — not a summary of someone else's work, not a comparator
   score cited in passing (comparators → Notes, per codebook §2).
2. **Evidence-backed in that report** — a measured result, observed behaviour, or documented
   process fact; not an opinion, recommendation, or forward-looking plan.
3. **Independently codeable** — it would warrant its own response (codebook §2 club test:
   "would the company respond to these as one thing?").

Three kinds qualify: **empirical model findings** (a specific system's capability, behaviour,
or safeguard — including reassuring nulls), **methodology/tooling findings**, and
**governance/process findings**. Announcements, partnership news, opinion pieces, and plans
contain no findings.

## 2. Sweep roster — DERIVED, not hand-picked (Stage 0 of every sweep)

"Venue" = any publication surface of an in-scope organisation — primarily the org's **own
website** (research/blog/publications pages, paginated to the end); arXiv and company release
artifacts are supplements. The roster itself is derived fresh at the start of every sweep from
three authoritative sources, and the derivation is logged with its date:

1. **Government institutes** = the current membership of the **International Network of AI
   Safety Institutes** (fetch the official membership list — as of last check: UK, US, Japan,
   Singapore, Korea, France, EU AI Office, Canada, Australia, **Kenya**) + any newly announced
   national institute (verify Germany, India, others at sweep time). Members with zero rows in
   the current sheet (EU AI Office, Canada, Kenya) are swept anyway — "swept, 0 qualifying
   reports" is itself a census result and must be logged.
2. **Third-party evaluators** = the current membership of the **AI Evaluators Forum** + every
   evaluator organisation already present in the dataset (METR, Apollo Research, SecureBio,
   Transluce, Holistic AI, Princeton HAL, Shanghai AI Lab, LatticeFlow, Robust Intelligence/
   Cisco, UL DSRI, Scale AI, CIP/Weval, Palisade, Dreadnode, FAR.AI, RAND, Redwood, CAIS,
   Citadel AI, Tsinghua CoAI, AVERI). Forum members with zero qualifying reports are logged
   as zeros.
3. **Orgs already in the dataset** that appear on neither list remain on the roster
   permanently (grandfathered).

> ⚠ **Grandfathering attaches to the PUBLISHER, never to a co-author** (added 2026-08-14).
> An organisation is grandfathered only when it is *the publisher* of an included report. An
> organisation named inside a joint `Institution` string is **not** thereby a roster org — the
> report is already captured under whoever published it.
>
> **Failure this fixes:** the single string
> `"UK AISI; University of Oxford; EPFL; Yale; UC Berkeley; Stanford; Allen Institute for AI"`
> on `UKAISI-2025-11a` put six universities on the roster as standalone venues, and
> `"UK AISI + Thorn"` added a seventh. Together they contributed **1,405 enumerated items,
> 1,400 screened rows and 0 inclusions**. The rule was also applied inconsistently — CMU appears
> in `"Gray Swan AI, with Center for AI Safety, CMU, EPFL"` and was never added. All seven are
> retired as `EXCLUDED - not a roster org`; their rows stay in the ledger for PRISMA.

### 2.1 Retired venues (2026-08-14)

Retired venues keep their ledger rows — the zero remains documented — but are dropped from the
active queue and from the corpus denominator.

| Retired | Basis | Enumerated |
|---|---|---|
| Ai2, UC Berkeley, Thorn, EPFL, Yale, Stanford, Oxford | Co-author affiliation only, never a publisher (§2 rule above) | 1,405 |
| EU AI Office, Kenya, Canada AISI, Australia AISI, IndiaAI SI, Germany AISI | Network members with **zero** qualifying reports across full enumeration; retired by explicit scope decision | 896 |

**Roster: 46 → 33 active organisations.** Note the trade-off accepted here: retiring Network
members means the paper can no longer claim to have swept *every* member of the International
Network. State the exclusion explicitly wherever coverage is described.

### 2.2 RAND filter

RAND publishes ~756 items across the window, the overwhelming majority unrelated to AI evaluation.
Two gates apply **before** an item enters the screening queue:

1. **Format gate** — drop `/pubs/commentary`, `/pubs/testimonies`, `/pubs/podcasts`,
   `/pubs/presentations`, `/pubs/visualizations`, `/pubs/corporate_pubs`,
   `/pubs/commercial_books`, `/pubs/rgs_dissertations`, `/multimedia/`, `/news/`, `/events/`.
   Research output only. → `EXCLUDED - out-of-scope format`
2. **Topic gate** — the title must carry at least one of: `AI` · `AGI` · artificial (general)
   intelligence · superintelligence · `LLM` · large language model · machine learning · model(s) ·
   agent(s) / agentic · chatbot · generative · foundation/frontier model · neural · algorithmic ·
   autonomous · deepfake · red-team · jailbreak · benchmark · fine-tuning · alignment · compute ·
   or a frontier-developer name (GPT, Claude, Gemini, Llama, DeepSeek, Qwen, Mistral, OpenAI,
   Anthropic, DeepMind, Google, Microsoft, Meta). → `EXCLUDED - off-topic`

Effect: 756 → **359** in scope (253 dropped on format, 144 on topic). RAND is an AI Evaluators
Forum member, so it cannot be retired; this filter is how its volume is made tractable without
leaving the roster rule.

**Company release artifacts** — every model/system card and safety blog post in the window from
OpenAI (incl. deploymentsafety.openai.com), Anthropic, **Google DeepMind**, and **Meta**.
(GDM/Meta expected to screen out — log the zero.)

> ⚠ **Company venues use a NARROWED test (codebook §1, 2026-08-14).** Do **not** screen these
> items for findings in general. Company self-reports — a developer's report on its own model(s)
> with no external evaluator named — are a **hard drop**. The only question to ask of an item on
> a company venue is:
>
> **"Is an external evaluator (government AISI or third-party) named as contributing findings?"**
>
> - **No** → `EXCLUDED — company self-report`. Stop. Do not read further, do not extract.
> - **Yes** → `INCLUDED`, but **only that evaluator's section**. The findings are filed under the
>   **evaluator's** Institution and Scope (`government-AISI` if a government AISI contributed,
>   else `third-party-evaluator`), with `company-published` on Finding Type. The company's own
>   surrounding self-assessment is still dropped.
>
> This is why the four company venues stay on the roster: `JOINT-2026-07-*` (GPT-5.6 System Card,
> UK AISI section), `OPENAI-2025-08-SELF` (GPT-5 System Card, Apollo section) and
> `ANTHROPIC-2026-06-SELF` exist **only** on the company's own site and would be lost if the
> venues were dropped. The narrowed test makes screening them cheap, not skippable.

**arXiv**: via each roster org's publication list and citation-chasing from included reports —
not open keyword search.

## 3. Window

Each venue's first publication → **2026-07-30** (frozen corpus cutoff). Items after the
cutoff are logged as `POST-CUTOFF` (ledger only, not corpus) so the next version ingests them.

## 4. Screening categories (every enumerated item gets exactly one)

| Decision | Meaning |
|---|---|
| `INCLUDED` | Contains ≥1 qualifying finding (per §1.0) by an in-scope, named evaluator |
| `EXCLUDED — no findings` | Announcement, opinion, methodology promise, plan |
| `EXCLUDED — no named evaluator` | "External evaluators"/"specialist groups" with no agency named (codebook §0 hard drop) |
| `EXCLUDED — company self-report` | Published by a model developer about its own model(s) with **no external evaluator named** (codebook §1 hard drop, added 2026-08-14). Ledger value: `EXCLUDED - company self-report`. Applies wherever it is published, not only on company venues — a developer's solo self-evaluation posted to arXiv is the same drop. Does **not** apply when a named evaluator contributed a section (§2 carve-out) |
| `EXCLUDED — non-English` | Non-English-only output |
| `EXCLUDED — out-of-scope org` | Publisher not on the roster and no roster co-author |
| `EXCLUDED - not a roster org` | Venue was on the roster only via a co-author affiliation, never as a publisher (§2, 2026-08-14) |
| `EXCLUDED - venue retired` | Venue retired by scope decision; rows kept as a documented zero (§2.1) |
| `EXCLUDED - out-of-scope format` | Non-research publication format (§2.2 format gate) |
| `EXCLUDED - off-topic` | No AI / LLM / model / agent / developer term in the title (§2.2 topic gate) |
| `EXCLUDED — duplicate/secondary` | Restates findings whose primary source is already INCLUDED (see §5) |
| `POST-CUTOFF` | Qualifying but published after 2026-07-30 |

Two operational (non-terminal) states also appear in the ledger:

| State | Meaning |
|---|---|
| `PENDING-FETCH` | Eval-candidate awaiting full-text screening |
| `PENDING-EVALUATOR-CHECK` | Item on a company venue awaiting the §2 narrowed test only. Resolves to `INCLUDED` (filed under the named evaluator) or `EXCLUDED - company self-report`. Cheaper than `PENDING-FETCH` — one question, no finding extraction |

## 5. Dedup rule

The **primary (earliest, fullest) source wins**. Progress reports / annual summaries are
`EXCLUDED — duplicate/secondary` **unless** they contain a finding published nowhere else,
in which case only that finding enters, with the summary as its source.

## 6. Ledger schema (`screening_ledger.csv`)

`venue, item_title, url, publication_date, decision, reason (1 line), report_id (if INCLUDED,
maps to the dataset), sweep_date, sweeper`

## 7. Reconciliation (end of every sweep)

0. **Rebuild the reconciliation key from the canonical CSV first.** `known_reports.json` must be
   regenerated from the live `v10.csv` Report ID column at the start of every reconciliation —
   never reused from a prior sweep. (2026-08-01 failure mode: the key held 153 IDs against a
   211-ID sheet, and the 59-ID gap caused 34 already-present reports to be mislabelled
   "genuinely new" and 31 already-present items to be counted as candidate misses.)
1. Every Report ID in the current canonical CSV must appear as `INCLUDED` — any missing =
   sweep gap, re-check the venue.
2. Any `INCLUDED` item with no Report ID = **candidate miss** → triage for extraction into
   the next dataset version. Before triage, match candidates against the canonical CSV by
   **URL and normalised title**, not by Report ID alone — Report IDs are absent by definition
   on these rows, and title variants ("System Card: Claude Opus 4 & Claude Sonnet 4" vs
   "Claude Opus 4 and Claude Sonnet 4 System Card"; "GPT-5.6 System Card (Sol/Terra/Luna)" vs
   "GPT-5.6 System Card") will otherwise read as new.
3. Zero-yield venues are reported explicitly ("swept N items, 0 included").

## 8. Evidence standard for the ledger itself

Item lists come from the venue's own publication index (paginated fully). URLs recorded as
found; archive (web.archive.org) capture requested for every INCLUDED item.
