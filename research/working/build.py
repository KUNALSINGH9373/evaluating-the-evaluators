#!/usr/bin/env python3
import csv, os

OUT = "/Users/kunalsingh/evaluating-the-evaluators/sweep_state/extract_jobs"

HEADER = ["Finding ID","Report ID","Institution","Institution Type","Report Title ","Publication Date","Domain","Models / Systems","Access Type","Source URL","Finding","Finding Quote","Severity (C1/C2) majority","Sonnet5 vote","GPT-5.5 vote","Gemini3.1 vote","Attribution","Company Response","Channel A Verbatim","Response Date","Lag (days)","Channel A Evidence","Action Level","Sources Checked (channel A)","Policy Level","Policy Response","Channel B Verbatim","Channel B Evidence","Media Outlets","Academic Citations","Social Highlights","Channel C Verbatim","Proportionality","","Eval? (trackable)","Action Trackable?","Finding Type","Tags","Scope","Notes"]

TODO = "TODO severity ensemble + Channel A/B/C."

def row(fid, rid, inst, itype, title, date, domain, models, access, url, finding, quote,
        ev, act, ftype, tags, notes):
    d = {k: "" for k in HEADER}
    d["Finding ID"] = fid; d["Report ID"] = rid; d["Institution"] = inst
    d["Institution Type"] = itype; d["Report Title "] = title; d["Publication Date"] = date
    d["Domain"] = domain; d["Models / Systems"] = models; d["Access Type"] = access
    d["Source URL"] = url; d["Finding"] = finding; d["Finding Quote"] = quote
    d["Eval? (trackable)"] = ev; d["Action Trackable?"] = act; d["Finding Type"] = ftype
    d["Tags"] = tags; d["Scope"] = "third-party-evaluator"
    d["Notes"] = (notes + " " if notes else "") + TODO
    return d

def write(key, rows):
    p = os.path.join(OUT, "out_%s.csv" % key)
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("wrote", p, len(rows), "rows")

def write_dups(key, rows):
    p = os.path.join(OUT, "dup_%s.csv" % key)
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["candidate_title","candidate_url","matched_finding_id","why_duplicate"])
        for r in rows:
            w.writerow(r)
    print("wrote", p, len(rows), "rows")

# ===================== CISCO =====================
CI = "Cisco (Robust Intelligence / Foundation AI)"
CT = "For-Profit"
cisco = []

u_ft = "https://www.robustintelligence.com/blog-posts/fine-tuning-llms-breaks-their-safety-and-security-alignment"
cisco.append(row(
 "CISCO-2024-05-JAI1","CISCO-2024-05",CI,CT,"Fine-Tuning LLMs Breaks Their Safety and Security Alignment","2024-05-28",
 "Jailbreaks","AdaptLLM-Biomedicine, AdaptLLM-Finance, AdaptLLM-Law (Microsoft; fine-tuned from Llama-2-7B)","Post-deployment",u_ft,
 "On 250 queries from the 'Jailbroken' benchmark, three Microsoft AdaptLLM chat models fine-tuned from Llama-2-7B scored 1.66, 1.73 and 1.72 on compliance with jailbreak instructions versus 0.54 for the base model, and produced responses with harmfulness above one in 26.4%, 26.8% and 27.6% of cases versus 1.6% for Llama-2-7B.",
 "these models are more than 3 times more compliant with jailbreak instructions with over 22 times greater odds of producing a harmful response",
 "yes","no","capability-finding; non-frontier","fine-tuning, alignment-degradation, jailbreak, domain-adaptation",
 "[Report tested: Llama-2-7B (Meta) as the well-aligned control/baseline.] Cross-posted verbatim at https://blogs.cisco.com/security/fine-tuning-llms-breaks-their-safety-and-security-alignment (same report, one row)."))

u_pg = "https://blogs.cisco.com/security/bypassing-metas-llama-classifier-a-simple-jailbreak"
cisco.append(row(
 "CISCO-2024-07-JAI1","CISCO-2024-07",CI,CT,"Bypassing Meta's LLaMA Classifier: A Simple Jailbreak","2024-07-29",
 "Jailbreaks","Prompt-Guard-86M (Meta, part of the Llama 3.1 safety suite)","Post-deployment",u_pg,
 "Spacing out characters and removing punctuation took Meta's Prompt-Guard-86M prompt-injection classifier from correctly flagging all 450 harmful prompts to 0.2% accuracy (449/450 misclassified as benign, a 99.8% bypass rate); Cisco traced the flaw to single-character embeddings left essentially unchanged by fine-tuning (average MAE < 0.0003 across shared tokens).",
 "the model's performance plummeted to 0.2% accuracy, misclassifying 449 out of 450 prompts as benign and demonstrating a complete circumvention of the model's safety mechanisms (Success Rate of 99.8%)",
 "yes","yes","capability-finding","guardrail-bypass, prompt-injection-classifier, fine-tuning, coordinated-disclosure",
 "Report states Cisco disclosed to Meta and that 'Meta acknowledged the issue and fixed it.' Evaluated on 450 harmful-intent prompt injections (Sorry-Bench)."))

u_so = "https://blogs.cisco.com/security/bypassing-openais-structured-outputs-another-simple-jailbreak"
cisco.append(row(
 "CISCO-2024-08-JAI1","CISCO-2024-08",CI,CT,"Bypassing OpenAI's Structured Outputs: Another Simple Jailbreak","2024-08-08",
 "Jailbreaks","OpenAI Structured Outputs API feature (refusal mechanism)","Post-deployment",u_so,
 "An ENUM-based custom data structure that forces every response step to begin with an attacker-chosen prefix raised attack success rate on SORRY-Bench from 12.44% (normal API calling) to 52.89% - a 4.25x increase - and cut appropriate refusals from 59.6% to 30.2%.",
 "The ENUM-based attack achieved an ASR of 52.89%, compared to 12.44% for normal API calling and 15.78% for function calling baselines.",
 "yes","yes","capability-finding","structured-outputs, refusal-bypass, api-safety-feature, sorry-bench",
 "Audit run within hours of the Structured Outputs release; Cisco says it notified OpenAI and was awaiting a response. Cross-posted at https://www.robustintelligence.com/blog-posts/bypassing-openais-structured-outputs-jailbreak (same report, one row)."))

