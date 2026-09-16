#!/usr/bin/env python3
"""Re-tier the two Scale AI reports whose findings were coded inconsistently across the halves.

§4 Tier A test, ALL must hold: (1) empirical model finding; (2) names a specific company or model;
(3) a concerning result for which a specific company response is reasonable to expect — which
EXCLUDES benchmark-score results with no dangerous threshold crossed, comparative rankings,
reassuring results, and anonymised models.
"""
import os, shutil, time, datetime, openpyxl
P=os.path.expanduser("~/Desktop/AISIEVAL.xlsx"); D="2026-08-16"
A_ONLY=["Action Level","Attribution","Policy Level","Proportionality"]

PLAN={
 # id: (eval, action_trackable, finding_type, reason)
 "SCALEAI-2026-04-AUT1": ("yes","no","capability-finding;anonymised-model",
   "(1) empirical: YES - a measured benchmark result about model behaviour, so the previous "
   "Eval?=no / Tier C was wrong. (2) names a specific model: NO - 'Frontier coding agents' is "
   "anonymised. -> Tier B. Finding Type corrected from 'methodology': the finding's subject is "
   "model capability, not the benchmark's construction; 'anonymised-model' modifier added."),
 "SCALEAI-2026-04-AUT2": ("yes","no","methodology;anonymised-model",
   "(1) empirical: YES - a measured training result, so Tier C was wrong. (2) names a specific "
   "model: NO - an unnamed 32B model trained by the authors. (3) concerning: NO - an improvement "
   "in help-seeking and pass rate, not a concerning result. -> Tier B. Finding Type stays "
   "'methodology' (the subject is the shaped-reward technique) with 'anonymised-model' added."),
 "SCALEAI-2026-04-AUT5": ("yes","no","capability-finding;anonymised-model",
   "Unchanged at Tier B and re-verified: (1) empirical YES; (2) anonymised frontier coding agents, "
   "so the named-model test fails. -> Tier B."),
 "SCALEAI-2026-06-BIO1": ("yes","no","capability-finding",
   "(1) empirical: YES - a measured solve rate, so Eval?=no / Tier C was wrong. (2) names specific "
   "models: YES (GPT-5.5, Claude Opus 4.8, Gemini 3.5 Flash). (3) concerning result with a "
   "reasonable company response: NO - a 51.6% solve rate is a benchmark-score result with no "
   "dangerous threshold crossed, which §4 condition (3) excludes; a capability shortfall is not an "
   "accountability trigger. -> Tier B. Finding Type corrected 'methodology' -> 'capability-finding'."),
 "SCALEAI-2026-06-BIO2": ("yes","no","capability-finding",
   "(1) empirical: YES, so Tier C was wrong. (2) named models: YES. (3) concerning: NO - a "
   "reasoning-effort/pass-rate scaling result, a benchmark-score result with no dangerous threshold "
   "crossed. -> Tier B. Finding Type corrected 'methodology' -> 'capability-finding'."),
 "SCALEAI-2026-06b-BIO1": ("yes","no","capability-finding",
   "(1) empirical: YES. (2) named models: YES (Claude Opus 4.8, Claude Sonnet 4.6). (3) concerning "
   "result with a reasonable company response: NO - the finding is OVER-refusal on routine analyses "
   "of already-published data, which Scale AI itself characterises as 'a capability gap rather than "
   "a safety boundary'. No dangerous threshold is crossed, so §4 condition (3) excludes it. "
   "-> Tier B (was Tier A). This was the v11 side of the cross-half tier conflict."),
 "SCALEAI-2026-06b-BIO2": ("yes","no","capability-finding;anonymised-model",
   "Unchanged at Tier B and re-verified: (1) empirical YES; (2) anonymised agents across six "
   "harnesses, so the named-model test fails. -> Tier B."),
}

def norm(v):
    if v is None: return ""
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return str(v).strip()
shutil.copy2(P, P.replace(".xlsx",".backup-"+time.strftime("%Y%m%d-%H%M%S")+".xlsx"))
wb=openpyxl.load_workbook(P); ws=wb["AISIEVAL"]
hdr=[norm(c.value) for c in ws[1]]; ix={h:i for i,h in enumerate(hdr,1) if h}
def g(r,n): return norm(ws.cell(r,ix[n]).value)
out=[]
for r in range(2, ws.max_row+1):
    fid=g(r,"Finding ID")
    if fid not in PLAN: continue
    ev,at,ft,why = PLAN[fid]
    old=("A" if g(r,"Action Trackable?")=="yes" else "B" if g(r,"Eval? (trackable)")=="yes" else "C")
    new=("A" if at=="yes" else "B" if ev=="yes" else "C")
    cleared=[f"{c}={g(r,c)}" for c in A_ONLY if g(r,c)]
    ws.cell(r,ix["Eval? (trackable)"]).value=ev
    ws.cell(r,ix["Action Trackable?"]).value=at
    oldft=g(r,"Finding Type")
    ws.cell(r,ix["Finding Type"]).value=ft
    if new!="A":
        for c in A_ONLY: ws.cell(r,ix[c]).value=""
    t=(f"[RE-TIER {D}] Tier {old} -> {new}. {why}")
    if oldft!=ft: t+=f" Finding Type {oldft!r} -> {ft!r}."
    if cleared and new!="A":
        t+=(" Tier-A-only codings cleared and preserved here: " + "; ".join(cleared) + ".")
    ws.cell(r,ix["Notes"]).value=(g(r,"Notes")+"  "+t).strip()
    out.append((fid,old,new,oldft,ft,len(cleared)))
wb.save(P)
print(f"{'Finding':<26}{'was':<5}{'now':<5}{'Finding Type change':<52}cleared")
for fid,o,n,oft,nft,cl in out:
    ch = f"{oft} -> {nft}" if oft!=nft else "(unchanged)"
    print(f"{fid:<26}{o:<5}{n:<5}{ch:<52}{cl}")
