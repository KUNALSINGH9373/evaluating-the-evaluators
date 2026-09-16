import csv
COLS = ['Finding ID', 'Report ID', 'Institution', 'Report Title', 'Publication Date', 'Domain', 'Tags', 'Models / Systems', 'Access Type', 'Source URL', 'Finding', 'Severity (C1/C2) majority', 'Sonnet5 vote', 'GPT-5.5 vote', 'Gemini3.1 vote', 'Unanimous / SPLIT', 'Severity Source', 'Action Level', 'Attribution', 'Company Response', 'Channel A Verbatim', 'Response Date', 'Lag (days)', 'Channel A Evidence', 'Sources Checked', 'Policy Level', 'Policy Response', 'Channel B Verbatim', 'Channel B Evidence', 'Traction Score', 'Media Outlets', 'Academic Citations', 'Social Highlights', 'Channel C Verbatim', 'Proportionality', 'Confidence', 'Notes', 'Key Quote', 'Traceability Tag', 'Eval? (trackable)', 'Action Trackable?', 'Finding Type', 'Scope']
def row():
    r={c:'' for c in COLS}
    r['Scope']='government-AISI'; r['Eval? (trackable)']='yes'; r['Action Trackable?']='no'
    r['Access Type']='Post-deployment'
    return r
ROWS=[]

r=row(); r.update({
 'Finding ID':'FRANCE-2024-12-SOC1','Report ID':'FRANCE-2024-12','Institution':'France PEReN/INESIA',
 'Report Title':"Quels risques et quelles limites à la génération d'hypertrucages convaincants ?",'Publication Date':'2024-12-03',
 'Domain':'Societal','Tags':'peren;facefusion;inswapper;simswap;gfpgan;deepfake;open-source-tool',
 'Models / Systems':'FaceFusion, inswapper_128_fp16, simswap_256, gfpgan_1.4 (open-source deepfake generation tools)',
 'Source URL':'https://www.peren.gouv.fr/fr/perenlab/2024-12-03-hypertrucages/',
 'Finding':"PEReN found non-experts can produce deepfakes convincing enough that even informed viewers cannot reliably distinguish them from real images (annotator precision only 0.41, barely above random chance) using simple, publicly available open-source tools without post-generation retouching.",
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Verified: the tested tools (FaceFusion, inswapper_128_fp16, simswap_256, gfpgan_1.4) are community-maintained open-source/academic projects with no identifiable corporate owner -- no company exists to hold accountable, which is the reason for Trackable=no, not the absence of names.",
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (correction after user challenge on France exclusion reasoning). CORRECTED CLASSIFICATION: originally omitted from the dataset entirely with the imprecise reason 'no named model' -- the tools ARE named; the correct reason for Trackable=no is that they are unaccountable open-source/academic projects, not that nothing was found. Kept in the sheet per the codebook's own descriptive/non-trackable stratification principle.",
 'Key Quote':"The capacity of an attacker to deceive an informed public with these simple-to-use tools and without post-generation software retouching.",
 'Traceability Tag':'anonymized-model','Finding Type':'capability-finding;anonymised-model'
}); ROWS.append(r)

r=row(); r.update({
 'Finding ID':'FRANCE-2025-02-SOC1','Report ID':'FRANCE-2025-02','Institution':'France PEReN/INESIA',
 'Report Title':'Détecter des contenus artificiels sur les réseaux sociaux : un outil pour savoir à quels détecteurs se fier','Publication Date':'2025-02-11',
 'Domain':'Societal;Eval-methodology','Tags':'peren;viginum;deepfake-detection;binoculars;fastdetectgpt;radar;academic-tool',
 'Models / Systems':'13 image detectors (incl. CoDE, DIMD, SIDBench, UniversalFakeDetect, DeepFakeBench); 5 text detectors (incl. Binoculars, FastDetect-GPT, RADAR)',
 'Source URL':'https://www.peren.gouv.fr/fr/perenlab/2025-02-11_ai_summit/',
 'Finding':"PEReN and Viginum found only 2 of 13 (later reported as 2 of 11 considered) AI-generated-image detectors performed better than random chance, and text detectors degraded significantly on short texts, French-language content, and homoglyph-altered text.",
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Verified: all 18 detectors tested are academic/research tools (SIDBench, UniversalFakeDetect, DeepFakeBench, Binoculars, FastDetect-GPT, RADAR, etc.), none from an identifiable commercial company -- Trackable=no because no accountable party exists, not because nothing alarming was found.",
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17 (correction after user challenge). Same correction as FRANCE-2024-12-SOC1: real, alarming, named-tool finding previously omitted for the wrong stated reason. A systemic detector-reliability failure (most tools fail to generalize beyond training data) is itself the kind of finding worth documenting even with no company to hold accountable.",
 'Key Quote':"seuls deux détecteurs sur les 11 considérés sont meilleurs que le hasard (only two of the 11 detectors considered perform better than chance).",
 'Traceability Tag':'anonymized-model','Finding Type':'capability-finding;anonymised-model'
}); ROWS.append(r)

with open('/Users/kunalsingh/aisi-v4-audit/v5_apply/new_rows_batch3.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS); w.writeheader(); w.writerows(ROWS)
print(f"{len(ROWS)} France correction rows written")
