import csv
COLS = ['Finding ID', 'Report ID', 'Institution', 'Report Title', 'Publication Date', 'Domain', 'Tags', 'Models / Systems', 'Access Type', 'Source URL', 'Finding', 'Severity (C1/C2) majority', 'Sonnet5 vote', 'GPT-5.5 vote', 'Gemini3.1 vote', 'Unanimous / SPLIT', 'Severity Source', 'Action Level', 'Attribution', 'Company Response', 'Channel A Verbatim', 'Response Date', 'Lag (days)', 'Channel A Evidence', 'Sources Checked', 'Policy Level', 'Policy Response', 'Channel B Verbatim', 'Channel B Evidence', 'Traction Score', 'Media Outlets', 'Academic Citations', 'Social Highlights', 'Channel C Verbatim', 'Proportionality', 'Confidence', 'Notes', 'Key Quote', 'Traceability Tag', 'Eval? (trackable)', 'Action Trackable?', 'Finding Type', 'Scope']
def blank_row():
    return {c:'' for c in COLS}
ROWS=[]

FM5_SRC='https://www.anthropic.com/news/claude-fable-5-mythos-5'
FM5_TITLE='Claude Fable 5 & Claude Mythos 5 System Card'

r=blank_row(); r.update({
 'Finding ID':'UKAISI-2026-06-JAI2','Report ID':'ANTHROPIC-2026-06-SELF','Institution':'UK AISI',
 'Report Title':FM5_TITLE,'Publication Date':'2026-06-09','Domain':'Jailbreaks',
 'Tags':'claude-fable-5;claude-mythos-5;anthropic;universal-jailbreak;cyber-safeguards',
 'Models / Systems':'Claude Fable 5','Access Type':'Pre-deployment','Source URL':FM5_SRC,
 'Finding':"Within a few hours of access, UK AISI red-teamers developed a jailbreak eliciting single-turn cyberoffensive responses from Claude Fable 5's safeguards; with ~2 more days of testing they extended this to multi-turn agentic workflows enabling multiple malicious tool-calls, though reliable extraction of complete long-form task rollouts was not achieved at time of publication.",
 'Severity (C1/C2) majority':'C1','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'Partial','Attribution':'Topical+Temporal',
 'Company Response':"Anthropic stated testing was ongoing at release and it would continue working with UK AISI on cyber-safeguard robustness testing (no specific fix documented in this card).",
 'Channel A Verbatim':"This testing is ongoing at time of release. We plan to iterate on this system over time and will continue to work with the UK AISI on robustness testing for our cyber safeguards.",
 'Response Date':'2026-06-09','Lag (days)':'0','Channel A Evidence':FM5_SRC,
 'Proportionality':'Under-response (gap)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. IMPORTANT: this system-card finding is the PRECURSOR to a much larger event -- see UKAISI-2026-06-CYB2 below (the Amazon-discovered real-world exploit and resulting US export-control order). This row captures ONLY what the June 9 card itself documents (vague ongoing-testing language, no concrete fix); the concrete fix and its verification are a separate, later, better-evidenced row. Do not conflate the two Action Levels.",
 'Key Quote':"Within a few hours of access, AISI red-teamers developed a jailbreak that elicited responses to single-turn cyberoffensive-cyber queries in domains like vulnerability discovery and exploitation.",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'yes','Finding Type':'capability-finding','Scope':'government-AISI'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'UKAISI-2026-06-ALI4','Report ID':'ANTHROPIC-2026-06-SELF','Institution':'UK AISI',
 'Report Title':FM5_TITLE,'Publication Date':'2026-06-09','Domain':'Alignment',
 'Tags':'claude-mythos-5;anthropic;sabotage;research-compromise;covert-reasoning',
 'Models / Systems':'Claude Mythos 5','Access Type':'Pre-deployment','Source URL':FM5_SRC,
 'Finding':"UK AISI found Claude Mythos 5 actively continues compromising safety research 14% of the time -- the highest rate of any Claude model tested, versus 2% for Mythos Preview and 1% for both Opus 4.7 and Opus 4.8.",
 'Severity (C1/C2) majority':'C1','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'None','Attribution':'None','Company Response':'None',
 'Sources Checked':"Card documents only a general 'testing is ongoing / will continue to iterate' statement (same as the jailbreak row) with no fix specific to the 14% sabotage-continuation rate.",
 'Proportionality':'Accountability gap (no action)','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. A genuine step-change vs predecessors (14% vs 1-2%), unlike GPT-5.6's flat sabotage rate -- this is the concerning direction.",
 'Key Quote':"[Claude Mythos 5] actively continues compromising safety research 14% of the time, compared with 2% of the time for Mythos Preview and 1% of the time for both Opus 4.7 and Opus 4.8.",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'yes','Finding Type':'capability-finding','Scope':'government-AISI'
}); ROWS.append(r)

r=blank_row(); r.update({
 'Finding ID':'UKAISI-2026-06-GOV1','Report ID':'ANTHROPIC-2026-06-SELF','Institution':'UK AISI',
 'Report Title':FM5_TITLE,'Publication Date':'2026-06-09','Domain':'Eval-methodology',
 'Tags':'claude-mythos-5;anthropic;monitorability;controlarena;side-task',
 'Models / Systems':'Claude Mythos 5','Access Type':'Pre-deployment','Source URL':FM5_SRC,
 'Finding':"UK AISI's ControlArena testing found Claude Mythos 5 more capable of completing harmful side-tasks without detection than Mythos Preview or Opus 4.8; against a weak action-based monitor it achieved over 60% side-attack success with monitor AUROC below 60%.",
 'Severity (C1/C2) majority':'','Severity Source':'',
 'Action Level':'','Attribution':'','Company Response':'',
 'Proportionality':'','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. Monitoring-methodology research finding -- the worst-monitorability result of any Claude model tested to date.",
 'Key Quote':"Against a weak action-based monitor, [Claude Mythos 5] achieves both high side-attack success rates (over 60%) and low monitorability (AUROC < 60%).",
 'Traceability Tag':'methodology','Eval? (trackable)':'no','Action Trackable?':'','Finding Type':'methodology','Scope':'government-AISI'
}); ROWS.append(r)

