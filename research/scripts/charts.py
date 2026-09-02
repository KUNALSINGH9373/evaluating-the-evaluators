#!/usr/bin/env python3
"""Chart suite for the AISIEVAL_V12 sheet — paper-ready: very large type, bright colours, no overlap."""
import os
import dataset_source, re, collections, datetime, textwrap
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, MaxNLocator
import numpy as np, openpyxl
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palette import *   # single source of colour truth

OUT = CHARTS_OUT; os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({
 "figure.dpi":200,"savefig.dpi":200,"font.family":"DejaVu Sans",
 "axes.spines.top":False,"axes.spines.right":False,
 "axes.edgecolor":INK_2,"axes.linewidth":2.2,
 "figure.facecolor":"white","axes.facecolor":"white","savefig.facecolor":"white",
 "axes.titlesize":40,"axes.labelsize":31,"xtick.labelsize":27,"ytick.labelsize":27,
 "xtick.major.width":2.2,"ytick.major.width":2.2,"xtick.major.size":8,"ytick.major.size":8,
 "axes.grid":True,"grid.color":GRID,"grid.linewidth":1.6,"axes.axisbelow":True})
# colours come from palette.py; these aliases keep the existing call sites readable
SKY=NEUTRAL[2]; PURPLE=NEUTRAL[3]; TEAL=NEUTRAL[0]; MAGENTA=NEUTRAL[5]; LIME=AMBER
TIER={k:TIER_INK[k] for k in "ABC"}
PROP_C=PROP; AL_C=ACTION; PL_C=POLICY

def norm(v):
    if v is None: return ""
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return str(v).strip()
ws=dataset_source.sheet()
hdr=[norm(c.value) for c in ws[1]]
ROWS=[{h:norm(ws.cell(r,i).value) for i,h in enumerate(hdr,1) if h} for r in range(2,ws.max_row+1)]
ROWS=[r for r in ROWS if r.get("Finding ID")]
tier=lambda r:("A" if r.get("Action Trackable?")=="yes" else "B" if r.get("Eval? (trackable)")=="yes" else "C")
A=[r for r in ROWS if tier(r)=="A"]
H=[r for r in A if r.get("Severity (C1/C2) majority")=="C1"]          # headline population
isgap=lambda r: r.get("Proportionality")=="Accountability gap (no action)"

DEVMAP=[("OpenAI",("gpt","o1-","o3","o4-","chatgpt","codex","operator","gpt-oss")),
 ("Anthropic",("claude","opus","sonnet","haiku","mythos","fable")),("Google",("gemini","gemma","deepmind")),
 ("Meta",("llama","prompt-guard","promptguard","muse spark")),("DeepSeek",("deepseek",)),
 ("Alibaba (Qwen)",("qwen",)),("Mistral",("mistral",)),("Moonshot",("kimi","moonshot")),
 ("xAI",("grok",)),("Z.ai",("glm",)),("Thinking Machines",("inkling",))]
def dev(r):
    s=(r.get("Models / Systems","")+" "+r.get("Report Title","")).lower()
    for d,ks in DEVMAP:
        if any(k in s for k in ks): return d
    return "Other / unnamed"

def save(fig,name):
    p=os.path.join(OUT,name); fig.savefig(p,bbox_inches="tight",pad_inches=0.45); plt.close(fig)
    print("  ",name)

def vbar(ax,labels,vals,colors,total=None,pct=True,fs=27):
    b=ax.bar(range(len(vals)),vals,color=colors,width=0.62,zorder=3)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels,fontsize=fs)
    top=max(vals) if vals else 1
    for i,v in enumerate(vals):
        t=f"{v}\n({v/total:.0%})" if (pct and total) else f"{v}"
        ax.text(i,v+top*0.025,t,ha="center",va="bottom",fontsize=fs+1,fontweight="bold",linespacing=1.35)
    ax.set_ylim(0,top*1.24); ax.grid(axis="x",visible=False)
    return b

