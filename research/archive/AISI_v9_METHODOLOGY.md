# Evaluating the Evaluators — Methodology (Dataset v9)

*Do AISI / third-party evaluations lead to meaningful, proportionate action?*
Kunal Singh · MATS Summer 2026 (mentor: Stephen Casper)

---

## 1. Scope & inclusion

The dataset comprises **345 distinct evaluation findings** about frontier AI systems, each a single, specific empirical claim from a published evaluation. A finding is included if it was produced by one of three actor types:

- **Government AI Safety Institutes** — UK AISI, US CAISI, joint US–UK pre-deployment tests, and other national institutes (e.g. Singapore SGAISI, Korea K-AISI).
- **Independent third-party evaluators** — e.g. METR, Apollo Research, SecureBio, FAR.AI, Scale AI, HAL, CIP, Holistic AI, LatticeFlow, and members of the AI Evaluators Forum.
- **Company self-reports** of external red-teaming (filed under a distinct `company-self-report` provenance so they are not mistaken for independent evaluation).

Findings authored by none of these actor types (e.g. the Bengio *International AI Safety Report*) are excluded. Each row is one finding from one report; a report contributes multiple rows only where it makes genuinely distinct claims.

**Provenance split:** government-AISI **272** (79%), third-party-evaluator **70** (20%), company-self-report **3** (1%).

**Institution roster** (51 distinct institutions/consortia; joint pre-deployment tests appear as combined attributions):

*Government AI Safety Institutes* — **UK AISI** (179 findings; also lead on most joint tests), **US CAISI / NIST** (23 solo + joint), **Singapore AI Safety Institute** (SGAISI / IMDA), **Korea AI Safety Institute** (K-AISI / TTA), **Japan AI Safety Institute** (J-AISI), **Australia AI Safety Institute**, **France INESIA / PEReN**, and the **International Network of AI Safety Institutes** (multi-country joint evaluations). Major joint attributions: Joint UK AISI + US CAISI (27), Joint UK + US + Singapore (5), Joint US AISI + UK AISI (3), + Gray Swan (3), + Anthropic/OpenAI as company-published (6).

*Independent third-party evaluators* — METR (13), SecureBio (10), Apollo Research (~10 incl. partnerships), Holistic AI (5), Princeton Holistic Agent Leaderboard / HAL (5), Transluce (3), Shanghai AI Laboratory / AI45 Lab (3), Robust Intelligence – Cisco (3), UK AISI + Thorn (3, CSAM), LatticeFlow AI (3), Scale AI (2), Collective Intelligence Project / Weval (2), UL Research Institutes / DSRI (2), plus Redwood Research, Center for AI Safety, Palisade Research, Dreadnode, Citadel AI, RAND, FAR.AI, Tsinghua CoAI, and AVERI (1 each).

*Company self-reports of external red-teaming* — Anthropic (2), OpenAI (1).

## 2. Provenance & evidentiary standard

Every cell is held to a **real-data-or-empty** rule: a value is entered only if it can be traced to an admissible source, otherwise the cell is left blank (never fabricated, never filled with a placeholder). For claims of *company response* specifically, only six categories of source are admissible as a company statement: (1) marketing/PR, (2) investor/SEC filings, (3) regulatory testimony, (4) legal/ToS documents, (5) safety reports/system cards, (6) formal policy statements. **News reporting that quotes a company is not admissible** as a company statement — it may support a Channel C (ecosystem) entry only. A **coherence rule** governs the response columns: response evidence exists only where a response exists; where a source was checked but nothing found, that is recorded under `Sources Checked`, not as a response.

## 3. Severity coding (Critical / non-critical)

Each finding is assigned a binary severity — **C1 (Critical)** or **C2 (non-critical)** — using a fixed, finding-independent codebook grounded in published frontier-safety frameworks (Anthropic RSP, OpenAI Preparedness Framework, Google DeepMind Frontier Safety Framework). A finding is **C1 if it *demonstrates* any one** of seven dangerous-capability domains:

| | Domain |
|---|---|
| D1 | CBRN / bio-chem uplift |
| D2 | Offensive cyber operations |
| D3 | Autonomy / AI R&D / self-replication |
| D4 | Persuasion / manipulation / societal harm at scale |
| D5 | Deceptive alignment / misalignment |
| D6 | Safeguard failure (deployed defence bypassed) |
| D7 | Evaluation-integrity compromise |

