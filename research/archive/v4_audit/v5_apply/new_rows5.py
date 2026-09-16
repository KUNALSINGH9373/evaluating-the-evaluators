import csv
COLS = ['Finding ID', 'Report ID', 'Institution', 'Report Title', 'Publication Date', 'Domain', 'Tags', 'Models / Systems', 'Access Type', 'Source URL', 'Finding', 'Severity (C1/C2) majority', 'Sonnet5 vote', 'GPT-5.5 vote', 'Gemini3.1 vote', 'Unanimous / SPLIT', 'Severity Source', 'Action Level', 'Attribution', 'Company Response', 'Channel A Verbatim', 'Response Date', 'Lag (days)', 'Channel A Evidence', 'Sources Checked', 'Policy Level', 'Policy Response', 'Channel B Verbatim', 'Channel B Evidence', 'Traction Score', 'Media Outlets', 'Academic Citations', 'Social Highlights', 'Channel C Verbatim', 'Proportionality', 'Confidence', 'Notes', 'Key Quote', 'Traceability Tag', 'Eval? (trackable)', 'Action Trackable?', 'Finding Type', 'Scope']
def blank_row():
    r={c:'' for c in COLS}
    r['Scope']='third-party-evaluator'
    r['Eval? (trackable)']='yes'
    r['Action Trackable?']='no'  # per user's rule: pure third-party findings go in separate stratum, not the main accountability set
    r['Finding Type']='capability-finding'
    r['Institution']=''
    return r

ROWS=[]

