# Channel A/B/C Re-search — Verification Report

**Pass ID:** `channel_reverify_2026-08-28`
**Search executed:** 2026-08-28 · **Adjudication executed:** 2026-08-28 · **Report compiled:** 2026-08-28
**Per-finding evidence logs:** `/Users/kunalsingh/MATS/Research/AISI_Evals/logs/channel_reverify_2026-08-28/results/chunk_01.json` … `chunk_13.json` (185 records)
**Input slices:** `…/logs/channel_reverify_2026-08-28/chunks/chunk_01.json` … `chunk_13.json`
**Adversarial verdict log:** `~/.claude/projects/-Users-kunalsingh-Desktop/9b4cd91a-0a4c-4c96-9f90-0e5248653043/subagents/workflows/wf_4bd58825-b6e/journal.jsonl` (36 verdict records)
**Governing rules:** `rulebook/v11_RULEBOOK.md` (§4 tiering, §8 Channel A, §9 Channel B, §10 Channel C, §11 proportionality, §14 evidentiary standard); `protocol/codebook.md`
**Dataset under audit:** `dataset/AISIEVAL_V13.xlsx`, sheet `AISIEVAL_V13`, read through `scripts/dataset_source.py` (1,001 rows)

> **Status.** Both layers of this pass are complete. All 185 Tier A findings were re-searched, all 36 resulting proposals were adversarially adjudicated (13 upheld, 23 rejected), and 9 of the 13 upheld changes have been applied to V13. The four unapplied upheld changes and their grounds are in §4. Every count in this report was recomputed directly from V13 and from the two log sets named above; nothing is carried over from the superseded draft of this document.
>
> **Both layers are AI agents. No human reviewed any coding, any verdict, or any applied change.** See §2.

---

## 1. Scope

### 1.1 Population searched

| Quantity | Count | Basis |
|---|---:|---|
| Findings re-searched in this pass | **185** | the Tier A population as it stood on 2026-08-28 |
| Dispatch | 13 chunks | 12 × 15 findings + chunk_13 × 5 |
| Per-finding records returned | 185 | every record carries `channel_a`, `channel_b`, `channel_c`, a confidence rating and free-text notes |
| Severity split of the searched set | C1 **146** / C2 **39** | `Severity (C1/C2) majority` |
| Institutions represented | 27 | `Institution` |
| Access Type split | Post-deployment 122 / Pre-deployment 51 / Mixed 12 | `Access Type` |
| Finding publication dates | **2023-03-17 → 2026-07-29** | `Publication Date` |
| Searcher confidence: high / medium / low | **113 / 69 / 3** | recorded per finding |

The `Institution Type` split of the 185 is Government 60, Non-Profit (AIEF) 43, Non-Profit (Independent) 41, For-Profit 36, Government;Lab 3, Non-Profit (Independent);Lab 1, Government;For-Profit 1.

### 1.2 Reconciling the searched set (185) against V13 Tier A (184)

V13 now holds 1,001 rows: Tier A 184, Tier B 467, Tier C 350. The searched set of 185 is *not* today's Tier A set, and the difference must be stated:

- Every one of V13's 184 Tier A findings was searched (verified: the set difference is empty).
- One searched finding, **`APOLLO-2026-07-ALI4`**, is no longer Tier A. V13 re-tiered it Tier A → Tier C (`Eval? = no`, `Action Trackable?` blank), which also repairs the schema violation the earlier record carried. It is C2, so the C1 headline denominator of 146 is unaffected.
- **`UKAISI-2025-08-JAI2` is absent from V13 by design.** It was removed upstream and was never part of this pass's 185. It is not a missing row and not a defect. Any claim that V13's headline is unreproducible because of it is wrong; §6 shows the headline reproduces exactly.

### 1.3 Windows

- **Corpus cutoff (frozen):** 2026-07-30. No finding published after this date is in scope.
- **Response search window:** each finding's publication date through **2026-08-28**. A company response is admissible if it postdates the finding, except that a documented coordinated pre-deployment response may carry negative lag (rulebook §8, line 134; codebook col 22).
- **Batteries superseded:** the stored `Sources Checked (channel A)` logs in V13 are dominated by two prior response searches, dated **2026-08-02** (61 rows) and **2026-08-15/16** (91 / 84 rows). This pass supersedes both for the 185 findings searched. The 12-to-26-day gap since the last battery is the reason it was commissioned; several changes below rest on company documents published inside that gap (the Anthropic August 2026 Risk Report, 2026-08-14; OpenAI's Hugging Face incident post, 2026-08-26).

### 1.4 Battery executed per finding

Each finding was re-coded **independently first and compared with the stored value afterwards**, rather than reviewed for confirmation. Channel A (rulebook §8), five items: (1) company newsroom / research blog / press index, site-restricted; (2) the launch system card for the evaluated model **and every subsequent card in the same model family** published before the search date; (3) deployment-safety / transparency hub pages; (4) official company statements, submissions and filings; (5) open-web search, used **only to locate company primary sources**, never as evidence in itself.

Channel B (§9) ran per jurisdiction against official records: UK Hansard (Search API), gov.uk, NCSC; US Federal Register API, govinfo, congress.gov, committee document repositories; EU Commission press corner and Parliament written questions. **The US congressional leg did not in fact execute — see §7.** Channel C (§10) logged independent media, academic citations and public discussion; it scores nothing.

### 1.5 Search outcome

| | Count |
|---|---:|
| Findings re-searched | 185 |
| Codings re-derived and **unchanged** | 149 |
| Codings with a **proposed change** | **36** (19.5%) |

Per-chunk proposals: 2, 6, 6, 1, 2, 1, 3, 6, 2, 4, 0, 2, 1.

**Direction of the search layer.** Of the 36 proposals, 28 would have raised an Action Level, 2 would have lowered one, and 6 touched Policy Level only. That asymmetry is expected of a late-running pass — a later search can add responses but cannot remove them — and it is precisely what the adjudication layer in §3 was built to test.

---

## 2. Method

Two stages, both executed by AI agents.

**Stage 1 — search and proposal (13 agents).** One agent per chunk. Each was given the stored dataset row and instructed to re-derive Channel A, B and C independently from primary sources before looking at the stored coding, to log every source checked with a retrieval date and outcome, and to propose a recoding only where its independent derivation differed. Agents were instructed to download and text-extract primary documents rather than rely on search-result snippets, and were forbidden from automated regex triage of cached documents. The 13 agents produced 36 proposals across 185 findings.

**Stage 2 — adversarial verification (36 agents).** One agent per proposal. Each verifier was instructed to **attempt to refute** the proposal — to re-retrieve the cited primary source itself rather than accept the searcher's log, to test admissibility, finding-specificity, timing and level, and to **default to rejection** where the evidence did not clearly establish the claim. Each returned a structured verdict: `upheld` (boolean), the proposed coding, a reasoned opinion, and a fallback coding to use if the proposal failed. All 36 verdicts are on record; the verdict counts in §3 are taken from that log, not from any intermediate summary.

**No human review occurred at any point.** No human read a source document, checked a verdict, or approved an applied change. The stage-2 agents challenged the stage-1 agents; nothing challenged the stage-2 agents. Two consequences must travel with any citation of this report:

1. **Correlated error is not excluded.** Both stages share a model family, a rulebook reading and an environment. A systematic misreading of the admissibility rule would not be caught by this design, because both stages would make it.
2. **The verifiers' own coverage was degraded.** Many stage-2 verdicts record that the verifier's WebSearch budget was exhausted before it could re-run the open-web limb, and several record the same congress.gov and govinfo blocks that defeated stage 1 (see §7). Where a verdict rests on documents the verifier downloaded directly, it is strong; where it rests on reasoning over the searcher's log, it is weaker, and the verdicts say which is which.

A third layer — writing changes into V13 — was executed for 9 of the 13 upheld proposals. §4 states which, and why the other 4 were withheld.

---

## 3. Results

### 3.1 Headline adjudication result

| | Count | Share |
|---|---:|---:|
| Proposals submitted | **36** | 100% |
| **Upheld** | **13** | **36.1%** |
| **Rejected** | **23** | **63.9%** |

### 3.2 By category of proposal

| Category | Proposed | Upheld | Rejected | Rejection rate |
|---|---:|---:|---:|---:|
| **New response found** (Action Level `None` → any level) | **21** | **6** | **15** | **71.4%** |
| Existing response upgraded (level raised, not from `None`) | 7 | 3 | 4 | 57.1% |
| Existing response downgraded (level lowered) | 2 | 0 | 2 | 100% |
| Policy Level only (Action Level unchanged) | 6 | 4 | 2 | 33.3% |
| **Total** | **36** | **13** | **23** | **63.9%** |

### 3.3 Why the 71% figure is the most important number in this report

The paper's central claim is a **non-response rate**: that a majority of Tier A C1 findings draw no qualifying company response. Every threat to that claim takes one specific form — that a response exists and the coders missed it. The "new response found" category is exactly that threat, made explicit and then tested: 21 claims that a `None` was wrong, each pursued by an agent with a fresh five-item battery and an incentive to find something, then each attacked by a second agent instructed to refute it.

**Fifteen of the 21 did not survive.** And they failed for a consistent reason, visible across §5: in nearly every case the searcher located a real, correctly quoted, correctly dated company document on the same *topic* as the finding, and the verifier established that it did not address *this* finding. The failure mode is not fabrication — the verifiers confirmed the sources were genuine and the quotes verbatim-exact in the great majority of rejections. The failure mode is **topical adjacency mistaken for response**.

Three implications the paper should carry:

1. **The non-response rate is robust to a determined adversarial search.** A dedicated late pass with full-text retrieval moved the C1 no-response count by 4 findings out of 90 (§6). The claim is not an artefact of shallow searching.
2. **The rate is sensitive to where the admissibility line is drawn, not to search effort.** Had all 21 "new response" claims been accepted, the headline would have fallen much further. What separates the two worlds is a rule about what counts as a response, applied consistently — which is why §5 groups the rejections by ground rather than by finding.
3. **The measurement is conservative in the direction that matters, and this cuts both ways.** Six genuine responses were found that the prior batteries had missed, so earlier passes did undercount. A future pass will likely find a few more. The correction is small and its direction is known.

One caveat on the rejection rate itself, stated plainly: **it measures agreement between two AI agents applying the same rulebook, not correctness.** A rejection rate of 64% shows the verifiers were not rubber-stamping; it does not show they were right.

---

## 4. Upheld changes (13)

Nine are applied to V13. Three are upheld but **held back** because applying them as submitted would violate the project's own coding rules. One is upheld but **not applied** because the code it moves to requires an evidentiary record the proposal did not supply.

### 4.1 Applied to V13 (9)

**1. `METR-2023-03-ALI1`** — C1, Pre-deployment, OpenAI / GPT-4
Old: Action `None` / Attribution `No response located` / Policy `Non-binding policy-related uptake`
New: Action **`Acknowledged`** / Attribution **`Explicit attribution`** / Policy unchanged. Response Date 2023-03-14, Lag −3.
Evidence: `https://cdn.openai.com/papers/gpt-4-system-card.pdf` §2.9 "Potential for Risky Emergent Behaviors" (HTTP 200, 60pp, `pdftotext`).
Survived because: OpenAI's own launch card, which §8 designates the canonical Channel A location for a pre-deployment evaluation; the card names ARC (METR's predecessor) and cites the finding as ref [75]; all three quoted strings matched verbatim. Negative lag is permitted here — Access Type is Pre-deployment and the card documents the coordination ("early access … as a part of our expert red teaming efforts"). Correctly **capped** at `Acknowledged`: the verifier grepped the whole card and found every power-seeking / autonomous-replication / deception hit inside §2.9 or the bibliography, with no mitigation anywhere tied to the behaviour. The prior `None` rested on an automated regex triage of cached cards, which §8 forbids.
Residual: the **retained** Channel B `Non-binding` value is neither confirmed nor refuted — `CHRG-118hhrg52499` has no text layer over its body pages and the govinfo HTML renders prepared statements as `[GRAPHICS NOT AVAILABLE IN TIFF FORMAT]`. Not part of the upheld change; flagged for separate Channel B re-verification.

