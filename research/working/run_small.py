import sys
sys.path.insert(0, "/private/tmp/claude-501/-Users-kunalsingh-Desktop/9b4cd91a-0a4c-4c96-9f90-0e5248653043/scratchpad")
from emit import row, write, write_dups

GOV = "Government"
NPI = "Non-Profit (Independent)"
NPA = "Non-Profit (AIEF)"
FP = "For-Profit"
TPE = "third-party-evaluator"
GAISI = "government-AISI"

# ============================================================ UK AISI
write("uk_ai_security_institute_uk_.csv", [])
write_dups("uk_ai_security_institute_uk_.csv", [[
    "Inoculation Prompting: Eliciting traits from LLMs during training can suppress them at test-time",
    "https://www.aisi.gov.uk/research/inoculation-prompting-eliciting-traits-from-llms-during-training-can-suppress-them-at-test-time",
    "UKAISI-2026-08b-ALI1 (staging)",
    "Same report, same claim (inoculation prompting reduces emergent misalignment / backdoors / subliminal trait transmission). Already staged by coordinator; cached page contains only the abstract, so no additional codeable finding.",
]])

# ============================================================ US CAISI
u = "https://www.nist.gov/news-events/news/2026/02/new-report-expanding-ai-evaluation-toolbox-statistical-models"
write("us_center_for_ai_standards_a.csv", [
    row("USCAISI-2026-02-GOV2", "USCAISI-2026-02",
        "US Center for AI Standards and Innovation (CAISI), NIST", GOV,
        "New Report: Expanding the AI Evaluation Toolbox with Statistical Models (NIST AI 800-3)",
        "2026-02-19", "Eval-methodology",
        "22 frontier LLMs (unnamed) on GPQA-Diamond, BIG-Bench Hard, Global-MMLU Lite", "Aggregate", u,
        "Applying GLMMs to GPQA-Diamond, CAISI found the benchmark's chemistry questions were particularly difficult for the 22 tested LLMs, and that model-estimated question difficulty has only a weak relationship with the difficulty labels assigned by the humans who wrote the questions.",
        "These estimates show that GPQA-Diamond's chemistry questions were particularly difficult for the 22 tested LLMs. On the other hand, question difficulty for LLMs has a weak relationship with question-writer-labeled difficulty. This may suggest that humans and the tested LLMs find different questions difficult, and/or could call into question whether writer annotations are accurate even for human difficulty.",
        "no", "", "methodology;anonymised-model",
        "caisi;nist;nist-ai-800-3;glmm;gpqa-diamond;benchmark-quality;eval-methodology", GAISI,
        "[Report tested: 22 frontier LLMs, unnamed in the news release.] Distinct from staged USCAISI-2026-02-GOV1, which codes the three benchmark-analysis defects and the GLMM framework; this row codes the benchmark-composition result about GPQA-Diamond."),
])
write_dups("us_center_for_ai_standards_a.csv", [[
    "New Report: Expanding the AI Evaluation Toolbox with Statistical Models",
    u, "USCAISI-2026-02-GOV1 (staging)",
    "The framework finding (benchmark vs generalized accuracy, three analysis defects, GLMM proposal) is already staged. Only the GPQA-Diamond question-difficulty result is emitted as new.",
]])

# ============================================================ Japan AISI
u2 = "https://aisi.go.jp/activity/activity_notes/260708/"
write("japan_ai_safety_institute_j_.csv", [
    row("JAISI-2026-07-CYB2", "JAISI-2026-07",
        "Japan AI Safety Institute (J-AISI)", GOV,
        "AI Experiment Notes: AI Models Differ in the Vulnerabilities They Find! (AI検証ノート：AIが見つける脆弱性に違い！)",
        "2026-07-08", "Cyber;Jailbreaks",
        "anonymised (three generally available AI models, 'Model 1/2/3')", "Post-deployment", u2,
        "During a defensive software vulnerability assessment, the generally available models' own safety controls sometimes blocked part of the output, so Japan AISI reported its finding counts (15, 13 and 13 issues) as reference values only; it attributes this to the difficulty of distinguishing defensive vulnerability-finding from attack-oriented use.",
        "However, in some cases, safety controls prevented part of the output from being obtained. This is a safety feature designed to prevent the malicious use of AI. Because it can be difficult to automatically distinguish such misuse from the purpose of finding vulnerabilities, this kind of intervention can occur even during normal, defensive use. Accordingly, the number of findings reported here should be treated as reference information only.",
        "yes", "no", "capability-finding;anonymised-model",
        "j-aisi;japan;vulnerability-detection;over-refusal;safety-controls;defensive-use;anonymised", GAISI,
        "Bilingual JP/EN page - not a non-English drop. Distinct from staged JAISI-2026-07-CYB1 (which codes the between-model divergence in detected vulnerabilities); this row codes the over-refusal/safeguard interference with defensive use."),
])
write_dups("japan_ai_safety_institute_j_.csv", [
    ["AI検証ノート：AIが見つける脆弱性に違い！/ AI Experiment Notes: AI Models Differ in the Vulnerabilities They Find!",
     u2, "JAISI-2026-07-CYB1 (staging)",
     "The between-model divergence finding (15/13/13 issues, differing severity assignments) is already staged. Only the safeguard-interference finding is emitted as new."],
    ["2025年度 データ品質 SWG 活動報告書の公開 (FY2025 Data Quality SWG Activity Report)",
     "https://aisi.go.jp/output/output_information/260415/", "JAISI-2026-04-GOV1 (staging)",
     "Entire page is a release notice for the SWG activity report; the only codeable content (quality characteristics by use case, checklist development/validation, gazette-data verification) is exactly what the staged row captures."],
])

