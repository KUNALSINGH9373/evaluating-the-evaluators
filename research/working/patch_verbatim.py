#!/usr/bin/env python3
"""Finish the specificity reclassification: Channel A Verbatim was missed.

The coherence invariant is 'response fields filled <-> level != None', and Channel A Verbatim
counts. Preserve it losslessly (Notes + the sensitivity CSV, which is rewritten with the extra
column) before clearing.
"""
import openpyxl, os, shutil, time, csv, collections, datetime

P = os.path.expanduser("~/Desktop/AISIEVAL.xlsx")
CSV = os.path.expanduser("~/Documents/AISIEVAL_sensitivity_general_response.csv")
D = "2026-08-17"
IDS = ["CAIS-2023-07-JAI1", "CAIS-2023-07-JAI3", "APOLLO-2023-11-ALI1", "SCALEAI-2024-10-JAI1",
       "SCALEAI-2025-02b-JAI3", "CISCO-2024-07-JAI1", "CIP-2025-08-ALI1", "FARAI-2024-08-JAI1",
       "FARAI-2024-10-ALI1", "FARAI-2024-10-JAI1", "FARAI-2025-02a-JAI2"]

shutil.copy2(P, P.replace(".xlsx", f".backup-{time.strftime('%Y%m%d-%H%M%S')}.xlsx"))
wb = openpyxl.load_workbook(P)
ws = wb[wb.sheetnames[0]]
hdr = [c.value for c in ws[1]]
ix = {h: i + 1 for i, h in enumerate(hdr) if h}


def norm(v):
    if v is None:
        return ""
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime("%Y-%m-%d")
    return str(v).strip()


verb = {}
for r in range(2, ws.max_row + 1):
    fid = ws.cell(r, 1).value
    if fid not in IDS:
        continue
    v = norm(ws.cell(r, ix["Channel A Verbatim"]).value)
    verb[fid] = v
    if v:
        nt = ws.cell(r, ix["Notes"]).value or ""
        ws.cell(r, ix["Notes"]).value = (
            nt + f"\n\n[SPECIFICITY RULE — FIELD PRESERVED {D}] Channel A Verbatim cleared to hold the "
                 f"coherence invariant (response fields filled <-> Action Level != None). PRIOR VALUE: {v!r}").strip()
    ws.cell(r, ix["Channel A Verbatim"]).value = None
wb.save(P)
print(f"cleared Channel A Verbatim on {sum(1 for v in verb.values() if v)} of {len(verb)} rows")

# rewrite the sensitivity CSV with the extra column so it stays lossless
rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
fn = list(rows[0].keys())
if "Channel A Verbatim" not in fn:
    fn.append("Channel A Verbatim")
for d in rows:
    d["Channel A Verbatim"] = verb.get(d["Finding ID"], "")
with open(CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fn)
    w.writeheader()
    w.writerows(rows)
print(f"sensitivity CSV rewritten with Channel A Verbatim: {CSV}")
tot = sum(len(str(v)) for d in rows for v in d.values())
print(f"  {len(rows)} rows · {len(fn)} columns · {tot:,} chars preserved")
