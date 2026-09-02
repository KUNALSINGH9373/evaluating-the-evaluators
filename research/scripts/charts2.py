#!/usr/bin/env python3
"""Non-bar figures for AISIEVAL: donut, lollipops, line, dot plot, heatmaps, stacked area, scatter."""
import os
import dataset_source, re, collections, datetime, textwrap
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np, openpyxl
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palette import *   # single source of colour truth
OUT = CHARTS_OUT
plt.rcParams.update({"figure.dpi":200,"savefig.dpi":200,"font.family":"DejaVu Sans",
 "axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":INK_2,"axes.linewidth":2.2,
 "figure.facecolor":"white","axes.facecolor":"white","savefig.facecolor":"white",
 "axes.titlesize":38,"axes.labelsize":30,"xtick.labelsize":26,"ytick.labelsize":26,
 "xtick.major.width":2.2,"ytick.major.width":2.2,"axes.grid":True,"grid.color":GRID,
 "grid.linewidth":1.6,"axes.axisbelow":True})
SKY=NEUTRAL[2]; PURPLE=NEUTRAL[3]; TEAL=NEUTRAL[0]; MAGENTA=NEUTRAL[5]; LIME=AMBER
TIER={k:TIER_INK[k] for k in "ABC"}
def norm(v):
    if v is None: return ""
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return str(v).strip()
ws=dataset_source.sheet()
hdr=[norm(c.value) for c in ws[1]]
R=[{h:norm(ws.cell(r,i).value) for i,h in enumerate(hdr,1) if h} for r in range(2,ws.max_row+1)]
R=[r for r in R if r.get("Finding ID")]
tier=lambda r:("A" if r.get("Action Trackable?")=="yes" else "B" if r.get("Eval? (trackable)")=="yes" else "C")
A=[r for r in R if tier(r)=="A"]; H=[r for r in A if r.get("Severity (C1/C2) majority")=="C1"]
isgap=lambda r: r.get("Proportionality")=="Accountability gap (no action)"
def save(fig,n):
    fig.savefig(os.path.join(OUT,n),bbox_inches="tight",pad_inches=0.42); plt.close(fig); print("  ",n)

# 07 is a BAR chart, owned by charts.py. A donut lived here and silently overwrote it,
# because charts2.py runs second. Removed 2026-08-18 — do not re-add a second writer
# for a figure another script already owns.

# ---- 01 LOLLIPOP: institutions -------------------------------------------
# Sole owner of this figure. No percentages: 18 shares of a 1,002 corpus round to a column of
# near-identical 3%s that crowd the counts and say nothing. Short names keep every row on one
# line — wrapped labels were colliding with the row above.
c=collections.Counter(r["Institution"] for r in R).most_common(18)
fig,ax=plt.subplots(figsize=(18,16.5))
y=np.arange(len(c))[::-1]; v=[n for _,n in c]
ax.hlines(y,0,v,color="#B8CCE0",linewidth=7,zorder=2)
ax.scatter(v,y,s=620,color=NEUTRAL[0],zorder=3,edgecolor="white",linewidth=3)
for yy,vv in zip(y,v): ax.text(vv+4,yy,f"{vv}",va="center",fontsize=24,fontweight="bold",color="#111111")
ax.set_yticks(y); ax.set_yticklabels([short_inst(k) for k,_ in c],fontsize=23)
ax.set_ylim(-0.75,len(c)-0.25)
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
pal=ramp(10)
ax.hlines(y,0,v,color=GRID,linewidth=6,zorder=2)
ax.scatter(v,y,s=560,color=[pal[i%len(pal)] for i in range(len(c))],zorder=3,edgecolor="white",linewidth=3)
for yy,vv in zip(y,v): ax.text(vv+5,yy,f"{vv}",va="center",fontsize=23,fontweight="bold")
ax.set_yticks(y); ax.set_yticklabels([k for k,_ in c],fontsize=23)
ax.set_xlim(0,max(v)*1.13); ax.grid(axis="y",visible=False)
ax.set_title("Findings per Risk Domain   (multi-label; total exceeds n)",pad=22); ax.set_xlabel("Findings")
save(fig,"11_domain_distribution.png")

# ---- 10 100% STACKED: proportionality by severity -------------------------
order=["Proportionate","Under-response (gap)","Accountability gap (no action)"]
COL=[GREEN,AMBER,RED]
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
ax.plot(range(len(yrs)),rate,color=RED,linewidth=6,marker="o",markersize=24,
        markerfacecolor="white",markeredgewidth=6,zorder=3)
