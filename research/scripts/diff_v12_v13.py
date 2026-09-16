#!/usr/bin/env python3
"""Cell-by-cell diff: every V12 row against its V13 counterpart.

V12 is the frozen baseline. Any V12 cell that differs in V13 must correspond to a deliberate,
documented change; anything else is silent damage. Nothing is modified here.
"""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds
import openpyxl

V12P = "/Users/kunalsingh/evaluating-the-evaluators/AISI  Eval Findings.xlsx"
wb = openpyxl.load_workbook(V12P, data_only=True, read_only=True)
ws = wb["AISIEVAL_V12"]
rows = list(ws.iter_rows(values_only=True))
hdr = [str(c).strip() if c is not None else "" for c in rows[0]]
COLS = [c for c in hdr if c]
i_id = hdr.index("Finding ID")

def n(v):
    import datetime
    if v is None: return ""
    if isinstance(v, (datetime.datetime, datetime.date)): return v.strftime("%Y-%m-%d")
    if isinstance(v, float) and v.is_integer(): return str(int(v))
    return str(v).strip()

V12 = {}
for r in rows[1:]:
    if not r[i_id]: continue
    V12[n(r[i_id])] = {h: n(r[hdr.index(h)]) for h in COLS}

V13 = {r["Finding ID"]: r for r in ds.rows()}

missing = [k for k in V12 if k not in V13]
added   = [k for k in V13 if k not in V12]
print(f"V12 rows {len(V12)} · V13 rows {len(V13)}")
print(f"V12 rows MISSING from V13 : {len(missing)}  {missing[:5]}")
print(f"rows added in V13         : {len(added)}")

changed = collections.defaultdict(list)
per_row = collections.Counter()
for fid, a in V12.items():
    b = V13.get(fid)
    if not b: continue
    for c in COLS:
        if a[c] != (b.get(c) or ""):
            changed[c].append((fid, a[c], b.get(c) or ""))
            per_row[fid] += 1

tot = sum(len(v) for v in changed.values())
print(f"\nCELLS CHANGED on pre-existing V12 rows: {tot}  across {len(per_row)} rows, {len(changed)} columns\n")
for c in COLS:
    if c in changed:
        print(f"  [{len(changed[c]):>4}]  {c}")
json.dump({c: [{"finding_id": f, "v12": o, "v13": nv} for f, o, nv in v] for c, v in changed.items()},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs/diff_v12_v13.json"), "w"),
          indent=1)
print("\ndetail -> logs/diff_v12_v13.json")
