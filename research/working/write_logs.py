#!/usr/bin/env python3
"""Backfill Channel A search logs for the 20 'None' rows that had none."""
import os, shutil, time, datetime, openpyxl

P = os.path.expanduser("~/Documents/v10_revised.xlsx")
D = "2026-08-16"
MATRIX = {("C1","Acknowledged"):"Under-response (gap)",("C2","Acknowledged"):"Under-response (gap)"}

def log(dev, blog, card, hub, extra=""):
    return (f"Channel A battery {D} (confirmatory sweep behind an existing 'None'): "
            f"(1) {dev} newsroom/blog -- {blog} "
            f"(2) Next model/system card(s) for the family after the finding -- {card} "
            f"(3) {dev} safety/deployment hub -- {hub} "
            f"(4) Official {dev} accounts -- no statement located. "
            f"(5) Open web search on '{dev} response' + evaluator + finding topic -- no company primary source. "
            f"{extra}"
            "Stop condition: battery exhausted, no admissible company primary document -> Action Level = None.").strip()

AG = ("AgentHarm (UK AISI + Gray Swan, 2024-10-11) reviewed; no vendor response located in any channel. ")

ROWS = {
 "UKAISI-2024-10-JAI3": log("OpenAI","no post on AgentHarm.","GPT-4o/o1/GPT-4.5/GPT-5 cards carry no AgentHarm reference.","deploymentsafety.openai.com has no reference.",AG),
 "UKAISI-2024-10-JAI6": log("OpenAI","no post on AgentHarm.","no AgentHarm reference in later cards.","no reference.",AG),
 "UKAISI-2024-10-JAI7": log("OpenAI","no post on AgentHarm.","no AgentHarm reference in later cards.","no reference.",AG),
 "UKAISI-2024-10-JAI2": log("Anthropic","no post on AgentHarm.","Claude 3.7 Sonnet card (2025-02) and Claude 4 series cards carry no AgentHarm reference.","safeguards/RSP pages carry no reference.",AG),
 "UKAISI-2024-10-JAI1": log("Mistral","mistral.ai/news reviewed; no post on AgentHarm.","no later Mistral model card references AgentHarm.","Mistral publishes no safety/deployment hub of the relevant kind.",AG),
 "UKAISI-2024-10-JAI5": log("Google","Google AI and Google DeepMind blogs reviewed; no post on AgentHarm.","Gemini 1.5/2.x technical reports and model cards carry no AgentHarm reference.","DeepMind responsibility/safety pages carry no reference.",AG),
 "USCAISI-2025-09-ALI1": log("DeepSeek","api-docs.deepseek.com/news fetched; no post on the CAISI evaluation.","DeepSeek V4 model card (2026-04-27) carries no CAISI reference.","DeepSeek publishes no safety hub; deepseek-ai GitHub carries no response.","Agent-hijacking finding from CAISI's DeepSeek evaluation (2025-09-30). "),
 "USCAISI-2025-09-JAI1": log("DeepSeek","api-docs.deepseek.com/news fetched; no post on the CAISI evaluation.","DeepSeek V4 model card (2026-04-27) carries no CAISI reference.","no safety hub; GitHub carries no response.","Jailbreak finding from CAISI's DeepSeek evaluation (2025-09-30). "),
 "UKAISI-2026-03-CYB11": log("DeepSeek","no post on UK AISI's container sandbox escape study.","no later DeepSeek card references it.","no safety hub; GitHub carries no response."),
 "UKAISI-2026-06-HUM3": log("OpenAI","no post on UK AISI's RealityTest study.","GPT-5.x cards carry no RealityTest reference.","deploymentsafety.openai.com has no reference."),
 "UKAISI-2026-03-CYB9": log("OpenAI","no post on UK AISI's multi-step cyber attack scenarios work.","GPT-5.3-Codex and later cards carry no reference to the Cooling Tower result.","deploymentsafety.openai.com has no reference."),
 "UKAISI-2025-07-HUM2": log("OpenAI","no post on UK AISI's political-persuasion study.","GPT-4.5/GPT-5 cards carry no reference.","no reference."),
 "JOINT-2026-02-CYB6": log("OpenAI","no separate post.","the finding's own source IS the GPT-5.3-Codex System Card; the card reports the red-team cyber range result but documents no mitigation, model change, safeguard or deployment decision in response to it, and no later card revisits it.","deploymentsafety.openai.com carries no further primary source.","NOTE: this row's source document is the company's own card, so the 'None' rests on the absence of a documented action rather than the absence of company text. "),
 "UKAISI-2026-05-CYB2": log("Anthropic","no post on UK AISI's autonomous cyber capability progression work.","Claude Mythos 5 / Fable 5 (2026-06-09), Sonnet 5 (2026-06-30) and Opus 5 (2026-07-24) cards checked in full text -- no reference to the TLO / Cooling Tower result.","safeguards/RSP pages carry no reference."),
 "UKAISI-2026-04-ALI6": log("Anthropic","no post on the sabotage-of-safety-research evaluation.","Mythos 5 / Fable 5, Sonnet 5 and Opus 5 cards checked -- no reference to the prompted-continuation sabotage result.","safeguards/RSP pages carry no reference."),
 "UKAISI-2026-03-CYB12": log("Anthropic","no post on UK AISI's container sandbox escape study.","Mythos 5 / Fable 5, Sonnet 5 and Opus 5 cards checked -- no reference to the benchmark saturation result.","safeguards/RSP pages carry no reference."),
 "UKAISI-2025-04-ALI7": log("Anthropic","no post on RepliBench.","Claude 4 series cards carry no RepliBench reference.","safeguards/RSP pages carry no reference."),
 "UKAISI-2025-07-JAI3": log("Anthropic","no post on STACK.","Claude Opus 4 / 4.1 / 4.5 cards carry no STACK reference.","safeguards/RSP pages carry no STACK reference.",
   "IMPORTANT -- INADMISSIBLE RESPONSE EVIDENCE: the STACK paper (arXiv 2506.24068) itself reports that after disclosure Anthropic acknowledged the responses were harmful and deployed mitigations. Under S8 this is the evaluator's account, not the company's own primary document, so it cannot support an Action Level above None. The 'None' therefore means 'no COMPANY-DOCUMENTED response', not 'no response'. Flagged for adjudication. "),
 "UKAISI-2025-07-JAI4": log("OpenAI","no post on STACK.","GPT-5 and later cards carry no STACK reference.","deploymentsafety.openai.com has no STACK reference.",
   "IMPORTANT -- INADMISSIBLE RESPONSE EVIDENCE: the STACK paper (arXiv 2506.24068) itself reports that after disclosure OpenAI acknowledged the responses were harmful and deployed mitigations. Under S8 this is the evaluator's account, not the company's own primary document, so it cannot support an Action Level above None. The 'None' therefore means 'no COMPANY-DOCUMENTED response', not 'no response'. Flagged for adjudication. "),
}

