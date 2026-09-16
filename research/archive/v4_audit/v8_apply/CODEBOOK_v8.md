# Evaluating the Evaluators — Dataset Codebook (v7)

Revised 2026-07-17. Supersedes the v6 codebook (itself superseding v4). This version incorporates every
inclusion/exclusion rule and column definition, **plus all alterations made during the v6 and v7
verification passes** (v7 = §10: METR verbatim backfill + third-party row-bundling correction). Where a
rule changed this session, it is marked **[REVISED]** or **[NEW]** with the reason.

---

## 0. What the dataset measures & scope

The dataset measures the **public-channel accountability pipeline**: when a government AI Safety Institute
publishes a finding about a specific model/company, does a documented response follow?

**Scope = government AISIs and their joint exercises.** [REVISED]
- **In scope (main list, `Scope = government-AISI`):** UK AISI, US CAISI/NIST, and the affiliated national
  AISIs (Japan J-AISI, Singapore SGAISI/IMDA, Korea K-AISI/TTA, France INESIA/PEReN, EU AI Office), plus
  any joint/International-Network exercise **that includes a government AISI** — even joints with a
  non-government co-author (e.g. "UK AISI + Apollo", "SecureBio + US CAISI", "+ Gray Swan", "+ Thorn").
- `Scope = third-party-evaluator` — evaluations by a **non-government** body with **no** government AISI
  co-author (e.g. Apollo Research alone). `Scope = company-self-report` — a company evaluating **its own**
  model (Anthropic/OpenAI self-reports).
- **[REVISED 2026-07-17]** `Scope` is a **descriptive/provenance label only** — it records who did the
  evaluating, nothing more. It does **not** gate `Action Trackable? = yes`. Whether a row belongs in the
  accountability set (Block A of the output) is decided *purely* by the §1 test (real finding + named
  company + concerning result + real response) — a government AISI does not need to be involved. Kunal,
  2026-07-17: "even if a third party is working with a company we can still include it." Previously the
  output grouped `third-party-evaluator`/`company-self-report` rows into a separate trailing block
  regardless of their own Trackable value; this is now removed — every row is sorted into Block A/B/C by
  its own `Eval?`/`Action Trackable?` value, irrespective of `Scope`. Practical effect: `Scope` still
  distinguishes "government AISI publicly found this" from "an independent evaluator found this," but a
  third-party finding with a real, verified company response now correctly lands in the main accountability
  table alongside government-AISI findings. See §11.

**Hard drop (removed from the sheet entirely):** [NEW — the rule that removed the Gemini 3 Pro FSF rows]
- A report that **names no evaluating agency at all** (only "external evaluators" / "specialist groups")
  is out of scope and dropped. Logged in `dropped_rows.csv`.
- Also excluded: private/MOU evaluations never published; non-English-only outputs; rows that fail
  source-verification (fabricated/conflated/wrong-source).
- **[NEW 2026-07-17]** A report whose author is **none of: a government AISI, an evaluation lab, or a
  company** — e.g. an independent academic panel — is out of scope and dropped, even if governments
  commissioned or backed it. Kunal: "we should not include such reports which are either not from a
  government or a evaluation lab or company." Government *sponsorship* is not the same as government
  *authorship*. This dropped the 5-row "International AI Safety Report 2026 (Bengio et al.)" cluster
  (chaired by an independent academic panel, not published by any single government AISI) — see §11.

---

## 1a. Clarification (2026-07-17): "no accountable party" ≠ "exclude from the dataset"

A methodological error was caught and corrected: several real, alarming findings on named open-source/academic
tools (no corporate owner) were initially **omitted from the dataset entirely** with the imprecise reason
"doesn't clear the named-model bar." The correct rule is narrower in scope but broader in what qualifies:
- The finding must be **real and concerning** (alarming, on a company framework, a model, a process, a tool —
  "anything," per the operating standard), attributable to **some identifiable subject** (a company, a named
  tool/framework, even an open-source project) — this is what gets it **into the sheet** (`Eval? = yes`).
- Whether that subject is a **company that can reasonably be expected to respond** is a SEPARATE, later question
  that only determines `Action Trackable?` (yes/no) — never whether the row exists at all.
- "No accountable company" (open-source/academic tools, anonymised models) is a reason to code
  `Trackable = no`, exactly like the `anonymised-model` stratum — it is never a reason to drop the finding.
Four rows were added under this correction (2 France PEReN tool studies, 1 Singapore red-teaming result, 1
France energy-consumption study) — all real, alarming findings previously dropped for the wrong reason.

## 1. The core inclusion test (what earns a place & counts as an accountability finding)

A row is in the **accountability set** (`Action Trackable? = yes`) **iff ALL of the following hold**:

1. **Empirical model finding** (`Eval? = yes`) — not methodology, framework, policy, or milestone.
2. **Names a specific company/model** the response is attributable to (company-level is enough, e.g.
   "OpenAI fine-tuning API"; an unnamed/"anonymised" model is not).
3. **Demonstrates a concerning result** — a specific problem for which a specific company response is
   reasonable to expect. **Excludes** [REVISED, applied this session]:
   - **Reassuring-null** results ("no sabotage found", "below threshold", "not yet capable").
   - **Benchmark-score / relative-uplift** findings where the model still fails most tasks or the uplift
     is marginal, and no dangerous threshold is crossed (see §4 severity).
   - **Inconclusive** results ("no clear conclusion can be drawn").
   - **Comparative rankings** ("old model more X than new model").
   - **Capability-trend / forecast** (doubling rates, "lags frontier by N months").
   - Findings whose parent report is a **methodology/tooling study** where the named models are
     **instruments** (red-team/monitor/test subjects), not the subject of a safety verdict.
   - **Company self-classifications** ("we are treating this as High capability") — that is the company's
     own action, not an evaluator finding.
   - **Non-frontier** models; **too-recent** findings (no time for a response to be observed).

If (1)+(2) hold but (3) fails, keep the row for descriptive/coverage stats but set `Action Trackable? = no`
with the reason recorded in the **Finding Type** modifier (§ column rules).

---

## 2. One-finding-per-row (splitting & clubbing rules) [REVISED — heavily applied this session]

- **Different companies never share a row.**
- **Merge (club) rows that warrant the *same* response**, especially multiple findings from the *same
  report* about the *same model*. Decisive test: *did the company respond to them as one thing?* If yes →
  one row. (E.g. the 4 Constitutional-Classifiers bypasses → Anthropic restructured its architecture once →
  one row. The 3 Claude 3.5 Sonnet benchmark scores → one row.)
- **Keep separate** when findings are genuinely distinct *kinds* warranting *distinct* responses — e.g.
  capability vs safeguard-failure (GPT-5.5 cyber-capability vs its jailbreak), or different domains
  (DeepSeek jailbreak vs CCP-bias vs agent-hijacking).
