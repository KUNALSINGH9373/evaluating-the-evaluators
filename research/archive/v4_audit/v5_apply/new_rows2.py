import csv
COLS = ['Finding ID', 'Report ID', 'Institution', 'Report Title', 'Publication Date', 'Domain', 'Tags', 'Models / Systems', 'Access Type', 'Source URL', 'Finding', 'Severity (C1/C2) majority', 'Sonnet5 vote', 'GPT-5.5 vote', 'Gemini3.1 vote', 'Unanimous / SPLIT', 'Severity Source', 'Action Level', 'Attribution', 'Company Response', 'Channel A Verbatim', 'Response Date', 'Lag (days)', 'Channel A Evidence', 'Sources Checked', 'Policy Level', 'Policy Response', 'Channel B Verbatim', 'Channel B Evidence', 'Traction Score', 'Media Outlets', 'Academic Citations', 'Social Highlights', 'Channel C Verbatim', 'Proportionality', 'Confidence', 'Notes', 'Key Quote', 'Traceability Tag', 'Eval? (trackable)', 'Action Trackable?', 'Finding Type', 'Scope']
def blank_row():
    return {c:'' for c in COLS}
ROWS=[]

# ============ Claude Opus 4.6 (2026-02-05) ============
O46_SRC='https://www.anthropic.com/claude-opus-4-6-system-card'
r=blank_row(); r.update({
 'Finding ID':'USCAISI-2026-02-BIO1','Report ID':'ANTHROPIC-2026-02-SELF','Institution':'US CAISI',
 'Report Title':'Claude Opus 4.6 System Card','Publication Date':'2026-02-05','Domain':'Bio-Chem;Transparency/Disclosure',
 'Tags':'claude-opus-4.6;anthropic;caisi;bio-chem;asl-4;no-disclosed-result',
 'Models / Systems':'Claude Opus 4.6','Access Type':'Pre-deployment','Source URL':O46_SRC,
 'Finding':"CAISI (US Center for AI Standards and Innovation) red-teamed Claude Opus 4.6's biological-protocol capabilities over a one-week window, assessing whether the model can suggest accurate protocols and propose actionable ideas for biology experts in a national security context -- no specific quantitative result is disclosed in the card.",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Process/acknowledgement statement only, no disclosed result -> governance/transparency row, not an accountability finding (same pattern as the Claude 3.7 Sonnet and Opus 4 base-card joint-eval rows).",
 'Key Quote':"CAISI assessed the extent to which the model can suggest accurate protocols and propose actionable ideas for biology experts in a national security context.",
 'Traceability Tag':'too-recent','Eval? (trackable)':'no','Action Trackable?':'','Finding Type':'governance','Scope':'government-AISI'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'USCAISI-2026-02-CYB1','Report ID':'ANTHROPIC-2026-02-SELF','Institution':'US CAISI',
 'Report Title':'Claude Opus 4.6 System Card','Publication Date':'2026-02-05','Domain':'Cyber',
 'Tags':'claude-opus-4.6;anthropic;caisi;cyber;vulnerability-disclosure;third-party-software',
 'Models / Systems':'Claude Opus 4.6','Access Type':'Pre-deployment','Source URL':O46_SRC,
 'Finding':"CAISI red-teamed Claude Opus 4.6's cyber capabilities over a one-week window (tens of millions of tokens, multi-day probing), discovering novel vulnerabilities in open- and closed-source software that CAISI will responsibly disclose to the impacted (third-party) maintainers -- this is not an Anthropic product/infrastructure issue.",
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Card explicitly frames disclosure as CAISI's responsibility to third-party software maintainers, not Anthropic; no Anthropic-side remediation is documented or applicable.",
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Unusual case: the accountable party for the discovered vulnerabilities is unnamed third-party software maintainers, not Anthropic -- coded as an accountability gap on the anonymous-target axis rather than an Anthropic-attributable one; flagged for a scope decision (does 'no company response expected of Anthropic, since the vulnerability isn't theirs' belong in the headline denominator?).",
 'Key Quote':"a number of novel vulnerabilities in both open and closed source software were discovered that CAISI will be responsibly disclosing to impacted maintainers.",
 'Traceability Tag':'anonymized-model','Eval? (trackable)':'yes','Action Trackable?':'no','Finding Type':'capability-finding;anonymised-model','Scope':'government-AISI'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'UKAISI-2026-02-ALI4','Report ID':'ANTHROPIC-2026-02-SELF','Institution':'UK AISI',
 'Report Title':'Claude Opus 4.6 System Card','Publication Date':'2026-02-05','Domain':'Alignment',
 'Tags':'claude-opus-4.6;anthropic;sabotage;reassuring-null;access-inequality',
 'Models / Systems':'Claude Opus 4.6 (early snapshot)','Access Type':'Pre-deployment','Source URL':O46_SRC,
 'Finding':"UK AISI tested an early Opus 4.6 snapshot for AI-safety-research-sabotage propensity over only 3 working days (versus the full one-week window CAISI received for bio/cyber) and found no instances of research sabotage.",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Reassuring-null result. Also documents an access-inequality worth flagging in the paper: UK AISI's window (3 days) was markedly shorter than CAISI's (7 days) in the same card.",
 'Key Quote':"We find no instances of research sabotage from [Opus 4.6] on our task suite.",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'no','Finding Type':'capability-finding;reassuring-null','Scope':'government-AISI'
}); ROWS.append(r)

# ============ Claude Opus 4.7 (2026-04-16) ============
O47_SRC='https://www.anthropic.com/claude-opus-4-7-system-card'
r=blank_row(); r.update({
 'Finding ID':'UKAISI-2026-04-CYB12','Report ID':'ANTHROPIC-2026-04-SELF','Institution':'UK AISI',
 'Report Title':'Claude Opus 4.7 System Card','Publication Date':'2026-04-16','Domain':'Cyber',
 'Tags':'claude-opus-4.7;anthropic;cyber-range;reassuring-null;mythos-preview',
 'Models / Systems':'Claude Opus 4.7','Access Type':'Pre-deployment','Source URL':O47_SRC,
 'Finding':"UK AISI's cyber-range testing found Claude Opus 4.7 unable to fully solve the corporate-network attack simulation that Claude Mythos Preview solved in 3 of 10 tries (Opus 4.6 completed more steps than 4.7 but also did not solve it).",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Reassuring/comparative result -- Opus 4.7 is LESS cyber-capable on this range than Mythos Preview, not a new threshold.",
 'Key Quote':"Opus 4.7 was unable to fully solve the cyber range. Mythos Preview was able to solve the same range in 3 out of 10 tries.",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'no','Finding Type':'capability-finding;reassuring-null','Scope':'government-AISI'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'UKAISI-2026-04-ALI7','Report ID':'ANTHROPIC-2026-04-SELF','Institution':'UK AISI',
 'Report Title':'Claude Opus 4.7 System Card','Publication Date':'2026-04-16','Domain':'Alignment',
 'Tags':'claude-opus-4.7;anthropic;over-refusal;safety-research;model-comparison',
 'Models / Systems':'Claude Opus 4.7','Access Type':'Pre-deployment','Source URL':O47_SRC,
 'Finding':"UK AISI found Claude Opus 4.7 partially refuses AI-safety-research tasks 13.7% of the time (0% full refusals) -- the lowest full-refusal rate of the compared Claude models (vs 33%/0.7% Mythos Preview, 6.3%/2.2% Opus 4.6, 22.2%/10.7% Sonnet 4.6).",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Cross-model over-refusal comparison, same nature as the earlier over-refusal cluster (rows 6-8) coded methodology/side-observation, not a company-actionable finding.",
 'Key Quote':"Opus 4.7 does partially refuse to assist with AI safety research tasks 13.7% of the time (with 0% full refusals).",
 'Traceability Tag':'methodology','Eval? (trackable)':'yes','Action Trackable?':'no','Finding Type':'methodology','Scope':'government-AISI'
}); ROWS.append(r)

# ============ Claude Opus 4.8 (2026-05-28) ============
O48_SRC='https://www.anthropic.com/claude-opus-4-8-system-card'
r=blank_row(); r.update({
 'Finding ID':'UKAISI-2026-05-ALI3','Report ID':'ANTHROPIC-2026-05-SELF','Institution':'UK AISI',
 'Report Title':'Claude Opus 4.8 System Card','Publication Date':'2026-05-28','Domain':'Alignment',
 'Tags':'claude-opus-4.8;anthropic;sabotage;reassuring-null;evaluation-awareness',
 'Models / Systems':'Claude Opus 4.8 (early checkpoint)','Access Type':'Pre-deployment','Source URL':O48_SRC,
 'Finding':"UK AISI tested an early Opus 4.8 checkpoint for safety-research-sabotage propensity, finding no instances of spontaneous compromise (partial refusals 14.1%, near-zero full refusals) and that the model distinguishes synthetic task reproductions from real deployment data at 79% accuracy (comparable to Mythos Preview, above Opus 4.7's 68%).",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'Medium',
 'Notes':"NEW-CANDIDATE 2026-07-17. Reassuring-null. Note: source is the standalone system-card PDF (anthropic.com/claude-opus-4-8-system-card), not the news announcement page; the 79% figure specifically concerns distinguishing synthetic-vs-real deployment data, not eval-vs-deployment as an earlier draft summary conflated -- corrected per verification pass.",
 'Key Quote':"There were no instances of spontaneous compromise of AI safety research.",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'no','Finding Type':'capability-finding;reassuring-null','Scope':'government-AISI'
}); ROWS.append(r)

with open('/Users/kunalsingh/aisi-v4-audit/v5_apply/new_rows_batch.csv','a',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS)
    for r in ROWS: w.writerow(r)
print(f"Batch 2 (Opus 4.6/4.7/4.8): {len(ROWS)} rows appended")