def hbar(ax,labels,vals,colors,total=None,fs=25,height=0.68):
    y=np.arange(len(labels))
    ax.barh(y,vals,color=colors,height=height,zorder=3)
    ax.set_yticks(y); ax.set_yticklabels(labels,fontsize=fs); ax.invert_yaxis()
    m=max(vals) if vals else 1
    for i,v in enumerate(vals):
        t=f"{v}  ({v/total:.0%})" if total else f"{v}"
        ax.text(v+m*0.015,i,t,va="center",ha="left",fontsize=fs,fontweight="bold")
    ax.set_xlim(0,m*(1.20 if total else 1.10)); ax.grid(axis="y",visible=False)

# ---------------------------------------------------------------- 00 hero
fig,ax=plt.subplots(figsize=(20,11.5)); ax.axis("off")
g=sum(1 for r in H if isgap(r))
ax.text(.5,.965,"Evaluating the Evaluators",ha="center",fontsize=60,fontweight="bold",color="#111111")
ax.text(.5,.888,"The public-channel AI accountability pipeline",ha="center",fontsize=31,color=MUTED)
boxes=[(f"{len(ROWS):,}","findings in\nthe corpus",BLUE),
       (f"{len(A)}","Tier A\naccountability-\nrelevant",TIER["A"]),
       (f"{len(H)}","Tier A + C1\nheadline\npopulation",PURPLE),
       (f"{g/len(H):.0%}","accountability gap\nno documented\naction",ORANGE)]
BW,GAP=0.212,0.024
x0=(1-(4*BW+3*GAP))/2
for i,(big,small,col) in enumerate(boxes):
    x=x0+i*(BW+GAP)
    ax.add_patch(plt.Rectangle((x,.335),BW,.44,transform=ax.transAxes,facecolor=col,alpha=.13,
                               edgecolor=col,linewidth=5,zorder=1))
    ax.text(x+BW/2,.655,big,ha="center",va="center",fontsize=58,fontweight="bold",color=col)
    ax.text(x+BW/2,.445,small,ha="center",va="center",fontsize=21,color=INK_2,linespacing=1.55)
ax.text(.5,.205,f"{g} of {len(H)} significant-risk findings about a named, accountable developer",
        ha="center",fontsize=29,color="#111111",fontweight="bold")
ax.text(.5,.135,"have no documented company response by the corpus cutoff",
        ha="center",fontsize=29,color="#111111",fontweight="bold")
_nrep = len({r["Report ID"] for r in ROWS if r.get("Report ID")})
_d = [r["Publication Date"] for r in ROWS if r.get("Publication Date")]
ax.text(.5,.035,f"Corpus: {len(ROWS):,} findings · {_nrep} reports · {min(_d)} to {max(_d)}",
        ha="center",fontsize=21,color=MUTED)
# 00_title_hero.png is owned by hero.py (the v10-style schematic funnel). This older
# 4-box version used to overwrite it whenever charts.py ran after hero.py — disabled.
plt.close(fig)

# ---------------------------------------------------------------- 01 institutions
# SUPERSEDED. charts2.py owns 01 as a lollipop and, running second, silently overwrote the bar
# built here — the fourth time two scripts have fought over one filename. Withdrawn 2026-08-19.

# ---------------------------------------------------------------- 02 developer (Tier A)
c=collections.Counter(dev(r) for r in A)
c.pop("Other / unnamed",None)
c=c.most_common(12)
fig,ax=plt.subplots(figsize=(18,12))
hbar(ax,[k for k,_ in c],[v for _,v in c],ramp(len(c)),len(A))
ax.set_title(f"Tier A Findings per Model Developer (n={len(A)})",pad=26); ax.set_xlabel("Tier A findings")
# WITHDRAWN 2026-08-18: this figure attributes findings to a developer via a regex over
# "Models / Systems" + "Report Title". Two reasonable regexes disagreed on 7 of 147 headline
# rows, 11 rows name multiple vendors and were silently assigned to the first match, and report
# titles contaminate the match. Not defensible for per-company claims. Restore only once the
# workbook carries a hand-verified Developer column.
plt.close(fig)

