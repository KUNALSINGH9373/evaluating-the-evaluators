import sys
sys.path.insert(0, "/private/tmp/claude-501/-Users-kunalsingh-Desktop/9b4cd91a-0a4c-4c96-9f90-0e5248653043/scratchpad")
from emit import row, write, write_dups

RW = "Redwood Research"
NPI = "Non-Profit (Independent)"
TPE = "third-party-evaluator"
uSH = "https://www.anthropic.com/research/shade-arena-sabotage-monitoring"
uSL = "https://alignment.anthropic.com/2026/sleight-bench"
TSH = "SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents"
TSL = "SLEIGHT-Bench: Finding Blind Spots in AI Monitors"
NSH = "Company-published: Anthropic research post, in scope because Redwood Research (Tyler Tracy, Buck Shlegeris) and Scale AI (Xiang Deng, Chen Bo Calvin Zhang) are named collaborating co-authors. Filed under the independent evaluator per the venue rule."
NSL = "Company-published: Anthropic Alignment Science blog post, in scope because Tyler Tracy of Redwood Research is a named co-author. Filed under the independent evaluator per the venue rule."

rows = [
    row("ANTHROPIC-2025-06-SELF-ALI1", "ANTHROPIC-2025-06-SELF-SHADE", RW, NPI, TSH,
        "2025-06-16", "Alignment;Autonomy",
        "anonymised (14 large language models tested as saboteurs in SHADE-Arena)", "Post-deployment", uSH,
        "Across 14 models on SHADE-Arena's 17 paired benign/sabotage agentic tasks, no model exceeded a 30% overall sabotage success rate and most were below 10%, which the authors read as current models being unable to engage in these behaviours.",
        "Success rates were generally low. No models exceeded an overall success rate of 30% on the tasks; most were below 10%. This reflects the very high difficulty of the tasks in SHADE-Arena—this is good news in the sense that current models aren't able to engage in these dangerous behaviours, and that there's a lot of room for the evaluation to be used with even smarter models in future.",
        "yes", "no", "capability-finding;reassuring-null;anonymised-model;company-published",
        "redwood;shade-arena;sabotage;agentic;monitoring;reassuring-null;company-published", TPE, NSH),
    row("ANTHROPIC-2025-06-SELF-ALI2", "ANTHROPIC-2025-06-SELF-SHADE", RW, NPI, TSH,
        "2025-06-16", "Alignment;Autonomy",
        "anonymised (strongest of 14 models tested in SHADE-Arena)", "Post-deployment", uSH,
        "Although overall SHADE-Arena success rates were low, the strongest models achieved the malicious side task without being caught by the monitor (evasion success) almost 60% of the time, and some individual tasks were solved by the strongest models around 50% of the time.",
        "However, the strongest models were able to successfully achieve the side task without being caught (evasion success) almost 60% of the time. Looking across the different tasks, we found a range of difficulties: some were solved around 50% of the time by the strongest models, and some were hardly ever solved at all by any model, even with tens of attempts.",
        "yes", "no", "capability-finding;anonymised-model;company-published",
        "redwood;shade-arena;evasion;monitor-evasion;sabotage;anonymised;company-published", TPE, NSH),
    row("ANTHROPIC-2025-06-SELF-ALI3", "ANTHROPIC-2025-06-SELF-SHADE", RW, NPI, TSH,
        "2025-06-16", "Alignment;Eval-methodology",
        "Gemini 2.5 Pro (Google), best monitor tested; default monitor Claude Sonnet 3.6 (Anthropic)", "Post-deployment", uSH,
        "The best monitor model tested, Gemini 2.5 Pro, still required accepting a false positive rate of over 20% to reach an 80% chance of spotting a sabotage side task - which the authors judge is not feasible for real-world deployment - though the best monitors did outperform human evaluators who spent more than 1.5 hours reading the same transcripts.",
        "The best monitor model we tested in our experiments was Gemini 2.5 Pro. But even that wasn't a particularly effective monitor: our results showed that to have an 80% chance of spotting a side task, we'd have to accept a false positive rate (where the monitor claims it's seen a side task occurring when no such side task was present) of over 20%. That's not feasible for a real-world deployment, so we have to work harder to train monitors to spot these subtle sabotage attempts.",
        "yes", "no", "capability-finding;company-published",
        "redwood;shade-arena;gemini-2-5-pro;google;monitoring;false-positive-rate;company-published", TPE,
        NSH + " [Report tested: a group of human evaluators reading the same transcripts as comparator.]"),
    row("ANTHROPIC-2025-06-SELF-ALI4", "ANTHROPIC-2025-06-SELF-SHADE", RW, NPI, TSH,
        "2025-06-16", "Alignment", "Claude Opus 4; Claude Sonnet 3.7 (Anthropic)", "Post-deployment", uSH,
        "When the monitor was given access to the attacking model's chain of thought, Claude Opus 4 revealed the secret side task in every example studied, whereas Claude Sonnet 3.7 in extended-thinking mode was often able to hide its true intention while still completing the side task when instructed not to mention it.",
        "For example, when we turned on \"extended thinking\" mode, revealing Claude Sonnet 3.7's thought process, and instructed it not to mention the side task, it was often able to hide its true intention even as it completed the side task. But Claude Opus 4 revealed the side task in every example we studied—sometimes, ironically, mentioning that it was critical that it not mention the side task",
        "yes", "no", "capability-finding;company-published",
        "redwood;shade-arena;claude-opus-4;claude-sonnet-3-7;anthropic;cot-monitorability;company-published", TPE, NSH),

    row("ANTHROPIC-2026-05-SELF-ALI1", "ANTHROPIC-2026-05-SELF-SLEIGHT", RW, NPI, TSL,
        "2026-05", "Alignment;Cyber", "Claude Opus 4.6 as monitor (Anthropic)", "Post-deployment", uSL,
        "On SLEIGHT-Bench's 40 synthetic attacks across 11 monitor blind-spot categories, Claude Opus 4.6 - the main monitor studied - never caught 50% of the attacks in any of 10 trials and reliably detected only 8 of 40 at a 1% false positive rate; catch rates were 0% for the n-hops, omission and jailbreak blind spots and 13-15% for counting, model-priors and file/object-reuse attacks.",
        "Detection rates are generally low. On Opus 4.6, the main monitor we work with, 50% of attacks are never caught on any of the 10 trials. Only 8 out of 40 are reliably detected. We believe current frontier models would not independently discover and execute attacks like ours. But our dataset shows that attacks targeting monitor blind spots can reliably evade detection, and monitoring systems are not yet robust to more sophisticated adversaries.",
        "yes", "yes", "capability-finding;company-published",
        "redwood;sleight-bench;claude-opus-4-6;anthropic;ai-control;monitoring;blind-spots;company-published", TPE,
        NSL + " [Report tested: frontier models from multiple providers including Claude, Gemini and GPT models as monitors; only Opus 4.6 results are quantified in the post.] Per-blind-spot catch rates at 1% FPR are from the post's blind-spot table."),
    row("ANTHROPIC-2026-05-SELF-GOV1", "ANTHROPIC-2026-05-SELF-SLEIGHT", RW, NPI, TSL,
        "2026-05", "Alignment;Eval-methodology", "Claude Opus 4.6 as monitor (Anthropic)", "Post-deployment", uSL,
        "Prompts targeted at specific monitor blind spots improved detection in the categories they targeted but degraded performance in at least one other category, so no single prompt covered everything; the agentic Claude Code monitor variant that helps close some blind spots costs on average about 10x more model invocations and about 14x more output tokens than a single API call.",
        "Interestingly, we find these prompts improve detection on the categories they target, but degrade performance on at least one other. For instance, the state-tracking prompt catches more file-reuse attacks, but misses more authorization-confusion attacks. No single prompt covers everything, suggesting that using an ensemble of multiple specialized prompts, each watching for different blind spots, may be a promising path forward.",
        "no", "", "methodology;company-published",
        "redwood;sleight-bench;monitor-prompts;ensembling;claude-code;cost;eval-methodology;company-published", TPE,
        NSL + " Cost figures from the post: 'The Claude Code monitor on average takes ~10x more model invocations and generates ~14x more output tokens than the API call.'"),
]
write("anthropic", rows)

