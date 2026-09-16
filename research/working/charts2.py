#!/usr/bin/env python3
"""Non-bar figures for AISIEVAL: donut, lollipops, line, dot plot, heatmaps, stacked area, scatter."""
import os, re, collections, datetime, textwrap
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np, openpyxl
OUT=os.path.expanduser("~/MATS/Research/AISI_Evals/charts")
plt.rcParams.update({"figure.dpi":200,"savefig.dpi":200,"font.family":"DejaVu Sans",
 "axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":"#333333","axes.linewidth":2.2,
 "figure.facecolor":"white","axes.facecolor":"white","savefig.facecolor":"white",
 "axes.titlesize":38,"axes.labelsize":30,"xtick.labelsize":26,"ytick.labelsize":26,
 "xtick.major.width":2.2,"ytick.major.width":2.2,"axes.grid":True,"grid.color":"#DDDDDD",
 "grid.linewidth":1.6,"axes.axisbelow":True})
GREEN,AMBER,ORANGE,RED="#00A36C","#E8A80C","#D2570A","#E03131"
BLUE,SKY,PURPLE,TEAL,MAGENTA,LIME="#0A6EBD","#4FADEE","#7B4FBF","#00A6A6","#D4267D","#7CB518"
TIER={"A":"#E8453C","B":"#F5A623","C":"#2D9CDB"}
def norm(v):
    if v is None: return ""
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return str(v).strip()
ws=openpyxl.load_workbook(os.path.expanduser("~/MATS/Research/AISI_Evals/dataset/AISIEVAL.xlsx"),data_only=True)["AISIEVAL"]
hdr=[norm(c.value) for c in ws[1]]
R=[{h:norm(ws.cell(r,i).value) for i,h in enumerate(hdr,1) if h} for r in range(2,ws.max_row+1)]
R=[r for r in R if r.get("Finding ID")]
tier=lambda r:("A" if r.get("Action Trackable?")=="yes" else "B" if r.get("Eval? (trackable)")=="yes" else "C")
A=[r for r in R if tier(r)=="A"]; H=[r for r in A if r.get("Severity (C1/C2) majority")=="C1"]
isgap=lambda r: r.get("Proportionality")=="Accountability gap (no action)"
def save(fig,n):
    fig.savefig(os.path.join(OUT,n),bbox_inches="tight",pad_inches=0.42); plt.close(fig); print("  ",n)

# ---- 07 DONUT: tier -------------------------------------------------------
c=collections.Counter(tier(r) for r in R)
fig,ax=plt.subplots(figsize=(14,11))
vals=[c["A"],c["B"],c["C"]]
labs=["Tier A\naccountability-relevant","Tier B\nno accountable party","Tier C\nnot an empirical finding"]
w,_,at=ax.pie(vals,colors=[TIER["A"],TIER["B"],TIER["C"]],startangle=90,counterclock=False,
    wedgeprops=dict(width=0.42,edgecolor="white",linewidth=5),
    autopct=lambda p:f"{p:.0f}%\n({int(round(p*sum(vals)/100))})",pctdistance=0.79,
    textprops=dict(fontsize=25,fontweight="bold",color="white"))
ax.text(0,0.06,f"{len(R):,}",ha="center",va="center",fontsize=54,fontweight="bold",color="#111111")
ax.text(0,-0.16,"findings",ha="center",va="center",fontsize=25,color="#555555")
ax.legend(w,labs,loc="upper center",bbox_to_anchor=(0.5,0.02),ncol=3,fontsize=19,frameon=False,handlelength=1.6)
ax.set_title("Tier Distribution",pad=18)
save(fig,"07_tier_distribution.png")

# ---- 01 LOLLIPOP: institutions -------------------------------------------
c=collections.Counter(r["Institution"] for r in R).most_common(18)
fig,ax=plt.subplots(figsize=(18,15))
y=np.arange(len(c))[::-1]; v=[n for _,n in c]
ax.hlines(y,0,v,color="#B8CCE0",linewidth=7,zorder=2)
ax.scatter(v,y,s=620,color=BLUE,zorder=3,edgecolor="white",linewidth=3)
for yy,vv in zip(y,v): ax.text(vv+4,yy,f"{vv}",va="center",fontsize=24,fontweight="bold",color="#111111")
ax.set_yticks(y); ax.set_yticklabels(["\n".join(textwrap.wrap(k,32)) for k,_ in c],fontsize=23)
ax.set_xlim(0,max(v)*1.13); ax.grid(axis="y",visible=False)
ax.set_title(f"Findings per Evaluating Institution (top 18 of {len({r['Institution'] for r in R})})",pad=22)
ax.set_xlabel("Findings")
save(fig,"01_findings_per_institution.png")