# ---------------------------------------------------------------- 03 access type
order_keys=["Pre-deployment","Post-deployment","Mixed","Aggregate","N/A"]
order=order_keys
c=collections.Counter(r.get("Access Type") for r in ROWS)
v=[c.get(k,0) for k in order]
fig,ax=plt.subplots(figsize=(17,11))
vbar(ax,[k.replace("-","-\n") if k=="Post-deployment" else k for k in order],v,colours_for(ACCESS,order_keys),len(ROWS))
ax.set_title(f"Findings by Model Access Type (n={len(ROWS):,})",pad=26); ax.set_ylabel("Findings")
save(fig,"03_findings_per_access_type.png")

# ---------------------------------------------------------------- 04 headline outcome
order=["Proportionate","Under-response (gap)","Accountability gap (no action)"]
c=collections.Counter(r.get("Proportionality") for r in H)
fig,ax=plt.subplots(figsize=(18,11))
vbar(ax,["Proportionate","Under-response\n(gap)","Accountability gap\n(no action)"],
     [c.get(k,0) for k in order],[PROP_C[k] for k in order],len(H))
ax.set_title(f"Headline Outcome Distribution — Tier A, C1 Findings (n={len(H)})",pad=26)
ax.set_ylabel("Findings")
save(fig,"04_headline_outcome_distribution.png")

# ---------------------------------------------------------------- 05 pre vs post substantive rate
fig,ax=plt.subplots(figsize=(16,11))
labs=[];vals=[];ns=[]
for k in ("Pre-deployment","Post-deployment"):
    S=[r for r in H if r.get("Access Type")==k]
    if not S: continue
    s=sum(1 for r in S if r.get("Action Level")=="Substantive")
    labs.append(f"{k}\n(n={len(S)})"); vals.append(s/len(S)); ns.append(s)
b=ax.bar(range(len(vals)),vals,color=colours_for(SCOPE,["government-AISI","third-party-evaluator"]),width=0.56,zorder=3)
ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs,fontsize=28)
for i,(v,n) in enumerate(zip(vals,ns)):
    ax.text(i,v+max(vals)*0.03,f"{v:.0%}\n({n} findings)",ha="center",va="bottom",fontsize=29,fontweight="bold",linespacing=1.4)
ax.set_ylim(0,max(vals)*1.34); ax.yaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_title("Substantive Response Rate: Pre- vs Post-Deployment\nTier A, C1 findings",pad=26,fontsize=36)
ax.set_ylabel("Substantive response rate"); ax.grid(axis="x",visible=False)
save(fig,"05_pre_vs_post_deployment_response_rate.png")

# ---------------------------------------------------------------- 06 findings per year
c=collections.Counter(r.get("Publication Date","")[:4] for r in ROWS)
yrs=sorted(k for k in c if k)
fig,ax=plt.subplots(figsize=(16,10.5))
vbar(ax,yrs,[c[y] for y in yrs],ramp(len(yrs)),len(ROWS))
ax.set_title(f"Findings per Publication Year (n={len(ROWS):,})",pad=26); ax.set_ylabel("Findings")
save(fig,"06_findings_per_year.png")

# ---------------------------------------------------------------- 07 tier distribution
# Three tier bars only — no total/corpus bar; n is stated in the title instead.
c=collections.Counter(tier(r) for r in ROWS)
fig,ax=plt.subplots(figsize=(17,10.5))
vbar(ax,["Tier A\naccountability-relevant","Tier B\nno accountable party","Tier C\nnot an empirical finding"],
     [c["A"],c["B"],c["C"]],[TIER["A"],TIER["B"],TIER["C"]],len(ROWS),fs=26)
ax.set_title(f"Tier Distribution (n={len(ROWS):,} findings)",pad=26); ax.set_ylabel("Findings")
save(fig,"07_tier_distribution.png")

# ---------------------------------------------------------------- 08 action level
order=["Substantive","Partial","Acknowledged","None"]
c=collections.Counter(r.get("Action Level") for r in A)
fig,ax=plt.subplots(figsize=(17,11))
vbar(ax,["Substantive","Partial","Acknowledged","None\n(no response found)"],
     [c.get(k,0) for k in order],[AL_C[k] for k in order],len(A))
ax.set_title(f"Channel A — Company Response Strength (Tier A, n={len(A)})",pad=26)
ax.set_ylabel("Findings")
save(fig,"08_action_level_distribution.png")

