#!/usr/bin/env python3
"""NeurIPS Figure 2 — the coding rule and the headline outcome in one panel.

Absorbs three figures from the old set:
  21  severity x action level matrix
  08  action level distribution   -> the column marginal
  10  proportionality by severity -> the row marginals
  26  the Action Level definitions -> the legend strip beneath

The grid IS the proportionality rule, so every cell is labelled with the outcome it derives and
filled with that outcome's colour. Cell shade carries magnitude within the outcome colour. The
outcome in each cell is read from the rows themselves and asserted against the rule, so the figure
cannot drift from the workbook.
"""
import os, sys, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds
from palette import *

OUT = os.path.expanduser("~/MATS/Research/AISI_Evals/charts/neurips")
plt.rcParams.update({"figure.dpi": 200, "savefig.dpi": 200, "font.family": "DejaVu Sans",
                     "figure.facecolor": "white", "axes.facecolor": "white",
                     "savefig.facecolor": "white"})
INK, SOFT, FAINT = "#111111", "#4A4A4A", "#8A959F"

R = ds.rows()
A = [r for r in R if r["Eval? (trackable)"] == "yes" and r["Action Trackable?"] == "yes"]
AL = ["Substantive", "Partial", "Acknowledged", "None"]
SV = ["C1", "C2"]
RULE = {("C1", "Substantive"): "Proportionate", ("C1", "Partial"): "Under-response (gap)",
        ("C1", "Acknowledged"): "Under-response (gap)", ("C1", "None"): "Accountability gap (no action)",
        ("C2", "Substantive"): "Proportionate", ("C2", "Partial"): "Proportionate",
        ("C2", "Acknowledged"): "Under-response (gap)", ("C2", "None"): "Accountability gap (no action)"}
SHORT = {"Proportionate": "PROPORTIONATE", "Under-response (gap)": "UNDER-RESPONSE",
         "Accountability gap (no action)": "ACCOUNTABILITY GAP"}
DEFN = {"Substantive": "a specific mitigation or\ndeployment decision",
        "Partial": "interim or incomplete, or\nclaimed but unverifiable",
        "Acknowledged": "referenced, with no\naction specified",
        "None": "nothing located after a\nfive-source battery"}

M = {(s, a): sum(1 for r in A if r["Severity (C1/C2) majority"] == s and r["Action Level"] == a)
     for s in SV for a in AL}
for s in SV:
    for a in AL:
        got = {r["Proportionality"] for r in A
               if r["Severity (C1/C2) majority"] == s and r["Action Level"] == a}
        assert got <= {RULE[(s, a)]}, f"{s}/{a} disagrees with the rule: {got}"
rowN = {s: sum(M[(s, a)] for a in AL) for s in SV}
colN = {a: sum(M[(s, a)] for s in SV) for a in AL}
mx = max(M.values())

fig = plt.figure(figsize=(16.0, 9.0))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(100, 0); ax.axis("off")

L, TOPY, CW, CH = 18.0, 29.0, 19.5, 23.0
ax.text(2.0, 9.0, "Severity × company response determines the outcome",
        fontsize=33.5, fontweight="bold", color=INK, va="baseline")
ax.text(2.0, 16.5, "Proportionality is a function of these two columns and nothing else. "
        "The bar is severity-relative: C1 needs a substantive response, C2 needs at least a partial one.",
        fontsize=17.4, color=SOFT, va="baseline")

for j, a in enumerate(AL):
    ax.text(L + j * CW + CW / 2, TOPY - 6.4, a, ha="center", fontsize=22.8, fontweight="bold", color=INK)
    ax.text(L + j * CW + CW / 2, TOPY - 2.6, f"{colN[a]} of {len(A)}", ha="center",
            fontsize=16.1, color=FAINT)
for i, s in enumerate(SV):
    ax.text(L - 2.0, TOPY + i * CH + CH / 2 - 1.6, s, ha="right", va="center",
            fontsize=29.5, fontweight="bold", color=SEV[s])
    ax.text(L - 2.0, TOPY + i * CH + CH / 2 + 3.0, "significant risk" if s == "C1" else "low risk",
            ha="right", va="center", fontsize=16.1, color=SOFT)
    ax.text(L - 2.0, TOPY + i * CH + CH / 2 + 6.6, f"n = {rowN[s]}", ha="right", va="center",
            fontsize=14.7, color=FAINT)
    for j, a in enumerate(AL):
        n = M[(s, a)]; out = RULE[(s, a)]; col = PROP[out]
        w = 0.80 - 0.66 * (n / mx)
        x0, y0 = L + j * CW, TOPY + i * CH
        ax.add_patch(Rectangle((x0, y0), CW - 0.7, CH - 0.7, facecolor=tint(col, w),
                               edgecolor="white", linewidth=2.5))
        ink = "white" if w < 0.34 else INK
        ax.text(x0 + (CW - 0.7) / 2, y0 + 7.2, f"{n}", ha="center", va="center",
                fontsize=44.2, fontweight="bold", color=ink)
        ax.text(x0 + (CW - 0.7) / 2, y0 + 12.4, f"{n/rowN[s]:.0%} of {s}", ha="center",
                va="center", fontsize=14.7, color=ink)
        ax.text(x0 + (CW - 0.7) / 2, y0 + 16.6, SHORT[out], ha="center", va="center",
                fontsize=14.1, fontweight="bold",
                color="white" if ink == "white" else shade(col, 0.22))

# definitions strip — absorbs figure 26
DY = TOPY + 2 * CH + 4.5
ax.text(L, DY, "ACTION LEVEL", fontsize=14.7, fontweight="bold", color=FAINT, va="baseline")
for j, a in enumerate(AL):
    x0 = L + j * CW
    ax.add_patch(Rectangle((x0, DY + 1.6), 3.0, 2.6, facecolor=ACTION[a], edgecolor="none"))
    ax.text(x0 + 4.0, DY + 3.4, DEFN[a], ha="left", va="center", fontsize=13.4,
            color=SOFT, linespacing=1.4)

short = sum(M[(s, a)] for s in SV for a in AL if RULE[(s, a)] != "Proportionate")
c1short = sum(M[("C1", a)] for a in AL if RULE[("C1", a)] != "Proportionate")
ax.text(2.0, 92.0, f"Outcome is derived, never hand-entered. Of the {rowN['C1']} significant-risk "
        f"findings, {c1short} ({c1short/rowN['C1']:.0%}) fall short of a proportionate response; "
        f"across all {len(A)} Tier A findings, {short} do.",
        fontsize=14.7, color=FAINT, va="baseline")

p = os.path.join(OUT, "fig2_severity_x_action.png")
fig.savefig(p, bbox_inches="tight", pad_inches=0.25)
plt.close(fig)
print(f"wrote {p}")
for s in SV: print(f"  {s}: " + " · ".join(f"{a} {M[(s,a)]}" for a in AL) + f"  (n={rowN[s]})")
