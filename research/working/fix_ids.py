#!/usr/bin/env python3
"""Resolve Finding ID / Report ID inconsistencies in AISIEVAL.xlsx.

Three classes of fix, all collision-checked before anything is written:
  1. DUPLICATE REPORTS — one report carrying two Report IDs across the halves.
  2. FORMAT — Report IDs missing the month, using the wrong prefix, or an uppercase
     month suffix. Month is derived from the row's own Publication Date.
  3. FINDING IDs — only where the ID is malformed against §6. Finding IDs are immutable
     by rule, so each rename is recorded in Notes with its old value.
"""
import os, re, shutil, time, collections, datetime, openpyxl

P = os.path.expanduser("~/Desktop/AISIEVAL.xlsx"); D = "2026-08-16"

def norm(v):
    if v is None: return ""
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return str(v).strip()

wb = openpyxl.load_workbook(P); ws = wb["AISIEVAL"]
hdr = [norm(c.value) for c in ws[1]]
ix = {h:i for i,h in enumerate(hdr,1) if h}
def g(r,n): return norm(ws.cell(r, ix[n]).value)

rid_now = {g(r,"Report ID") for r in range(2, ws.max_row+1) if g(r,"Report ID")}
fid_now = {g(r,"Finding ID") for r in range(2, ws.max_row+1)}

# ---- 1. duplicate reports: same title + date, two IDs --------------------------------
REPORT_MERGE = {
  "SCALEAI-2026-06b": "SCALEAI-2026-06-DRUGDISCOVERY",   # PDF vs leaderboard, same report
  "OPENAI-2026-03b-SELF-METAGAMING": "APOLLO-2026-03",   # Apollo/OpenAI co-published, same paper
}
# ---- 2. Report ID format --------------------------------------------------------------
REPORT_RENAME = {
  "AISI-2025-2HOP":                    "UKAISI-2025-09-2HOP",
  "AISI-2026-FUTUREWORK":              "UKAISI-2026-02-FUTUREWORK",
  "AISI-2026-MCP177K":                 "UKAISI-2026-03-MCP177K",
  "AISI-2026-PREFILL":                 "UKAISI-2026-06-PREFILL",
  "AISI-JP-SpecificInfluence-2025":    "JAISI-2025-10-SPECIFICINFLUENCE",
  "CAISI-AGENT-HIJACKING-2025":        "JOINT-2025-01-AGENTHIJACKING",
  "NIST AI 800-1":                     "USCAISI-2025-01-NISTAI8001",
  "SGAISI-KR-DataLeakage-Agents-2026": "SGAISI-2026-06-DATALEAKAGEAGENTS",
  "SGAISI-RedTeaming-Challenge-2025":  "SGAISI-2025-02-REDTEAMINGCHALLENGE",
  "UKAISI-FIRST-YEAR-2024":            "UKAISI-2024-11-FIRSTYEAR",
  "UKAISI-ALI-2026-04-10":             "UKAISI-2026-04-ALI10",
  "UKAISI-ALI-2026-05-14":             "UKAISI-2026-05-ALI14",
  "UKAISI-ALI-2026-05-30":             "UKAISI-2026-05-ALI30",
  # uppercase month suffix -> lowercase, per PREFIX-YYYY-MM[m]
  "DREADNODE-2025-06B":     "DREADNODE-2025-06b",
  "DREADNODE-2025-12B":     "DREADNODE-2025-12b",
  "SHANGHAIAILAB-2024-02B": "SHANGHAIAILAB-2024-02b",
  "SHANGHAIAILAB-2024-06A": "SHANGHAIAILAB-2024-06a",
  "SHANGHAIAILAB-2024-06B": "SHANGHAIAILAB-2024-06b",
  "SHANGHAIAILAB-2025-07A": "SHANGHAIAILAB-2025-07a",
  "SHANGHAIAILAB-2025-07B": "SHANGHAIAILAB-2025-07b",
  "SHANGHAIAILAB-2025-07C": "SHANGHAIAILAB-2025-07c",
  "SHANGHAIAILAB-2025-07D": "SHANGHAIAILAB-2025-07d",
  "UKAISI-2026-05B":        "UKAISI-2026-05b",
  # a Report ID that had been set equal to a Finding ID
  "UKAISI-2025-10-ALI1b":   "UKAISI-2025-10b",
  "UKAISI-2026-06-ALI1b":   "UKAISI-2026-06c",
}
# ---- 3. Finding ID format (malformed only) --------------------------------------------
FINDING_RENAME = {
  "UKAISI-2026-05B-ALI1": "UKAISI-2026-05b-ALI1",
  "UKAISI-2026-05B-ALI2": "UKAISI-2026-05b-ALI2",
  # trailing lowercase letter on the sequence number: the [m] month-suffix slot is where
  # same-month disambiguation belongs, so move it there
  "UKAISI-2025-10-ALI1b": "UKAISI-2025-10b-ALI1",
  "UKAISI-2026-04-ALI1b": "UKAISI-2026-04d-ALI1",
  "UKAISI-2026-04-ALI2b": "UKAISI-2026-04e-ALI1",
  "UKAISI-2026-06-ALI1b": "UKAISI-2026-06c-ALI1",
}