# ---------------------------------------------------------------- 09 policy level
order=["Binding policy action","Non-binding policy-related uptake","No policy uptake identified"]
c=collections.Counter(r.get("Policy Level") for r in A)
fig,ax=plt.subplots(figsize=(18,11))
vbar(ax,["Binding\npolicy action","Non-binding\npolicy-related uptake","No policy uptake\nidentified"],
     [c.get(k,0) for k in order],[PL_C[k] for k in order],len(A))
ax.set_title(f"Channel B — Policy Uptake (Tier A, n={len(A)})",pad=26); ax.set_ylabel("Findings")
save(fig,"09_policy_level_distribution.png")

# ---------------------------------------------------------------- 10 proportionality by severity
order=["Proportionate","Under-response (gap)","Accountability gap (no action)"]
fig,ax=plt.subplots(figsize=(19,11))
w=0.36; x=np.arange(len(order))
for j,(sev,col,alpha) in enumerate([("C1",ORANGE,1.0),("C2",SKY,1.0)]):
    S=[r for r in A if r.get("Severity (C1/C2) majority")==sev]
    v=[sum(1 for r in S if r.get("Proportionality")==k) for k in order]
    ax.bar(x+(j-0.5)*w,v,width=w,color=col,zorder=3,label=f"{sev} ({'significant' if sev=='C1' else 'low'} risk), n={len(S)}")
    for i,val in enumerate(v):
        ax.text(x[i]+(j-0.5)*w,val+2,f"{val}\n{val/len(S):.0%}",ha="center",va="bottom",fontsize=24,fontweight="bold",linespacing=1.3)
ax.set_xticks(x); ax.set_xticklabels(["Proportionate","Under-response\n(gap)","Accountability gap\n(no action)"],fontsize=27)
ax.set_ylim(0,max([sum(1 for r in A if r.get("Proportionality")==k) for k in order])*1.05)
ax.legend(fontsize=26,frameon=False,loc="upper left"); ax.grid(axis="x",visible=False)
ax.set_title("Proportionality Outcome by Severity (Tier A)",pad=26); ax.set_ylabel("Findings")
save(fig,"10_proportionality_by_severity.png")

# ---------------------------------------------------------------- 11 domains
d=collections.Counter()
for r in ROWS:
    for p in [x.strip() for x in r.get("Domain","").split(";") if x.strip()]: d[p]+=1
c=d.most_common()
fig,ax=plt.subplots(figsize=(18,14))
pal=[BLUE,ORANGE,TEAL,PURPLE,GREEN,MAGENTA,AMBER,SKY,LIME,RED]
hbar(ax,[k for k,_ in c],[v for _,v in c],[pal[i%len(pal)] for i in range(len(c))],len(ROWS))
ax.set_title("Findings per Risk Domain  (multi-label; total exceeds n)",pad=26); ax.set_xlabel("Findings")
save(fig,"11_domain_distribution.png")

# ---------------------------------------------------------------- 12 scope
c=collections.Counter(r.get("Scope") for r in ROWS)
fig,ax=plt.subplots(figsize=(15,10.5))
vbar(ax,["Government AISI","Third-party evaluator"],
     [c.get("government-AISI",0),c.get("third-party-evaluator",0)],[BLUE,ORANGE],len(ROWS),fs=29)
ax.set_title(f"Evaluator Scope (n={len(ROWS):,})",pad=26); ax.set_ylabel("Findings")
save(fig,"12_evaluator_scope.png")

# ---------------------------------------------------------------- 13 institution type
# SUPERSEDED. This flat bar of institution-type counts is replaced by tree.py's
# 13_institution_type_tree.png, which shows the same counts plus which institutions sit
# under each type. Kept unbuilt rather than deleted so the count is still recomputable.

# ---------------------------------------------------------------- 14 lag distribution
lags=[int(r["Lag (days)"]) for r in A if re.fullmatch(r"-?\d+", r.get("Lag (days)",""))]
fig,ax=plt.subplots(figsize=(18,10.5))
bins=[-650,-90,-30,0,30,90,180,365,700]
n,_,patches=ax.hist(lags,bins=bins,color=BLUE,edgecolor="white",linewidth=3,zorder=3)
for p,v in zip(patches,n):
    if v: ax.text(p.get_x()+p.get_width()/2,v+0.5,f"{int(v)}",ha="center",va="bottom",fontsize=27,fontweight="bold")