u_ic = "https://blogs.cisco.com/ai/inherited-circuits-learned-semantics-how-security-fine-tuning-can-create-hidden-evasion-risk"
cisco.append(row(
 "CISCO-2026-06-CYB1","CISCO-2026-06",CI,CT,"Inherited Circuits, Learned Semantics: How Security Fine-Tuning Can Create Hidden Evasion Risk","2026-06-29",
 "Cyber","Foundation-Sec-8B-Instruct (Cisco Foundation AI), fine-tuned from Llama-3.1-8B-Instruct (Meta)","Post-deployment",u_ic,
 "Cisco's security fine-tuned Foundation-Sec-8B-Instruct beat its Llama-3.1-8B-Instruct base by 4.7% accuracy on PowerShell malicious/benign classification but missed behaviour-preserving rewrites the base model caught, with 4/4 misses on full-command Invoke-Expression case mutation and 4/4 on case-mutated IEX aliases; mechanistic analysis shows fine-tuned feed-forward components suppress or invert malicious evidence carried by an inherited classification circuit.",
 "The strongest misses concentrated around full-command Invoke-Expression case mutation (4/4 missed) and case-mutated IEX alias variants (4/4 missed)",
 "yes","no","capability-finding; company-self-report; non-frontier","security-fine-tuning, evasion, powershell-classification, mechanistic-interpretability",
 "[Report tested: Llama-3.1-8B-Instruct as the base-model comparator.] Cisco evaluating its own released model."))

cisco.append(row(
 "CISCO-2026-06-GOV1","CISCO-2026-06",CI,CT,"Inherited Circuits, Learned Semantics: How Security Fine-Tuning Can Create Hidden Evasion Risk","2026-06-29",
 "Governance / evaluation methodology","Foundation-Sec-8B-Instruct and Llama-3.1-8B-Instruct (used as instruments)","N/A",u_ic,
 "Cisco proposes a pre-deployment monitoring method for fine-tuned security classifiers: a linear probe trained on the base model's residual stream and reused after fine-tuning (correlations r = 0.80-0.87) plus an indicator-token sign test that flags command families where an indicator flips from malicious driver to suppressor, producing a ranked list of families to red team.",
 "The probe works well in our setting, with correlations around r = 0.80-0.87.",
 "no","","methodology","representation-drift, linear-probe, pre-deployment-monitoring, red-team-targeting",""))

cisco.append(row(
 "CISCO-2026-06-GOV2","CISCO-2026-06",CI,CT,"Inherited Circuits, Learned Semantics: How Security Fine-Tuning Can Create Hidden Evasion Risk","2026-06-29",
 "Governance / evaluation methodology","Foundation-Sec-8B-Instruct (Cisco Foundation AI)","N/A",u_ic,
 "A prompt-level fix that told the model to classify by overall purpose removed the Invoke-WebRequest alias misses but opened or amplified misses in other families (Invoke-Expression, IEX, DownloadString), showing prompt remediation redistributes rather than eliminates the evasion surface.",
 "This reveals that prompt remediation can redistribute the failure surface, rather than eliminate it.",
 "no","","methodology","prompt-remediation, evasion, mitigation-limits",""))

u_faith = "https://cisco-foundation-ai.github.io/blogs/new-cybersecurity-benchmarks-cti-reasoning-cwe-prediction"
cisco.append(row(
 "CISCO-2026-07-GOV1","CISCO-2026-07",CI,CT,"New Cybersecurity Reasoning Benchmarks in FAITH: CTI-Reasoning and CWE-Prediction","2026-07-17",
 "Governance / evaluation methodology","N/A (benchmark release; evaluated with Foundation-Sec-8B-Instruct and 15 open/proprietary models)","N/A",u_faith,
 "Cisco released two open cybersecurity reasoning benchmarks in FAITH 0.4.0: CTI-Reasoning (200 multiple-choice questions from CAPEC/CWE, 96% requiring analytical rather than recall-based reasoning) and CWE-Prediction (3,000 questions over 263 CWE classes built from 2025 CVE and 2024-2025 GHSA advisories that postdate most model training cutoffs, to test generalisation rather than memorisation).",
 "96% of questions require analytical reasoning rather than factual recall - specifically, 77.5% demand analysis-based cognitive processing and 22.5% require comprehension-based reasoning.",
 "no","","methodology","benchmark-release, cyber-threat-intelligence, cwe, memorisation-resistance",""))

cisco.append(row(
 "CISCO-2026-07-CYB1","CISCO-2026-07",CI,CT,"New Cybersecurity Reasoning Benchmarks in FAITH: CTI-Reasoning and CWE-Prediction","2026-07-17",
 "Cyber","15 open and proprietary models (per-model scores not rendered in cached text); anonymised","Post-deployment",u_faith,
 "Across 15 open and proprietary models evaluated over 5 trials, both new FAITH cybersecurity reasoning benchmarks remained unsaturated, with Cisco reporting substantial headroom even for frontier models.",
 "Both benchmarks are challenging and unsaturated - even frontier models leave substantial headroom, which makes them useful yardsticks for measuring progress.",
 "yes","no","capability-trend; anonymised-model","benchmark-headroom, cyber-reasoning, unsaturated-benchmark",
 "Per-model score table and charts did not render in the cached text, so no individual model numbers are recorded here; full results are in the Foundation-Sec-8B-Reasoning technical report."))

write("cisco_robust_intelligence_fou", cisco)

write_dups("cisco_robust_intelligence_fou", [
 ["Safety Evaluation of DeepSeek Models in Chinese Contexts","https://arxiv.org/abs/2502.11137","ROBUSTINT-2025-01-JAI1",
  "Not a Cisco report: authored by China Unicom (Wenjing Zhang, Shiguo Lian et al.). The only Cisco content is a citation of Robust Intelligence's DeepSeek-R1 100% attack-success-rate result, which is already in v10 as ROBUSTINT-2025-01-JAI1. Cached text is the arXiv abstract page only."],
 ["Safety Evaluation and Enhancement of DeepSeek Models in Chinese Contexts","https://arxiv.org/abs/2503.16529","ROBUSTINT-2025-01-JAI1",
  "Same as above - China Unicom authorship; the Cisco/Robust Intelligence 100% ASR claim it cites is already in v10 as ROBUSTINT-2025-01-JAI1. Cached text is the arXiv abstract page only."],
 ["Fine-Tuning LLMs Breaks Their Safety and Security Alignment (Cisco cross-post)","https://blogs.cisco.com/security/fine-tuning-llms-breaks-their-safety-and-security-alignment","CISCO-2024-05-JAI1",
  "Identical cached text to the robustintelligence.com post; same report published on two domains, extracted once."],
 ["Bypassing OpenAI's Structured Outputs: Another Simple Jailbreak","https://www.robustintelligence.com/blog-posts/bypassing-openais-structured-outputs-jailbreak","CISCO-2024-08-JAI1",
  "Identical cached text to the blogs.cisco.com cross-post; same report published on two domains, extracted once."],
])

# ===================== DREADNODE =====================
DI = "Dreadnode"
dread = []