# ---- 11 LOLLIPOP: domains -------------------------------------------------
d=collections.Counter()
for r in R:
    for p in [x.strip() for x in r.get("Domain","").split(";") if x.strip()]: d[p]+=1
c=d.most_common()
fig,ax=plt.subplots(figsize=(17,13))
y=np.arange(len(c))[::-1]; v=[n for _,n in c]
pal=[BLUE,ORANGE,TEAL,PURPLE,GREEN,MAGENTA,AMBER,SKY,LIME,RED]
ax.hlines(y,0,v,color="#DDDDDD",linewidth=6,zorder=2)
ax.scatter(v,y,s=560,color=[pal[i%len(pal)] for i in range(len(c))],zorder=3,edgecolor="white",linewidth=3)
for yy,vv in zip(y,v): ax.text(vv+5,yy,f"{vv}",va="center",fontsize=23,fontweight="bold")
ax.set_yticks(y); ax.set_yticklabels([k for k,_ in c],fontsize=23)
ax.set_xlim(0,max(v)*1.13); ax.grid(axis="y",visible=False)
ax.set_title("Findings per Risk Domain   (multi-label; total exceeds n)",pad=22); ax.set_xlabel("Findings")
save(fig,"11_domain_distribution.png")

# ---- 10 100% STACKED: proportionality by severity -------------------------
order=["Proportionate","Under-response (gap)","Accountability gap (no action)"]
COL=[GREEN,AMBER,ORANGE]
fig,ax=plt.subplots(figsize=(19,7.6))
rows=[("C1  significant risk",[r for r in A if r["Severity (C1/C2) majority"]=="C1"]),
      ("C2  low risk",       [r for r in A if r["Severity (C1/C2) majority"]=="C2"])]
for i,(lab,S) in enumerate(rows):
    left=0
    for k,col in zip(order,COL):
        n=sum(1 for r in S if r["Proportionality"]==k); frac=n/len(S)
        ax.barh(i,frac,left=left,color=col,height=0.55,zorder=3)
        if frac>0.045:
            ax.text(left+frac/2,i,f"{n}\n{frac:.0%}",ha="center",va="center",fontsize=23,
                    fontweight="bold",color="white",linespacing=1.3)
        left+=frac
ax.set_yticks(range(len(rows))); ax.set_yticklabels([f"{l}\n(n={len(S)})" for l,S in rows],fontsize=25)
ax.invert_yaxis(); ax.set_xlim(0,1); ax.xaxis.set_major_formatter(PercentFormatter(1.0))
ax.grid(axis="y",visible=False)
hs=[plt.Rectangle((0,0),1,1,color=c) for c in COL]
ax.legend(hs,["Proportionate","Under-response (gap)","Accountability gap (no action)"],
          loc="upper center",bbox_to_anchor=(0.5,-0.16),ncol=3,fontsize=21,frameon=False)
ax.set_title("Proportionality Outcome by Severity (Tier A)",pad=22)
ax.set_xlabel("Share of findings")
save(fig,"10_proportionality_by_severity.png")

# ---- 15 LINE: gap rate over time -----------------------------------------
yrs=sorted({r["Publication Date"][:4] for r in H})
rate=[];ns=[]
for y_ in yrs:
    S=[r for r in H if r["Publication Date"].startswith(y_)]
    rate.append(sum(1 for r in S if isgap(r))/len(S)); ns.append(len(S))
fig,ax=plt.subplots(figsize=(15,10))
ax.plot(range(len(yrs)),rate,color=ORANGE,linewidth=6,marker="o",markersize=24,
        markerfacecolor="white",markeredgewidth=6,zorder=3)
for i,(v,n) in enumerate(zip(rate,ns)):
    ax.annotate(f"{v:.0%}",(i,v),textcoords="offset points",xytext=(0,30),ha="center",
                fontsize=29,fontweight="bold",color=ORANGE)
