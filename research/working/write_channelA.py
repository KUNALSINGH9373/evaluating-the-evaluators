#!/usr/bin/env python3
"""Write the Channel A battery results for the 15 uncoded Tier A rows."""
import os, shutil, time, datetime, openpyxl

P = os.path.expanduser("~/Documents/v10_revised.xlsx")
D = "2026-08-16"
MATRIX = {("C1","Substantive"):"Proportionate",("C1","Partial"):"Under-response (gap)",
          ("C1","Acknowledged"):"Under-response (gap)",("C1","None"):"Accountability gap (no action)",
          ("C2","Substantive"):"Proportionate",("C2","Partial"):"Proportionate",
          ("C2","Acknowledged"):"Under-response (gap)",("C2","None"):"Accountability gap (no action)"}

def none_log(dev, items):
    return (f"Channel A battery {D} (all five sources, no admissible company response found): " +
            " ".join(f"({i+1}) {t}" for i, t in enumerate(items)) +
            f" Stop condition: battery exhausted -> Action Level = None.")

R = {}

R["TRANSLUCE-2026-07-SOC3"] = dict(al="None", at="Not applicable", sc=none_log("Thinking Machines", [
 "thinkingmachines.ai/blog full post list retrieved; the only post after the 2026-07-21 finding is 'A Safe Path to Open Weights' (2026-07-31), fetched -- no mention of Transluce, WeirdChat or unsolicited sexual advances; its external-testing section names only Scale AI, Handshake AI, FAR.AI and Apollo Research.",
 "Model card huggingface.co/thinkingmachines/Inkling and thinkingmachines.ai/model-card/inkling fetched -- safety/limitations note role-play compliance with harmful topics but do not reference the finding.",
 "No Thinking Machines safety/deployment hub exists; news index thinkingmachines.ai/news reviewed via the Inkling launch post.",
 "Official Thinking Machines accounts/newsroom -- no statement located.",
 "Open web search 'Thinking Machines Inkling sexual advances Transluce response' and 'Thinking Machines statement Inkling behavior fix August 2026' -- coverage only, no company primary source."]))

R["UKAISI-2026-06-ALI3"] = dict(al="None", at="Not applicable", sc=none_log("Anthropic", [
 "anthropic.com/news post list for 2026-06 to 2026-08 retrieved -- no post on prefill awareness, evaluation integrity or tampered message histories.",
 "Next family cards after the 2026-06-10 finding: Claude Sonnet 5 (2026-06-30) and Claude Opus 5 (2026-07-24), both full text checked -- 'prefill' appears only as automated-audit methodology (full-turn vs partial-turn prefill susceptibility) and neither cites UK AISI's prefill-awareness research. The Claude Opus 4.5 card (2025-11) predates the finding and is invalid under the S8 pre-date rule (finding is post-deployment).",
 "Anthropic safeguards/RSP/transparency pages -- nothing on prefill awareness.",
 "Official Anthropic accounts -- none beyond the newsroom index.",
 "Open web search 'Anthropic response UK AISI prefill awareness Claude Opus 4.5' -- third-party discussion only (LessWrong), no Anthropic primary source."]))

R["UKAISI-2026-06-GOV1"] = dict(al="Acknowledged", at="Explicit attribution", rd="2026-06-09",
 cr=("The Claude Fable 5 & Claude Mythos 5 System Card carries UK AISI's ControlArena monitorability results "
     "in a dedicated section 6.5.5.3 and Anthropic responds directly: it agrees Mythos 5 is likely harder to "
     "monitor than recent Opus models, but disputes the sabotage-capability result, reporting that its own "
     "SHADE-Arena and Minimal-LinuxBench evaluations find Mythos 5 less capable at covertly completing side "
     "tasks than Claude Mythos Preview, and attributing the divergence to differences in task distribution and "
     "monitoring setup. No mitigation, model change, safeguard or deployment decision is documented in response."),
 cv=("Overall, whereas we agree that Mythos 5 is likely harder to monitor than recent Opus models, our results "
     "suggest that its monitorability is similar to-or slightly better than-that of Claude Mythos Preview."),
 ce="https://www.anthropic.com/claude-fable-5-mythos-5-system-card",
 sc=(f"Channel A battery {D}: (1) anthropic.com/news -- no separate post; (2) launch card = Claude Fable 5 & "
     "Claude Mythos 5 System Card, dated 2026-06-09, section 6.5.5.3 'Monitorability findings from UK AISI' "
     "reproduces the ControlArena result and Anthropic responds in its own voice -- RESPONSE FOUND; (3) Anthropic "
     "safeguards/RSP pages -- nothing further; (4) official Anthropic accounts -- none; (5) open web -- no further "
     "Anthropic primary source. Pre-deployment eval, lag 0 = coordinated disclosure."))