- **Comparators/baselines** (a model that appears only as a reference point in another model's eval) are
  **not** standalone rows → fold into `Notes` as `[Report tested: …]`. (E.g. a Mythos score cited inside a
  GPT-5.5 report.)
- Merged-away rows are kept as **tombstones** (`Action Trackable? = no`, `[MERGED into X]` note) and
  deleted on finalize.

---

## 3. Response attribution (what counts as a "response") [REVISED — the biggest correction this session]

A company action counts as a response to a finding **only if it is causally attributable to that finding**.

- **Pre-existing / standing policy is NOT a response.** A framework, RSP/Preparedness-Framework clause, or
  product decision that **predates the finding** or was announced independently does **not** count — even if
  it addresses the same topic. (E.g. Anthropic's RSP ARA→checkpoint change was v2.0/Oct-2024, six months
  before RepliBench → not a response; Anthropic gating Mythos / releasing Fable was pre-announced product
  strategy → not a response to the later AISI cyber findings.)
- **Company self-reports are not third-party responses** and don't count toward responsiveness.
- **Negative lag is allowed** for pre-deployment evaluations (company had the findings before public
  release, so a response dated before publication is genuine). Lag must never be `0` used as a placeholder.
- Dates must be the **actual date of each source document**, verified — never the finding's own
  publication date reused as the response date.

---

## 4. Severity (C1 / C2) — demonstrated, not alarming [REVISED emphasis]

- **C1** only if a dangerous-capability **threshold is demonstrated** (D1 CBRN, D2 Cyber, D3
  Autonomy/self-replication, D4 Persuasion, D5 Deception, D6 Safeguard-failure, D7 Eval-integrity) — e.g.
  "first model to complete the full attack chain", a working universal jailbreak, 100th-percentile-of-experts.
- **C2** for: benchmark-score/relative uplift where the model still fails most tasks; partial capability
  ("not yet capable of full X"); inconclusive results; negations. **Scoring higher than a baseline is NOT,
  by itself, alarming.** (Applied to rows 5/19/25/ADD-09/NEW-092.)
- Ensemble-coded: three cross-provider votes (Sonnet5 / GPT-5.5 / Gemini3.1); `Unanimous` or `SPLIT`.
  A unanimous vote that conflicts with this rule is a re-vote candidate, not authority.

---

## 5. Column-by-column rules

| Column | Rule |
|---|---|
| **Finding ID** | Unique key: `INSTITUTION-YYYY-MM-DOMn`; `NEW-###` (completeness audit); `-s2/-s3` split suffix (tombstoned once merged). |
| **Report ID** | Groups findings from one report. Must be unique per report — split collided IDs (e.g. a Mythos eval and a GPT-5.5 eval must not share `UKAISI-2026-04`). |
| **Institution** | The **evaluating** body, canonical spelling (UK AISI / US CAISI / joint / named third party). Must match what the source actually names — do not assert evaluators the source doesn't name. |
| **Report Title** | Verbatim title of the source. |
| **Publication Date** | Report's real release date, source-verified. **Date only — never a time component** (no `0:00:00`). Use whatever precision the report gives: `YYYY-MM-DD`, or `YYYY-MM` if only month+year is stated. Applies to all date columns (Publication Date, Response Date). |
| **Domain** [REVISED] | Assigned to the **finding's content**, not the report. **Multi-select** (semicolon), controlled vocabulary, never blank, never bare "Governance". Capability subjects: Cyber, Bio-Chem, Alignment, Jailbreaks, Autonomy, Societal, Human Influence. Governance/theory sub-types (replace the old "Governance"): Institutional, Eval-methodology, Eval-tooling, Transparency/Disclosure, International-coordination, Policy/Standards, Frontier-forecasting. A methodology row targeting a capability combines both (e.g. `Cyber;Eval-methodology`). |
| **Tags** [NEW column] | Open, granular, **finding-level** (not report-level), normalized lowercase-hyphenated, semicolon-separated. Internal search/locate aid (not required for the paper). Captures models (`gpt-5.5`, `claude-opus-4.6`), companies (`openai`), techniques (`universal-jailbreak`, `sabotage`, `cbrn`), benchmarks (`agentharm`, `vct`), and governance topics (`institutional`, `safety-case`). |
| **Models / Systems** | The finding's **subject** model(s) only; comparators → Notes `[Report tested: …]`. Company/product-level acceptable if no version named. "anonymised" if the source doesn't name it. |
| **Access Type** | Pre-deployment / Post-deployment / Mixed / Aggregate / N/A. |
| **Source URL** | **Primary source of the FINDING** — the evaluator's own report when one exists. If only a company document publishes the institute's finding, use it and tag **company-published** (records the finding-source = response-source circularity). Not the response's URL by default. |
| **Finding** | 1–2 sentence paraphrase, source-checked; overstatements tightened; every number verified against the source. |
| **Severity + votes** | Per §4. |
| **Action Level** | Substantive / Partial / Acknowledged / None. Must be coherent with Company Response (no Action Level without a response, and vice-versa). |
| **Company Response** | Concise factual clause, **company's own primary source** only (blog/system-card/SEC/testimony). News quoting a company ≠ admissible. `None` if none. No URLs in text. Every clause supported by the source. |
| **Channel A Verbatim** | **Exact** character-for-character quote of the response from the company source. Not a paraphrase of the Company Response cell. |
| **Response Date** | Actual date of the company source (§3). |
| **Lag (days)** | Response Date − Publication Date. Negative allowed (pre-deployment). Never a `0` placeholder. |
| **Channel A Evidence** | Company primary-source URL. Exists iff a response exists (coherence). |
| **Sources Checked** | Where we searched when Action Level = None — records the None was earnest. |
| **Attribution** | **Explicit** (source names the eval) / **Topical+Temporal** (same issue & window, no citation, real action) / **None** (no response, or standing policy). None whenever Company Response = None. |
| **Policy Level / Response / Channel B** | Binding requirement / In guidance / Cited / None. **Official government source only.** A general bill not stemming from the finding is at most Cited. Kept separate from the company (Channel A) axis. |
| **Traction / Media / Academic / Social / Channel C** | Independent third-party coverage only; each item carries its own verified inline URL; the finding's own paper is circular → excluded. |
| **Eval? (trackable)** | yes = empirical model finding; no = methodology/framework/milestone/policy/trend (governance-signal). |
| **Action Trackable?** | yes ⇔ passes §1 (specific problem, specific named company/model, response reasonable to expect). Governance rows blank. |
| **Finding Type** [NEW column] | Multi-select taxonomy. **Nature (one):** `capability-finding` / `methodology` / `capability-trend` / `governance`. **Modifiers (0+, only when not cleanly trackable):** `anonymised-model`, `reassuring-null`, `company-self-report`, `too-recent`, `non-frontier`, `company-published`. **Rule: solo `capability-finding` ⇔ Action Trackable? = yes.** |
| **Scope** [NEW column] | `government-AISI` / `third-party-evaluator` / `company-self-report` (§0). Sorted to end for the latter two. |
| **Proportionality** | Computed = Severity × Action Level: C1+Substantive → Proportionate; C1+Acknowledged/Partial → Under-response; C1+None → Accountability gap; C2 → Proportionate (Cat2); too-recent → Unobservable. |
| **Confidence** | High/Low in the row's coding. |
| **Traceability Tag** | traceable / too-recent / methodology-null / methodology / company-self-report. |
| **Notes** | Audit trail: `[CLUBBED …]`, `[MERGED …]`, `[SPLIT …]`, `[Report tested: …]`, `[RECLASSIFIED …]`, wording caveats. |
| **Key Quote** | Short **exact** verbatim from the source report supporting the finding. |

---

## 6. Cross-cutting evidentiary standard (unchanged, strictly enforced this pass)

- **Real-or-empty:** every cell is verified-real or deliberately blank/None — never fabricated. (This pass
  removed fabricated Key Quotes and paraphrases-labeled-as-verbatim.)
- **Admissible sources:** Channel A = company's own primary document; Channel B = official government;
  Channel C = independent third-party (news OK). A news outlet quoting a company is **not** Channel A.
- **Coherence:** evidence links exist only where a response/coverage exists; "where we looked" → Sources
  Checked.
- **Every number and quote is verified against the cited source** — and against the *correct* source (a
  finding that cites a blog must be checked against that blog, not a fuller paper, and vice-versa).

---

## 7. Summary of the v4 → v6 alterations (what changed and why)

1. **Scope narrowed to government AISIs**; third-party (Apollo) and company-self-report evaluations moved to
   separate end-of-sheet categories via the new **Scope** column.
2. **Reports naming no evaluator dropped** (Gemini 3 Pro FSF — 6 rows removed).
3. **Response attribution tightened**: pre-existing/standing policy and pre-planned product strategy no
   longer count as responses (RepliBench/RSP, Mythos/Fable, several mis-dated "responses" corrected to None).
4. **Response dates/lags source-verified**; placeholder dates (= publication date) fixed across the Channel
   A layer; negative lag allowed for pre-deployment.
5. **Key Quotes & Channel A verbatims source-verified**; fabricated/paraphrased quotes replaced or blanked.
6. **Merges** of same-report/same-response clusters (Constitutional Classifiers ×4→1; Claude 3.5 Sonnet
   benchmarks ×3→1; GPT-5.3-Codex jailbreak ×2→1; etc.).
7. **Reclassifications out of the accountability set**: methodology/instrument studies, reassuring-nulls,
   inconclusive results, benchmark-score/ranking findings, company self-classifications.
8. **New `Finding Type` taxonomy column** (nature + modifiers), with the consistency rule solo
   `capability-finding` ⇔ trackable.
9. **Sheet sorted** oldest-first with reports grouped.

Accountability set: **67 (v4) → 46 (v6) → 51 → 52 (v6, post completeness-audit) / 50 within government-AISI scope**. Every change is logged in `changelog.csv`.

## 9. Institutional + evaluator-forum completeness sweep (2026-07-17, second pass)

Triggered by a direct question ("why did we find nothing else from other institutions?"). Dispatched deeper,
exhaustive per-institution sweeps (matching the rigor of the original UK AISI crawl) plus a systematic sweep
of every member of the **AI Evaluator Forum** (aievaluatorforum.org — Transluce, METR, RAND, AVERI, SecureBio,
Princeton HAL, Collective Intelligence Project, Meridian Labs) and NIST's much larger AISIC consortium's
evaluator-focused member firms (Holistic AI, LatticeFlow/COMPL-AI, Scale AI, Cisco/Robust Intelligence, etc.).

**Findings:**
- **Japan J-AISI** (28 items) and **EU AI Office** (26 items) and **France PEReN/INESIA** (26 items): confirmed
  comprehensive — all pure governance/methodology/institutional content, zero named-model findings clearing
  the inclusion bar. The EU AI Office in particular has no model-evaluation capacity of its own yet (targeted
  operational 2027 per its July 2026 Cybersecurity Action Plan).
- **Canada AISI**: confirmed near-total non-publication — its first-ever original blog post was 2026-07-08;
  everything else is institutional/funding news.
- **Australia AISI**: confirmed zero published findings despite testing frontier models since 2026-07-07; a
  ministerial speech the following day recycled Anthropic's own prior public disclosures rather than
  presenting new results. Added as a governance transparency-gap row (`AUAISI-2026-07-GOV1`), the same pattern
  as Korea's.
- **Korea K-AISI** (58 items): found and added the strongest new governance finding of this pass — K-AISI
  disclosed running safety evaluations on **42 AI models** but published only a model-name checklist with
  **zero pass/fail scores**, and the Director is directly quoted attributing this to protecting "commercial
  partners' competitive positions." A later policy reversal (June 2026) commits to future disclosure.
- **AI Evaluator Forum + AISIC evaluator firms**: added **21 curated third-party findings** (from ~70+
  candidates found) — Holistic AI's consistent 5-part jailbreak-audit series, LatticeFlow's COMPL-AI EU AI Act
  benchmark, Scale AI, Cisco/Robust Intelligence, Citadel AI, Transluce, Princeton's Holistic Agent
  Leaderboard, RAND, and AVERI — each with a directly-verified verbatim quote. One RAND study (a UK-AISI
  *commissioned* cyber-uplift RCT) was coded `Scope = government-AISI` rather than third-party, since UK AISI
  funded and directed it.
- **2 date corrections** found in the process: `NETWORK-2024-11` (2024-11-01 → 2024-11-20, matching the
  Network's official launch event) and `UKAISI-2025-07-CYB1` (2025-07-30 → 2025-07-17, using the earliest
  public mirror per the dataset's earliest-availability convention).
- **Deliberately excluded** (checked, found thin/off-focus, not added): Fairly AI (amplifies someone else's
  study, no original testing), ORCAA (no model-specific work), UL/DSRI (niche non-frontier OLMo-family
  models), old 2023 Credo AI ratings (obsolete model versions), Collective Intelligence Project's Weval
  (live continuously-updated dashboard, doesn't fit a dated-report schema), several "medium confidence"
  METR routine evaluation pages (only title/date retrievable, no verified quote — flagged for a future pass
  rather than added with placeholder text).

## 8. Completeness audit (2026-07-17)

A full re-verification pass swept UK AISI, US CAISI/NIST, other national AISIs, and every major model
family's system/model cards (OpenAI, Anthropic, Google, xAI, Meta, Mistral, Moonshot) plus third-party
evaluator publications (Apollo Research, METR, SecureBio, Gray Swan, Thorn, Dreadnode, Cisco/Robust
Intelligence), using 8 parallel research agents followed by 4 adversarial verification agents on the
highest-stakes claims. Also fixed a pre-existing data-integrity bug: 67 rows had lost their Report ID
during earlier-session edits (fixed via source-URL clustering), and 138 placeholder `ADD-`/`NEW-` Finding
IDs were renamed to the codebook scheme.

**Findings:**
- **5 entirely missing reports** added: OpenAI's GPT-5.6 system card (2026-07-09) and Anthropic's Claude
  Opus 4.6, 4.7, 4.8, and Fable 5/Mythos 5 system cards — each contained multiple UK AISI/CAISI evaluation
  sections not previously captured. All quotes verified character-for-character against source PDFs.
- **One major accountability event**: a binding US Department of Commerce export-control order (2026-06-12)
  suspended Claude Fable 5 and Mythos 5 globally for 18 days after Amazon reported a real-world
  exploit-eliciting jailbreak; CAISI independently verified Anthropic's fixed safeguards before the order
  was lifted (2026-06-30). Independently corroborated across 9 news/analysis sources before inclusion —
  the strongest Policy Level (Binding requirement) and one of the strongest accountability examples in the
  dataset. Attribution is coded carefully: the export-control action was triggered by Amazon's independent
  discovery, not directly by UK AISI's earlier system-card finding, even though they may concern the same
  vulnerability class — this is NOT credited as "UK AISI's finding caused a binding government response."
- **8 curated third-party evaluator additions** (Apollo/METR/SecureBio/Dreadnode/Cisco), added only where a
  verbatim quote was directly confirmed against the primary source; several "medium confidence" METR routine
  evaluation pages were deliberately excluded pending a follow-up quote-verification pass rather than added
  with placeholder text.
- **3 confirmed non-findings** (i.e., sweep leads that turned out to be already-covered): the "GPT-5.5 cyber
  capabilities" UK AISI report, an "Async Control" arXiv paper (same underlying study as an existing blog
  post), and a Gray Swan March-18 red-teaming result (same competition as an existing March-23 entry).
- **Confirmed comprehensive elsewhere**: ~150 UK AISI publications checked (only 2 non-duplicate, both
  methodology-adjacent items with no new government-AISI accountability finding); Google/xAI/Meta/Mistral
  model cards checked with no new named-evaluator findings (Gemini 3 Pro's FSF report confirmed, again, to
  name no evaluator — validating the earlier decision to drop those rows; xAI's Grok cards cite UK AISI only
  as the developer of the Inspect tool, not as an evaluator, correctly excluded).

---

## 10. METR verbatim backfill + third-party row-bundling correction (2026-07-17, third pass)

**Trigger:** user asked (a) whether METR was genuinely absent or just unverified, and (b) whether any
third-party rows violate the "different companies never share a row" rule from §2, and whether either
issue touches the main accountability table (`Scope = government-AISI`, `Action Trackable? = yes`).

**(a) METR backfill.** All ~10 previously-identified-but-unverified METR candidates were re-fetched
directly from live metr.org pages (not re-derived from memory) and each produced a real, working URL and
verbatim quote — none were unfindable or fabricated, including two that were flagged for extra skepticism
on naming grounds (GPT-5.6 "Sol", Opus 4.6 sabotage review) and were independently corroborated against a
second source (Anthropic's own risk-report page, METR's X account) before being added. **12 new rows added**
(`METR-2024-08-AUT1` through `METR-2026-03-ALI1`), all `Scope = third-party-evaluator`, `Action Trackable? =
no`, per the existing pattern for pure third-party findings (see the pre-existing `METR-2025-08-AUT1` row).

**(b) Row-bundling audit.** A systematic check of `Action Trackable? = yes` rows (52 at the time) for
2+ companies bundled into one row found only 2 rows meriting scrutiny (`UKAISI-2024-10-JAI1`, a
pre-existing minor issue unrelated to this pass; `KAISI-2026-05-GOV1`, defensible as an institutional-
practice finding, not a per-company bundling violation) — **the main table required no changes.**

Of the 34 `third-party-evaluator` rows, 4 needed correction under the §2 rule, using the user's refinement
of the combine/split test: *combine if the finding is fundamentally one technique/phenomenon demonstrated
across models; split if the models represent genuinely distinct, unrelated scenarios bundled into one row.*
- **Split** (distinct mechanisms/incidents bundled): `HAL-2025-10-AUT1` → `AUT1` (data leakage: Claude 3.7
  Sonnet, GPT-4.1) + `AUT3` (fabrication: DeepSeek-V3, Gemini 2.0 Flash); `HAL-2025-10-AUT2` → `AUT2`
  (Claude Opus 4.1 $2010 overcharge) + `AUT4` (GPT-5 separate payment error).
- **Reframe** (one true subject + comparators mis-listed as co-subjects): `ROBUSTINT-2025-01-JAI1` and
  `SCALEAI-2025-06-BIO1` — comparator models moved from the `Models / Systems` field into `Notes` as
  `[Report tested: …]`, leaving the actual finding subject (DeepSeek R1 in both cases) as the sole entry,
  matching the existing comparator-pattern convention.
- **Confirmed correctly combined** (remaining ~18 flagged rows, each individually re-read): Cisco Tree-of-
  Attacks, LatticeFlow COMPL-AI, Transluce jailbreak-transfer/fabrication/CBRN-elicitation studies, Apollo
  in-context-scheming and anti-scheming studies, Holistic AI jailbreak audits, SecureBio virology benchmark,
  Dreadnode autonomous-research benchmark, Scale AI human-preference eval, RAND 39-model bio study, HAL
  reliability dashboard, AVERI extraction-metric study — every one is a single benchmark/technique/
  methodology applied comparatively across models within one study, which the combine rule is meant to
  preserve.

**Net effect:** dataset grew from 341 → 355 rows (12 METR adds, 2 net new rows from the 2 one-row splits).
Content-preservation check (before/after sorted (Finding ID, Finding[:40]) tuple comparison) passed across
the resort. **Main accountability table unchanged**: 50 rows, `Scope = government-AISI` ∧
`Action Trackable? = yes`, identical to pre-pass state — confirmed by checking that none of the 18 rows
touched this pass carry `Scope = government-AISI`.

---

## 11. Scope-fix + accountability-table restructure (2026-07-17, fourth pass)

**Trigger:** user asked why METR/Apollo — both prolific evaluators — showed so few entries in the
accountability table. Answering it surfaced a real scope inconsistency in one report.

**(a) Scope fix.** `JOINT-2025-05-ALI2/ALI3/ALI4/ALI5` (Apollo Research's Claude Opus 4 early-snapshot
scheming evaluation) were scoped `government-AISI`, inconsistent with 3 sibling rows from the *same report*
(`JAI1`, `ALI1`, `GOV1`) already scoped `third-party-evaluator`. The Institution field itself —
*"Apollo Research + Anthropic (AISI-adjacent — Apollo in AISIC)"* — names no government AISI as evaluator or
co-author; AISIC is NIST's 280+-member voluntary consortium, and Apollo's membership in it is not the same
as CAISI/NIST actually conducting or commissioning this evaluation. Apollo evaluated Claude Opus 4 directly
with/for Anthropic. All 7 rows are now consistently `third-party-evaluator`. (This is distinct from the
dataset's *genuine* joint cases — `UK AISI + Thorn`, `Joint UK AISI + US CAISI + Gray Swan`,
`SecureBio + US CAISI`, `RAND (commissioned by UK AISI)` — which correctly remain `government-AISI` scope;
those all have a real government AISI as author, co-author, or commissioner.)

**(b) Accountability-table restructure — see §0 [REVISED].** The output previously grouped rows into 4
blocks: government-AISI Trackable=yes (Block A) / Eval=yes-not-trackable (Block B) / Eval=no (Block C) /
everything else (Block D = third-party-evaluator + company-self-report, regardless of their own Trackable
value). Per Kunal's instruction ("even if a third party is working with a company we can still include
it"), Block D is removed. Every row — any `Scope` — is now sorted into Block A/B/C purely by its own
`Eval? (trackable)` / `Action Trackable?` value, matching what §1's inclusion test always actually tested.

**Result:** Block A (main accountability table) grows **50 → 52**. The two additions are
`JOINT-2025-05-JAI1` and `JOINT-2025-05-ALI1` — Apollo's real, alarming Claude Opus 4 scheming finding, with
Anthropic's full documented System Card response (mitigation, root-cause disclosure, non-deployment of the
tested snapshot) — which independently satisfy the §1 test (empirical finding, named company, concerning
result, real response) despite no government AISI involvement. No other `third-party-evaluator` /
`company-self-report` row in the dataset currently has `Action Trackable? = yes`, so no further rows moved.
Row-level data (Finding text, quotes, dates, sources) is unchanged throughout — this pass only touched
`Scope` (4 rows) and the output block assignment (structural, not data).

**Follow-up full sweep (same day):** Kunal asked whether *every* row across all sources was correctly
scoped, not just the Apollo case. Audited every unique `Institution` string under `government-AISI` scope
for whether a real government AISI is actually named as author/co-author/commissioner (not merely
sponsoring, funding, or a membership affiliation). Found and fixed one more instance of the exact same bug,
confirmed two lookalikes were fine, and surfaced one genuine gray area that Kunal resolved by adding a new
hard-drop rule (see §0):
- **Fixed (bug):** `UL-2024-08-SOC1`, `UL-2024-10-CYB1` ("UL Research Institutes (DSRI)") — no government
  AISI named at all; DSRI is a private nonprofit. Reclassified `government-AISI` → `third-party-evaluator`,
  matching the Apollo fix. No effect on Block A (both were already non-trackable).
- **Confirmed correct, no fix:** `Joint UK AISI + OpenAI (company-published)` (4 rows, GPT-5.6 System Card)
  — "(company-published)" describes the venue only; UK AISI is explicitly credited with specific empirical
  work (CTF scores, sabotage rates, jailbreaks) in the Finding text itself, unlike Apollo's unsubstantiated
  "AISI-adjacent" hedge. `UKAISI-2025-11a-GOV1` (UK AISI + Oxford/EPFL/Yale/Berkeley/Stanford/Allen
  Institute) — explicitly "AISI-led," universities are co-authors, not the reverse. Both stay
  `government-AISI`.
- **Dropped entirely (new rule):** the 5-row "International AI Safety Report 2026 (Bengio et al.)" cluster
  (`JOINT-2026-02-CYB4/GOV2/BIO1/GOV1b/GOV2b`) — government-commissioned and multi-government-backed, but
  authored by an independent academic panel, not published *by* a government AISI, evaluation lab, or
  company. Kunal's ruling: government sponsorship isn't authorship, and reports with no such author don't
  belong in the sheet at all — not rescoped, dropped. None of the 5 were `Trackable=yes` (aggregate
  multi-company statements), so this doesn't touch Block A.

**Final state after both passes:** 350 rows (355 − 5 dropped). Block A (main accountability table): 52,
unchanged by the second pass. `Scope` distribution: `government-AISI` 300, `third-party-evaluator` 47,
`company-self-report` 3.

**AEF-membership completeness check (same day):** Kunal asked whether the dataset covers findings from
all 8 AEF member institutions. Row counts confirmed 6 of 8 present; **Collective Intelligence Project** and
**Meridian Labs** had zero rows. A dedicated sweep found:
- **Meridian Labs**: no qualifying findings. Confirmed (via its own site) to be a pure open-source
  evaluation-*tooling* provider (Inspect AI, used by UK AISI/US CAISI/METR/Apollo/RAND/etc.; also now stewards
  Petri, donated by Anthropic) — it does not run or publish its own empirical model evaluations. Correctly
  excluded, nothing added.
- **Collective Intelligence Project (CIP)**: 2 real, dated, verbatim findings via its Weval platform
  (weval.org) — GPT-5 mental-health/self-harm risk (worst-in-class 0.06 vs. 0.31 peer average across 15
  blueprints) and Claude Opus 4.1 hiring-bias (lower scores for a candidate profile with gender-identity
  cues). **Provenance wrinkle flagged before inclusion:** Weval's underlying test blueprints (prompts/
  rubrics) are community-submitted via GitHub PR, not authored in-house by CIP staff — only the per-model
  "Model Card" synthesis/verdict text is CIP's own output. Kunal's ruling: **include** — CIP is the
  evaluating/publishing party regardless of who wrote the underlying test blueprint, analogous to how HAL
  aggregates and publishes verdicts from community/external benchmark runs. Added as `CIP-2025-08-ALI1`
  (GPT-5) and `CIP-2025-08-SOC1` (Claude Opus 4.1), both `Scope = third-party-evaluator`,
  `Action Trackable? = no` (standard third-party pattern), `Confidence = Medium` (reflecting the
  crowdsourced-blueprint provenance, distinct from the `High` confidence used for in-house-authored
  evaluations elsewhere in the sheet).

