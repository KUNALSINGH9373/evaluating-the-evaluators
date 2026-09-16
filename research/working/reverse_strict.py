#!/usr/bin/env python3
"""Reverse the bulk specificity reclassification; re-adjudicate the 11 rows individually.

WHY REVERSED: col 17 measures the CONTENT of the documented response and expressly does not
establish causation, and it lists "access restriction" among qualifying actions. Requiring the
company to have linked the action to the finding is col 18's test, not col 17's -- these rows
already carry "No explicit attribution", so downgrading Action Level too was counting the same
absence twice.

WHAT SURVIVES: a genuine distinction between an action landing on the MODEL TESTED versus on
SUCCESSOR systems only. The latter addresses part of the identified problem, which is col 17's
Partial branch. Three rows therefore step down from Substantive to Partial on their merits.
"""
import openpyxl, os, shutil, time, csv, collections, datetime

P = os.path.expanduser("~/Desktop/AISIEVAL.xlsx")
CSV = os.path.expanduser("~/Documents/AISIEVAL_sensitivity_general_response.csv")
D = "2026-08-17"
MATRIX = {("C1", "Substantive"): "Proportionate", ("C1", "Partial"): "Under-response (gap)",
          ("C1", "Acknowledged"): "Under-response (gap)", ("C1", "None"): "Accountability gap (no action)",
          ("C2", "Substantive"): "Proportionate", ("C2", "Partial"): "Proportionate",
          ("C2", "Acknowledged"): "Under-response (gap)", ("C2", "None"): "Accountability gap (no action)"}

# level -> (restored Action Level, rationale for the level chosen)
LEVEL = {
 "CISCO-2024-07-JAI1": ("Substantive",
   "Prompt Guard 2 86M is the successor to the very classifier the finding broke, and Meta describes it as "
   "\"an update to our Llama Prompt Guard classifier model\" that \"improves on its performance in jailbreak and "
   "prompt injection detection\". Same component, same failure mode -> a mitigation that directly addressed the "
   "identified problem."),
 "CIP-2025-08-ALI1": ("Substantive",
   "Same model and same behaviour as the finding, 68 days later, with a measured 65-80% reduction in non-ideal "
   "responses and two new evaluation sets created for the exact categories. Directly addressed."),
 "SCALEAI-2024-10-JAI1": ("Substantive",
   "The finding is that GPT-4o-based browser agents pursue harmful behaviours their backbone refuses in chat; "
   "OpenAI shipped a GPT-4o browser agent with \"proactive refusals of high-risk tasks, confirmation prompts "
   "before critical actions, and active monitoring\". Same surface, same behaviour class -> directly addressed."),
 "CAIS-2023-07-JAI1": ("Partial",
   "STEPPED DOWN from Substantive. Deliberative alignment documents improved resistance to malicious jailbreak "
   "prompts, which is the identified problem class, but it was applied to o-series successors rather than the "
   "tested GPT-3.5 and GPT-4. Col 17 Partial: addressed only part of the identified problem."),
 "SCALEAI-2025-02b-JAI3": ("Partial",
   "STEPPED DOWN from Substantive. Safety Reasoner is deployed and described as \"a core component of our safety "
   "stack\", addressing jailbreak-elicited unsafe outputs, but across successor systems -- the tested GPT-4o's "
   "vulnerability is not itself fixed. Col 17 Partial."),
 "APOLLO-2023-11-ALI1": ("Partial",
   "STEPPED DOWN from Substantive. OpenAI does \"fully restrict the model from assisting with certain tasks, such "
   "as selling or purchasing stocks\", which removes the scenario the finding used, but the identified problem is "
   "strategic deception and concealment, which the restriction does not address. Col 17 Partial: addressed only "
   "part of the identified problem."),
 "CAIS-2023-07-JAI3": ("Partial",
   "Unchanged at Partial. Constitutional Classifiers targets universal jailbreaks, the right problem, but is "
   "expressly a prototype intended for possible future deployment -- col 17's 'expressly described as interim' branch."),
 "FARAI-2024-08-JAI1": ("Partial", "Unchanged at Partial. The fine-tuning wind-down is an access restriction, which col 17 lists as a qualifying action, and it removes the surface the finding exploited. Partial because it is phased and inference on already fine-tuned models continues. Motive is not col 17's test; that the notice states a capability rather than safety rationale, and never cites the evaluator, is recorded in col 18 as No explicit attribution."),
 "FARAI-2024-10-ALI1": ("Partial", "Unchanged at Partial. Same wind-down and same reasoning as FARAI-2024-08-JAI1."),
 "FARAI-2024-10-JAI1": ("Partial", "Unchanged at Partial. Same wind-down and same reasoning as FARAI-2024-08-JAI1."),
 "FARAI-2025-02a-JAI2": ("Partial", "Unchanged at Partial. Same wind-down and same reasoning as FARAI-2024-08-JAI1."),
}
prior = {d["Finding ID"]: d for d in csv.DictReader(open(CSV, encoding="utf-8"))}
assert set(prior) == set(LEVEL), set(prior) ^ set(LEVEL)

