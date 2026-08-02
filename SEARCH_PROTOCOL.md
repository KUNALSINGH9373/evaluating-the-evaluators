# Search & Screening Protocol (SOP Step 1) — v1, 2026-08-01

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

**Company release artifacts** (screened for *named-evaluator* findings only):
every model/system card and safety blog post in the window from OpenAI (incl.
deploymentsafety.openai.com), Anthropic, **Google DeepMind**, and **Meta**. (GDM/Meta expected
to screen out — log the zero.)

**arXiv**: via each roster org's publication list and citation-chasing from included reports —
not open keyword search.

## 3. Window

Each venue's first publication → **2026-07-09** (frozen corpus cutoff). Items after the
cutoff are logged as `POST-CUTOFF` (ledger only, not corpus) so the next version ingests them.

## 4. Screening categories (every enumerated item gets exactly one)

| Decision | Meaning |
|---|---|
| `INCLUDED` | Contains ≥1 qualifying finding (per §1.0) by an in-scope, named evaluator |
| `EXCLUDED — no findings` | Announcement, opinion, methodology promise, plan |
| `EXCLUDED — no named evaluator` | "External evaluators"/"specialist groups" with no agency named (codebook §0 hard drop) |
| `EXCLUDED — non-English` | Non-English-only output |
| `EXCLUDED — out-of-scope org` | Publisher not on the roster and no roster co-author |
| `EXCLUDED — duplicate/secondary` | Restates findings whose primary source is already INCLUDED (see §5) |
| `POST-CUTOFF` | Qualifying but published after 2026-07-09 |

## 5. Dedup rule

The **primary (earliest, fullest) source wins**. Progress reports / annual summaries are
`EXCLUDED — duplicate/secondary` **unless** they contain a finding published nowhere else,
in which case only that finding enters, with the summary as its source.

## 6. Ledger schema (`screening_ledger.csv`)

`venue, item_title, url, publication_date, decision, reason (1 line), report_id (if INCLUDED,
maps to the dataset), sweep_date, sweeper`

## 7. Reconciliation (end of every sweep)

1. Every Report ID in the current canonical CSV must appear as `INCLUDED` — any missing =
   sweep gap, re-check the venue.
2. Any `INCLUDED` item with no Report ID = **candidate miss** → triage for extraction into
   the next dataset version.
3. Zero-yield venues are reported explicitly ("swept N items, 0 included").

## 8. Evidence standard for the ledger itself

Item lists come from the venue's own publication index (paginated fully). URLs recorded as
found; archive (web.archive.org) capture requested for every INCLUDED item.