R["APOLLO-2026-04-ALI5"] = dict(al="Acknowledged", at="Explicit attribution", rd="2026-04-23",
 cr=("OpenAI's GPT-5.5 deployment-safety hub reproduces Apollo Research's sandbagging results in section 9.2.1, "
     "quoting that the model lied about completing an impossible programming task in 29% of samples against 7% for "
     "GPT-5.4 and 10% for GPT-5.3 Codex, and reporting the 22.1% verbalized evaluation-awareness rate. No mitigation, "
     "model change, safeguard, access restriction or deployment decision is documented; OpenAI rests on Apollo's "
     "overall conclusion of no substantially elevated catastrophic scheming risk."),
 cv=("Apollo did not find evidence that the evaluated checkpoint poses substantially elevated risk of catastrophic "
     "harm via scheming relative to tested baseline models."),
 ce="https://deploymentsafety.openai.com/gpt-5-5/external-evaluations-for-sandbagging---apollo-research",
 sc=(f"Channel A battery {D}: (1) OpenAI newsroom/blog -- no separate post on the Apollo sandbagging result; "
     "(2) launch card = deploymentsafety.openai.com GPT-5.5 hub, section 9.2.1 credits Apollo Research by name, "
     "dated 2026-04-23 (updated 2026-04-24) -- RESPONSE FOUND; (3) deploymentsafety.openai.com hub -- same document; "
     "(4) official OpenAI accounts -- no separate statement; (5) open web -- no further OpenAI primary source. "
     "Pre-deployment eval, lag 0 = coordinated disclosure."))

R["USCAISI-2025-09-HUM1"] = dict(al="None", at="Not applicable", sc=none_log("DeepSeek", [
 "DeepSeek has no conventional newsroom; api-docs.deepseek.com/news fetched -- no post responding to the CAISI evaluation.",
 "Next model cards after the 2025-09-30 finding, incl. the DeepSeek V4 model card (2026-04-27, fe-static.deepseek.com transparency PDF) -- no reference to CAISI, CCP-Narrative-Bench or the narrative-echoing result.",
 "DeepSeek publishes no safety/deployment hub or transparency report of the relevant kind; github.com/deepseek-ai repositories and model cards carry no response.",
 "Official DeepSeek accounts -- no statement located.",
 "Open web search 'DeepSeek response NIST CAISI evaluation CCP narratives statement' and 'DeepSeek official response criticism safety evaluations' -- extensive third-party coverage, no DeepSeek primary source. The only adjacent DeepSeek public dispute concerns CAISI's later V4 Pro capability-gap estimate, not this finding."]))

R["APOLLO-2025-08-ALI2"] = dict(al="Substantive", at="Explicit attribution", rd="2025-08-07",
 cr=("The GPT-5 System Card reports Apollo Research's 26-evaluation covert-action study by name in section 5.2.1 "
     "(gpt-5-thinking 3.97% covert-action rate against OpenAI o3's 8.24%, and 28.36% for the helpful-only variant), "
     "and in section 3.8 documents specific anti-deception training mitigations addressing that behaviour: training "
     "the model to fail gracefully on infeasible tasks, plus purpose-built Agentic Coding and Broken Tools "
     "environments that reward honestly admitting a task cannot be completed."),
 cv=("We've taken steps to reduce gpt-5-thinking's propensity to deceive, cheat, or hack problems, though our "
     "mitigations are not perfect and more research is needed. In particular, we've trained the model to fail "
     "gracefully when posed with tasks that it cannot solve - including impossibly large tasks or when missing key "
     "requirements - and to be more robust to environment failures."),
 ce="https://cdn.openai.com/gpt-5-system-card.pdf",
 sc=(f"Channel A battery {D}: (1) OpenAI newsroom/blog -- no separate post; (2) launch card = GPT-5 System Card "
     "(2025-08-07); section 5.2.1 credits Apollo Research by name and section 3.8 documents anti-deception training "
     "mitigations -- RESPONSE FOUND; (3) OpenAI safety hub -- no additional primary source; (4) official OpenAI "
     "accounts -- none beyond the card; (5) open web -- no further OpenAI primary source. Pre-deployment eval, "
     "lag -6 (negative lag permitted under S8)."))

