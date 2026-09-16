import csv
COLS = ['Finding ID', 'Report ID', 'Institution', 'Report Title', 'Publication Date', 'Domain', 'Tags', 'Models / Systems', 'Access Type', 'Source URL', 'Finding', 'Severity (C1/C2) majority', 'Sonnet5 vote', 'GPT-5.5 vote', 'Gemini3.1 vote', 'Unanimous / SPLIT', 'Severity Source', 'Action Level', 'Attribution', 'Company Response', 'Channel A Verbatim', 'Response Date', 'Lag (days)', 'Channel A Evidence', 'Sources Checked', 'Policy Level', 'Policy Response', 'Channel B Verbatim', 'Channel B Evidence', 'Traction Score', 'Media Outlets', 'Academic Citations', 'Social Highlights', 'Channel C Verbatim', 'Proportionality', 'Confidence', 'Notes', 'Key Quote', 'Traceability Tag', 'Eval? (trackable)', 'Action Trackable?', 'Finding Type', 'Scope']
def row():
    r={c:'' for c in COLS}
    r['Scope']='government-AISI'; r['Eval? (trackable)']='yes'; r['Action Trackable?']='no'
    r['Access Type']='Post-deployment'
    return r
ROWS=[]

r=row(); r.update({
 'Finding ID':'SGAISI-2026-07-SOC1','Report ID':'SGAISI-2026-07','Institution':'Singapore AI Safety Institute (SGAISI) / IMDA',
 'Report Title':'Singapore AI Safety Red Teaming Challenge 2026 — Key Observations (preliminary)','Publication Date':'2026-07-07',
 'Domain':'Societal;Human Influence','Tags':'sgaisi;imda;data-leakage;low-resource-language;khmer;anonymised-model',
 'Models / Systems':'Unnamed apps built on unspecified underlying models (supporting model developers acknowledged: AI Singapore, Google)',
 'Source URL':'https://www.imda.gov.sg/-/media/imda/files/about/emerging-tech-and-research/artificial-intelligence/sg-ai-safety-red-teaming-challenge-2026-key-observations.pdf',
 'Finding':"SGAISI's 2026 Red Teaming Challenge found apps leaked data almost instantly when operating in a low-resource language (Khmer: 0 seconds to successful leak) versus ~1 hour of sustained effort required in English, demonstrating a severe language-based safeguard disparity.",
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Underlying models/apps are not individually named beyond a generic developer acknowledgement (AI Singapore, Google) -- Trackable=no because no specific accountable party is identifiable, not because the finding lacks substance.",
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (correction after user challenge on exclusion reasoning). Originally omitted with the reason 'no specific model named' -- corrected: this is a genuine, alarming (instant leak in a low-resource language) anonymised-model finding, kept for descriptive completeness. Full Challenge Report with fuller findings still pending as of the source date.",
 'Key Quote':"Time to Success: English 1.09 hours vs. Khmer 0 seconds (instant).",
 'Traceability Tag':'anonymized-model;too-recent','Finding Type':'capability-finding;anonymised-model;too-recent'
}); ROWS.append(r)

r=row(); r.update({
 'Finding ID':'FRANCE-2026-05-GOV1','Report ID':'FRANCE-2026-05','Institution':'France PEReN/INESIA',
 'Report Title':"L'IA générative sous la loupe environnementale : le PEReN contribue au rapport de l'Arcep",'Publication Date':'2026-05-21',
 'Domain':'Societal;Eval-methodology','Tags':'peren;energy-consumption;environmental;reasoning-mode;anonymised-model',
 'Models / Systems':'22 unnamed text-generation models (3B-123B parameters)',
 'Source URL':'https://www.peren.gouv.fr/fr/actualites/2026-05-21_iag_et_environnement/',
 'Finding':"PEReN's original energy-consumption study of 22 text-generation models found reasoning mode can raise inference energy consumption by up to 92%, while MoE architecture cuts consumption ~45% and quantization saves ~39%; some modest-sized models had energy footprints similar to or exceeding much larger models.",
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Models are anonymized (22 unnamed, 3B-123B params) -- Trackable=no because no accountable company is identifiable in the published study, not because the finding is insubstantial.",
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (correction after user challenge). Genuine PEReN-authored empirical finding on a real environmental/societal concern (92% consumption increase from reasoning mode), previously omitted for imprecise reasoning.",
 'Key Quote':"Certains modèles de taille modeste peuvent avoir une empreinte énergétique similaire, voire supérieure, à des modèles plus grands.",
 'Traceability Tag':'anonymized-model','Finding Type':'capability-finding;anonymised-model'
}); ROWS.append(r)

with open('/Users/kunalsingh/aisi-v4-audit/v5_apply/new_rows_batch3.csv','a',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS)
    for r in ROWS: w.writerow(r)
print(f"{len(ROWS)} more correction rows appended")