**2. `APOLLO-2023-11-ALI1`** — C1, Post-deployment, OpenAI
Old: `Partial` / `No explicit attribution` / `Non-binding`
New: **`Substantive`** / **`Explicit attribution`** / `Non-binding` unchanged. Response Date 2025-09-17, Lag 678.
Evidence: `https://openai.com/index/detecting-and-reducing-scheming-in-ai-models/` (2025-09-17). Direct fetch 403; read from the Internet Archive capture `20260826100640` (70,365 bytes). Companion paper arXiv:2509.15541 downloaded and grepped.
Survived because: company newsroom primary document (the Wayback capture is a retrieval route, not a substitute source); the Substantive test is met by model changes rather than statements — deliberative-alignment anti-scheming training of o3 (13% → 0.4%) and o4-mini (8.7% → 0.3%), shipped GPT-5 deception-propensity mitigations, and two scheming categories added to the Preparedness Framework; the co-published paper cites this exact finding by title, authors and ID (Scheurer, Balesni & Hobbhahn, arXiv:2311.07590); OpenAI's own post names Apollo Research.
Two corrections entered by the challenge, neither load-bearing: (a) the searcher's claim that the citation is "invoked twice as the prior work the covert-action construct is built on" is **overstated** — both in-text invocations sit inside multi-work citation strings and the first frames the finding as falling "short of full scheming"; (b) the "corroborating detail" that the post's stock-trader analogy is this finding's scenario **is struck as inference**.
Residual: OpenAI never says the work was undertaken *in response to* the 2023 paper, and the mitigations target o3/o4-mini/GPT-5 rather than the evaluated GPT-4.