u_aa = "https://dreadnode.io/research/the-automation-advantage-in-ai-red-teaming"
dread.append(row(
 "DREADNODE-2025-04-JAI1","DREADNODE-2025-04",DI,CT,"The Automation Advantage in AI Red Teaming","2025-04-29",
 "Jailbreaks","30 LLM red-teaming challenges on Dreadnode's Crucible platform (target models not named; anonymised)","Post-deployment",u_aa,
 "Analysing 214,271 attack attempts by 1,674 users across 30 LLM challenges, Dreadnode found automated attack sessions succeeded 69.5% of the time versus 47.6% for manual attempts, with purely automated approaches at 76.9% and hybrid at 63.1%, even though only 5.2% of users employed automation.",
 "Our analysis shows that automated approaches achieve significantly higher success rates (69.5%) compared to manual attempts (47.6%)-a difference of 21.8 percentage points.",
 "yes","no","capability-trend; anonymised-model","automated-red-teaming, crucible, attack-success-rate, adoption-gap",
 "Same report as the arXiv paper https://arxiv.org/abs/2504.19855 (2025-04-28); extracted once. Dreadnode notes a selection bias: harder challenges attract automation."))

dread.append(row(
 "DREADNODE-2025-04-GOV1","DREADNODE-2025-04",DI,CT,"The Automation Advantage in AI Red Teaming","2025-04-29",
 "Governance / evaluation methodology","30 LLM red-teaming challenges on Crucible (anonymised)","N/A",u_aa,
 "Although automation won on success rate, manual attempts solved challenges roughly 5.2x faster by median time (1.5 minutes versus 11.6 minutes), with the direction reversing on some challenge types, which Dreadnode uses to argue for hybrid human-plus-automated testing.",
 "median solve times showed manual attempts were approximately 5.2 times faster (1.5 minutes versus 11.6 minutes for automated approaches)",
 "no","","methodology","time-to-solve, hybrid-red-teaming, evaluation-design",""))

u_tt = "https://dreadnode.io/research/ai-red-teaming-case-study-claude-sonnet-solves-turtle"
for n,(mdl,fnd,q) in enumerate([
 ("Claude 3.7 Sonnet (Anthropic)",
  "In AIRTBench's turtle challenge - crafting a prompt that makes a target LLM emit shell-injection-vulnerable code, solved by only 6% of human operators - Claude-3.7-Sonnet succeeded autonomously in about 9 minutes over 30 conversation turns, persisting through failed attempts and switching strategies after sophisticated techniques failed.",
  "Claude-3.7-Sonnet: Solve time: ~9 minutes"),
 ("Gemini 2.5 Pro (Google)",
  "On the same turtle challenge (6% human solve rate), Gemini-2.5-Pro succeeded autonomously in about 18 minutes over 41 conversation turns by systematically testing prompt formats until one bypassed the target's controls.",
  "Gemini-2.5-Pro: Solve time: ~18 minutes"),
 ("Llama-4-17B (Meta)",
  "On the same turtle challenge, Llama-4-17B - the only open-source model to solve it - succeeded in about 1 minute over 6 conversation turns by presenting vulnerable code and asking for it to be 'made more secure', inducing the target to emit a different vulnerable implementation.",
  "Solve time: ~1 minute Strategy: The only open-source model among the successful solutions employed a creative security-focused approach"),
]):
    dread.append(row(
     "DREADNODE-2025-06-CYB%d" % (10+n), "DREADNODE-2025-06B", DI, CT,
     "AI Red Teaming Case Study: Claude 3.7 Sonnet Solves the Turtle Challenge","2025-06-18",
     "Cyber", mdl, "Post-deployment", u_tt, fnd, q,
     "yes","no","capability-finding","airtbench, autonomous-red-teaming, ctf, shell-injection, turtle-challenge",
     "Companion case study to AIRTBench (already in v10 as DREADNODE-2025-06-CYB1/CYB2, which cover overall solve rates). This row records only the turtle-specific result, which is not in the existing index. Report ID suffixed 'B' to avoid collision with the existing 2025-06 AIRTBench report."))

u_ev = "https://dreadnode.io/research/evals-the-foundation-for-autonomous-offensive-security"
dread.append(row(
 "DREADNODE-2025-07-GOV1","DREADNODE-2025-07",DI,CT,"Evals: The Foundation for Autonomous Offensive Security","2025-07-30",
 "Governance / evaluation methodology","OpenAI o1 (o1-2024-12-17) driving a Mythic/Apollo agent harness in the GOAD Active Directory lab; used as an instrument","N/A",u_ev,
 "Dreadnode documents an evaluation methodology for autonomous offensive-security agents (action-space design, string/structured-object/LLM-judge verifiers, repeated trials with logged independent variables), motivated by the observation that the same o1-driven agent found the planted SYSVOL domain credentials on one run and failed to find anything usable on another.",
 "In this run, the model performed some basic recon, but hasn't given us anything usable and failed to find the credentials. So does the agent work, or not?",
 "no","","methodology","offensive-agent-evaluation, verifiers, run-to-run-variance, active-directory",
 "The planned five-model comparison (o1, gpt-4o-mini, claude-sonnet-4, DeepSeek-R1, gemini-2.5-pro) is described but no success-rate numbers are reported in the post."))

u_186 = "https://dreadnode.io/research/186-jailbreaks-applying-mlops-to-ai-red-teaming"
dread.append(row(
 "DREADNODE-2025-12-JAI1","DREADNODE-2025-12B",DI,CT,"186 Jailbreaks: Applying MLOps to AI Red Teaming","2025-12-11",
 "Jailbreaks","Llama Maverick-17B-128E-Instruct (Meta), deployed in production environments","Post-deployment",u_186,
 "Running TAP, GOAT and Crescendo against 80 AdvBench prompts spanning eight harm categories, Dreadnode obtained 186 successful jailbreaks out of 240 attack runs (~78% ASR) against Llama Maverick-17B-128E-Instruct in about 137 minutes and 2,645 queries, including step-by-step explosive-preparation content and insider-trading tradecraft.",
 "We ran an AI risk assessment against Llama Maverick-17B-128E-Instruct that resulted in 186 successful jailbreaks at an attack success rate of 78%.",
 "yes","yes","capability-finding","advbench, tap, goat, crescendo, harmful-content, multi-modal",
 "Report ID suffixed 'B' to avoid collision with the existing DREADNODE-2025-12 AMSI report. Attacker and judge LLM: Moonshot Kimi-2 Instruct."))

dread.append(row(
 "DREADNODE-2025-12-JAI2","DREADNODE-2025-12B",DI,CT,"186 Jailbreaks: Applying MLOps to AI Red Teaming","2025-12-11",
 "Jailbreaks","Llama Maverick-17B-128E-Instruct (Meta)","Post-deployment",u_186,
 "Multi-turn gradual escalation was by far the strongest attack against Llama Maverick: Crescendo reached 97.5% ASR (19 queries per attack on average) versus 78% for GOAT and 57% for TAP, and was 100% effective in the self-harm and violence categories, indicating safety training that holds for single-turn refusals but degrades across a conversation.",
 "Self-harm and violence: Crescendo was devastatingly effective (100% ASR), while other methods struggled.",
 "yes","yes","capability-finding","multi-turn-jailbreak, crescendo, self-harm, violence, safety-training-gap",
 "Split from the overall-ASR row because the multi-turn weakness warrants a distinct remediation. GOAT reached 78% ASR with only 7 queries per attack, which Dreadnode flags as harder to detect."))