write_dups("anthropic", [
    ["Claude 3 Model Card", "https://www-cdn.anthropic.com/c6a80a657af445f40e31afac050f3bf76d3b1404.pdf",
     "n/a - excluded, no evaluator finding reproduced",
     "UK AISI, US AISI and METR are named but no results of theirs are reproduced: 'The UK AISI also conducted pre-deployment testing of a near-final model, and shared their results with the US AI Safety Institute as part of a Memorandum of Understanding' and 'METR did an initial exploration of the model's autonomy-relevant capabilities.' Per the venue rule this is an MOU/no-results mention, so no row."],
    ["Claude 3.5 Sonnet Model Card Addendum", "https://www-cdn.anthropic.com/fed9cc193a14b84131812372d8d5857f8f304c52/Model_Card_Claude_3_Addendum.pdf",
     "n/a - excluded, no evaluator finding reproduced",
     "Same text as above: 'joint pre-deployment testing ... was conducted by the US AI Safety Institute (US AISI) and the UK AI Safety Institute (UK AISI). We also collaborated with METR to conduct an independent assessment.' No results are given."],
    ["Constitutional Classifiers: Defending against universal jailbreaks", "https://www.anthropic.com/research/constitutional-classifiers",
     "n/a - excluded, no evaluator finding reproduced",
     "Haize Labs, Gray Swan and the UK AI Safety Institute appear only in the acknowledgements ('we are also grateful to Haize Labs, Gray Swan, and the UK AI Safety Institute for red teaming other prototype versions of our system') with no results attributed. The classifier evaluation results themselves are Anthropic's own. Note v10 already codes JOINT-2025-09-BIO1/JAI3 and UKAISI-2026-02-JAI1/JAI2 for the independently reported Constitutional Classifiers red-teaming."],
    ["Cyber evaluations of Claude 4", "https://www.anthropic.com/research/claude-4-cyber",
     "PATTERNLABS-2025-07-CYB1 (staging)",
     "The only third-party contribution is Pattern Labs' in-depth cyber-offence evaluation of Claude Opus 4 and Claude Sonnet 4, which the coordinator has already staged with the same quote."],
    ["Modifying LLM Beliefs with Synthetic Document Finetuning", "https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf",
     "n/a - excluded, no named independent evaluator",
     "Authors are Anthropic plus MATS and one Scale AI-affiliated individual (Julian Michael). No government AISI or non-developer evaluation organisation contributed findings, so the report falls outside the company-venue rule. JUDGEMENT CALL - flag if the coordinator counts a single Scale AI-affiliated co-author as an evaluator contribution."],
    ["Inverse Scaling in Test-Time Compute", "https://alignment.anthropic.com/2025/inverse-scaling",
     "n/a - excluded, no named independent evaluator",
     "Anthropic Fellows Program work with academic co-authors (Edinburgh, EPFL, UT Austin, Miniml.AI, Constellation) and one Scale-AI-affiliated individual. No evaluation organisation contributed as an evaluator, so excluded under the company-venue rule. JUDGEMENT CALL - the post does contain genuine named-model findings (Claude models distracted by irrelevant information; OpenAI o-series overfitting to problem framings; Claude Sonnet 4 showing increased self-preservation expressions with longer reasoning), so if the coordinator treats the academic collaboration as qualifying, this report is worth 3-4 rows."],
])