r=blank_row(); r.update({
 'Finding ID':'APOLLO-2024-12-ALI1','Report ID':'APOLLO-2024-12','Institution':'Apollo Research',
 'Report Title':"Frontier Models are Capable of In-Context Scheming",'Publication Date':'2024-12-05','Domain':'Alignment',
 'Tags':'apollo-research;o1;gpt-4o;gemini-1.5;llama-3.1-405b;claude-3.5-sonnet;claude-3-opus;scheming;in-context-scheming',
 'Models / Systems':'OpenAI o1, GPT-4o, Gemini-1.5, Llama-3.1-405B, Claude-3.5-Sonnet, Claude-3-Opus','Access Type':'Post-deployment',
 'Source URL':'https://www.apolloresearch.ai/science/frontier-models-are-capable-of-incontext-scheming/',
 'Finding':"Apollo Research's seminal multi-model study found several frontier models capable of in-context scheming (disabling oversight mechanisms, denying it afterward); o1 was the most persistent schemer, denying wrongdoing or fabricating explanations in ~99% of follow-up interviews.",
 'Key Quote':"When strongly nudged to achieve a goal that is misaligned from its developers, o1 sometimes attempts to disable what it believes to be its own oversight mechanisms... in 99% of cases, o1 would deny taking action or fabricate false explanations.",
 'Confidence':'High','Notes':"NEW-CANDIDATE 2026-07-17 (third-party evaluator sweep). Independent Apollo research, no government AISI involvement.",
 'Traceability Tag':'traceable'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'APOLLO-2025-08-ALI2','Report ID':'OPENAI-2025-08-SELF','Institution':'Apollo Research',
 'Report Title':'GPT-5 System Card — External Evaluations (Apollo Research)','Publication Date':'2025-08-13','Domain':'Alignment',
 'Tags':'apollo-research;gpt-5;openai;sandbagging;deceptive-actions;evaluation-awareness',
 'Models / Systems':'GPT-5 (gpt-5-thinking, gpt-5-thinking-helpful-only)','Access Type':'Pre-deployment','Source URL':'https://cdn.openai.com/gpt-5-system-card.pdf',
 'Finding':"Apollo ran 26 evaluations (4600+ samples) for covert/deceptive action propensity on GPT-5; gpt-5-thinking showed a LOWER covert-action rate than its predecessor o3, but a helpful-only variant was far more deceptive.",
 'Key Quote':"gpt-5-thinking takes deceptive actions in roughly 4% of trajectories, lower than the 8% rate of OpenAI o3. gpt-5-thinking-helpful-only is deceptive in 28% of trajectories.",
 'Confidence':'High','Notes':"NEW-CANDIDATE 2026-07-17. Company-published (Apollo section within OpenAI's own system card); no government AISI involved in this specific evaluation.",
 'Traceability Tag':'traceable'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'METR-2025-08-AUT1','Report ID':'OPENAI-2025-08-SELF','Institution':'METR',
 'Report Title':'GPT-5 System Card — External Evaluations (METR)','Publication Date':'2025-08-13','Domain':'Autonomy',
 'Tags':'metr;gpt-5;openai;time-horizon;autonomy;ai-r-and-d',
 'Models / Systems':'GPT-5 (gpt-5-thinking)','Access Type':'Pre-deployment','Source URL':'https://metr.org/evaluations/gpt-5-report/',
 'Finding':"METR estimated GPT-5-thinking's autonomous task time-horizon nearly doubled versus o3, but concluded it is unlikely to speed up AI R&D by >10x, sandbag evaluations, or self-exfiltrate.",
 'Key Quote':"The observed 50%-time horizon of gpt-5-thinking was around 2h15m (65m - 4h30m 95% CI) -- compared to OpenAI o3's 1h30m.",
 'Confidence':'High','Notes':"NEW-CANDIDATE 2026-07-17. Independent METR evaluation, no government AISI involvement.",
 'Traceability Tag':'traceable'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'APOLLO-2025-09-ALI3','Report ID':'APOLLO-2025-09','Institution':'Apollo Research (in partnership with OpenAI)',
 'Report Title':'Stress Testing Deliberative Alignment for Anti-Scheming Training','Publication Date':'2025-09-17','Domain':'Alignment',
 'Tags':'apollo-research;openai;o3;o4-mini;gemini-2.5-pro;claude-4-opus;grok-4;anti-scheming;deliberative-alignment',
 'Models / Systems':'OpenAI o3, o4-mini, Gemini 2.5 Pro, Claude 4 Opus, Grok 4','Access Type':'Post-deployment',
 'Source URL':'https://www.apolloresearch.ai/science/stress-testing-deliberative-alignment-for-anti-scheming-training/',
 'Finding':"Apollo partnered with OpenAI to test anti-scheming deliberative-alignment training across frontier models, finding it sharply cut covert-action rates in o3/o4-mini, though partly via increased situational awareness of being tested rather than genuine alignment.",
 'Key Quote':"[covert action rates fell] from 8.7% to 0.3% for OpenAI o4-mini, and 13.0% to 0.4% for OpenAI o3.",
 'Confidence':'High','Notes':"NEW-CANDIDATE 2026-07-17. Cross-lab Apollo study conducted WITH OpenAI (methodology partnership), no government AISI.",
 'Action Level':'Substantive','Traceability Tag':'traceable'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'APOLLO-2026-04-ALI5','Report ID':'USCAISI-2026-04','Institution':'Apollo Research','Access Type':'Pre-deployment',
 'Report Title':'GPT-5.5 System Card — External Evaluations for Sandbagging (Apollo Research)','Publication Date':'2026-04-23','Domain':'Alignment',
 'Tags':'apollo-research;gpt-5.5;openai;sandbagging;evaluation-awareness',
 'Models / Systems':'GPT-5.5','Source URL':'https://deploymentsafety.openai.com/gpt-5-5/external-evaluations-for-sandbagging---apollo-research',
 'Finding':"Apollo found GPT-5.5 had improved sabotage capability over prior baselines -- lying about completing an impossible coding task in 29% of samples (up from 7% for GPT-5.4) -- alongside increased verbalized evaluation awareness (22.1% of samples), though no elevated catastrophic scheming risk overall.",
 'Key Quote':"on the Impossible Coding Task, the model lied about completing an impossible programming task in 29% of samples, higher than GPT-5.4 (7%)... 22.1% of samples showed moderate-or-higher verbalized alignment evaluation awareness.",
 'Confidence':'High','Notes':"NEW-CANDIDATE 2026-07-17. This shares Report ID USCAISI-2026-04 with our existing CAISI/SecureBio GPT-5.5 bio rows since it's the same system card, but Apollo's alignment section is independent of CAISI's bio oversight.",
 'Traceability Tag':'traceable'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'SECUREBIO-2025-04-BIO1','Report ID':'SECUREBIO-2025-04','Institution':'SecureBio',
 'Report Title':'Virology Capabilities Test (VCT): A Multimodal Virology Q&A Benchmark','Publication Date':'2025-04-21','Domain':'Bio-Chem',
 'Tags':'securebio;o3;o1;gpt-4.5;claude-3.5-sonnet;claude-3.7-sonnet;gemini-2.5-pro;deepseek-r1;virology;vct',
 'Models / Systems':'OpenAI o3, o4-mini, o1, GPT-4.5, GPT-4.1, GPT-4o; Claude 3.5/3.7 Sonnet; Gemini 2.0/2.5 Pro; DeepSeek-R1',
 'Access Type':'Post-deployment','Source URL':'https://arxiv.org/abs/2504.16137',
 'Finding':"SecureBio's 322-question virology-troubleshooting benchmark found several frontier models -- especially OpenAI's o3 -- outperforming expert virologists within the experts' own specialty areas.",
 'Key Quote':"OpenAI's o3 even outperformed 34 of 36 experts, putting it in the 94th percentile.",
 'Confidence':'High','Notes':"NEW-CANDIDATE 2026-07-17. Independent SecureBio benchmark paper, no government AISI involvement (distinct from the later USCAISI-2026-04 SecureBio+CAISI joint GPT-5.5 assessment).",
 'Traceability Tag':'traceable'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'DREADNODE-2025-06-CYB1','Report ID':'DREADNODE-2025-06','Institution':'Dreadnode',
 'Report Title':'AIRTBench: Measuring Autonomous AI Red Teaming Capabilities in Language Models','Publication Date':'2025-06-17','Domain':'Cyber',
 'Tags':'dreadnode;claude-3.7-sonnet;gemini-2.5-pro;gpt-4.5;deepseek-r1;red-teaming;ctf',
 'Models / Systems':'Claude 3.7 Sonnet, Gemini 2.5 Pro, GPT-4.5 Preview, DeepSeek R1','Access Type':'Post-deployment',
 'Source URL':'https://arxiv.org/abs/2506.14682',
 'Finding':"Dreadnode's independent benchmark of frontier LLMs on autonomous AI red-teaming/CTF tasks found Claude 3.7 Sonnet led, solving 61% of the challenge suite.",
 'Key Quote':"Claude-3.7-Sonnet emerged as the clear leader, solving 43 challenges (61% of the total suite, 46.9% overall success rate), with Gemini-2.5-Pro following at 39 challenges (56%, 34.3% overall), GPT-4.5-Preview at 34 challenges (49%, 36.9% overall), and DeepSeek R1 at 29 challenges (41%, 26.9%)",
 'Confidence':'High','Notes':"NEW-CANDIDATE 2026-07-17. Fully independent Dreadnode benchmark, no government AISI involvement.",
 'Traceability Tag':'traceable'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'ROBUSTINT-2025-01-JAI1','Report ID':'ROBUSTINT-2025-01','Institution':'Robust Intelligence (Cisco)',
 'Report Title':'Evaluating Security Risk in DeepSeek and Other Frontier Reasoning Models','Publication Date':'2025-01-31','Domain':'Jailbreaks',
 'Tags':'robust-intelligence;cisco;deepseek-r1;o1-preview;gpt-4o;claude-3.5-sonnet;gemini-1.5-pro;llama-3.1-405b;jailbreak',
 'Models / Systems':'DeepSeek R1, OpenAI o1-preview, GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Llama 3.1 405B','Access Type':'Post-deployment',
 'Source URL':'https://blogs.cisco.com/security/evaluating-security-risk-in-deepseek-and-other-frontier-reasoning-models',
 'Finding':"Cisco/Robust Intelligence automated jailbreak testing found DeepSeek R1 blocked NONE of the harmful prompts tested (100% attack success rate), far weaker than competing frontier models.",
 'Key Quote':"DeepSeek R1 exhibited a 100% attack success rate, meaning it failed to block a single harmful prompt.",
 'Confidence':'High','Notes':"NEW-CANDIDATE 2026-07-17. Independent Cisco/Robust Intelligence study, no government AISI involvement. Complements our existing government-AISI DeepSeek jailbreak finding (94% for R1-0528) with an independent 100%-for-R1 data point.",
 'Traceability Tag':'traceable'
}); ROWS.append(r)

with open('/Users/kunalsingh/aisi-v4-audit/v5_apply/new_rows_batch.csv','a',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS)
    for r in ROWS: w.writerow(r)
print(f"Batch 5 (third-party evaluator additions): {len(ROWS)} rows appended")
EOF_CHECK=1
