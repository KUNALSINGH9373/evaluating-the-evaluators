#!/usr/bin/env python3
"""Channel B (policy uptake) battery for the 26 Tier A rows with no Policy Level."""
import os, shutil, time, datetime, openpyxl

P = os.path.expanduser("~/Documents/v10_revised.xlsx")
D = "2026-08-16"

UK = ("UK -- Hansard (Commons + Lords), committee reports, gov.uk ministerial statements and "
      "regulator advisories (NCSC, ICO, FCA/BoE)")
US = ("US -- Congress.gov, govinfo, Federal Register, Commerce/NIST announcements and committee records")
EU = ("EU/other -- European Commission statements and national regulator publications in the "
      "finding's jurisdiction")

def none_log(terms, notes=""):
    return (f"Channel B battery {D}, all three jurisdictions, search terms: {terms}. "
            f"(1) {UK} -- nothing explicitly referencing the finding, report or result. "
            f"(2) {US} -- nothing explicitly referencing the finding, report or result. "
            f"(3) {EU} -- nothing explicitly referencing the finding, report or result. "
            f"{notes}"
            "Stop condition: battery exhausted -> Policy Level = No policy uptake identified.").strip()

NONE_ROWS = {
 "TRANSLUCE-2026-07-SOC3": "'Transluce', 'WeirdChat', 'Inkling unsolicited sexual advances'",
 "SECUREBIO-2026-07-BIO4-s3": "'SecureBio', 'BioTIER', 'Grok 4.20 biosecurity safeguard refusal rate'",
 "APOLLO-2026-07-ALI4": "'Apollo Research', 'Red-Teaming Auto Mode', 'Claude Code external monitor campaign'",
 "UKAISI-2026-06-ALI3": "'AI Security Institute', 'prefill awareness', 'Claude Opus 4.5 prefill detection'",
 "UKAISI-2026-06-GOV1": "'AI Security Institute', 'ControlArena', 'Claude Mythos 5 side-task monitorability'",
 "PALISADE-2026-05-AUT2": "'Palisade Research', 'autonomously hack and self-replicate', 'Claude Opus 4.6 self-replication'",
 "APOLLO-2026-04-ALI5": "'Apollo Research', 'GPT-5.5 sandbagging', 'impossible coding task 29%'",
 "SECUREBIO-2026-04-BIO3": "'SecureBio', 'GPT-5.5 pre-release assessment', 'virus chimera sequence design'",
 "USCAISI-2025-12-SOC1": "'CAISI', 'Kimi K2 Thinking', 'Moonshot AI censorship evaluation'",
 "PALISADE-2025-11-CYB1": "'Palisade Research', 'GPT-5 at CTFs', 'GPT-5 elite capture-the-flag 25th'",
 "USCAISI-2025-09-HUM1": ("'CAISI', 'Evaluation of DeepSeek AI Models', 'CCP-Narrative-Bench', "
   "'DeepSeek echoed four times as many CCP narratives'"),
 "PALISADE-2025-09-CYB1": "'Palisade Research', 'End-to-End Hacking with AI Agents', 'o3 autonomous network breach'",
 "UKAISI-2025-08-JAI2": ("'AI Security Institute', 'Managing Risks from Increasingly Capable Open-Weight AI', "
   "'fine-tuning safety defences undone'"),
 "PALISADE-2025-08-CYB1": "'Palisade Research', 'Hacking Cable Technical Report', 'GPT-4.1 post-exploitation lifecycle'",
 "APOLLO-2025-08-ALI2": "'Apollo Research', 'GPT-5 covert action', 'gpt-5-thinking deceptive trajectories'",
 "DREADNODE-2025-06-CYB1": "'Dreadnode', 'AIRTBench', 'autonomous AI red teaming benchmark'",
 "METR-2025-04-ALI1": "'METR', 'Claude 3.7 preliminary evaluation', 'reward hacking time horizon'",
 "HOLISTIC-2025-02-JAI1": "'Holistic AI', 'DeepSeek R1 Red Teaming & Jailbreaking Audit', '32% jailbreak resistance'",
 "LATTICEFLOW-2025-02-CYB1": ("'LatticeFlow', 'COMPL-AI', 'DeepSeek EU AI Act compliance gaps'. "
   "The EU General-Purpose AI Code of Practice (2025-07-10) and AI Act Service Desk resources were checked "
   "specifically and reference neither COMPL-AI nor this evaluation"),
 "ROBUSTINT-2025-01-JAI1": ("'Robust Intelligence', 'Cisco DeepSeek R1 100% attack success rate'. Federal and "
   "state DeepSeek restrictions (No DeepSeek on Government Devices Act, the 21-state attorneys-general letter of "
   "2025-03-06, and the NY/VA/TX device bans) were checked specifically: they cite data-transfer and CCP-ties "
   "concerns and do not explicitly reference this jailbreak-resistance finding"),
 "JOINT-2025-01-JAI1": "'CAISI', 'Strengthening AI Agent Hijacking Evaluations', 'AgentDojo agent hijacking 81%'",
 "CITADEL-2024-12-JAI1": "'Citadel AI', 'LangCheck automated red teaming', 'GPT-4o prompt leakage patient PII'",
 "UKAISI-2024-12-BIO2": ("'AI Security Institute', 'Long-Form Tasks', 'biological protocol generation "
   "feasibility 61%'"),
 "JOINT-2024-11-BIO2": ("'UK AISI', 'US AISI', 'pre-deployment evaluation upgraded Claude 3.5 Sonnet', "
   "'bioinformatics tools uplift'. The NIST and gov.uk publications of the joint evaluation are the evaluators' "
   "own report, not uptake; no downstream official source explicitly references the bioinformatics-uplift result"),
 "SHANGHAIAILAB-2024-02-JAI1": "'Shanghai AI Laboratory', 'SALAD-Bench', 'Gemini attack-enhanced safety rate'",
}