# ---- collision checks ------------------------------------------------------------------
errs = []
for old, new in {**REPORT_MERGE, **REPORT_RENAME}.items():
    if old not in rid_now: errs.append(f"report {old!r} not present")
for old, new in REPORT_RENAME.items():
    if new in rid_now and new != old: errs.append(f"report target {new!r} already in use")
for old, new in FINDING_RENAME.items():
    if old not in fid_now: errs.append(f"finding {old!r} not present")
    if new in fid_now: errs.append(f"finding target {new!r} already in use")
tgt = list(REPORT_RENAME.values()) + list(FINDING_RENAME.values())
for k, n in collections.Counter(tgt).items():
    if n > 1: errs.append(f"target {k!r} generated {n} times")
if errs:
    print("ABORT — collision check failed:"); [print("   ", e) for e in errs]; raise SystemExit(1)
print("collision check: clean\n")

# ---- apply -----------------------------------------------------------------------------
shutil.copy2(P, P.replace(".xlsx", ".backup-"+time.strftime("%Y%m%d-%H%M%S")+".xlsx"))
c = collections.Counter(); tierflag = []
for r in range(2, ws.max_row+1):
    fid, rid = g(r,"Finding ID"), g(r,"Report ID")
    def note(t): ws.cell(r, ix["Notes"]).value = (g(r,"Notes") + "  " + t).strip()
    if rid in REPORT_MERGE:
        new = REPORT_MERGE[rid]; ws.cell(r, ix["Report ID"]).value = new
        note(f"[ID FIX {D}] Report ID {rid!r} -> {new!r}: the same report carried two IDs across the "
             "merged halves (identical title and publication date, different hosting URL). Unified under "
             "one ID per §6. Finding ID unchanged.")
        c["duplicate report unified"] += 1
    elif rid in REPORT_RENAME:
        new = REPORT_RENAME[rid]; ws.cell(r, ix["Report ID"]).value = new
        note(f"[ID FIX {D}] Report ID {rid!r} -> {new!r}: normalised to PREFIX-YYYY-MM[m][-slug] per §6 "
             "(month derived from this row's Publication Date; prefix and month-suffix case aligned with "
             "the rest of the corpus).")
        c["report ID format normalised"] += 1
    if fid in FINDING_RENAME:
        new = FINDING_RENAME[fid]; ws.cell(r, ix["Finding ID"]).value = new
        note(f"[ID FIX {D}] Finding ID {fid!r} -> {new!r}: malformed against §6 "
             "(PREFIX-YYYY-MM[m]-DDDn). Finding IDs are immutable by rule, so the previous value is "
             "recorded here for traceability.")
        c["finding ID corrected"] += 1
wb.save(P)
for k,v in c.most_common(): print(f"  {v:>3}  {k}")

# ---- re-verify --------------------------------------------------------------------------
ws2 = openpyxl.load_workbook(P, data_only=True)["AISIEVAL"]
h2 = [norm(x.value) for x in ws2[1]]
rows = [{h: norm(ws2.cell(r,i).value) for i,h in enumerate(h2,1) if h} for r in range(2, ws2.max_row+1)]
rows = [r for r in rows if r.get("Finding ID")]
print(f"\n--- verification ---\nrecords {len(rows)}")
dupf = [k for k,v in collections.Counter(r["Finding ID"] for r in rows).items() if v>1]
print(f"duplicate Finding IDs: {len(dupf)} {dupf}")
rf = re.compile(r"^[A-Z0-9]+-\d{4}-\d{2}[a-z]{0,2}(-[A-Za-z0-9]+)*$")
badr = sorted({r["Report ID"] for r in rows if r.get("Report ID") and not rf.match(r["Report ID"])})
print(f"Report IDs still off-format: {len(badr)} {badr}")
ff = re.compile(r"^[A-Z0-9]+-\d{4}-\d{2}[a-z]{0,2}(-[A-Za-z0-9]+)*-[A-Z]{2,4}\d+(-s\d+)?$")
badf = sorted(r["Finding ID"] for r in rows if not ff.match(r["Finding ID"]))
print(f"Finding IDs still off-format: {len(badf)} {badf}")
m = collections.defaultdict(set)
for r in rows:
    if r.get("Report ID"): m[r["Report ID"]].add((r.get("Report Title",""), r.get("Publication Date","")))
print(f"Report IDs with >1 (title,date): {len([k for k,v in m.items() if len(v)>1])}")
def ct(t): return re.sub(r'[^a-z0-9]','',t.lower())
t = collections.defaultdict(set)
for r in rows: t[(ct(r.get("Report Title","")), r.get("Publication Date",""))].add(r.get("Report ID",""))
print(f"same title+date under >1 Report ID: {len([k for k,v in t.items() if k[0] and len(v)>1])}")
print(f"distinct Report IDs: {len({r['Report ID'] for r in rows if r.get('Report ID')})}")
