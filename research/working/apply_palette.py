#!/usr/bin/env python3
"""Point every chart script at scripts/palette.py."""
import os, re

S = os.path.expanduser("~/MATS/Research/AISI_Evals/scripts")
IMPORT = "from palette import *   # single source of colour truth\n"

def patch(fn, subs, add_import_after=None):
    p = os.path.join(S, fn)
    t = open(p).read()
    for a, b in subs:
        if a not in t:
            print(f"  !! {fn}: not matched -> {a[:60]}")
            continue
        t = t.replace(a, b)
    if "from palette import" not in t:
        anchor = add_import_after or "import openpyxl"
        t = t.replace(anchor, anchor + "\nimport sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n" + IMPORT, 1)
    open(p, "w").write(t)
    print(f"  patched {fn}")

# ---- charts.py -------------------------------------------------------------------------
patch("charts.py", [
 ('GREEN="#00A36C"; AMBER="#E8A80C"; ORANGE="#D2570A"; RED="#E03131"\n'
  'BLUE="#0A6EBD"; SKY="#4FADEE"; PURPLE="#7B4FBF"; TEAL="#00A6A6"; MAGENTA="#D4267D"; LIME="#7CB518"\n'
  'TIER={"A":"#E8453C","B":"#F5A623","C":"#2D9CDB"}\n'
  'PROP_C={"Proportionate":GREEN,"Under-response (gap)":AMBER,"Accountability gap (no action)":ORANGE}\n'
  'AL_C={"Substantive":GREEN,"Partial":LIME,"Acknowledged":AMBER,"None":ORANGE}\n'
  'PL_C={"Binding policy action":BLUE,"Non-binding policy-related uptake":SKY,"No policy uptake identified":"#B0B7BF"}',
  '# colours come from palette.py; these aliases keep the existing call sites readable\n'
  'SKY=NEUTRAL[2]; PURPLE=NEUTRAL[3]; TEAL=NEUTRAL[0]; MAGENTA=NEUTRAL[5]; LIME=AMBER\n'
  'TIER={k:TIER_INK[k] for k in "ABC"}\n'
  'PROP_C=PROP; AL_C=ACTION; PL_C=POLICY'),
 # institutions / developers / years / domains -> neutral ramp
 ('[BLUE if i%2==0 else SKY for i in range(len(c))]', 'ramp(len(c))'),
 ('[ORANGE if i%2==0 else AMBER for i in range(len(c))]', 'ramp(len(c))'),
 ('[BLUE,SKY,PURPLE,TEAL,"#B0B7BF"]', 'order(ACCESS,order_keys)'),
 ('order=["Pre-deployment","Post-deployment","Mixed","Aggregate","N/A"]',
  'order_keys=["Pre-deployment","Post-deployment","Mixed","Aggregate","N/A"]\norder=order_keys'),
 ('b=ax.bar(range(len(vals)),vals,color=[BLUE,SKY],width=0.56,zorder=3)',
  'b=ax.bar(range(len(vals)),vals,color=order(SCOPE,["government-AISI","third-party-evaluator"]),width=0.56,zorder=3)'),
 ('[TEAL,BLUE,PURPLE,MAGENTA][:len(yrs)]', 'ramp(len(yrs))'),
 ('[ORANGE,SKY]', 'order(SEV,["C1","C2"])'),
 ('[GREEN,AMBER,"#B0B7BF"]', 'order(ATTRIB,["Explicit attribution","No explicit attribution","No response located"])'),
 ('color=[GREEN,ORANGE,AMBER,PURPLE][:len(keys)]', 'color=order(ACCESS,keys)'),
 ('cols=[BLUE,TIER["A"],PURPLE,AMBER,GREEN,TEAL]',
  'cols=[NEUTRAL[0],TIER_INK["A"],NEUTRAL[1],ORANGE,GREEN,NEUTRAL[3]]'),
])

# ---- charts2.py ------------------------------------------------------------------------
patch("charts2.py", [
 ('GREEN,AMBER,ORANGE,RED="#00A36C","#E8A80C","#D2570A","#E03131"\n'
  'BLUE,SKY,PURPLE,TEAL,MAGENTA,LIME="#0A6EBD","#4FADEE","#7B4FBF","#00A6A6","#D4267D","#7CB518"\n'
  'TIER={"A":"#E8453C","B":"#F5A623","C":"#2D9CDB"}',
  'SKY=NEUTRAL[2]; PURPLE=NEUTRAL[3]; TEAL=NEUTRAL[0]; MAGENTA=NEUTRAL[5]; LIME=AMBER\n'
  'TIER={k:TIER_INK[k] for k in "ABC"}'),
 ('pal=[BLUE,ORANGE,TEAL,PURPLE,GREEN,MAGENTA,AMBER,SKY,LIME,RED]', 'pal=ramp(10)'),
 ('COL=[GREEN,AMBER,ORANGE]', 'COL=[GREEN,AMBER,RED]'),
 ('color=[GREEN if v<0.4 else AMBER if v<0.7 else ORANGE for v in vals]',
  'color=[GREEN if v<0.4 else AMBER if v<0.7 else RED for v in vals]'),
 ('ax.plot(range(len(yrs)),rate,color=ORANGE,', 'ax.plot(range(len(yrs)),rate,color=RED,'),
 ('fontsize=29,fontweight="bold",color=ORANGE)', 'fontsize=29,fontweight="bold",color=RED)'),
 ('color=BLUE,alpha=0.78', 'color=NEUTRAL[0],alpha=0.78'),
 ('ax.scatter(v,y,s=620,color=BLUE,', 'ax.scatter(v,y,s=620,color=NEUTRAL[0],'),
])

# ---- hero.py ---------------------------------------------------------------------------
patch("hero.py", [
 ('GREEN,AMBER,RED="#1E9E63","#E8A80C","#C62F1F"', '# GREEN / AMBER / RED come from palette.py'),
 ('L1,L2,L3="#C6DDF2","#5B9BD5","#1F6FB2"', 'L1,L2,L3="#9BCBEA","#4FA7DC","#2E7CA8"'),
])

# ---- tree.py ---------------------------------------------------------------------------
patch("tree.py", [
 ('COL = {"Government": "#1F6FB2", "Non-Profit (AIEF)": "#1E9E63",\n'
  '       "Non-Profit (Independent)": "#5B9BD5", "For-Profit": "#E8A80C"}', 'COL = INSTTYPE'),
 ('L1 = "#C6DDF2"', 'L1 = "#DCEDF8"'),
 ('WIRE = "#9AA7B2"', '# WIRE comes from palette.py'),
])

# ---- fig12_scope.py --------------------------------------------------------------------
patch("fig12_scope.py", [
 ('GREEN, AMBER, ORANGE = "#1E9E63", "#E8A80C", "#D2570A"', '# colours come from palette.py'),
 ('("Accountability gap (no action)", "No documented response", ORANGE)',
  '("Accountability gap (no action)", "No documented response", RED)'),
 ('fontsize=17, color="#C62F1F", fontweight="bold"', 'fontsize=17, color=RED, fontweight="bold"'),
])

# ---- fig15b.py -------------------------------------------------------------------------
patch("fig15b.py", [
 ('RED, AMBER, GREY = "#C62F1F", "#E8A80C", "#666666"', 'GREY_LINE = MUTED'),
 ('ax.plot(years, noact, "--s", color=GREY,', 'ax.plot(years, noact, "--s", color=GREY_LINE,'),
 ('ha="center", fontsize=19, color=GREY)', 'ha="center", fontsize=19, color=GREY_LINE)'),
])
print("\ndone")
