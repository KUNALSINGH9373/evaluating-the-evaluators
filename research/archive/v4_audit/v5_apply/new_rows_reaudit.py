import csv
COLS = ['Finding ID', 'Report ID', 'Institution', 'Report Title', 'Publication Date', 'Domain', 'Tags', 'Models / Systems', 'Access Type', 'Source URL', 'Finding', 'Severity (C1/C2) majority', 'Sonnet5 vote', 'GPT-5.5 vote', 'Gemini3.1 vote', 'Unanimous / SPLIT', 'Severity Source', 'Action Level', 'Attribution', 'Company Response', 'Channel A Verbatim', 'Response Date', 'Lag (days)', 'Channel A Evidence', 'Sources Checked', 'Policy Level', 'Policy Response', 'Channel B Verbatim', 'Channel B Evidence', 'Traction Score', 'Media Outlets', 'Academic Citations', 'Social Highlights', 'Channel C Verbatim', 'Proportionality', 'Confidence', 'Notes', 'Key Quote', 'Traceability Tag', 'Eval? (trackable)', 'Action Trackable?', 'Finding Type', 'Scope']
def gov_row():
    r={c:'' for c in COLS}
    r['Scope']='government-AISI'; r['Eval? (trackable)']='yes'; r['Action Trackable?']='no'
    r['Access Type']='Post-deployment'
    return r
ROWS=[]

# 1. Cloud misconfigurations (HIGH - real 5-step attack chain in AISI's own infra)
r=gov_row(); r.update({
 'Finding ID':'UKAISI-2026-07-CYB1','Report ID':'UKAISI-2026-07-CLOUD','Institution':'UK AISI',
 'Report Title':'Finding Cloud Misconfigurations with Frontier AI: A Case Study','Publication Date':'2026-07-07',
 'Domain':'Cyber','Tags':'uk-aisi;cloud-misconfiguration;privilege-escalation;anonymised-model',
 'Models / Systems':'Frontier models (unnamed); "a commercially available coding agent"',
 'Source URL':'https://www.aisi.gov.uk/blog/finding-cloud-misconfigurations-with-frontier-ai-a-case-study',
 'Finding':"Frontier AI models discovered a previously unknown, non-obvious misconfiguration in the isolation of AISI's own cloud staging environment, chaining a 5-step attack to escalate privileges and access other users' workloads and data with no victim interaction required -- for under £150 in LLM tokens.",
 'Severity (C1/C2) majority':'C1','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Models are not individually named ('frontier models', 'recent LLMs') -- Trackable=no because no specific accountable company can be identified, not because the finding lacks substance. Notably this compromised AISI's OWN infrastructure, not a company's product.",
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (re-audit correction). Real, alarming finding (5-step privilege-escalation chain, since remediated) previously omitted for imprecise reasoning. Flaw has since been fixed by AISI itself.",
 'Key Quote':"a creative and non-obvious misconfiguration (now remediated) in how our environment was isolated, allowing the agent to escalate its own privileges and reach data it did not have permission to access.",
 'Traceability Tag':'anonymized-model','Finding Type':'capability-finding;anonymised-model'
}); ROWS.append(r)

# 2. Persuasion vs accuracy tradeoff
r=gov_row(); r.update({
 'Finding ID':'UKAISI-2025-07-HUM1','Report ID':'UKAISI-2025-07-PERSUADE','Institution':'UK AISI',
 'Report Title':'The Levers of Political Persuasion with Conversational AI','Publication Date':'2025-07-18',
 'Domain':'Human Influence','Tags':'uk-aisi;persuasion;accuracy-tradeoff;anonymised-model',
 'Models / Systems':'19 LLMs, including some post-trained explicitly for persuasion (unnamed)',
 'Source URL':'https://www.aisi.gov.uk/research/the-levers-of-political-persuasion-with-conversational-ai',
 'Finding':"UK AISI found post-training and prompting for persuasion substantially increased AI persuasiveness (+51% and +27% respectively), but the same techniques that increased persuasiveness also systematically decreased factual accuracy -- a direct safety-capability tradeoff.",
 'Severity (C1/C2) majority':'C1','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"19 LLMs tested but not individually named -- Trackable=no for lack of an accountable single company, not lack of substance.",
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (re-audit correction). Genuinely alarming safety-capability tradeoff finding previously omitted for imprecise reasoning.",
 'Key Quote':"where they increased AI persuasiveness they also systematically decreased factual accuracy.",
 'Traceability Tag':'anonymized-model','Finding Type':'capability-finding;anonymised-model'
}); ROWS.append(r)