for i,(v,n) in enumerate(zip(rate,ns)):
    ax.annotate(f"{v:.0%}",(i,v),textcoords="offset points",xytext=(0,30),ha="center",
                fontsize=29,fontweight="bold",color=RED)
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
ax.axvline(overall,color=MUTED,linestyle="--",linewidth=3,zorder=1)
ax.text(overall,len(keys)-0.35,f"  overall {overall:.0%}",fontsize=21,color=MUTED,va="top")
ax.hlines(y,0,vals,color=GRID,linewidth=7,zorder=2)
ax.scatter(vals,y,s=900,color=[GREEN if v<0.4 else AMBER if v<0.7 else RED for v in vals],
           zorder=3,edgecolor="white",linewidth=4)
for i,v in enumerate(vals): ax.text(v+0.028,i,f"{v:.0%}",va="center",fontsize=27,fontweight="bold")
ax.set_yticks(y); ax.set_yticklabels([f"{k}\n(n={n})" for k,n in zip(keys,ns)],fontsize=24)
ax.set_xlim(0,1.14); ax.xaxis.set_major_formatter(PercentFormatter(1.0)); ax.grid(axis="y",visible=False)
ax.set_title("Accountability Gap Rate by Model Access Type (Tier A, C1)",pad=22,fontsize=35)
ax.set_xlabel("Share with no documented action")
save(fig,"16_gap_rate_by_access_type.png")

# ---- 21 MATRIX: severity x action level ----------------------------------
# This grid IS the proportionality rule, so every cell is labelled with the outcome it produces
# and filled with that outcome's colour. It previously used a count-magnitude colormap with no
# outcome label, which left the figure descriptive when it could be definitional.
# Cell shade carries magnitude within the outcome colour; the outcome is read from the rows
# themselves and cross-checked against the rule, so the label cannot drift from the workbook.
AL=["Substantive","Partial","Acknowledged","None"]
SV=["C1","C2"]
RULE={("C1","Substantive"):"Proportionate",("C1","Partial"):"Under-response (gap)",
      ("C1","Acknowledged"):"Under-response (gap)",("C1","None"):"Accountability gap (no action)",
      ("C2","Substantive"):"Proportionate",("C2","Partial"):"Proportionate",
      ("C2","Acknowledged"):"Under-response (gap)",("C2","None"):"Accountability gap (no action)"}
SHORT={"Proportionate":"Proportionate","Under-response (gap)":"Under-response",
       "Accountability gap (no action)":"Accountability gap"}
M=np.array([[sum(1 for r in A if r["Severity (C1/C2) majority"]==s and r["Action Level"]==a) for a in AL] for s in SV])
for s in SV:
    for a in AL:
        got={r["Proportionality"] for r in A
             if r["Severity (C1/C2) majority"]==s and r["Action Level"]==a}
        assert got <= {RULE[(s,a)]}, f"cell {s}/{a} disagrees with the rule: {got}"
fig,ax=plt.subplots(figsize=(17,9.2))
mx=M.max()
for i in range(len(SV)):
    for j in range(len(AL)):
        v=M[i,j]; out=RULE[(SV[i],AL[j])]; base=PROP[out]
        shade_w=0.80-0.68*(v/mx)                      # heavier fill = more findings
        ax.add_patch(plt.Rectangle((j-0.5,i-0.5),1,1,facecolor=tint(base,shade_w),
                                   edgecolor="white",linewidth=4,zorder=2))
        ink="white" if shade_w<0.34 else "#111111"
        ax.text(j,i-0.20,f"{v}",ha="center",va="center",fontsize=40,fontweight="bold",
                color=ink,zorder=3)
        ax.text(j,i+0.09,f"{v/M[i].sum():.0%} of {SV[i]}",ha="center",va="center",fontsize=19,
                color=ink,zorder=3)
        ax.text(j,i+0.30,SHORT[out].upper(),ha="center",va="center",fontsize=17,
                fontweight="bold",color=shade(base,0.20) if ink=="#111111" else "white",zorder=3)
ax.set_xlim(-0.5,len(AL)-0.5); ax.set_ylim(len(SV)-0.5,-0.5); ax.set_aspect("auto")
ax.set_xticks(range(len(AL))); ax.set_xticklabels(AL,fontsize=26)
ax.set_yticks(range(len(SV))); ax.set_yticklabels(["C1\nsignificant risk","C2\nlow risk"],fontsize=25)
ax.tick_params(length=0)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_title("Severity \u00d7 Company Response (Tier A)",pad=22)
ax.set_xlabel("Action Level"); ax.grid(False)
hand=[plt.Rectangle((0,0),1,1,facecolor=PROP[o]) for o in
      ("Proportionate","Under-response (gap)","Accountability gap (no action)")]