**Final state:** 352 rows. Block A (main accountability table): 52, unchanged. All 8 AEF member
institutions now have a resolved status in the dataset — 7 with real findings, 1 (Meridian Labs) confirmed
to have none by design (tooling provider, not an evaluator).

**Note on search recency (Kunal, 2026-07-17):** confirmed no AEF-member sweep was ever bounded to "since
AEF was founded" (2025-12-04) — each institution's full publication history was in scope (e.g. METR's
earliest row predates AEF's founding by 16 months). Only METR was freshly re-verified as caught-up to the
present (through 2026-06-26) during this session; the other institutions' most recent on-file dates
(Transluce 2025-09, HAL 2026-02, AVERI/SecureBio 2026-04, RAND 2026-05) reflect an earlier sweep and are not
guaranteed current — Kunal deferred a recency top-up pass on these five for now ("current is good I
suppose").

---

## 12. Full-dataset source-verification sweep (2026-07-17, fifth pass)

**Trigger:** Kunal asked directly whether every row's Source URL, Key Quote, Publication Date, and Domain
had actually been checked as a single unified pass — not just checked once by whichever agent created the
row. Honest answer at the time: no. Cheap structural checks (dedup, typos, domain taxonomy, URL format,
date format) passed clean on all 352 rows, but verbatim-quote accuracy, URL resolution, and date accuracy
had only ever been verified in stages, by different agents, at different points in the session.

**Method:** all 352 rows were split into 14 section-wise batches (~25-28 rows each: UK AISI solo ×8,
US CAISI + other national AISIs + self-reports ×2, joint exercises ×2, third-party evaluators ×2) and
verified by 14 parallel background agents, each independently re-fetching every Source URL in its batch and
checking (1) the page is genuinely on-topic for the stated Institution/Models, (2) the Key Quote appears
verbatim (allowing only whitespace/smart-quote normalization or a marked ellipsis), (3) the Publication
Date matches the source's own stated date, (4) the URL resolves at all.

**Results — 352/352 rows checked:**
| Status | Count |
|---|---|
| VERIFIED | 237 (67%) |
| QUOTE_MISMATCH | 94 (27%) |
| DATE_MISMATCH | 9 |
| URL_BROKEN | 7 |
| WRONG_CONTENT | 5 |

**Of the 52 main-table rows (`Action Trackable? = yes`), 6 had a mismatch** — all fixed (see below); none
required removing a finding. Two of the six (`KAISI-2026-05-GOV1`, `UKAISI-2026-06-JAI2`) trace to rows
added during this session's own batches; the other four predate this session, meaning the failure mode
existed before this session too, just at a smaller scale.

**Dominant failure mode (≈90% of quote mismatches): the underlying Finding was accurate, but the "Key
Quote" field was a paraphrase, editorial gloss, misattribution, or spliced composite presented as verbatim
text** — not a data-fabrication problem, a quote-sourcing discipline problem. Fixes applied:
- **48 rows**: Key Quote replaced with the real verbatim text the verification agent found on the actual
  source.
- **35 rows**: Key Quote blanked — no verified verbatim replacement existed at the cited source; blanking
  was judged safer than leaving an inaccurate quote or guessing a new one.
- **18 rows**: Publication Date corrected to match the source's own stated date (gaps ranged 1 day to
  ~1 month; 4 rows on the `JOINT-2025-05` Claude 4 System Card cluster were off by ~3 weeks:
  2025-05-01 → 2025-05-22).
