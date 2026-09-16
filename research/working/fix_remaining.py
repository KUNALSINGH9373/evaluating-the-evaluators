#!/usr/bin/env python3
"""Close the five remaining inconsistency classes in AISIEVAL.xlsx."""
import os, re, shutil, time, collections, datetime, openpyxl
P=os.path.expanduser("~/Desktop/AISIEVAL.xlsx"); D="2026-08-16"
def norm(v):
    if v is None: return ""
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return str(v).strip()

# A. negative-search prose sitting in Company Response -> Sources Checked
A_ROWS={"JOINT-2026-07-CYB3","PALISADE-2026-05-AUT1","UKAISI-2026-03-CYB1","FARAI-2026-02-HUM1","HAL-2025-10-AUT2"}
# B. Access Type: launch system card predates the evaluator's report => the eval had pre-release access
B_FIX={"UKAISI-2026-04-CYB11":"Pre-deployment","UKAISI-2026-04-JAI1":"Pre-deployment",
       "UKAISI-2025-11b-ALI1":"Pre-deployment"}
B_FLAG={"UKAISI-2026-05-CYB3"}
# C. month-precision publication dates -> exact
C_FIX={"SHANGHAIAILAB-2023-11-SOC1":("2023-11-12","arXiv 2311.06899 v1 submission date, verified on arxiv.org"),
       "SHANGHAIAILAB-2025-07-ALI2":("2025-07-27","ACL 2025 proceedings date (Vienna, 27 Jul - 1 Aug 2025); aclanthology 2025.acl-long.590"),
       "SHANGHAIAILAB-2025-07-ALI3":("2025-07-27","ACL 2025 proceedings date; aclanthology 2025.acl-long.590"),
       "SHANGHAIAILAB-2025-07-SOC1":("2025-07-27","ACL 2025 proceedings date; aclanthology 2025.findings-acl.754")}
# D. Finding Type
D_FIX={"ANTHROPIC-2026-07-OPUS5-CYB2":("capability-trend;company-published",
        "two Nature values; the claim is progression across model generations (22/23 vs previous best 21/23), "
        "so Nature = capability-trend and 'capability-finding' is dropped"),
       "METR-2026-03-ALI1":("governance",
        "two Nature values; this is METR's external review of Anthropic's safety case, not an empirical model "
        "result (row is Tier C), so Nature = governance"),
       "SHANGHAIAILAB-2023-11-ALI1":("methodology;non-frontier;reassuring-null",
        "modifier delimiter corrected from comma to semicolon")}

shutil.copy2(P, P.replace(".xlsx",".backup-"+time.strftime("%Y%m%d-%H%M%S")+".xlsx"))
wb=openpyxl.load_workbook(P); ws=wb["AISIEVAL"]
hdr=[norm(c.value) for c in ws[1]]; ix={h:i for i,h in enumerate(hdr,1) if h}
def g(r,n): return norm(ws.cell(r,ix[n]).value)
c=collections.Counter()
for r in range(2, ws.max_row+1):
    fid=g(r,"Finding ID")
    if not fid: continue
    def note(t): ws.cell(r,ix["Notes"]).value=(g(r,"Notes")+"  "+t).strip()
    if fid in A_ROWS:
        txt=g(r,"Company Response")
        sc=g(r,"Sources Checked (channel A)")
        ws.cell(r,ix["Sources Checked (channel A)"]).value=(sc+"  " if sc else "")+f"[moved from Company Response {D}] {txt}"
        ws.cell(r,ix["Company Response"]).value=""
        note(f"[COHERENCE {D}] Company Response held a negative SEARCH note, not a response, which broke the "
             "col 17 invariant 'response fields filled <=> level != None'. Text moved verbatim to Sources "
             "Checked, where §9 col 24 puts dated search logs. Action Level = None unchanged.")
        c["negative-search prose moved out of Company Response"]+=1
    if fid in B_FIX:
        old=g(r,"Access Type"); ws.cell(r,ix["Access Type"]).value=B_FIX[fid]
        note(f"[ACCESS TYPE {D}] {old!r} -> {B_FIX[fid]!r}. The cited company document is the launch system "
             "card / deployment-safety page and predates the evaluator's report, which is only possible if the "
             "evaluator had pre-release access; §8's negative-lag allowance applies to pre-deployment "
             "evaluations, so the lag is valid and the Access Type was the error.")
        c["Access Type corrected"]+=1
    if fid in B_FLAG:
        note(f"[UNRESOLVED {D}] Negative lag (-20) on an Access Type of 'Aggregate'. The cited OpenAI GPT-5.5 "
             "cyber page (2026-04-23) predates this aggregate trend report (2026-05-13). §8 invalidates a "
             "response dated before the finding unless it is a documented pre-deployment coordinated "
             "disclosure, which an aggregate trend report cannot be. Either the Access Type or the response "
             "linkage needs review; left unchanged pending adjudication.")
        c["flagged for review"]+=1
    if fid in C_FIX:
        new,why=C_FIX[fid]; old=g(r,"Publication Date")
        ws.cell(r,ix["Publication Date"]).value=new
        note(f"[DATE {D}] Publication Date {old!r} -> {new!r}: month-precision only, resolved to the day. Basis: {why}.")
        c["publication date resolved to ISO"]+=1
    if fid in D_FIX:
        new,why=D_FIX[fid]; old=g(r,"Finding Type")
        ws.cell(r,ix["Finding Type"]).value=new
        note(f"[FINDING TYPE {D}] {old!r} -> {new!r}: {why}.")
        c["Finding Type corrected"]+=1
    if "comparative-ranking" in g(r,"Finding Type"):
        note(f"[REGISTRY {D}] Retains the 'comparative-ranking' modifier, now registered: §4 names comparative "
             "rankings as a Tier A exclusion, so the modifier records why the row sits outside Tier A. "
             "Registry extended rather than the value discarded.")
        c["comparative-ranking registered"]+=1
wb.save(P)
for k,v in c.most_common(): print(f"  {v:>3}  {k}")
