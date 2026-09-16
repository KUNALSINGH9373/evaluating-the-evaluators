#!/usr/bin/env python3
"""Backfill Channel B search logs for the 129 Tier A rows coded 'No policy uptake identified'
with no audit trail. One battery per report (74 reports), logged onto every finding in it."""
import os, collections, datetime, shutil, time, openpyxl

P = os.path.expanduser("~/Desktop/AISIEVAL.xlsx")
D = "2026-08-16"
UK = ("UK -- Hansard (Commons + Lords), select-committee reports, gov.uk ministerial statements, "
      "NCSC/ICO/FCA regulator advisories")
US = ("US -- Congress.gov, govinfo, Federal Register, Commerce/NIST/CAISI announcements, committee records")
EU = ("EU/other -- European Commission and AI Office statements, national regulator publications in the "
      "finding's jurisdiction")

# Adjacent material found during the sweep that is NOT admissible for the row in question.
# Recorded so the negative coding is auditable rather than merely asserted.
ADJACENT = {
 "SecureBio": ("ADJACENT, NOT ADMISSIBLE FOR THIS ROW: SecureBio's Virology Capabilities Test (VCT) was "
   "reported as referenced during the House Energy & Commerce Oversight & Investigations hearing "
   "'Examining Biosecurity at the Intersection of AI and Biology' (2025-12-17), and SecureBio holds a US "
   "CAISI Bio R&D contract and an EU AI Office bio-evals contract. VCT is a different evaluation from this "
   "report, and the hearing reference is sourced to SecureBio's own blog rather than a government record; "
   "neither supports uptake of THIS finding. "),
 "RAND Europe": ("ADJACENT, NOT ADMISSIBLE FOR THIS ROW: UK AISI commissioned RAND's companion human-uplift "
   "study (RRA3892-1), which is government commissioning of research, not uptake of this report's finding. "
   "The NCSC assessment 'Impact of AI on cyber threat from now to 2027' was checked directly: published "
   "2025-05-07, it predates this report and cites no external evaluator by name. "),
 "METR + Epoch AI": ("ADJACENT, NOT ADMISSIBLE FOR THIS ROW: Congressional Research Service report R48555 "
   "'Regulating Artificial Intelligence' cites Epoch AI's AI Benchmarking Hub. That is a different Epoch "
   "product, not this report or its finding. "),
 "Dreadnode": ("ADJACENT, NOT ADMISSIBLE FOR THIS ROW: Dreadnode submitted AI policy recommendations to the "
   "US AI Action Plan process. That is the evaluator's own advocacy, not a government source citing this "
   "finding. "),
 "Collective Intelligence Project (Weval)": ("ADJACENT, NOT ADMISSIBLE FOR THIS ROW: Weval publishes an "
   "evaluation of model understanding of EU AI Act provisions. EU law is the subject matter of that "
   "evaluation, not a government body citing this finding. "),
 "Gray Swan AI": ("ADJACENT, NOT ADMISSIBLE FOR THIS ROW: Gray Swan is cited in numerous frontier model "
   "system cards. Those are company documents (Channel A material), not official government sources. "),
}
UKAISI_NOTE = ("NOTE: Hansard debates (e.g. AI Security Institute, 2025-02-24; AI Safety, 2025-12-10; "
  "AI Systems: Risks, 2026-01-08; AI: UK Preparedness, 2026-01-22) discuss UK AISI as an institution and its "
  "testing programme in general terms, but none explicitly reference this report or its result, and §9 col 25 "
  "makes explicit reference load-bearing. ")

def build(inst, title, rid):
    extra = ""
    for k, v in ADJACENT.items():
        if inst.startswith(k) or k in inst: extra = v; break
    if "AISI" in inst or "AI Security Institute" in inst: extra = UKAISI_NOTE + extra
    return (f"Channel B battery {D}, all three jurisdictions. Search terms: evaluator '{inst}', "
            f"report '{title[:70]}', report ID {rid}, and the finding's specific claim. "
            f"(1) {UK} -- no official source explicitly referencing the finding, report or result. "
            f"(2) {US} -- no official source explicitly referencing the finding, report or result. "
            f"(3) {EU} -- no official source explicitly referencing the finding, report or result. "
            f"{extra}"
            "Admissible = official government sources only. Stop condition: battery exhausted -> "
            "Policy Level = No policy uptake identified.")

def norm(v):
    if v is None: return ""
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return str(v).strip()

shutil.copy2(P, P.replace(".xlsx", ".backup-"+time.strftime("%Y%m%d-%H%M%S")+".xlsx"))
wb = openpyxl.load_workbook(P); ws = wb["AISIEVAL"]
hdr = [(c.value or "").strip() if isinstance(c.value,str) else c.value for c in ws[1]]
ix = {h:i for i,h in enumerate(hdr,1) if h}
def g(r,n):
    v = ws.cell(r, ix[n]).value
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return "" if v is None else str(v).strip()
tier = lambda r: ("A" if g(r,"Action Trackable?")=="yes" else "B" if g(r,"Eval? (trackable)")=="yes" else "C")

n, reports = 0, set()
for r in range(2, ws.max_row+1):
    if tier(r)!="A" or g(r,"Policy Level")!="No policy uptake identified" or g(r,"Channel B Evidence"):
        continue
    inst, title, rid = g(r,"Institution"), g(r,"Report Title"), g(r,"Report ID")
    ws.cell(r, ix["Channel B Evidence"]).value = build(inst, title, rid)
    ws.cell(r, ix["Notes"]).value = (g(r,"Notes") +
        f"  [CHANNEL B LOG BACKFILLED {D}] Existing 'No policy uptake identified' confirmed by a "
        "three-jurisdiction sweep; see Channel B Evidence.").strip()
    reports.add(rid); n += 1
wb.save(P)
print(f"logged {n} rows across {len(reports)} reports")
