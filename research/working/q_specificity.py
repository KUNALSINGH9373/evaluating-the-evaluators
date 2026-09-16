#!/usr/bin/env python3
"""Blast radius of applying col 17's existing 'directly addressed the identified problem' test.

The test is ACTION SPECIFICITY, not attribution. So classify every positive Tier A row by how
tightly its response is bound to the finding, independent of whether the company gave credit:

  SPECIFIC   the response names the finding, the evaluator, the exact attack/benchmark, or
             the exact model behaviour -- it could not be describing anything else
  DOMAIN     the response is a capability designation or safeguard stack for the risk DOMAIN
             the finding sits in, and the source document reports this finding as an input
  GENERAL    the response is a company-wide method, product decision or successor-model
             change that would read identically had this finding never been published

Only GENERAL is at risk under a strict reading of col 17.
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
pos = [r for r in A if r["Action Level"] in ("Substantive", "Partial", "Acknowledged")]

# GENERAL is decided by hand -- these are the rows whose response text describes a company-wide
# method / product decision rather than anything tied to the finding. Everything else is
# classified automatically as SPECIFIC (evaluator or finding named) or DOMAIN (designation).
GENERAL = {
    "CAIS-2023-07-JAI1": "deliberative alignment: a general safety-training method for the o-series",
    "CAIS-2023-07-JAI3": "Constitutional Classifiers prototype, not deployed, not tied to GCG",
    "APOLLO-2023-11-ALI1": "Operator product scope decision (no stock trading)",
    "SCALEAI-2024-10-JAI1": "Operator launched with generic agentic refusals",
    "SCALEAI-2025-02b-JAI3": "Safety Reasoner deployed company-wide",
    "CISCO-2024-07-JAI1": "Prompt Guard 2 released as the successor classifier",
    "CIP-2025-08-ALI1": "Oct 2025 mental-health update built with 170+ experts",
    "FARAI-2024-08-JAI1": "self-serve fine-tuning wind-down, stated rationale is capability not safety",
    "FARAI-2024-10-ALI1": "same wind-down",
    "FARAI-2024-10-JAI1": "same wind-down",
    "FARAI-2025-02a-JAI2": "same wind-down",
}
DESIGNATION = re.compile(r'High capability|Preparedness safeguards|ASL-3|risk designation|'
                         r'classified .{0,40}as High|treating .{0,40}as High', re.I)


def classify(r):
    if r["Finding ID"] in GENERAL:
        return "GENERAL"
    blob = r["Company Response"]
    inst_key = r["Institution"].split("(")[0].strip().split("+")[0].strip()
    named = bool(inst_key and re.search(re.escape(inst_key[:9]), blob, re.I))
    if DESIGNATION.search(blob):
        return "DOMAIN"
    if named or re.search(r'VERBATIM', blob):
        return "SPECIFIC"
    return "UNCLEAR"


buckets = collections.defaultdict(list)
for r in pos:
    buckets[classify(r)].append(r)

print("=== every positive Tier A row, by how tightly the response is bound to the finding ===")
for k in ("SPECIFIC", "DOMAIN", "GENERAL", "UNCLEAR"):
    rows = buckets[k]
    inH = [r for r in rows if r in H]
    print(f"\n{k:<9} {len(rows):>3} Tier A rows ({len(inH)} of them C1)")
    if k in ("GENERAL", "UNCLEAR"):
        for r in sorted(rows, key=lambda r: -int(r["Lag (days)"] or 0)):
            tag = "C1" if r in H else "C2"
            why = GENERAL.get(r["Finding ID"], "")
            print(f"    {r['Finding ID']:<26} {tag} lag {r['Lag (days)'] or '-':>4} "
                  f"{r['Action Level']:<12} {r['Attribution'][:22]:<22} {why[:52]}")

# does GENERAL correlate with missing attribution, or is it a separate axis?
print("\n=== is 'GENERAL' the same thing as 'no attribution'? ===")
ct = collections.Counter((classify(r), r["Attribution"]) for r in pos)
for (k, a), v in sorted(ct.items()):
    print(f"   {k:<9} x {a:<24} {v}")

# headline if GENERAL C1 rows fall to None
c = collections.Counter(r["Proportionality"] for r in H)
gap, und, n = c["Accountability gap (no action)"], c["Under-response (gap)"], len(H)
gen_h = [r for r in buckets["GENERAL"] if r in H]
gB = gap + len(gen_h)
uB = und - sum(1 for r in gen_h if r["Proportionality"] == "Under-response (gap)")
print(f"\nCURRENT                       gap {gap}/{n} = {gap/n:.1%} · falls short {gap+und}/{n} = {(gap+und)/n:.1%}")
print(f"STRICT col 17 (GENERAL->None) gap {gB}/{n} = {gB/n:.1%} · falls short {gB+uB}/{n} = {(gB+uB)/n:.1%}")
print(f"\nrows affected: {len(gen_h)} C1 (+{len(buckets['GENERAL'])-len(gen_h)} C2). "
      f"SPECIFIC and DOMAIN rows are untouched: {len(buckets['SPECIFIC'])+len(buckets['DOMAIN'])} rows.")