ax.legend(hand,["Proportionate","Under-response","Accountability gap"],loc="upper center",
          bbox_to_anchor=(0.5,-0.24),ncol=3,frameon=False,fontsize=21)
# Reading order below the grid is x-label, then legend, then footnote — the footnote used to be
# pinned to the figure floor and collided with the x-label.
fig.subplots_adjust(bottom=0.30)
fig.text(0.5,0.018,"Outcome is derived from severity \u00d7 action level, never hand-entered: "
         "C1 needs a Substantive response to be proportionate, C2 needs at least a Partial one.",
         fontsize=15,color=INK_2,ha="center")
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
# RdYlGn_r encoded VALENCE on a magnitude scale, so a "Proportionate 0%" cell rendered dark green
# — reading as "good" when 0% proportionate is the worst possible outcome. palette.py SEQ is the
# documented ramp for heatmaps: magnitude only, never valence. Column headers carry the valence.
im=ax.imshow(Mp,cmap=SEQ,aspect="auto",vmin=0,vmax=1)
ax.set_xticks(range(3)); ax.set_xticklabels(["Proportionate","Under-\nresponse","Accountability\ngap"],fontsize=23)
ax.set_yticks(range(len(doms)))
ax.set_yticklabels([f"{d0}  (n={int(M[i].sum())})" for i,d0 in enumerate(doms)],fontsize=22)
for i in range(len(doms)):
    for j in range(3):
        ax.text(j,i,f"{int(M[i,j])}\n{Mp[i,j]:.0%}",ha="center",va="center",fontsize=21,fontweight="bold",
                color="white" if Mp[i,j]>0.55 else INK,linespacing=1.3)
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
ax.axhline(sum(1 for r in H if isgap(r))/len(H),color=MUTED,linestyle="--",linewidth=3,zorder=1)
# The corpus-average label sat on top of the right-most point; park it at the left instead.
ax.text(0.4,sum(1 for r in H if isgap(r))/len(H)-0.045,"corpus average",fontsize=20,color=MUTED,ha="left")
ax.scatter(xs,ys,s=[80+p[1]*26 for p in pts],color=NEUTRAL[0],alpha=0.78,edgecolor="white",linewidth=3,zorder=3)
ax.set_xlim(0,max(xs)*1.22); ax.set_ylim(-0.05,1.16)

# Every label used a fixed (0,+26) offset, so co-located evaluators printed on top of one another
# ("RedwoAdpolboRResearch"). Try candidate offsets around each point and take the first that
# collides with nothing already placed, measuring real rendered text boxes.
fig.canvas.draw()
placed=[]
CAND=[(0,26),(0,-34),(14,14),(-14,14),(14,-24),(-14,-24),(0,46),(0,-54),(26,0),(-26,0)]
for inst,n,g in pts:
    label=short_inst(inst).split("(")[0].strip()
    best=None
    for dx,dy in CAND:
        ha="center" if dx==0 else ("left" if dx>0 else "right")
        tx=ax.annotate(label,(n,g),textcoords="offset points",xytext=(dx,dy),
                       ha=ha,fontsize=18,color=INK,zorder=4)
        fig.canvas.draw()
        bb=tx.get_window_extent().expanded(1.04,1.18)
        if not any(bb.overlaps(b) for b in placed):
            placed.append(bb); best=tx; break
        tx.remove()
    if best is None:            # every candidate collided — keep it, offset furthest out
        best=ax.annotate(label,(n,g),textcoords="offset points",xytext=(0,62),
                         ha="center",fontsize=18,color=INK,zorder=4)
        fig.canvas.draw(); placed.append(best.get_window_extent().expanded(1.04,1.18))
ax.yaxis.set_major_formatter(PercentFormatter(1.0))
ax.set_title("Evaluator Volume vs Accountability Gap Rate (Tier A, C1; n≥4)",pad=22,fontsize=33)
ax.set_xlabel("Tier A C1 findings published"); ax.set_ylabel("Share with no documented action")
save(fig,"24_evaluator_volume_vs_gap.png")
print(f"\n{len(os.listdir(OUT))} files in {OUT}")
