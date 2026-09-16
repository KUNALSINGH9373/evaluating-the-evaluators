import csv
COLS = ['Finding ID', 'Report ID', 'Institution', 'Report Title', 'Publication Date', 'Domain', 'Tags', 'Models / Systems', 'Access Type', 'Source URL', 'Finding', 'Severity (C1/C2) majority', 'Sonnet5 vote', 'GPT-5.5 vote', 'Gemini3.1 vote', 'Unanimous / SPLIT', 'Severity Source', 'Action Level', 'Attribution', 'Company Response', 'Channel A Verbatim', 'Response Date', 'Lag (days)', 'Channel A Evidence', 'Sources Checked', 'Policy Level', 'Policy Response', 'Channel B Verbatim', 'Channel B Evidence', 'Traction Score', 'Media Outlets', 'Academic Citations', 'Social Highlights', 'Channel C Verbatim', 'Proportionality', 'Confidence', 'Notes', 'Key Quote', 'Traceability Tag', 'Eval? (trackable)', 'Action Trackable?', 'Finding Type', 'Scope']
def gov_row():
    return {c:'' for c in COLS}
def tp_row():
    r={c:'' for c in COLS}
    r['Scope']='third-party-evaluator'; r['Eval? (trackable)']='yes'; r['Action Trackable?']='no'
    r['Finding Type']='capability-finding'; r['Traceability Tag']='traceable'
    return r

ROWS=[]

# ============ GOVERNMENT-AISI ADDITIONS ============
r=gov_row(); r.update({
 'Finding ID':'KAISI-2026-05-GOV1','Report ID':'KAISI-2026-05','Institution':'Korea AI Safety Institute (K-AISI)',
 'Report Title':'AI 모델 42종 안전성 평가 수행 실적 공개 (42-Model Safety Evaluation Disclosure)','Publication Date':'2026-05-13',
 'Domain':'Transparency/Disclosure','Tags':'k-aisi;deepseek;gpt;claude;gemini;kimi;kanana;gauss;exaone;non-disclosure',
 'Models / Systems':'DeepSeek, GPT, Claude, Gemini, Kimi (global); Kanana, Gauss, EXAONE (domestic Korean)',
 'Access Type':'Post-deployment','Source URL':'https://www.aisi.re.kr/kor/article/ATCL75b4fb0a5/101',
 'Finding':"K-AISI disclosed it had safety-evaluated 42 AI models (29 in 2024-2025, 13 more through April 2026) across CBRN-E, cyber, data-exposure, prompt-injection, over-refusal, and agentic-misuse categories using ~60,000 evaluation scenarios -- but published only the model-name checklist, with NO pass/fail scores or per-model results disclosed, and as of this date had no MOU with OpenAI or Anthropic.",
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Director Kim Myung-joo directly quoted attributing non-disclosure to protecting 'commercial partners' competitive positions'; corroborated by DDaily (2026-05-13) noting zero independent frontier-model findings published in 1.5 years of operation.",
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (institutional deep-sweep). Same pattern as UK AISI's early undisclosed pre-deployment evaluations (Gemini Ultra, 'zero results from 16 models'). POLICY REVERSAL: a follow-up ZDNet Korea report (2026-06-19) has Kim Myung-joo committing to a new transparency policy -- 'going forward we plan to disclose as much content as possible unless the target company objects' -- and OpenAI/Anthropic MOUs were subsequently signed June 17-18, 2026.",
 'Key Quote':"앞으로는 대상 기업이 반대하지 않는 한 최대한 내용을 공개할 계획 (Going forward, we plan to disclose as much content as possible unless the target company objects)",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'yes','Finding Type':'capability-finding','Scope':'government-AISI'
}); ROWS.append(r)

r=gov_row(); r.update({
 'Finding ID':'AUAISI-2026-07-GOV1','Report ID':'AUAISI-2026-07','Institution':'Australia AI Safety Institute',
 'Report Title':"Australia's AI Safety Institute begins testing frontier models (no findings published)",'Publication Date':'2026-07-07',
 'Domain':'Transparency/Disclosure','Tags':'australia-aisi;non-disclosure;institutional',
 'Models / Systems':'','Access Type':'Post-deployment','Source URL':'https://cryptobriefing.com/australia-ai-safety-institute-testing-crypto-implications/',
 'Finding':"Australia's AI Safety Institute (established Nov 2025, A$29.9M/4yr) began testing frontier models on 2026-07-07 but had published zero results as of that date; a follow-up ministerial speech (2026-07-08) at the AI Safety Forum discussed AI risks by recycling Anthropic's own prior public disclosures (blackmail, chess-hacking examples) rather than presenting new AISI findings.",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Same transparency-gap pattern as K-AISI and UK AISI's early history. Independent academic commentary (The Conversation, 2026-07-09) separately confirms no specific published results exist yet and critiques the budget as insufficient.",
 'Key Quote':"committed to publicly disseminating its evaluations... but these findings had not yet been released.",
 'Traceability Tag':'too-recent','Eval? (trackable)':'no','Action Trackable?':'','Finding Type':'governance','Scope':'government-AISI'
}); ROWS.append(r)

r=gov_row(); r.update({
 'Finding ID':'UKAISI-2026-05-CYB4','Report ID':'RAND-2026-05','Institution':'RAND (commissioned by UK AISI)',
 'Report Title':'Investigating the potential use of frontier AI models for offensive cyberattacks: A human uplift study','Publication Date':'2026-05-28',
 'Domain':'Cyber','Tags':'rand;o3;gpt-5;claude-opus-4.1;claude-sonnet-3.7;gemini-2.5-pro;cyber-uplift;rct',
 'Models / Systems':'OpenAI o3, GPT-5, Claude Opus 4.1, Claude Sonnet 3.7, Gemini 2.5 Pro','Access Type':'Post-deployment',
 'Source URL':'https://www.rand.org/pubs/research_reports/RRA3892-1.html',
 'Finding':"In a UK-AISI-commissioned randomized controlled trial (157 participants), RAND found generally statistically insignificant AI uplift for completing full end-to-end offensive cyberattack chains across five frontier models, though novice participants completed tasks faster with AI access.",
 'Severity (C1/C2) majority':'C2','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (AI Evaluator Forum sweep). Government-commissioned third-party research (UK AISI funded RAND to run this RCT) -- coded government-AISI scope, not pure third-party, since UK AISI is the commissioning body. Reassuring-null result across all 5 models tested.",
 'Key Quote':"Our study finds generally statistically insignificant uplift estimates, across our skill tiers, for successful completions of our three end-to-end attack chains.",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'no','Finding Type':'capability-finding;reassuring-null','Scope':'government-AISI'
}); ROWS.append(r)

with open('/Users/kunalsingh/aisi-v4-audit/v5_apply/new_rows_batch2.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS); w.writeheader(); w.writerows(ROWS)
print(f"Government-AISI additions: {len(ROWS)} rows")
