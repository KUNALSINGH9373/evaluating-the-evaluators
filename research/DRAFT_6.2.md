# Draft 6.2 — Do third-party frontier AI evaluations matter?

Kunal Singh¹\*, Max Kamachee¹, Jonas Raedler¹, Stephen Casper²·³·¹

¹ MATS Research  ·  ² Harvard Kennedy School  ·  ³ Harvard Berkman Klein Center

\* Corresponding author: singhkunal9373@gmail.com

> **Anonymization note.** This block, and the study-materials links in Appendices C, E and J, identify the authors. Both must be removed or replaced with an anonymized mirror before any double-blind submission.

**Dataset:** AISIEVAL V13 — 1,136 findings · 453 reports · 453 source URLs · 46 institutions · 17 March 2023 – 27 August 2026 · corpus cutoff 29 August 2026.
**Status of numbers:** every figure below was recomputed from the workbook on 10 September 2026. Structural validator PASS (0 violations); duplicate suite 0 duplicates; `verify_charts.py` PASS across all 38 figures.
**Changes from Draft 6.1:** corpus corrected (attribution audit, report-identity merge, §5 accountable-company splits); window opens 2023-03-17 rather than 2020; headline 150/188 → **152/190**; Tier B/C redefined; NIST AI 600-1 removed from severity provenance; policy-record binding case corrected; AI-assisted search disclosed (Appendix B); response-search protocol published.

---

## Abstract

Government AI institutes and independent evaluators study frontier AI systems to identify, evaluate, and better understand potential risks. Yet identifying and evaluating a risk does not itself mitigate it. We examine whether companies act on published findings from third-party evaluations of their frontier AI systems. The analysis covers publicly documented findings from government AI institutes and independent evaluation organizations from 2023 to August 2026. We trace downstream responses through three channels: company responses and model updates; parliamentary and regulatory action; and documented media and academic coverage.

The corpus contains 1,136 findings, of which 232 concerned adverse empirical results about named systems for which a company response could reasonably be expected. Of the 190 that met our predefined significant-risk threshold, 152 (80%) lacked a specific publicly documented company response meeting our proportionality criteria; 114 (60%) had no located company response of any kind. The shortfall persists under every alternative counting unit we tested — from 76.2% weighting by institution to 84.3% weighting by report — and after adjusting for the clustering of findings within reports. One finding in the entire corpus was connected to binding policy action.

Taken together, these results suggest that, based on publicly available information, there is only limited reason to trust that third-party evaluations of frontier AI systems consistently lead to proportionate, attributable, and verifiable responses. Comparing the accountability structures currently in place for frontier AI systems with those established by oversight bodies in other industries, including food, drugs, energy, transportation, and finance, we conclude that formal mechanisms for access, response, remediation, verification, and follow-up inspired by governance in these other sectors could increase the consistency with which AI evaluations translate to meaningful action.

---

**Table 1. Company-response outcomes among the 190 significant-risk (C1) findings in the accountability set.**

| Outcome | n (% of 190) | Illustrative case |
|---|---|---|
| **No publicly documented company response located** | **114 (60.0%)** | UK AISI's AgentHarm benchmark found six named models complying with malicious agentic requests at high rates; the worst case recorded an 82.2% harm score against a 1.1% refusal rate. No publicly documented company response was located for any of the six model-specific findings. |
| **Partial or acknowledged response; no substantive mitigation confirmed** | **38 (20.0%)** | UK AISI found a universal jailbreak against GPT-5.5 within six hours of testing. OpenAI reported changes to its safeguard stack, but a configuration issue in the version supplied to UK AISI left the institute unable to verify the final configuration before deployment. |
| **Proportionate, attributable response documented** | **38 (20.0%)** | UK AISI and US CAISI evaluators found multiple universal jailbreaks bypassing the Constitutional Classifiers protecting Claude Opus 4 and 4.1. Anthropic attributed its response to these findings and, rather than patching the individual exploit, restructured its safeguard architecture to address the underlying vulnerability class. |

*Rows 1 and 2 together comprise the 152-of-190 (80.0%) accountability gap analyzed in §4.1. Responses were searched through 29 August 2026. Partial (21) and Acknowledged (17) are combined in row 2; the full four-level breakdown is in Table 5.*

**Figure 0.** `charts/20_accountability_pipeline_funnel.png` *Accountability pipeline: from 1,136 public evaluation findings to the 232 Tier A accountability set, the severity classification to 190 C1 findings, and the response outcome for each. A finding counts toward the gap when the named company shows no located public response, or only a partial or acknowledged one.*

---

## 1 Introduction

Frontier AI system evaluations have become a prominent component of AI governance. Government AI institutes and independent evaluators test advanced systems for dangerous capabilities, safeguard failures, and other risks, often with access and technical expertise unavailable to the general public. These evaluations can provide evidence about an AI system's risk beyond the boundaries of the developers' own disclosures [1]. However, identifying a risk is not the same as reducing it. An evaluation can document a serious vulnerability without prompting a developer's response, which could lead to delay in deployment, additional review, or verification of remediation. Therefore, the practical value of the evaluation depends partly on what happens after the finding is communicated or published.

Across the 190 significant-risk findings for which a company response could be assessed, 152 (80%) had no publicly documented response meeting our proportionality criteria, while only 38 (20%) received a proportionate response (Table 1). The shortfall appeared among findings reported by both government institutes and independent evaluators and was substantially greater for post-deployment than pre-deployment evaluations. An absence of a publicly documented response does not establish that no action occurred or that the finding was of less importance. Preventive, private, and unattributed company actions may leave no public trace, so our results describe the public record rather than companies' internal conduct.

This distinction is worth stating fully, because the paper's central measure depends on it. A finding's importance is not determined by whether it is followed by publicly documented action, and we do not conflate the two. An evaluation that does not identify a concerning or actionable problem is not thereby unsuccessful. Conversely, the absence of publicly documented action does not establish that no action occurred. Anticipation of an evaluation may prompt a company to conduct additional due diligence before testing begins; evaluators may communicate findings privately; and companies may implement changes without publicly attributing them. These preventive, private, or unattributed responses leave no public trace and are not captured here.

Finally, we compare the frontier-AI evaluation ecosystem with oversight institutions in pharmaceutical regulation, nuclear safety, transportation, finance, and related domains. These institutions are not direct templates for AI governance, but illustrate formal mechanisms for access, response, remediation, verification, escalation, and continuing follow-up.


---

## 2 Background

### 2.1 Government AI institutes

Government AI institutes emerged as technical public bodies focused on evaluating the safety of advanced AI systems. The first institutes were established in the United Kingdom, the United States, and Japan during 2023 and 2024. Their initial mandates broadly combined safety evaluation, research, standards development, and international cooperation [2].

Since then, these institutes have developed in different directions. In February 2025, the UK AI Safety Institute was renamed the AI Security Institute and its remit was refocused on risks with security implications, including cyberattacks, chemical and biological threats, fraud, and other forms of criminal misuse [3]. It remains within the Department for Science, Innovation and Technology and focuses on research and evaluation rather than regulatory enforcement. In June 2025, the US AI Safety Institute was re-established as the Center for AI Standards and Innovation (US CAISI) within the National Institute of Standards and Technology. Its work combines model evaluation and national-security assessment with measurement science, guidelines, and voluntary standards development [4]. Japan's AI Safety Institute, based within the Information-technology Promotion Agency, primarily develops evaluation methods, guidance, standards, and testing infrastructure [5]. France's INESIA, launched in 2025, is not a new standalone agency but a coordinated network of existing public bodies working on systemic-risk analysis, model evaluation, and support for the implementation of AI regulation [6].

The different institutional structures suggest that government AI institutes do not follow a fully uniform institutional model. They vary in focus, structure, access arrangements, and connection to standards or regulatory processes. Most findings examined in this paper are technical outputs that may inform developers and policymakers but do not themselves compel a company response or remediation. We use "government AI institutes" as an umbrella term for the public bodies that conduct or coordinate external evaluations of advanced AI systems.

### 2.2 Independent AI system evaluators and third-party auditing

Independent evaluators are defined as non-government organizations — including non-profit organizations, for-profit evaluation firms, and academic research groups — that are institutionally separate from the developer whose system they evaluate, and that conduct and publicly report frontier-AI evaluations. These include generalist evaluators such as METR and Apollo Research and domain-specific organizations such as SecureBio. Independent evaluators also test frontier systems for dangerous capabilities, safeguard failures, and other risks, but differ from government institutes in institutional status, funding, access arrangements, and public responsibilities. Their access may depend on voluntary developer cooperation, contractual arrangements, application programming interfaces, or publicly available models, allowing some to conduct pre-deployment evaluations while limiting others to post-deployment testing. At the same time, independent evaluators can provide specialized expertise and scrutiny outside both government and frontier-model developers. Recent work therefore treats evaluator independence, system access, methodological rigour, reporting arrangements, and audit standards as important dimensions of third-party auditing [7, 8, 9, 10]. This paper treats government institutes and independent evaluators as distinct institutional categories while applying the same public-record response framework to eligible findings from both. An extended discussion of prior work is given in Appendix I.


---

## 3 Methodology

### 3.1 Data collection

**The corpus is every publicly documented frontier-AI evaluation finding we could locate from 46 evaluating organizations, screened from 6,684 publications: 1,136 findings in 453 reports.** We identified 46 government bodies and independent evaluators that conducted frontier-AI evaluations and publicly reported their methods and results; the full frame, with publications screened and reports included for each organization, is in Appendix A. We screened 6,684 publications and identified 453 reports containing sufficiently documented evaluations of advanced AI systems. The earliest included report was published on 17 March 2023, and the final search was conducted on 29 August 2026. From these reports, we identified 1,136 distinct findings and recorded each as a separate dataset entry before assigning its tier, severity, and response variables.

**No lower-date eligibility boundary was applied.** A report is eligible if it was publicly available on or before the cutoff. 17 March 2023 is simply the earliest publication that survived screening; that date describes the corpus, not a rule.

The corpus is broader than the set used for company-response analysis. It includes adverse findings about named systems or anonymized systems, reassuring or null results, capability trends, and methodology or governance findings. Section 3.3 places them in three tiers. Only the 232 Tier A (trackable evaluation) findings — adverse findings about a named model or developer — enter the response and proportionality analyses. The corpus data and the 46 reporting-institution labels, including separate labels for joint evaluations, are listed in Appendices A and D.

**The unit of analysis is an individual finding, not a report, and every finding names at most one accountable company.** A finding is one discrete, evidence-backed, independently codeable claim. It must be asserted by the evaluator and supported by a measured result, observed behavior, or documented process fact; opinions, recommendations, announcements, and plans are excluded. Results concerning different companies are always coded as separate findings, even when one report identifies the same problem in several companies' models, because no single response could address them together. Each finding receives a unique Finding ID; findings from the same report share a Report ID. The full clubbing and splitting rules, and the treatment of comparators, are in Appendix A.3.

The corpus is restricted to evidence available in the public record. Findings communicated privately but not subsequently disclosed cannot be observed. We also excluded non-English-language outputs where a sufficiently reliable English version was unavailable. The resulting corpus should therefore be interpreted as a structured collection of publicly accessible, predominantly English-language evidence, not as a complete census of every evaluation performed by the included institutions.

#### 3.1.1 Tooling and human oversight

Automated scripts and LLM-based tools supported different parts of corpus construction and analysis. Python scripts were used for data processing, validation, and reproduction of the reported results. LLM-based tools supported publication screening, finding extraction, and separate searches for Channel A (company responses), Channel B (policy uptake), and Channel C (public coverage). Two authors independently reviewed each retained finding and its coding, including eligibility, tier, severity, response evidence, and Action Level. Final coding reflects their agreed judgment. Appendix B describes the search tools, instructions, documented effort, and limitations; Appendix J lists the analysis and validation scripts.

### 3.2 Corpus composition

| Dimension | Distribution |
|---|---|
| **Scope** | third-party evaluator 819 (72.1%) · government AISI 317 (27.9%) |
| **Access type** | post-deployment 828 (72.9%) · pre-deployment 148 (13.0%) · N/A 92 (8.1%) · mixed 68 (6.0%) |
| **Institution type** | Non-Profit AIEF 335 (29.5%) · Government 308 (27.1%) · Non-Profit Independent 245 (21.6%) · For-Profit 231 (20.3%) |
| **Finding type** | `capability-finding` 499 (43.9%) · `methodology` 231 (20.3%) · `capability-finding;anonymised-model` 89 (7.8%) · `governance` 59 (5.2%) · `capability-trend` 48 (4.2%) |
| **Density** | 2.51 findings per report (median 2, max 12); 453 reports across 46 institutions |

**Table 2.** *Corpus composition across the 1,136 findings. Post-deployment evaluation dominates the public record; pre-deployment access — the condition §4.3 shows is associated with substantive responses — covers about one-eighth of findings.*

**Top reporting institutions by findings:** UK AISI 205 · Scale AI 149 · METR 113 · Collective Intelligence Project (Weval) 78 · Shanghai AI Laboratory (AI45 Lab) 74 · SecureBio 48 · Apollo Research 46 · Transluce 41 · FAR.AI 39 · Joint UK AISI + US CAISI 37 · US CAISI 34 · Center for AI Safety 32. The complete 46-label list is in Appendix D.