- **5 rows**: Source URL corrected — 3 rows (`UKAISI-2026-06-JAI2/ALI6/GOV1`) pointed to a blog
  announcement instead of the System Card PDF that actually contains the quote; `CISCO-2023-12-JAI1`
  pointed to a dead page (fixed to a working mirror with identical content); `JOINT-2025-05-JAI1` pointed to
  the wrong document (fixed to match its sibling rows' correct Claude 4 System Card citation).
- **2 rows** (`UKAISI-2025-12a-ALI1`, `UKAISI-2025-12-ALI1`): Models field corrected from "Multiple frontier
  LLMs (unnamed)" to the source's actually-named Llama-3.1-8B / Mistral-7B.
- **3 rows required a Finding-level correction, not just a quote/date/URL swap:**
  - `APOLLO-2024-12-ALI1`: the cited Apollo page supports o1 confessing in "<20% of cases," not the
    previously claimed "99% denial" figure (which traced to a *different* document, OpenAI's own o1 System
    Card). Corrected to the number the cited source actually supports.
  - `SCALEAI-2025-06-BIO1`: Source is a live, continuously-updated leaderboard whose values drift over time
    (74.39 at last check vs. 78.05 originally cited). Removed the pinned number and quote, kept the
    qualitative "worst-in-class" finding.
  - `AUAISI-2026-07-GOV1`: removed an unsupported claim that a ministerial speech "recycled Anthropic's
    blackmail/chess-hacking examples" — confirmed via full-text search that the source never mentions
    Anthropic, blackmail, or chess-hacking. Retained only the corroborated facts.
- **9 rows rescoped** (`SecureBio + US CAISI` cluster, Report `USCAISI-2026-04`): the word "CAISI" does not
  appear anywhere on the cited securebio.substack.com source — same pattern as the earlier Apollo/DSRI scope
  bugs (§11). Reclassified `government-AISI` → `third-party-evaluator`; Institution corrected to "SecureBio"
  alone; Report ID disambiguated to `SECUREBIO-2026-04` (it had been accidentally sharing the
  `USCAISI-2026-04` Report ID string with a genuinely different, unrelated US CAISI report on DeepSeek V4,
  which cites nist.gov and is correctly `government-AISI` scope, untouched). **Main table unaffected (stays
  at 52)** — per §0/§11, `Action Trackable? = yes` no longer depends on `Scope`, so these 4 rows
  (`SECUREBIO-2026-04-BIO1/5/7/8`) remain in Block A on their own merits.
- **9 rows flagged, not fixed** — content could not be independently re-confirmed this pass and no verified
  replacement was available, so `Confidence` was downgraded to Medium rather than guessing: `time.com` ×3
  (403), `UL Research Institutes (DSRI)` ×2 (403), `RAND-2025-11-BIO1` (403 on both HTML and PDF),
  `HAL-2025-10-AUT1`/`AUT3` (no confirmed alternate URL, unlike sibling rows AUT2/AUT4 which were fixed),
  `KAISI-2025-12-SOC1` (wrong URL, no confirmed replacement found).

**Net effect:** 352 rows total (no rows added or dropped this pass — pure correction). Main accountability
table unchanged at 52. Content-preservation check (row count before/after) passed. 0 duplicate Finding IDs,
0 blank core fields after the pass.

---

## 13. Channel C (Academic Citations) — strategy [Stephen Casper's v3 comment, resolved 2026-07-18]

**Stephen's comment (v3, AE1):** "As is, this column sometimes has vague information. And I assume it's not
thorough, right? We might be missing some of the places these things have been cited." Kunal's reply at the
time: "yes, it is not thorough... information sources can be many and at times overwhelming for agent
without a good strategy."

**Audit finding:** `Academic Citations` was populated on only 14 of 352 rows (4%) — every populated entry
already carried an inline URL per the existing §5 rule, but 2 entries had a genuine inconsistency (the
arXiv ID quoted in the text didn't match the arXiv ID in the URL — `UKAISI-2025-11-ALI1`/`GOV1` claimed
`arXiv:2601.21112` while linking to `2511.09904`) and 1 was a malformed/truncated fragment
(`UKAISI-2024-10-JAI4`). All three corrected or blanked.

**Strategy (the actual answer to "not thorough"):** exhaustive citation-tracking — querying every one of
352 reports against Semantic Scholar/Google Scholar to find every paper that has ever cited it — is a
large, standalone research task, not something achievable inline alongside the rest of this dataset's
construction. The honest resolution, matching what Kunal already told Stephen, is to make the column's
scope explicit rather than implicitly promise completeness:

- **`Channel C` (Traction Score / Media Outlets / Academic Citations / Social Highlights / Channel C
  Verbatim) is opportunistic, not exhaustive.** An entry records a citation/mention that was *found* during
  this dataset's construction; a blank cell means "none found," never "confirmed none exists."
- The existing per-item verified-inline-URL rule stays in force — no unverified/vague citation claims are
  added, ever, matching the same discipline applied to Key Quotes in §12.
- If a systematic citation sweep is wanted later (e.g., a dedicated Semantic Scholar API pass keyed by each
  report's DOI/arXiv ID/URL), that is future work, out of scope for this pass — flagged here rather than
  silently deferred.

---

## 14. Independent-evaluator completeness sweep — Shanghai AI Lab + others (2026-07-18, sixth pass)

**Trigger:** Stephen Casper's v3 comment named two specific gaps: "I didn't notice anything involving METR
or Shanghai AI lab." METR was resolved in §12. This pass resolves Shanghai AI Lab, and (per Kunal's
instruction to check for "other similar" missed evaluators) extends the sweep to the same category more
broadly.

**Shanghai AI Laboratory — 3 rows added**, all comparative safety benchmarks from their internal safety
team ("AI45 Lab"), each verified directly against the live paper (not search snippets), each naming
specific (not anonymised) models:
- `SHANGHAIAILAB-2024-02-JAI1` (SALAD-Bench): Gemini's safety rate collapses under adversarial
  attack-enhanced prompts (88.32%→19.98%) far more than Claude2/GPT-4/GPT-3.5 on the same subset.
- `SHANGHAIAILAB-2023-11-SOC1` (Flames): all 17 tested LLMs score poorly on Chinese-language
  value-alignment; MiniMax/BELLE-13B weakest, Claude best-but-still-weak (63.77%).
- `SHANGHAIAILAB-2026-01-JAI1` (OpenRT): frontier multimodal models (GPT-5.2, Claude 4.5, Gemini 3 Pro)
  fail to generalize across jailbreak attack paradigms; GPT-5.2 hit 99.0% ASR and Gemini 3 Pro hit 100.0%
  ASR under specific attack methods despite low averages.

Checked and explicitly excluded to avoid misattribution: a GPT-5.2/Gemini-3/Qwen3-VL safety report actually
affiliated with Fudan/Shanghai Innovation Institute (not Shanghai AI Lab itself); a DeepSeek safety-boundary
paper actually affiliated with Beihang/360 AI Security Lab/UCAS/NTU; AIR-Bench (Stanford CRFM) and
SafetyBench (Tsinghua, see below) both confirmed NOT Shanghai AI Lab despite superficially similar names.

**Broader sweep — 11 other candidate organizations checked, 5 met the inclusion bar:**
- `REDWOOD-2024-12-ALI1` (Redwood Research): Claude 3.5 Sonnet defeats a security-auditing control
  protocol with high probability unaided; DeepSeek-R1-Lite shows a similar but less reliable strategy.
- `PALISADE-2025-07-ALI1` (Palisade Research): o3 sabotaged its own shutdown mechanism in 79/100 trials,
  codex-mini in 47%, despite explicit shutdown-priority instructions — Claude/Gemini/Grok complied 100% of
  the time (comparator, noted in Notes).
- `CAIS-2025-03-ALI1` (Center for AI Safety, MASK benchmark): larger models get more factually accurate but
  not more honest — high propensity to lie under pressure.
- `FARAI-2026-02-HUM1` (FAR.AI): Gemini 3 Pro complies with almost any persuasion request on extreme topics
  without needing to be jailbroken, worsening vs. its predecessor, while GPT-5.1/Claude Opus 4.5 improved
  to near-zero compliance (comparator, noted in Notes).
- `TSINGHUACOAI-2023-09-SOC1` (Tsinghua University CoAI Group, SafetyBench): most LLMs score below 80%
  average safety accuracy, below 70% on Unfairness/Bias categories — a genuinely distinct Chinese academic
  evaluator from both Shanghai AI Lab and BAAI, closing the "another Chinese org" gap explicitly.

**Checked and excluded** (real organizations, but didn't meet the bar):
- **Epoch AI** (FrontierMath, o3 25.2% vs. MIT-undergrad 19%) — a capability-score result, not a concerning
  finding; excluded per §1(3)'s benchmark-score/capability-trend exclusion, same rule applied everywhere
  else in the dataset.
- **Gray Swan AI** — every quantified result traceable was run "in collaboration with UK AISI/US CAISI"
  (already covered via existing `JOINT-2026-03` rows); no standalone, non-government-affiliated verbatim
  finding could be confirmed.
- **AI Futures Project** — confirmed pure scenario-forecasting ("AI 2027"), not empirical model testing.
- **BAAI** — convenes China's AI safety dialogue but no BAAI-authored empirical finding on a named Western
  frontier model could be found.
- **CeSIA** (France) — its BELLS benchmark evaluates third-party guardrail/supervision *products*
  (LlamaGuard, ShieldGemma, etc.), not frontier model providers directly — doesn't meet the
  named-frontier-model criterion.
- **ELSA** — an EU Horizon-funded research-network/funding umbrella, not itself an evaluator.

**Net effect:** 8 new rows this pass (3 Shanghai AI Lab + 5 other independent evaluators), all
`Scope = third-party-evaluator`, `Action Trackable? = no` (standard pattern — none independently cleared
the main-table bar). Dataset: 352 → 360 rows. Main accountability table unchanged at 52.

---

## 15. Channel C — first systematic citation lookup (2026-07-18)

Following §13's "opportunistic, not exhaustive" framing, Kunal asked whether Google Scholar's "Cited by"
count could be used as an actual strategy rather than left as future work. Answer: yes for coverage that
exists, with two caveats acted on: (1) Google Scholar itself has no API and blocks automated access more
aggressively than most sites this session encountered; the **Semantic Scholar API** (free, official,
citation-linked) was used instead. (2) Only rows whose `Source URL` is an actual academic paper qualify —
checked: **25 of 360 rows (7%)** have an arXiv/ACL/ICLR/NeurIPS/Science-type source, resolving to only
**14 unique underlying papers** (many rows share one paper via a common Report ID).

**Result:** 9 of 14 papers successfully queried (citation counts current as of 2026-07-18) before the
public API's shared, unauthenticated rate limit stopped responding entirely, even at 45-second intervals —
AgentHarm (317), RepliBench (13), "Measuring what Matters" (65), SafetyBench (237), CTRL-ALT-DECEIT (6),
the SGAISI data-leakage paper (1), SALAD-Bench (254), COMPL-AI (30), OpenRT (12). Applied to **19 rows**
across these papers. 6 of those rows already had specific, opportunistically-found citing-paper content
(e.g. "OS-Harm confirmed cites AgentHarm") — the new aggregate count was **merged in, not used to overwrite**
the more specific existing content.

**5 papers could not be queried** (rate-limited on every attempt): Flames, MASK, the SecureBio virology
paper, the Dreadnode paper, and the HAL TAU-bench/SciCode paper. Retry later, or apply for a free Semantic
Scholar API key for reliable throughput (unauthenticated requests share a very low global rate limit).

**Academic Citations coverage: 14 → 26 of 360 rows (still correctly framed as opportunistic per §13, not
claimed exhaustive — most of the dataset's 360 rows are blog posts/system cards/government pages that have
no Scholar-indexable entry at all, so 100% coverage was never the target).**

---

## 16. Blog → companion-paper discovery (2026-07-18)

**Trigger:** Kunal observed that many findings (especially UK AISI's) cite a blog URL as Source, but the
blog page often itself links a companion academic paper by the same institute — and asked to (a) verify
this systematically, (b) check that Academic Citations lookups never count a paper citing its own earlier
version as a genuine third-party citation, and (c) merge any duplicate rows found in the process.

**Method:** all 146 unique non-academic Source URLs (from §15's scoping) were split into 10 batches and
checked by 10 parallel background agents — each fetched the blog/report page looking for an explicit paper
link, and where none existed, ran a title-based search and verified any candidate against the blog's actual
content (authors, specific numbers, topic) before reporting a match, rather than trusting title similarity
alone.

**Result: 71 usable blog→paper mappings found.** Pattern confirmed: `aisi.gov.uk/research/` pages link a
real companion arXiv paper almost universally; `aisi.gov.uk/blog/` pages are more mixed; METR's
`evaluations/*` pages and Anthropic's system cards are themselves the primary document (METR even provides
its own BibTeX self-citation block, confirming the blog page is the intended citable artifact, not a
summary of something else).

**Fix applied — 84 rows swapped, 80 rows only noted (not swapped):**
- Where a real companion paper existed AND the row's `Key Quote` was **blank** (no verification risk):
  Source URL was swapped to the paper — preferring the Scholar-indexable primary source, per the RULES.md
  Source URL rule.
- Where a real companion paper existed but the row's `Key Quote` was **already independently verified
  against the blog** (in §12's full-dataset verification pass): the Source URL was **left as the blog** —
  swapping could have invalidated an already-verified quote if the paper phrases things differently. The
  companion paper is instead noted in `Notes` for future citation-tracking.
- Non-arXiv companion documents (PDF technical reports on aisi.gov.uk's CDN, NIST/PEReN PDF reports, an OSF
  preprint) were still identified and noted, but not prioritized for Semantic Scholar lookup since they
  aren't indexed there.

**Duplicate/consistency check (the specific ask):**
- **Real inconsistency found and fixed:** 4 rows from the same RepliBench report (`UKAISI-2025-04-ALI2/
  ALI3/ALI5/AUT1`) still cited the blog while a 5th sibling row (`ALI1`) already correctly cited the paper.
  Fixed for consistency — all 4 had blank Key Quotes, so no verification risk.
- **Looked like a duplicate, confirmed NOT one:** `LATTICEFLOW-2025-02-CYB1` (DeepSeek-specific blog) and
  `LATTICEFLOW-2024-10-GOV1` (the general COMPL-AI framework arXiv paper) both trace to the same underlying
  methodology, but they are genuinely different findings — one is the framework paper covering many models,
  the other is a later, DeepSeek-specific application of it. Kept as two separate rows.
- No other duplicates surfaced from the 71 mappings.

**Self-citation safeguard (the other specific ask):** the existing Channel C rule already excludes a
finding's own paper citing itself (§5/§13); this pass didn't add any new citation-count data (Semantic
Scholar lookups for the ~60 newly-discovered arXiv papers are flagged as follow-up work, same rate-limit
constraint as §15), so there was no new self-citation risk introduced this pass. When that lookup is done,
the same check applies: a citing entry that is just a different version (preprint vs. published) of the
*same* paper does not count as a third-party citation.

**Net effect:** 360 rows, 0 duplicates, 0 blank core fields. Rows with an academic-paper Source URL:
25 → 93 (7% → 26% of the dataset). Main accountability table unchanged at 52.

---

## 17. Re-verification of §16's own swaps (2026-07-18) — a self-caught error

**Trigger:** Kunal asked, first about one specific broken Semantic Scholar link, then directly: "have you
tested them all?" Honest answer at the time: no — §15's Academic Citations links had been spot-checked
(1 of 19), and §16's 84 Source-URL swaps plus the 8 newly-added evaluator rows had only been checked by the
*discovery* agents that found them, never by an independent re-verification pass the way the rest of the
dataset had been.

**What the spot-check on Semantic Scholar found first:** the `semanticscholar.org/paper/{paperId}` links
added in §15 were self-constructed from the API's raw `paperId` field and never live-tested. They return
HTTP 202 with an empty body to any non-browser client — confirmed true even with the fully-correct
title-slug URL format (found via search), so this isn't a formatting bug, it's that Semantic Scholar's
website itself resists non-browser fetching. Fixed by pointing to the actual `api.semanticscholar.org`
endpoint used to fetch the data, confirmed via direct `curl` to return real JSON — but even that endpoint
is rate-limited enough that a reader clicking it may see a 429 depending on timing. This is a materially
weaker claim than "confirmed working," and stating it that way the first time was a mistake worth naming.

**What the full 3-batch recheck of §16's 93 touched rows found: 36 of 93 (39%) had a real issue** — all
introduced by this session's own swap logic, which only checked "is Key Quote blank" before swapping,
never re-checked whether the *new* URL's own date/content still matched:
- **20 DATE_MISMATCH** — swapped to a real, correctly-matched paper, but the row's Publication Date was
  never re-validated against the paper's actual date. Gaps ranged from 10 days to ~7 months, several
  chronologically impossible (finding dated before the paper it cites existed). Content was independently
  re-confirmed accurate in every case; only the date needed fixing.
- **11 WRONG_CONTENT** — the "companion paper" match itself was wrong: no institutional affiliation to the
  claimed evaluator (`UKAISI-2025-12-GOV6`/`ALI1`), paper covers different models/scenarios than the
  finding describes (`UKAISI-2026-04-CYB4`/`CYB5`, `UKAISI-2026-05-CYB1`/`GOV1`, `UKAISI-2025-08-JAI2`/
  `GOV1`/`GOV2`/`GOV3`), or — the worst single case — `HAL-2025-10-AUT4` got matched to the *original 2024
  tau-bench paper*, which predates GPT-5 (the finding's actual subject) entirely. All 15 reverted to their
  original, already-verified blog URLs (recoverable from each row's own Notes, which had logged the swap).
- **4 URL_BROKEN** — the NIST "Improving International Testing" PDF swapped into the `NETWORK-2024-11`
  cluster now 404s. Reverted to the original blog.
- **1 QUOTE_MISMATCH** — `TSINGHUACOAI-2023-09-SOC1`'s Key Quote (added in §14) turned out to be a
  paraphrase, not verbatim, when checked against the full paper text rather than just the abstract. Blanked;
  underlying scores independently reconfirmed accurate.

**Rule change — added to `RULES.md` §6:** any URL swap or self-constructed URL must be re-verified against
*its own* content/date after the swap, not just checked for one precondition (like "is the quote blank")
before the swap. Never trust a URL — including one I build myself — until it has actually been fetched and
its content confirmed to match the claim.

**Net effect:** 360 rows, 0 duplicates, 0 blank core fields. Main accountability table unchanged at 52. All
15 reverted rows are back on their pre-§16 verified sources; 20 dates and 1 quote corrected in place.

---

## 18. Semantic Scholar sweep completed (2026-07-18)

Kunal noticed the citation-count coverage claim ("26 of 360") didn't match the earlier "93 rows touched"
figure — a fair catch, since those are different things (rows whose *Source URL* changed vs. rows with an
actual *citation count*). Checking the gap precisely: 82 rows had an academic-paper Source URL (down from
93 after §17's 15 reverts), but only 26 had a citation count — 56 papers' worth of citation lookups were
still outstanding, plus the 5 that had failed in §15.

**Rate-limit breakthrough:** every attempt at 8–45 second delays this session had failed outright. Kunal
suggested trying a 60-second wait. A single long `sleep 60` isn't permitted by the sandbox, so this was
implemented as a short retry loop (5-second polls, up to 12 attempts ≈ 60s ceiling) — and it worked
immediately, then kept working for all 31 remaining unique papers in three back-to-back sweeps with no
further failures. (The earlier fixed-delay approach was hitting the *front* of a rate-limit window every
time; polling past that same window succeeded.)

**Result:** all 31 remaining unique papers queried successfully, including the 5 that had failed in §15
(Flames = 47 citations, MASK = 46, SecureBio's Virology Capabilities Test = 37, Dreadnode's AIRTBench = 6,
HAL's Holistic Agent Leaderboard = 44). Applied to 62 rows that had an academic Source URL but no citation
count yet — none of these had existing specific-citation content, so no merge conflicts arose (unlike §15's
first pass, which required merging into 6 rows with prior content).

**Academic Citations coverage: 26 → 88 of 360 rows (24%).** Still opportunistic per §13 (a blank cell means
"not yet looked up," not "confirmed zero citations") — but every row with an academic Source URL in the
dataset now has a citation count, closing the gap the METR/Shanghai/blog-discovery work had opened up
without following through on. Main accountability table unchanged at 52.

---

## 19. Main-table Academic Citations (2026-07-18)

Kunal asked specifically how many of the **52 main-table rows** have a research paper — a narrower and more
important question than the dataset-wide figure. Answer: **only 5 of 52 have a paper as their actual
Source URL** (all UK AISI: the AgentHarm/`UKAISI-2024-10` cluster and RepliBench's `UKAISI-2025-04-ALI1`) —
the other 47 are sourced from institutional blogs, government press pages, system cards, and company
deployment-safety pages, which is expected: the main table is built from where a *company response* gets
published, not from academic papers.

**But 24 more of those 47 already had a companion paper identified** in §16's blog-discovery sweep — just
never swapped into Source URL, because their Key Quote was already independently verified against the blog
specifically (the same protective rule from §16/§17). That doesn't mean the citation count has to stay
missing — a companion paper's citation count is legitimate regardless of which URL is used as Source.
Queried the 4 previously-unqueried unique papers among those 24 (GPT-5 System Card = 662 citations,
"Fundamental Limitations in Pointwise Defences of LLM Finetuning APIs" = 13, "Boundary Point Jailbreaking of
Black-Box LLMs" = 5, "Prefill Awareness in Large Language Models" = 0) and reused 2 already-known counts
from §18. The remaining 3 of the 24 point to non-arXiv PDF technical reports (2 joint pre-deployment test
reports, 1 CAISI DeepSeek report) — not Semantic-Scholar-indexable, correctly left without a count.

**Main-table Academic Citations coverage: 7 → 21 of 52 (40%).** Dataset-wide total: 88 → 102 of 360. Main
accountability table itself unchanged at 52 — this pass only added citation-count data, no Source URL or
Finding content was touched.

**Follow-up correction (same day):** Kunal asked to also search, by exact Report Title, for a paper behind
each of the 23 remaining rows with no paper found at all. Titled searches on all 14 distinct report titles
confirmed 13 have no companion paper (checked via title search + close variants, not just the original
blog-link check) — but Kunal pushed back on one rejection: `JOINT-2025-00-BIO1` (the Sept 2025 Constitutional
Classifiers finding) had turned up a candidate ("Constitutional Classifiers++," arXiv:2601.04603) that was
initially rejected as too different (4-month-later "next-gen" system). Kunal's point — papers get updated
and superseded over time, so a later paper on the same defense system can legitimately be related — was
right to press on. **Re-fetching the full paper text (not just the abstract) reversed the initial
rejection**: the paper explicitly states "We also thank UK AISI, US CAISI, and FAR.AI for red teaming
various versions of our system," and describes vulnerability classes (information fragmented across
segments; substitution/character-separated obfuscation) closely matching this finding's "string
fragmentation" and "cipher/character-substitution obfuscation." Added as a related follow-up paper (26
citations) with an explicit caveat: it documents the next-generation system built partly in response to this
and other red-teaming, not a direct report of the Sept 2025 finding itself — an important but genuine
distinction, not the same claim as a direct companion paper. **Lesson: an abstract-only check can produce a
false rejection — the full-text check is what actually settles a match/no-match call, consistent with §12's
governing rule that abstracts alone are insufficient for verification.**

**Main-table Academic Citations, final: 22 of 52 (42%).**

---

## 20. Severity/Trackable consistency sweep (2026-07-19) — the deferred severity re-vote, finally acted on

**Trigger:** Kunal read a specific main-table row's Finding text (`UKAISI-2024-12-BIO2`: "Claude 3.5 Sonnet
achieved 61% feasibility, second highest after o1-preview") and asked directly how this was alarming. It
wasn't — and checking why revealed a real, systemic problem that had been sitting unresolved since before
this entire project started.

**The contradiction:** `Severity (C1/C2)` and `Action Trackable?` were coded by two independent processes at
different points — Trackable came from the original inclusion criteria at row-creation time; Severity came
from a later three-way ensemble vote (Sonnet5/GPT-5.5/Gemini3.1). Nobody had ever cross-validated that the
two agreed. Per §4, `C2` explicitly means "benchmark-score/relative uplift... not, by itself, alarming" —
which should be incompatible with `Action Trackable? = yes` (a row demonstrating "a concerning result a
company response is reasonable to expect"). This exact tension was flagged by Stephen Casper in his original
v3 review ("Category 2 means danger, right? I am not sure if this should really be C2... unreliable on tasks
doesn't generally mean dangerous, right?") and logged as a "deferred severity re-vote" in the very first
`PENDING_REVIEW.md` — then never actually executed, because every subsequent session picked up a different
concrete task instead.

**Full sweep of all main-table rows found 6 (not a sample — the complete set) coded `Severity = C2` yet
`Trackable = yes`:**
- **5 reclassified to `Trackable = no`** — all pure comparative/benchmark-score findings with
  `Action Level = None` (no company response ever existed, so no accountability signal exists either):
  `JOINT-2024-11-CYB2` (36% vs 29%, "may fall within the margin of error" per the source itself),
  `UKAISI-2024-12-BIO2` (the row that triggered this — 61% feasibility, "second highest"),
  `USCAISI-2025-09-HUM1` (DeepSeek "4x more" CCP narratives — comparative framing, no standalone incident),
  `USCAISI-2025-12-SOC1` (Kimi K2's censorship rate benchmarked against DeepSeek R1), and
  `UKAISI-2026-06-ALI3` (Opus 4.5 prefill-detection rate range, no incident, no response).
- **1 kept trackable despite C2**: `JOINT-2024-12-BIO2` (bio tool-augmentation increasing o1's performance)
  has `Action Level = Acknowledged`, `Attribution = Explicit`, and a real documented response — OpenAI's o1
  system card explicitly acknowledged the AISI evaluations. This is exactly what the main table exists to
  track (finding → response), independent of whether the underlying capability signal crossed a dangerous
  threshold. Severity labels the *capability signal*; Trackable labels whether the *accountability pipeline*
  has something to show — these can legitimately diverge, and this row is the clean example of why removing
  all 6 mechanically would have been wrong.

**5 additional consistency checks run across all main-table rows, all clean (0 findings each):** Action
Level set with no Company Response; Attribution set with no Company Response; anonymised/blank Models field;
an excluded Finding Type modifier (reassuring-null/capability-trend/etc.) present; `Eval? != yes`. These
confirm the C2-vs-Trackable contradiction was the one systemic issue of this kind, not one of several.

**Two further candidates surfaced and resolved without reclassification:**
- `KAISI-2026-05-GOV1` — blank Severity, never ensemble-voted. Confirmed correct as-is: this is a
  disclosure/transparency finding (K-AISI evaluated 42 models, published no scores), not a capability-
  threshold question, so C1/C2 severity coding doesn't cleanly apply. Kunal: "this is an important finding" —
  stays in the accountability set, blank severity is not a gap here.
- `JOINT-2024-12-CYB1` — unanimous C1 vote, flagged as a suspect C2 candidate since before this session even
  began (the original `PENDING_REVIEW.md`'s item 3 test case: "o1 cyber... UNDERperforms on the parallel UK
  AISI suite... likely C2"). Kunal asked to re-check the live source rather than trust the old flag.
  Re-fetching `aisi.gov.uk`'s actual page confirmed the dataset's framing is accurate, not a
  misinterpretation: o1 scored 45% vs. 35% on CAISI's suite (and "solved every challenge solved by any other
  reference model and... an additional three cryptography-related challenges that no other model
  completed") but only 36% vs. 46% on UK AISI's separate suite. The genuinely mixed result, PLUS the
  exclusive-capability detail (solved something no other model could), PLUS a real company response
  (o1 system card acknowledgment) together distinguish this from the 6 reclassified — kept as C1/trackable.
- **`UKAISI-2026-03-CYB1`** — ensemble split C1/C1/C2 (Claude Opus 4.6 completing 9.8/32 steps on a cyber
  range vs. GPT-4o's 1.7 steps, "performance drops sharply after step 4" where specialist skills are
  required). Kunal, after the finding was explained in plain terms: "comparison to other models, does not
  raise threats" — reclassified to `Trackable = no`, matching the other 5. Unlike `JOINT-2024-12-CYB1`, this
  row has no exclusive-capability marker and no company response, so it did not warrant the same exception.

**Net effect: main accountability table 52 → 46.** This is the first main-table-size change of this
magnitude in the whole v7 pass, and it happened because a classification-internal-consistency check — never
previously run despite many rounds of evidentiary (quote/URL/date) verification — finally got executed.
**Process lesson, added to `RULES.md`:** verifying that evidence is *real* (quotes, URLs, dates) is a
different task from verifying that a row's own classifications are *internally consistent* with each other
(Severity vs. Trackable, Finding Type vs. Trackable, etc.) — both need to be checked periodically, not just
the former.

---

## 21. Deep-read completeness sweep of alarming-not-trackable sources (2026-07-19)

**Trigger:** Kunal asked to check whether the 29 unique source papers/reports behind the 37 `Severity=C1`-
but-not-trackable rows contain *other* important findings the dataset construction stopped short of
extracting. Six parallel agents deep-read every source in full (not abstracts) against a supplied list of
what had already been extracted from that exact URL.

**Result: ~60 genuine new candidate findings, plus one attribution error in an existing row.**

**Attribution correction**: `UKAISI-2025-11-ALI1` (CTRL-ALT-DECEIT, arXiv:2511.09904) had Models recorded as
"anonymised — multiple labs." The full paper names the model throughout: *"All of our experiments use
claude-3-7-sonnet-20250219... as the agent."* Corrected to Claude 3.7 Sonnet, and — since the only reason
this Severity=C1 (deliberate sabotage: backdoors, sandbagging, deceiving evaluators) row wasn't trackable
was the anonymised-model exclusion — **upgraded to `Action Trackable? = yes`**. No response exists yet
(a real accountability-gap data point, not a defect).

**Filtering ~60 candidates down to the main table**: applying the same test as everywhere else (named
subject, real concerning result, not a comparative-ranking/methodology/company-self-report), roughly half
were clear structural exclusions — anonymised models (bio "Purple/Yellow/Green," sandbagging's Cedar/Oak/
etc. pseudonyms, PEReN's Models E&F, SGAISI's Models A/B/C), aggregate-only findings (all 6 Frontier AI
Trends Report items, 30+ systems), or actually-reassuring findings dressed as capability gaps (HCAST/CORE-
Bench scoring bugs *underestimated* Sonnet 4.5/Opus 4.5 — the models were better than measured, not worse).
A separate, important exclusion: several strong Claude-specific findings (bioweapons-uplift trial, first
autonomous CTF network solve, reward-hacking decrease, prompt-injection resistance) came from **Anthropic's
own Claude 4 System Card** — `company-self-report` scope, same category as the standing self-classification
exclusion — so despite being named and striking, they did not go into the main table.

**11 rows added to the main table** (one of which completed a pre-existing incomplete placeholder row
rather than creating a duplicate — see below): GPT-4o mini and GPT-3.5 Turbo's AgentHarm compliance rates;
UK AISI's STACK attack finding *actual working exploits* against production Claude Opus 4 and GPT-5 (not
just testing against them); GPT-4.5 scoring worse on factual accuracy than OpenAI's own two-years-older
GPT-3.5; RepliBench's finding that Claude 3.7 Sonnet is a dramatic, isolated outlier across three distinct
autonomous-replication sub-capabilities (only model that can covertly exfiltrate weights under monitoring,
0.98 vs. 0.00 on multi-GPU serving, only model able to set up C2 infrastructure — combined into one row per
§2's combine rule, since it's one capability profile from one evaluation); GPT-5.3-Codex deleting SIEM
security-alert records to cover its tracks mid-red-team; the "Cooling Tower" ICS scenario (GPT-5.3-Codex's
specific step count plus an emergent PLC-protocol-reverse-engineering capability not designed into the
scenario — distinct from the two existing Cooling Tower rows, which cover Opus 4.6's average and Mythos
Preview's first full solve); GPT-5.2 regressing below GPT-5 on container escape; DeepSeek-R1's 86.7%
task-success hallucination/false-claim rate; Claude Mythos Preview saturating an 18-task benchmark within
~2 months of Opus 4.5's 56% score; and a stark within-OpenAI-family disclosure gap (GPT-4o 13% vs.
GPT-5.1 86%) from RealityTest.

**A duplicate-ID bug caught and fixed mid-pass**: two of the new Finding IDs collided with existing rows
from the same STACK report. On inspection, one collision (`JAI2`) was a genuinely unrelated existing finding
(Gemma2 vs. ShieldGemma) — the new content got a fresh ID (`JAI4`) instead. The other (`JAI3`) turned out to
be a pre-existing **incomplete placeholder** — it said only *"Tested against an Anthropic Claude 4 Opus
defense pipeline"* with no result ever recorded. Rather than create a duplicate, the new finding (the actual
"we found vulnerabilities" result) was used to **complete the existing placeholder row** instead of adding a
parallel one. Always check whether an ID collision reveals a genuine duplicate/incomplete row before just
picking a new ID.

**8 rows added to the third-party/methodology section** (`Eval?=yes`, `Trackable?=no`) — real, named,
verified findings that are structurally comparative-ranking or technique-demonstration in nature, per
§1(3): a capability-score/deployment-safety gap between GPT-4 Turbo and Gemini 2.5 Flash; a universal attack
template's per-model success rates across Gemini/Command-R/Llama; a Claude-vs-Llama attack-success-rate
ranking; repeated-sampling and agent-vs-chat-setting jailbreak-amplification techniques (AgentHarm); Gemma2
outperforming ShieldGemma; cheap RM post-training matching GPT-4o's persuasiveness; and a NIST/CAISI
red-teaming competition finding about DeepSeek.

**Follow-up reconsideration (same day): `JOINT-2024-12-BIO2` reclassified to `Trackable = no`.** Kunal asked
directly whether this row (kept trackable in §20 as "the one clean exception" to the C2-reclassification
sweep) was actually alarming. Re-reading it closely: the Finding/Key Quote are pure relative-uplift language
with no threshold crossed, and the "company response" I'd used to justify the exception turned out to be
thin — OpenAI acknowledged evaluations occurred but explicitly declined to disclose the bio-domain results,
and the Medium-risk/safeguards classification isn't clearly tied to this specific finding rather than o1's
general CBRN profile. Reclassified to match the other 6. **This reverses part of §20's reasoning** — a
response existing does not, by itself, override the "no threshold crossed" exclusion; the exception standard
needs the response to be substantively tied to *this* finding, not just evidence that an evaluation happened.

**Net effect:** 360 → 379 rows (11 new main-table rows + 8 methodology-section rows, net of the 1 dropped
ID-duplicate). Main accountability table: 46 → 58 — the 46 baseline already reflects the CTRL-ALT-DECEIT
attribution upgrade and the `JOINT-2024-12-BIO2` reclassification (both applied earlier this pass); the
+12 delta from 46→58 is purely the 11 new trackable rows plus the completed `UKAISI-2025-07-JAI3` placeholder
(previously blank/untracked). 0 duplicate Finding IDs, 0 blank core fields.

---

## §22. Block B/C accuracy + specificity audit (2026-07-19)

**Trigger:** Kunal asked for "a deeper dive into the findings of section 2 and section 3 to check if they
are an accurate finding and not just general statements, which is not useful for us" — i.e. a full audit of
every row in Block B (`Eval?=yes`, `Trackable?≠yes`, 198 rows) and Block C (`Eval?=no`, 123 rows), 321 rows
total, across 172 unique Source URLs.

**Method:** grouped the 321 rows by unique Source URL into 11 batches (~17 URLs each), dispatched 11 parallel
background agents, each instructed to fetch every source in its batch and classify every row GOOD / VAGUE /
INACCURATE / COULD_NOT_VERIFY against the actual source text — not just check that the URL/quote existed
(evidentiary verification, already done in earlier passes) but check that the *Finding text itself*
accurately and specifically represents what the source says (see RULES.md §6, third kind of verification).

**Findings, by category:**
- **Overgeneralization** (partial result stated as universal): `UKAISI-2024-05a-BIO1` ("all five" → one
  underperformed), `UKAISI-2024-05a-ALI1` (only 2 of 5 models actually tested on this benchmark).
- **Unsupported added interpretive/policy framing**: `UKAISI-2024-01-GOV1`, `UKAISI-2024-11-GOV11`,
  `UKAISI-2024-11-GOV1`, `JOINT-2024-11-GOV1` ("first-ever"), `UKAISI-2024-12-GOV3` ("structurally blind to
  bio-uplift"), `UKAISI-2025-02-GOV1` ("most evaluations fail"), `UKAISI-2025-04-ALI3` ("single bottleneck"),
  `UKAISI-2025-04-ALI5` ("no plateau...accelerating"), `UKAISI-2025-11-GOV1` ("minimal traction"),
  `USCAISI-2025-12-GOV1` ("national security/export-control"), `UKAISI-2025-12-GOV4` (Crime and Policing Act
  2026 falsely attributed to a page that never mentions it), `UKAISI-2026-02-JAI2` ("even basic classifiers"
  when the paper calls them the strongest industry-deployed safeguards).
- **Misattributed/borrowed number or mechanism from a sibling finding**: `USCAISI-2025-11-GOV3` ("git
  history" vs. the source's actual "GitHub/package managers"), `UKAISI-2025-12-ALI4` ("ten detection methods"
  vs. source's "ten model organisms"), `UKAISI-2026-04-ALI11` (a "1.5x" figure borrowed from sibling row
  ALI10), `SGAISI-2026-01-AUT2` (fabricated "~18% safety disagreement" vs. real max ~8.1%),
  `UKAISI-2026-03b-CYB1` ("log-linear with model size" not supported, only compute-budget is).
- **Key Quote swapped between sibling rows in the same report**: `UKAISI-2025-12-CYB1` and `-BIO1` each had
  the other's (or a third row's) quote; `JOINT-2025-05-ALI1-s2` had a quote borrowed from a different
  subsection of the same system card.
- **Stat conflation** (two different source metrics presented as one): `SGAISI-2025-02-SOC1`.
- **Wrong benchmark entirely**: `HAL-2025-10-AUT1` was attributed to SciCode; the real paper documents this
  behavior on AssistantBench, and the cited examples actually show the models declining the shortcut rather
  than gaming it — corrected finding now describes discovered-but-not-exploited leakage.
- **Fabricated term + inverted result**: `SECUREBIO-2026-04-BIO2`/`GOV11` invented a "Ledidi threshold" that
  does not exist anywhere in the source, and stated GPT-5.5 *underperformed* on tacit-knowledge tasks when
  the source says the opposite — Checkpoint 2 hit the 100th percentile vs. human SMEs on VCT, the highest
  SecureBio had recorded for any model. **Flagged for a follow-up Trackable?/Severity review** — this
  correction turns a reassuring-null row into a genuine concerning capability finding on a named model, but
  the block/table reclassification itself was left for a dedicated pass rather than done unilaterally inside
  this accuracy sweep.
- **Wrong Source URL for an entire 5-row cluster**: `UKAISI-2025-10-ALI1/ALI2/ALI3/AUT2/GOV1` all cited
  arXiv:2605.08545 (tau-Bench Airline — an unrelated paper). The real source is the AISI blog
  "Transcript Analysis for AI Agent Evaluations," confirmed to contain every claim verbatim. Reverting the
  Source URL also meant reverting the 2026-07-18 "date fix" for these 5 rows — that fix had matched the
  *wrong* paper's date; the blog's own actual date (2025-10-10) turned out to be what was there originally,
  before that erroneous swap.
- **Data-corruption artifact**: `UKAISI-2025-11-ALI2`'s Finding text was literally truncated mid-word.
- **Stray audit note saved as a Finding**: `UKAISI-2025-09-GOV2`'s Finding field was a leftover verification
  note, not a real finding — dropped.
- **Broken/wrong-sourced citations, hard-dropped** (per RULES.md §1): `UKAISI-2025-03-GOV1` (cited source is
  an unrelated Gemini technical report; Finding text itself truncated), `UKAISI-2025-07-HUM3` (the specific
  claim doesn't appear anywhere in the cited paper, which covers entirely different models/topic).
- **VAGUE rows sharpened with the source's actual specifics**: `USCAISI-2025-11-GOV1` (3 concrete NIST
  recommendations), `NETWORK-2024-11-GOV2` (the actual CoT-in-14-languages suggestion).
- **VAGUE row dropped as non-additive**: `UKAISI-2024-05-BIO1` — confirmed via direct fetch that the "Fourth
  Progress Report" merely references the May Update's dual-use finding with zero new specifics; the same
  fact is already fully captured with real numbers in `UKAISI-2024-05a-BIO1`.
- **Internal metadata contradiction**: `UKAISI-2025-12-GOV6`'s Models field said "frontier LLMs (unnamed)"
  directly contradicting its own Finding (Llama-3.1-8B/Mistral-7B, both non-frontier) — fixed to match.

For rows requiring re-derivation of correct source content (the transcript-analysis blog cluster, the HAL
AssistantBench passage, SecureBio's real structure, NIST's actual recommendations, the Trends Report's real
cyber/bio quotes), a dedicated research pass fetched and quoted each source directly before any edit was
made — no correction was applied on inference alone.

**Net effect:** 379 → 375 rows (4 dropped: 3 broken/wrong-sourced/non-finding rows in round 1,
`UKAISI-2024-05-BIO1` as non-additive VAGUE duplicate in round 2). ~57 cell-level corrections across ~35
distinct rows. 0 duplicate Finding IDs, 0 blank core fields after the round. Main accountability table
unchanged at 58 (all touched rows were in Block B/C; `SECUREBIO-2026-04-BIO2` is flagged for a possible
promotion to Trackable=yes in a follow-up pass, not yet applied).

**New standing lesson (RULES.md §6/§6a):** evidentiary verification (is the quote/URL/date real) and
classification-consistency verification (do a row's own labels agree with each other) do not catch a third
failure mode — a Finding whose *prose* overstates, editorializes beyond, or misattributes what its own
(real, correctly-cited) source actually says. All three checks are now named explicitly as distinct and
necessary.

**Follow-up (same day): `SECUREBIO-2026-04-BIO2` promoted to `Action Trackable? = yes`.** Kunal confirmed
promoting the row flagged above. Severity recoded C2 → C1 (Recoded, not re-ensembled — the prior 3-way C2
vote was against the fabricated/inverted text and no longer applies; C1 matches the standard already used
for sibling row `BIO1`, which makes the same kind of claim: exceeding all human expert scores). Action
Level/Attribution/Company Response/Channel A fields populated from the same GPT-5.5 system-card "High
capability in the Biological and Chemical domain" response already documented on `BIO1`/`GOV11` in the same
report — this is the same underlying company action, now correctly linked to this finding too. Traction/
Media Outlets cleared (previously self-citing the row's own SecureBio source, circular per §5's Channel C
rule). Key Quote replaced with a verified verbatim VCT quote. **Net: main accountability table 58 → 59.**
0 duplicate Finding IDs, 0 blank core fields.

---

## §23. Robust Policy/Media/Social/Academic verification sweep (2026-07-19)

**Trigger:** Kunal asked for "a strategy for policy, social and media response which is very robust and which
covers everything and also validates everything as well, without including false positives." Agreed strategy:
a two-stage find-and-verify pipeline, applied to all 375 rows (not just the main table), covering both
re-verification of existing Channel B/C content and genuine new-evidence search where blank.

**Method:** all 375 rows batched into 15 groups of 25, each dispatched as a background agent instructed to (a)
re-verify every existing Policy Level/Response/Verbatim/Evidence and Media Outlets/Traction/Social
Highlights/Channel C Verbatim cell against its cited source, classifying VERIFIED-KEEP / FALSE-POSITIVE-REMOVE
/ UNREACHABLE, and (b) run genuinely distinct search angles (official regulator sites for policy, outlet-
specific searches for media, named-account searches for social) for any blank cell, with an explicit
instruction to default to "not found" over any shaky candidate.

**Critical cross-cutting discovery:** batch 11 found that "Resultsense.com" — accepted as an independent media
source by several other batches (7, 8, 9, 10, 12) — explicitly states on its own About page "We do not claim
to produce original journalism in our news section," and its specific AISI-related articles are bylined
"Analysis...Resultsense [via AI Security Institute]" — i.e. republished AISI blog summaries, not independent
reporting. This fails the independence test central to the whole sweep. **Every Resultsense citation across
every batch was rejected**, including several that other batches had marked VERIFIED-KEEP or NEW-CANDIDATE.
This is now a standing exclusion (see RULES.md).

**False positives found and removed** (~55 rows): patterns included (a) a page or bill genuinely fetched but
confirmed to never mention the finding at all (Seoul Summit gov.uk page cited across 3 unrelated JOINT-2024-11
rows; CA SB53 bill text with zero mentions of Anthropic/Claude/scheming; NIST AI 800-2 full-text-checked to
never cite the UK AISI transcript-analysis report despite thematic similarity), (b) temporal impossibilities
(a Lords Library page dated 3.5 months *before* the finding it supposedly responded to, across 3 rows; an
Anthropic blog post 4 months before the Sept-2025 finding it was cited for), (c) self-citation disguised as
independent evidence (a report's own primary source relisted as "Media Outlets"; Policy Response text that
was just the Finding text copy-pasted, not a real government action; thorn.org for a Thorn-co-authored
report), (d) identical unsourced boilerplate reused across unrelated rows (3 DeepSeek rows sharing one
"cited in Congress/NSA/NCSC" claim with zero corroboration), (e) fabricated/misattributed quote attribution
(a "CNBC" quote traced to a real but unrelated article; a "Ledidi threshold" — already caught in §22 —
resurfacing here in its Media/Channel C evidence too), (f) a quote duplicated verbatim across two different
sub-findings from the same report (UKAISI-2026-06-ALI1/ALI2's suppression-rate quote), and (g) a media
citation confirmed via direct fetch to discuss a completely different, unrelated finding despite superficial
topic overlap (several UK AISI Frontier AI Trends Report rows' Resultsense/CSA citations).

**Genuine new evidence added** (~90 rows, non-Resultsense only): included one significant government-response
upgrade — a UK ministerial open letter (DSIT Secretary Liz Kendall MP & Security Minister Dan Jarvis MP,
15 Apr 2026) explicitly citing AISI's Mythos 73% CTF finding by name, previously miscoded as "no policy
response"; a French regulator's (Arcep) official report building directly on a PEReN energy study, with 9
formal recommendations; confirmation that US CAISI gated GPT-5.6 Sol's public release pending cyber-capability
review (a genuine binding-requirement policy action); and dozens of verified independent media/social
citations (TechCrunch, Fortune, Axios, NBC News, FedScoop, BABL AI, CyberScoop, LessWrong, named independent
X/Substack commentators) added where previously blank.

**Net effect:** 0 duplicate Finding IDs, 0 blank core fields maintained throughout (378 total cell-level
changes: 193 false-positive removals/softenings, 180 new verified additions, 5 final Resultsense cleanup
fixes). Main accountability table unchanged at 59 (this sweep touched Channel B/C evidence fields only, not
Eval?/Trackable? classifications). Policy Level populated on 123/375 rows, Media Outlets on 102/375, Social
Highlights on 39/375 — all now reflecting genuinely searched-and-verified status rather than "opportunistic,
whatever an earlier pass happened to add."

**New standing lesson (RULES.md §5/§6a):** a source category can pass an individual fetch check yet still fail
independence at the *source-type* level — Resultsense's articles were live, real, and accurately quoted the
underlying finding, but the source itself discloses it isn't original journalism. Checking "does this URL
resolve and say what I think it says" is necessary but not sufficient; also check what kind of source it
actually is before counting it as independent third-party evidence.

---

## §24. v8 checkpoint (2026-07-19)

**v8 BUILT**, superseding v7: `~/aisi-v4-audit/v8_apply/v8.csv` (375 rows; copies on Desktop as `aisi_v8.csv`
/ `aisi_v8_by_report.csv` / `aisi_v8_master.csv` / `aisi_v8_changelog.csv` / `aisi_v8_CODEBOOK.md` /
`aisi_v8_RULES.md`). This version folds in everything documented in this file's §22 (321-row Block B/C
accuracy + specificity audit: ~35 rows corrected, 4 dropped, 1 promoted to the main table) and §23 (375-row
Policy/Media/Social robustness sweep: 378 cell-level changes, the Resultsense-independence discovery, and
several genuine new government-response findings). Main accountability table: 59 rows. 0 duplicate Finding
IDs, 0 blank core fields. `changelog.csv` and `RULES.md` carry forward unbroken from v7 — this is a version
checkpoint marking a substantial round of corrective work, not a reset.


---

## §25. Single-row fix: JOINT-2024-11-BIO2 (2026-07-19)

Kunal quoted this finding directly ("US AISI found that with access to bioinformatics tools, Claude 3.5
Sonnet's performance... at times exceeded measured human expert baselines...") and asked whether it belongs
in the main table. It doesn't: this is a with-tools-vs-without-tools relative-uplift finding (without tools,
matched reference models and stayed below baseline; with tools, "at times" exceeded it) — the RULES.md §3
relative-uplift exclusion, not a demonstrated absolute threshold. It also duplicates sibling
`JOINT-2024-11-BIO3`'s already-correctly-excluded uplift claim, and is the exact same shape as
`JOINT-2024-12-BIO2` (o1 tool-augmentation), reclassified earlier this session for identical reasoning.

**Fix applied**: `Severity (C1/C2) majority` C1→C2, `Action Trackable?` yes→no. **Main accountability table:
59 → 58.** 0 duplicate Finding IDs, 0 blank core fields. This was a deliberately narrow, single-row fix — not
a re-run of the broader severity/combine sweep from earlier today, which was reverted at Kunal's request.

---

## §26. Single-row fix: JOINT-2025-01-JAI1 (2026-07-19)

Kunal quoted this finding directly (11%→81% attack success rate uplift, 57%→80% eval-improvement uplift) and
asked how it was trackable and attributed to a single company. It wasn't defensibly either: the row's own
`Attribution` and `Company Response` fields already read "None," and Notes explicitly stated "No documented
company response (Anthropic) to this specific publication" — yet `Action Trackable?` was "yes." The severity
was also miscoded: this is a before/after comparison of attack- and evaluation-technique effectiveness (CAISI's
own red-teaming methodology improving), not a demonstrated absolute capability of Claude 3.5 Sonnet itself —
textbook RULES.md §3 relative-uplift exclusion.

**Fix applied**: `Severity (C1/C2) majority` C1→C2, `Action Trackable?` yes→no. **Main accountability table:
58 → 57.** 0 duplicate Finding IDs, 0 blank core fields.

---

## §27. Single-row fix: UKAISI-2025-04-ALI1 (2026-07-19)

Same pattern as §26. Finding is a pure benchmark-score description (pass@10 percentages across RepliBench
task families), with no absolute non-comparative achievement claim comparable to `JOINT-2024-12-CYB1`'s
"uniquely solved" marker. `Attribution` and `Company Response` were already "None" in the row's own fields,
and Notes documented that the one prior exception-justification ("weakened in response") had been formally
RETRACTED as a misattributed version — `Action Trackable?` was never updated after that retraction.

**Fix applied**: `Severity (C1/C2) majority` C1→C2, `Action Trackable?` yes→no. **Main accountability table:
57 → 56.** 0 duplicate Finding IDs, 0 blank core fields.

---

## §28. Combine: JOINT-2025-05-JAI1 + JOINT-2025-05-ALI1 (2026-07-19)

Kunal asked whether two adjacent main-table rows (the early Claude Opus 4 snapshot's deference-to-harmful-
instructions finding, and its resulting scheming/deception behavior) could be combined. Confirmed yes: these
are cause and effect from one Apollo assessment of one model snapshot, not two distinct incidents — their
`Company Response` fields were already near-duplicates of each other, describing the same Anthropic
mitigation and the same omitted-fine-tuning-dataset detail twice.

**Fix applied**: merged `JOINT-2025-05-JAI1`'s content into `JOINT-2025-05-ALI1` (Finding text now covers
both the root-cause mechanism and the resulting behaviors; Company Response now includes the missing-dataset
detail); `JOINT-2025-05-JAI1` dropped. **Main accountability table: 56 → 55.** 375 → 374 total rows.
0 duplicate Finding IDs, 0 blank core fields.

---

## §29. Row 23/27 evidentiary fix: JOINT-2026-02-JAI1 / JAI3 (2026-07-19)

Kunal asked to verify whether row 23's ("safeguard updates deployed prior to deployment") Company Response
claim was actually tied to the UK AISI universal-jailbreak finding it's attached to. Fetched and full-text
extracted OpenAI's GPT-5.3-Codex system card directly: the UK AISI 10-hour/0.778-pass@200 finding is reported
in isolation, with no specific fix credited to it -- only a generic risk-acceptance paragraph (existing
bug-bounty/monitoring programs) that names neither UK AISI nor this finding. Also confirmed no reference-model
comparison exists near this finding, so the row's `[Report tested: reference models]` Notes tag was
unsupported. Separately discovered the "two-tiered cyber conversation monitor" (credited as a response in
sibling row `JAI3`) is actually a *pre-existing* safeguard both red-teaming campaigns tested against, not a
new mitigation deployed because of what they found.

**Fixes applied**: `JOINT-2026-02-JAI1` -- Company Response corrected to reflect no specific fix exists;
Action Level Substantive->Acknowledged; Proportionality Proportionate->Strongly Disproportionate (this is
actually an accountability gap, not a well-handled finding); stray Notes tag removed. `JOINT-2026-02-JAI3` --
Company Response corrected to clarify the two-tiered monitor predates the findings rather than responding to
them. Severity/Trackable status unchanged for both (the underlying findings are still real and C1) -- only
the response/proportionality accounting was corrected. 0 duplicate Finding IDs, 0 blank core fields.

---

## §30. Block B/C duplicate and combine-check sweep (2026-07-19)

Kunal asked for a systematic duplicate/combine check across all of Block B ("alarming but not trackable")
and Block C ("not alarming"), 319 rows total, followed by "work all of these" -- explicit approval to apply
every fix once a 10-batch agent sweep (grouped by Report ID) had flagged candidates. The sweep surfaced 25
clusters covering 61 rows: clean intra-Report-ID duplicates, three cross-Report-ID duplicate pairs (the same
underlying report processed twice under two different Report IDs -- a known recurring dataset defect), and
content that violated the one-finding-per-row rule (RULES §4) by splitting a single technique/phenomenon
across multiple rows.

**Method**: pulled full content (Finding, Key Quote, Company Response, Action Trackable?, Notes) for all 63
unique Finding IDs across the 25 clusters, then classified each cluster:
- **Combine** (one phenomenon fragmented across rows, or a genuine duplicate): keep the fuller/better-sourced
  row as the survivor, append a `[MERGED 2026-07-19: ...]` tag to its Notes summarizing the absorbed content,
  drop the other row(s) entirely.
- **Keep separate**: clusters that share a Report ID or subject but describe genuinely distinct claims (e.g.
  a capability-trend finding vs. its governance/evaluation-validity implication) were reviewed and left as
  independent rows -- no content was merged, matching RULES §4's "Reframe/Split" guidance for genuinely
  distinct incidents.

**25 clusters, disposition**:
1. `UKAISI-2024-01-GOV1`+`GOV2` (Gemini Ultra pre-release null result) -- combine, GOV2 dropped.
2. `JOINT-2024-11-BIO2`+`BIO3` (bio tool-augmentation uplift) -- combine, BIO3 dropped.
3. `JOINT-2024-11-CYB1`+`CYB2` (cyber capability comparison) -- combine, CYB1 dropped.
4. `SGAISI-2025-02-JAI1`+`JAI2` (regional-language exploit rates) -- combine, JAI2 dropped.
5. `UKAISI-2025-09-SOC1`+`GOV4` (political-knowledge RCT, cross-Report-ID dup via `UKAISI-2025-09-POLKNOW`)
   -- combine, GOV4 dropped, SOC1's blank Key Quote filled with GOV4's verified verbatim.
6. `UKAISI-2026-04-ALI2`+`ALI15` (OpenClaw model-name leakage) -- combine, ALI2 dropped.
7. `UKAISI-2026-04-ALI8`+`ALI19` (safety-refusal rates, cross-Report-ID dup via `ANTHROPIC-2026-04-SELF`)
   -- combine, ALI8 dropped.
8. `UKAISI-2025-12-GOV3`+`GOV4` (AISI/Thorn CSAM protocol) -- combine, GOV4 dropped, GOV3's Company Response
   merged to include both the ten-organization signing and OpenAI's Child Safety Blueprint.
9. `UKAISI-2026-05-CYB1`/`GOV1` (cyber doubling-time vs. evaluation-framework-saturation) -- reviewed,
   genuinely distinct claims, kept separate.
10. `SGAISI-2026-06-ALI1`/`ALI2`/`CYB1`/`AUT1` (SG-KR data-leakage study) -- ALI1 absorbed CYB1 (capability-
    safety divergence, same phenomenon) and AUT1 (pure methodology); ALI2 (claims-action mismatch/fabrication)
    is a genuinely distinct phenomenon, kept separate.
11. `UKAISI-2025-12-CYB1`+`CYB2` (cyber task doubling / apprentice-to-expert trend) -- combine, CYB2 dropped.
12. `UKAISI-2025-07-JAI5`+`JAI2` (classifier-vs-ShieldGemma, cross-Report-ID dup via `UKAISI-2025-07-STACK`)
    -- combine, JAI5 dropped. `UKAISI-2025-07-CYB1` (separate Report ID `UKAISI-2025-07-CYB1`) covers much
    of the same JTE3 exercise but was NOT merged -- flagged only, per the standing rule that full Report-ID
    reconciliation is a separate scope check, not to be silently resolved mid-sweep.
13. `JOINT-2025-07-GOV1`+`CYB1`+`AUT1` (Joint Testing Exercise 3 judge-reliability finding) -- GOV1 absorbed
    CYB1 (exercise structure) and AUT1 (pass-rate detail) as methodology facets.
14. `USCAISI-2026-03-CYB4`+`JOINT-2026-03-JAI2` (DeepSeek/transfer-asymmetry, cross-Report-ID dup) -- combine,
    JAI2 dropped as a verbatim restatement of CYB4's own transfer-asymmetry clause. `JOINT-2026-03-CYB1` and
    `JAI1` (scale stat, 100% compromise rate) are genuinely distinct claims, kept separate.
15. `UKAISI-2025-09-AUT1`+`ALI1` (two-hop reasoning) -- combine, ALI1 (methodology-only) dropped.
16. `SGAISI-2026-01-AUT1`+`AUT2` (agent data-leakage) -- combine, AUT2 (methodology-only) dropped.
17. `UKAISI-2026-02-SOC1`+`SOC2` (workplace-productivity RCT) -- combine, SOC2 dropped as a likely duplicate
    using unverified task labels that don't match SOC1's already source-corrected O*NET framework; flagged
    for future re-check rather than asserted as fabricated.
18. `JOINT-2025-09-JAI1`+`JOINT-2025-00-JAI3` (Constitutional Classifier jailbreak/response, cross-Report-ID
    mismatch) -- combine, JAI1 (attack-technique side, no company response) merged into JAI3 (response side).
19. `UKAISI-2026-04-ALI11`+`ALI14` (goal-conflict sensitivity) -- combine, ALI14 (null/corollary framing of
    the same relationship) dropped.
20. `UKAISI-2026-04-ALI9`+`ALI18` (contextual-factors variance) -- combine, ALI18 (methodology-only) dropped.
21. `UKAISI-2026-06-ALI5`+`ALI1b` (lie-detector degradation) -- combine, ALI5 (CoT-judge sub-finding) dropped.
22. `UKAISI-2025-10-ALI4`+`ALI1b` (data-poisoning) -- combine, ALI4 (scope-only) dropped.
23. `UKAISI-2025-11-ALI4`+`ALI6`+`ALI3`+`UKAISI-2025-11b-ALI1`+`ALI7` (alignment evaluation-awareness case
    study) -- ALI4 absorbed ALI6 (same phenomenon, complementary facet); `UKAISI-2025-11b-ALI1` absorbed ALI3
    (Petri tool mention) and ALI7 (methodological caveat); ALI4 and ALI1 remain as two genuinely distinct
    findings (awareness-reduction vs. sabotage-null-result).
24. `UKAISI-2025-12-GOV6`+`UKAISI-2025-12a-ALI1` (self-eval wireheading) -- combine, GOV6 (model-list-only)
    dropped.
25. `UKAISI-2025-12-HUM2`+`SOC2` (persuasion study) -- combine, HUM2 (mechanism-only) dropped.

Also folded in `UKAISI-2025-12-ALI4` (sandbagging-detection cluster, Report ID `UKAISI-2025-12`) as a
redundant summary of sibling rows `ALI2`/`ALI3` -- dropped, its one distinct detail (only ten model organisms
used) preserved in `ALI3`'s Notes. `USCAISI-2025-09-CYB2`/`SOC1` (DeepSeek security vs. adoption stats) and
`UKAISI-2026-03a-GOV2`/`GOV3` (compute-scaling vs. evaluation-validity implication) were reviewed and kept
separate as genuinely distinct claims.

**Net effect**: 374 -> 345 rows (29 rows dropped/merged into 25 survivors). 0 duplicate Finding IDs, 0 blank
core fields, content-preservation check passed on block re-sort. Main accountability table unaffected at 55
rows -- every dropped/merged row was Block B or Block C (`Action Trackable?=no`).