dread.append(row(
 "DREADNODE-2025-12-JAI3","DREADNODE-2025-12B",DI,CT,"186 Jailbreaks: Applying MLOps to AI Red Teaming","2025-12-11",
 "Jailbreaks","GPT-3.5 (OpenAI)","Post-deployment",u_186,
 "Against GPT-3.5, which refused a direct password-cracking request, the TAP attack combined with a simple character-level transform (inserting underscores between characters) bypassed the refusal and elicited the harmful content.",
 "In one run, we found that inserting underscores between characters in the prompt completely circumvented safety mechanisms.",
 "yes","no","capability-finding; non-frontier","character-level-transform, tap, refusal-bypass, legacy-model",
 "Single illustrative run; no ASR reported for this example. GPT-3.5 is a legacy model by the report date."))

u_live = "https://dreadnode.io/research/ai-red-teaming-frontier-model-live-demo"
dread.append(row(
 "DREADNODE-2026-06-JAI1","DREADNODE-2026-06",DI,CT,"AI Red Teaming a Frontier Model, Live: From Natural Language to Findings","2026-06-16",
 "Jailbreaks","Llama 4 Scout (meta-llama/llama-4-scout-17b-16e-instruct, Meta)","Post-deployment",u_live,
 "In a live demonstration driven by one natural-language instruction, Dreadnode's red-teaming agent (orchestrated by Claude Opus 4.8) used Tree of Attacks with Pruning to elicit password-breaking code from Llama 4 Scout with a 100% attack success rate in just 2 trials, rated high severity; a Crescendo attack with a Telugu-language transform also reached 100% success (0.9 severity) and a trace-recommended nested-fiction transform reached 70% on violent-category probing.",
 "It succeeded in just 2 trials with a 100% attack success rate and was categorized as high severity.",
 "yes","yes","capability-finding","tap, crescendo, low-resource-language, nested-fiction, malware-code-generation",
 "The report's other Llama Scout result (68 objectives, ~85% ASR in ~3 hours) is the case study already in v10 as DREADNODE-2026-05-JAI1 and is NOT re-extracted here."))

dread.append(row(
 "DREADNODE-2026-06-AUT1","DREADNODE-2026-06",DI,CT,"AI Red Teaming a Frontier Model, Live: From Natural Language to Findings","2026-06-16",
 "Autonomy / agentic risk","A DevOps agent built on GPT-4o-mini (OpenAI) with read_file, execute_command, query_database, send_email, fetch_url and list_directory tools, deployed in Azure Container Apps","Post-deployment",u_live,
 "Attacking a deliberately undefended GPT-4o-mini DevOps agent with graph-of-attacks and TAP aimed at data exfiltration, credential extraction, RCE and SSRF produced a critical finding: the agent read sensitive configuration files and exfiltrated credentials through its read_file tool.",
 "The result was a critical finding: the agent read sensitive configuration files and exfiltrated credentials via its read_file tool call, traced down to the exact tool invocations.",
 "yes","no","capability-finding","agentic-risk, credential-exfiltration, tool-calling, devops-agent",
 "Dreadnode states the demo agent was deliberately undefended (no content-safety classifier, tool allow-lists, input validation or per-user scoping), so the result reflects the unguarded scaffold as much as the underlying model."))

dread.append(row(
 "DREADNODE-2026-06-GOV1","DREADNODE-2026-06",DI,CT,"AI Red Teaming a Frontier Model, Live: From Natural Language to Findings","2026-06-16",
 "Governance / evaluation methodology","LLM-as-judge scorers in Dreadnode's red-teaming platform","N/A",u_live,
 "Dreadnode reports that because finding severity is scored by LLM-as-judge, judges hallucinate and sometimes score refusals as jailbreaks, so the platform requires human-in-the-loop reclassification (with logged reasons and live metric updates), especially for critical categories such as remote code execution and data exfiltration.",
 "Because scoring uses LLM-as-judge, judges can hallucinate or flag refusals as jailbreaks, so the platform supports human-in-the-loop review",
 "no","","methodology","llm-as-judge, false-positives, human-in-the-loop, scoring-reliability",""))

write("dreadnode", dread)

write_dups("dreadnode", [
 ["AI Red Teaming a Frontier Model, Live: From Natural Language to Findings (Llama Scout 68-objective case study result)",
  "https://dreadnode.io/research/ai-red-teaming-frontier-model-live-demo","DREADNODE-2026-05-JAI1",
  "The blog's headline case-study figure (Llama Scout, 68 objectives, ~3 hours, ~85% ASR) is the same measured result already recorded from 'Redefining AI Red Teaming in the Agentic Era'. Only the new live-demo measurements were extracted."],
 ["The Automation Advantage in AI Red Teaming (arXiv paper)","https://arxiv.org/abs/2504.19855","DREADNODE-2025-04-JAI1",
  "Same report as the Dreadnode blog post of 2025-04-29 (arXiv preprint of the same study); extracted once from the blog, which contains the fuller numbers."],
 ["AI Red Teaming Case Study: Claude 3.7 Sonnet Solves the Turtle Challenge (overall AIRTBench solve rates)",
  "https://dreadnode.io/research/ai-red-teaming-case-study-claude-sonnet-solves-turtle","DREADNODE-2025-06-CYB1 / CYB2",
  "Partial overlap only: the AIRTBench overall solve rates (Claude 61%, Gemini 55.7%, GPT-4.5 49%) are already in v10, so they were not re-extracted; the turtle-specific solve times/turns are new and were kept."],
])

# ===================== HOLISTIC AI =====================
HI = "Holistic AI"
hol = []

u_dcwp = "https://www.holisticai.com/blog/nyc-bias-audit-impact-ratio-regression"
hol.append(row(
 "HOLISTIC-2023-01-GOV1","HOLISTIC-2023-01",HI,CT,"Disparate Impact in Bias Audits: Evaluating the DCWP's Impact Ratio Metrics for Regression Systems","2023-01-23",
 "Societal / governance - audit methodology","N/A (NYC DCWP proposed impact-ratio metrics for automated employment decision tools under Local Law 144)","N/A",u_dcwp,
 "Holistic AI demonstrates that the DCWP's proposed regression impact-ratio metrics for NYC Local Law 144 bias audits can be pushed into the 'fair' range without reducing bias: raising a single female candidate's score from 36 to 100 moved the average-score ratio from 0.69 to 0.84, and adding a constant of 30 to every score moved it from 0.66 to 0.83; the revised median-based metric is more robust but still fails for bimodal score distributions, where an impact ratio of 1.0 at the median collapses once only the top 20% are hired.",
 "By increasing the score of a single female candidate from 36 to 100, the impact ratio has increased from 0.69 to 0.84.",
 "no","","governance","nyc-local-law-144, bias-audit, impact-ratio, regression, metric-gaming",
 "Regulatory-metric critique, not a model evaluation."))

