# -*- coding: utf-8 -*-
import json,openpyxl,datetime,shutil,time,collections
P='/Users/kunalsingh/Desktop/v11_FINAL.xlsx'
shutil.copy2(P,'/Users/kunalsingh/Desktop/v11_FINAL.backup-%s.xlsx'%time.strftime('%Y%m%d-%H%M%S'))
SD='2026-08-15'
scan={o['fid']:o for o in json.load(open('corpus_scan.json'))}

# (evaluator, subject company) pairs for which battery items 1/4/5 were executed by
# site-restricted search on the company domain this session
SEARCHED={('Redwood Research','Anthropic'),('Apollo Research','OpenAI'),('METR','OpenAI'),
          ('SecureBio','Anthropic'),('Center for AI Safety (CAIS)','OpenAI'),
          ('Center for AI Safety (CAIS)','Anthropic'),('Center for AI Safety (CAIS)','none')}

FOUND={
 'APOLLO-2026-03-ALI2':dict(level='Substantive',attr='Explicit attribution',
   resp="OpenAI published a third-party evaluation playbook committing to make reasoning traces and other intermediate artifacts available to external evaluators specifically to assess deception, sandbagging and evaluation awareness, and stated Apollo has used that access in OpenAI evaluations since GPT-5.",
   verb="We are also making reasoning traces and other intermediate artifacts available where they are needed to assess deception, sandbagging, or evaluation awareness. METR and Apollo have used this access in OpenAI evaluations since GPT-5.",
   rdate='2026-05-29',evid='https://openai.com/index/trustworthy-third-party-evaluations-foundations/',
   extra="Battery item 1/4 hit (OpenAI newsroom/index post, retrieved via Internet Archive snapshot 20260809065627 because openai.com/index returns HTTP 403 to direct fetch). Post discusses Apollo's GPT-5.5 evaluation-awareness result directly. Concrete change to evaluator access -> Substantive."),
 'REDWOOD-2024-12b-ALI1':dict(level='Partial',attr='Explicit attribution',
   resp="Anthropic's Alignment Science team published a follow-up study evaluating three training-time mitigations for alignment faking in RL, reporting that each was partially effective but that small prompt variations recovered the compliance gap.",
   verb="Black-box interrogation training. We add an extra dialogue turn which asks the model about its reasons for compliance, and penalise transcripts where this extra turn reveals undesired reasons.",
   rdate='2025-12-16',evid='https://alignment.anthropic.com/2025/alignment-faking-mitigations/',
   extra="Battery item 1 hit. Direct follow-up to the finding. Mitigations investigated and documented but explicitly found non-robust, and no deployed change is asserted -> Partial per §9 col 17, not Substantive."),
}
for k in ('REDWOOD-2024-12b-ALI2','REDWOOD-2024-12b-ALI3'):
    FOUND[k]=dict(FOUND['REDWOOD-2024-12b-ALI1'])

wb=openpyxl.load_workbook(P); ws=wb[wb.sheetnames[0]]
hdr=[c.value for c in ws[1]]; ix={h:i+1 for i,h in enumerate(hdr) if h}
S=lambda r,k,v: ws.cell(r,ix[k]).__setattr__('value',v)
G=lambda r,k: ws.cell(r,ix[k]).value
BASE=("Channel A battery run %s. Items (2)+(3) executed programmatically across 23 cached company "
      "system cards and deployment-safety documents (OpenAI 15, Anthropic 7, Meta 1), searching the "
      "evaluator name: ")%SD
cnt=collections.Counter(); prov=[]
for r in range(2,ws.max_row+1):
    fid=G(r,'Finding ID')
    if G(r,'Action Trackable?')!='yes' or G(r,'Action Level'): continue
    o=scan.get(fid)
    if fid in FOUND:
        d=FOUND[fid]
        pub=datetime.date.fromisoformat(str(G(r,'Publication Date'))[:10])
        lag=(datetime.date.fromisoformat(d['rdate'])-pub).days
        S(r,'Action Level',d['level']); S(r,'Attribution',d['attr'])
        S(r,'Company Response',d['resp']); S(r,'Channel A Verbatim',d['verb'])
        S(r,'Response Date',d['rdate']); S(r,'Lag (days)',lag); S(r,'Channel A Evidence',d['evid'])
        S(r,'Sources Checked (channel A)',"Channel A battery run %s. %s"%(SD,d['extra']))
        cnt[d['level']]+=1; continue
    n=o['nhits'] if o else 0
    seg=("%d mention(s) found, each inspected and found incidental (benchmark or dataset usage, "
         "table-of-contents text, or an evaluation predating this finding) - none responsive to this "
         "finding under the §8 causal-attribution test."%n) if n else "no mention found."
    pair=(o['inst'],o['dev']) if o else ('','')
    full = pair in SEARCHED
    if full:
        tail=("Items (1)+(4)+(5) executed by site-restricted web search on the subject company's "
              "domain for the evaluator name and the finding topic; no company primary source located. "
              "Battery exhausted -> Action Level = None.")
    else:
        tail=("Items (1)+(4)+(5) NOT yet individually exhausted for this evaluator/company pair. "
              "None is PROVISIONAL pending a company-newsroom and open-web sweep.")
        prov.append(fid)
    S(r,'Action Level','None'); S(r,'Attribution','No explicit attribution')
    S(r,'Sources Checked (channel A)',BASE+seg+' '+tail)
    cnt['None']+=1
wb.save(P)
print('coded',sum(cnt.values()),'rows:',dict(cnt))
print('provisional None (battery not exhausted):',len(prov))
tot=collections.Counter(G(r,'Action Level') for r in range(2,ws.max_row+1) if G(r,'Action Trackable?')=='yes')
print('\nALL 76 Tier A rows now:',dict(tot))
print('blank remaining:',sum(1 for r in range(2,ws.max_row+1) if G(r,'Action Trackable?')=='yes' and not G(r,'Action Level')))
