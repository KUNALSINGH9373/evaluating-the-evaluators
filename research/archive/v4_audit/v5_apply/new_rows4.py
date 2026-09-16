import csv
COLS = ['Finding ID', 'Report ID', 'Institution', 'Report Title', 'Publication Date', 'Domain', 'Tags', 'Models / Systems', 'Access Type', 'Source URL', 'Finding', 'Severity (C1/C2) majority', 'Sonnet5 vote', 'GPT-5.5 vote', 'Gemini3.1 vote', 'Unanimous / SPLIT', 'Severity Source', 'Action Level', 'Attribution', 'Company Response', 'Channel A Verbatim', 'Response Date', 'Lag (days)', 'Channel A Evidence', 'Sources Checked', 'Policy Level', 'Policy Response', 'Channel B Verbatim', 'Channel B Evidence', 'Traction Score', 'Media Outlets', 'Academic Citations', 'Social Highlights', 'Channel C Verbatim', 'Proportionality', 'Confidence', 'Notes', 'Key Quote', 'Traceability Tag', 'Eval? (trackable)', 'Action Trackable?', 'Finding Type', 'Scope']
def blank_row():
    return {c:'' for c in COLS}
ROWS=[]

# o3/o4-mini domain-assignment (governance/transparency - process only, no result)
r=blank_row(); r.update({
 'Finding ID':'JOINT-2025-04-GOV2','Report ID':'OPENAI-2025-04-SELF','Institution':'Joint US AISI + UK AISI',
 'Report Title':'o3 and o4-mini System Card','Publication Date':'2025-04-16','Domain':'Transparency/Disclosure',
 'Tags':'o3;o4-mini;openai;pre-deployment;domain-assignment',
 'Models / Systems':'OpenAI o3, o4-mini','Access Type':'Pre-deployment','Source URL':'https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf',
 'Finding':"OpenAI granted early access to o3 and o4-mini to the US AI Safety Institute (cyber and biological capability domains) and the UK AI Security Institute (cyber, chemical/biological, autonomy, and an early safeguards version) -- no specific quantitative results are attributed to either institute in the card itself.",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Process/transparency statement only (pre-CAISI-rename era, uses 'U.S. AI Safety Institute'); notable for specifying DIFFERENT domain splits between the two institutes.",
 'Key Quote':"OpenAI granted early access to these versions of o3 and o4-mini to the U.S. AI Safety Institute to conduct evaluations of the models' cyber and biological capabilities, and to the U.K. AI Security Institute to conduct evaluations of cyber, chemical and biological, and autonomy capabilities, and an early version of the safeguards.",
 'Traceability Tag':'too-recent','Eval? (trackable)':'no','Action Trackable?':'','Finding Type':'governance','Scope':'government-AISI'
}); ROWS.append(r)

# Claude 3.7 Sonnet joint eval (governance, no disclosed result)
r=blank_row(); r.update({
 'Finding ID':'JOINT-2025-02-GOV2','Report ID':'ANTHROPIC-2025-02-SELF','Institution':'Joint US AISI + UK AISI',
 'Report Title':'Claude 3.7 Sonnet System Card','Publication Date':'2025-02-24','Domain':'Transparency/Disclosure',
 'Tags':'claude-3.7-sonnet;anthropic;pre-deployment;asl-determination;no-disclosed-result',
 'Models / Systems':'Claude 3.7 Sonnet','Access Type':'Pre-deployment','Source URL':'https://www.anthropic.com/claude-3-7-sonnet-system-card',
 'Finding':"Under voluntary MOUs, the US AI Safety Institute and UK AI Security Institute conducted pre-deployment testing of Claude 3.7 Sonnet across Anthropic's RSP-framework domains, informing Anthropic's ASL determination; the capabilities report was also shared with METR for feedback -- no specific result is disclosed in the card.",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Process/transparency statement only, no disclosed result -> governance row, matching the pattern for undisclosed pre-deployment evals elsewhere in the sheet.",
 'Key Quote':"Under our voluntary Memorandums of Understanding, the U.S. AI Safety Institute (U.S. AISI) and U.K. AI Security Institute (U.K. AISI) conducted pre-deployment testing of Claude 3.7 Sonnet across the domains outlined in our RSP framework.",
 'Traceability Tag':'too-recent','Eval? (trackable)':'no','Action Trackable?':'','Finding Type':'governance','Scope':'government-AISI'
}); ROWS.append(r)

# Claude Opus 4 & Sonnet 4 base card joint eval (governance, no disclosed result, distinct from Constitutional Classifiers)
r=blank_row(); r.update({
 'Finding ID':'JOINT-2025-05-GOV2','Report ID':'ANTHROPIC-2025-05b-SELF','Institution':'Joint US AISI + UK AISI',
 'Report Title':'Claude Opus 4 & Claude Sonnet 4 System Card (base card)','Publication Date':'2025-05-22','Domain':'Transparency/Disclosure',
 'Tags':'claude-opus-4;claude-sonnet-4;anthropic;pre-deployment;cbrn;cyber;autonomy;no-disclosed-result',
 'Models / Systems':'Claude Opus 4; Claude Sonnet 4','Access Type':'Pre-deployment','Source URL':'https://www.anthropic.com/claude-4-system-card',
 'Finding':"The US AI Safety Institute and UK AI Security Institute conducted joint pre-deployment testing of Claude Opus 4 focused on catastrophic risks in CBRN, cybersecurity, and autonomous-capabilities domains -- no specific result is disclosed in this base system card (distinct from the later, separately-published Constitutional Classifiers red-teaming report).",
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Verified as genuinely distinct from JOINT-2025-00 (Constitutional Classifiers, Sept 2025) -- zero mentions of Constitutional Classifiers in this May 2025 base card. Process/transparency statement only.",
 'Key Quote':"joint pre-deployment testing of the new Claude Opus 4 model was conducted by the US AI Safety Institute (US AISI) and the UK AI Security Institute (UK AISI).",
 'Traceability Tag':'too-recent','Eval? (trackable)':'no','Action Trackable?':'','Finding Type':'governance','Scope':'government-AISI'
}); ROWS.append(r)

with open('/Users/kunalsingh/aisi-v4-audit/v5_apply/new_rows_batch.csv','a',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS)
    for r in ROWS: w.writerow(r)
print(f"Batch 4 (o3/o4-mini + governance rows): {len(ROWS)} rows appended")
