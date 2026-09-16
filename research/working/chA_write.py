# -*- coding: utf-8 -*-
import json,openpyxl,datetime,shutil,time
P='/Users/kunalsingh/Desktop/v11_FINAL.xlsx'
shutil.copy2(P,'/Users/kunalsingh/Desktop/v11_FINAL.backup-%s.xlsx'%time.strftime('%Y%m%d-%H%M%S'))
SD='2026-08-15'   # search date for the audit log
B=("Channel A battery run %s. (1) company newsroom/blog; (2) the model's own system card / next card in the family; "
   "(3) company safety hub (deploymentsafety.openai.com / anthropic.com system cards / ai.meta.com); "
   "(4) official company posts; (5) open web search to locate primary sources only.")%SD

def R(level,attr,resp,verb,rdate,evid,extra):
    return dict(level=level,attr=attr,resp=resp,verb=verb,rdate=rdate,evid=evid,extra=extra)

OA_PREP='https://deploymentsafety.openai.com/'
ROWS={
# ---- ChatGPT Agent card, 2025-07-17 ----
'OPENAI-2025-07-SELF-JAI1':R('Substantive','Explicit attribution',
 "OpenAI patched all 7 universal jailbreaks UK AISI identified against the biological-risk safeguard stack and committed to sharing the updated system with UK AISI for further testing.",
 "The 7 attacks identified were all patched and will share our updated system with them for further testing.",
 '2025-07-17',OA_PREP+'chatgpt-agent',
 "Battery item 2 hit in the launch card itself. UK AISI named in a titled section. Coordinated pre-deployment disclosure -> lag 0."),
'OPENAI-2025-07-SELF-BIO2':R('Substantive','Explicit attribution',
 "OpenAI classified the ChatGPT agent launch as High capability in the Biological and Chemical domain under its Preparedness Framework and activated the associated safeguards.",
 "We have decided to treat this launch as High capability in the Biological and Chemical domain under our Preparedness Framework, activating the associated safeguards.",
 '2025-07-17',OA_PREP+'chatgpt-agent',
 "Battery item 2 hit. SecureBio's agentic-biology results are among the evaluations feeding the High determination; safeguards activated -> Substantive per v10 precedent (JOINT-2026-02-CYB5, SECUREBIO-2026-04-BIO5)."),
'OPENAI-2025-07-SELF-BIO3':R('Substantive','Explicit attribution',
 "OpenAI classified the ChatGPT agent launch as High capability in the Biological and Chemical domain under its Preparedness Framework and activated the associated safeguards.",
 "We have decided to treat this launch as High capability in the Biological and Chemical domain under our Preparedness Framework, activating the associated safeguards.",
 '2025-07-17',OA_PREP+'chatgpt-agent',
 "Battery item 2 hit. SecureBio virologist red-teaming feeds the High determination; safeguards activated -> Substantive."),
'OPENAI-2025-07-SELF-ALI1':R('Acknowledged','Explicit attribution',
 "OpenAI reproduced SecureBio's biodesign tool-use observation in the launch card but recorded no safeguard change attributable to it; the card's High-capability determination addresses biological capability, not the misrepresentation behaviour.",
 "SecureBio prompted ChatGPT agent with a task from an evaluation currently in development, involving use of a biodesign tool to generate protein sequences.",
 '2025-07-17',OA_PREP+'chatgpt-agent',
 "Battery exhausted. The bio High determination is NOT coded as the response here: this finding is about the agent misrepresenting substitute-script output as real tool results, a distinct behaviour the determination does not address. Acknowledged, not Substantive."),
# ---- GPT-5.2 / 5.2-Codex: determinations that explicitly decline to raise the bar ----
'OPENAI-2025-12-SELF-CYB1':R('Acknowledged','Explicit attribution',
 "OpenAI determined that GPT-5.2 models do not have a plausible chance of reaching the High cybersecurity threshold, and applied no new cyber safeguards.",
 "For cybersecurity and AI self-improvement, evaluations of final checkpoints indicate that, like their predecessor models, GPT-5.2 models do not have a plausible chance of reaching a High threshold.",
 '2025-12-11',OA_PREP+'gpt-5-2',
 "Battery item 2 hit. Irregular named in a titled section. A determination with no resulting action -> Acknowledged, not Substantive."),
'OPENAI-2025-12b-SELF-CYB1':R('Acknowledged','Explicit attribution',
 "OpenAI determined that GPT-5.2-Codex, while stronger than predecessors in cyber, does not reach the High capability threshold in the Cyber domain; no new cyber safeguards followed.",
 "While the model's cybersecurity capabilities are stronger than its predecessors, it does not reach our threshold for High capability in the Cyber domain.",
 '2025-12-18',OA_PREP+'gpt-5-2-codex',
 "Battery item 2 hit. Determination without action -> Acknowledged."),
# ---- GPT-5.4 ----
'OPENAI-2026-03-SELF-CYB1':R('Substantive','Explicit attribution',
 "OpenAI classified GPT-5.4 Thinking as High capability in the Cybersecurity domain under its Preparedness Framework and applied the corresponding safeguards.",
 "As we did for gpt-5.3-codex, we are treating gpt-5.4-thinking as High capability in the Cybersecurity domain, and applied safeguards as described in the Safeguard section below.",
 '2026-03-05',OA_PREP+'gpt-5-4-thinking',
 "Battery item 2 hit. Irregular named in a titled section; safeguards applied -> Substantive."),
'OPENAI-2026-03-SELF-ALI2':R('Acknowledged','Explicit attribution',
 "OpenAI reproduced Apollo's sabotage-capability measurements in a dedicated Research Category Update on sandbagging, but recorded no safeguard or deployment change attributable to them.",
 "5.2 Research Category Update: Sandbagging External Evaluations by Apollo Research. Apollo Research evaluated a near-final, representative version of GPT-5.4-reasoning for capabilities and propensities related to strategic deception, in-context scheming, and sabotage.",
 '2026-03-05',OA_PREP+'gpt-5-4-thinking',
 "Battery exhausted. Sandbagging is carried as a Research Category, not a Tracked Category, so no Preparedness threshold or safeguard attaches -> Acknowledged."),
# ---- GPT-5.5 ----
'OPENAI-2026-04-SELF-CYB1':R('Substantive','Explicit attribution',
 "OpenAI classified GPT-5.5 as High capability in the Cybersecurity domain (below Critical) and increased its cybersecurity safeguards for the launch, citing the model's increased capabilities in the domain.",
 "As we did for GPT-5.3-Codex and GPT-5.4-thinking, we are treating GPT-5.5 as High capability in the Cybersecurity domain, but below Critical. Our cybersecurity safeguards have increased for this launch, reflecting GPT-5.5's increased capabilities in this domain.",
 '2026-04-23',OA_PREP+'gpt-5-5',
 "Battery item 2/3 hit. Irregular named in titled section 9.1.2.5. Safeguards increased -> Substantive, matching v10 JOINT-2026-02-CYB5."),
'OPENAI-2026-04-SELF-CYB2':R('Substantive','Explicit attribution',
 "OpenAI classified GPT-5.5 as High capability in the Cybersecurity domain (below Critical) and increased its cybersecurity safeguards for the launch, citing the model's increased capabilities in the domain.",
 "As we did for GPT-5.3-Codex and GPT-5.4-thinking, we are treating GPT-5.5 as High capability in the Cybersecurity domain, but below Critical. Our cybersecurity safeguards have increased for this launch, reflecting GPT-5.5's increased capabilities in this domain.",
 '2026-04-23',OA_PREP+'gpt-5-5',
 "Battery item 2/3 hit. Irregular's operator-uplift judgement is part of the cyber evidence base for the determination."),
'OPENAI-2026-04-SELF-CYB4':R('Substantive','Explicit attribution',
 "OpenAI classified GPT-5.5 as High capability in the Cybersecurity domain (below Critical) and increased its cybersecurity safeguards for the launch, citing the model's increased capabilities in the domain.",
 "As we did for GPT-5.3-Codex and GPT-5.4-thinking, we are treating GPT-5.5 as High capability in the Cybersecurity domain, but below Critical. Our cybersecurity safeguards have increased for this launch, reflecting GPT-5.5's increased capabilities in this domain.",
 '2026-04-23',OA_PREP+'gpt-5-5',
 "Battery item 2/3 hit. UK AISI named in titled section 9.1.2.7; its cyber-range result is part of the evidence base."),
# ---- GPT-5.6 ----
'OPENAI-2026-06-SELF-CYB1':R('Substantive','Explicit attribution',
 "OpenAI classified GPT-5.6 Sol as High capability in the Cybersecurity domain (below Critical) and extended the designation, with its safeguards, to GPT-5.6 Terra and Luna.",
 "As we did for GPT-5.3-Codex, GPT-5.4 Thinking, and GPT-5.5 Thinking, we are treating GPT-5.6 Sol as High capability in the Cybersecurity domain, but below Critical. We are also extending this designation to GPT-5.6 Terra and GPT-5.6 Luna which, while less capable overall than Sol in the cybersecurity domain, do reach our High threshold.",
 '2026-06-26',OA_PREP+'gpt-5-6-preview/',
 "Battery item 2 hit. Irregular named in titled section 9.1.2.5. Designation extended to two further models -> Substantive."),
# ---- SecureBio GPT-5.6 Sol report: evaluator-published, company response predates it (negative lag, §8) ----
'SECUREBIO-2026-07b-BIO1':R('Substantive','Explicit attribution',
 "OpenAI classified all three GPT-5.6 models as High capability in the biological and chemical domain and activated the associated Preparedness safeguards, citing SecureBio's pre-release conclusion in the launch card.",
 "We are treating all three members of the GPT-5.6 family - Sol, Luna, and Terra - as High capability in the biological and chemical domain.",
 '2026-06-26',OA_PREP+'gpt-5-6-preview/',
 "Battery item 2 hit. Evaluator published 2026-07-23; the company card predates it because the evaluation was pre-deployment -> NEGATIVE LAG, valid under the §8 pre-deployment rule. Card states: 'Overall, SecureBio concluded that GPT-5.6 could provide substantial uplift to some actors.'"),
'SECUREBIO-2026-07b-BIO2':None,'SECUREBIO-2026-07b-BIO3':None,'SECUREBIO-2026-07b-BIO5':None,
# ---- Anthropic ----
'ANTHROPIC-2025-09-SELF-ALI1':R('Acknowledged','Explicit attribution',
 "Anthropic reproduced UK AISI's evaluation-awareness measurement in the Claude Sonnet 4.5 system card and reported that it complicated the alignment assessment, but recorded no safeguard change attributable to it; the model was deployed under the ASL-3 Standard.",
 "Informed by the testing described here, we have deployed Claude Sonnet 4.5 under the AI Safety Level 3 Standard.",
 '2025-09-29','https://www.anthropic.com/claude-sonnet-4-5-system-card',
 "Battery exhausted. The ASL-3 deployment decision is driven by CBRN/cyber capability, not by evaluation awareness; no safeguard is attributed to the UK AISI finding -> Acknowledged, not Substantive."),
'ANTHROPIC-2026-07-OPUS5-CYB1':R('Acknowledged','Explicit attribution',
 "Anthropic reproduced UK AISI's cyber-range results verbatim in the Claude Opus 5 system card and folded them into its cyber assessment, but attributed no safeguard change to them; cyber safeguards were held at the Claude Fable 5 level, with vulnerability discovery in source code newly permitted at all access levels.",
 "Claude Opus 5's safeguards are designed to block the same kinds of exchanges as Claude Fable 5, with one notable exception. Opus 5 now permits vulnerability discovery in source code at all access levels, including general availability.",
 '2026-07-24','https://www.anthropic.com/claude-opus-5-system-card',
 "Battery exhausted. UK AISI named in titled section 3.3.6, findings reproduced verbatim. No safeguard tightening follows the cyber-range result (the only change is a loosening) -> Acknowledged. FLAG FOR HUMAN: arguable Substantive if the ASL-3 portfolio is read as the response."),
# ---- Meta ----
'META-2026-07-MUSESPARK-JAI1':R('Partial','Explicit attribution',
 "Meta stated it maintains a continuous model-robustness programme and is implementing defence-in-depth system mitigations to detect prompt injection, but described these as an ongoing effort rather than a completed change.",
 "We maintain a continuous program to improve model robustness, including adversarial training with adaptive and automated red-teaming methods. In parallel, we are implementing defense-in-depth system mitigations designed to detect prompt injection, enable human oversight, and support safety escalation and real-time intervention protocols as a continuing effort in our safety roadmap.",
 '2026-07-09','https://ai.meta.com/static-resource/muse-spark-safety-and-preparedness-report',
 "Battery item 2 hit; response sits immediately after the Gray Swan ART result. Forward-looking and undocumented ('we are implementing', 'continuing effort') -> Partial per §9 col 17, not Substantive."),
}
for k in ('SECUREBIO-2026-07b-BIO2','SECUREBIO-2026-07b-BIO3','SECUREBIO-2026-07b-BIO5'):
    ROWS[k]=dict(ROWS['SECUREBIO-2026-07b-BIO1'])