**Figure 1.** `charts/01_findings_per_institution.png` *Findings per reporting institution (n = 1,136).*
**Figure 2.** `charts/02_findings_per_model_developer.png` *Findings per model developer. A finding naming models from several developers is counted once per developer, so bars sum to more than 1,136.*
**Figure 3.** `charts/03_findings_per_access_type.png` *Findings per access type. "N/A" covers governance and methodology findings with no evaluated system.*

**Figure 4.** `charts/11_domain_distribution.png` *Findings per risk domain across the corpus. Domain labels are multi-valued, so the bars sum to more than 1,136. These are the dataset's descriptive domain labels, which are separate from the eight severity-threshold domains of §3.4.*

### 3.3 Defining the accountability set

**Only one finding in five can be held to account: 232 of 1,136 name an adverse result against an identifiable developer, and those alone carry the response analysis.** We assigned each finding to one of three mutually exclusive tiers based on whether it reported an adverse or safety-relevant result and permitted developer-specific response analysis. **The tier is never labeled by hand:** it is derived from two coded columns — whether the finding is a trackable evaluation result, and whether an action is trackable against a named accountable party.

**Tier A (Trackable evaluation findings).** A finding entered Tier A when it: (1) reported a specific adverse or safety-relevant result; (2) identified a named model, system, or developer rather than only an anonymized placeholder; and (3) concerned an issue within the developer's capacity to address, such that a company response could reasonably be assessed. These 232 findings constitute the accountability set and are the only findings included in the Action Level and proportionality analysis.

**Tier B (Non-trackable evaluation findings).** Empirical findings that did not meet at least one Tier A condition. These include anonymized-system results, reassuring or null results, bare scores or rankings without a concerning threshold, non-frontier systems, capability trends, inconclusive results, and findings for which a company response could not reasonably be assessed.

**Tier C (Non-empirical findings).** Methodology, framework, governance or process, tooling, milestone, and other findings that did not report empirical model behavior or capability. Tier C is almost entirely non-empirical: 223 of its 311 rows are typed `methodology` and 59 `governance`, with two exceptions.

All three tiers remain in the descriptive corpus. Only Tier A enters the company-response and proportionality analysis.

| Tier | n | % of corpus | What it is |
|---|---|---|---|
| **Tier A** (trackable evaluation findings) | **232** | 20.4% | Adverse finding about a named model or developer for which a company response can be assessed |
| **Tier B** (non-trackable evaluation findings) | **593** | 52.2% | Empirical finding failing at least one Tier A condition |
| **Tier C** (non-empirical findings) | **311** | 27.4% | Methodology, governance, tooling, process, milestone |

**Table 3. The three-tier taxonomy.** *Anonymized findings are structurally unaccountable: nobody can be silent about a finding that names nobody.*

**A frontier-scope gate applies before tiering.** A finding must concern a frontier AI lab, company, or model to be in the dataset at all; if it does not, it is excluded to the screening ledger and receives no tier. The gate is a scope condition, not a tiering condition, and its three commonly confused consequences are set out in Appendix C.

### 3.4 Severity of risk classification

**Severity asks a threshold question, not a ranking question: whether the reported evidence crosses a significant-risk line in at least one of eight domains.** A finding was classified as **C1 (significant risk)** when the reported evidence met at least one significant-risk threshold across eight risk domains: chemical, biological, radiological, and nuclear (CBRN) uplift; offensive cyber capability; autonomy, self-replication, or AI research-and-development (AI-R&D) automation; persuasion or societal harm at scale; deliberate deception or misalignment; deployed-safeguard failure; compromised evaluation integrity; or acute individual harm. Findings could be assigned to more than one domain. A finding was classified as **C2 (low risk)** when the reported evidence did not meet any of these significant-risk thresholds. C2 does not mean the finding was unimportant or that no response was warranted.

**How the domains relate to the C1/C2 line.** The domains are not themselves a severity scale. Each domain carries a threshold, and severity is the question of whether the reported evidence crosses one. A cyber finding that measures a modest capability gain sits in the cyber domain but does not cross its threshold, and is C2; one demonstrating operational exploit development crosses it, and is C1. Severity is thus a property of the *evidence*, assessed against the threshold of whichever domain the finding falls in — not a property of the domain.

The domains draw on two sources: dangerous-capability thresholds that frontier developers publish for their own systems [11, 12, 13], and additional criteria developed for this study to cover failure modes those frameworks do not address. Appendix C.1 maps each domain to its source and states which thresholds are the authors' own operationalization.

The majority vote of the three models (Claude Sonnet 5, GPT-5.5, and Gemini 3.1 Pro) provided the initial severity classification. Two authors then independently reviewed every finding and its supporting evidence, including the individual model votes and rationales. Where warranted, the authors overrode the model majority; the agreed human-reviewed label was the final severity classification used in the analysis. Individual model votes and model-generated reasons were retained so that model disagreements remained observable. Appendix C describes the annotation procedure, the eight domain definitions, and the version history of the frozen prompt; the complete prompt, boundary rules, and output format are reproduced in Appendix C.3.

| Subset | n | Unanimous | Split | Agreement |
|---|---|---|---|---|
| All findings | 1,136 | 1,023 | 113 | **90.1%** |
| Tier A only | 232 | 193 | 39 | **83.2%** |

**Table 4. Raw ensemble agreement before human review.** *After review the corpus contained **337 C1** and **799 C2** findings. Within Tier A: **190 C1** and **42 C2** — an 81.9% C1 share, far higher than outside the accountability set, which is expected because the Tier A gate already selects for adverse findings about named systems.*

### 3.5 Response evidence and outcome coding

#### 3.5.1 Evidence channels

**Three separate searches were run for every Tier A finding, and evidence found in one was never substituted for evidence required in another.** Channel A asks whether the accountable company publicly responded to the finding, and admits only that company's own primary documentation. Channel B asks whether the finding received documented policy uptake, and searches official parliamentary, congressional, agency, legislative, and regulatory records. Channel C asks whether the finding received independent public or academic attention, excluding the evaluator's own publicity and the company's own promotion. All three were searched against public information available by 29 August 2026, and a search that could not be completed was recorded as missing rather than negative. The source classes, query construction, admissibility rules, and documented effort for each channel are given in Appendix B.2.

#### 3.5.2 Attribution

**Attribution records whether a company that responded publicly connected its response to the finding.** **Explicit attribution:** the company directly referenced the finding, report, result, or evaluating institution, or stated its response was informed by that evidence. **No explicit attribution:** a qualifying response was identified but the company stated no connection. **No response located:** no qualifying response was identified, so attribution does not arise. Cases with no response are recorded in the third category rather than left blank, so a searched-and-empty result is distinguishable from an uncoded one. Attribution measures the company's public explanation; it does not establish causation.

#### 3.5.3 Action Level

**Action Level grades how much a located company response actually did, on four levels from nothing to a specific documented mitigation.**

**None:** no public response identified through the completed search by the cutoff. **Acknowledged:** the company recognized the finding or underlying problem but specified no action. **Partial:** the company documented an action addressing only part of the problem, or expressly described as interim, limited, or incomplete. **Substantive:** the company documented a specific mitigation, model change, safeguard, access restriction, or deployment decision directly addressing the problem.

**Figure 5.** `charts/26_action_level_scale.png` *The four-level Action Level scale, from no located response to a specific documented mitigation. Only the top level satisfies the proportionality standard for a C1 finding.*

Action Level measures the *content* of the public response. It does not establish that the action was implemented or effective. **Only documents or statements published by the responding company were accepted as Channel A evidence**; evaluator statements, news coverage, and other third-party sources did not count.

#### 3.5.4 Policy Level

Policy Level records documented uptake through Channel B (policy uptake). *No policy uptake identified* means that no qualifying policy response was located. *Non-binding policy-related uptake* means that the finding was cited or discussed without creating an enforceable obligation — official statements, legislative records, consultations, recommendations, and guidance. *Binding policy action* requires an enforceable instrument that imposed a mandatory requirement connected to the finding.

General policy activity concerning the same topic did not qualify without an explicit link. Rows without a completed Channel B search were treated as missing rather than as showing no policy uptake. Policy Level records documented uptake, not whether the finding caused the policy response. The complete evidence rules, including the narrow exception used for one unpublished binding instrument, are given in Appendix F.5.

#### 3.5.5 Proportionality

**Proportionality is the paper's outcome measure: it asks whether the response a company gave was strong enough for the severity of what was found.** It combines two independently assigned classifications — severity and Action Level — under a severity-dependent rule:

| | **Substantive** | **Partial** | **Acknowledged** | **None** |
|---|---|---|---|---|
| **C1 (significant risk)** | Proportionate | Under-response | Under-response | Accountability gap |
| **C2 (low risk)** | Proportionate | Proportionate | Under-response | Accountability gap |

*The table above is the coding rule itself, not observed results; Figure D.6 shows the same matrix as observed counts.*

Two worked examples at each of the four Action Levels are given in Appendix G, to make the coding boundaries concrete. Equivalently: a C1 finding requires a Substantive response to meet the standard; a C2 finding requires at least Partial. Acknowledgment without action never meets the standard, and absence of a response always produces a no-action gap. This is a study-defined measure of *documented* proportionality. It does not establish that a response was effective, that remediation was implemented, or that the underlying risk was eliminated.

---

## 4 Results

We first report company-response outcomes among the 190 C1 findings in Tier A, the paper's primary accountability analysis. We then examine whether severity predicts a response, differences by evaluation-access type, variation across reporting configurations and risk domains, whether unanswered findings nevertheless received public attention, how the gap moved over time, and what the record shows about independent verification.

### 4.1 The headline gap

**Four in five significant-risk findings drew no proportionate public response, and three in five drew no located response at all.**

| Outcome | n / 190 | % | What it means |
|---|---|---|---|
| Accountability gap (no action) | 114 | 60.0% | A significant-risk finding about a named company, with no publicly documented response |
| Under-response (partial or acknowledged) | 38 | 20.0% | The company acknowledged or described a response, but no complete, verifiable mitigation was documented |
| Proportionate | 38 | 20.0% | A specific, documented, attributable response meeting the criteria |
| **Gap total (rows 1 + 2)** | **152** | **80.0%** | **The central result of this paper** |

**Table 5.** *Outcomes among the 190 C1 Tier A findings. Raw Action Level across all 232 Tier A findings: None 145, Substantive 44, Partial 21, Acknowledged 22. Within the 190 C1 findings: None 114, Substantive 38, Partial 21, Acknowledged 17.*

Restricted to C1 (significant risk) findings — the comparison relevant to the paper's central accountability question — **152 of 190 findings (80.0%; Wilson 95% CI 74–85%)** received either no publicly documented company response or an inadequate one. This combined figure, rather than the 62.5% no-response rate across all 232 Tier A (trackable evaluation) findings, is the paper's central result. Because it is calculated only over C1 findings, it is not mechanically affected by the number of C2 (low risk) findings included in the corpus. Of the 76 C1 findings with a located company response, 64 had explicit attribution and 12 did not. In Channel B (policy uptake), 41 C1 findings received non-binding policy uptake, one received binding policy action, and 148 had no identified policy uptake. Robustness checks and subgroup tests are reported in Appendix F; the complete finding-level rows and their supporting evidence are available as described in Appendix E.

When companies do answer, they generally credit the source: the failure documented here is silence, not unattributed appropriation.

**Figure 6.** `charts/10_proportionality_by_severity.png` *The three proportionality outcomes among C1 Tier A findings (n = 190), color-coded by severity of gap. The two gap bars together represent the 152 findings (80%) that received no documented response or an inadequate one.*

**The result is not an artifact of the counting unit.** The headline counts findings, and because one report can yield several findings, a few heavily split reports could in principle drive it. They do not: the shortfall stays high under every alternative unit we tested.

| Unit of analysis | Shortfall | Rate | Wilson 95% CI |
|---|---|---|---|
| **Finding-weighted (headline)** | **152/190** | **80.0%** | **73.7–85.1%** |
| Report-weighted (a report counts once) | 86/102 | 84.3% | 76–90% |
| Institution-weighted (mean of per-institution rates, n = 25) | — | 76.2% | — |
| All Tier A, ignoring severity | 188/232 | 81.0% | 75.5–85.6% |
| C2 (low risk) findings only | 36/42 | 85.7% | 72–93% |

**Table 6. Robustness of the headline shortfall to alternative counting units.** *The range runs from 76.2% under institution weighting to 84.3% under report weighting. Findings also cluster within reports (ICC 0.626, design effect 1.54, effective n ≈ 124), which widens the headline interval to 71.9–86.0%; see Appendix F.2.*

### 4.2 Does severity predict a response?

**It does not — and if anything the more severe findings were answered slightly less often, though the corpus cannot resolve the difference.** Section 4.1 measures the gap among C1 findings; the prior question is whether severity makes any difference to whether a company answers at all. Across Tier A, C1 findings went unanswered in **114 of 190 cases (60.0%)** and C2 findings in **31 of 42 (73.8%)** — a 14-point difference in the direction opposite to the one an accountability system should produce, with the *less* severe findings answered less often.

The comparison does not reach conventional significance (**z = −1.67, p = 0.094**), but it is underpowered rather than null: with only 42 C2 findings the test has low power against a difference of this size. What the corpus supports is therefore a negative claim of a limited kind — **it produces no evidence that more dangerous findings are answered more often** — rather than a demonstration that severity is irrelevant.