u_face = "https://www.holisticai.com/papers/uncovering-bias-in-face-generation-models"
hol.append(row(
 "HOLISTIC-2023-02-SOC1","HOLISTIC-2023-02",HI,CT,"Uncovering Bias in Face Generation Models","2023-02-23",
 "Societal / bias","GAN and diffusion face-generation models trained on CelebA (including InterFaceGAN attribute modifiers and post-processing bias mitigators)","Post-deployment",u_face,
 "Across all CelebA-trained generators studied, Holistic AI measured attribute preferences of 75-85% for whiteness and 60-80% for female gender, with low probabilities of generating children and older men; post-processing mitigators shifted feature concentration (self-similarity) even where KL divergence and FID looked similar.",
 "generators suffer from bias across all social groups with attribute preferences such as between 75%-85% for whiteness and 60%-80% for the female gender (for all trained CelebA models) and low probabilities of generating children and older men",
 "yes","no","capability-finding; non-frontier","face-generation, demographic-bias, gan, celeba, bias-mitigation",
 "Cached text is the paper landing page (abstract only); the full PDF sits behind a download form, so only abstract-level numbers were used."))

u_lib = "https://www.holisticai.com/papers/libvulnwatch"
hol.append(row(
 "HOLISTIC-2025-05-GOV1","HOLISTIC-2025-05",HI,CT,"LibVulnWatch: A Deep Assessment Agent System and Leaderboard for Uncovering Hidden Vulnerabilities in Open-Source AI Libraries","2025-05-13",
 "Governance / evaluation methodology","LibVulnWatch agent system (LangGraph-orchestrated); applied to 20 open-source AI libraries","N/A",u_lib,
 "Holistic AI's graph-orchestrated assessment agents reproduced up to 88% of applicable OpenSSF Scorecard checks (55-88% baseline alignment across libraries) while surfacing typically 5-13 and up to 19 unique additional risks per library, though they sometimes missed contributor declarations, CI testing evidence and explicit security-testing policies that the baseline tool caught.",
 "our approach covers up to 88% of OpenSSF Scorecard checks while surfacing up to 19 additional risks per library, such as critical RCE vulnerabilities, missing SBOMs, and regulatory gaps.",
 "no","","methodology","agentic-assessment, openssf-scorecard, supply-chain, leaderboard",""))

hol.append(row(
 "HOLISTIC-2025-05-CYB1","HOLISTIC-2025-05",HI,CT,"LibVulnWatch: A Deep Assessment Agent System and Leaderboard for Uncovering Hidden Vulnerabilities in Open-Source AI Libraries","2025-05-13",
 "Cyber / supply-chain governance","20 widely used open-source AI libraries (ML frameworks, LLM inference engines, agent orchestration tools; e.g. PyTorch, TensorFlow, vLLM, SGLang, LangChain, LangGraph, JAX)","N/A",u_lib,
 "Assessing 20 widely used open-source AI libraries across licensing, security, maintenance, dependency and regulatory domains, Holistic AI found systemic weaknesses - widespread absence of SBOMs and unmanaged transitive dependencies, RCEs from insecure defaults, unsigned releases and immature disclosure policies, and pervasive GDPR/HIPAA/AI Act documentation gaps - with newer AI agent frameworks scoring lower than mature core ML frameworks.",
 "Our findings reveal a critical gap: many technically advanced AI libraries exhibit significant shortcomings in enterprise readiness, particularly in supply chain security and regulatory preparedness",
 "no","","governance","open-source-supply-chain, sbom, rce, regulatory-gaps, ai-libraries",
 "Finding concerns software libraries rather than models, so no company-model accountability row is created."))

u_mtg = "https://www.holisticai.com/papers/mind-the-gap"
hol.append(row(
 "HOLISTIC-2025-09-JAI1","HOLISTIC-2025-09",HI,CT,"Mind the Gap: Evaluating Model- and Agentic-Level Vulnerabilities in LLMs with Action Graphs","2025-09-05",
 "Jailbreaks","GPT-OSS-20B (OpenAI)","Post-deployment",u_mtg,
 "Using HarmBench single-turn and iterative-refinement attacks, Holistic AI measured a 39.47% model-level attack success rate for GPT-OSS-20B, and found agentic deployment adds vulnerabilities invisible to model-level testing, with tool-calling showing 24-60% higher ASR and direct model-to-agentic attack transfer reaching 57% human-injection ASR.",
 "Model-level evaluation reveals baseline differences: GPT-OSS-20B (39.47% ASR) versus Gemini-2.0-flash (50.00% ASR), with both models showing susceptibility to social engineering while maintaining logic-based attack resistance.",
 "yes","no","capability-finding; non-frontier","agentseer, harmbench, agentic-vulnerability, tool-calling",
 "Models are used partly as instruments validating the AgentSeer framework. Cached text is the paper landing page (abstract only)."))

hol.append(row(
 "HOLISTIC-2025-09-JAI2","HOLISTIC-2025-09",HI,CT,"Mind the Gap: Evaluating Model- and Agentic-Level Vulnerabilities in LLMs with Action Graphs","2025-09-05",
 "Jailbreaks","Gemini-2.0-flash (Google)","Post-deployment",u_mtg,
 "Under the same HarmBench attacks, Gemini-2.0-flash showed a 50.00% model-level attack success rate - higher than GPT-OSS-20B - with agentic tool-calling contexts raising ASR by 24-60%, while direct model-to-agentic attack transfer degraded to 28% human-injection ASR.",
 "Direct attack transfer from model-level to agentic contexts shows degraded performance (GPT-OSS-20B: 57% human injection ASR; Gemini-2.0-flash: 28%), while context-aware iterative attacks successfully compromise objectives that failed at model-level, confirming systematic evaluation gaps.",
 "yes","no","capability-finding","agentseer, harmbench, agentic-vulnerability, tool-calling",
 "Models are used partly as instruments validating the AgentSeer framework. Cached text is the paper landing page (abstract only)."))