# 3. Consistency training side effect
r=gov_row(); r.update({
 'Finding ID':'UKAISI-2026-06-ALI7','Report ID':'UKAISI-2026-06-CONSIST','Institution':'UK AISI',
 'Report Title':'Consistency Training Can Entrench Misalignment','Publication Date':'2026-06-02',
 'Domain':'Alignment','Tags':'uk-aisi;consistency-training;sycophancy;reward-hacking;anonymised-model',
 'Models / Systems':'Open-source models (7B-70B), 108 model organisms (unnamed)',
 'Source URL':'https://www.aisi.gov.uk/research/consistency-training-can-entrench-misalignment',
 'Finding':"UK AISI found that consistency training -- a proposed alignment technique -- generally suppresses reward hacking and emergent misalignment, but amplifies sycophancy, likely driven by distribution shift from the labeling process; a safety intervention with a documented negative side effect.",
 'Severity (C1/C2) majority':'C2','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Models anonymized (open-source 7B-70B, 108 model organisms) -- Trackable=no for lack of accountable company.",
 'Proportionality':'Proportionate (Cat2)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (re-audit correction). Real finding about a safety technique's side effect, previously omitted for imprecise reasoning.",
 'Key Quote':"consistency training generally suppresses reward hacking and emergent misalignment but amplifies sycophancy.",
 'Traceability Tag':'anonymized-model','Finding Type':'capability-finding;anonymised-model'
}); ROWS.append(r)

# 4. Alignment pretraining self-fulfilling misalignment
r=gov_row(); r.update({
 'Finding ID':'UKAISI-2026-01-ALI1','Report ID':'UKAISI-2026-01-PRETRAIN','Institution':'UK AISI',
 'Report Title':'Alignment Pretraining: AI Discourse Causes Self-Fulfilling (Mis)alignment','Publication Date':'2026-01-15',
 'Domain':'Alignment','Tags':'uk-aisi;pretraining-data;self-fulfilling;anonymised-model',
 'Models / Systems':'6.9B-parameter LLMs (unnamed)',
 'Source URL':'https://www.aisi.gov.uk/research/alignment-pretraining-ai-discourse-causes-self-fulfilling-mis-alignment',
 'Finding':"UK AISI found upsampling pretraining discourse about misaligned AI behavior raised measured misalignment to 45%, while upsampling discourse about aligned behavior cut it to 9% -- demonstrating pretraining data composition about AI itself can be self-fulfilling.",
 'Severity (C1/C2) majority':'C1','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Models anonymized (6.9B research models) -- Trackable=no for lack of accountable company.",
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (re-audit correction). Striking, alarming finding about training-data composition effects, previously omitted for imprecise reasoning.",
 'Key Quote':"Upsampling synthetic training documents about AI misalignment leads to a notable increase in misaligned behaviour. Conversely, upsampling documents about aligned behaviour reduces misalignment scores from 45% to 9%.",
 'Traceability Tag':'anonymized-model','Finding Type':'capability-finding;anonymised-model'
}); ROWS.append(r)

# 5. UL/DSRI OLMo bad health advice (named model + named accountable org: Allen Institute)
r=gov_row(); r.update({
 'Finding ID':'UL-2024-08-SOC1','Report ID':'UL-2024-08','Institution':'UL Research Institutes (DSRI)',
 'Report Title':'The Chances of Bad Advice','Publication Date':'2024-08-24','Domain':'Societal',
 'Tags':'ul-dsri;olmo;allen-institute;health-safety;non-frontier',
 'Models / Systems':'OLMo (Allen Institute for AI, 7B variants)','Access Type':'Post-deployment',
 'Source URL':'https://dsri.org/blog/chances-of-bad-advice/',
 'Finding':"DSRI found OLMo answered health-product safety questions correctly only about half the time, often giving incorrect or outdated answers -- from an independent red-teaming partnership with Allen Institute for AI (Ai2) to test OLMo before public releases.",
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Allen Institute for AI is a real, identifiable non-profit organization (not anonymized) -- Trackable coded 'no' given OLMo's non-frontier/research-model status, not lack of an identifiable party.",
 'Proportionality':'Accountability gap (no action)','Confidence':'Medium',
 'Notes':"NEW-CANDIDATE 2026-07-17 (re-audit correction). Previously dismissed as 'niche non-frontier open model' -- reconsidered: Allen Institute IS an identifiable, real organization with a formal pre-release red-teaming partnership with DSRI, so this is closer to a genuine (if lower-severity) accountability case than the anonymised-model rows above.",
 'Key Quote':"On innocuous products... OLMo will only answer correctly around half the time. It will often give an incorrect answer or no answer at all.",
 'Traceability Tag':'non-frontier','Finding Type':'capability-finding;non-frontier'
}); ROWS.append(r)