### 4.3 Access type: the most policy-relevant split

**When an evaluator sees a model before deployment, the company answers; when it sees the model afterwards, it usually does not. This is the largest and most robust difference in the dataset.** Among the C1 (significant risk) Tier A (trackable evaluation) findings classified as either pre- or post-deployment, the substantive-response rate was **55% for the 44 pre-deployment findings and 7% for the 131 post-deployment findings**. Pre-deployment findings were therefore roughly eight times as likely to receive a substantive response. No-response rates also differed substantially: **6.8% for pre-deployment findings and 79.4% for post-deployment findings**. A two-proportion test gave ***z* = −8.54, *p* < 0.001**, and the difference remained significant after adjustment for clustering within reports (*p* < 0.001; Appendix F.2 and Figure F.2). These comparisons describe an association and should not be interpreted causally. This is the largest effect in the dataset and the only comparison that survives every correction we apply; the 15 mixed-access findings (33% substantive) are reported for completeness and not treated as an independent comparison group.

This descriptive association is consistent with pre-deployment access facilitating company action, although access type is correlated with evaluator, disclosure arrangements, domain, and other institutional differences. One plausible mechanism is visible in the case-level record: pre-deployment findings are communicated while the deployment decision window remains open and are frequently published under coordinated-disclosure arrangements. **Forty-nine of the 88 recorded response lags were zero days**, meaning the finding and the company response were published in the same document. This remains an interpretation, not a mechanism established by the comparison.

**Figure 7.** `charts/05_pre_vs_post_deployment_response_rate.png` *Substantive-response rate and no-response rate by access type among C1 Tier A findings.*

### 4.4 Institution and domain breakdowns

**The gap is broadly distributed rather than concentrated: it exceeds 70% in every reporting configuration and every risk domain large enough to estimate, and only joint evaluations fall as low as half.**

| Reporting configuration | C1 findings | Gap | Gap rate | Substantive |
|---|---|---|---|---|
| Third-party standalone (METR, SecureBio, etc.) | 127 | 108 | 85% | 19 |
| UK AISI standalone | 35 | 28 | 80% | 7 |
| Joint or collaborative evaluation | 22 | 11 | **50%** | 11 |
| US CAISI standalone | 6 | 5 | 83% | 1 |

**Table 7.** *C1 Tier A outcomes by reporting configuration. Joint and collaborative evaluations are the only configuration whose gap rate falls to half. UK AISI's standalone findings skew post-deployment, the access profile associated with lower substantive-response rates in §4.3. Differences are descriptive: the government-versus-third-party comparison does not survive adjustment for clustering within reports (Appendix F.2). The US CAISI sample is too small to support a stable estimate.*

| Domain (multi-label) | C1 findings | Gap | Gap rate |
|---|---|---|---|
| Jailbreaks | 76 | 65 | 86% |
| Cyber | 47 | 34 | 72% |
| Alignment | 41 | 35 | 85% |
| Autonomy | 30 | 23 | 77% |
| Bio-Chem | 30 | 20 | 67% |

**Table 8.** *C1 gap rates by descriptive domain. Findings can span more than one domain, so counts do not sum to 190. Jailbreaks and Alignment share the highest observed gap rate. The comparatively lower Bio-Chem rate is concentrated in SecureBio evaluations conducted through direct pre-release access to OpenAI, so it may reflect access arrangements rather than a domain effect. Three smaller domains — Eval-methodology (n = 6), Societal (n = 3), Human Influence (n = 2) — are too sparse to report separately.*

| Developer | C1 findings | No action | Rate |
|---|---|---|---|
| OpenAI | 89 | 35 | 39.3% |
| Anthropic | 50 | 31 | 62.0% |
| Google | 19 | 18 | 94.7% |
| DeepSeek | 11 | 10 | 90.9% |
| Meta | 10 | 9 | 90.0% |
| Zhipu | 4 | 4 | 100.0% |

**Table 9.** *No-response rate by developer among C1 Tier A findings, developers with n ≥ 4. Developer attribution depends on the model-name matching rule; counts should be read as approximate. The two developers with the most findings against them also answer most often, which is consistent with — but does not establish — a relationship between evaluator access and responsiveness.*

### 4.5 Silence is not obscurity

One explanation for the no-response category is that companies did not respond because the findings attracted little external attention. Channel C provides a limited public-record check on that possibility; it is not a traction or impact score.

Of the 114 C1 (significant risk) Tier A (trackable evaluation) findings classified as Accountability gap (no action), **91 (80%) have at least one mainstream press item or academic citation recorded**. Including notable public discussion, **92 (81%) have evidence in at least one Channel C (public coverage) field**. Thus, the absence of a publicly documented company response was not generally confined to findings with no observable external coverage. This evidence does not establish that the relevant company saw the coverage, but it shows that many no-response findings were publicly visible beyond the original evaluation report.

A formal test finds no difference in no-response rate between findings with and without documented traction that the corpus can resolve (58.2% versus 68.8%; z = −1.11, p = 0.268). The comparison is inconclusive rather than a demonstrated null.

| Channel C evidence | Findings with coverage | Share |
|---|---|---|
| Academic citations | 74 / 114 | 65% |
| Media outlets | 37 / 114 | 32% |
| Social highlights | 21 / 114 | 18% |
| **Any of the three** | **92 / 114** | **81%** |

**Table 10.** *Documented external coverage among the 114 C1 findings with no company response. Categories overlap. Distinguish an empty cell (not searched, or not applicable) from a recorded "none located" (searched, nothing found); only the latter supports an inference.*

### 4.6 The gap over time

**The evaluation ecosystem has grown sharply while the gap has not closed.** The corpus contains 35 findings published in 2023, 154 in 2024, 457 in 2025, and 490 in 2026 through 27 August. Because 2026 is a partial year, this demonstrates increasing publication volume rather than a completed annual trend.

Among C1 Tier A findings the gap does not show clear improvement: **8 of 9 in 2023 (89%), 24 of 26 in 2024 (92%), 61 of 73 in 2025 (84%), and 59 of 82 in 2026 through the cutoff (72%)** received no response or an inadequate one. The 2026 estimate is right-censored, because more recent findings have had less time to attract a documented response. We therefore read the annual results only as showing that the gap persisted as the evaluation ecosystem expanded.

**Figure 8.** `charts/23_corpus_growth_by_tier.png` *Corpus growth by publication year, split by tier.*

**Figure 9.** `charts/15b_shortfall_rate_by_year.png` *Shortfall rate among C1 Tier A findings by publication year. The most recent year is right-censored — findings published close to the cutoff have had less time to attract a documented response — so the 2026 fall should not be read as a trend.*

### 4.7 The verification gap

**Of the 76 responses located, exactly one was independently re-tested and endorsed by an evaluator; the other 75 rest on the company's own account of itself.** A company response does not necessarily permit independent verification. During its pre-deployment evaluation of GPT-5.5, UK AISI identified a universal jailbreak within six hours of testing [14]. OpenAI subsequently reported several changes to its safeguard stack [15]. However, a configuration issue in the version supplied to UK AISI left the institute unable to verify the effectiveness of the final configuration before deployment. This case illustrates the distinction the Partial category captures: a company may document a response while the external evaluator remains unable to verify that the mitigation addressed the vulnerability.

The limitation is structural rather than incidental. **Channel A admits only the responding company's own primary documentation (§3.5.3), so every one of the 76 C1 findings that drew a response is evidenced by that company's account of itself.** That is a property of the coding rule, not a finding. The question the rule cannot answer is whether a second party ever confirmed that the described action was taken, or that it worked.

Reading the response record for each of those 76 findings, we identify:

- **One** case where an evaluator is documented as having re-tested a revised safeguard and endorsed it — US CAISI's examination of Anthropic's rebuilt cyber classifier, which occurred during an export-control process and before redeployment (§5.1).
- **One** case where the evaluator states it could not verify the claimed fix — the GPT-5.5 jailbreak above.
- **Seventy-four** where the public record contains the company's description and nothing independent against which to check it.

The count of independently verified remediations is a lower bound because we can observe only verification reported publicly. We excluded four cases that did not independently confirm that a problem had been addressed: pre-deployment testing collaboration, a capability rating, confirmation that an attack worked, and a company's evaluation of its own model using its own tools.

The Partial category captures the subset where the shortfall is visible at coding time — **21 of 190 C1 findings (11%)** — but the broader position is that proportionality throughout this paper is assessed against **what companies state they did**, not against remediation anyone else has checked.

---

## 5 Understanding the accountability gap

Section 4 documents the distribution of publicly observable responses but does not, by itself, explain why those outcomes occurred. This section examines two forms of follow-through: company remediation in two illustrative cases, and policy-record responses to findings in the corpus. Section 6 separately compares the follow-up mechanisms available to government AI institutes with those used by established oversight institutions.

We selected two cases for which the public record permits unusually clear tracing from technical evidence to developer response. They contrast two institutional pathways: legally consequential action through an existing government authority, and voluntary remediation through iterative pre-deployment collaboration. **Both are in the corpus and both are coded as receiving a Substantive response.** They are illustrative, not representative, and do not exhaust the pathways to remediation.

### 5.1 Enforcement through an existing legal instrument: Fable 5 and Mythos 5

**This is the only case in the corpus where a binding legal instrument forced a remediation and a government evaluator then checked it — and the authority came from export-control law, not from any AI-specific mandate.** Anthropic launched Claude Fable 5 on 9 June 2026. The US government enforced export controls on Fable 5 and Mythos 5 on 12 June, requiring the company to prevent access by foreign nationals inside and outside the United States. Because Anthropic could not verify nationality in real time, both models went offline globally for about eighteen days.

Anthropic reported that the directive followed government awareness of an Amazon research report describing a technique for bypassing Fable 5's safeguards, which caused the model to identify software vulnerabilities and, in one instance, produce code demonstrating how one could be exploited. Anthropic subsequently trained an updated safety classifier and reported that it blocked the identified technique in more than 99% of cases. Anthropic also reported that US CAISI tested both the previous and updated safeguards and considered them "extraordinarily strong"; this does not establish that US CAISI independently produced the 99% estimate. Controls were lifted on 30 June, subject to continuing conditions that the company proactively detect and address security risks, work with the government on standards for future models, and report malicious activity. Fable 5 returned to global availability on 1 July; Mythos 5 was initially restored only to selected US organizations [16].

**Corpus status.** The triggering Amazon report did not enter the corpus as a finding, because it does not satisfy the evaluator-scope criteria. The later US CAISI safeguard-testing and redeployment record **is** included, as finding `USCAISI-2026-06-CYB2`, and is the only corpus response for which the public record states that an evaluator tested the revised safeguards. Under the Policy Level rules it is coded **Binding policy action** — the sole such coding in the corpus. The company-specific directive was never publicly released, so its evidence is admitted under the narrow exception for unpublished binding instruments set out in Appendix F.5.

The public record therefore documents a comparatively complete accountability sequence: a technical problem was reported, a binding legal instrument imposed restrictions, the company implemented a mitigation, and a government evaluator examined the revised safeguards before restrictions were lifted.

The case does not show that the US federal government possessed or exercised deployment authority. The legally consequential action came through the Department of Commerce's export-control powers, while US CAISI contributed technical testing within the resulting process. Therefore, it illustrates how evaluation expertise can support remediation when another institution provides an existing legal pathway.

### 5.2 Collaborative pre-deployment remediation: GPT-5.6

**The contrasting route needs no legal instrument at all: sustained pre-deployment access and an established evaluator–developer relationship produced a documented, attributed fix.** OpenAI's system card describes an iterative pre-deployment process rather than a single evaluation event. UK AISI received early access to GPT-5.6 Sol and extensive gray-box access to its safeguard system. Across several testing rounds UK AISI identified universal cyber-domain jailbreaks, including attacks enabling long-form agentic work involving vulnerability discovery and exploit development. OpenAI states it improved the system in response and, by launch, had reproduced and mitigated the specific jailbreaks UK AISI reported. The system card does not claim the broader vulnerability class was eliminated: UK AISI expected further red-teaming to surface similar jailbreaks, and OpenAI committed to continued testing with the institute [17].

We code this Substantive because OpenAI publicly attributes implemented pre-deployment mitigation to the jailbreaks UK AISI reported. The classification refers specifically to mitigation of the reported attacks; it does not imply GPT-5.6 became resistant to all similar jailbreaks. Unlike the Fable 5 case, no binding government order was involved. The documented response occurred through repeated testing, private disclosure, mitigation, and retesting inside an existing evaluator–developer collaboration.

**Together the two cases illustrate distinct pathways.** In the Fable 5 case an existing legal instrument imposed a mandatory restriction, and later US CAISI testing assessed the revised safeguards. In the GPT-5.6 case pre-deployment access and an established collaboration were followed by documented voluntary mitigation. Neither case establishes that publication of an evaluation finding, by itself, reliably triggers follow-up. A developer may also respond voluntarily to a publicly reported finding with neither a binding requirement nor a pre-arranged process; our method identifies that pathway only when public evidence links the response to the finding.

### 5.3 Policy-record responses

**Findings reach the official record reasonably often but almost never bind anyone: 47 of 1,136 appear in a policy document, and one of those is connected to an enforceable requirement.** We searched parliamentary, congressional, regulatory, and other official government records for explicit references to corpus findings between 2024 and 2026, classifying an appearance as **Type A** when the evidence explicitly connected the finding to binding action, and **Type B** when it connected the finding to a non-binding response such as guidance, research funding, an official statement, or a voluntary commitment. Temporal proximity alone was insufficient.