hol.append(row(
 "HOLISTIC-2025-09-GOV1","HOLISTIC-2025-09",HI,CT,"Mind the Gap: Evaluating Model- and Agentic-Level Vulnerabilities in LLMs with Action Graphs","2025-09-05",
 "Governance / evaluation methodology","AgentSeer observability framework (validated on GPT-OSS-20B and Gemini-2.0-flash)","N/A",u_mtg,
 "Holistic AI introduces AgentSeer, which decomposes agentic executions into action and component graphs, and shows model-level safety evaluation systematically misses agentic risk: 'agentic-only' vulnerabilities emerge exclusively in agentic contexts, agent transfer operations are the highest-risk tools, and vulnerability mechanisms are semantic rather than syntactic across both models tested.",
 "We discover \"agentic-only\" vulnerabilities that emerge exclusively in agentic contexts, with tool-calling showing 24-60% higher ASR across both models.",
 "no","","methodology","agentseer, action-graphs, agentic-evaluation, observability",""))

write("holistic_ai", hol)

write_dups("holistic_ai", [
 ["Claude 3 7 sonnet jailbreaking audit","https://www.holisticai.com/red-teaming/claude-3-7-sonnet-jailbreaking-audit","HOLISTIC-2025-02-JAI3",
  "Same audit already in v10: Claude 3.7 Sonnet blocked all 37 jailbreak attempts (100% resistance), 0/237 unsafe responses. No new measured result in the cached page."],
 ["Chatgpt 4 5 jailbreaking red teaming","https://www.holisticai.com/red-teaming/chatgpt-4-5-jailbreaking-red-teaming","HOLISTIC-2025-03-JAI1",
  "Same audit already in v10: GPT-4.5 blocked 97% of jailbreak attempts with >99% overall safe-response rate, higher than o1, at higher per-token cost. The page's recaps of the DeepSeek R1 (32%) and Grok-3 (2.7%) audits are also already in v10 as HOLISTIC-2025-02-JAI1 and JAI2."],
])

# ===================== SHANGHAI AI LAB =====================
SI = "Shanghai AI Laboratory (AI45 Lab)"
ST = "Non-Profit (Independent)"
sh = []

u_wm = "https://research.ai45.shlab.org.cn/Blog_pics/94-Building%20intelligence%20identification%20system%20via%20large%20language%20model%20watermarking%20a%20survey%20and%20beyond.pdf"
sh.append(row(
 "SHANGHAIAILAB-2025-04-SOC1","SHANGHAIAILAB-2025-04",SI,ST,"Building intelligence identification system via large language model watermarking: a survey and beyond (Artificial Intelligence Review)","2025-04",
 "Societal / content provenance","N/A (survey and evaluation of published LLM watermarking algorithms)","N/A",u_wm,
 "Scoring published LLM watermarking algorithms against the ten evaluation dimensions the authors define, the team finds none covers them all - methods such as Yoo et al. (2024) and Li et al. (2023) score well on accuracy and AUROC but fall short on robustness and imperceptibility - and argues existing watermark evaluation tools need extending to cover all ten.",
 "current watermarking algorithms do not fully address all ten dimensions that an ideal watermarking algorithm should encompass.",
 "no","","methodology","watermarking, provenance, evaluation-metrics, survey",
 "Primarily a survey; only the authors' own framework, metric analysis (Table 4) and experiments are treated as findings."))

sh.append(row(
 "SHANGHAIAILAB-2025-04-SOC2","SHANGHAIAILAB-2025-04",SI,ST,"Building intelligence identification system via large language model watermarking: a survey and beyond (Artificial Intelligence Review)","2025-04",
 "Societal / content provenance","Three multi-bit watermarking schemes (Cyclic-Shift hash, MPAC, CTWL), with LLaMA-2-13B as the perplexity oracle","N/A",u_wm,
 "In the authors' own experiments on three multi-bit watermarking schemes, success rate, text quality (perplexity) and information density (bits per word) trade off against each other: at fixed information density, better text quality comes with lower extraction success rate, and lowering information density improves both other metrics.",
 "a trade-off exists between text quality, watermark success rate, and information density. At the same information density, achieving better text quality often results in a decreased success rate.",
 "no","","methodology","watermarking, multi-bit, text-quality, information-density",""))

u_tr = "https://arxiv.org/pdf/2402.19465"
sh.append(row(
 "SHANGHAIAILAB-2024-02-ALI1","SHANGHAIAILAB-2024-02B",SI,ST,"Towards Tracing Trustworthiness Dynamics: Revisiting Pre-training Period of Large Language Models (ACL 2024 Findings)","2024-02",
 "Alignment","LLM360 Amber pre-training checkpoints (360 checkpoints), plus AmberChat and AmberSafe","N/A",u_tr,
 "Linear probing across 360 LLM360 Amber pre-training checkpoints shows LLMs already encode linearly separable representations of reliability, privacy, toxicity, fairness and robustness early in pre-training, and mutual-information probing reveals a two-phase fitting-then-compression dynamic over the pre-training period.",
 "The high probing accuracy suggests that LLMs in early pre-training can already distinguish concepts in each trustworthiness dimension.",
 "yes","no","capability-finding; non-frontier","probing, pre-training-dynamics, trustworthiness, mutual-information",
 "Report ID suffixed 'B' because SHANGHAIAILAB-2024-02 is already used by SALAD-Bench in v10."))

sh.append(row(
 "SHANGHAIAILAB-2024-02-ALI2","SHANGHAIAILAB-2024-02B",SI,ST,"Towards Tracing Trustworthiness Dynamics: Revisiting Pre-training Period of Large Language Models (ACL 2024 Findings)","2024-02",
 "Alignment","LLM360 Amber pre-training checkpoints","N/A",u_tr,
 "The authors show pre-training checkpoints can be used as an alignment resource: steering vectors extracted from them improve the trustworthiness of the fully pre-trained model, a technique not available if only the final checkpoint is studied.",
 "we extract steering vectors from a LLM's pre-training checkpoints to enhance the LLM's trustworthiness.",
 "no","","methodology","steering-vectors, alignment-technique, pre-training-checkpoints",""))

u_vis = "https://arxiv.org/pdf/2507.02844"
sh.append(row(
 "SHANGHAIAILAB-2025-07-JAI1","SHANGHAIAILAB-2025-07A",SI,ST,"Visual Contextual Attack: Jailbreaking MLLMs with Image-Driven Context Injection (EMNLP 2025)","2025-07",
 "Jailbreaks","GPT-4o and GPT-4o-mini (OpenAI)","Post-deployment",u_vis,
 "The VisCo vision-centric jailbreak reached an average attack success rate of 85.00% on GPT-4o and 86.13% on GPT-4o-mini on MM-SafetyBench (gains of 62.80 and 62.56 percentage points over the QR Attack baseline), with a toxicity score of 4.78 on GPT-4o versus 2.48 for the baseline; on SafeBench-Tiny, GPT-4o's ASR rose from 12% under the original FigStep attack to 76% under VisCo.",
 "In terms of average ASR, VisCo Attack achieves 85.00%, 86.13%, 91.07%, and 89.88% on GPT-4o, GPT-4o-mini, Gemini-2.0-Flash, and InternVL2.5-78B, respectively, corresponding to absolute gains of 62.80, 62.56, 60.00, and 55.83 percentage points (pp) over QR Attack.",
 "yes","yes","capability-finding","multimodal-jailbreak, mm-safetybench, context-injection, black-box",
 "Report ID suffixed 'A' to disambiguate four Shanghai AI Lab reports dated 2025-07. [Report tested: Qwen2.5-VL-72B-Instruct as an additional target, 64% ASR under the FigStep baseline.]"))

