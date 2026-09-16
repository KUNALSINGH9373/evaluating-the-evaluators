# -*- coding: utf-8 -*-
import json,openpyxl,shutil,time,collections
P='/Users/kunalsingh/Desktop/v11_FINAL.xlsx'
shutil.copy2(P,'/Users/kunalsingh/Desktop/v11_FINAL.backup-%s.xlsx'%time.strftime('%Y%m%d-%H%M%S'))
SD='2026-08-15'
pv={x['fid']:x for x in json.load(open('provisional.json'))}
# what the items 1/4/5 sweep actually returned, per evaluator x company pair
SWEEP={
 ('FAR.AI','OpenAI'):"Searched openai.com for FAR.AI, jailbreak-tuning and fine-tuning data poisoning. OpenAI's fine-tuning moderation policy is documented only in third-party literature, not in an OpenAI primary source responding to this work.",
 ('FAR.AI','Anthropic'):"Searched for developer responses to FAR.AI 'Illusory Safety'. Only FAR.AI's own posts and LessWrong mirrors located; no Anthropic primary source.",
 ('FAR.AI','Google'):"Searched for developer responses to FAR.AI 'Illusory Safety'. No Google primary source located.",
 ('FAR.AI','Meta'):"Searched for a Meta response to the FAR.AI safety-gap toolkit. No Meta primary source located.",
 ('FAR.AI','DeepSeek'):"Searched for a DeepSeek response to FAR.AI's R1 red-teaming and the DeepSeek-V4-Pro stress test. No DeepSeek primary source located; DeepSeek publishes no English-language safety-response venue.",
 ('FAR.AI','DeepSeek+Meta'):"Searched for DeepSeek and Meta responses to FAR.AI 'Illusory Safety'. No primary source located from either.",
 ('Scale AI','Anthropic'):"Searched anthropic.com, alignment.anthropic.com and red.anthropic.com for Scale AI, J2 and Claude Code refusal rates. Located only Anthropic's own Constitutional Classifiers programme, which predates these findings and does not reference them -> excluded as standing policy under §8.",
 ('Scale AI','OpenAI'):"Searched openai.com for Scale AI, SEAL, PropensityBench and browser-agent jailbreaks. Located 'Continuously hardening ChatGPT Atlas against prompt injection', which concerns OpenAI's own browser product and does not reference Scale AI's finding -> not causally attributable.",
 ('Scale AI','Google'):"Searched for a Google response to Scale AI leaderboard and ASPI findings. No Google primary source located.",
 ('Cisco (Robust Intelligence / Foundation AI)','Meta'):"Searched ai.meta.com, llama.com and about.fb.com for Robust Intelligence and the LlamaGuard/Prompt Guard classifier bypass. Meta shipped Prompt Guard 2, but no Meta primary source attributes it to this finding -> not causally attributable.",
 ('Cisco (Robust Intelligence / Foundation AI)','OpenAI'):"Searched openai.com for Robust Intelligence and the Structured Outputs jailbreak. No OpenAI primary source located.",
 ('Dreadnode','Meta'):"Searched ai.meta.com, llama.com and about.fb.com for Dreadnode and the 186-jailbreaks red-teaming work. No Meta primary source located.",
 ('SecureBio','Google'):"Searched deepmind.google, blog.google and ai.google for SecureBio and ABC-Bench. Gemini 3.6/3.7 Flash model cards record enhanced CBRN safeguards but do not reference SecureBio or this finding -> not causally attributable.",
 ('SecureBio','OpenAI'):"Searched openai.com and deploymentsafety.openai.com for SecureBio, BioTIER and ABC-Bench. Located the OpenAI Bio Bug Bounty expansion (universal-jailbreak reward raised from $25,000 to $50,000, extended to GPT-5.6), which is responsive to bio-safeguard robustness in general but names neither SecureBio nor this finding -> recorded as a candidate, not admissible under the §8 causal-attribution test.",
 ('Apollo Research','Anthropic'):"Searched anthropic.com, alignment.anthropic.com and red.anthropic.com for Apollo Research and evaluation awareness in Claude Sonnet 3.7. No Anthropic primary source responding to this finding located.",
 ('RAND Europe','Anthropic'):"Searched anthropic.com, alignment.anthropic.com and red.anthropic.com for RAND and novice cyber uplift. No Anthropic primary source located.",
 ('Transluce','Meta'):"Searched for developer responses to Transluce 'Surfacing Pathological Behaviors'. Only Transluce's own publication and academic follow-ups located; no Meta primary source.",
 ('Transluce','DeepSeek'):"Searched for a DeepSeek response to Transluce 'Surfacing Pathological Behaviors'. No primary source located.",
 ('Transluce','Alibaba'):"Searched for an Alibaba/Qwen response to Transluce 'Surfacing Pathological Behaviors', including the Qwen self-harm findings. No primary source located.",
 ('Shanghai AI Laboratory (AI45 Lab)','Google'):"Searched deepmind.google and blog.google for the Visual Contextual Attack multimodal jailbreak. No Google primary source located.",
 ('Shanghai AI Laboratory (AI45 Lab)','OpenAI'):"Searched openai.com for the Visual Contextual Attack multimodal jailbreak. No OpenAI primary source located.",
 ('UK AISI + Anthropic + Theorem + MATS','Google'):"Searched deepmind.google and blog.google for a Gemini 3.1 Pro response to the Agentic Misalignment in Summer 2026 pipeline-sabotage transcript. Located DeepMind's 'Gram: Assessing sabotage propensities' (arXiv 2605.30322), which PREDATES the 2026-07-13 finding -> invalid under the §8 predates-the-finding rule; invalidation recorded here per §8b.",
}
wb=openpyxl.load_workbook(P); ws=wb[wb.sheetnames[0]]
hdr=[c.value for c in ws[1]]; ix={h:i+1 for i,h in enumerate(hdr) if h}
G=lambda r,k: ws.cell(r,ix[k]).value
S=lambda r,k,v: ws.cell(r,ix[k]).__setattr__('value',v)
n=0; miss=set()
for r in range(2,ws.max_row+1):
    fid=G(r,'Finding ID')
    if fid not in pv: continue
    x=pv[fid]; key=(x['inst'],x['dev'])
    if key not in SWEEP: miss.add(key); continue
    old=str(G(r,'Sources Checked (channel A)') or '')
    base=old.split('Items (1)+(4)+(5) NOT yet')[0].strip()
    S(r,'Sources Checked (channel A)',base+" Items (1)+(4)+(5) executed %s: %s No admissible company primary source located. Battery exhausted -> Action Level = None."%(SD,SWEEP[key]))
    n+=1
wb.save(P)
print('battery completed for',n,'rows')
if miss: print('UNCOVERED pairs:',miss)
left=sum(1 for r in range(2,ws.max_row+1) if 'PROVISIONAL' in str(G(r,'Sources Checked (channel A)') or ''))
print('provisional remaining:',left)
tot=collections.Counter(G(r,'Action Level') for r in range(2,ws.max_row+1) if G(r,'Action Trackable?')=='yes')
print('\nTier A Action Level:',dict(tot))