ax.set_xticks(range(len(yrs))); ax.set_xticklabels([f"{y_}\n(n={n})" for y_,n in zip(yrs,ns)],fontsize=26)
ax.set_ylim(0,1.02); ax.yaxis.set_major_formatter(PercentFormatter(1.0)); ax.grid(axis="x",visible=False)
ax.set_title("Accountability Gap Rate over Time (Tier A, C1)",pad=22)
ax.set_ylabel("Share with no documented action")
save(fig,"15_gap_rate_by_year.png")

# ---- 16 DOT PLOT: gap rate by access type --------------------------------
keys=[k for k in ("Pre-deployment","Post-deployment","Mixed","Aggregate") if any(r.get("Access Type")==k for r in H)]
vals=[];ns=[]
for k in keys:
    S=[r for r in H if r.get("Access Type")==k]
    vals.append(sum(1 for r in S if isgap(r))/len(S)); ns.append(len(S))
o=np.argsort(vals); keys=[keys[i] for i in o]; vals=[vals[i] for i in o]; ns=[ns[i] for i in o]
fig,ax=plt.subplots(figsize=(17,9))
y=np.arange(len(keys))
overall=sum(1 for r in H if isgap(r))/len(H)
ax.axvline(overall,color="#999999",linestyle="--",linewidth=3,zorder=1)
ax.text(overall,len(keys)-0.35,f"  overall {overall:.0%}",fontsize=21,color="#666666",va="top")
ax.hlines(y,0,vals,color="#E2E2E2",linewidth=7,zorder=2)
ax.scatter(vals,y,s=900,color=[GREEN if v<0.4 else AMBER if v<0.7 else ORANGE for v in vals],
           zorder=3,edgecolor="white",linewidth=4)
for i,v in enumerate(vals): ax.text(v+0.028,i,f"{v:.0%}",va="center",fontsize=27,fontweight="bold")
ax.set_yticks(y); ax.set_yticklabels([f"{k}\n(n={n})" for k,n in zip(keys,ns)],fontsize=24)
ax.set_xlim(0,1.14); ax.xaxis.set_major_formatter(PercentFormatter(1.0)); ax.grid(axis="y",visible=False)
ax.set_title("Accountability Gap Rate by Model Access Type (Tier A, C1)",pad=22,fontsize=35)
ax.set_xlabel("Share with no documented action")
save(fig,"16_gap_rate_by_access_type.png")

# ---- 21 HEATMAP: severity x action level ---------------------------------
AL=["Substantive","Partial","Acknowledged","None"]
SV=["C1","C2"]
M=np.array([[sum(1 for r in A if r["Severity (C1/C2) majority"]==s and r["Action Level"]==a) for a in AL] for s in SV])
fig,ax=plt.subplots(figsize=(16,7.6))
im=ax.imshow(M,cmap="YlOrRd",aspect="auto")
ax.set_xticks(range(len(AL))); ax.set_xticklabels(AL,fontsize=26)
ax.set_yticks(range(len(SV))); ax.set_yticklabels(["C1\nsignificant risk","C2\nlow risk"],fontsize=25)
for i in range(len(SV)):
    for j in range(len(AL)):
        v=M[i,j]
        ax.text(j,i,f"{v}\n{v/M[i].sum():.0%}",ha="center",va="center",fontsize=27,fontweight="bold",
                color="white" if v>M.max()*0.55 else "#111111",linespacing=1.3)
ax.set_title("Severity × Company Response (Tier A)",pad=22)
ax.set_xlabel("Action Level"); ax.grid(False)
cb=fig.colorbar(im,ax=ax,fraction=0.032,pad=0.02); cb.ax.tick_params(labelsize=20); cb.set_label("Findings",size=22)
save(fig,"21_severity_x_action_heatmap.png")

# ---- 22 HEATMAP: domain x outcome (Tier A) -------------------------------
doms=[d0 for d0,_ in collections.Counter(
    p for r in A for p in [x.strip() for x in r.get("Domain","").split(";") if x.strip()]).most_common(9)]
OUTC=["Proportionate","Under-response (gap)","Accountability gap (no action)"]
M=np.zeros((len(doms),3))
for i,d0 in enumerate(doms):
    S=[r for r in A if d0 in [x.strip() for x in r.get("Domain","").split(";")]]
    for j,o_ in enumerate(OUTC): M[i,j]=sum(1 for r in S if r["Proportionality"]==o_)
