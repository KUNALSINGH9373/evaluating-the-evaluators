#!/usr/bin/env python3
"""Schematic funnel hero for AISIEVAL. The institution tree lives in tree.py."""
import os
import dataset_source, collections, datetime, textwrap
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np, openpyxl
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palette import *   # single source of colour truth

OUT = CHARTS_OUT; os.makedirs(OUT,exist_ok=True)
plt.rcParams.update({"figure.dpi":200,"savefig.dpi":200,"font.family":"DejaVu Sans",
 "figure.facecolor":"white","axes.facecolor":"white","savefig.facecolor":"white"})
L1,L2,L3="#9BCBEA","#4FA7DC","#2E7CA8"
# GREEN / AMBER / RED come from palette.py
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
c=collections.Counter(r["Proportionality"] for r in H)
gap,und,pro=c["Accountability gap (no action)"],c["Under-response (gap)"],c["Proportionate"]
nrep=len({r["Report ID"] for r in R if r.get("Report ID")}); ninst=len({r["Institution"] for r in R})

# ---------------------------------------------------------------- HERO
fig,ax=plt.subplots(figsize=(20,8.6)); ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis("off")
ax.text(2,97,f"From {len(R):,} public findings to the accountability gap",
        fontsize=31,color="#111111",va="top")
# Plain-language labels throughout: no tier letters, no severity codes.
# The span was hard-coded "Jan 2023 - Jul 2026" and contradicted both the extended corpus window
# and this figure's own cutoff footer. Derive it from the data so it cannot drift again.
_d=sorted(r["Publication Date"][:10] for r in R if r.get("Publication Date"))
_MON=["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
_span=f"{_MON[int(_d[0][5:7])]} {_d[0][:4]} \u2013 {_MON[int(_d[-1][5:7])]} {_d[-1][:4]}"
BOX=[(2.0,f"{len(R):,}","published\nfindings",L1,INK,
      f"{nrep} reports \u00b7 {ninst} evaluators\n{_span}"),
     (23.0,f"{len(A)}","names a company\nor model",L2,"white",
      "a specific developer is named,\nso a response could\nreasonably be expected"),
     (44.0,f"{len(H)}","significant risk",L3,"white",
      "graded the more serious of\ntwo risk levels by a\n3-model severity ensemble")]
W,Hh,Y=18.0,25.0,42.0
for x,big,sub,col,txt,foot in BOX:
    ax.add_patch(FancyBboxPatch((x,Y),W,Hh,boxstyle="round,pad=0,rounding_size=1.6",
                 facecolor=col,edgecolor="none",transform=ax.transData))
    ax.text(x+W/2,Y+Hh*0.64,big,ha="center",va="center",fontsize=40,color=txt)
    ax.text(x+W/2,Y+Hh*0.24,sub,ha="center",va="center",fontsize=18,color=txt,linespacing=1.3)
    ax.text(x+W/2,Y-3.6,foot,ha="center",va="top",fontsize=15,color=INK_2,linespacing=1.55)
for x0,lab in ((20.3,"filter"),(41.3,"severity")):
    ax.add_patch(FancyArrowPatch((x0,Y+Hh/2),(x0+2.4,Y+Hh/2),arrowstyle="-|>",mutation_scale=26,
                 linewidth=2.4,color=MUTED))
    ax.text(x0+1.2,Y+Hh+2.4,lab,ha="center",va="bottom",fontsize=15,color=INK_2)
ax.add_patch(FancyArrowPatch((62.4,Y+Hh/2),(65.4,Y+Hh/2),arrowstyle="-|>",mutation_scale=26,
             linewidth=2.4,color=MUTED))
ax.text(65.8,Y+Hh+2.4,"trace response",ha="right",va="bottom",fontsize=15,color=INK_2)

# proportional outcome bar
BX,BW,BY,BH=66.5,8.0,22.0,54.0
tot=len(H); y=BY
for n,col,lab in ((pro,GREEN,"Proportionate"),(und,AMBER,"Under-response"),(gap,RED,"No action")):
    h=BH*n/tot
    ax.add_patch(plt.Rectangle((BX,y),BW,h,facecolor=col,edgecolor="none"))
    ax.text(BX+BW/2,y+h/2,str(n),ha="center",va="center",fontsize=24,color="white")
    ax.text(BX+BW+1.4,y+h/2,lab,ha="left",va="center",fontsize=18,color=col)
    y+=h
ax.text(BX+BW/2,BY+BH+2.6,f"outcomes (n = {tot})",ha="center",fontsize=18,color="#111111")
# bracket over the two segments that fall short, labelled with the percentage only
gy0=BY+BH*pro/tot
ax.plot([88.6,90.1,90.1,88.6],[gy0,gy0,BY+BH,BY+BH],color=RED,linewidth=2.4,solid_joinstyle="miter")
ax.text(91.4,(gy0+BY+BH)/2+7.5,"FALLS SHORT\nOF THE\nSTANDARD",ha="left",va="center",
        fontsize=18,color=RED,linespacing=1.45)
ax.text(91.4,(gy0+BY+BH)/2-8.0,f"{(gap+und)/tot:.0%}",ha="left",va="center",
        fontsize=36,color=RED,fontweight="bold")
ax.text(2,10.5,"Boxes are schematic (not to scale); the outcome bar is proportional. A finding falls short when the named company\n"
        "shows no located public response (red) or only a partial / acknowledged one (orange). "
        "Corpus cutoff 29 August 2026.",
        fontsize=15.5,color=INK_2,va="top",linespacing=1.6)
fig.savefig(os.path.join(OUT,"00_title_hero.png"),bbox_inches="tight",pad_inches=0.35); plt.close(fig)
print("  00_title_hero.png  (schematic funnel)")

# The institution tree lives in tree.py. It used to be here, and a stale copy of this file
# twice reverted it to a top-down layout with colliding leaf labels. Do not re-add it.