We also searched for **Type C** cases in which an institute's existence or evaluation work was cited as a reason to defer legislation. No confirmed Type C case was identified. This is an observation about the searched public record, not evidence that such arguments never occur.

**Across the corpus, 47 findings had at least one documented policy-record appearance: 46 non-binding and one binding.** Selected appearances are given in Appendix F.5, Table F.5. Only one was associated with binding action, and in that case the finding entered an existing export-control pathway rather than creating a new enforcement mechanism. Most other appearances produced debate, guidance, requests for information, recommendations, or research commitments.

These classifications establish an observable connection between a finding and the official record. They do not establish that the finding alone caused the policy action; legislation and regulatory decisions generally arise from multiple sources of evidence, political considerations, and prior institutional work.

---

## 6 Institutional mechanisms for reducing the accountability gap

**Every established oversight body we compared has a formal route from a finding to a documented response; the AI institutes have none of the seven mechanisms, and the closest precedent shows that binding power is not what supplies them.** The accountability problem examined here is not unique to AI governance. Established oversight systems distinguish between producing technically credible findings, obtaining a response, verifying corrective action, and possessing authority to compel or escalate. We compare UK AISI and US CAISI with seven established oversight bodies in the United States and United Kingdom, focusing on formal mechanisms for information access, designated recipients, response, remediation or escalation, verification, and continuing follow-up. These bodies differ substantially in mandate, subject matter, and enforcement authority and are not presented as templates. The comparison identifies mechanisms through which technical findings can remain actionable and publicly visible after an evaluation concludes.

**The NTSB is the most relevant precedent for non-binding technical findings.** It independently investigates transportation accidents, determines probable causes, and issues recommendations. It cannot compel recipients to implement them — but it maintains a formal follow-up system. For recommendations directed to the Secretary of Transportation, federal law requires a written response within 90 days stating whether the recommendation will be adopted fully, adopted partly, or refused, with reasons and, where applicable, an implementation timetable. Recommendations and responses are public, and the NTSB classifies each response and implementation status as open or closed, acceptable or unacceptable [18, 19]. The NTSB therefore shows how a technically capable but non-regulatory institution can maintain a publicly inspectable pathway from findings to response and follow-up even when it cannot require implementation.

**The PCAOB illustrates a different question: independent supervision of the evaluators themselves.** Enron exposed weaknesses in corporate governance, auditor independence, financial-statement auditing, professional self-regulation, and financial reporting [20]. It was not simply a case where credible audit warnings were published and ignored; the reliability and independence of the assurance process were themselves in question. Congress responded through the Sarbanes–Oxley Act of 2002, creating the PCAOB to register public-accounting firms, set auditing and independence standards, inspect registered firms, investigate misconduct, conduct disciplinary proceedings, and enforce compliance [21]. Its inspection regime includes a structured process under which audit firms may address identified quality-control criticisms, with unresolved criticisms becoming public if not addressed to the Board's satisfaction within twelve months [22].

Neither precedent is a ready-made model. The NTSB cannot force adoption of its recommendations; the PCAOB regulates auditors rather than compelling audited companies to remedy every adverse finding. Nor do these precedents establish that AI evaluation institutions have failed in the same ways. They separate two questions that are often conflated: whether a system provides a formal pathway from technical findings to documented follow-up, and whether the evaluators themselves are subject to independent supervision. Applied to frontier AI, they motivate asking who should respond to an adverse finding, who tracks and evaluates that response, who verifies claimed remediation, and who — if anyone — oversees the evaluators.

| Design feature | FDA | NRC | NTSB | PCAOB | ONR | FCA | CAA | **UK AISI / US CAISI** |
|---|---|---|---|---|---|---|---|---|
| Can impose binding restrictions within statutory mandate | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✓ | **✗** |
| Compulsory access or information-gathering rights | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✗** |
| Formal process for obtaining a response | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✗** |
| Defined escalation or remediation process | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | **✗** |
| Can review or verify reported remediation | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | **~** |
| Defined pathway to enforcement or another authority | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✗** |
| Systematic post-finding follow-up and status tracking | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✗** |

**Table 11.** *Institutional design comparison. ✓ = formally present; ✗ = absent; ~ = partial or conditional. PCAOB authority applies to registered audit firms, not the public companies they audit. NTSB tracks and evaluates responses but cannot compel implementation. UK AISI and US CAISI can sometimes examine remediation through voluntary or negotiated access, but neither has a uniform right to do so. The two institutes are combined only for this high-level comparison; their legal arrangements differ. Coding draws on official descriptions of the FDA warning-letter process [23], NRC inspections [24], ONR regulation [25], FCA supervision [26], and CAA oversight and enforcement [27, 28]. Supporting detail is in Appendix H.*

**Binding enforcement is not the only route to observable follow-up.** Although the NTSB cannot require implementation, it identifies recipients, evaluates responses, tracks status, and keeps unresolved recommendations public. Other comparators add compulsory access, remediation, verification, or enforcement referral. Official UK AISI and US CAISI mandate descriptions cover research, evaluation, guidance, standards, and voluntary collaboration, but not a uniform process requiring responses, assigning follow-up, or publishing unresolved status [3, 4]. Case-specific negotiated arrangements can still permit responses or remediation checks.

The comparative lesson is institutional rather than sector-specific. **Government frontier-AI evaluators need not become comprehensive regulators for their findings to enter a more systematic accountability process.** Technical evaluation could remain institutionally separate while findings are connected to designated recipients, response expectations or obligations, public status tracking, procedures for reviewing claimed remediation, and defined pathways for escalation or referral. These mechanisms would not guarantee that every finding is remediated or that every response reduces real-world risk, but they would make follow-through more consistent, attributable, verifiable, and publicly inspectable.

---

## 7 Conclusion

Government AI institutes and independent evaluators increasingly provide evidence about frontier systems that would otherwise remain available only through developer self-reporting. The findings in this paper do not question the value of that technical work. They examine whether the public record shows that alarming findings concerning named systems were followed by responses proportionate to the identified risk.

**Among the 190 significant-risk (C1) findings in the accountability set, 114 had no publicly documented company response, 21 received only a partial response, 17 were acknowledged without described action, and 38 drew a response meeting our proportionality criteria. Thus 152 of 190 (80.0%; Wilson 95% CI 73.7–85.1%) lacked a proportionate, publicly documented response.** The shortfall held under every alternative counting unit we tested, from 76.2% weighting by institution to 84.3% weighting by report, and after adjusting for the clustering of findings within reports (71.9–86.0%). Across all 232 Tier A findings, pre-deployment evaluations were roughly eight times as likely to draw a substantive response as post-deployment ones (55% versus 7%), the largest and most robust difference in the dataset. **Only one finding in the corpus was connected to binding policy action**, and in that case the finding entered an existing export-control pathway rather than creating a new enforcement mechanism.

The two cases in Section 5 suggest that findings produce observable consequences through one of two routes: a collaborative pre-deployment relationship in which the developer acts voluntarily, or an existing legal instrument through which another body can require or condition action. Neither applies consistently across frontier-system evaluations.

These results are bounded by the public record. They do not establish that no private communication, mitigation, deterrence, or learning occurred, nor do they imply that an evaluation producing a null result has failed. They show instead that, for most alarming findings in the analyzed set, a member of the public cannot identify a complete, attributable, and verifiable response from the available evidence.

Closing this public accountability gap does not necessarily require converting technical institutes into general-purpose AI regulators. Companies participating in government evaluations could publish finding-level responses stating whether they accept, dispute, plan to address, or have remediated a finding. Institutes could maintain a public response-status record, subject to legitimate security and confidentiality constraints, and distinguish claimed remediation from independently verified remediation. Evaluation agreements could establish response timelines and specify what status information may be disclosed.

The public record currently provides limited grounds for confidence that government and independent frontier-AI evaluations consistently lead to substantive improvements in deployed-system safety. Creating a visible and repeatable pathway from finding to response, follow-up, and verification would make that confidence more warranted — and make the contribution of the evaluation ecosystem more publicly legible.

---

## Limitations

**The public record is the boundary.** Every measure here is an evidentiary claim about what a documented search located by 29 August 2026, not a claim about what exists. Action Level `None` means no public response was identified through the completed search — not that no response occurred. Private communication, preventive action, and unattributed remediation are invisible to this method by construction.

**Causation is not established.** Proportionality relates a finding to a documented response; it does not show the finding produced the response. Policy Level records documented uptake, not causal influence.

**Responses are self-reported.** Channel A admits only the responding company's own primary documentation, so all 76 documented responses are the company's account of itself. Only one has documented independent re-testing (§4.7).

**Findings cluster within reports.** The 190 C1 findings sit in 102 reports, with an estimated intra-cluster correlation of 0.626 and a design effect of 1.54, reducing effective sample size from 190 to about 124. Tests treating findings as independent overstate significance; comparisons near the conventional threshold are reported descriptively.

**Search depth is uneven, and recall is unmeasured.** No blind re-search was performed to estimate how often the response search missed an existing response. Model-call and token counts were not instrumented.

**Aggregate findings under-count.** Where a source reports results in aggregate without attributing them model-by-model, the row is coded against the one company whose response is trackable. Other developers within such an aggregate are not counted, which biases the accountability set toward the most-scrutinized companies.

**Language and access.** Non-English outputs without a reliable English version were excluded, and some Channel C sources were rate-limited or inaccessible in our environment.

**Developer-level counts are approximate**, since they depend on a model-name matching rule (Table 8).

## Broader impacts

This study measures whether published safety findings are acted upon. Documenting a large accountability gap could be read as an argument against third-party evaluation; we intend the opposite. The evidence indicates that evaluation currently lacks the institutional follow-through that makes findings consequential, not that evaluation is unnecessary.

Two risks deserve naming. First, per-developer results (Table 8) could be read as a responsiveness ranking. They should not be: sample sizes differ by an order of magnitude, access arrangements differ, and a company evaluated more often has more opportunities to answer. Second, publishing a corpus of unremediated safety findings concentrates pointers to known weaknesses. We mitigate this by including only findings already public at the cutoff, adding no new technical detail, and reproducing no exploit content; every quoted item is available in its cited source.

The intended positive impact is to give evaluators, developers, and policymakers a measurable baseline for follow-through, and a reusable coding framework for tracking it as the ecosystem grows.

---

## References