Mp=M/M.sum(axis=1,keepdims=True)
fig,ax=plt.subplots(figsize=(15,12))
im=ax.imshow(Mp,cmap="RdYlGn_r",aspect="auto",vmin=0,vmax=1)
ax.set_xticks(range(3)); ax.set_xticklabels(["Proportionate","Under-\nresponse","Accountability\ngap"],fontsize=23)
ax.set_yticks(range(len(doms)))
ax.set_yticklabels([f"{d0}  (n={int(M[i].sum())})" for i,d0 in enumerate(doms)],fontsize=22)
for i in range(len(doms)):
    for j in range(3):
        ax.text(j,i,f"{int(M[i,j])}\n{Mp[i,j]:.0%}",ha="center",va="center",fontsize=21,fontweight="bold",
                color="white" if Mp[i,j]>0.62 or Mp[i,j]<0.12 else "#111111",linespacing=1.3)
ax.set_title("Outcome Composition by Risk Domain (Tier A)",pad=22,fontsize=34); ax.grid(False)
save(fig,"22_domain_x_outcome_heatmap.png")

# ---- 23 STACKED AREA: findings per year by tier --------------------------
yrs=sorted({r["Publication Date"][:4] for r in R if r.get("Publication Date")})
series={t:[sum(1 for r in R if r["Publication Date"].startswith(y_) and tier(r)==t) for y_ in yrs] for t in "ABC"}
fig,ax=plt.subplots(figsize=(16,10))
ax.stackplot(range(len(yrs)),[series["A"],series["B"],series["C"]],
    colors=[TIER["A"],TIER["B"],TIER["C"]],labels=["Tier A","Tier B","Tier C"],alpha=0.95,edgecolor="white",linewidth=3)
tot=[sum(series[t][i] for t in "ABC") for i in range(len(yrs))]
for i,v in enumerate(tot): ax.text(i,v+12,str(v),ha="center",fontsize=25,fontweight="bold")
ax.set_xticks(range(len(yrs))); ax.set_xticklabels(yrs,fontsize=27)
ax.set_ylim(0,max(tot)*1.16); ax.grid(axis="x",visible=False)
ax.legend(loc="upper left",fontsize=23,frameon=False)
ax.set_title("Corpus Growth by Publication Year and Tier",pad=22)
ax.set_ylabel("Findings")
save(fig,"23_corpus_growth_by_tier.png")

# ---- 24 SCATTER: evaluator volume vs gap rate ----------------------------
pts=[]
for inst,S in collections.defaultdict(list,{k:[r for r in H if r["Institution"]==k]
        for k in {r["Institution"] for r in H}}).items():
    if len(S)>=4: pts.append((inst,len(S),sum(1 for r in S if isgap(r))/len(S)))
pts.sort(key=lambda p:-p[1])
fig,ax=plt.subplots(figsize=(17,11))
xs=[p[1] for p in pts]; ys=[p[2] for p in pts]
ax.axhline(sum(1 for r in H if isgap(r))/len(H),color="#999999",linestyle="--",linewidth=3,zorder=1)
ax.text(max(xs)*1.0,sum(1 for r in H if isgap(r))/len(H)+0.025,"corpus average",fontsize=20,color="#666666",ha="right")
ax.scatter(xs,ys,s=[80+p[1]*26 for p in pts],color=BLUE,alpha=0.78,edgecolor="white",linewidth=3,zorder=3)
for inst,n,g in pts:
    ax.annotate(inst.split("(")[0].strip()[:22],(n,g),textcoords="offset points",xytext=(0,26),
                ha="center",fontsize=18,color="#111111")
ax.set_xlim(0,max(xs)*1.22); ax.set_ylim(-0.05,1.16)
ax.yaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_title("Evaluator Volume vs Accountability Gap Rate (Tier A, C1; n≥4)",pad=22,fontsize=33)
ax.set_xlabel("Tier A C1 findings published"); ax.set_ylabel("Share with no documented action")
save(fig,"24_evaluator_volume_vs_gap.png")
print(f"\n{len(os.listdir(OUT))} files in {OUT}")