shutil.copy2(P, P.replace(".xlsx", f".backup-{time.strftime('%Y%m%d-%H%M%S')}.xlsx"))
wb = openpyxl.load_workbook(P)
ws = wb[wb.sheetnames[0]]
hdr = [c.value for c in ws[1]]
ix = {h: i + 1 for i, h in enumerate(hdr) if h}

REST = ["Company Response", "Channel A Verbatim", "Channel A Evidence", "Response Date", "Lag (days)"]
log = []
for r in range(2, ws.max_row + 1):
    fid = ws.cell(r, 1).value
    if fid not in LEVEL:
        continue
    d = prior[fid]
    lvl, why = LEVEL[fid]
    sev = str(ws.cell(r, ix["Severity (C1/C2) majority"]).value or "")
    for c in REST:                                   # restore the cleared evidence verbatim
        v = d.get(c, "")
        ws.cell(r, ix[c]).value = (int(v) if c == "Lag (days)" and v.lstrip("-").isdigit() else (v or None))
    ws.cell(r, ix["Action Level"]).value = lvl
    ws.cell(r, ix["Attribution"]).value = "No explicit attribution"
    ws.cell(r, ix["Proportionality"]).value = MATRIX[(sev, lvl)]
    note = (f"[SPECIFICITY RULE REVERSED {D}] The bulk reclassification to None is WITHDRAWN and the cleared "
            f"evidence restored verbatim. Reason: col 17 measures the CONTENT of the documented response, expressly "
            f"does not establish causation, and lists access restriction among qualifying actions -- so requiring "
            f"the company to have linked its action to the finding was col 18's test applied a second time. These "
            f"rows already carry No explicit attribution, which is where that absence belongs. Re-adjudicated "
            f"individually: Action Level = {lvl}. {why} Prior-to-reversal state: None / Accountability gap (no "
            f"action) / No response located, applied {D} and withdrawn the same day.")
    nt = ws.cell(r, ix["Notes"]).value or ""
    ws.cell(r, ix["Notes"]).value = (nt + "\n\n" + note).strip()
    log.append((fid, d["Action Level"], lvl, MATRIX[(sev, lvl)]))
wb.save(P)
print(f"{'Finding ID':<24} {'was (pre-rule)':<13} {'now':<13} outcome")
print("-" * 88)
for fid, was, now, out in sorted(log, key=lambda x: (x[2], x[0])):
    mark = "  <- stepped down" if was == "Substantive" and now == "Partial" else ""
    print(f"{fid:<24} {was:<13} {now:<13} {out}{mark}")


def norm(v):
    if v is None:
        return ""
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime("%Y-%m-%d")
    return str(v).strip()


ws2 = openpyxl.load_workbook(P, data_only=True)[wb.sheetnames[0]]
R = [{h: norm(ws2.cell(r, ix[h]).value) for h in ix} for r in range(2, ws2.max_row + 1) if ws2.cell(r, 1).value]
tier = lambda r: ("A" if r["Action Trackable?"] == "yes" else "B" if r["Eval? (trackable)"] == "yes" else "C")
A = [r for r in R if tier(r) == "A"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]
c = collections.Counter(r["Proportionality"] for r in H)
gap, und, n = c["Accountability gap (no action)"], c["Under-response (gap)"], len(H)
print(f"\nC1 headline n={n}")
print(f"  gap          {gap}/{n} = {gap/n:.1%}")
print(f"  falls short  {gap+und}/{n} = {(gap+und)/n:.1%}")
print(f"  outcomes     {dict(c.most_common())}")
print("  action level:", dict(collections.Counter(r["Action Level"] for r in A).most_common()))
