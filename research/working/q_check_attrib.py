#!/usr/bin/env python3
"""Do the 12 'No explicit attribution' rows really lack a documented link?

If a response cell quotes the company naming the evaluator, the row's Attribution value is
simply wrong and the row does not belong in the permissive bloc at all.
"""
import openpyxl, os, re, datetime

P = os.path.expanduser("~/Desktop/AISIEVAL.xlsx")
ws = openpyxl.load_workbook(P, data_only=True)[openpyxl.load_workbook(P).sheetnames[0]]
hdr = [c.value for c in ws[1]]
ix = {h: i + 1 for i, h in enumerate(hdr) if h}


def norm(v):
    if v is None:
        return ""
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime("%Y-%m-%d")
    return str(v).strip()


R = [{h: norm(ws.cell(r, ix[h]).value) for h in ix} for r in range(2, ws.max_row + 1)
     if ws.cell(r, 1).value]
tier = lambda r: ("A" if r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")
H = [r for r in R if tier(r) == "A" and r["Severity (C1/C2) majority"] == "C1"]
bloc = [r for r in H if r["Attribution"] == "No explicit attribution"
        and r["Action Level"] in ("Substantive", "Partial", "Acknowledged")]

EVAL = {"UK AISI": [r'UK AI\s?S(?:ecurity|afety) Institute', r'UK AISI'],
        "US CAISI": [r'\bCAISI\b', r'Center for AI Standards'],
        "METR": [r'\bMETR\b'], "Apollo Research": [r'Apollo'],
        "Center for AI Safety (CAIS)": [r'Center for AI Safety', r'\bCAIS\b(?!I)'],
        "FAR.AI": [r'FAR\.?AI'], "Scale AI": [r'Scale AI', r'\bSEAL\b'],
        "Cisco (Robust Intelligence / Foundation AI)": [r'Cisco', r'Robust Intelligence'],
        "Collective Intelligence Project (Weval)": [r'Collective Intelligence', r'Weval'],
        "Redwood Research": [r'Redwood'], "SecureBio": [r'SecureBio'],
        "Palisade Research": [r'Palisade'], "Transluce": [r'Transluce']}

print(f"{'Finding ID':<26} {'lag':>5} {'level':<12} evaluator named in the response cell?")
print("-" * 104)
wrong = []
for r in sorted(bloc, key=lambda r: -int(r["Lag (days)"] or 0)):
    pats = None
    for k, v in EVAL.items():
        if r["Institution"].startswith(k[:12]):
            pats = v
            break
    blob = r["Company Response"] + " " + r["Channel A Evidence"]
    hit = None
    if pats:
        for p in pats:
            m = re.search(p, blob, re.I)
            if m:
                hit = m.group(0)
                break
    flag = f"YES -> {hit!r}  ** Attribution value looks WRONG **" if hit else "no"
    if hit:
        wrong.append(r["Finding ID"])
    print(f"{r['Finding ID']:<26} {r['Lag (days)']:>5} {r['Action Level']:<12} {flag}")

print(f"\nrows whose Attribution value is contradicted by their own response cell: {len(wrong)} {wrong}")
print(f"genuine permissive bloc after correction: {len(bloc) - len(wrong)} rows")
for f in wrong:
    r = next(x for x in R if x["Finding ID"] == f)
    print(f"\n--- {f}  (attr currently {r['Attribution']!r}, lag {r['Lag (days)']})")
    print(f"    {r['Company Response'][:520]}")