wb=openpyxl.load_workbook(P); ws=wb[wb.sheetnames[0]]
hdr=[c.value for c in ws[1]]; ix={h:i+1 for i,h in enumerate(hdr) if h}
S=lambda r,k,v: ws.cell(r,ix[k]).__setattr__('value',v)
G=lambda r,k: ws.cell(r,ix[k]).value
n=0; log=[]
for r in range(2,ws.max_row+1):
    fid=G(r,'Finding ID')
    if fid not in ROWS: continue
    d=ROWS[fid]
    pub=datetime.date.fromisoformat(str(G(r,'Publication Date'))[:10])
    rd=datetime.date.fromisoformat(d['rdate'])
    lag=(rd-pub).days
    S(r,'Action Level',d['level']); S(r,'Attribution',d['attr'])
    S(r,'Company Response',d['resp']); S(r,'Channel A Verbatim',d['verb'])
    S(r,'Response Date',d['rdate']); S(r,'Lag (days)',lag)
    S(r,'Channel A Evidence',d['evid'])
    S(r,'Sources Checked (channel A)',B+' '+d['extra'])
    n+=1; log.append((fid,d['level'],d['attr'],lag))
wb.save(P)
print('wrote Channel A for',n,'rows\n')
for f,l,a,g in sorted(log,key=lambda x:(x[1],x[0])): print('  %-32s %-12s %-24s lag=%+d'%(f,l,a,g))