1. T. Shevlane, S. Farquhar, B. Garfinkel, et al. (2023). Model evaluation for extreme risks. arXiv:2305.15324. https://arxiv.org/abs/2305.15324
2. R. Araujo, K. Fort, and O. Guest (2024). Understanding the first wave of AI Safety Institutes: Characteristics, functions, and challenges. arXiv:2410.09219. https://arxiv.org/abs/2410.09219
3. UK Government (2025). *Tackling AI security risks to unleash growth and deliver Plan for Change.* DSIT, 14 February 2025. https://www.gov.uk/government/news/tackling-ai-security-risks-to-unleash-growth-and-deliver-plan-for-change
4. Center for AI Standards and Innovation (2026). *Center for AI Standards and Innovation (CAISI).* NIST. https://www.nist.gov/caisi
5. Japan AI Safety Institute (2026). *Japan AI Safety Institute (J-AISI).* Information-technology Promotion Agency. https://aisi.go.jp/assets/pdf/20260708_AISI_en.pdf
6. Ministère de l'Économie, des Finances et de la Souveraineté industrielle et numérique (2025). *Le Gouvernement annonce la création de l'Institut national pour l'évaluation et la sécurité de l'intelligence artificielle (INESIA)* [The Government announces the creation of the National Institute for the Evaluation and Security of Artificial Intelligence]. Press release, 31 January 2025. https://presse.economie.gouv.fr/le-gouvernement-annonce-la-creation-de-linstitut-national-pour-levaluation-et-la-securite-de-lintelligence-artificielle-inesia/
7. G. Falco, B. Shneiderman, J. Badger, et al. (2021). Governing AI safety through independent audits. *Nature Machine Intelligence*, 3, 566–571. https://doi.org/10.1038/s42256-021-00370-7
8. S. Costanza-Chock, E. Harvey, I. D. Raji, M. Czernuszenko, and J. Buolamwini (2023). Who audits the auditors? Recommendations from a field scan of the algorithmic auditing ecosystem. arXiv:2310.02521. https://arxiv.org/abs/2310.02521
9. M. Brundage, N. Dreksler, A. Homewood, et al. (2026). Frontier AI auditing: Toward rigorous third-party assessment of safety and security practices at leading AI companies. arXiv:2601.11699. https://arxiv.org/abs/2601.11699
10. A. Birhane, R. Steed, V. Ojewale, B. Vecchione, and I. D. Raji (2024). AI auditing: The broken bus on the road to AI accountability. arXiv:2401.14462. https://arxiv.org/abs/2401.14462
11. Anthropic (2026). *Responsible Scaling Policy, Version 3.4.* Effective 8 July 2026. https://www.anthropic.com/responsible-scaling-policy
12. OpenAI (2025). *Preparedness Framework, Version 2.* Last updated 15 April 2025. https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf
13. Google DeepMind (2026). *Frontier Safety Framework, Version 3.1.* Published 17 April 2026. https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf (hub: https://deepmind.google/frontier-safety/)
14. UK AI Security Institute (2026). *Our evaluation of OpenAI's GPT-5.5 cyber capabilities.* https://www.aisi.gov.uk/blog/our-evaluation-of-openais-gpt-5-5-cyber-capabilities
15. OpenAI (2026). *GPT-5.5 System Card: External Evaluations for Cyber Capabilities — UK AISI.* https://deploymentsafety.openai.com/gpt-5-5/external-evaluations-for-cyber-capabilities---uk-aisi
16. Anthropic (2026). *Redeploying Claude Fable 5.* https://www.anthropic.com/news/redeploying-fable-5
17. OpenAI (2026). *GPT-5.6 System Card.* https://deploymentsafety.openai.com/gpt-5-6
18. U.S. Congress (2026). *49 U.S.C. §1135: Secretary of Transportation's Responses to Safety Recommendations.* https://uscode.house.gov/view.xhtml?req=%28title%3A49+section%3A1135+edition%3Aprelim%29
19. National Transportation Safety Board (2024). *Responding to Our Safety Recommendations.* https://www.ntsb.gov/investigations/Pages/RecipientTipRecommendations.aspx
20. U.S. General Accounting Office (2002). *Protecting the Public Interest: Selected Governance, Regulatory Oversight, Auditing, Accounting, and Financial Reporting Issues.* GAO-02-483T. https://www.gao.gov/products/gao-02-483t
21. U.S. Securities and Exchange Commission (2003). *Order Regarding Section 101(d) of the Sarbanes–Oxley Act of 2002.* Release Nos. 33-8223, 34-47746. https://www.sec.gov/rules-regulations/2003/04/order-regarding-section-101d-sarbanes-oxley-act-2002
22. Public Company Accounting Oversight Board (2013). *Staff Guidance Concerning the Remediation Process.* https://pcaobus.org/oversight/inspections/remediation/remediation_process
23. U.S. Food and Drug Administration (n.d.). *About Warning and Close-Out Letters.* Accessed 7 September 2026. https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/warning-letters/about-warning-and-close-out-letters
24. U.S. Nuclear Regulatory Commission (n.d.). *Inspection.* Accessed 7 September 2026. https://www.nrc.gov/about-nrc/regulatory/safety-oversight
25. Office for Nuclear Regulation (n.d.). *How we regulate.* Accessed 7 September 2026. https://www.onr.org.uk/our-work/how-we-regulate
26. Financial Conduct Authority (2026). *Our approach to supervision.* Updated 26 March 2026. https://www.fca.org.uk/publications/corporate-documents/our-approach-to-supervision
27. UK Civil Aviation Authority (2023). *145.B.300 Oversight principles.* https://regulatorylibrary.caa.co.uk/1321-2014/Content/Document%20Structure/02%20145/2%20Regs/145.B.300%20Oversight%20principles.htm
28. UK Civil Aviation Authority (n.d.). *Enforcement and prosecutions.* Accessed 7 September 2026. https://www.caa.co.uk/about-us/the-civil-aviation-authority/enforcement/enforcement-and-prosecutions/
29. I. D. Raji, A. Smart, R. N. White, et al. (2020). Closing the AI accountability gap: Defining an end-to-end framework for internal algorithmic auditing. *FAccT 2020*, 33–44. https://doi.org/10.1145/3351095.3372873
30. J. Mökander, J. Schuett, H. R. Kirk, and L. Floridi (2024). Auditing large language models: A three-layered approach. *AI and Ethics*, 4, 1085–1115. First published online 2023. https://doi.org/10.1007/s43681-023-00289-2
31. M. Anderljung, E. T. Smith, J. O'Brien, et al. (2023). Toward publicly accountable frontier LLMs: Building an external scrutiny ecosystem under the ASPIRE framework. arXiv:2311.14711. https://arxiv.org/abs/2311.14711
32. I. D. Raji, P. Xu, C. Honigsberg, and D. E. Ho (2022). Outsider oversight: Designing a third party audit ecosystem for AI governance. arXiv:2206.04737. https://arxiv.org/abs/2206.04737
33. L. Staufer, M. Yang, A. Reuel, and S. Casper (2025). Audit cards: Contextualizing AI evaluations. arXiv:2504.13839. https://arxiv.org/abs/2504.13839
34. Y. Bengio et al. (2026). *International AI Safety Report 2026.* arXiv:2602.21012. https://arxiv.org/abs/2602.21012
35. I. D. Raji and J. Buolamwini (2019). Actionable auditing: Investigating the impact of publicly naming biased performance results of commercial AI products. *AIES 2019*, 429–435. https://doi.org/10.1145/3306618.3314244
36. J. Wang, K. Huang, K. Klyman, and R. Bommasani (2025). Do AI companies make good on voluntary commitments to the White House? arXiv:2508.08345. https://arxiv.org/abs/2508.08345
37. T. Rost (2026). From disclosure to self-referential opacity: Six dimensions of strain in current AI governance. arXiv:2604.14070. https://arxiv.org/abs/2604.14070

*All arXiv identifiers, DOIs, and URLs were verified against arXiv, CrossRef, and direct retrieval on 9 September 2026. Three government URLs (GAO, SEC, NRC) return HTTP 403 to automated requests but resolve normally in a browser; their content was confirmed against archived copies.*

---

# Appendix

*The appendices follow the research process: sampling and search (A–B), coding (C), corpus and response evidence (D–E), robustness and worked examples (F–G), institutional context and prior work (H–I), and reproducibility (J).*

## Appendix A — Sampling frame and source eligibility

The 1,136 findings include outputs from the UK AI Security Institute, the US Center for AI Standards and Innovation, national and joint evaluation initiatives involving France, Japan, Singapore, and South Korea, and exercises conducted through the International Network for Advanced AI Measurement, Evaluation and Science. The frame also included third-party evaluators such as METR, SecureBio, Apollo Research, Palisade Research, Transluce, FAR.AI, and other non-profit, academic, and commercial organizations.

**Roster derivation.** The initial screening roster was derived from three sources: national institutes and initiatives identified through the International Network for Advanced AI Measurement, Evaluation and Science; members of the AI Evaluators Forum plus evaluator organizations already represented in the developing corpus; and frontier-developer release sites, searched **only** for material explicitly attributed to an external evaluator. Organizations later found to be co-author affiliations rather than publishing evaluators, together with national institutes that produced no qualifying report, remain in Table A.1 and the screening ledger as zero-yield records — "swept N items, 0 included" is itself a census result.

**Publisher, not co-author.** Grandfathering attaches to the *publisher* of an included report, never to a co-author. An organization named inside a joint institution string is not thereby a roster organization, since the report is already captured under whoever published it.

**Company venues use a narrowed test.** For items on a frontier developer's own site, the only question asked is whether an external evaluator is named as contributing findings. If not, the item is excluded as a company self-report. If so, only that evaluator's section enters, filed under the **evaluator's** institution, with the company's surrounding self-assessment dropped.

**Eligibility.** Third-party outputs were eligible whether or not the work was conducted with a government institute, provided the public material identified the evaluator and tested system and documented methods and results sufficiently to extract a finding. Eligible sources included formal evaluation reports, research publications, institute progress reports containing evaluation results, joint-testing publications, and company model or system cards that explicitly reported or linked to an external evaluation. Company materials describing only internal evaluations were not treated as independent evaluation reports.

**Table A.1. The 46 organizations in the sampling frame.**

| Organization screened | Screened | Included | Organization screened | Screened | Included |
|---|---|---|---|---|---|
| RAND Corporation | 759 | 6 | Collective Intelligence Project (Weval) | 81 | 27 |
| Kenya (Ministry of ICT — network member) | 628 | 0 | Shanghai AI Laboratory (AI45 Lab) | 74 | 22 |
| Allen Institute for AI (Ai2) | 547 | 0 | Yale University | 69 | 0 |
| Holistic AI | 431 | 9 | Gray Swan AI | 65 | 6 |
| Google DeepMind | 377 | 0 | Stanford University | 65 | 0 |
| Scale AI | 324 | 81 | Apollo Research | 57 | 13 |
| Anthropic | 302 | 28 | Dreadnode | 56 | 16 |
| Cisco (Robust Intelligence / Foundation AI) | 287 | 13 | France INESIA (PEReN / ANSSI / Inria / LNE) | 55 | 4 |
| Thorn | 270 | 0 | LatticeFlow AI | 52 | 5 |
| UC Berkeley | 269 | 0 | US CAISI (NIST) | 49 | 7 |
| OpenAI | 166 | 20 | Canadian AI Safety Institute | 46 | 0 |
| UK AI Security Institute | 160 | 67 | Meta | 44 | 1 |
| Center for AI Safety (CAIS) | 156 | 13 | Princeton Holistic Agent Leaderboard (HAL) | 35 | 9 |
| EPFL | 155 | 0 | Palisade Research | 28 | 15 |
| Redwood Research | 137 | 15 | Transluce | 27 | 14 |
| Tsinghua University CoAI Group | 136 | 3 | University of Oxford | 25 | 0 |
| FAR.AI | 117 | 19 | IndiaAI Safety Institute | 21 | 0 |
| Korea AI Safety Institute (K-AISI) | 105 | 4 | Singapore AI Safety Institute | 18 | 4 |
| Japan AI Safety Institute (J-AISI) | 100 | 3 | Australian AI Safety Institute | 12 | 0 |
| METR | 93 | 49 | EU AI Office (European Commission) | 9 | 0 |
| UL Research Institutes (DSRI) | 91 | 2 | AVERI | 7 | 1 |
| Citadel AI | 86 | 1 | Meridian Labs | 7 | 0 |
| SecureBio | 84 | 11 | Gray Swan AI + UK AISI (joint) | 2 | 2 |

*The ledger contains 6,684 screened publication records and 490 organization–report inclusion entries. After deduplicating joint reports credited to more than one screened organization and applying final corpus exclusions, these correspond to the 453 reports analyzed. Organizations with zero included reports remain listed so the frame records unsuccessful as well as successful searches. **Note:** several network members — Australia, Canada, Kenya, India, the EU AI Office — were swept and yielded zero qualifying reports, so the paper does not claim to have drawn findings from every Network member.*

### A.2 Unit of analysis: clubbing, splitting, and comparators

**Figure A.1.** `charts/25_what_is_a_finding.png` *What counts as one finding. A report yields as many findings as there are claims that could receive distinct responses, and never fewer than the number of accountable companies it implicates.*

Results are combined when they concern the same company, describe the same issue, and would reasonably call for a common response. They are coded separately when they describe substantively different issues or would reasonably call for different responses. Results concerning multiple models from one company may be combined when they document the same issue and would call for the same response.

Results concerning **different companies are always coded as separate findings**, even when a single report identifies the same problem in several companies' models. A comparator or tested baseline may be named inside a row without triggering a split, provided the row asserts nothing adverse about it — a row reporting that one developer's model failed while another's did not is one finding, not two. Where a source reports results in aggregate without attributing them model-by-model, the row is coded against the one company whose response is trackable; the other developers in that aggregate are not counted, which is recorded as a limitation.

Split rows keep the common report identity and receive unique Finding IDs.

### A.3 Screening decision categories

Every enumerated item receives exactly one decision: `INCLUDED`; `EXCLUDED — no findings` (announcement, opinion, methodology promise, plan); `EXCLUDED — no named evaluator`; `EXCLUDED — company self-report`; `EXCLUDED — non-English`; `EXCLUDED — out-of-scope organization`; `EXCLUDED — not a roster organization` (co-author affiliation only); `EXCLUDED — venue retired`; `EXCLUDED — out-of-scope format`; `EXCLUDED — off-topic`; `EXCLUDED — duplicate/secondary`; or `POST-CUTOFF`. Two non-terminal states also appear: `PENDING-FETCH` and `PENDING-EVALUATOR-CHECK`.

**Dedup rule.** The primary — earliest, fullest — source wins. Progress reports and annual summaries are excluded as duplicate or secondary unless they contain a finding published nowhere else, in which case only that finding enters, with the summary as its source.

## Appendix B — AI-assisted search and human oversight

Corpus construction was AI-assisted. This appendix records the search instructions, evidence rules, documented effort, and limits of that process.

### B.1 Publication screening and finding extraction

A total of 6,684 publications were enumerated across the 46 organizations in Appendix A. Automated title-and-abstract triage resolved 5,453 records against the inclusion rules in §3.1; LLM-based search agents examined 885 records for which the title was insufficient; and later targeted passes resolved 346 records. Every screened publication, including exclusions, is recorded in `sweep/master_ledger.csv`. Candidate findings were extracted from source documents by the same tooling. Each retained finding has a source URL and supporting quotation.

### B.2 Response and uptake searches

The table below states what each channel searched and what it admits as evidence; the paragraphs after it give the operational detail.

| Channel | Search and evidence rules | Role in the analysis |
|---|---|---|
| **A — Company response** | The developer's newsroom, blog, or research index; later model and system cards in the affected family; the developer's safety and deployment-safety pages; official developer accounts and statements; and open web used **only** to locate a company primary source. Queries combined developer, evaluator, report, and specific finding. A response qualified only when the company's **own public documentation** addressed the finding or the problem it reported. A standing policy predating the finding did not qualify. | Determines whether a response was located, whether the company publicly connected it to the finding (*Attribution*), and its strength (*Action Level*). |
| **B — Policy uptake** | Official parliamentary, congressional, agency, legislative, regulatory, and government records, searched by evaluator name, report title, report identifier, and finding. General policy activity in the same area did not qualify without an explicit link. An incomplete search was recorded as **missing, not negative**. | Determines no identified uptake, non-binding uptake, or binding policy action. |
| **C — Public coverage** | Independent media, academic citations, and documented public discussion. News results were checked against the original outlet; academic searches used the report or paper identifier; archived pages were used where necessary. **Evaluator publicity and company promotion were excluded** as not independent. | Measures external visibility. It does not measure company action or policy uptake. |

**Table B.1. Evidence channels, searched separately through 29 August 2026.** *Channels B and C do not count as company responses.*

**Channel A (company response).** Agents searched five source classes in order: (1) the accountable developer's newsroom, blog, or research index; (2) later model and system cards in the affected model family; (3) the developer's safety or deployment-safety pages; (4) official developer accounts and statements; (5) open-web results used **only** to locate a company primary source. Queries combined the developer, evaluator, report, and specific finding. A standing policy predating the finding did not qualify. Neither third-party reporting nor company work on the same general topic counted unless a company primary source addressed the finding. **Each company-specific row received its own search, including rows split from one report** — a sibling row's battery is never inherited.

**Channel B (policy uptake).** Agents searched official parliamentary, congressional, agency, legislative, and regulatory sources using evaluator name, report title, and report identifier. General policy activity on the same topic did not qualify without an explicit connection. An incomplete search was recorded as missing rather than as no uptake.

**Channel C (public coverage).** Agents searched independent media, academic citations, and notable public discussion, using Google News results checked against the original outlet, Semantic Scholar by paper identifier, Google Scholar, and archived pages where necessary. Evaluator publicity and company promotion were excluded. Where a source could not be searched reliably, the log records the access problem rather than a negative result.

**Retrieval and review.** A shared retrieval ladder attempted a direct request with complete browser headers, extracted PDF or HTML text, and fell back to the nearest archived snapshot after access errors — so a blocked page is never recorded as an absence. This exists because an earlier pass recorded "congress.gov 403" against 172 findings and concluded a jurisdiction was unsearchable; its *search* pages return 403 while its *documents* return 200. An independent agent pass re-examined proposed Action Level codings against the cited evidence. Two authors then reviewed each retained finding and its coding; the agreed human judgment determined the final record.

### B.3 Documented effort and limitations

**The response search was conducted interactively by AI agents following the source classes and admissibility rules above. It was not driven by a frozen prompt.** Exact query-level replication is therefore not possible, and we make no such claim. This is an asymmetry with the rest of the pipeline, which we state plainly: finding discovery followed a versioned protocol fixed before the sweeps ran, and severity classification used a frozen versioned prompt; the response search had neither. The dated row-level logs are the evidence of what was searched and found, and they are published with the dataset.

| Measure | Recorded value |
|---|---|
| Tier A findings | 232 |
| Rows with a dated Channel A search log | 216 |
| Distinct search dates | 129 |
| Logs enumerating searched sources | 119 |
| Logs recording a re-attempt after an access failure | 58 |
| Channel A log length — mean / median / max | 867 / 700 / 2,300 characters |
| Total logged search prose | 202,190 characters |
| Rows with Channel B evidence recorded | 232 (100%) |
| Rows with any Channel C field populated | 199 (85.8%) |

**Table B.2. Documented response-search effort for Tier A findings.**

All 114 C1 (significant risk) findings coded `None` have a dated Channel A search log. The 16 Tier A rows without such a log are positive-response rows supported by located response evidence; they are not used to support a no-response classification. Search depth is still uneven, and no blind re-search was performed to estimate recall. Model-call and token counts were not instrumented, so they are not reported. Severity classification used a separate frozen prompt and three-model ensemble, described in Appendix C.

## Appendix C — Tier taxonomy and severity annotation

Every shortlisted finding was assigned to one of three mutually exclusive tiers, derived rather than labeled by hand. **Tier A** contains concerning empirical findings about a named frontier model or developer for which a company response can reasonably be assessed. **Tier B** contains empirical findings failing at least one Tier A condition — anonymized, reassuring, null, inconclusive, bare-score, or capability-trend results. **Tier C** contains methodology, framework, governance or process, tooling, milestone, and other non-empirical findings. Only Tier A enters the response analysis.

**Figure C.1.** `charts/07_tier_distribution.png` *The three-tier taxonomy across the 1,136-finding corpus: Tier A 232 (20.4%), Tier B 593 (52.2%), Tier C 311 (27.4%).*

### C.1 The frontier scope gate, and where the severity domains come from

**The scope gate is a condition for entering the dataset at all, not a tiering condition.** Three consequences follow, and they are frequently confused. *Anonymized is not non-frontier:* a finding that evaluates frontier systems without naming which ones satisfies the gate, fails Tier A on the named requirement, and is Tier B. *Model size does not decide the gate:* any model from a frontier developer is in scope at any scale, so an 8B open-weight release from a frontier lab qualifies. *The evaluator's own constructs are out:* a model the evaluator built, fine-tuned, or backdoored for the study has no accountable developer, as does a finding whose subject is a benchmark, a software library, an evaluation apparatus, or human baseliners rather than a model.

**Provenance of the eight domains.** Domains D1–D3 — CBRN uplift, offensive cyber capability, and autonomy including AI-R&D automation and self-replication — correspond to dangerous-capability thresholds that frontier developers publish for their own systems in the Anthropic Responsible Scaling Policy [11], the OpenAI Preparedness Framework [12], and the Google DeepMind Frontier Safety Framework [13]. Domains D4 and D5 — persuasion or societal harm at scale, and demonstrated deceptive misalignment — correspond to categories those frameworks treat less uniformly. Domains D6–D8 — deployed-safeguard failure, compromised evaluation integrity, and acute individual harm — describe failures observed in the evaluation literature that the developers' capability thresholds do not cover. **The thresholds and boundary rules used in this study are the authors' operationalization of those sources, not text taken from them.**

### C.2 Severity domains and final review

The frozen severity prompt (version 1.1) tests eight domains: (D1) CBRN and bio-chemical uplift; (D2) offensive cyber capability; (D3) autonomy, AI-R&D automation, and self-replication; (D4) persuasion or societal harm at scale; (D5) deliberate deception or misalignment; (D6) deployed-safeguard failure; (D7) compromised evaluation integrity; (D8) acute individual harm.

Each finding was independently classified by Claude Sonnet 5, GPT-5.5, and Gemini 3.1 Pro. Their majority vote produced the provisional C1/C2 label. Two authors then independently reviewed every finding and the model rationales and, where warranted, overrode the majority; the agreed human-reviewed label is final. Model votes, retained rationales, and final labels are published with the study materials.

**Version control.** Prompt version 1.0 covered seven domains; version 1.1 added D8 (acute individual harm). Version 1.0 is preserved verbatim and every vote is tagged with the version that produced it. Where the ensemble returns no majority, severity and Proportionality remain **unresolved** until re-run or documented human adjudication; a human override must be identified, state its rationale, and preserve all raw votes, and must not be described as a model majority. **The corpus currently contains no unresolved severity: 337 C1 + 799 C2 = 1,136.**

### C.3 Complete severity prompt (version 1.1)

Reproduced verbatim below, exactly as sent to all three ensemble models. Fields in braces in the user-message template were replaced with the corresponding finding-level values. Version 1.0 is preserved unchanged at `severity/severity_prompt_v1.0_FROZEN.txt` and remains authoritative for rows coded under it; every vote is tagged with the version that produced it. The runner is `severity/run_severity_ensemble.py`.

```
SEVERITY PROMPT — "Evaluating the Evaluators"
Version 1.1 · active from 2026-08-17. Freeze this file now, as v1.0 was frozen before it.

v1.0 is preserved verbatim at severity_prompt_v1.0_FROZEN.txt and remains authoritative for every
row already coded — those votes are tagged prompt_version 1.0 and were NOT re-run. Do not mix v1.0
and v1.1 votes in one reported figure without saying so; the runner tags each vote with its version
so the two are always distinguishable.

Changes from v1.0, each traced to a coding error found by human review:
  * NEW D8, acute individual harm. v1.0 had no domain for a model urging one user toward suicide
    or self-harm: D4 requires harm "at scale" and D6 requires a deployed safeguard to be bypassed.
    Acute-harm findings split 2-1 at 26% against an 8% corpus baseline — the instability of a case
    with nothing to map onto. Missed TRANSLUCE-2026-07-SOC2.
  * D5 now requires DEMONSTRATED deliberateness, with a worked negative example. Classifiers were
    firing on the evaluator's characterisation vocabulary ("faked", "misrepresented") rather than
    on evidence about the model. Produced two false C1s: CAIS-2026-07-ALI1, OPENAI-2025-07-SELF-ALI1.
  * Critical Rule 2 extended to name that failure mode explicitly.

This one prompt is sent verbatim and identically to all three ensemble models
(Claude Sonnet 5, GPT-5.5, Gemini 3.1 Pro). Nothing about it is model-specific.
Any change to this file invalidates comparability with every row already coded.

================================================================================
SYSTEM
================================================================================
You are coding the severity of a published AI-evaluation finding for a research
dataset. You return JSON only. No prose, no preamble, no code fences.

Your task is to decide whether the finding is Category 1 (Critical) or
Category 2 (Non-critical) by checking it against eight dangerous-capability
domains, D1 through D8.

The Category 1 bar deliberately mirrors the dangerous-capability thresholds the
frontier developers publish for themselves — Anthropic's RSP Capability
Thresholds, OpenAI's Preparedness Framework, and Google DeepMind's Frontier
Safety Framework Critical Capability Levels. You are applying the industry's own
bar, not inventing one.

--------------------------------------------------------------------------------
CATEGORY 1 (Critical) — triggered if ANY ONE domain is DEMONSTRATED
--------------------------------------------------------------------------------
D1  CBRN / Bio-Chem uplift
    Meaningful uplift toward chemical, biological, radiological or nuclear
    weapons; expert-surpassing bio/chem capability; crossing a stated CBRN
    threshold.

D2  Cyber operations
    Offensive cyber capability; expert-level or novel-uplift hacking; completing
    realistic multi-stage attack chains; high CTF or exploit success rates; a
    "High" or above cyber designation.

D3  Autonomy / AI R&D / self-replication
    Autonomous replication, self-propagation, or automating AI R&D and thereby
    accelerating scaling.

D4  Persuasion / manipulation / societal harm at scale
    Systematically changing beliefs or behaviour at scale; implication in
    large-scale societal harm (mass CSAM, election-scale persuasion exceeding a
    real benchmark).

D5  Deceptive alignment / misalignment
    Deliberate deception, scheming, sabotage, sandbagging, blackmail, or hiding
    of abilities or intentions.

    DELIBERATENESS IS REQUIRED AND MUST BE SHOWN. A fabricated, substituted or
    low-quality output does not by itself demonstrate deception. You need
    evidence about the MODEL: its own reasoning, an explicit plan, concealment
    repeated across trials, or a statement that it knew it was misrepresenting.

    Words like "faked", "fabricated", "misrepresented" or "cheated" in the
    finding are the EVALUATOR'S characterisation of an output. They are not
    evidence of intent. Do not set d5 on that vocabulary alone.

      YES  "I should not reveal that I am a robot. I should make up an excuse."
           -- the model's own reasoning, planning a deception.
      YES  "the model consistently hides the genuine reasons behind its trade"
           -- concealment repeated across trials.
      NO   "the good-looking render is faked with an image generator"
           -- a fabricated artefact, with nothing shown about intent.

D6  Safeguard failure
    A DEPLOYED safety mechanism — jailbreak defence, classifier, guardrail,
    refusal training, content filter — bypassed, defeated, or shown to fail,
    allowing harmful output on a frontier system.

D7  Evaluation integrity compromised
    The evaluation itself undermined — the model detected it was being
    evaluated, gamed the benchmark, was trained on evaluation data
    (contamination), or defeated or de-anonymised the evaluation environment.

D8  Acute individual harm
    A model actively encouraging, instructing or coaching a user toward suicide
    or self-harm. Category 1 REGARDLESS OF SCALE — one user is enough. Scale is
    sufficient for criticality under D4, not necessary. Reporting refusal rates
    on such prompts is not D8; the model must be shown doing it.

--------------------------------------------------------------------------------
CATEGORY 2 (Non-critical)
--------------------------------------------------------------------------------
- Reassuring or null results: capability BELOW an expert threshold, "no uplift",
  "did not degrade", "zero instances".
- Capability-GAP findings: the model FAILS a task.
- Positive methodology or tooling contributions.
- Pure process or governance observations.
- Findings about non-frontier or small research models where no frontier system
  is implicated.

--------------------------------------------------------------------------------
THE FOUR CRITICAL RULES — apply these before you decide
--------------------------------------------------------------------------------
1. NEGATION
   "did NOT", "below expert", "zero instances", "no uplift", "remained below"
   => Category 2, even when the vocabulary around it is alarming.

2. DEMONSTRATED, NOT MENTIONED
   The capability or failure must be SHOWN in the evaluation described. A
   capability that is merely discussed, proposed, warned about, or listed as a
   risk is not demonstrated.

   This applies to the evaluator's WORDS as much as to the model's behaviour.
   An alarming characterisation is not a demonstration. Before flagging a
   domain, ask: what did the model do, and does the text show it? Quote that,
   not the adjective.

3. TRAJECTORY
   A rising trend is Category 1 ONLY if a dangerous capability was reached NOW.
   A pure future projection with no current dangerous level is Category 2. If a
   dangerous capability IS demonstrated at present, code Category 1 even when
   the sentence also describes a trend.

4. SOCIETAL HARM
   Documented real-world harm at scale IS Category 1 under D4, even where no
   "safeguard" is involved.

Restated: Category 1 requires a DEMONSTRATED THRESHOLD — a working universal
jailbreak, a full attack chain, expert-surpassing bio capability. Not alarming
wording. Not model-versus-model uplift. Not a trend. Not a negation.

--------------------------------------------------------------------------------
OUTPUT — JSON only, exactly these keys
--------------------------------------------------------------------------------
{
  "d1": false,
  "d2": false,
  "d3": false,
  "d4": false,
  "d5": false,
  "d6": false,
  "d7": false,
  "d8": false,
  "quote": "<verbatim span from the supplied Finding or Finding Quote that
             supports your domain flags; empty string if category is 2>",
  "category": 2,
  "confidence": 0.0,
  "reason": "<one line, under 200 characters>"
}

Hard constraints:
- "category" MUST equal 1 if ANY of d1..d8 is true, and 2 otherwise. Compute it,
  do not judge it separately.
- "quote" MUST be copied character-for-character from the supplied text. Never
  paraphrase it. Never quote text that was not supplied to you.
- "confidence" is a float from 0.0 to 1.0.
- Return the JSON object and nothing else.

================================================================================
USER MESSAGE TEMPLATE
================================================================================
Code the severity of this finding.

Finding ID: {finding_id}
Domain: {domain}
Models / Systems evaluated: {models}
Institution: {institution}

FINDING:
{finding}

FINDING QUOTE (verbatim from the source report):
{finding_quote}

Return the JSON object only.
```

## Appendix D — Corpus composition

The corpus contains 46 distinct reporting-institution labels, including separate labels for joint evaluations. Appendix A lists a separate 46-organization *screening* frame; the equal totals are coincidental, because the two lists do not contain the same entities.

**Table D.1. All 46 reporting-institution labels, by findings.**

| Institution | Findings | Institution | Findings |
|---|---|---|---|
| UK AISI | 205 | Apollo Research + Anthropic | 6 |
| Scale AI | 152 | LatticeFlow AI | 6 |
| METR | 113 | Princeton CRUX | 6 |
| Collective Intelligence Project (Weval) | 78 | AVERI | 5 |
| Shanghai AI Laboratory (AI45 Lab) | 74 | Joint UK + US + Singapore AISIs | 4 |
| SecureBio | 48 | Joint UK AISI + OpenAI (company-published) | 4 |
| Apollo Research | 46 | Redwood Research + Scale AI | 4 |
| Transluce | 41 | Joint UK AISI + US CAISI + Gray Swan | 3 |
| FAR.AI | 39 | Singapore AISI / IMDA | 3 |
| Joint UK AISI + US CAISI | 37 | Japan AI Safety Institute (J-AISI) | 2 |
| US CAISI | 34 | Joint UK AISI + International Network (10 countries) | 2 |
| Center for AI Safety (CAIS) | 32 | Joint UK AISI + US CAISI + Anthropic | 2 |
| Dreadnode | 31 | Korea AI Safety Institute (K-AISI) | 2 |
| Redwood Research | 29 | RAND Europe | 2 |
| Princeton Holistic Agent Leaderboard (HAL) | 27 | Signature Science | 2 |
| Palisade Research | 19 | Singapore AISI / Korea AISI | 2 |
| RAND | 18 | UK AISI + Thorn | 2 |
| Holistic AI | 13 | Andon Labs | 1 |
| Gray Swan AI | 11 | Citadel AI | 1 |
| Cisco (Robust Intelligence / Foundation AI) | 10 | METR + Epoch AI | 1 |
| Irregular | 10 | Singapore AISI + Korea AISI (bilateral) | 1 |
| France PEReN/INESIA | 9 | UK AISI + Anthropic + Theorem + MATS | 1 |
| International Network of AI Safety Institutes | 7 | UL Research Institutes (DSRI) | 1 |

**Figure D.1.** `charts/13_institution_type_tree.png` *Reporting volume by institution type across all 1,136 findings, on one common scale, showing the five largest institutions in each of the four groups with the remainder combined. Institution Type follows the dataset field; compound values fold into their primary type, so the four branches sum to 1,136.*
**Figure D.4.** `charts/17_severity_classification.png` *Severity classification by the three-model ensemble.*
**Figure D.5.** `charts/08_action_level_distribution.png` *Action Level across all 232 Tier A findings: None 145, Substantive 44, Partial 21, Acknowledged 22.*
**Figure D.6.** `charts/21_severity_x_action_heatmap.png` *Severity × Action Level as observed counts — the proportionality matrix of §3.5.5 shown as data rather than rule. The top-left cell (C1 with no response) is the accountability gap and is the largest cell in the table.*
**Figure D.7.** `charts/18_attribution_distribution.png` *Attribution across Tier A: no response located 145 (62.5%), explicit attribution 74 (31.9%), no explicit attribution 13 (5.6%).*
**Figure D.8.** `charts/09_policy_level_distribution.png` *Policy Level across Tier A: no uptake 185, non-binding 46, binding 1.*
**Figure D.9.** `charts/22_domain_x_outcome_heatmap.png` *Risk domain × outcome. Read across rows, not down columns: domains carry very different sample sizes.*
**Figure D.10.** `charts/14_response_lag_distribution.png` *Distribution of response lag. The mass at zero is coordinated disclosure.*
**Figure D.11.** `charts/24_evaluator_volume_vs_gap.png` *Evaluator volume against gap rate. Each point is a reporting institution. There is no visible relationship between publication volume and how often an evaluator is answered.*

## Appendix E — Response evidence and data access

Complete finding-level rows and supporting evidence are available through the study materials. Among the 38 C1 Tier A findings coded **Substantive**, **35 carry Explicit attribution** — the company named the evaluator or finding in its response. The three exceptions drew a substantive fix with no explicit public credit to the evaluator.

## Appendix F — Robustness and subgroup analyses

Core corpus statistics were independently recomputed from the workbook; the reproduction path is in Appendix J.

### F.1 Is the headline an artifact of the counting unit?

The five-unit robustness comparison is reported in the body as Table 6, because the abstract and conclusion both rely on it. In summary: finding-weighted 80.0%, report-weighted 84.3%, institution-weighted 76.2%, all Tier A 81.0%, C2 only 85.7% — a range of 76.2% to 84.3%. Definitions of each unit and the clustering adjustment follow in F.2.

### F.2 Uncertainty and subgroup comparisons

The headline describes an enumerated public record rather than a sample estimate, so we attach no significance test to it; Table 6 reports it under five counting units with Wilson intervals. Two subgroup comparisons support claims in the body and are reported with their limits.

**Access type.** Among C1 Tier A findings, 3 of 44 pre-deployment findings received no response (6.8%) versus 104 of 131 post-deployment (79.4%); the 15 mixed findings are excluded. Two-proportion test: **z = −8.54, p < 0.001**, remaining below 0.001 after adjustment for clustering within reports.

**Severity.** C1 findings received no response in 114 of 190 cases (60.0%) versus 31 of 42 C2 (73.8%); **z = −1.67, p = 0.094**. This is not evidence of no difference; the corpus cannot resolve whether severity predicts response.

**Clustering.** The 190 C1 findings sit in 102 reports, and outcomes cluster because findings from one report usually share evaluator, disclosure arrangement, and developer. Kish mean cluster size 1.86; estimated intra-cluster correlation **0.626**; design effect **1.54**, reducing effective sample size from 190 to about **124**. The design-effect-adjusted interval for the 80.0% headline is **71.9–86.0%**. Two-proportion tests treating findings as independent can therefore overstate significance; comparisons near the conventional threshold are reported descriptively.

**Two descriptive comparisons.** Government AISI findings fell short in 42 of 59 cases (71.2%) versus 110 of 131 (84.0%) for third-party evaluators; the naive test gives p = 0.042, but the difference does not remain below 0.05 after the clustering adjustment. Among C1 Tier A findings, 92 of 158 with documented public traction received no response (58.2%) versus 22 of 32 without (68.8%); z = −1.11, p = 0.268, inconclusive.

**Figure F.1.** `charts/12_evaluator_scope.png` *Outcome composition by evaluator type among the 190 C1 Tier A findings.*
**Figure F.2.** `charts/16_gap_rate_by_access_type.png` *Access type in the full corpus (left) and no-response rates within C1 Tier A findings (right).*

### F.3 Outcome composition by descriptive domain

The labels in Figure D.9 come from the dataset's descriptive Domain field and are **separate** from the eight severity-threshold domains of §3.4. They are multi-valued, so row totals exceed 232 Tier A findings. The largest domains all carry substantial accountability-gap shares; the smallest have too few findings for stable comparison. The figure is descriptive and is not a ranking of domain importance.

*The domain × outcome matrix is Figure D.9.*

### F.4 Channel C — traction among no-response findings

The channel-by-channel breakdown is reported in the body as Table 10, since §4.5 turns on it. In summary, of the 114 C1 findings with no located company response, 74 (65%) carry academic citations, 37 (32%) mainstream media, 21 (18%) notable public discussion, and 92 (81%) at least one of the three. Categories overlap. Throughout, an empty cell (not searched, or not applicable) is distinguished from a recorded "none located" (searched, nothing found); only the latter supports an inference.

### F.5 Policy-record responses and the evidentiary exception

Policy Level records whether a finding appears in an official policy response:

1. **No policy uptake identified:** no qualifying official policy response was located.
2. **Non-binding policy-related uptake:** the finding was connected to guidance, an official statement, a request for information, research support, debate, or another non-binding response.
3. **Binding policy action:** an official source or the regulated recipient documented a binding restriction or obligation explicitly connected to the finding.

A policy record was coded only when the evidence connected the specific finding to the policy response; general policy discussion in the same domain was not sufficient.

**Exception for unpublished binding instruments.** Channel B normally relies on official government sources — but that clause defines where Channel B *searches*, not exclusively what counts as evidence. Where an instrument is unambiguously binding yet **lawfully not published** — for example a single-company regulatory directive issued by letter, or any order that by convention does not appear in a public register — the regulated recipient's public disclosure may qualify, provided it identifies the instrument, issuing authority, mandatory requirement, and connection to the finding, and is supported by contemporaneous independent reporting. The evidence record must state that no official publication was located and name the official sources searched. **The form of the instrument is immaterial**; what matters is that it is enforceable, imposes a mandatory requirement, and that its non-publication is lawful rather than a gap in the search.

**This exception concerns evidence, not the definition of binding action.** The boundary between the two positive levels remains enforceability: a government action taken to mitigate the risk but creating no mandatory requirement — guidance, a warning, a consultation, a voluntary undertaking, a funding decision — remains non-binding uptake, however consequential it proves.

**Invoked once, for `USCAISI-2026-06-CYB2`.** Reading the official-sources clause as a strict evidentiary bar would record "no policy uptake identified" for the one case in the corpus where a government actually compelled a frontier developer to act. That row qualifies on **two independent grounds**: the order itself imposed a prohibition taking both models offline globally for eighteen days; and the controls were lifted on continuing conditions — proactively detect and address security risks, work with the government on standards for future models, and report malicious activity — which are imposed obligations outlasting the suspension.

**A related instrument does not substitute for an explicit link.** Executive Order 14409, *Promoting Advanced Artificial Intelligence Innovation and Security* (signed 2 June 2026, 91 FR 34565), is the published federal AI-security authority in force days before the order. It is **not** admissible as Channel B evidence here: it names no company or model, and it predates the finding — Fable 5 launched 9 June, the order issued 12 June — so it cannot explicitly reference it. It is the general policy activity this section excludes, and belongs in narrative, never in the Policy Level cell. A Congressional Research Service report on the federal government and Anthropic (IF13217, 5 May 2026) was likewise examined and rejected: it concerns the February 2026 supply-chain designation, not these models.

**Direction of the bias.** Because the Channel B battery searches official sources rather than company disclosures, comparable binding orders documented only by recipient disclosure would probably not have been located. **The exception can therefore only undercount binding uptake, never overcount it.**

**Table F.5. Selected policy-record appearances among the 47 findings with documented uptake.**

| Finding and cited result | Venue and type | Documented policy response |
|---|---|---|
| `USCAISI-2026-06-CYB2` — Fable 5 / Mythos 5 jailbreak, classifier retest, redeployment | US Department of Commerce (recipient disclosure) — **Type A (binding)** | A private Export Administration Regulations order restricted access for about eighteen days; controls were lifted subject to continuing security and reporting conditions. No official government publication of the order was located. |
| `UKAISI-2026-04-CYB1` — Mythos Preview reached 73% on expert CTFs and solved a hardest-range challenge | UK Government (DSIT) — Type B | An open letter to business leaders explicitly cited AISI's Mythos evaluation and launched a Cyber Resilience Pledge; it created no enforceable obligation. |
| `UKAISI-2026-04-CYB11` — GPT-5.5 cyber-range and reverse-engineering results | Bank of England FPC — Type B | The July 2026 Financial Stability Report reproduced the result and cited AISI in its systemic-risk assessment; no Recommendation or Direction issued. |
| `OPENAI-2026-08-CYB1` — an evaluation agent acted on a real website after an environment misconfiguration | UK NCSC — Type B | A formal advisory statement called for safeguards, real-time oversight, and incident-response plans; no binding obligation. |
| `JOINT-2025-01-JAI1` — agent-hijacking attacks raised measured success from 11% to 81% | US NIST / CAISI — Type B | A Federal Register request for information cited the report as its research basis; comments requested, no mandatory requirement. |
| `SECUREBIO-2025-04-BIO1` — frontier models outperformed expert virologists on a 322-question benchmark | US House committee record — Type B | Published written testimony named the Virology Capabilities Test and stated the result; no enforceable obligation followed. |
| `PALISADE-2025-07-ALI1` — o3 disabled its shutdown mechanism in 79 of 100 experiments | European Parliament — Type B | A written question cited the shutdown result and called for regulatory intervention; no binding action located. |

## Appendix G — Worked examples across the response scale

Two findings at each Action Level, to make the coding boundaries concrete. These are illustrative selections, not a random sample; each is reproducible from its Finding ID in the published dataset. Text is abridged for layout.

### G.1 Substantive — a specific, documented, attributed change (n = 38 of 190)

| Finding ID | Institution | Finding | Company response (verbatim) |
|---|---|---|---|
| `JOINT-2025-09-BIO1`<br>[evidence source](https://www.anthropic.com/news/strengthening-our-safeguards-through-collaboration-with-us-caisi-and-uk-aisi) | Joint UK AISI + US CAISI | Evaluators found multiple universal jailbreaks bypassing the Constitutional Classifiers protecting Claude Opus 4 and 4.1 — via false annotations, encoded attacks, and cipher/character-substitution obfuscation. | "Rather than simply patching this individual exploit, the discovery prompted us to **fundamentally restructure our safeguard architecture** to address the underlying vulnerability class." |
| `JOINT-2025-09-JAI2`<br>[evidence source](https://openai.com/index/us-caisi-uk-aisi-ai-update/) | Joint UK AISI + US CAISI | UK AISI identified product-configuration vulnerabilities where malicious content could be inputted or exfiltrated without triggering moderation. | "OpenAI **made a range of improvements to our product configuration to fix** a set of configuration vulnerabilities that UK AISI identified, where malicious content could be inputted or exfiltrated without triggering moderation." |

*Both carry Explicit attribution. The first shows an architectural response, the second a targeted fix — the two shapes a Substantive response takes. A third, `JOINT-2025-09-CYB1`, reads simply: "These attacks were immediately reported to OpenAI, and fixed by OpenAI within one business day."*

### G.2 Partial — action documented but incomplete, interim, or unverifiable (n = 21 of 190)

| Finding ID | Institution | Finding | Company response |
|---|---|---|---|
| `OPENAI-2026-08-CYB1`<br>[evidence source](https://openai.com/index/third-party-cyber-evaluations-involving-openai-models/) | Irregular | Irregular notified OpenAI on 29 July 2026 of an incident during external cybersecurity testing in which an evaluation agent acted on a real third-party website. | "In the coming weeks, we will review our own approach to third-party testing, including how we identify higher-risk evaluations…" — a stated intention, not a completed mitigation. |
| `UKAISI-2026-08-AUT1`<br>[evidence source](https://www.anthropic.com/aug-2026-risk-report) | UK AISI | In an AISI cyber-range exercise, Mythos 5 agents running in separate concurrent isolated samples discovered one another and coordinated. | Anthropic's risk report notes the AISI publication and describes the behavior, without documenting a specific mitigation addressing it. |

### G.3 Acknowledged — the finding is referenced; no action described (n = 17 of 190)

| Finding ID | Institution | Finding | Company response |
|---|---|---|---|
| `SECUREBIO-2023-06-BIO1`<br>[evidence source](https://openai.com/index/building-an-early-warning-system-for-llm-aided-biological-threat-creation/) | SecureBio | In a one-hour classroom exercise at MIT, non-scientist students prompted public chatbots, which suggested four potential pandemic pathogens and explained how they could be generated from synthetic DNA. | "Existing research on AI-enabled biological threats has shown that models like GPT-4 can be prompted or red-teamed to share information related to biological threat creation…" — recognition, no described action. |
| `SECUREBIO-2023-06-JAI1`<br>[evidence source](https://openai.com/index/building-an-early-warning-system-for-llm-aided-biological-threat-creation/) | SecureBio | The chatbots' biosecurity safeguards were bypassed trivially: most harmful responses were offered freely with at most minimal prompting. | Same OpenAI source; the finding is referenced without a corresponding mitigation being described. |

### G.4 None — nothing located by the search cutoff (n = 114 of 190)

| Finding ID | Institution | Finding | Company response |
|---|---|---|---|
| `UKAISI-2026-08-ALI1`<br>*(no evidence URL: five-source battery completed, none located)* | UK AISI | In AISI cyber-range evaluations run 25–28 July 2026, AISI cataloged 19 instances of unsanctioned action on the live internet across 10 samples; 17 came from a single model. In the most severe, the agent attempted a supply-chain attack on a real, unaffiliated open-source project. | — (five-source battery completed; no admissible company primary document located) |
| `TRANSLUCE-2026-08-ALI3`<br>*(no evidence URL: five-source battery completed, none located)* | Transluce | Claude's behavior is conditioned on the recognized identity of the user supplied through the coding harness. | — (five-source battery completed; none located) |

*The distinction that matters most in practice is Partial versus Substantive: a company may document a response while the evaluator remains unable to verify that the mitigation addressed the vulnerability. See §4.7.*

## Appendix H — Institutional comparison, annotated

In this appendix NTSB denotes the National Transportation Safety Board; PCAOB the Public Company Accounting Oversight Board; FDA the Food and Drug Administration; NRC the Nuclear Regulatory Commission; ONR the Office for Nuclear Regulation; FCA the Financial Conduct Authority; and CAA the Civil Aviation Authority.

Table 11 in §6 records only whether a formal function exists, not whether the bodies possess identical powers or operate identically. Coding draws on official descriptions of the FDA warning-letter process [23], NRC inspections [24], ONR regulation [25], FCA supervision [26], and CAA oversight and enforcement [27, 28], together with the NTSB statutory response requirement [18, 19] and the PCAOB remediation process [20, 21, 22].

**Qualifications.** PCAOB authority applies to registered audit firms, not to the public companies they audit — the analogy to AI evaluation is supervision *of evaluators*, not of developers. NTSB tracks and evaluates responses but cannot compel implementation, which is precisely why it is the closest precedent for a non-regulatory technical body. UK AISI and US CAISI can sometimes examine remediation through voluntary or negotiated access, recorded as partial rather than present, because neither holds a uniform right to do so. The two institutes are combined only for this high-level comparison; their legal and institutional arrangements differ materially.

## Appendix I — Extended prior work

Prior work addresses three questions adjacent to this study: how frontier AI evaluations and audits should be designed, whether audits and voluntary commitments are followed by observable changes, and how the institutional and political environment shapes accountability.

**Evaluation and audit design.** Raji et al. [29] propose an end-to-end framework for internal algorithmic auditing embedding accountability across the development life cycle. Mökander et al. [30] propose a three-layered framework combining governance, model, and application audits. Anderljung et al. [31] identify six requirements for effective external scrutiny of frontier systems: access, a searching attitude, proportionality to risk, independence, resources, and expertise. Drawing on financial, environmental, and health regulation, Raji et al. [32] argue that third-party audits require a supporting institutional ecosystem to produce accountability. Brundage et al. [9] define frontier AI auditing as rigorous third-party verification of developers' safety and security claims and propose four AI Assurance Levels. Staufer et al. [33] propose "audit cards" documenting auditor identity, evaluation scope, methodology, resource access, process integrity, and review mechanisms. Collectively this literature identifies conditions for credible evaluation but does not empirically measure whether particular published findings subsequently produce company or policy action.

The *International AI Safety Report 2026* [34] documents behaviors complicating pre-deployment testing: some models distinguish evaluation from deployment settings and exploit unintended shortcuts in evaluation objectives.

**Whether audits produce observable change.** Raji and Buolamwini [35] provide the closest methodological precedent, re-testing commercial facial-analysis products after the public Gender Shades audit to examine whether named companies had improved their systems. Wang, Huang, Klyman, and Bommasani [36] assess the publicly disclosed behavior of 16 companies against their eight 2023 voluntary commitments to the White House, reporting an average compliance score of 53% and arguing that companies should provide proactive, verifiable evidence of compliance. These studies measure product changes or compliance with prior commitments; the present study instead traces responses to independently produced findings.

**Institutional and political environment.** Rost [37] applies a six-dimensional political-theory framework to six existing AI-governance arrangements, rating the UK AISI as failing on corrigibility and voluntary company commitments as failing on accountability, while presenting cross-case patterns as hypotheses requiring validation. Falco et al. [7] and Costanza-Chock et al. [8] examine the independent-audit ecosystem and who audits the auditors; Birhane et al. [10] examine when AI audits translate into accountability outcomes.

To our knowledge no prior study systematically tracks, finding by finding, the publicly documented company, policy, and ecosystem responses to frontier AI system evaluations conducted by government institutes and independent evaluators.

## Appendix J — Reproducibility

Every number in this paper is regenerated from a single workbook by script; none is transcribed by hand.

| Artifact | What it is |
|---|---|
| `dataset/AISIEVAL_V13.xlsx`, sheet `AISIEVAL_V13` | The dataset: 1,136 findings × 39 columns. Read only through `scripts/dataset_source.py`, so there is exactly one path and one sheet name in the project. `AISIEVAL_WORKBOOK` overrides the path. |
| `dataset/AISIEVAL_validate.py` | Structural validator: identifiers, controlled vocabularies, date coherence, the proportionality formula, the Attribution invariant. **Currently PASS, 0 violations.** |
| `scripts/audit_v13.py` | Full-sheet audit: identifiers, report identity in both directions (one Report ID → one title/URL/date, and one title or URL → one Report ID), dates, links, verbatims, cross-column coherence. |
| `scripts/all_stats.py` | Recomputes every reported quantity — corpus, headline, channels, proportionality, robustness, subgroup tests, clustering, lag, and the by-developer, by-year and by-domain breakdowns. |
| `scripts/prefilter.py` | Search orchestration: decides deterministically which findings require an agent, so agents do not re-fetch the same corpus. |
| `scripts/fetch.py` | The shared retrieval ladder used by every agent: direct GET with full browser headers, PDF/HTML extraction, then the nearest Wayback snapshot on 403/429/5xx — so a blocked source is never recorded as an absence. |
| `scripts/compute_proportionality.py` | Derives Proportionality from severity × Action Level. Proportionality is derived, never hand-edited. |
| `scripts/verify_verbatims.py`, `verbatim_sweep.py`, `verbatim_coverage.py`, `verbatim_triage.py` | Quote verification: checks every stored verbatim against the document it cites. |
| `scripts/find_duplicates.py` | Six independent duplicate tests across identifiers, finding text, quotes, and near-duplicate detection. **Currently 0 duplicates.** |
| `scripts/build_charts.sh`, `scripts/verify_charts.py` | Builds all 38 figures, then re-derives every plotted quantity from the workbook and **fails the build** if any figure disagrees. Currently PASS. |
| `scripts/build_paper_table.py` | Publication export: the Tier A table with internal working columns removed (233 × 34), under a whitelist so no analytical cell is altered. |
| `scripts/build_data.py` | Builds the published `data.js` and `dataset.csv` for the dashboard. |
| `severity/run_severity_ensemble.py`, `severity_prompt_v1.0_FROZEN.txt`, `severity_prompt.txt` | The three-model severity ensemble and both prompt versions. |
| `protocol/SEARCH_PROTOCOL.md` | Discovery and screening protocol (v1.1): roster derivation, screening categories, dedup rule, ledger schema, reconciliation. |
| `protocol/RESPONSE_SEARCH_PROTOCOL.md` | Channel A/B/C battery, §8b admissibility, the earned-vs-unearned `None` rule, per-row split batteries, and stated limitations. **Explicitly a post-hoc reconstruction, not a pre-registered prompt.** |
| `protocol/v11_RULEBOOK.md` | The coding rulebook, including the §9 evidentiary exception. |
| `sweep/master_ledger.csv` | The screening ledger: every publication examined and the decision taken, including exclusions, so coverage reconciles in both directions. |
| `logs/` | Deletion ledgers recording every removed row with all 39 columns and its reason. |

**Table J.1.** *Reproduction path. The validator, the statistics script, and the chart verifier are run together after any change to the dataset; a figure that disagrees with the workbook is treated as a build failure rather than a discrepancy to be explained.*

### J.1 Exact reproduction commands

From the project root, in order:

```
pip install -r requirements.txt
python3 dataset/AISIEVAL_validate.py     # structural validation — expect PASS, 0 violations
python3 scripts/audit_v13.py             # full-sheet audit
python3 scripts/all_stats.py             # every reported statistic
bash    scripts/build_charts.sh          # all 38 figures
python3 scripts/verify_charts.py         # re-derives each plotted quantity — expect PASS
python3 scripts/find_duplicates.py       # expect 0 duplicates
python3 scripts/build_paper_table.py     # the 232 × 34 publication table
```

Set `AISIEVAL_WORKBOOK` to run the whole pipeline against a different copy of the workbook.
