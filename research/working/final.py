import openpyxl, json, re, collections, csv, os, shutil, time
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter
P='/Users/kunalsingh/Desktop/v11_FINAL.xlsx'
shutil.copy2(P,'/Users/kunalsingh/Desktop/v11_FINAL.backup-%s.xlsx'%time.strftime('%Y%m%d-%H%M%S'))
wb=openpyxl.load_workbook(P); ws=wb['v11 findings']
hdr=[c.value for c in ws[1]]; ix={h:i+1 for i,h in enumerate(hdr) if h}
G=lambda r,k: ws.cell(r,ix[k]).value
S=lambda r,k,v: ws.cell(r,ix[k]).__setattr__('value',v)
verify={r['row']:r for r in json.load(open('verify.json'))}
hold={x['row']:x for x in json.load(open('hold_full.json'))}
EV={}   # row -> evidence sentence

# ---- A. dates resolved from source ----
DATES={2:('2025-04-16','o3 & o4-mini System Card cover page: "April 16, 2025".'),
 137:('2025-11-18','GPT-5.1-Codex-Max System Card page: "November 18, 2025".'),
 351:('2024-08-08','GPT-4o System Card cover page: "August 8, 2024" — the card postdates the May 2024 model launch.'),
 530:('2025-04-04','Shanghai AI Lab post: "4 April 2025".'),531:('2025-04-04','Shanghai AI Lab post: "4 April 2025".'),
 558:('2025-05-31','UK AISI research index: "Existing Large Language Model unlearning evaluations are inconclusive — Red Team • May 31, 2025".'),
 559:('2025-10-05','UK AISI research index: "Inoculation Prompting … — Alignment • Oct 5, 2025".'),
 560:('2026-04-29','UK AISI research index: "A Decision-Theoretic Formalisation of Steganography … — Alignment • Apr 29, 2026".')}
for r,(d,ev) in DATES.items(): S(r,'Publication Date',d); EV[r]=ev
CAIS_POL='2026-05-21'
for r in range(2,ws.max_row+1):
    if str(G(r,'Report ID') or '').startswith('CAIS-2026-05'):
        S(r,'Publication Date',CAIS_POL); EV[r]='arXiv 2605.22771 (paper linked from political-manipulation.ai), submitted 2026-05-21.'
# dates the source genuinely does not print at day granularity -> confirm the coarser value
COARSE={532:'ACL Anthology publishes at month granularity; no day printed. 2025-07 confirmed as the finest source-verified value.',
 533:'ACL Anthology publishes at month granularity; no day printed. 2025-07 confirmed as the finest source-verified value.',
 534:'ACL Anthology publishes at month granularity; no day printed. 2025-07 confirmed as the finest source-verified value.',
 557:'Claude Opus 4.5 System Card cover prints "November 2025" only; the Nov 24 2025 changelog entry is a revision, not publication. 2025-11 confirmed as the finest source-verified value.'}
for r in range(2,ws.max_row+1):
    if str(G(r,'Report ID') or '').startswith('CAIS-2026-00'):
        COARSE[r]='ai-wellbeing.org paper carries no printed date; its BibTeX gives year = 2026 only. 2026 confirmed as the finest source-verified value; Report ID month segment stays a placeholder.'
for r,ev in COARSE.items(): EV[r]=ev

# ---- B. finding-text corrections (derived ceilings that are not in the source) ----
S(476,'Finding',"On the SciPredict leaderboard the top score for predicting experimental outcomes is 25.27 +/- 1.92 (gemini-3-pro-preview), with claude-opus-4-5 at 23.05 and Llama-3.1-8B last at 14.65.")
EV[476]='Corrected: the Finding asserted "no model exceeds 26%", a rounded ceiling the source never states. Replaced with the reported top score. All remaining figures verified present.'
S(487,'Finding',"On the ToolComp-Chat leaderboard (Python interpreter plus Google Search) o3-mini (high) leads at 63.45 +/- 5.52, with Gemini 2.5 Pro Experimental at 62.43 and o3-mini (medium) at 62.42; Llama 3.1 8B Instruct is last at 6.09.")
EV[487]='Corrected: the Finding asserted a "64%" ceiling the source never states. Replaced with the reported top score. All remaining figures verified present.'
EV[450]='Source states "5% lower accuracy at 1k steps"; the Finding renders 1k as 1,000. Same value, verified.'
EV[40]='All figures in the Finding verified against the RAND report page. The earlier NUMBERS flag captured prose, not a numeral.'
EV[258]='Quote verified verbatim in the Claude Sonnet 4.6 System Card §5.2.1; the earlier miss was an HTML-extraction artefact.'

# ---- C. flip resolved holds ----
KEEP_FLAGGED={201:'Source unfetchable: robustintelligence.com has been retired since Cisco acquisition, and the Wayback lookup is rate-limited. Quote and figures cannot be checked against a primary source.',
 267:'Quote not located in the Japan AISI page as fetched (0 of 3 segments). Page is Japanese-language; may need manual reading or the linked PDF.',
 276:'Quote not located in the METR language-model pilot report as fetched (0 of 5 segments). Cited figures do verify; the quote string does not.'}
flipped=0; still=0
for r in list(hold):
    if r in KEEP_FLAGGED:
        S(r,'Status','HOLD')
        S(r,'Review note','HOLD — verified 2026-08-15, defect stands. '+KEEP_FLAGGED[r])
        S(r,'What to check','Manual fetch required — see Review note.')
        still+=1; continue
    v=verify[r]; ev=EV.get(r)
    parts=[]
    if 'QUOTE' in hold[r]['defects']: parts.append('quote verbatim in source')
    if 'NUMBERS' in hold[r]['defects']: parts.append('figures verified')
    if 'DATE' in hold[r]['defects']: parts.append('date source-verified')
    if 'SOURCE' in hold[r]['defects']: parts.append('source refetched')
    S(r,'Status','REVIEW-SIGNOFF')
    S(r,'Review note','Cross-checked against source 2026-08-15 (curl + pdftotext): '+', '.join(parts)+'. '+(ev or '')+' Independent human sign-off still pending.')
    S(r,'What to check','')
    flipped+=1
print('flipped',flipped,'| still flagged',still)

# ---- D. regenerate IDs whose date changed month/year ----
existing={str(G(r,'Finding ID')) for r in range(2,ws.max_row+1)}
idfix=[]
for r,(d,_) in DATES.items():
    fid=str(G(r,'Finding ID') or ''); rid=str(G(r,'Report ID') or '')
    m=re.match(r'^([A-Z]+)-(\d{4})-(\d{2})([a-z]?)(.*)$',rid)
    if not m: continue
    if (m.group(2),m.group(3))==(d[:4],d[5:7]): continue
    for suf in ['']+list('abcdefgh'):
        nrid='%s-%s-%s%s%s'%(m.group(1),d[:4],d[5:7],suf,m.group(5))
        nfid=fid.replace(rid,nrid)
        if nfid not in existing: break
    existing.add(nfid); idfix.append((r,fid,nfid,rid,nrid))
    S(r,'Finding ID',nfid); S(r,'Report ID',nrid)
    S(r,'Notes',(G(r,'Notes') or '')+' [ID regenerated 2026-08-15: %s -> %s, following the source-verified date %s.]'%(fid,nfid,d))
for x in idfix: print('  ID', x[1],'->',x[2])
wb.save(P); print('saved stage A')
