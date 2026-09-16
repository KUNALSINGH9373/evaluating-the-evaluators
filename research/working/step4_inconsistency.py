#!/usr/bin/env python3
"""Quantify the one rule the corpus applies inconsistently.

QUESTION: does an UNATTRIBUTED later mitigation -- a successor-model training change, a
platform wind-down, a new classifier -- count as a company response to an earlier published
finding, when the company never references the finding or the evaluator?

The corpus currently answers YES on some rows and NO on others. Both answers are defensible;
they move the headline in opposite directions. This script measures each direction.
"""
import openpyxl, os, re, datetime, collections

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
A = [r for r in R if tier(r) == "A"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]

# --- SIDE 1: rows that CURRENTLY rely on the permissive reading -----------------------
# positive Action Level + No explicit attribution + a lag long enough that the response is
# a later product rather than a document answering the finding.
permissive = [r for r in H if r["Action Level"] in ("Substantive", "Partial", "Acknowledged")
              and r["Attribution"] == "No explicit attribution"]
print("=" * 100)
print("SIDE 1 — rows whose POSITIVE coding depends on the permissive reading")
print("(positive Action Level, company never referenced the finding or evaluator)")
print(f"{'Finding ID':<28} {'lag':>5}  {'level':<12} {'outcome':<24} response")
print("-" * 118)
for r in sorted(permissive, key=lambda r: -int(r["Lag (days)"] or 0)):
    print(f"{r['Finding ID']:<28} {r['Lag (days)']:>5}  {r['Action Level']:<12} "
          f"{r['Proportionality']:<24} {r['Company Response'][:52]}")
print(f"\n  count: {len(permissive)} C1 rows")

# --- SIDE 2: rows that WOULD become positive under the permissive reading -------------
# identified by hand during the sweep; each has a located, unattributed later mitigation
CANDIDATES = {
    "METR-2025-06-ALI1": "GPT-5 card §3.8 trains gpt-5-thinking against 'deceive, cheat, or hack problems' (13 environments)",
    "METR-2025-06-ALI2": "same GPT-5 card §3.8 anti-cheating training; the finding is that prompt-level mitigations failed",
    "METR-2025-06-ALI3": "same GPT-5 card §3.8 anti-cheating training",
    "METR-2025-04-ALI2": "ALREADY Acknowledged — its note wrongly says no reward-hacking mitigation exists in the GPT-5 follow-up",
    "UKAISI-2025-02-JAI1": "self-serve fine-tuning wind-down removes the tested attack surface",
    "PALISADE-2024-12-JAI1": "same fine-tuning wind-down, same surface",
}
byid = {r["Finding ID"]: r for r in R}
print("\n" + "=" * 100)
print("SIDE 2 — rows that WOULD move to a positive coding if the permissive reading is upheld")
print(f"{'Finding ID':<28} {'sev':<4} {'level':<12} {'outcome':<24} candidate response")
print("-" * 118)
for fid, why in CANDIDATES.items():
    r = byid.get(fid)
    if not r:
        print(f"{fid:<28} !! not found")
        continue
    print(f"{fid:<28} {r['Severity (C1/C2) majority']:<4} {r['Action Level'] or 'None':<12} "
          f"{r['Proportionality']:<24} {why[:60]}")

# --- headline under each resolution ---------------------------------------------------
c = collections.Counter(r["Proportionality"] for r in H)
gap, und, pro = (c["Accountability gap (no action)"], c["Under-response (gap)"], c["Proportionate"])
n = len(H)
print("\n" + "=" * 100)
print(f"CURRENT (mixed):  gap {gap}/{n} = {gap/n:.1%} · falls short {gap+und}/{n} = {(gap+und)/n:.1%}")

# Option A: permissive upheld -> the four None candidates in H become positive (leave gap)
moves_out = [f for f in CANDIDATES if byid.get(f) and byid[f] in H
             and byid[f]["Proportionality"] == "Accountability gap (no action)"]
gA, uA = gap - len(moves_out), und + len(moves_out)
print(f"OPTION A (uphold): {len(moves_out)} rows leave the gap  -> "
      f"gap {gA}/{n} = {gA/n:.1%} · falls short {gA+uA}/{n} = {(gA+uA)/n:.1%}")

# Option B: permissive rejected -> the Side 1 rows fall to None (enter gap)
enter = [r for r in permissive if r["Proportionality"] != "Accountability gap (no action)"]
gB = gap + len(enter)
uB = und - sum(1 for r in enter if r["Proportionality"] == "Under-response (gap)")
print(f"OPTION B (reject): {len(enter)} rows fall to None      -> "
      f"gap {gB}/{n} = {gB/n:.1%} · falls short {gB+max(uB,0)}/{n} = {(gB+max(uB,0))/n:.1%}")
print(f"\nSpread on the headline: {min(gA,gB)/n:.1%} to {max(gA,gB)/n:.1%} "
      f"({abs(gA-gB)} rows, {abs(gA-gB)/n:.1%} of the population)")