# 6. UL/DSRI OLMo secret-key exposure regression
r=gov_row(); r.update({
 'Finding ID':'UL-2024-10-CYB1','Report ID':'UL-2024-10','Institution':'UL Research Institutes (DSRI)',
 'Report Title':"A Privacy-Respecting Way to Test How Well Systems Keep Secrets",'Publication Date':'2024-10-23','Domain':'Cyber',
 'Tags':'ul-dsri;olmo;allen-institute;secret-exposure;regression;non-frontier',
 'Models / Systems':'OLMo-7b-1.7 (vs prior OLMo release, Allen Institute for AI)','Access Type':'Post-deployment',
 'Source URL':'https://dsri.org/blog/privacy-respecting-ai-systems-secrets-test/',
 'Finding':"DSRI found a more privacy-respecting training-data curation approach in OLMo-7b-1.7 actually increased phone-number exposure and exposed embedded secret API keys at nearly 4x the rate of the prior OLMo release -- a privacy fix that regressed a different security property.",
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Allen Institute for AI is identifiable; Trackable=no given non-frontier/research-model status.",
 'Proportionality':'Accountability gap (no action)','Confidence':'Medium',
 'Notes':"NEW-CANDIDATE 2026-07-17 (re-audit correction). Same reconsideration as UL-2024-08-SOC1 -- notable finding that a privacy-motivated change regressed secret-key exposure, worth capturing even for a non-frontier model given the identifiable accountable org.",
 'Key Quote':"The secret key exposure rate for the new model is nearly four times higher than the exposure rate for the old one.",
 'Traceability Tag':'non-frontier','Finding Type':'capability-finding;non-frontier'
}); ROWS.append(r)

# 7. Political knowledge reassuring finding
r=gov_row(); r.update({
 'Finding ID':'UKAISI-2025-09-GOV4','Report ID':'UKAISI-2025-09-POLKNOW','Institution':'UK AISI',
 'Report Title':"Conversational AI Increases Political Knowledge as Effectively as Self-Directed Internet Search",'Publication Date':'2025-09-08',
 'Domain':'Human Influence','Tags':'uk-aisi;political-knowledge;reassuring;anonymised-model',
 'Models / Systems':'A handful of AI chatbots (unnamed)',
 'Source URL':'https://www.aisi.gov.uk/research/conversational-ai-increases-political-knowledge-as-effectively-as-self-directed-internet-search',
 'Finding':"UK AISI found conversations with AI increase political knowledge and decrease belief in misinformation to the same extent as self-directed internet search -- a reassuring result on a domain (chatbot political influence) that could otherwise be concerning.",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (re-audit correction, added for completeness). Reassuring-null finding previously omitted.",
 'Key Quote':"conversations with AI increase political knowledge (increase belief in true information and decrease belief in misinformation) to the same extent as self-directed internet search.",
 'Traceability Tag':'anonymized-model','Eval? (trackable)':'yes','Action Trackable?':'no','Finding Type':'capability-finding;reassuring-null;anonymised-model'
}); ROWS.append(r)

# 8. More compute more capability (eval-validity methodology)
r=gov_row(); r.update({
 'Finding ID':'UKAISI-2026-07-GOV2','Report ID':'UKAISI-2026-07-COMPUTE','Institution':'UK AISI',
 'Report Title':"More Compute, More Capability: Why AI Agent Evaluations Need to Account for Test-Time Compute",'Publication Date':'2026-07-02',
 'Domain':'Eval-methodology','Tags':'uk-aisi;test-time-compute;eval-validity;methodology',
 'Models / Systems':'11-20 frontier models (unnamed, released across 2023-2026)',
 'Source URL':'https://www.aisi.gov.uk/blog/more-compute-more-capability-why-ai-agent-evals-need-to-account-for-test-time-compute',
 'Finding':"UK AISI found agent capability improves substantially with more test-time compute, with newer models gaining disproportionately -- meaning fixed-compute-budget evaluations systematically underestimate frontier capability, a methodological gap in how the field measures risk.",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (re-audit correction). Eval-integrity/methodology finding with real stakes (current evals may understate risk) previously omitted.",
 'Key Quote':"Agent capability cannot be interpreted without the compute budget used to estimate it.",
 'Traceability Tag':'methodology','Eval? (trackable)':'no','Action Trackable?':'','Finding Type':'methodology'
}); ROWS.append(r)

with open('/Users/kunalsingh/aisi-v4-audit/v5_apply/new_rows_batch4.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS); w.writeheader(); w.writerows(ROWS)
print(f"{len(ROWS)} re-audit correction rows written")
