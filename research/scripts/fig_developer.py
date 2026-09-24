#!/usr/bin/env python3
"""02_findings_per_model_developer.png — whose models the findings are about.

The corpus is described three ways in §3.2: who reports (01), whose models (this), and under
what access (03). The middle one was dropped when the v10 chart set was retired, leaving the
paper with a Figure 2 caption and no figure. This restores it on the current corpus.

A finding naming models from several developers counts once per developer, so the bars sum to
more than the corpus. Anonymised findings are shown as their own bar rather than omitted:
they are the third-largest category and their whole point is that no developer can be named,
which is the structural argument of §3.3.
"""
import os, re, sys, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source
from palette import *

OUT = CHARTS_OUT
plt.rcParams.update({"figure.dpi": 200, "savefig.dpi": 200, "font.family": "DejaVu Sans",
                     "figure.facecolor": "white", "axes.facecolor": "white",
                     "savefig.facecolor": "white"})

# Matching is by model-family name, not by a free-text developer field, because the sheet
# records the systems evaluated rather than the company. The rule is listed here so the
# caption's "counts are approximate" is checkable rather than a hedge.
# Each pattern matches the company's model families AND its bare name, because some rows name
# the developer without naming the model ("OpenAI models (the specific model is not named)").
# Those rows are Tier A on the named-developer limb of the rule, so treating them as anonymised
# would contradict the tier they carry.
OWNER = dataset_source.DEVELOPER_PATTERNS   # single source of truth, shared with all_stats.pyr|aya)\b")]
ANON = re.compile(r"anonymis|anonymiz|unnamed|not named|undisclosed", re.I)

R = [r for r in dataset_source.rows() if r.get("Finding ID")]
tier = lambda r: ("A" if r["Eval? (trackable)"] == "yes" and r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")

tot, tierA, c1 = collections.Counter(), collections.Counter(), collections.Counter()
for r in R:
    m = r.get("Models / Systems", "") or ""
    hits = [name for name, pat in OWNER if re.search(pat, m, re.I)]
    # Only anonymised when NO developer is identifiable. "OpenAI models (the specific model is
    # not named)" names the accountable developer and is Tier A on that basis, so it must not
    # be counted as anonymised merely because the phrase "not named" appears.
    if ANON.search(m) and not hits:
        hits.append("Anonymized /\nunspecified")
    for h in hits:
        tot[h] += 1
        if tier(r) == "A":
            tierA[h] += 1
            if r["Severity (C1/C2) majority"] == "C1":
                c1[h] += 1

order = [k for k, _ in tot.most_common()]
fig, ax = plt.subplots(figsize=(18, 11))
y = np.arange(len(order))
# Whole-corpus bar in neutral blue; the Tier A share overlaid in red, because the question the
# figure has to answer is not only "whose models" but "whose models are accountable-relevant".
ax.barh(y, [tot[k] for k in order], color=BLUE, height=0.66, zorder=3, label="All findings")
ax.barh(y, [tierA[k] for k in order], color=RED, height=0.66, zorder=4,
        label=lab("tier.A","of which Tier A (accountability set)",run=True))
mx = max(tot.values())
FS_TOT, FS_SUB, FS_TICK = 27, 22, 27
# Every row carried "(Tier A n · C1 n)" at the same weight as its total, eleven times over, and
# three of those rows read "(Tier A 0 · C1 0)" — a parenthesis that says nothing, on developers
# with no Tier A findings at all. The total now stands alone in bold; the breakdown follows it in
# a lighter grey, and is dropped where there is no Tier A share to break down.
def _sub(k):
    if not tierA[k]:
        return ""
    return (f"{tierA[k]} name a company · {c1[k]} significant risk" if PLAIN
            else f"Tier A {tierA[k]} · C1 {c1[k]}")

fig.canvas.draw()
rend = fig.canvas.get_renderer()

def _px(s_, fs, weight="normal"):
    if not s_:
        return 0.0
    t = ax.text(0, 0, s_, fontsize=fs, fontweight=weight, alpha=0)
    w = t.get_window_extent(renderer=rend).width
    t.remove()
    return w

# Sizing the x-limit so the longest annotation fits is self-referential if done in data units:
# the data-unit width of a fixed-pixel string depends on the very limit being chosen. Solve it in
# pixels instead. With an axes W px wide showing L data units, a bar of value v ends at (v/L)*W
# and its annotation needs T px, so L >= v*W/(W - gap - T) — taken over every row, not just the
# longest string, because the widest annotation and the longest bar need not be the same row.
W = ax.get_window_extent(renderer=rend).width
GAP1 = 0.012 * W          # bar end -> total
GAP2 = 0.016 * W          # total -> breakdown
need = []
for k in order:
    T = _px(str(tot[k]), FS_TOT, "bold")
    if _sub(k):
        T += GAP2 + _px(_sub(k), FS_SUB)
    need.append(tot[k] * W / max(W - GAP1 - T, 1.0))
ax.set_xlim(0, max(need) * 1.02)

inv = ax.transData.inverted()
def _du(px):
    return abs(inv.transform((px, 0))[0] - inv.transform((0, 0))[0])

for i, k in enumerate(order):
    x = tot[k] + _du(GAP1)
    ax.text(x, i, f"{tot[k]}", va="center", ha="left",
            fontsize=FS_TOT, fontweight="bold", color="#1A1A1A")
    if _sub(k):
        ax.text(x + _du(_px(str(tot[k]), FS_TOT, "bold") + GAP2), i, _sub(k),
                va="center", ha="left", fontsize=FS_SUB, color="#5A5A5A")
ax.set_yticks(y); ax.set_yticklabels(order, fontsize=FS_TICK); ax.invert_yaxis()
ax.grid(axis="y", visible=False)
ax.set_xlabel("Findings", fontsize=26, labelpad=10)
# The title is a label, not a sentence: "Whose models the findings concern" editorialised where
# every other figure in the set simply names its axes.
ax.set_title(f"Findings by Model Developer (n={len(R):,})",
             pad=24, fontsize=33)
ax.legend(fontsize=25, loc="lower right", frameon=False)

p = out_path("02_findings_per_model_developer")
# One line, below the axes in figure coordinates. Inside the axes it printed on top of the x
# tick labels and the axis title. The matching rule used to be spelled out here too; it lives in
# the figure caption in the paper instead, which is where a reader looks for it.
if NOTES:
    fig.text(0.5, -0.02,
             f"A finding naming several developers counts once per developer, so bars sum to more "
             f"than {len(R):,}.",
             fontsize=23, color="#555555", va="top", ha="center", transform=fig.transFigure)
fig.savefig(p, bbox_inches="tight", pad_inches=pad(0.3))
plt.close(fig)
print(f"wrote {p}")
for k in order:
    print(f"  {k:24} total {tot[k]:>4}  TierA {tierA[k]:>3}  C1 {c1[k]:>3}")