ax.set_xscale("symlog",linthresh=30)
ax.set_xticks([-365,-90,-30,0,30,90,365]); ax.set_xticklabels(["-365","-90","-30","0","30","90","365"],fontsize=25)
ax.axvline(0,color=RED,linewidth=4,linestyle="--",zorder=4)
ax.text(-60,max(n)*0.86,"publication\ndate  ",color=RED,fontsize=24,fontweight="bold",
        ha="right",va="center",linespacing=1.35)
ax.set_ylim(0,max(n)*1.18); ax.grid(axis="x",visible=False)
ax.set_title(f"Response Lag Distribution (Tier A, n={len(lags)})\nnegative = company documented before the finding was published",
             pad=24,fontsize=34)
ax.set_xlabel("Days between publication and company response (symlog)"); ax.set_ylabel("Findings")
save(fig,"14_response_lag_distribution.png")

# ---------------------------------------------------------------- 15 gap rate by year
yrs=sorted({r["Publication Date"][:4] for r in H})
vals=[];ns=[]
for y in yrs:
    S=[r for r in H if r["Publication Date"].startswith(y)]
    vals.append(sum(1 for r in S if isgap(r))/len(S)); ns.append(len(S))
fig,ax=plt.subplots(figsize=(16,10.5))
ax.bar(range(len(yrs)),vals,color=ORANGE,width=0.6,zorder=3)
ax.set_xticks(range(len(yrs))); ax.set_xticklabels([f"{y}\n(n={n})" for y,n in zip(yrs,ns)],fontsize=27)
for i,(v,n) in enumerate(zip(vals,ns)):
    ax.text(i,v+0.02,f"{v:.0%}",ha="center",va="bottom",fontsize=30,fontweight="bold")
ax.set_ylim(0,1.0); ax.yaxis.set_major_formatter(PercentFormatter(1.0)); ax.grid(axis="x",visible=False)
ax.set_title("Accountability Gap Rate by Year (Tier A, C1)",pad=26); ax.set_ylabel("Share with no documented action")
save(fig,"15_gap_rate_by_year.png")

# ---------------------------------------------------------------- 16 gap rate by access type
keys=[k for k in ("Pre-deployment","Post-deployment","Mixed","Aggregate") if any(r.get("Access Type")==k for r in H)]
vals=[];ns=[]
for k in keys:
    S=[r for r in H if r.get("Access Type")==k]
    vals.append(sum(1 for r in S if isgap(r))/len(S)); ns.append(len(S))
fig,ax=plt.subplots(figsize=(17,10.5))
ax.bar(range(len(keys)),vals,color=colours_for(ACCESS,keys),width=0.6,zorder=3)
ax.set_xticks(range(len(keys))); ax.set_xticklabels([f"{k}\n(n={n})" for k,n in zip(keys,ns)],fontsize=27)
for i,v in enumerate(vals): ax.text(i,v+0.02,f"{v:.0%}",ha="center",va="bottom",fontsize=31,fontweight="bold")
ax.set_ylim(0,1.05); ax.yaxis.set_major_formatter(PercentFormatter(1.0)); ax.grid(axis="x",visible=False)
ax.set_title("Accountability Gap Rate by Model Access Type (Tier A, C1)",pad=26,fontsize=36)
ax.set_ylabel("Share with no documented action")
save(fig,"16_gap_rate_by_access_type.png")

# ---------------------------------------------------------------- 17 severity
c=collections.Counter(r.get("Severity (C1/C2) majority") for r in ROWS)
fig,ax=plt.subplots(figsize=(15,10.5))
vbar(ax,["C1\nsignificant risk","C2\nlow risk"],[c["C1"],c["C2"]],colours_for(SEV,["C1","C2"]),len(ROWS),fs=29)
ax.set_title(f"Severity Classification — 3-model ensemble majority (n={len(ROWS):,})",pad=26,fontsize=35)
ax.set_ylabel("Findings")
save(fig,"17_severity_classification.png")

