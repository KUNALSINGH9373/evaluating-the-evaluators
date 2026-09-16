#!/usr/bin/env python3
"""Merge v10 revised + v11 final into AISIEVAL.xlsx — one sheet, tier-major, date-descending.

Nothing is dropped and nothing is silently rewritten. The single value change is the
Policy Level spelling, which is unambiguous: §9 col 25 names exactly three values and
v10 already carries the canonical one. Every other inconsistency is preserved as-is and
recorded in that row's Notes with a [MERGE …] tag, so it stays findable in the file.
"""
import os, collections, datetime, shutil, time, openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

V10 = os.path.expanduser("~/Documents/v10_revised.xlsx")
V11 = os.path.expanduser("~/Desktop/v11_FINAL.xlsx")
OUT = os.path.expanduser("~/Desktop/AISIEVAL.xlsx")
SHEET, PROV, D = "AISIEVAL", "Source Dataset", "2026-08-16"

MATRIX = {("C1","Substantive"):"Proportionate",("C1","Partial"):"Under-response (gap)",
          ("C1","Acknowledged"):"Under-response (gap)",("C1","None"):"Accountability gap (no action)",
          ("C2","Substantive"):"Proportionate",("C2","Partial"):"Proportionate",
          ("C2","Acknowledged"):"Under-response (gap)",("C2","None"):"Accountability gap (no action)"}
TIER_FILL = {"A":"FFFDECEC","B":"FFFFF8E1","C":"FFEFF6FF"}

def norm(v):
    if v is None: return ""
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return str(v).strip()

def load(p):
    ws = openpyxl.load_workbook(p, data_only=True)[openpyxl.load_workbook(p).sheetnames[0]]
    hdr = [norm(c.value) for c in ws[1]]
    rows = [{h: norm(ws.cell(r,i).value) for i,h in enumerate(hdr,1) if h}
            for r in range(2, ws.max_row+1)]
    return [h for h in hdr if h], [r for r in rows if r.get("Finding ID")]

h10, r10 = load(V10)
h11, r11 = load(V11)
assert h10 == h11, "schema drift between the two halves"
cols = list(h10) + [PROV]
for r in r10: r[PROV] = "v10 revised"
for r in r11: r[PROV] = "v11 final"
print(f"v10 revised {len(r10)} rows · v11 final {len(r11)} rows · {len(h10)} shared columns")

tier = lambda r: ("A" if r.get("Action Trackable?")=="yes"
                  else "B" if r.get("Eval? (trackable)")=="yes" else "C")

# --- 1. Finding ID is the merge key; a collision would need adjudication, not a rule ----
ids = collections.Counter(r["Finding ID"] for r in r10 + r11)
dup = [k for k,v in ids.items() if v > 1]
print(f"merge key · {len(ids)} unique Finding IDs · collisions {dup or 'none'}")
assert not dup, f"Finding ID collisions require adjudication: {dup}"

merged = r10 + r11

# --- 2. the one unambiguous normalisation -------------------------------------------
fixed = []
for r in merged:
    if r.get("Policy Level") == "Non-binding policy-related uptake":
        r["Policy Level"] = "Non-binding policy uptake"
        r["Notes"] = (r.get("Notes","") + f"  [MERGE {D}] Policy Level normalised "
                      "'Non-binding policy-related uptake' -> 'Non-binding policy uptake' (§9 col 25 "
                      "names exactly three values; v10 already carried the canonical spelling).").strip()
        fixed.append(r["Finding ID"])
print(f"normalised · Policy Level spelling on {len(fixed)} rows ({r10[0][PROV] if False else 'all v11'})")

# --- 3. inconsistencies preserved, flagged in-row ------------------------------------
DOMAIN_OK = {"Alignment","Autonomy","Bio-Chem","Cyber","Jailbreaks","Societal","Institutional",
  "Human Influence","Eval-methodology","Eval-tooling","Frontier-forecasting","Policy/Standards",
  "Transparency/Disclosure","International-coordination"}
flags = collections.Counter()

for r in merged:
    parts = [p.strip() for p in r.get("Domain","").split(";") if p.strip()]
    off = [p for p in parts if p not in DOMAIN_OK]
    if off:
        r["Notes"] = (r.get("Notes","") + f"  [MERGE {D}] UNRESOLVED: Domain value(s) "
                      f"{off} are outside the controlled vocabulary. Preserved verbatim; needs a "
                      "coding decision (map to an existing domain, or extend the registry).").strip()
        flags["Domain out-of-vocabulary"] += 1

    if r.get("Institution") == "UK AISI" and (r.get("Institution Type") != "Government"
                                              or r.get("Scope") != "government-AISI"):
        r["Notes"] = (r.get("Notes","") + f"  [MERGE {D}] UNRESOLVED: Institution is 'UK AISI' but "
                      f"Institution Type={r.get('Institution Type')!r} / Scope={r.get('Scope')!r}; UK AISI is "
                      "Government / government-AISI elsewhere in the corpus. Either the Institution cell names "
                      "the wrong evaluator for this row or the Type/Scope cells do. Preserved verbatim.").strip()
        flags["UK AISI typed inconsistently"] += 1

    if "Holistic Agent Leaderboard" in r.get("Institution","") and r.get("Scope") != "third-party-evaluator":
        r["Notes"] = (r.get("Notes","") + f"  [MERGE {D}] UNRESOLVED: Princeton HAL carries "
                      f"Scope={r.get('Scope')!r}; it is an academic third-party evaluator, not a government "
                      "AISI. Preserved verbatim.").strip()
        flags["Princeton HAL scope"] += 1

    if r.get("Report ID") == "SCALEAI-2025-06":
        r["Notes"] = (r.get("Notes","") + f"  [MERGE {D}] UNRESOLVED: Report ID collision — "
                      "SCALEAI-2025-06 is used by two different reports across the halves (v10 'FORTRESS', "
                      "arxiv.org/abs/2506.14922, 2025-06-17; v11 'Agent-RLVR', labs.scale.com/papers/agent_rlvr, "
                      "2025-06-13). §6 requires one Report ID per report; add a slug to disambiguate. "
                      "Preserved verbatim.").strip()
        flags["Report ID collision SCALEAI-2025-06"] += 1

    if tier(r) == "A" and r.get("Policy Level") == "No policy uptake identified" and not r.get("Channel B Evidence"):
        flags["Tier A 'No policy uptake' with no Channel B log"] += 1