# ============================================================ Gray Swan
write("gray_swan_ai.csv", [])
write_dups("gray_swan_ai.csv", [
    ["Comparing AI Agents to Cybersecurity Professionals In Real-World Penetration Testing (2025-12)",
     "https://www.grayswan.ai/research/comparing-ai-agents-to-cybersecurity-professionals-in-real-world-penetration-testing",
     "GRAYSWAN-2025-12-CYB1 / GRAYSWAN-2025-12-CYB2 (v10)",
     "Same December 2025 live-enterprise study already coded in v10 as 'Conducting The First Live Enterprise Comparison Between Agents and Humans' (ARTEMIS on Claude Sonnet 4; OpenAI Codex/CyAgent). Cached page carries only the abstract and says 'This research is currently only available at its source.'"],
    ["Comparing AI Agents to Cybersecurity Professionals In Real-World Penetration Testing (undated duplicate row)",
     "https://www.grayswan.ai/research/comparing-ai-agents-to-cybersecurity-professionals-in-real-world-penetration-testing",
     "GRAYSWAN-2025-12-CYB1 / GRAYSWAN-2025-12-CYB2 (v10)",
     "Exact duplicate URL of the row above within the worklist itself."],
])

# ============================================================ LatticeFlow
u3 = "https://latticeflow.ai/news/open-genai-models-proven-secure-for-enterprise-adoption-new-evaluation-shows"
u4 = "https://latticeflow.ai/news/finma-technical-blueprint-agentic-ai"
Q3 = "DeepSeek R1 : from 1.8% to 98.6% LLaMA-4 Maverick : from 33.5% to 99.4% LLaMA-3.3 70B Instruct : from 51.8% to 99.4% Qwen3-32B : security score increased from 56.3% to 99.6% All models maintained over 98% quality of service, confirming that security gains did not compromise user experience"
write("latticeflow_ai.csv", [
    row("LATTICEFLOW-2025-09b-CYB1", "LATTICEFLOW-2025-09b", "LatticeFlow AI", FP,
        "Open GenAI Models Proven Secure for Enterprise Adoption, New Evaluation Shows",
        "2025-09-23", "Cyber;Jailbreaks", "DeepSeek R1; DeepSeek-V3-0324 (DeepSeek)", "Post-deployment", u3,
        "In LatticeFlow AI's enterprise security evaluation of five open foundation models, DeepSeek R1 had the weakest baseline security score of any model tested at 1.8%, rising to 98.6% once a dedicated input-filtering guardrail layer was added.",
        Q3, "yes", "yes", "capability-finding",
        "latticeflow;deepseek-r1;prompt-injection;guardrails;open-weight;enterprise-security", TPE,
        "[Report tested: Qwen3-32B, DeepSeek-V3-0324, Llama-4-Maverick-17B-128E-Instruct, DeepSeek-R1, Meta-Llama-3.3-70B-Instruct; evaluation run with SambaNova.] Judgement call: report framing is reassuring ('proven secure') but the 1.8% unguarded score for a specific named model is a concerning result a developer could reasonably respond to, hence Tier A."),
    row("LATTICEFLOW-2025-09b-CYB2", "LATTICEFLOW-2025-09b", "LatticeFlow AI", FP,
        "Open GenAI Models Proven Secure for Enterprise Adoption, New Evaluation Shows",
        "2025-09-23", "Cyber;Jailbreaks", "Llama-4-Maverick-17B-128E-Instruct; Meta-Llama-3.3-70B-Instruct (Meta)", "Post-deployment", u3,
        "Meta's open models scored 33.5% (Llama-4 Maverick) and 51.8% (Llama-3.3 70B Instruct) on LatticeFlow's baseline enterprise security evaluation, each rising to 99.4% with a dedicated input-filtering guardrail layer while maintaining over 98% quality of service.",
        Q3, "yes", "no", "capability-finding",
        "latticeflow;llama-4-maverick;llama-3-3-70b;meta;prompt-injection;guardrails", TPE,
        "[Report tested: five open models incl. DeepSeek and Qwen.] Tier B: mid-range baseline scores presented comparatively and fully remediated by guardrails."),
    row("LATTICEFLOW-2025-09b-CYB3", "LATTICEFLOW-2025-09b", "LatticeFlow AI", FP,
        "Open GenAI Models Proven Secure for Enterprise Adoption, New Evaluation Shows",
        "2025-09-23", "Cyber;Jailbreaks", "Qwen3-32B (Alibaba)", "Post-deployment", u3,
        "Alibaba's Qwen3-32B had the highest baseline security score of the five open models LatticeFlow tested at 56.3%, rising to 99.6% with a guardrail layer while maintaining over 98% quality of service.",
        Q3, "yes", "no", "capability-finding;reassuring-null",
        "latticeflow;qwen3-32b;alibaba;prompt-injection;guardrails", TPE,
        "[Report tested: five open models.] Tier B: best-in-set comparative result, no dangerous threshold crossed."),
    row("LATTICEFLOW-2026-02-GOV1", "LATTICEFLOW-2026-02", "LatticeFlow AI (with Unique AI)", FP,
        "First FINMA-Aligned Technical Blueprint Sets a New Standard to Govern Agentic AI",
        "2026-02-10", "Policy/Standards", "Unique AI Investment Insights Agent (agentic AI deployed in banks)", "Post-deployment", u4,
        "LatticeFlow AI mapped FINMA guidance 08/2024 to measurable technical controls and applied the resulting assessment to Unique AI's Investment Insights Agent, an agentic system already deployed across financial institutions, producing evidence on output consistency, response to changing inputs, and whether human users can understand, challenge and override its recommendations.",
        "By mapping the Swiss Financial Market Supervisory Authority ( FINMA)’s guidance ( FINMA guidance 08/2024 ) to measurable technical controls (including testing, monitoring, explainability, and model robustness), the blueprint shows how banks can move from policy and abstract principles to audit-ready evidence.",
        "no", "", "governance",
        "latticeflow;unique-ai;finma;switzerland;agentic-ai;governance;banking", TPE,
        "UNCERTAIN: this is close to a joint product/initiative announcement and reports no measured results. Included as a Tier C governance/methodology row by analogy with the existing LATTICEFLOW-2024-10-GOV1 COMPL-AI framework row; drop if the coordinator prefers to exclude framework press releases."),
])
write_dups("latticeflow_ai.csv", [])