# ---------------------------------------------------------------- 18 attribution
order=["Explicit attribution","No explicit attribution","No response located"]
c=collections.Counter(r.get("Attribution") for r in A)
fig,ax=plt.subplots(figsize=(17,10.5))
vbar(ax,["Explicit\nattribution","No explicit\nattribution","No response\nlocated"],
     [c.get(k,0) for k in order],colours_for(ATTRIB,["Explicit attribution","No explicit attribution","No response located"]),len(A))
ax.set_title(f"Attribution of Company Responses (Tier A, n={len(A)})",pad=26); ax.set_ylabel("Findings")
save(fig,"18_attribution_distribution.png")

# ---------------------------------------------------------------- 19 gap rate by developer
c=collections.Counter(dev(r) for r in H); c.pop("Other / unnamed",None)
devs=[d for d,n in c.most_common() if n>=5]
vals=[];ns=[]
for d in devs:
    S=[r for r in H if dev(r)==d]
    vals.append(sum(1 for r in S if isgap(r))/len(S)); ns.append(len(S))
o=np.argsort(vals)[::-1]; devs=[devs[i] for i in o]; vals=[vals[i] for i in o]; ns=[ns[i] for i in o]
fig,ax=plt.subplots(figsize=(17,11))
y=np.arange(len(devs))
ax.barh(y,vals,color=[ORANGE if v>=0.5 else GREEN for v in vals],height=0.62,zorder=3)
ax.set_yticks(y); ax.set_yticklabels([f"{d}  (n={n})" for d,n in zip(devs,ns)],fontsize=27); ax.invert_yaxis()
for i,v in enumerate(vals): ax.text(v+0.015,i,f"{v:.0%}",va="center",fontsize=28,fontweight="bold")
ax.set_xlim(0,1.12); ax.xaxis.set_major_formatter(PercentFormatter(1.0)); ax.grid(axis="y",visible=False)
ax.set_title("Accountability Gap Rate by Developer (Tier A, C1; n≥5)",pad=26,fontsize=36)
ax.set_xlabel("Share with no documented action")
# WITHDRAWN 2026-08-18: this figure attributes findings to a developer via a regex over
# "Models / Systems" + "Report Title". Two reasonable regexes disagreed on 7 of 147 headline
# rows, 11 rows name multiple vendors and were silently assigned to the first match, and report
# titles contaminate the match. Not defensible for per-company claims. Restore only once the
# workbook carries a hand-verified Developer column.
plt.close(fig)

# ---------------------------------------------------------------- 20 pipeline funnel
stages=[("All findings in the corpus",len(ROWS)),
        ("Tier A — accountability-relevant",len(A)),
        ("Tier A + C1 — significant risk",len(H)),
        ("Company responded (any level)",sum(1 for r in H if r.get("Action Level")!="None")),
        ("Substantive company response",sum(1 for r in H if r.get("Action Level")=="Substantive")),
        ("Any documented policy uptake",sum(1 for r in H if r.get("Policy Level")!="No policy uptake identified"))]
fig,ax=plt.subplots(figsize=(19,11))
cols=[NEUTRAL[0],TIER_INK["A"],NEUTRAL[1],ORANGE,GREEN,NEUTRAL[3]]
v=[n for _,n in stages]; y=np.arange(len(v))
ax.barh(y,v,color=cols,height=0.66,zorder=3)
ax.set_yticks(y); ax.set_yticklabels([s for s,_ in stages],fontsize=27); ax.invert_yaxis()
for i,n in enumerate(v):
    ax.text(n+len(ROWS)*0.012,i,f"{n}   ({n/len(ROWS):.1%})",va="center",ha="left",fontsize=28,fontweight="bold")
ax.set_xlim(0,len(ROWS)*1.24); ax.grid(axis="y",visible=False)
ax.set_title("The Accountability Pipeline — attrition at each stage",pad=26)
ax.set_xlabel("Findings")
save(fig,"20_accountability_pipeline_funnel.png")
print(f"\n{len(os.listdir(OUT))} files in {OUT}")
