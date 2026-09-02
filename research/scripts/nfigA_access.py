#!/usr/bin/env python3
"""Appendix figure — access type, two panels (merges old 03 and 16).

Left  : how the corpus divides by access type (old 03).
Right : the no-response rate within each access type for significant-risk Tier A findings (old 16).

The right panel carries the paper's most actionable association, so the caption must state the
confound: companies choose who gets pre-deployment access, and pre-deployment findings are answered
in the launch card partly by construction.
"""
import os, sys, collections, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds
from palette import *

OUT = os.path.expanduser("~/MATS/Research/AISI_Evals/charts/neurips")
plt.rcParams.update({"figure.dpi": 200, "savefig.dpi": 200, "font.family": "DejaVu Sans",
                     "figure.facecolor": "white", "axes.facecolor": "white",
                     "savefig.facecolor": "white"})
R = ds.rows()
A = [r for r in R if r["Eval? (trackable)"] == "yes" and r["Action Trackable?"] == "yes"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]
ORDER = ["Pre-deployment", "Post-deployment", "Mixed", "Aggregate", "N/A"]
c = collections.Counter(r["Access Type"] for r in R)
keys = [k for k in ORDER if c[k]]

# (a) carries five categories against (b)'s three, so it needs the wider panel or the
# two-line tick labels collide.
fig, (a1, a2) = plt.subplots(1, 2, figsize=(17.0, 6.0),
                             gridspec_kw={"width_ratios": [1.3, 1.0]})

a1.bar(range(len(keys)), [c[k] for k in keys], color=[ACCESS[k] for k in keys],
       width=0.62, zorder=3)
for i, k in enumerate(keys):
    a1.text(i, c[k] + max(c.values()) * 0.02, f"{c[k]}\n{c[k]/len(R):.0%}", ha="center",
            va="bottom", fontsize=18.5, fontweight="bold", linespacing=1.3)
a1.set_xticks(range(len(keys))); a1.set_xticklabels([k.replace("-", "-\n") for k in keys], fontsize=18.5)
a1.set_ylim(0, max(c.values()) * 1.22); a1.set_ylabel("Findings", fontsize=18.5)
a1.set_title(f"(a)  Corpus by access type  (n = {len(R):,})", fontsize=21.3, pad=14, loc="left")
a1.grid(axis="y", color=GRID, zorder=0); a1.set_axisbelow(True)
for s in ("top", "right"): a1.spines[s].set_visible(False)

sub = [k for k in ORDER if sum(1 for r in H if r["Access Type"] == k) >= 5]
rate, ns = [], []
for k in sub:
    g = [r for r in H if r["Access Type"] == k]
    ns.append(len(g)); rate.append(sum(1 for r in g if r["Action Level"] == "None") / len(g))
a2.bar(range(len(sub)), rate, color=[RED if v > 0.5 else GREEN for v in rate], width=0.62, zorder=3)
for i, (v, n) in enumerate(zip(rate, ns)):
    a2.text(i, v + 0.025, f"{v:.0%}", ha="center", va="bottom", fontsize=24.1, fontweight="bold")
    a2.text(i, 0.02, f"n = {n}", ha="center", va="bottom", fontsize=17.0, color="white")
a2.set_xticks(range(len(sub))); a2.set_xticklabels([k.replace("-", "-\n") for k in sub], fontsize=18.5)
a2.set_ylim(0, 1.05); a2.set_yticks([0, .25, .5, .75, 1.0])
a2.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=17.0)
a2.set_ylabel("No documented response", fontsize=18.5)
a2.set_title("(b)  Significant-risk findings with no response, by access type",
             fontsize=21.3, pad=14, loc="left")
a2.grid(axis="y", color=GRID, zorder=0); a2.set_axisbelow(True)
for s in ("top", "right"): a2.spines[s].set_visible(False)

fig.text(0.012, 0.012, "Association, not causation: companies choose who receives pre-deployment "
         "access, and a pre-deployment finding is answered in the launch card partly by construction.",
         fontsize=15.6, color="#4A4A4A")
fig.subplots_adjust(left=0.06, right=0.99, top=0.90, bottom=0.17, wspace=0.22)
p = os.path.join(OUT, "figA2_access_type.png")
fig.savefig(p, bbox_inches="tight", pad_inches=0.25); plt.close(fig)
print(f"wrote {p}")
print("  corpus:", {k: c[k] for k in keys})
print("  no-response rate:", {k: f"{v:.1%} (n={n})" for k, v, n in zip(sub, rate, ns)})