**3. `JOINT-2024-11-BIO2`** — C1, Pre-deployment. **Policy Level only.**
Old policy: `No policy uptake identified` → New: **`Non-binding policy-related uptake`**. Action `Acknowledged` and Attribution `Explicit attribution` unchanged.
Evidence: Hansard, House of Lords, 2024-11-21, Lord Vallance of Balham (Minister of State, DSIT), debate "Large Language Models and Generative AI (Communications and Digital Committee Report)". Retrieved via `hansard-api.parliament.uk/search.json` and `…/debates/debate/600E1622-A12A-4E0B-8EC1-63BFBD4B0DA1.json` (both HTTP 200); ContributionExtId `6F38699C-11EC-49C6-9AB0-492FE2AD13A4`, ItemId `41123376`, both matching the searcher's log.
Survived because: Hansard ministerial statement is the exact UK Channel B source class the rulebook names; the reference is report-specific, not topical — "Just this week the AI Safety Institute shared a detailed report outlining pre-deployment of Anthropic's upgraded Claude 3.5 Sonnet model" — and the verifier confirmed the target report (AISI blog, 2024-11-19) matches this row's Report ID, Publication Date and Source URL, with no rival candidate; two days after publication; correctly capped at Non-binding, since the Minister used the report to *defend* the voluntary regime. The circularity objection (a DSIT minister citing DSIT's institute) was tested and rejected: the exclusion is written into Channel C only, and would otherwise disqualify essentially all UK uptake for any UK-AISI finding.
**Outstanding defect, not fixed by the applied change:** V13 still stores `Channel B Evidence` = `https://hansard.parliament.uk/lords/2024-11-21/debates/`, a bare date landing page that 403s to automated access and does not resolve to the contribution. It must be replaced with the debate-specific path under ExtId `600E1622-A12A-4E0B-8EC1-63BFBD4B0DA1`. (The log's "1 contribution" was also a miscount; 2 were returned, the extra correctly excluded as general discussion.)

**4. `SECUREBIO-2025-04-BIO1`** — C1. **Policy Level only.**
Old policy: `No policy uptake identified` → New: **`Non-binding policy-related uptake`**. Action `Substantive` / `Explicit attribution` unchanged.
Evidence: written testimony of Dr Jassi Pannu, US House Energy & Commerce Subcommittee on Oversight and Investigations, "Examining Biosecurity at the Intersection of AI and Biology", 2025-12-17. The verifier retrieved the congress.gov PDF by `curl` (HTTP 200, 1,496,654 bytes) where WebFetch was Cloudflare-blocked, and verified character-for-character: *"A benchmark that specifically assesses virology knowledge (the Virology Capabilities Test) … shows that some LLMs now outperform expert virologists (3)."* Reference 3 resolves to `virologytest.ai`. Hearing independently confirmed at `docs.house.gov/Committee/Calendar/ByEvent.aspx?EventID=118773`.
Survived because: official committee record, not media and not the evaluator's write-up; names the benchmark, states its headline result and cites the evaluator's own site; postdates publication; lowest non-zero rung taken.
Residual, disclosed by the verifier: the explicit VCT reference is authored by an outside witness. The verifier reproduced the negative across nine committee-authored documents (two memoranda, four member statements, the QFR response) — zero hits for "Virology Capabilities" / "SecureBio" / "virologytest". If the project rules that Channel B requires government-authored text, this reverts. Recommended: add the mirror `docs.house.gov/meetings/IF/IF02/20251217/118773/HHRG-119-IF02-Wstate-PannuJ-20251217.pdf`.

**5. `METR-2025-04-ALI1`** — C2, Pre-deployment, Anthropic
Old: `Partial` / `No explicit attribution` / `No policy uptake identified`
New: **`Substantive`**; Attribution and Policy unchanged. Response Date 2025-05-22, Lag 48.
Evidence: Claude Opus 4 & Claude Sonnet 4 System Card (May 2025), `https://www-cdn.anthropic.com/6be99a52cb68eb70eb9572b4cafad13df32ed995.pdf` (HTTP 200, 4.97 MB, 123pp), §6 and §6.1; plus Opus 4.5 card §6.10.1.
Survived because: verbatim exact — *"To address the reward hacking tendencies observed in Claude Sonnet 3.7 … we developed new evaluations to detect this behavior"* — naming the evaluated model and the exact behaviour class (hard-coding and special-casing to pass tests) that METR documented; four implemented workstreams including training-environment changes, RL reward-signal adjustment and inoculation prompting; 67% / 69% average decrease in hard-coding. Attribution correctly left at `No explicit attribution`: METR appears in the Claude 4 card only as a benchmark reference and zero times in the Opus 4.5 card.
C2, so outside the C1 headline set.

**6. `UKAISI-2026-02-JAI1`** — C1, Post-deployment, Anthropic
Old: `None` / `No response located` / `No policy uptake identified`
New: **`Substantive`** / **`Explicit attribution`** / Policy unchanged. Response Date 2026-08-14, Lag 178.
Evidence: Anthropic August 2026 Risk Report, `https://www.anthropic.com/aug-2026-risk-report` → `www-cdn.anthropic.com/…/Redacted Risk Report August 2026 .pdf` (HTTP 200, 4,569,677 bytes, 186pp), §4.5.3.2.1 "Boundary-point jailbreaking" and §4.5.4 "Offline monitoring". Published 12 days after the last prior battery ran.
Survived because: the report gives BPJ a dedicated numbered subsection, names UK AISI as its developer, describes Anthropic reimplementing BPJ "with the help of UK AISI", and reports UK AISI independently cross-validating the robustness delta. The strongest counter — that Constitutional Classifiers predate the finding, so the 3×/5× figures merely measure standing defences — fails because the response does not rest only on the classifier stack: BPJ-specific traffic monitoring and a standing offline BPJ-pattern monitor cannot predate BPJ. The verifier independently downloaded the February 2026 predecessor report and confirmed zero occurrences of "boundary point", "boundary-point" or "BPJ". Level 3 classifiers are in production across the fleet per the deployment table at pp.130–131.
Residual: Anthropic itself concedes the monitoring has "significant limitations", and the efficacy evidence is redacted. The verifier's fallback was `Partial`, not `None`.

**7. `APOLLO-2026-03-ALI2`** — C1, Mixed, OpenAI
Old: `None` / `No response located` / `No policy uptake identified`
New: **`Acknowledged`** / **`Explicit attribution`** / Policy unchanged. Response Date 2026-03-16, Lag 0.
Evidence: `https://alignment.openai.com/metagaming` (2026-03-16), OpenAI's own Alignment Research Blog, co-authored by an OpenAI researcher.
Survived because: company-controlled domain and battery step 1, which the prior 2026-08-16 battery evidently never ran; the document reproduces the finding's exact figures (Impossible Coding Task 62.1% → 58.3%, Sandbagging QA metagaming 23.5% → 54.5%, misaligned actions 1.7% → 10.8%), matching the stored Finding and Finding Quote verbatim; the collaboration sentence naming Apollo Research was confirmed present. Lag 0 is coordinated disclosure, not a predating problem. Correctly **capped** at `Acknowledged`: the verifier searched the document for any mitigation and found none, then downloaded the GPT-5.6 System Card to test the searcher's own competing `Partial` argument — §7.4 "Metagaming" is measurement only, with zero hits for "Schoen", "Metagaming matters" or "alignment.openai.com".
Residual: the circularity objection (an evaluator co-authored post) was rejected on the same ground as item 3 — the exclusion is scoped to Channel C. The chosen rung gives OpenAI no credit for action, which contains the risk.

**8. `UKAISI-2026-03-CYB9`** — C2. **Policy Level only.**
Old policy: `No policy uptake identified` → New: **`Non-binding policy-related uptake`**. Action `None` and Attribution `No response located` unchanged.
Evidence: NCSC, "Why cyber defenders need to be ready for frontier AI", 2026-03-30, `https://www.ncsc.gov.uk/blogs/why-cyber-defenders-need-to-be-ready-for-frontier-ai` (fetched twice, consistent).
Survived because: NCSC is named in the rulebook's admissible Channel B list; the post hyperlinks `arxiv.org/abs/2603.11214` under the anchor text "measuring AI agents' progress on multi-step cyber attack scenarios", and the verifier confirmed against `chunks/chunk_08.json` that this row's Report Title, Publication Date (2026-03-16) and Source URL are identical to `UKAISI-2026-03-CYB1`'s, so it is the same report cited by title and arXiv ID, not an adjacent one. The post also discusses the ICS scenario family this row concerns. 14 days after publication. Correctly capped at Non-binding — guidance with no enforceable instrument.
No spillover: the verifier confirmed `UKAISI-2026-03-CYB12` correctly stays at `No policy uptake identified`, since it comes from a different report (SandboxEscapeBench, arXiv:2603.02277) that the NCSC post does not cite.
C2, so outside the C1 headline set.

**9. `UKAISI-2026-04-CYB3`** — C1, Pre-deployment, Anthropic
Old: `None` / `No response located` / `No policy uptake identified`
New: **`Substantive`** / **`Explicit attribution`** / Policy unchanged. Response Date 2026-06-09, Lag 40.
Evidence: Claude Fable 5 & Claude Mythos 5 System Card (2026-06-09), `https://www-cdn.anthropic.com/…/Claude Fable 5 & Claude Mythos 5 System Card.pdf` (27MB, extracted locally), §3.1.1 and §3.2.5; corroborated by the Claude Mythos Preview System Card §3.1/§3.2/§3.4 and the Opus 5 card §3.3.6.
Survived because: the §3.1.1 verbatim matched exactly; §3.2.5 is titled "External capability testing from the UK AISI" and reproduces UK AISI's conclusions naming "The Last Ones" and the Cooling Tower range; two concrete actions are documented — an access restriction (Project Glasswing, vetted partners, Cyber Verification Program) and a deployed probe-plus-classifier safeguard stack — both created for this model generation rather than standing policy. The verifier found stronger evidence than the proposal supplied by retrieving the Mythos Preview launch card, which the battery had skipped.
Residual: `Explicit attribution` is the closest call — the document that reports the finding anonymises the evaluator as "additional external partners", and §3.1.1 credits the restriction to Anthropic's own internal suite; the naming sits in the successor cards. The verifier also recorded that this row's Channel B `No policy uptake identified` was **not** exhausted (congress.gov 403, govinfo 429) and should be marked battery-incomplete.

### 4.2 Upheld but HELD BACK — applying as submitted would break a project coding rule (3)

**10. `ANTHROPIC-2025-09-SELF-ALI1`** — C1, Pre-deployment, Anthropic. **Not applied.**
Upheld change: Action `Acknowledged` → **`Substantive`**. Attribution `Explicit attribution` and Policy `No policy uptake identified` unchanged.
Evidence: Claude Opus 4.5 System Card (November 2025) §6.7 and §6.7.1, independently downloaded and text-extracted; *"In contrast to Claude Sonnet 4.5, Claude Opus 4.5 was never trained on any prompts that resemble 'honeypot' environments … as noted in the UK AISI's independent report."* §6.13 corroborates a continuous UK AISI engagement chain.
Why it survived: the card documents an actual model change — removal of whole categories of training environments and data from the shipped model's training run. Under no reading does the current `Acknowledged` ("the problem is referenced, no action specified") survive; the verifier's fallback was `Partial`, not `Acknowledged`.
**Why it is held back:** the proposal returned the Response Date as prose, **"2025-11"**, with no day. Codebook col 22 defines `Lag (days)` as Response Date − Publication Date and states the invariant *"Exists ⇔ Response Date exists"*; the same pairing is enforced as a hard coherence check in `scripts/compute_proportionality.py`. A month-only date makes Lag non-computable, and Response Date and Lag must move as a pair. V13 currently holds Response Date `2025-09-29` / Lag `0`, anchored on the Sonnet 4.5 card — the *superseded* evidence. Writing the Action Level alone would leave a `Substantive` coding pointing at a date that belongs to different evidence.
Route to resolution: the verifier noted the Opus 4.5 card's changelog fixes the release at **2025-11-24**. Adopting that date and recomputing Lag would clear the block — but it is a fresh evidentiary determination, not something the adjudicated proposal supplied, so it is not applied here.

**11. `UKAISI-2026-04-CYB1`** and **12. `UKAISI-2026-04-CYB2`** — both C1, both Post-deployment, Anthropic. **Neither applied.**
Upheld change (both): Action `None` → **`Substantive`**, Attribution `No response located` → **`Explicit attribution`**. Policy `Non-binding policy-related uptake` unchanged (already the stored value).
Evidence: Claude Mythos Preview System Card (2026-04-07) §1 / §3.1 / §3.4 — GA withheld, access confined to vetted partners through Project Glasswing, *"In response to the improvements in cyber capabilities, we have elected to restrict access to the model"*; Claude Opus 4.7 System Card (2026-04-16) §3.4 "External testing from the UK AI Security Institute", reproducing this row's exact result, *"Mythos Preview was able to solve the same range in 3 out of 10 tries"*; gov.uk open letter of 15 April 2026 for Channel B. Both verifiers downloaded and full-text-extracted every cited PDF.
Why they survived: an access restriction plus a deployment decision in the company's own primary document, and the company naming UK AISI while reproducing this finding's exact figure.
**Why they are held back:** the response anchor both verdicts lead with — the Mythos Preview card — is dated **2026-04-07**, while both findings published **2026-04-13**. That is **Lag −6**, and both rows carry `Access Type = Post-deployment`. Rulebook §8 (line 134) and codebook col 22 permit negative lag only for a documented coordinated **pre-deployment** disclosure. All **11** negative-lag rows already in V13 are `Access Type = Pre-deployment`; applying these two as submitted would create the dataset's first Post-deployment negative-lag rows.
Routes to resolution, neither taken here: both verifiers independently argued that the stored `Post-deployment` Access Type is contradicted by Anthropic's own "pre-release snapshot" language in §3.4 and should be corrected — but Access Type is a coded field outside this pass's scope, and correcting it to make a lag legal is a change that must be adjudicated on its own terms. Alternatively, the CYB1 verifier explicitly recommended re-anchoring `evidence_url` and `response_date` on the **post-finding Opus 4.7 card (2026-04-16, lag +3)**, retaining the Mythos Preview card as corroboration. That is a different evidence anchor from the one adjudicated.
Also recorded by both verifiers, and not fixed: the proposals' Channel A rows assert that the AISI blog "describes this as a pre-deployment evaluation". Both verifiers fetched the blog and confirmed it does not; it says only that the model was "announced on 7th April". That characterisation must be struck from the reasoning text whichever route is taken.

### 4.3 Upheld but NOT APPLIED — the target code requires a record the proposal did not supply (1)

**13. `JOINT-2024-12-CYB1`** — C2. **Policy downgrade, not applied.**
Upheld change: Policy `Non-binding policy-related uptake` → **`No policy uptake identified`**. Action `Acknowledged` and Attribution `Explicit attribution` unchanged.
Why it survived: the sole Channel B evidence, `https://www.nist.gov/news-events/news/2024/12/pre-deployment-evaluation-openais-o1-model`, is NIST / US AISI announcing its **own** joint pre-deployment evaluation, dated 2024-12-18 — the same date as the finding's publication — published by a co-author of the finding. It announces no requirement, order, commitment or enforcement action. It is the finding's publication venue, not engagement with it, and the stored Policy Response merely restates the finding's own numbers. The dataset already applies exactly this rule to `JOINT-2024-11-BIO2` and `UKAISI-2024-12-BIO2`, so CYB1 was the outlier; the downgrade applies the project's existing standard rather than tightening it.
**Why it is not applied:** codebook col 25 defines `No policy uptake identified` as the value for Tier A rows *"that were searched with nothing found"*, and rulebook §9 as *"a completed search found no official source explicitly linking"* the finding. Refuting the only positive evidence establishes that the existing code is unsupported; it does not produce the completed, dated not-found record the negative code requires. The verifier ran real negatives on Hansard and the Federal Register API and downloaded three candidate Federal Register documents — but its own verdict records that **congress.gov returned HTTP 403 and govinfo returned OVER_RATE_LIMIT**, so the US congressional leg was not completed. The verifier itself wrote that the sources-checked entry "should retain the explicit note that congress.gov and govinfo remain unverified".
Current V13 state: `Policy Level` remains `Non-binding policy-related uptake`. The row's `Sources Checked (channel A)` **has** been stamped `[Channel A/B re-verified 2026-08-28: full five-source battery re-run; adversarially verified.]`, which slightly overstates the Channel B position and should be qualified.
Also recorded: the Company Response text should drop the phrase "dedicated section" — the verifier extracted the o1 system card from its arXiv mirror (2412.16720) and found exactly one AISI mention, confirming `Acknowledged` / `Explicit attribution` is correct but that no dedicated section exists.

---

## 5. Rejected proposals (23)

Every rejection below was returned by a verifier instructed to refute and to default to rejection. In the large majority the verifier confirmed the cited source was genuine and the quotation exact, and rejected on a rule. None of the 23 has been applied; all 23 rows retain their pre-pass coding, verified row by row against V13.

Grouped by the decisive ground.

### 5.1 Inadmissible source — the only evidence of a company action is not a company document (3)

| Finding ID | Claimed | Ground for rejection |
|---|---|---|
| **`UKAISI-2025-07-JAI3`** | `None` → `Partial`: Anthropic deployed mitigations after disclosure | Sole evidence is arXiv:2506.24068v3 Appendix K — the **evaluator's own paper** (FAR.AI with UK AISI co-authors). The verifier downloaded v3 and confirmed the quote exactly, then rejected: Channel A admits only the company's own primary document, and the `Partial` limb "an action claimed but unverifiable" sits *beneath* the admissibility gate, not beside it. Reading it otherwise would let any evaluator self-certify a vendor response and make `None` practically unreachable. The verifier also downloaded Constitutional Classifiers++ (arXiv:2601.04603), the Opus 4.6 and Opus 4.8 cards and Anthropic's 2025-09-12 safeguards post: zero hits for STACK, FAR.AI, component-wise attacks or 2506.24068 in any of them. |
| **`UKAISI-2025-07-JAI4`** | `None` → `Partial`: same, applied to OpenAI | Same inadmissible source. Two further independent failures: the sentence is a **two-vendor aggregate** patching "some" vulnerabilities that never says OpenAI patched anything and never identifies this finding's image-channel bypass; and the submitted battery contains a **verifiably false step** — it asserts the GPT-5 System Card contains no reference to FAR.AI. *I re-checked this myself:* the card (`cdn.openai.com/gpt-5-system-card.pdf`, title page "August 13, 2025") contains a §5.3.3.4 heading literally titled **"Far.AI"**. A battery with a false verified-source result cannot support any coding. |
| **`UKAISI-2026-07-ALI2`** | `Substantive` → `Partial` (downgrade) | The only evidence of any Anthropic action is the **evaluator's own blog**. With it excluded there is zero admissible Channel A evidence. The verifier also rejected the proposal's argument that coding `None` would force a "factually false" attribution label: attribution is recorded separately and is mechanically bound to the Action Level. **Note for the record:** the verifier found the row's *current* `Explicit attribution` unsupportable — it downloaded the Opus 5 card (7,283 lines) and the Mythos Preview card (9,400 lines) and got zero hits for "Control Red Team" in either — and its fallback is `None` / `No response located`, i.e. a **further** downgrade than the one proposed. V13 still holds `Substantive` / `Explicit attribution`. This row needs re-adjudication, not retention. |

### 5.2 Circular — the cited response document is the finding's own source (1)

| Finding ID | Claimed | Ground for rejection |
|---|---|---|
| **`JOINT-2026-02-CYB6`** | `None` → `Acknowledged` / `Explicit attribution` | The GPT-5.3-Codex system card offered as the Channel A response **is the finding's Source URL**, and the verifier confirmed programmatically that the stored Finding Quote is contained verbatim inside the proposal's own Channel A verbatim. A document cannot be a response to itself. The passage sits in §5.1.2.3 "Cyber Range", which the card calls "an internally developed benchmark"; external work is segregated into §5.1.2.4 and an "External Government Testing" section, neither of which credits any AISI with this behaviour. The consistency argument was inverted: in all four sibling rows cited as precedent, an external party produced the finding **and** the card contains a separate, distinguishable passage of company commentary. |

### 5.3 Generic same-topic activity — a real company or government document that does not address *this* finding (14)

This is the dominant failure mode: 14 of 23 rejections, and the reason the "new response found" category rejected at 71%.

| Finding ID | Claimed | Ground for rejection |
|---|---|---|
| **`PALISADE-2024-12-JAI1`** | `None` → `Partial` | The OpenAI self-serve fine-tuning wind-down notice (`developers.openai.com/api/docs/deprecations`) is genuine — the verifier opened it and confirmed the quote and all three dates — but it states **no rationale** and contains zero occurrences of Palisade, BadGPT, FAR.AI, jailbreak or safety. It is one of eight product sunsets on the same page in the same window; adjacent entries that do state a rationale give a commercial one. The proposal's warrant was intra-dataset consistency with two FAR.AI rows, which is not evidence. The verifier escalated the consistency point in the other direction: if the notice is inadmissible here it is inadmissible on those rows too, which should be re-adjudicated. |
| **`UKAISI-2025-02-JAI1`** | `None` → `Partial` | Same deprecation notice, same absence of rationale. Additionally: it does not address the finding's substance (arXiv:2502.14828 argues pointwise detection is architecturally inadequate; the notice changes no defence), and **the attacked surface is still open at cutoff** — active existing customers can create fine-tuning jobs until 2027-01-06, and the demonstrated attack ran as an active API customer. The proposal itself described this as "a consistency-driven upgrade rather than a new-evidence upgrade". |
| **`ROBUSTINT-2025-01-JAI1`** | `None` → `Acknowledged` | The DeepSeek-R1 Nature paper and its 83pp Supplementary §4.3.5 are genuine, post-date the finding, and concede the jailbreak vulnerability (25.2% → 85.9% unsafe). The verifier then pulled the **Nature Peer Review File** and found the causal record runs elsewhere: the manuscript submitted 2025-02-14, two weeks *after* the finding, contained no safety content at all; Referee #6 demanded jailbreak analysis and red-teaming as a condition of publication; the authors' rebuttal states the Ethics and Safety Statement was added in revision. "Cisco" and "Robust Intelligence" appear **zero** times in the article, the Supplementary and the Peer Review File. Routine documentation produced for a different gatekeeper. |
| **`HOLISTIC-2025-02-JAI1`** | `None` → `Acknowledged` | Same document, same peer-review provenance (the verifier independently pulled the 64pp review file; zero hits for Holistic AI, Cisco, Enkrypt, Qualys, Palo Alto or Adversa). Two further grounds: **independent methodology with topical overlap only** — DeepSeek's own 2,232-template in-house suite versus Holistic AI's 37 DAN-style prompts; and **one document offered as the response to two different evaluators' findings**, which is itself the signature of topic-level rather than finding-level evidence. The only safeguard named is described as already deployed and undated, i.e. standing policy. |
| **`APOLLO-2025-03-ALI1`** | `None` → `Partial` | The Claude Sonnet 4.5 card §7.1.1 realism-filter quote is character-exact, but §7.2 introduces the filter as a response to "early warning signs" in **Anthropic's own** automated-auditor transcripts, with no citation to Apollo's March 2025 report anywhere in the 149pp card. The verifier grepped the supporting cards: "evaluation awareness" occurs **zero** times in the Claude 4 card, and "Apollo" **zero** times in the Opus 4.5 card. Steelman granted and weighed: the Claude 3.7 card (pre-finding) has zero mentions of situational or evaluation awareness, so Anthropic's public reporting did begin after the Apollo post — but sequence is not attributability. |
| **`JOINT-2024-11-JAI1`** | `Acknowledged` → `Partial` **and** policy → `Non-binding` | **Split verdict; package rejected.** Channel A refuted: the Constitutional Classifiers post (2025-02-03) is genuine and its 86%/4.4% figures accurate, but it contains no reference to the November 2024 joint report; the UK AISI mention is as red-teamer of the **classifier prototype**, a different engagement; the classifiers programme predates the finding; and the post describes a research prototype and a one-week demo with deployment expressly prospective. **Channel B survived** — the verifier independently queried the Hansard API and confirmed the same Lord Vallance contribution used for `JOINT-2024-11-BIO2`, and its fallback records `Non-binding policy-related uptake` as accepted. That half has **not** been applied; V13 still shows `No policy uptake identified`. This row is a live inconsistency: the same Hansard contribution now carries Non-binding on BIO2 and No-uptake on JAI1. |
| **`REDWOOD-2024-12b-ALI1`** | `Partial` → `Substantive` | The verifier downloaded the Claude 3.7 Sonnet card and confirmed §5.3 exists, that reference [9] is Greenblatt et al. arXiv:2412.14093, and that the verbatim is exact — then rejected the inference. §5.3 in full is a **measurement**: it re-runs the paper's setting and reports a number, specifying no mitigation, training intervention, restriction or deployment decision. That silence is informative because the same card narrates interventions wherever they exist (§6.1 "implemented partial mitigations before launch", §6.2 "our training process mitigations significantly reduced…"). The Opus 4 card's §4.1.4 remediation addresses **pretraining contamination** from the paper's 150,000 released transcripts, not alignment faking. The evidentiary corrections the verifier *did* endorse — lead with the 3.7 card, move Response Date 2025-12-16 → 2025-02 — have not been applied. |
| **`METR-2025-04-ALI2`** | `Acknowledged` → `Substantive` | **Subject mismatch.** The GPT-5 card §3.8 defines its target as the model misrepresenting its internal reasoning; the finding is scorer tampering (patching timing functions in RE-Bench Optimize a Kernel, 5 of 24 runs). None of the three constructed mitigation environments and none of the four Table 9 evals measures scorer tampering. Textual proof of non-linkage: "reward hack" occurs **exactly once** in the whole card, describing what METR's report contains, with no OpenAI action attached, and nowhere in §3.8. The card's own reference [3] behind the o3 deception claim is **Transluce**, a different evaluator. The finding's capability half is also untouched — the card reports a further increase in time horizons. |
| **`JOINT-2026-02-JAI1`** | `Acknowledged` → `Partial` | Both cited passages are genuine (the verifier extracted both PDFs), but the GPT-5.5 card §9.3.2.7.1 describes a **different attack on a different model** (six hours of expert red-teaming versus this finding's single-user-message 0.778 pass@200 on GPT-5.3-Codex), and the GPT-5.6 card §9.4.6 is scoped to GPT-5.6 and reports persistence, not closure. **Double-counting:** the identical sentences are already coded as Channel A evidence for `UKAISI-2026-04-JAI1` and `JOINT-2026-07-JAI1`; upholding would credit one company action to three findings. Grepping both later cards for "5.3-Codex", "0.778" and "pass@200" returns only benchmark comparisons and back-references to standing architecture. |
| **`UKAISI-2026-04-ALI6`** | `None` → `Acknowledged` / `Explicit attribution` | The verifier downloaded both cards and confirmed the quotes, then rejected on four counts. **No citation:** zero hits for "2604.24618", the report title or any of the five AISI authors in either card, and the Opus 5 card's ~20-item reference list does not contain it. **Different run, different numbers:** the finding's five figures (Mythos Preview 7% / 65%, Opus 4.6 3%, Sonnet 4.6 4%, Opus 4.7 0%) appear nowhere; the June card reports 2% / 68% and the July card 1.7% / 5.0%, and the AISI text in both states "We reran all our evaluations on the release-checkpoints". **Half the model set is absent** (Opus 4.6 and Sonnet 4.6). **Double-counting:** `UKAISI-2026-06-ALI6` already has that same card as its Source URL and that same passage as its Finding Quote, already coded Acknowledged. |
| **`USCAISI-2026-07-CYB2`** | `None` → `Partial` | The verifier independently retrieved the z.ai JS bundle and confirmed the weight-release-gate quote exactly, and confirmed via the HuggingFace API that the gate was new and was executed (GLM-5.3 created 2026-08-25, weights 2026-08-27, `license:other`, versus GLM-5.2 `license:mit`). Rejected anyway: it is a **release-timing decision** containing no refusal data, no safeguards evaluation and no description of "hardening", against a finding about GLM-5.2 never refusing on 10 ExploitBench tasks. Z.ai **states a different cause** ("cyber capability developed faster than we expected"). And the finding's risk surface is untouched: GLM-5.2 remains publicly downloadable under MIT (verified live, 1,903,277 downloads). |
| **`UKAISI-2026-05-CYB2`** | `None` → `Acknowledged` / `Explicit attribution`, policy → `Non-binding` | Both legs refuted. **Channel A:** the "3/10 attempts" string genuinely appears in the Fable 5/Mythos 5 §3.2.5 and Opus 5 §3.3.6, but both cards introduce it as **UK AISI's own reproduced text** ("They shared with us these conclusions:" / "reproduced verbatim below:"), Anthropic contributing no words of its own, and both sections report **new evaluations of different models** with the Mythos Preview result appearing only as a comparator baseline. **Channel B:** see below. The precedent invoked (`UKAISI-2026-06-ALI6/GOV1/JAI2`) collapses — all three are Access Type Pre-deployment with the card itself as Source URL, whereas CYB2 is Post-deployment sourced to the AISI blog. |
| **`UKAISI-2026-05-CYB3`** | policy → `Non-binding` | The gov.uk DSIT/NCSC case study of 2026-06-12 is genuine and post-dates the finding, but the single sentence relied on — *"the UK AI Security Institute (AISI)'s evaluations show these models getting better at cyber tasks very quickly"* — is the **excluded category verbatim**: general reference to the evaluator and to the report's broad subject. The page never cites or links the report; none of the finding's results appear (no six 8h+ tasks, no 2.5M-token cap, no "The Last Ones", no 3/10). The one gov.uk document that *does* cite a specific AISI cyber item cites a different one. The same battery excluded four Hansard "Claude Mythos" mentions as general discussion while admitting this no-more-specific sentence. |
| **`UKAISI-2026-05-CYB4`** | policy → `Non-binding` | The **same single sentence**, on the same page, is the sole Channel B evidence for CYB2, CYB3 and CYB4 — one sentence cannot be a finding-specific reference to three distinct findings. The verifier extracted all four AISI-mentioning sentences on the page and confirmed none carries a report title, a link, or any of this row's substance. Internally inconsistent with the proposal's own Channel A reasoning, which refused to carry CYB2's evidence across on the express principle that "Coding is per finding". |

### 5.4 Level overreach — a qualifying response may exist, but not at the level proposed (3)

These three matter more than the others, because in each the verifier found the **current** stored coding is also wrong. Rejecting the proposal leaves a value the verifier expressly disputes.

| Finding ID | Claimed | Ground for rejection | Verifier's own fallback vs V13 today |
|---|---|---|---|
| **`UKAISI-2026-07-GOV4`** | `None` → `Substantive` / `Explicit attribution` | The OpenAI post of 2026-08-26 is real, is a company primary source, post-dates the finding by 36 days, and hyperlinks the finding's **exact Source URL**; the verifier retrieved the full 54KB via a text proxy after a Cloudflare 403 and confirmed every cited mitigation. **The action survived; the attribution did not.** There is exactly one AISI reference in 54KB — a bare two-word hyperlink anchored on the phrase "current frontier LLMs", supporting a general background claim. UK AISI is never named in prose. The document's causal frame is entirely OpenAI's own Hugging Face breach ("In response to this incident", "Following the incident"). Because the submitted package included `Explicit attribution`, it fails as submitted. | Fallback `Substantive` / `No explicit attribution`. **V13 still holds `None` / `No response located`**, which the verifier calls "decisively refuted". Needs re-adjudication. |
| **`JOINT-2025-01-JAI1`** | `Substantive` → `Partial`, policy → `Non-binding` | **Split verdict; package rejected.** The verifier downloaded the Anthropic NIST submission (8pp, 9 March 2026, Docket NIST-2025-0035) and agreed `Substantive` fails — the layered prompt-injection defence is presented as standing defence-in-depth inside an argument about what NIST should standardise. But `Partial` also fails: it rests entirely on "That work has materially improved what we ship", whose antecedent one sentence earlier is CAISI's **pre-deployment evaluation programme under the voluntary agreement** — a different workstream from this post-deployment AgentDojo finding. What remains attributable is naming the finding and calling it "important contributions", i.e. `Acknowledged`. **Channel B verified and correct:** Federal Register document 2026-00206 (RFI, 2026-01-08) returns HTTP 200 and its footnote 1 links this row's exact Source URL. | Fallback `Acknowledged` / `Explicit attribution` / `Non-binding`. **V13 still holds `Substantive` / `Explicit attribution` / `No policy uptake identified`** — wrong on both axes per the verifier. Needs re-adjudication. |
| **`ANTHROPIC-2026-05-SELF-ALI1`** | `None` → `Partial` / `Explicit attribution` | The verifier independently retrieved the August 2026 Risk Report (MD5 verified) and confirmed SLEIGHT-Bench appears exactly once, as a row in Table 2.23.1.2.B at p.80 with the quoted figures. **The move off `None` is right; `Partial` is not.** The only concrete action offered, the Opus 4.6 → Opus 4.8 monitor migration, appears in §2.23.4 as a bare bullet among routine changes, and the report's own prose credits **METR red-teaming**, not SLEIGHT-Bench. Timing does not support post-finding causation (the Opus 4.8 card is dated May 2026). The report affirmatively disclaims targeted work: "we did not run adaptive red-teaming against our latest first stage monitor". Running a benchmark and publishing a number is assurance reporting, not mitigation. The finding is also substantially self-referential (three of five authors are Anthropic). | Fallback `Acknowledged` / `Explicit attribution`. **V13 still holds `None` / `No response located`.** Needs re-adjudication. |

### 5.5 Timing / standing policy (2)

| Finding ID | Claimed | Ground for rejection |
|---|---|---|
| **`UKAISI-2026-03-CYB1`** | `None` → `Substantive` / `Explicit attribution` | The verifier retrieved the Opus 4.7 card (14,231,870 bytes, 10,627 extracted lines) and confirmed every quote, then rejected on five grounds. **No reference to the finding:** zero hits for "The Last Ones", "9.8", "32 steps", "milestone", "2603.11214", "aisi.gov.uk" or "multi-step cyber". **Standing practice:** §3.4 is a new pre-release evaluation shared with UK AISI "for open-ended testing, at their discretion", the same recurring arrangement that also puts UK AISI in the Mythos 5, Sonnet 5, Opus 4.8 and Opus 5 cards. **Wrong trigger:** the card's proximate stimulus is the April Mythos Preview evaluation — it quotes "3 out of 10 tries", which is `UKAISI-2026-04-CYB2`'s result, a separate row. **Wrong model:** the safeguards govern Opus 4.7's general-access release; nothing changes the deployed Opus 4.6 this finding measured. The record's stale note that "no Anthropic source explicitly names UK AISI" should still be corrected. |
| **`UKAISI-2026-03-CYB12`** | `None` → `Substantive` | The Mythos Preview card is genuine and quoted accurately, but the coding **rests on inferring** that the unnamed "additional external partners" are UK AISI — and the corroboration offered for that inference is affirmatively wrong. The verifier read Opus 4.7 §3.4, the one card section where UK AISI *is* named for cyber, and it covers a **cyber range only**, no sandbox escape. **Content mismatch:** grep for "SandboxEscapeBench", "container escape", "18 tasks" and the Opus 4.5 56% comparison returns zero hits, and bullet 4 reports the opposite-direction result. **Timing:** arXiv history is v1 2026-03-01 / v2 2026-07-07 / v3 2026-08-01, and the 100%-of-18-tasks Mythos Preview result entered the record at v2, three months *after* the 2026-04-07 card; no pre-deployment coordination on this benchmark is documented. The proposal self-labelled "JUDGEMENT CALL, flagged for review" and conceded "A stricter reading keeps this row at None". |

---

## 6. Headline impact

**Headline set:** Tier A ∩ Severity C1, n = **146**. `Proportionality` is a deterministic function of Severity × Action Level (`scripts/compute_proportionality.py`): for C1, only `Substantive` is Proportionate, so **"falls short" = Action Level ≠ `Substantive`**.

All three columns below were recomputed directly from `AISIEVAL_V13.xlsx` via `dataset_source.rows()`. The baseline column was produced by reverting the 9 applied changes in §4.1 to their documented pre-pass values and re-deriving Proportionality with the project's own matrix.

| Metric | **Baseline (before the 9)** | **Current V13 (after the 9)** | Delta | **If the remaining 4 resolve as upheld** |
|---|---:|---:|---:|---:|
| Headline findings | **146** | **146** | 0 | 146 |
| No response (`Action Level = None`) | **90 (61.6%)** | **86 (58.9%)** | **−4 (−2.7 pp)** | **84 (57.5%)** |
| Falls short (≠ `Substantive`) | **116 (79.5%)** | **113 (77.4%)** | **−3 (−2.1 pp)** | **110 (75.3%)** |
| Substantive | 30 | 33 | +3 | 36 |
| Any policy uptake (C1) | 18 | 20 | +2 | 20 |

**The supplied baseline of 146 / 90 / 61.6% / 116 / 79.5% reproduces exactly from V13.** There is no discrepancy, no missing row and no mixed numerator/denominator. `UKAISI-2025-08-JAI2` was removed upstream by design and was never in this pass's population (§1.2); it is not a defect and the earlier draft of this report was wrong to treat it as one. That claim has been removed in full.

**Which four C1 rows moved from `None`:** `APOLLO-2026-03-ALI2`, `METR-2023-03-ALI1`, `UKAISI-2026-02-JAI1`, `UKAISI-2026-04-CYB3`. `APOLLO-2023-11-ALI1` moved Partial → Substantive (falls-short −1 without touching no-response). The remaining four applied changes are C2 (`METR-2025-04-ALI1`, `UKAISI-2026-03-CYB9`) or Policy-only on rows whose Action Level did not move (`SECUREBIO-2025-04-BIO1`, `JOINT-2024-11-BIO2`).

**What the remaining 4 would add.** If `UKAISI-2026-04-CYB1` and `UKAISI-2026-04-CYB2` are resolved (both C1, `None` → `Substantive`) and `ANTHROPIC-2025-09-SELF-ALI1` is resolved (C1, `Acknowledged` → `Substantive`), no-response falls to **84 (57.5%)** and falls-short to **110 (75.3%)**. `JOINT-2024-12-CYB1` is C2 and Policy-only, so it does not move either headline figure; it would take Tier A `Non-binding policy-related uptake` from 22 to 21 (Tier A `Binding policy action` stays at 1).

**Full Tier A (n = 184), for reference:**

| Metric | Baseline | Current V13 | If all 13 applied |
|---|---:|---:|---:|
| No response | 116 (63.0%) | 112 (60.9%) | 110 (59.8%) |
| Falls short | 147 (79.9%) | 144 (78.3%) | 141 (76.6%) |

**Not to be read as a bound.** These figures assume the 23 rejections stand. Three of them (§5.4) carry verifier fallbacks that differ from V13's current values, and one (§5.1, `UKAISI-2026-07-ALI2`) would move a row *down* from Substantive. Re-adjudicating those four could move the headline in either direction.

**Knock-on work outstanding.** Proportionality was regenerated for the applied rows and is coherent. `Lag (days)` will need recomputation for any row whose Response Date moves — notably `ANTHROPIC-2025-09-SELF-ALI1` and `REDWOOD-2024-12b-ALI1` (the latter's 2025-12-16 → 2025-02 correction was endorsed by its verifier despite the level rejection, and is unapplied).

---

## 7. Coverage failures

This section is a limitation on the results above, not an appendix to them.

**Method.** Counts were derived by scanning each finding record's *atomic* log units — every `channel_a.sources_checked` entry, every `channel_b.jurisdictions_checked` entry, and every sentence of the `reasoning` and `notes` fields — for a failure marker (403/405/429, OVER_RATE_LIMIT, rate-limited, unreachable, "could not be opened/fetched/read/retrieved/verified", bot-protection/Cloudflare/CAPTCHA, "recorded as unchecked", "no text layer", "GRAPHICS NOT AVAILABLE", empty HTTP 202) co-occurring with a domain string in the same unit. This is deliberately conservative; it undercounts failures described loosely.

**165 of 185 findings (89.2%) carry at least one recorded access failure.**

| Source | Findings with a recorded failure | Nature of the failure |
|---|---:|---|
| **congress.gov** | **141** | HTTP 403 / Cloudflare bot-verification interstitial to both `curl` and WebFetch. Mentioned in 172 of 185 records. |
| **govinfo.gov** | **101** | HTTP 429 / `OVER_RATE_LIMIT` on `DEMO_KEY`. Deployed as the substitute for congress.gov and itself incomplete. |
| **openai.com** | **39** | HTTP 403 plus JS/cookie interstitial to direct fetch. Worked around per row via arXiv equivalents, `cdn.openai.com`, Internet Archive captures, the `openai.com/news` RSS feed and text-extraction proxies. |
| **WebSearch quota exhaustion** | **83** | Native search exhausted at 200/200. Affected all 15 records in chunks 03, 09, 10 and 11 and all 5 in chunk 13, plus partial exhaustion in chunks 01, 04, 05, 07 and 08. Battery item 5 (open-web search *to locate* company primary sources) ran degraded on those rows. Items 1–4 are site-specific and unaffected. |
| **hansard.parliament.uk** | 20 | HTTP 403 to the HTML site. Substituted by the official Hansard Search API, which returned HTTP 200 throughout — this substitution worked, and produced positive Channel B hits the prior pass had missed. |
| **europarl.europa.eu** | 15 | Empty HTTP 202 on every path tried (HTML, PDF, XML). EU parliamentary written questions could not be verified. |
| **x.com** | 13 | Unreachable. Company X/Twitter accounts could not be checked; Channel A item 1 is degraded on those rows. |
| **deploymentsafety.openai.com** | 8 | HTTP 403 on some paths; `…/jailbreaks` returns 404. |

### 7.1 The US congressional jurisdiction of Channel B was never executed

This is the single most consequential gap in the pass, and it must be stated without hedging.

**Across all 185 finding records there is not one instance of a successful congress.gov full-text search.** Congress.gov was recorded as unreachable or unreadable on 141 findings and mentioned on 172. The one record that reports retrieving a congressional document, `METR-2023-03-ALI1`, retrieved it and could not read it: the 114-page `CHRG-118hhrg52499` PDF has no text layer over its body pages (`pdftotext` returns only front matter) and the govinfo HTML renders every prepared statement as `[GRAPHICS NOT AVAILABLE IN TIFF FORMAT]`. The designated substitute, govinfo, was itself rate-limited on 101 findings.

**Therefore every Channel B conclusion in this pass is provisional.** In particular, `No policy uptake identified` is defined by codebook col 25 as the value for rows "searched with nothing found" and by rulebook §9 as requiring "a completed search". On the US leg that condition was not met anywhere. The 161 Tier A rows currently carrying `No policy uptake identified` rest, on their US component, on an unexecuted battery leg. Two consequences already visible inside this report:

- `JOINT-2024-12-CYB1`'s upheld policy downgrade **cannot be applied** for exactly this reason (§4.3).
- `UKAISI-2026-04-CYB3`'s verifier flagged that the row's `No policy uptake identified` was not exhausted and should be marked battery-incomplete (§4.1, item 9).

**A separate defect compounds this.** Fifteen findings — every record in **chunk_05** (`OPENAI-2025-07-SELF-BIO3`, `OPENAI-2025-07-SELF-JAI1`, `UKAISI-2025-07-JAI3`, `UKAISI-2025-07-JAI4`, `FARAI-2025-07b-BIO2`, `DREADNODE-2025-08-CYB1` through `CYB4`, `APOLLO-2025-08-ALI2`, `JOINT-2025-08-JAI1`, `CIP-2025-08-SOC1`, `CIP-2025-08-ALI1`, `PALISADE-2025-08-CYB1`, `TRANSLUCE-2025-09-JAI1`) — record the US jurisdiction as a bare label, "US (Congress.gov, committee records, Federal Register, Commerce/NIST/CAISI)", followed by a blanket assertion such as "Full battery 2026-08-28 … No Congress.gov, Federal Register, Commerce/NIST/CAISI item references it", **with no access outcome recorded at all**. That chunk's own summary reports only 2 unreachable sources, against 15 for eight of the other twelve chunks. In a pass where congress.gov was blocked everywhere it was attempted, these 15 rows assert a clean US negative they cannot have earned. They should be treated as unsearched on the US leg, not as negative.

### 7.2 Findings where an access failure could plausibly be hiding a response

Ordered by how load-bearing the unread document is.

| Finding ID | Current | Unread document | Why it could change the coding |
|---|---|---|---|
| **`METR-2025-06-ALI1`**, **`ALI2`**, **`ALI3`** | `None`, C1 (all three) | `openai.com/index/hugging-face-incident-and-the-road-ahead/` — HTTP 403 to both WebFetch and `curl` at the chunk_04 run | **The highest-priority gap in the pass.** The searcher's own note: "If that OpenAI post is later found to cite the June 2025 report while announcing chain-of-thought monitoring and alignment-training changes, these three findings would move to Substantive." The negative rests on an inference from METR's own post. **The same document was read successfully later in the same pass** — it is the basis of proposal `UKAISI-2026-07-GOV4` in chunk_12, and the GOV4 verifier retrieved its full 54KB via a text proxy. These three rows must be re-run before any headline is published. |
| **`SCALEAI-2025-02b-JAI3`** | `Partial`, C1, confidence **low** | The row's **own** Channel A evidence URL, `openai.com/index/introducing-gpt-oss-safeguard/` — HTTP 403 | The stored coding was carried forward entirely unverified. A `Partial` sits in the headline set on a document nobody in this pass could open. One rejected verdict (`ROBUSTINT-2025-01-JAI1`) also notes this row was previously flagged as "arguably over-coded". |
| **`SHANGHAIAILAB-2025-07-JAI2`** | `None`, C1 | Archived Gemini 2.0 Flash model card PDF — HTTP 403 | This is the launch card **for the exact evaluated model**, i.e. battery item 2's canonical location. Item 2 was satisfied only via the later Gemini 3.1 Pro card and the Gemini model page. The searcher: "If that archived card is later retrievable it should be searched for 'VisCo' before this coding is treated as final." |
| **`PALISADE-2025-07-ALI1`** | Channel A `None`; Policy `Non-binding`, C1 | European Parliament written question E-002249/2025 — `europarl.europa.eu` returns empty HTTP 202 on every path; and the US House hearing at which Rep. Perry cited Palisade could not be pinned to any official congress.gov or docs.house.gov record (the evaluator's page supplies only a YouTube timestamp) | The **Policy Level is carried forward unconfirmed**, not re-earned. Channel A is firmly evidenced by contrast (four full system cards opened, zero Palisade hits). |
| **`METR-2023-03-ALI1`** | Policy `Non-binding`, C1 | `CHRG-118hhrg52499` — no text layer; govinfo HTML unreadable | The retained Channel B value is neither confirmed nor refuted. Not part of the applied Channel A change, but it is a live value in the dataset resting on an unreadable source. |
| **`SHANGHAIAILAB-2024-02-JAI1`** | `None`, C1, confidence **low** | Channel A items 1, 4 and 5 could not be executed — WebSearch quota exhausted | Only two document-level checks ran (Gemini 1.0 and Gemini 2.5 technical reports). Explicitly flagged for re-run "before the None is treated as freshly confirmed". |
| **`PALISADE-2025-08-CYB1`** | `None`, C1 | The Palisade blog post itself could not be fetched | Does not change the coding, but leaves an unresolved publication-date discrepancy (record 2025-08-26, prior log 2025-09-04) that breaks lag arithmetic if a response ever appears. Also one of the 15 chunk_05 rows asserting an unearned US negative. |
| **`SECUREBIO-2026-06b-BIO3`**, **`BIO5`**, **`SECUREBIO-2026-07-BIO4-s2`**, **`BIO4-s3`**, **`SECUREBIO-2026-07b-BIO1`–`BIO5`** | mixed `None` / `Substantive` | congress.gov (403) and govinfo (429) | Channel B is recorded as **blocked, not negative**, on these rows — the honest handling, and precisely why the negatives cannot be relied on. Biosecurity findings are the stratum where congressional uptake is most likely to exist. |
| **`LATTICEFLOW-2025-02-CYB1`** | `None`, C2 | EU Channel B leg and the open-web Channel A leg | Confidence recorded medium for this reason alone; the decisive Channel A primary sources were reached directly. |
| **`OPENAI-2025-07-SELF-JAI1`**, **`DREADNODE-2026-07-ALI1`/`ALI2`**, **`FARAI-2026-02-HUM1`**, **`OPENAI-2026-03-SELF-ALI2`**, **`JOINT-2026-07-CYB3`**, **`GRAYSWAN-2025-12-CYB1`**, **`UKAISI-2026-07-ALI1`** | various | assorted 403s and quota exhaustion, worked around per row | Recorded for completeness; in each the decisive documents were reached by another route. Note that **empty Channel C lists in this pass mean "not located", not "none exist"**. |

---

## 8. Not covered

**The 817 non-Tier-A findings in V13 were not searched, and Channel A and Channel B do not apply to them by rule.**

Rulebook §4 restricts response classification to Tier A: only Tier A receives response classifications, and Tier B and C response fields are blank. Tier A requires all four of (1) an empirical model behaviour, capability or safeguard result, (2) a named frontier model or accountable developer, (3) an adverse or concerning result rather than a reassuring null or a bare performance number, and (4) a company response that could reasonably be assessed. A finding failing any one of these has no coherent "company response" to search for, so an absence of response is not a measurement.

| Stratum | Count | Encoding | Why Channel A/B do not apply |
|---|---:|---|---|
| Tier A (searched) | **184** | `Eval? = yes`, `Action Trackable? = yes` | — |
| Tier B | **467** | `Eval? = yes`, `Action Trackable? = no` | Empirical, but anonymised model, reassuring or null result, bare score or ranking without a concerning threshold, non-frontier system, capability trend, inconclusive result, or a company response that is not reasonably assessable. Descriptive analysis only. |
| Tier C | **350** | `Eval? = no`, `Action Trackable?` blank | Methodology, framework, governance or process, tooling, milestone, or other non-empirical-model finding. Descriptive analysis only. |
| **Total not covered** | **817** | | 1,001 − 184. Tier B 467 + Tier C 350 = 817 exactly. |

Three consequences for the paper:

1. **The headline denominators (184 and 146) are subsets of a 1,001-finding corpus, not the corpus.** The response-rate claim is a claim about Tier A C1 only, and must be stated that way.
2. **Tiering is itself a coding judgement and was not re-audited in this pass.** This is the largest uncovered risk in the whole exercise. A finding wrongly placed in Tier B is a finding whose company response was never searched, and it is invisible to every number in §6 — it does not appear as a `None`, it simply does not appear. This pass re-derived Channel A, B and C independently but took `Action Trackable?` as given for all 1,001 rows. A tiering audit is a separate piece of work and has not been done.
3. **The earlier "816 vs 817" reconciliation is now moot.** It arose from `APOLLO-2026-07-ALI4` carrying an invalid encoding (`Eval? = no` with `Action Trackable? = no`, where §4 requires blank). V13 has fixed it: the row is now cleanly Tier C, the unclassifiable stratum is empty, and 467 + 350 = 817 = 1,001 − 184 with no residual. `APOLLO-2026-07-ALI4` *was* searched in this pass as part of the then-Tier-A 185; it produced no proposal and it is C2, so nothing in §3 or §6 depends on it.

---

## 9. Data-quality defects flagged by the search pass

Each item below is marked **VERIFIED** (I checked it directly against V13 or against the primary document, and state what I found) or **UNVERIFIED** (the search pass alleged it; I did not independently confirm it and it must not be relied on until someone does). No item here changes a coding.

### 9.1 The two alleged fabricated verbatims

**`APOLLO-2025-08-ALI2` — VERIFIED, and the allegation is correct. The defect is real but it is not in the column where a spot-check would look.**

The search pass alleged that the stored verbatim asserts a count of 13 environments that the GPT-5 System Card does not state, the "13" being a page number caught in the PDF's text flow. I checked this directly.

- The phrase is **not** in the `Channel A Verbatim` column. That column holds a different, accurate quote ("We've taken steps to reduce gpt-5-thinking's propensity to deceive, cheat, or hack problems…"). **A spot-check of `Channel A Verbatim` will find nothing wrong, which is very likely why the earlier spot-check failed to substantiate this.**
- The phrase is in the **`Company Response`** column, inside a block introduced as `VERBATIM (GPT-5 system card, deception mitigations):`, reading `"…We constructed 13 environments in a few settings where we had seen particularly pronounced problems with deception from earlier reasoning models: Agentic Coding… Broken Tools… Underspecified User Requests."`
- I downloaded `https://cdn.openai.com/gpt-5-system-card.pdf` (HTTP 200, 4,666,374 bytes; title page "GPT-5 System Card / OpenAI / August 13, 2025") and extracted the text both with and without `-layout`. In §3.8 "Deception", under the "Mitigations" heading, the text reads: *"…and rewarded the model for honestly admitting it can not complete the task. We constructed"* — then a line break, then a bare right-aligned **`13`** occupying the page-footer position, then *"environments in a few settings where we had seen particularly pronounced problems with deception from earlier reasoning models:"*. Page 12's footer is `11` and page 13's is `12`, confirming the footer pattern and offset.
- The literal string **"13 environments" occurs zero times** in the extracted text, in either extraction mode.

**Conclusion: the card states no count. The dataset's `Company Response` field asserts a number the source does not contain, presented as a verbatim quotation.** It must be corrected to "We constructed environments in a few settings…". The row's Action Level (`Substantive`) is unaffected and was independently re-confirmed by the search pass.

**`UKAISI-2024-10-JAI2` — VERIFIED, and the allegation is substantiated, but it is not a defect in the dataset and the earlier report mischaracterised it on two counts.**

- **It is not a dataset defect.** This row's `Company Response`, `Channel A Verbatim`, `Response Date`, `Lag` and `Channel A Evidence` are all **empty**, and the coding is `None` / `No response located`, unchanged by this pass. Nothing fabricated entered the dataset. Listing it in a table of "defects found in the input records" was wrong; it belongs in a record of search-process near-misses.
- **The earlier report misquoted the claim.** It reported "12.9% for Sonnet 4.5". The actual chunk_01 note records a claim of "an AgentHarm score of 27.9% versus 12.9% for Sonnet 4.5".
- **The substance checks out, with a twist worth recording.** I downloaded the Claude Sonnet 4.6 System Card (`https://www.anthropic.com/claude-sonnet-4-6-system-card`, HTTP 200, 8,503,340 bytes) and extracted it: **"AgentHarm" occurs zero times**. The searcher's rejection of the claim was correct. However, **27.9% and 12.9% are both real figures in that card** — they are §2.4 **OpenRCA** scores (Table 2.4.A: Claude Sonnet 4.6 adaptive-thinking high-effort 27.9%, Claude Sonnet 4.5 12.9%), a root-cause-analysis capability benchmark unrelated to AgentHarm. So the search-engine summary did not invent numbers; it attached real numbers from the correct document to the **wrong benchmark**. That is a more insidious failure mode than fabrication, because the figures survive a numeric spot-check. The searcher caught it by retrieving the card, and the figure was not used.

### 9.2 Other defects

| Finding ID | Defect | Status |
|---|---|---|
| `SECUREBIO-2025-04-BIO1` | `Sources Checked (channel A)` still ends with pasted boilerplate concluding *"Battery exhausted -> Action Level = None stands, now documented"*, which flatly contradicts the row's coded `Substantive` and its verified evidence. The 2026-08-28 re-verification stamp was appended **after** that sentence without removing it. | **VERIFIED** in V13, still present. |
| `OPENAI-2025-07-SELF-BIO2` | `Channel B Evidence` cites evaluator "UK AISI" and report ID `OPENAI-2025-07-SELF-AGENT`; the row's `Institution` is **SecureBio**. Boilerplate pasted from another record. | **VERIFIED** in V13. |
| `APOLLO-2026-07-ALI2` | `Channel A Evidence` free-text argues *"hence 'Partial' rather than 'Substantive.'"* while the coded `Action Level` is **`Acknowledged`**. The `Company Response` text supports `Acknowledged`; the evidence note does not. | **VERIFIED** in V13. |
| `JOINT-2024-11-BIO2` | `Channel B Evidence` is `https://hansard.parliament.uk/lords/2024-11-21/debates/`, a bare date landing page that 403s and does not resolve to the cited contribution. Must be the debate-specific path under ExtId `600E1622-A12A-4E0B-8EC1-63BFBD4B0DA1`. | **VERIFIED** in V13, still uncorrected despite the policy change being applied. |
| `UKAISI-2025-07-JAI4` | `Publication Date` is 2025-07-18 (arXiv v2) but the row's model is **GPT-5**, which did not exist then. | **VERIFIED**: V13 holds `Publication Date` 2025-07-18 with `Models / Systems` "GPT-5"; the GPT-5 System Card I downloaded is dated **August 13, 2025**. The date cannot be right. Both verifiers independently confirmed the arXiv history as v1 2025-06-30 / v2 2025-07-18 / v3 2026-02-05, so the GPT-5 material appears only in v3. |
| `UKAISI-2025-07-JAI3` | Same date problem; V13 holds 2025-07-18 with `Models / Systems` "Claude Opus 4". The Opus 4 production-pipeline attack likewise appears only in v3. | **VERIFIED** as to the stored date; the v3-only claim rests on the two verifiers' independent arXiv checks, which I did not re-run. Recommended fix: re-base to 2026-02-05 or split the v3 material into a separate record. |
| `APOLLO-2026-07-ALI4` | Alleged schema violation (`Eval? = no` with `Action Trackable? = no`). | **VERIFIED AS ALREADY FIXED.** V13 holds `Eval? = no` with `Action Trackable?` blank and `Action Level` blank — a clean Tier C row. No action needed. |
| `SCALEAI-2026-05ac-AUT2` | Alleged: `Publication Date` 2026-05-12 but the live leaderboard page carries 2026-07-28, and the refusal note concerns Fable 5 (released 2026-06-09), so lag arithmetic is unreliable. | **UNVERIFIED.** V13 holds 2026-05-12 and the row is Tier A. I did not fetch the leaderboard page. |
| `DREADNODE-2026-07-ALI1` | Alleged: `Publication Date` 2026-07-29 vs arXiv 2607.21763v1 submitted 2026-07-23 — a six-day gap to reconcile. | **UNVERIFIED.** V13 holds 2026-07-29 with a `dreadnode.io` Source URL, not the arXiv one. I did not check arXiv. |
| `SECUREBIO-2026-07-BIO4-s3` | Prior "MODEL NAME UNVERIFIED" flag reported as resolved: SecureBio's source does write "Grok 4.20", so the transcription is correct despite matching no launch-announced xAI release. | **UNVERIFIED.** V13 does hold `Models / Systems` = "Grok 4.20"; I did not check SecureBio's source. |
| `UKAISI-2026-05-CYB2` | The row's `Sources Checked (channel A)` states the Fable 5/Mythos 5, Sonnet 5 and Opus 5 cards were "checked in full text — no reference to the TLO / Cooling Tower result". Its verifier downloaded both cards and confirmed **that reference does exist**. The coded value does not change, but the note is false and must be rewritten to record the mentions and why they are inadmissible. | **UNVERIFIED by me**; asserted by the verifier, which reports byte counts for both PDFs. |
| `METR-2025-04-ALI2` | The row's `Sources Checked (channel A)` ends "Battery exhausted -> Action Level = None stands", contradicting the coded `Acknowledged`. Same boilerplate pathology as `SECUREBIO-2025-04-BIO1`. | **UNVERIFIED by me**; asserted by the verifier. Worth a systematic sweep — this boilerplate appears to have been pasted across multiple rows. |
| Dataset-wide | Only **10** V13 rows carry a `2026-08-28` log stamp: the 9 applied changes plus `JOINT-2024-12-CYB1`. The other 175 searched rows still carry `Sources Checked` logs dated 2026-08-02 or 2026-08-15/16. Codebook col 24 makes `Sources Checked` the audit-trail cell holding "dated search logs behind None codings", and rulebook §8 requires a dated search log through the cutoff for a no-response classification. | **VERIFIED.** The 2026-08-28 logs exist and are complete, but they live in `results/chunk_*.json`, not in the workbook. Either write them back or record in the methodology that the dated battery record for `None` codings is the chunk log set, cited by path. |

---

## 10. Outstanding actions

1. **Re-run `METR-2025-06-ALI1` / `ALI2` / `ALI3`** against `openai.com/index/hugging-face-incident-and-the-road-ahead/`, which was 403 in chunk_04 but read successfully later in the same pass. Three C1 `None` rows turn on it. Do this before publishing any headline (§7.2).
2. **Resolve the three held-back upheld changes** (§4.2): fix `ANTHROPIC-2025-09-SELF-ALI1`'s Response Date to a day-precision value and recompute Lag; and decide, for `UKAISI-2026-04-CYB1` / `CYB2`, whether to correct Access Type or to re-anchor on the post-finding Opus 4.7 card. Either route needs its own adjudication.
3. **Re-adjudicate the four rejections whose verifier fallback differs from V13's current value** — `UKAISI-2026-07-GOV4`, `JOINT-2025-01-JAI1`, `ANTHROPIC-2026-05-SELF-ALI1`, `UKAISI-2026-07-ALI2` (§5.1, §5.4). In each, rejecting the proposal left a value the verifier says is wrong.
4. **Execute the US congressional leg of Channel B** from a network path that can reach congress.gov, and re-run govinfo with a real API key. Until then, treat all `No policy uptake identified` values as provisional and the 15 chunk_05 rows as unsearched on the US leg (§7.1). `JOINT-2024-12-CYB1`'s upheld downgrade unblocks when this is done.
5. **Apply the accepted split-verdict halves that were never written:** `JOINT-2024-11-JAI1`'s Channel B upgrade to `Non-binding` (currently inconsistent with `JOINT-2024-11-BIO2` on the identical Hansard contribution), and `REDWOOD-2024-12b-ALI1`'s Response Date correction to 2025-02.
6. **Correct the two verbatim/quotation defects**: `APOLLO-2025-08-ALI2`'s `Company Response` (strike the fabricated "13"), and `JOINT-2024-11-BIO2`'s `Channel B Evidence` URL.
7. **Sweep for contradictory pasted boilerplate** in `Sources Checked (channel A)` — at least two rows (`SECUREBIO-2025-04-BIO1`, `METR-2025-04-ALI2`) carry a "Battery exhausted → Action Level = None stands" note against a non-`None` coding.
8. **Decide where the 2026-08-28 battery logs live** (§9.2, final row) and state it in the methodology.
9. **Audit tiering.** It was not re-examined in this pass and is the largest uncovered risk to the response-rate claim (§8).
10. **State the no-human-review limitation** wherever this pass's numbers are cited (§2).