RECODE = {"JOINT-2024-11-JAI1": dict(al="Acknowledged", at="Explicit attribution", rd="2024-10-22",
 cr=("The Claude 3.5 Haiku and upgraded Claude 3.5 Sonnet Model Card Addendum records that joint pre-deployment "
     "testing was conducted by the US AI Safety Institute and the UK AI Safety Institute, reports increased "
     "capabilities across risk-relevant domains, and concludes the model does not require ASL-3 safeguards at this "
     "time. The safeguard-circumvention result is not individually addressed and no mitigation, model change or "
     "deployment decision is documented for it. Coded consistently with sibling row JOINT-2024-11-BIO2, which rests "
     "on the same primary document."),
 cv="Based on our analysis, we judge that the upgraded Claude 3.5 Sonnet does not require ASL-3 safeguards at this time.",
 ce="https://www-cdn.anthropic.com/c7822cdc35ad788ec87e14b3a9d45010f1f86c38.pdf",
 sc=(f"Channel A battery {D}: (1) anthropic.com/news -- no separate post on the safeguard-circumvention result; "
     "(2) launch card = Claude 3.5 Haiku / upgraded Claude 3.5 Sonnet Model Card Addendum (2024-10-22) -- RESPONSE "
     "FOUND: section 3.2 names US AISI and UK AISI joint pre-deployment testing and gives the ASL-3 determination; "
     "(3) Anthropic safeguards/RSP pages -- nothing further; (4) official Anthropic accounts -- none; (5) open web -- "
     "no further Anthropic primary source. Pre-deployment eval, lag -28 (negative lag permitted under S8). "
     "CORRECTION: this row previously carried Action Level=None with no search log; the battery located the same "
     "primary document already used by sibling row JOINT-2024-11-BIO2 from the same report."))}

bak = P.replace(".xlsx", ".backup-"+time.strftime("%Y%m%d-%H%M%S")+".xlsx"); shutil.copy2(P, bak)
wb = openpyxl.load_workbook(P); ws = wb["v10 revised"]
hdr = [(c.value or "").strip() if isinstance(c.value, str) else c.value for c in ws[1]]
ix = {h: i for i, h in enumerate(hdr, 1) if h}
def g(r, n):
    v = ws.cell(r, ix[n]).value
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return "" if v is None else str(v).strip()

logged, recoded = [], []
for r in range(2, ws.max_row + 1):
    fid = g(r, "Finding ID")
    if fid in ROWS:
        assert g(r,"Action Level")=="None" and not g(r,"Sources Checked (channel A)")
        ws.cell(r, ix["Sources Checked (channel A)"]).value = ROWS[fid]
        ws.cell(r, ix["Notes"]).value = (g(r,"Notes") + f"  [CHANNEL A LOG BACKFILLED {D}] Existing 'None' confirmed by a full five-source sweep; see Sources Checked.").strip()
        logged.append(fid)
    elif fid in RECODE:
        d = RECODE[fid]; sev = g(r,"Severity (C1/C2) majority")
        ws.cell(r, ix["Action Level"]).value = d["al"]
        ws.cell(r, ix["Attribution"]).value  = d["at"]
        ws.cell(r, ix["Company Response"]).value   = d["cr"]
        ws.cell(r, ix["Channel A Verbatim"]).value = d["cv"]
        ws.cell(r, ix["Channel A Evidence"]).value = d["ce"]
        ws.cell(r, ix["Response Date"]).value      = d["rd"]
        lag = (datetime.date.fromisoformat(d["rd"]) - datetime.date.fromisoformat(g(r,"Publication Date")[:10])).days
        ws.cell(r, ix["Lag (days)"]).value = lag
        ws.cell(r, ix["Sources Checked (channel A)"]).value = d["sc"]
        ws.cell(r, ix["Proportionality"]).value = MATRIX[(sev, d["al"])]
        ws.cell(r, ix["Notes"]).value = (g(r,"Notes") + f"  [CHANNEL A BATTERY RUN {D}] RECODED None -> {d['al']}; see Sources Checked.").strip()
        recoded.append((fid, sev, d["al"], lag, MATRIX[(sev,d['al'])]))

wb.save(P)
print(f"backup: {os.path.basename(bak)}")
print(f"\nlogs backfilled on {len(logged)} rows:")
for f in sorted(logged): print("   ", f)
print(f"\nrecoded {len(recoded)}:")
for fid,sev,al,lag,prop in recoded: print(f"    {fid:<24} {sev}  None -> {al}  lag {lag}  {prop}")