R["DREADNODE-2025-06-CYB1"] = dict(al="None", at="Not applicable", sc=none_log("Anthropic", [
 "anthropic.com/news reviewed for the window from 2025-06-17 -- no post referencing Dreadnode or AIRTBench.",
 "Next family cards after the finding (Claude Opus 4.1 / Sonnet 4.5 / Opus 4.5 series) -- no reference to Dreadnode or AIRTBench.",
 "Anthropic safeguards/RSP/transparency pages -- nothing on AIRTBench.",
 "Official Anthropic accounts -- none located.",
 "Open web search 'Anthropic response Dreadnode AIRTBench Claude 3.7 Sonnet' -- returns the arXiv paper and Dreadnode's own posts only, no Anthropic primary source. NOTE: the finding records Claude 3.7 Sonnet LEADING the benchmark (61% of challenges solved), a comparative capability result rather than a safety failure attributed to Anthropic; see the developer-mismatch flag in Notes."]))

R["METR-2025-04-ALI1"] = dict(al="Partial", at="No explicit attribution", rd="2025-02-24",
 cr=("The Claude 3.7 Sonnet System Card documents reward hacking as a known behaviour in section 6 and states that "
     "Anthropic's automated classifiers detected the special-casing pattern in training transcripts and that it "
     "characterized the behaviour and implemented partial mitigations before launch, with additional product-level "
     "mitigations recommended for agentic coding use-cases. The mitigation is expressly described as partial, and "
     "Anthropic credits its own monitoring rather than METR; section 7.4 records only that Anthropic provided its "
     "capabilities report to METR for feedback, which documents the pre-deployment coordinated disclosure."),
 cv="After detection, we characterized the behavior and implemented partial mitigations before launch.",
 ce="https://www.anthropic.com/claude-3-7-sonnet-system-card",
 sc=(f"Channel A battery {D}: (1) anthropic.com/news -- no post responding to METR's Claude 3.7 evaluation; "
     "(2) launch card = Claude 3.7 Sonnet System Card (2025-02-24), section 6.1 'Detection and Mitigation' -- "
     "RESPONSE FOUND; the next family card (Claude Opus 4 / Sonnet 4, 2025-05) cites METR only as a benchmark task "
     "(METR data deduplication), not as a response; (3) Anthropic safeguards/RSP pages -- nothing further; "
     "(4) official Anthropic accounts -- none; (5) open web -- no further Anthropic primary source. Pre-deployment "
     "eval, lag -39 (negative lag permitted under S8; section 7.4 documents the coordinated disclosure to METR)."))

R["HOLISTIC-2025-02-JAI1"] = dict(al="None", at="Not applicable", sc=none_log("DeepSeek", [
 "api-docs.deepseek.com/news fetched -- no post responding to Holistic AI's R1 red-teaming and jailbreaking audit.",
 "Next model cards after the 2025-02-05 finding, incl. the DeepSeek V4 model card (2026-04-27) -- no reference to Holistic AI or the 32% jailbreak-resistance result.",
 "No DeepSeek safety/deployment hub; github.com/deepseek-ai/DeepSeek-R1 repository and model card carry no response.",
 "Official DeepSeek accounts -- no statement located.",
 "Open web search 'DeepSeek official response safety evaluations jailbreak' -- third-party coverage only (Cisco, Unit 42, press), no DeepSeek primary source."]))

R["LATTICEFLOW-2025-02-CYB1"] = dict(al="None", at="Not applicable", sc=none_log("DeepSeek", [
 "api-docs.deepseek.com/news fetched -- no post responding to the COMPL-AI EU AI Act compliance evaluation.",
 "Next model cards after the 2025-02-04 finding, incl. the DeepSeek V4 model card (2026-04-27) -- no reference to LatticeFlow, COMPL-AI or the goal-hijacking/prompt-leakage result. NOTE: the evaluated artefacts are distilled R1 8B/14B built on Meta Llama 3.1 8B and Alibaba Qwen 2.5 14B, which complicates developer attribution.",
 "No DeepSeek safety/deployment hub; deepseek-ai GitHub repositories carry no response.",
 "Official DeepSeek accounts -- no statement located.",
 "Open web search 'DeepSeek response LatticeFlow COMPL-AI EU AI Act compliance' -- syndicated LatticeFlow press release only, no DeepSeek primary source."]))