Otherwise the finding is C2. Coding is on what is **demonstrated**, not on how alarming the wording is; negation ("no uplift", "below expert baseline"), capability gaps (model *fails*), reassuring trends, and non-frontier-only results all code C2.

**Codebook v2 boundary rules** (universal thresholds, applied identically to every finding — never per-incident):
- **D1/D4** require crossing an expert/human baseline or stated threshold; matching/exceeding a *prior model* is insufficient.
- **D2** partial multi-stage completion counts only at a decisive/majority share, a full solve, or an official "High" designation; any frontier model fully solving ⇒ C1.
- **D5** requires *deliberate* deception; a measured behavioural rate/pattern is insufficient.
- **D6** requires a *deployed*-safeguard breach; an unreliable *monitoring/detection method* is insufficient.
- **D7** excludes researcher detection methods and gaming shown only on non-frontier models.

## 4. Ensemble annotation & reliability

Severity is assigned by a **three-model cross-provider ensemble** — Claude Sonnet 5, GPT-5.5, and Gemini 3.1 Pro — each independently applying the codebook, with the final label by **majority vote**. Result on v9: **112 C1 / 233 C2**, **Fleiss' κ = 0.844** (30 of 345 split). The three annotators show complementary directional biases — Gemini tends to over-flag (D6/D7), GPT-5.5 is the most conservative, Sonnet the moderate — so majority voting cancels both directions and lands on the defensible middle.

**Validation.** An independent, label-blind re-code of all 345 findings agreed with the ensemble on **93.6%**; every disagreement fell on a pre-identified edge case, and only 2 touched the trackable analysis set. Across the two independently developed codebooks the headline result moved just 72.9% → 72.7%, i.e. the conclusion is robust to labelling choices (a built-in sensitivity check).

## 5. Action-trackability filter

A finding is **Action Trackable = yes** only if it names a *specific problem* about a *specific named company/model* for which a *specific company response is reasonable to expect*. 55 findings qualify (the accountability set); the remainder are alarming-but-untrackable or non-alarming context. Anonymised-model, too-recent, response-unobservable, and non-frontier findings are excluded from trackability and recorded via a `Traceability Tag` so exclusions are explicit, not silent.

## 6. Response channels

For each trackable finding, three response channels are recorded, each held to the evidentiary standard above:

- **Channel A — company response.** The developer's *own primary source* only. Coded by **Action Level** (`Substantive` / `Partial` / `Acknowledged` / `None`) and **Attribution** (`Explicit` / `Topical+Temporal` / `None`), with verbatim quote, response date, and lag (days between finding and response; a legitimately negative lag for pre-deployment evals is set to 0 and flagged).
- **Channel B — policy / government response.** Policy-level actions or statements citing the finding.
- **Channel C — ecosystem traction.** Media, academic, and social uptake, summarised as a **Traction Score** (`High` / `Medium` / `Low`), web-verified and citation-lag-adjusted for 2025–26 findings. Channel C is *context only* and does not enter the proportionality judgment.

## 7. Proportionality

The central outcome variable is **Proportionality = Severity × Action Level**, computed for the trackable set:

| Severity | Action Level | Proportionality |
|---|---|---|
| C1 | Substantive | Proportionate |
| C1 | Partial / Acknowledged | Under-response (gap) |
| C1 | None | Accountability gap (no action) |
| C2 | any | Proportionate (Cat2) |
| — | too-recent | Too-recent (unobservable) |

**Headline result:** of the **44 Critical trackable findings, 32 (72.7%) show a response gap** (23 no-action + 9 under-response).

## 8. Data integrity & reproducibility

Findings are de-duplicated within and across reports via semantic-similarity checks; the coding scheme, per-model votes, per-model reasons (`severity_permodel_v9.csv`), the annotation prompt, and the codebook are retained for release. All transformations are scripted and backed up at each step.

## 9. Known limitations

- Severity labels are LLM-ensemble-generated; a human-expert validation sample is the recommended next step for peer review.
- Response observability is bounded by public disclosure — private/pre-deployment fixes cannot always be excluded (flagged in Notes where relevant).
- The trackable set (n = 55) is small; results are reported as descriptive rates, not inferential estimates.