# ============================================================ Tsinghua CoAI
u5 = "https://arxiv.org/abs/2105.08920"
u6 = "https://arxiv.org/abs/2201.06025"
write("tsinghua_university_coai_gro.csv", [
    row("TSINGHUACOAI-2021-05-GOV1", "TSINGHUACOAI-2021-05",
        "Tsinghua University CoAI Group", NPI,
        "OpenMEVA: A Benchmark for Evaluating Open-ended Story Generation Metrics",
        "2021", "Eval-methodology", "anonymised (existing automatic NLG metrics)", "N/A", u5,
        "Evaluating existing automatic NLG metrics on the OpenMEVA benchmark, the CoAI group found the metrics correlate poorly with human judgments, fail to recognise discourse-level incoherence, and lack inferential knowledge, generalization ability and robustness.",
        "We evaluate existing metrics on OpenMEVA and observe that they have poor correlation with human judgments, fail to recognize discourse-level incoherence, and lack inferential knowledge (e.g., causal order between events), the generalization ability and robustness.",
        "no", "", "methodology;anonymised-model",
        "tsinghua-coai;openmeva;nlg-metrics;automatic-evaluation;llm-judge;eval-methodology", TPE,
        "Only the arXiv abstract page was cached; no per-metric numbers available. Relevance is indirect (automatic-metric reliability, adjacent to LLM-judge reliability)."),
    row("TSINGHUACOAI-2022-01-SOC1", "TSINGHUACOAI-2022-01",
        "Tsinghua University CoAI Group", NPI,
        "COLD: A Benchmark for Chinese Offensive Language Detection",
        "2022", "Societal", "anonymised (popular Chinese pre-trained generative language models)", "Post-deployment", u6,
        "Using their COLDETECTOR classifier, the CoAI group found that popular Chinese pre-trained generative models all expose varying degrees of offensive output, and that anti-bias content and keywords referring to particular groups or expressing negative attitudes make offensive generations more likely.",
        "We first analyze the offensiveness of existing generative models and show that these models inevitably expose varying degrees of offensive issues. Furthermore, we investigate the factors that influence the offensive generations, and we find that anti-bias contents and keywords referring to certain groups or revealing negative attitudes trigger offensive outputs easier.",
        "yes", "no", "capability-finding;anonymised-model;non-frontier",
        "tsinghua-coai;cold;chinese;offensive-language;toxicity;non-frontier", TPE,
        "Only the arXiv abstract page was cached; individual models are not named there. Non-frontier 2022 Chinese PLMs."),
])
write_dups("tsinghua_university_coai_gro.csv", [])