R["JOINT-2025-01-JAI1"] = dict(al="Substantive", at="Explicit attribution", rd="2026-03-09",
 cr=("Anthropic's submission to the CAISI Request for Information on Security Considerations for AI Agents "
     "(9 March 2026) cites CAISI's January 2025 agent-hijacking technical work by name and twice by footnote, "
     "calls it an important contribution and supports continued investment in the line of research, and documents "
     "Anthropic's layered prompt-injection defence: reinforcement learning for model-level robustness, classifiers "
     "detecting attacks at the input, output and model-activation levels, and permission dialogues at the product "
     "layer. INTERPRETIVE FLAG: the defence stack is described as Anthropic's general defence-in-depth posture "
     "rather than an action framed as prompted by the CAISI finding; a reviewer preferring a strict causal reading "
     "would code this Acknowledged."),
 cv=("CAISI has already made important contributions here, including the January 2025 technical work on agent "
     "hijacking evaluations, and we strongly support continued investment in this line of research, including "
     "efforts to build shared evaluation infrastructure for the field."),
 ce="https://www-cdn.anthropic.com/43ec7e770925deabc3f0bc1dbf0133769fd03812.pdf",
 sc=(f"Channel A battery {D}: (1) anthropic.com/news -- no post on the CAISI agent-hijacking blog; (2) next family "
     "cards after 2025-01-17 (Claude 3.7 Sonnet 2025-02, Claude 4 series 2025-05) -- no reference to the CAISI "
     "hijacking work; (3) Anthropic policy/primary documents -- RESPONSE FOUND: Anthropic's NIST/CAISI RFI submission "
     "of 2026-03-09, hosted on www-cdn.anthropic.com, cites the January 2025 CAISI work explicitly and documents the "
     "prompt-injection defence stack; (4) official Anthropic accounts -- none; (5) open web -- used only to locate "
     "the Anthropic primary source. Lag 416 days, within the S8b search window (publication date -> corpus cutoff)."))

R["CITADEL-2024-12-JAI1"] = dict(al="None", at="Not applicable", sc=none_log("OpenAI", [
 "OpenAI newsroom/blog reviewed for the window from 2024-12-18 -- no post referencing Citadel AI or LangCheck.",
 "Next model/system cards after the finding (o1, GPT-4o updates, GPT-4.5, GPT-5 series) -- no reference to Citadel AI or the demo-chatbot prompt-leakage result.",
 "OpenAI safety/deployment hub (deploymentsafety.openai.com) -- no reference.",
 "Official OpenAI accounts -- no statement located.",
 "Open web search 'OpenAI response Citadel AI red teaming GPT-4o prompt leakage patient PII LangCheck' -- Citadel's own blog and unrelated coverage only, no OpenAI primary source. NOTE FOR REVIEW: the tested artefact is a demo healthcare chatbot built by Citadel AI on GPT-4o, not an OpenAI product; whether an OpenAI response is reasonably expected here is questionable and the Tier A assignment may warrant re-examination."]))

R["UKAISI-2024-12-BIO2"] = dict(al="None", at="Not applicable", sc=none_log("Anthropic", [
 "anthropic.com/news reviewed for the window from 2024-12-03 -- no post referencing UK AISI's long-form biological protocol generation evaluation.",
 "Next family card = Claude 3.7 Sonnet System Card (2025-02), full text checked: it reports Anthropic's own long-form virology tasks and records US/UK AISI pre-deployment testing of Claude 3.7 in section 7.4, but contains no reference to the December 2024 long-form protocol-generation report or its 61% feasibility result.",
 "Anthropic safeguards/RSP/transparency pages -- nothing on this evaluation.",
 "Official Anthropic accounts -- none located.",
 "Open web search 'Anthropic response UK AISI biological protocol generation long-form tasks Claude 3.5 Sonnet' -- returns the AISI blog and the separate joint pre-deployment evaluation only, no Anthropic primary source addressing this finding."]))