sh.append(row(
 "SHANGHAIAILAB-2025-07-JAI2","SHANGHAIAILAB-2025-07A",SI,ST,"Visual Contextual Attack: Jailbreaking MLLMs with Image-Driven Context Injection (EMNLP 2025)","2025-07",
 "Jailbreaks","Gemini-2.0-Flash (Google)","Post-deployment",u_vis,
 "The VisCo vision-centric jailbreak reached an average attack success rate of 91.07% against Gemini-2.0-Flash on MM-SafetyBench, 60.00 percentage points above the QR Attack baseline, with toxicity scores above 4.5 in every case.",
 "In terms of average ASR, VisCo Attack achieves 85.00%, 86.13%, 91.07%, and 89.88% on GPT-4o, GPT-4o-mini, Gemini-2.0-Flash, and InternVL2.5-78B, respectively, corresponding to absolute gains of 62.80, 62.56, 60.00, and 55.83 percentage points (pp) over QR Attack.",
 "yes","yes","capability-finding","multimodal-jailbreak, mm-safetybench, context-injection, black-box",""))

sh.append(row(
 "SHANGHAIAILAB-2025-07-JAI3","SHANGHAIAILAB-2025-07A",SI,ST,"Visual Contextual Attack: Jailbreaking MLLMs with Image-Driven Context Injection (EMNLP 2025)","2025-07",
 "Jailbreaks","InternVL2.5-78B (OpenGVLab / Shanghai AI Laboratory)","Post-deployment",u_vis,
 "The VisCo jailbreak reached an average attack success rate of 89.88% against the open-weight InternVL2.5-78B on MM-SafetyBench, 55.83 percentage points above the QR Attack baseline.",
 "In terms of average ASR, VisCo Attack achieves 85.00%, 86.13%, 91.07%, and 89.88% on GPT-4o, GPT-4o-mini, Gemini-2.0-Flash, and InternVL2.5-78B, respectively, corresponding to absolute gains of 62.80, 62.56, 60.00, and 55.83 percentage points (pp) over QR Attack.",
 "yes","no","capability-finding; company-self-report","multimodal-jailbreak, open-weights, mm-safetybench",
 "InternVL is developed by OpenGVLab/Shanghai AI Laboratory, so this is the evaluator testing an in-house model."))

u_esc = "https://arxiv.org/pdf/2406.14952"
sh.append(row(
 "SHANGHAIAILAB-2024-06-HUM1","SHANGHAIAILAB-2024-06A",SI,ST,"ESC-Eval: Evaluating Emotion Support Conversations in Large Language Models (EMNLP 2024)","2024-06",
 "Human Influence / emotional support","14 LLMs used as emotion-support models, including general assistants (e.g. ChatGPT, Llama3) and ESC-oriented models (e.g. ExTES-Llama); evaluated in aggregate","Post-deployment",u_esc,
 "Interacting 14 LLMs with a trained role-playing agent (ESC-Role) over 2,801 role cards and manually annotating the multi-turn dialogues, the team found ESC-oriented LLMs outperform general-purpose assistants at emotional support but all remain below human performance.",
 "exhibit superior ESC abilities compared to general AI-assistant LLMs, but there is still a gap behind human performance",
 "yes","no","capability-trend; anonymised-model","emotional-support, mental-health, role-play-evaluation, human-comparison",
 "Report ID suffixed 'A' to disambiguate two Shanghai AI Lab reports dated 2024-06. Aggregate finding across 14 models; per-model scores are in the paper's tables and were not extracted."))

sh.append(row(
 "SHANGHAIAILAB-2024-06-HUM2","SHANGHAIAILAB-2024-06A",SI,ST,"ESC-Eval: Evaluating Emotion Support Conversations in Large Language Models (EMNLP 2024)","2024-06",
 "Governance / evaluation methodology","ESC-Role role-playing evaluator and ESC-RANK automatic scorer","N/A",u_esc,
 "The team built an interactive evaluation pipeline for emotional-support conversation - a role-playing model (ESC-Role) driven by 2,801 reorganised role cards, followed by human annotation - and trained ESC-RANK on 59,654 manual evaluation results, reporting scoring performance that surpasses GPT-4 by 35 points.",
 "we developed ESC-RANK, which trained on the annotated data, achieving a scoring performance surpassing 35 points of GPT-4.",
 "no","","methodology","role-play-agent, automatic-judge, esc-rank, evaluation-pipeline",""))

u_cel = "https://arxiv.org/pdf/2406.19131v1"
sh.append(row(
 "SHANGHAIAILAB-2024-06-AUT1","SHANGHAIAILAB-2024-06B",SI,ST,"CELLO: Causal Evaluation of Large Vision-Language Models (EMNLP)","2024-06",
 "Autonomy / embodied reasoning","GPT-4o, Gemini-1.5-Pro, Claude-3-opus, Claude-3-sonnet, plus BLIP-2, LLaVA-Mistral, BakLlava, LLaVA-Vicuna, MiniCPM-Llama3-V-2.5 and Qwen-VL (aggregate)","Post-deployment",u_cel,
 "On CELLO's 14,094 causal questions spanning discovery, association, intervention and counterfactual levels, no LVLM without CELLO-CoT prompting exceeded 0.5 accuracy on multiple-choice questions; GPT-4o was best overall at 0.59 while Claude-3-sonnet and BLIP-2 scored 0.49 on binary questions, below the 0.5 random baseline.",
 "Notably, their scores on binary questions (0.49) fail to surpass the random baseline of 0.5, indicating significant deficiencies in their causal reasoning abilities.",
 "yes","no","capability-trend","causal-reasoning, vision-language, benchmark, embodied-agents",
 "Aggregate capability-trend row rather than per-company rows; per-model numbers are in Table 2 (GPT-4o 0.59, Gemini-1.5-Pro 0.54, Claude-3-opus 0.52, Claude-3-sonnet 0.40, BLIP-2 0.30 overall). Report ID suffixed 'B' to disambiguate two Shanghai AI Lab reports dated 2024-06. Borderline scope: capability benchmark rather than safety evaluation."))