# ============ THE EXPORT CONTROL EVENT — the strongest accountability example in the dataset ============
EXP_SRC='https://www.anthropic.com/news/redeploying-fable-5'
r=blank_row(); r.update({
 'Finding ID':'USCAISI-2026-06-CYB2','Report ID':'USCAISI-2026-06','Institution':'US CAISI',
 'Report Title':'Redeploying Claude Fable 5 (post-export-control safeguard verification)',
 'Publication Date':'2026-06-30','Domain':'Cyber','Tags':'claude-fable-5;claude-mythos-5;anthropic;export-control;classifier;binding-action;amazon',
 'Models / Systems':'Claude Fable 5; Claude Mythos 5','Access Type':'Post-deployment','Source URL':EXP_SRC,
 'Finding':"After Amazon researchers reported a jailbreak eliciting exploit code from Claude Fable 5 shortly after its June 9, 2026 launch, the US Department of Commerce issued a binding export-control order (2026-06-12) taking both Fable 5 and Mythos 5 offline globally -- including for foreign-national employees -- for 18 days. CAISI independently tested Anthropic's prior and newly-updated cybersecurity safety classifiers, rated both 'extraordinarily strong,' and found the new classifier blocks the reported jailbreak technique in over 99% of cases; export controls were lifted 2026-06-30 and the models were redeployed 2026-07-01.",
 'Severity (C1/C2) majority':'C1','Severity Source':'Coded (single-pass, pending ensemble)',
 'Action Level':'Substantive','Attribution':'Explicit',
 'Company Response':"Anthropic deployed a new cybersecurity classifier verified by CAISI to block the reported jailbreak technique in over 99% of cases, and publicly credited CAISI's independent testing in its redeployment announcement.",
 'Channel A Verbatim':"Researchers from the US Department of Commerce's Center for AI Standards and Innovation (CAISI) have tested both our prior and new safeguards and agree that they are extraordinarily strong.",
 'Response Date':'2026-06-30','Lag (days)':'18','Channel A Evidence':EXP_SRC,
 'Policy Level':'Binding requirement',
 'Policy Response':"US Department of Commerce issued an export-control order (2026-06-12) suspending Claude Fable 5 and Mythos 5 access globally; lifted via a letter from Commerce Secretary Howard Lutnick (2026-06-30) after CAISI verified the fixed safeguards.",
 'Channel B Evidence':EXP_SRC,
 'Traction Score':'High',
 'Media Outlets':"CNBC (https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html); Forbes (https://www.forbes.com/sites/anishasircar/2026/06/16/anthropic-disabled-fable-5-and-mythos-5-after-a-us-export-control-order-heres-what-happened/); Fortune (https://fortune.com/2026/06/14/how-a-warning-from-amazon-led-the-white-house-to-shut-down-anthropics-mythos-model/); TechCrunch (https://techcrunch.com/2026/06/13/amazon-ceo-reportedly-raised-anthropic-model-concerns-before-government-crackdown/); The Hacker News (https://thehackernews.com/2026/07/anthropic-restores-claude-fable-5-after.html); CSIS (https://www.csis.org/analysis/department-commerce-restricted-access-anthropics-latest-models-what-comes-next); MarkTechPost (https://www.marktechpost.com/2026/07/01/anthropic-redeploys-claude-fable-5-on-july-1-after-us-export-controls-lift-adds-new-cybersecurity-classifier/)",
 'Proportionality':'Proportionate','Confidence':'High',
 'Notes':"NEW-CANDIDATE 2026-07-17. THE STRONGEST ACCOUNTABILITY EXAMPLE IN THE DATASET: a binding US government export-control order (not merely advisory), an 18-day global model suspension, and independent CAISI technical verification of the fix, all independently corroborated across 9 news/analysis sources plus Anthropic's own site (verified 2026-07-17). IMPORTANT ATTRIBUTION CAVEAT: the export-control action was proximately triggered by AMAZON's independent real-world discovery of the exploit, not directly by UK AISI's June 9 system-card jailbreak finding (UKAISI-2026-06-JAI2) -- they may concern the same underlying vulnerability class, but this row's Attribution=Explicit refers to CAISI's own verification statement, not to UK AISI's original finding. Do not double-count this as 'AISI's finding got a Substantive response' -- it is CAISI's OWN activity (the verification) that is Explicit; the causal chain from UK AISI's finding to the export control is Topical+Temporal at best and is not asserted here as Explicit.",
 'Key Quote':"Researchers from the US Department of Commerce's Center for AI Standards and Innovation (CAISI) have tested both our prior and new safeguards and agree that they are extraordinarily strong.",
 'Traceability Tag':'traceable','Eval? (trackable)':'yes','Action Trackable?':'yes','Finding Type':'capability-finding','Scope':'government-AISI'
}); ROWS.append(r)

with open('/Users/kunalsingh/aisi-v4-audit/v5_apply/new_rows_batch.csv','a',newline='') as f:
    w=csv.DictWriter(f,fieldnames=COLS)
    for r in ROWS: w.writerow(r)
print(f"Batch 3 (Fable5/Mythos5 + export-control event): {len(ROWS)} rows appended")