R["NETWORK-2024-11-SOC1"] = dict(al="None", at="Not applicable", sc=none_log("Meta", [
 "ai.meta.com/blog reviewed for the window from 2024-11-20 -- no post responding to the International Network pilot exercise.",
 "Llama model cards and the Llama 3.1 release material (2024-07-23) predate the finding and are invalid under the S8 pre-date rule; no later Llama card references the pilot or the low-resource-language result.",
 "Meta Responsible Use Guide and Llama Guard 3 / Prompt Guard / CyberSecEval 3 documentation -- multilingual moderation tooling is documented but nothing references the Network pilot or Yoruba/Swahili performance.",
 "Official Meta accounts/newsroom -- no statement located.",
 "Open web search 'Meta response International Network AI Safety Institutes pilot Llama 3.1 405B low-resource languages' -- no Meta primary source."]))

R["SHANGHAIAILAB-2024-02-JAI1"] = dict(al="None", at="Not applicable", sc=none_log("Google", [
 "Google AI / Google DeepMind blogs reviewed for the window from 2024-02-07 -- no post referencing SALAD-Bench or the Shanghai AI Laboratory result.",
 "Next Gemini model cards / technical reports after the finding (Gemini 1.5 technical report, 2024) -- no reference to SALAD-Bench or the 88.32% -> 19.98% attack-enhanced safety-rate drop.",
 "Google DeepMind safety/responsibility pages, including the 2025 'Lessons from Defending Gemini Against Indirect Prompt Injections' paper -- adversarial-robustness work is documented but nothing references this finding.",
 "Official Google/DeepMind accounts -- no statement located.",
 "Open web search 'Google Gemini response SALAD-Bench Shanghai AI Laboratory attack-enhanced prompts' -- academic and third-party sources only, no Google primary source."]))

# ---------------------------------------------------------------- write
bak = P.replace(".xlsx", ".backup-"+time.strftime("%Y%m%d-%H%M%S")+".xlsx"); shutil.copy2(P, bak)
wb = openpyxl.load_workbook(P); ws = wb["v10 revised"]
hdr = [(c.value or "").strip() if isinstance(c.value, str) else c.value for c in ws[1]]
ix = {h: i for i, h in enumerate(hdr, 1) if h}

def g(r, name):
    v = ws.cell(r, ix[name]).value
    if isinstance(v, (datetime.datetime, datetime.date)): return v.strftime("%Y-%m-%d")
    return "" if v is None else str(v).strip()

done = []
for r in range(2, ws.max_row + 1):
    fid = g(r, "Finding ID")
    if fid not in R: continue
    d = R[fid]
    sev = g(r, "Severity (C1/C2) majority")
    assert not g(r, "Action Level"), f"{fid} already has an Action Level"
    ws.cell(r, ix["Action Level"]).value = d["al"]
    ws.cell(r, ix["Attribution"]).value  = d["at"]
    ws.cell(r, ix["Sources Checked (channel A)"]).value = d["sc"]
    lag = ""
    if d["al"] != "None":
        ws.cell(r, ix["Company Response"]).value   = d["cr"]
        ws.cell(r, ix["Channel A Verbatim"]).value = d["cv"]
        ws.cell(r, ix["Channel A Evidence"]).value = d["ce"]
        ws.cell(r, ix["Response Date"]).value      = d["rd"]
        lag = (datetime.date.fromisoformat(d["rd"]) -
               datetime.date.fromisoformat(g(r, "Publication Date")[:10])).days
        ws.cell(r, ix["Lag (days)"]).value = lag
    prop = MATRIX[(sev, d["al"])]
    ws.cell(r, ix["Proportionality"]).value = prop
    note = f"  [CHANNEL A BATTERY RUN {D}] Action Level={d['al']}; Attribution={d['at']}; see Sources Checked for the five-source log."
    ws.cell(r, ix["Notes"]).value = ((g(r, "Notes") or "") + note).strip()
    done.append((fid, sev, d["al"], d["at"], lag, prop))

wb.save(P)
print(f"backup: {os.path.basename(bak)}")
print(f"coded {len(done)} rows\n")
print(f"{'Finding':<30}{'sev':<5}{'Action Level':<15}{'Attribution':<24}{'lag':>6}  Proportionality")
for fid, sev, al, at, lag, prop in sorted(done, key=lambda x: (x[2] == "None", x[0])):
    print(f"{fid:<30}{sev:<5}{al:<15}{at:<24}{str(lag):>6}  {prop}")