u_tug = "https://aclanthology.org/2025.acl-long.590.pdf"
sh.append(row(
 "SHANGHAIAILAB-2025-07-ALI2","SHANGHAIAILAB-2025-07B",SI,ST,"The Tug of War Within: Mitigating the Fairness-Privacy Conflicts in Large Language Models (ACL 2025)","2025-07",
 "Alignment / fairness and privacy","Qwen-2-7B-Instruct and other open-weight instruction-tuned LLMs","N/A",u_tug,
 "The team documents a counter-intuitive trade-off: supervised fine-tuning that raises an LLM's privacy awareness on thousands of samples significantly reduces its fairness awareness, a coupling they attribute to shared neurons carrying mutual information between the two dimensions.",
 "we discover a counterintuitive trade-off phenomenon that enhancing an LLM's privacy awareness through Supervised Fine-Tuning (SFT) methods significantly decreases its fairness awareness with thousands of samples.",
 "yes","no","capability-finding; non-frontier","fairness, privacy, sft-side-effects, neuron-coupling",
 "Report ID suffixed 'B' to disambiguate four Shanghai AI Lab reports dated 2025-07 (and to avoid the existing SHANGHAIAILAB-2025-07-ALI1 finding ID in v10)."))

sh.append(row(
 "SHANGHAIAILAB-2025-07-ALI3","SHANGHAIAILAB-2025-07B",SI,ST,"The Tug of War Within: Mitigating the Fairness-Privacy Conflicts in Large Language Models (ACL 2025)","2025-07",
 "Governance / evaluation methodology","Qwen-2-7B-Instruct and other open-weight instruction-tuned LLMs","N/A",u_tug,
 "SPIN, a training-free method that suppresses neurons coupling privacy and fairness awareness, removes the trade-off and improves both dimensions simultaneously without degrading general capabilities - for example improving Qwen-2-7B-Instruct's fairness awareness by 12.2% and privacy awareness by 14.0% - and remains effective with limited or even malicious fine-tuning data where SFT fails.",
 "significantly improves LLMs' fairness and privacy awareness simultaneously without compromising general capabilities, e.g., improving Qwen-2-7B-Instruct's fairness awareness by 12.2% and privacy awareness by 14.0%",
 "no","","methodology","spin, neuron-suppression, training-free-mitigation, fairness-privacy",""))

u_evo = "https://aclanthology.org/2025.findings-acl.754.pdf"
sh.append(row(
 "SHANGHAIAILAB-2025-07-SOC1","SHANGHAIAILAB-2025-07C",SI,ST,"EvoBench: Towards Real-world LLM-Generated Text Detection Benchmarking for Evolving Large Language Models (ACL 2025)","2025-07",
 "Societal / content provenance","14 LLM-generated-text detection methods (incl. Fast-DetectGPT, RADAR) evaluated against 7 LLM families and 29 evolving versions (GPT-4o, Claude, LLaMA and others)","N/A",u_evo,
 "Evaluating 14 detection methods on EvoBench, the team found all of them fail to generalise as LLMs evolve: Fast-DetectGPT falls by up to 25%, from 0.91 AUROC on Claude-3-haiku-20240307 to 0.65 on Claude-3-5-haiku-20241022, and from 0.8003 average accuracy on GPT-4o-05-13 to 0.7422 on GPT-4o-latest, so static benchmarks overstate real-world detector effectiveness.",
 "The widely used detection method, Fast-DetectGPT, declines up to 25% drop when detecting the Claude-3-5-haiku20241022 compared to Claude-3-haiku-20240307.",
 "no","","methodology","llm-text-detection, generalisation, evolving-models, emg-metric",
 "Finding is about detection tooling, not about a model developer's safeguards. Report ID suffixed 'C' to disambiguate four Shanghai AI Lab reports dated 2025-07."))

u_pol = "https://research.ai45.shlab.org.cn/Blog_pics/93-Collectivism%20and%20Individualism%20Political%20Bias%20in%20Large%20Language%20Models%20A%20Two-Step%20Approach.pdf"
sh.append(row(
 "SHANGHAIAILAB-2025-07-SOC2","SHANGHAIAILAB-2025-07D",SI,ST,"Collectivism and Individualism Political Bias in Large Language Models: A Two-Step Approach","2025-07-18",
 "Societal / political bias","12 LLMs from China and the US, including ChatGPT (GPT-3.5-turbo), Claude-1.3, ChatGLM2-6B, InternLM2-20B, Baichuan2-13B, Qwen and Vicuna-7B/13B/33B (aggregate)","Post-deployment",u_pol,
 "Prompting 12 Chinese and US LLMs with 20 purpose-built economic and social questions on a five-point Likert scale, the team found most models produce non-neutral output on collectivism versus individualism and that several also fail the factual test of distinguishing the two concepts; on the same question different models take opposite positions (ChatGPT individualist, ChatGLM2-6B collectivist, InternLM2-20B neutral).",
 "The latter indicates that many LLMs not only fail to accurately distinguish between collectivism and individualism but also exhibit significant political biases in their outputs.",
 "yes","no","capability-finding; anonymised-model","political-bias, collectivism, individualism, value-judgement, likert",
 "Aggregate row across 12 models rather than per-company rows; per-model Likert means are in Table 4. Report ID suffixed 'D' to disambiguate four Shanghai AI Lab reports dated 2025-07."))

sh.append(row(
 "SHANGHAIAILAB-2025-07-SOC3","SHANGHAIAILAB-2025-07D",SI,ST,"Collectivism and Individualism Political Bias in Large Language Models: A Two-Step Approach","2025-07-18",
 "Governance / evaluation methodology","12 LLMs (as instruments of the methodology)","N/A",u_pol,
 "The paper contributes a two-step political-bias evaluation protocol - a value assessment that scores generated content on a five-point Likert scale against a neutrality midpoint of 3, followed by a factual assessment checking whether the model can correctly classify statements as collectivist or individualist - arguing a trustworthy LLM should be accurate on facts while neutral in value judgements.",
 "We propose a two-step approach to evaluate the patterns of bias in the outputs of LLMs as well as a specific set of questions to examine LLM outputs' political bias on collectivism and individualism.",
 "no","","methodology","evaluation-protocol, political-neutrality, value-vs-fact",""))

write("shanghai_ai_laboratory_ai45_l", sh)

write_dups("shanghai_ai_laboratory_ai45_l", [
 ["Safety Benchmarks and Governance Practices for Foundation Models","https://research.ai45.shlab.org.cn/Blog_pics/The%20Tug%20of%20War%20Within%20Mitigating%20the%20Fairness-Privacy%20Conflicts.pdf","SHANGHAIAILAB-2025-07-ALI2 / ALI3",
  "Worklist URL and cached text are byte-identical to 'The Tug of War Within' (same MD5); the titled report is not retrievable at this URL, so no separate rows were created."],
])
