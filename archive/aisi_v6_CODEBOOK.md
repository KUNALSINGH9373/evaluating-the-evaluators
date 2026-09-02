# Evaluating the Evaluators — Dataset Codebook (v6)

Revised 2026-07-16. Supersedes the v4 codebook. This version incorporates every inclusion/exclusion
rule and column definition, **plus all alterations made during the v6 verification pass**. Where a rule
changed this session, it is marked **[REVISED]** or **[NEW]** with the reason.

---

## 0. What the dataset measures & scope

The dataset measures the **public-channel accountability pipeline**: when a government AI Safety Institute
publishes a finding about a specific model/company, does a documented response follow?

**Scope = government AISIs and their joint exercises.** [REVISED]
- **In scope (main list, `Scope = government-AISI`):** UK AISI, US CAISI/NIST, and the affiliated national
  AISIs (Japan J-AISI, Singapore SGAISI/IMDA, Korea K-AISI/TTA, France INESIA/PEReN, EU AI Office), plus
  any joint/International-Network exercise **that includes a government AISI** — even joints with a
  non-government co-author (e.g. "UK AISI + Apollo", "SecureBio + US CAISI", "+ Gray Swan", "+ Thorn").
- **Kept but stratified at the END of the sheet, excluded from headline stats:** [NEW]
  - `Scope = third-party-evaluator` — evaluations by a **non-government** body with **no** government AISI
    co-author (e.g. Apollo Research alone).
  - `Scope = company-self-report` — a company evaluating **its own** model (Anthropic/OpenAI self-reports).

**Hard drop (removed from the sheet entirely):** [NEW — the rule that removed the Gemini 3 Pro FSF rows]
- A report that **names no evaluating agency at all** (only "external evaluators" / "specialist groups")
  is out of scope and dropped. Logged in `dropped_rows.csv`.
- Also excluded: private/MOU evaluations never published; non-English-only outputs; rows that fail
  source-verification (fabricated/conflated/wrong-source).

---

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

Accountability set: **67 (v4) → 46 (v6)**. Every change is logged in `changelog.csv`.
