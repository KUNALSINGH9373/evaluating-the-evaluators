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
        hits.append("Anonymised /\nunspecified")
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
        label="of which Tier A (accountability set)")
mx = max(tot.values())
for i, k in enumerate(order):
    ax.text(tot[k] + mx * 0.012, i, f"{tot[k]}   (Tier A {tierA[k]} · C1 {c1[k]})",
            va="center", ha="left", fontsize=21, fontweight="bold", color="#1A1A1A")
ax.set_yticks(y); ax.set_yticklabels(order, fontsize=23); ax.invert_yaxis()
ax.set_xlim(0, mx * 1.42); ax.grid(axis="y", visible=False)
ax.set_xlabel("Findings", fontsize=23)
ax.set_title(f"Whose models the findings are about (n = {len(R):,} findings)",
             pad=24, fontsize=33, fontweight="bold")
ax.legend(fontsize=21, loc="lower right", frameon=False)
ax.text(0, len(order) - 0.25,
        "A finding naming several developers counts once per developer, so bars sum to more than "
        f"{len(R):,}.\nMatching is by model-family name; see scripts/fig_developer.py for the rule.",
        fontsize=18, color="#555555", va="top", ha="left", linespacing=1.4)

p = os.path.join(OUT, "02_findings_per_model_developer.png")
fig.savefig(p, bbox_inches="tight", pad_inches=0.22)
plt.close(fig)
print(f"wrote {p}")
for k in order:
    print(f"  {k:24} total {tot[k]:>4}  TierA {tierA[k]:>3}  C1 {c1[k]:>3}")
