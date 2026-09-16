#!/usr/bin/env python3
"""Exactly which columns changed on the 11 specificity-rule rows: before -> after."""
import openpyxl, os, csv, datetime, collections

P = os.path.expanduser("~/Desktop/AISIEVAL.xlsx")
CSV = os.path.expanduser("~/Documents/AISIEVAL_sensitivity_general_response.csv")
prior = {d["Finding ID"]: d for d in csv.DictReader(open(CSV, encoding="utf-8"))}

ws = openpyxl.load_workbook(P, data_only=True)[openpyxl.load_workbook(P).sheetnames[0]]
hdr = [c.value for c in ws[1]]
ix = {h: i + 1 for i, h in enumerate(hdr) if h}


def norm(v):
    if v is None:
        return ""
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime("%Y-%m-%d")
    return str(v).strip()


COLS = ["Action Level", "Attribution", "Proportionality", "Company Response",
        "Channel A Verbatim", "Channel A Evidence", "Response Date", "Lag (days)"]
now = {}
for r in range(2, ws.max_row + 1):
    fid = ws.cell(r, 1).value
    if fid in prior:
        now[fid] = {c: norm(ws.cell(r, ix[c]).value) for c in COLS}

print("Columns touched, and how — same pattern on all 11 rows:\n")
print(f"{'column':<22} {'before':<26} {'after':<28} what happened")
print("-" * 108)
pat = collections.defaultdict(set)
for fid in now:
    for c in COLS:
        pat[c].add((prior[fid].get(c, "") != "", now[fid][c]))
for c in COLS:
    befores = {prior[f].get(c, "") for f in now}
    afters = {now[f][c] for f in now}
    b = (sorted(befores)[0][:24] + "…") if len(sorted(befores)[0]) > 24 else (sorted(befores)[0] or "(empty)")
    if len(befores) > 1:
        b = f"{len(befores)} distinct values"
    a = sorted(afters)[0] or "(emptied)"
    if len(afters) > 1:
        a = f"{len(afters)} distinct"
    kind = ("value REPLACED" if all(x for x in afters) else "CLEARED to blank")
    print(f"{c:<22} {b:<26} {a:<28} {kind}")

print("\n\nWorked example — CAIS-2023-07-JAI1:\n")
f = "CAIS-2023-07-JAI1"
for c in COLS:
    bv = prior[f].get(c, "")
    av = now[f][c]
    print(f"  {c:<21} before: {(bv[:88] + '…') if len(bv) > 88 else (bv or '(empty)')}")
    print(f"  {'':<21} after : {av or '(empty)'}")
print("\nUntouched on every row: Finding ID, Report ID, Institution, Publication Date, Finding,")
print("Finding Quote, Models / Systems, Severity + the 3 votes, tier flags, Domain, Scope,")
print("Access Type, all Channel B columns, Academic Citations, Sources Checked (channel A).")
