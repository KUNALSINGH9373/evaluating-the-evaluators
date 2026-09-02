#!/usr/bin/env python3
"""NeurIPS Figure 1 — the whole pipeline in one panel.

Absorbs four separate figures from the old set:
  20  the accountability funnel (corpus -> Tier A -> C1 -> outcome)
  07  the tier distribution
  17  the severity classification
  04  the headline outcome distribution

The old hero showed the funnel and nothing else, so tier and severity had to be argued from two
more figures. Here each gate carries its own split inline, and the outcome bar is proportional, so
one panel answers: how many findings, how many are accountability-relevant, how many are severe,
and what happened to them.
"""
import os, sys, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds
from palette import *

OUT = os.path.expanduser("~/MATS/Research/AISI_Evals/charts/neurips")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 200, "savefig.dpi": 200, "font.family": "DejaVu Sans",
                     "figure.facecolor": "white", "axes.facecolor": "white",
                     "savefig.facecolor": "white"})
INK, SOFT, FAINT = "#111111", "#4A4A4A", "#8A959F"

R = ds.rows()
# Span derived from the data — it was hard-coded "Jan 2023 - Jul 2026", which predated the
# corpus-window extension back to 2018 and silently misstated the range.
_d=sorted(r["Publication Date"][:10] for r in R if r.get("Publication Date"))
_MON=["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
SPAN=f"{_MON[int(_d[0][5:7])]} {_d[0][:4]} \u2013 {_MON[int(_d[-1][5:7])]} {_d[-1][:4]}"

tier = lambda r: ("A" if r["Eval? (trackable)"] == "yes" and r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")
T = collections.Counter(tier(r) for r in R)
A = [r for r in R if tier(r) == "A"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]
SEV = collections.Counter(r["Severity (C1/C2) majority"] for r in R)
OUTC = collections.Counter(r["Proportionality"] for r in H)
gap = OUTC["Accountability gap (no action)"]; und = OUTC["Under-response (gap)"]
prop = OUTC["Proportionate"]; short = gap + und
NREP = len({r["Report ID"] for r in R if r["Report ID"]})
NORG = len({r["Institution"] for r in R})

fig, ax = plt.subplots(figsize=(17.0, 6.9))
ax.set_xlim(0, 100); ax.set_ylim(21, 100); ax.axis("off")

BOXES = [
    (f"{len(R):,}", "published\nfindings",
     f"{NREP} reports · {NORG} evaluators\n{SPAN}", NEUTRAL[1]),
    (f"{T['A']}", "name a company\nor model",
     f"Tier B {T['B']} no accountable party\nTier C {T['C']} not an empirical finding", NEUTRAL[0]),
    (f"{len(H)}", "significant risk",
     f"C1 {SEV['C1']} · C2 {SEV['C2']} corpus-wide\n3-model majority, 8.1% split", RED),
]
BW, BH, GAP0, Y = 15.0, 32.0, 6.0, 44.0
x = 2.0
for i, (big, mid, sub, col) in enumerate(BOXES):
    ax.add_patch(FancyBboxPatch((x, Y), BW, BH, boxstyle="round,pad=0,rounding_size=1.1",
                                facecolor=tint(col, 0.86), edgecolor=col, linewidth=2.0))
    ax.text(x + BW / 2, Y + 20.5, big, ha="center", va="center", fontsize=50,
            fontweight="bold", color=shade(col, 0.15))
    ax.text(x + BW / 2, Y + 9.5, mid, ha="center", va="center", fontsize=20.7,
            color=INK, linespacing=1.35)
    ax.text(x + BW / 2, Y - 5.0, sub, ha="center", va="top", fontsize=12.5,
            color=SOFT, linespacing=1.5)
    if i < len(BOXES) - 1:
        ax.add_patch(FancyArrowPatch((x + BW + 0.8, Y + BH / 2), (x + BW + GAP0 - 0.8, Y + BH / 2),
                                     arrowstyle="-|>", mutation_scale=20, lw=2.0, color="#9AA7B2"))
        ax.text(x + BW + GAP0 / 2, Y + BH / 2 + 4.2, ["filter", "severity"][i], ha="center",
                fontsize=15.2, color=FAINT, style="italic")
    x += BW + GAP0

# outcome bar — proportional, replacing figure 04
BX, BWID = x + 2.5, 24.0
seg = [(gap, RED, "No response located"),
       (und, AMBER, "Under-response"),
       (prop, GREEN, "Proportionate")]
top = Y + BH
ax.add_patch(FancyArrowPatch((x - GAP0 + 0.8, Y + BH / 2), (BX - 1.0, Y + BH / 2),
                             arrowstyle="-|>", mutation_scale=20, lw=2.0, color="#9AA7B2"))
ax.text((x - GAP0 + BX) / 2, Y + BH / 2 - 4.6, "trace\nresponse", ha="center", va="top",
        fontsize=15.2, color=FAINT, style="italic", linespacing=1.3)
yy = top
for n, col, lab in seg:
    h = BH * n / len(H)
    yy -= h
    ax.add_patch(FancyBboxPatch((BX, yy), BWID, h, boxstyle="square,pad=0",
                                facecolor=col, edgecolor="white", linewidth=1.6))
    # count and label both sit inside the segment; every segment is tall enough for one line
    ax.text(BX + 1.6, yy + h / 2, f"{n}", ha="left", va="center", fontsize=23.5,
            fontweight="bold", color="white")
    ax.text(BX + 7.4, yy + h / 2, lab.replace("\n", " "), ha="left", va="center",
            fontsize=15.2, color="white")
ax.text(BX, top + 1.6, f"outcomes  (n = {len(H)})", fontsize=16.6, color=SOFT)

# the fall-short bracket spans the top two segments, at the far right so it clears the arrow
BRX = BX + BWID + 1.8
ytop, ybot = Y + BH, Y + BH - BH * short / len(H)
ax.plot([BRX, BRX], [ybot, ytop], color=RED, lw=3.0, solid_capstyle="butt")
for yv in (ybot, ytop):
    ax.plot([BRX - 1.4, BRX], [yv, yv], color=RED, lw=3.0, solid_capstyle="butt")
ax.text(BRX + 1.6, (ytop + ybot) / 2, f"{short/len(H):.0%}\nfall short", ha="left", va="center",
        fontsize=22.1, fontweight="bold", color=RED, linespacing=1.3)

ax.text(2.0, 97.0, "From published finding to documented response",
        fontsize=34.5, fontweight="bold", color=INK, va="top")
ax.text(2.0, 86.5, f"{gap} of {len(H)} significant-risk findings about named frontier systems "
        f"drew no documented company response.", fontsize=20.0, color=SOFT, va="top")
ax.text(2.0, 27.0, "Boxes are schematic, not to scale; the outcome bar is proportional. A finding "
        "falls short when the company response is absent, or weaker than the finding's severity "
        "warrants.", fontsize=14.5, color=FAINT, va="top")

p = os.path.join(OUT, "fig1_pipeline.png")
fig.savefig(p, bbox_inches="tight", pad_inches=0.25)
plt.close(fig)
print(f"wrote {p}")
print(f"  corpus {len(R)} · TierA {T['A']} (B {T['B']} C {T['C']}) · C1 {SEV['C1']} · headline {len(H)}")
print(f"  outcomes: gap {gap} · under {und} · proportionate {prop} · falls short {short} ({short/len(H):.1%})")
