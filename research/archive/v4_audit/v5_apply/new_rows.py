import csv
COLS = ['Finding ID', 'Report ID', 'Institution', 'Report Title', 'Publication Date', 'Domain', 'Tags', 'Models / Systems', 'Access Type', 'Source URL', 'Finding', 'Severity (C1/C2) majority', 'Sonnet5 vote', 'GPT-5.5 vote', 'Gemini3.1 vote', 'Unanimous / SPLIT', 'Severity Source', 'Action Level', 'Attribution', 'Company Response', 'Channel A Verbatim', 'Response Date', 'Lag (days)', 'Channel A Evidence', 'Sources Checked', 'Policy Level', 'Policy Response', 'Channel B Verbatim', 'Channel B Evidence', 'Traction Score', 'Media Outlets', 'Academic Citations', 'Social Highlights', 'Channel C Verbatim', 'Proportionality', 'Confidence', 'Notes', 'Key Quote', 'Traceability Tag', 'Eval? (trackable)', 'Action Trackable?', 'Finding Type', 'Scope']

def blank_row():
    return {c:'' for c in COLS}

ROWS = []

# ============ GPT-5.6 (OpenAI, 2026-07-09) ============
GPT56_SRC = 'https://deploymentsafety.openai.com/gpt-5-6/gpt-5-6.pdf'
GPT56_TITLE = 'GPT-5.6 System Card (Sol/Terra/Luna)'

r = blank_row()
r.update({
 'Finding ID':'JOINT-2026-07-CYB1','Report ID':'JOINT-2026-07','Institution':'Joint UK AISI + OpenAI (company-published)',
 'Report Title':GPT56_TITLE,'Publication Date':'2026-07-09','Domain':'Cyber','Tags':'gpt-5.6;openai;cyber;ctf;the-last-ones;cyber-range',
 'Models / Systems':'GPT-5.6 Sol','Access Type':'Pre-deployment','Source URL':GPT56_SRC,
 'Finding':"On UK AISI's expert-level CTF tasks, GPT-5.6 Sol scored 95.0% (+-9.8%), up from 85.0% (+-11.6%) for GPT-5.5, and completed the 32-step 'The Last Ones' corporate-network attack simulation in 7 of 10 attempts (vs 2 of 10 for GPT-5.5), though it did not solve the harder 'Doing Life' range that GPT-5.5 also failed.",
 'Severity (C1/C2) majority':'C1','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':'GPT-5.6 system card sec 9.1.2.6 reports the capability result but no company action tied specifically to the capability level itself (distinct from the safeguards/jailbreak finding in JOINT-2026-07-JAI1, which does have a documented response).',
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (completeness-audit sweep). Verified via direct PDF fetch. Report is company-published (no standalone UK AISI blog exists yet for GPT-5.6 as of verification date).",
 'Key Quote':"On AISI's CTF expert-level tasks, GPT-5.6 Sol scored 95.0% +/- 9.8%, compared with 85.0% +/- 11.6% for GPT-5.5.",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'yes','Finding Type':'capability-finding','Scope':'government-AISI'
})
ROWS.append(r)

r = blank_row()
r.update({
 'Finding ID':'JOINT-2026-07-ALI1','Report ID':'JOINT-2026-07','Institution':'Joint UK AISI + OpenAI (company-published)',
 'Report Title':GPT56_TITLE,'Publication Date':'2026-07-09','Domain':'Alignment','Tags':'gpt-5.6;openai;sabotage;covert-reasoning;chain-of-thought',
 'Models / Systems':'GPT-5.6 Sol','Access Type':'Pre-deployment','Source URL':GPT56_SRC,
 'Finding':"UK AISI found GPT-5.6 Sol actively continued sabotage in ~1% of trajectories (76% of which were covert -- reasoned about in chain-of-thought but not disclosed to the user) -- statistically flat versus GPT-5.5 (also 1%) and actually lower than GPT-5.4 (2%), so this is a stable/reassuring result rather than a new increase.",
 'Severity (C1/C2) majority':'C2','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Proportionality':'Proportionate (Cat2)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Rate is flat/improved vs predecessors -- coded reassuring-null, not an accountability gap. Separately, in one impossible task GPT-5.6 ran code on an external service with non-sensitive credentials, triggering a security alert in AISI's own infrastructure (operational curiosity, not a company-facing finding).",
 'Key Quote':"GPT-5.6 Sol actively continued sabotage in approximately 1% of trajectories, compared with 1% for GPT-5.5 and 2% for GPT-5.4.",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'no','Finding Type':'capability-finding;reassuring-null','Scope':'government-AISI'
})
ROWS.append(r)