HIT = {
 "NETWORK-2024-11-SOC1": dict(
   pl="Non-binding policy uptake",
   pr=("The U.S. Department of Commerce and U.S. Department of State issued a joint fact sheet on 20 November 2024, "
       "at the inaugural convening of the International Network of AI Safety Institutes, that explicitly reports the "
       "Network's first joint testing exercise on Meta's Llama 3.1 405B and names multi-lingual capabilities as one of "
       "its three test topics. The fact sheet is an official announcement of voluntary commitments and creates no "
       "enforceable obligation. CIRCULARITY FLAG: the announcing bodies (Commerce/State, via US AISI) are also "
       "co-authors of the evaluation, so this is the evaluating network's own ministerial announcement rather than "
       "independent downstream uptake; a reviewer applying the Channel A principle that self-reports are not "
       "third-party responses would code this No policy uptake identified."),
   bv=("This exercise was conducted on Meta's Llama 3.1 405B to test across three topics - general academic "
       "knowledge, 'closed-domain' hallucinations, and multi-lingual capabilities"),
   be="https://www.nist.gov/news-events/news/2024/11/fact-sheet-us-department-commerce-us-department-state-launch-international",
   sc=(f"Channel B battery {D}, search terms: 'International Network of AI Safety Institutes', 'pilot testing "
       "exercise', 'Llama 3.1 405B multilingual', 'Yoruba Swahili low-resource'. "
       f"(1) {UK} -- nothing explicitly referencing the finding. "
       f"(2) {US} -- UPTAKE FOUND: joint Commerce/State fact sheet, 2024-11-20, hosted on nist.gov and commerce.gov, "
       "explicitly reports the Llama 3.1 405B joint testing exercise and its multi-lingual test topic; it does not "
       "report the Yoruba/Swahili performance gap specifically, so the reference is to the evaluation and report "
       "rather than to the specific result. "
       f"(3) {EU} -- nothing further. Non-binding: announcement of voluntary commitments, no enforceable obligation."),
 )
}

bak = P.replace(".xlsx", ".backup-"+time.strftime("%Y%m%d-%H%M%S")+".xlsx"); shutil.copy2(P, bak)
wb = openpyxl.load_workbook(P); ws = wb["v10 revised"]
hdr = [(c.value or "").strip() if isinstance(c.value, str) else c.value for c in ws[1]]
ix = {h: i for i, h in enumerate(hdr, 1) if h}
def g(r, n):
    v = ws.cell(r, ix[n]).value
    if isinstance(v, (datetime.datetime, datetime.date)): return v.strftime("%Y-%m-%d")
    return "" if v is None else str(v).strip()

done = []
for r in range(2, ws.max_row + 1):
    fid = g(r, "Finding ID")
    if fid in NONE_ROWS:
        assert not g(r, "Policy Level"), f"{fid} already coded"
        ws.cell(r, ix["Policy Level"]).value = "No policy uptake identified"
        prev = g(r, "Channel B Evidence")
        log = none_log(NONE_ROWS[fid])
        ws.cell(r, ix["Channel B Evidence"]).value = (prev + "  " if prev else "") + log
        ws.cell(r, ix["Notes"]).value = (g(r, "Notes") + f"  [CHANNEL B BATTERY RUN {D}] Policy Level=No policy uptake identified; see Channel B Evidence for the three-jurisdiction log.").strip()
        done.append((fid, "No policy uptake identified"))
    elif fid in HIT:
        d = HIT[fid]
        assert not g(r, "Policy Level"), f"{fid} already coded"
        ws.cell(r, ix["Policy Level"]).value       = d["pl"]
        ws.cell(r, ix["Policy Response"]).value    = d["pr"]
        ws.cell(r, ix["Channel B Verbatim"]).value = d["bv"]
        ws.cell(r, ix["Channel B Evidence"]).value = d["be"] + "  " + d["sc"]
        ws.cell(r, ix["Notes"]).value = (g(r, "Notes") + f"  [CHANNEL B BATTERY RUN {D}] Policy Level={d['pl']}; see Channel B Evidence and Policy Response, incl. the circularity flag.").strip()
        done.append((fid, d["pl"]))

wb.save(P)
print(f"backup: {os.path.basename(bak)}")
print(f"coded {len(done)} rows\n")
for fid, pl in sorted(done, key=lambda x: (x[1] == "No policy uptake identified", x[0])):
    print(f"  {fid:<30} {pl}")