print("preserved-and-flagged:")
for k,v in flags.most_common(): print(f"    {v:>4}  {k}")

# --- 4. Proportionality is derived; recompute as a consistency check ------------------
changed = []
for r in merged:
    if tier(r) == "A" and r.get("Action Level"):
        want = MATRIX.get((r.get("Severity (C1/C2) majority"), r["Action Level"]))
        if want and r.get("Proportionality") != want:
            changed.append((r["Finding ID"], r.get("Proportionality"), want)); r["Proportionality"] = want
print(f"proportionality · recomputed from the matrix · {len(changed)} corrections {changed[:4]}")

# --- 5. order: tier-major, then publication date DESCENDING (both halves' convention) --
order = {"A":0,"B":1,"C":2}
merged.sort(key=lambda r: (order[tier(r)],
                           [-int(x) for x in (r.get("Publication Date","0-0-0")[:10].split("-")+["0","0"])[:3]
                            if x.isdigit()] or [0],
                           r["Finding ID"]))

# --- 6. verification against the untouched sources ------------------------------------
print("\n--- verification ---")
src = {r["Finding ID"]: r for r in r10 + r11}
out = {r["Finding ID"]: r for r in merged}
print(f"records {len(merged)} (expected {len(r10)+len(r11)})")
assert len(merged) == len(r10) + len(r11)
assert set(out) == set(src), "records lost or invented"
MUT = {"Policy Level","Notes","Proportionality"}
lost = [(f,c) for f,r in src.items() for c in cols
        if c not in MUT and norm(r.get(c)) != norm(out[f].get(c))]
print(f"non-mutated cells altered (must be 0): {len(lost)}  {lost[:4]}")
assert not lost
shrunk = [f for f,r in src.items() if len(norm(out[f].get("Notes"))) < len(norm(r.get("Notes")))]
print(f"rows whose Notes lost content (must be 0): {len(shrunk)}")
assert not shrunk
t = collections.Counter(tier(r) for r in merged)
print("tiers  " + " · ".join(f"{k} {t[k]}" for k in "ABC"))
print("source " + " · ".join(f"{k} {v}" for k,v in collections.Counter(r[PROV] for r in merged).most_common()))
prev = None
for r in merged:
    k = (order[tier(r)], r.get("Publication Date",""))
    if prev and k[0] == prev[0]: assert k[1] <= prev[1], f"date order broken at {r['Finding ID']}"
    prev = k
print("order verified: tier-major A->B->C, publication date descending within tier")

# --- 7. write --------------------------------------------------------------------------
if os.path.exists(OUT):
    shutil.copy2(OUT, OUT.replace(".xlsx", ".backup-"+time.strftime("%Y%m%d-%H%M%S")+".xlsx"))
wb = openpyxl.Workbook(); ws = wb.active; ws.title = SHEET
ws.append(cols)
for r in merged: ws.append([r.get(c,"") for c in cols])
wide = {"Finding ID":30,"Report ID":26,"Institution":30,"Report Title":44,"Source URL":46,
        "Finding":70,"Finding Quote":70,"Models / Systems":30,"Notes":60,
        "Company Response":50,"Sources Checked (channel A)":50,"Channel B Evidence":50,PROV:14}
for i,c in enumerate(cols,1):
    ws.column_dimensions[get_column_letter(i)].width = wide.get(c,18)
    cell = ws.cell(1,i)
    cell.fill = PatternFill("solid", start_color="FFD9D9D9", end_color="FFD9D9D9")
    cell.font = Font(bold=True); cell.alignment = Alignment(vertical="center", wrap_text=True)
for j,r in enumerate(merged, start=2):
    rgb = TIER_FILL[tier(r)]
    f = PatternFill("solid", start_color=rgb, end_color=rgb)
    for i in range(1, len(cols)+1): ws.cell(j,i).fill = f
ws.freeze_panes = "A2"
last = get_column_letter(len(cols))
tbl = Table(displayName="AISIEVAL", ref=f"A1:{last}{ws.max_row}")
tbl.tableStyleInfo = TableStyleInfo(name="TableStyleLight1", showRowStripes=False)
ws.add_table(tbl)
wb.save(OUT)

chk = openpyxl.load_workbook(OUT)[SHEET]
print(f"\nwrote {OUT}")
print(f"  {chk.max_row-1} records x {chk.max_column} columns · sheet {SHEET!r} · table {list(chk.tables)}")
print(f"  table ref {chk.tables['AISIEVAL'].ref} · freeze {chk.freeze_panes} · {os.stat(OUT).st_size:,} bytes")