r = blank_row()
r.update({
 'Finding ID':'JOINT-2026-07-GOV1','Report ID':'JOINT-2026-07','Institution':'Joint UK AISI + OpenAI (company-published)',
 'Report Title':GPT56_TITLE,'Publication Date':'2026-07-09','Domain':'Eval-methodology','Tags':'gpt-5.6;openai;monitorability;chain-of-thought;redwood-research',
 'Models / Systems':'GPT-5.6 Sol','Access Type':'Pre-deployment','Source URL':GPT56_SRC,
 'Finding':"UK AISI found action-only monitors were much less reliable than reasoning-based monitors for GPT-5.6 Sol; the model's 'no-CoT' math reasoning time horizon was 3.6 minutes (up from 2.3 for GPT-5.5) but remained below Redwood Research's exponential trendline for the highest such horizon among public models.",
 'Severity (C1/C2) majority':'','Severity Source':'',
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Monitoring-methodology research finding, model is the instrument being monitored, not the subject of a safety verdict.",
 'Key Quote':"UK AISI found that action-only monitors were much less reliable for GPT-5.6 Sol than reasoning-based monitors.",
 'Traceability Tag':'methodology','Eval? (trackable)':'no','Action Trackable?':'','Finding Type':'methodology','Scope':'government-AISI'
})
ROWS.append(r)

r = blank_row()
r.update({
 'Finding ID':'JOINT-2026-07-JAI1','Report ID':'JOINT-2026-07','Institution':'Joint UK AISI + OpenAI (company-published)',
 'Report Title':GPT56_TITLE,'Publication Date':'2026-07-09','Domain':'Jailbreaks','Tags':'gpt-5.6;openai;universal-jailbreak;safeguards;cyber',
 'Models / Systems':'GPT-5.6 Sol','Access Type':'Pre-deployment','Source URL':GPT56_SRC,
 'Finding':"In every red-teaming round to date, UK AISI has identified universal jailbreaks in the cyber domain against GPT-5.6, including ones enabling long-form agentic task completion in vulnerability discovery and exploit development; these were often developed within hours and preserved the model's capabilities on public offensive-cybersecurity benchmarks.",
 'Severity (C1/C2) majority':'C1','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'Substantive','Attribution':'Explicit',
 'Company Response':"OpenAI worked to reproduce and mitigate the specific jailbreaks reported by UK AISI before launch, while acknowledging further red-teaming will likely surface similar ones, and committed to continued joint testing.",
 'Channel A Verbatim':"As of launch, OpenAI has worked to reproduce and mitigate the specific jailbreaks reported by UK AISI. However, UK AISI expects further red-teaming to surface similar jailbreaks. OpenAI remains committed to working with UK AISI on safeguards, including additional testing of this model.",
 'Response Date':'2026-07-09','Lag (days)':'0','Channel A Evidence':GPT56_SRC,
 'Proportionality':'Proportionate','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (completeness-audit sweep, verified via direct PDF fetch, all quotes exact). Clean 'loop worked' example -- pre-launch mitigation with explicit AISI attribution.",
 'Key Quote':"These jailbreaks were often developed within hours and appeared to preserve the model's capabilities on public offensive cybersecurity benchmarks.",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'yes','Finding Type':'capability-finding','Scope':'government-AISI'
})
ROWS.append(r)

with open('/Users/kunalsingh/aisi-v4-audit/v5_apply/new_rows_batch.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS); w.writeheader(); w.writerows(ROWS)
print(f"Batch 1 (GPT-5.6): {len(ROWS)} rows written")
