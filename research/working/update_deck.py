#!/usr/bin/env python3
"""Bring the deck's numbers in line with the final workbook, headline = 80.3%."""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck.html")
t = open(p, encoding="utf-8").read()

SUBS = [
    # fact bar: 80.3% promoted to the hero slot, 61.9% demoted to a plain fact
    ("""<div class="fact hero"><div class="n">62.6%</div><div class="l">no documented response</div></div>
  <div class="fact hero"><div class="n">78.9%</div><div class="l">fall short of the standard</div></div>""",
     """<div class="fact hero"><div class="n">80.3%</div><div class="l">fall short of the standard</div></div>
  <div class="fact"><div class="n">61.9%</div><div class="l">no response at all</div></div>"""),
    # slide 1
    ("""Of <b class="num">147</b> findings that name a company and were graded the more serious of
    two risk levels, <b class="num">92</b> have no documented company response at all.""",
     """Of <b class="num">147</b> findings that name a company and were graded the more serious of two
    risk levels, <b class="num">118</b> &mdash; <b>80%</b> &mdash; drew no response proportionate to
    what they found."""),
    # slide 4
    ("""<span class="o r">92</span> no action · <span class="o a">24</span> under-response ·
    <span class="o g">31</span> proportionate. <b>78.9%</b> of significant-risk findings fall short of a
    proportionate response.""",
     """<span class="o r">91</span> no action · <span class="o a">27</span> under-response ·
    <span class="o g">29</span> proportionate. <b>80.3%</b> fall short of a response proportionate to the
    severity &mdash; 91 drew nothing at all, 27 drew something too weak."""),
    # slide 5
    ("""<b class="num">37</b> substantive, <b class="num">13</b> partial,
    <b class="num">17</b> acknowledged. <b class="num">54</b> responses cite the evaluator explicitly,
    <b class="num">13</b> act without saying why. Median lag: <b>0 days</b>.""",
     """<b class="num">35</b> substantive, <b class="num">16</b> partial,
    <b class="num">18</b> acknowledged. <b class="num">57</b> responses cite the evaluator explicitly,
    <b class="num">12</b> act without saying why. Median lag: <b>0 days</b>."""),
    # define the term on first use
    ("""Every number is
read from <code>AISIEVAL.xlsx</code> after the Action&nbsp;Level re-verification sweep.""",
     """Every number is read from
<code>AISIEVAL.xlsx</code> after the Action&nbsp;Level re-verification sweep. <b>Falls short of the
standard</b> means the response was weaker than the severity warranted &mdash; for a significant-risk
finding, only a substantive response qualifies."""),
    # slide 8's method line
    ("""All <b class="num">67</b> rows with a documented response were re-verified against the source
    document; <b class="num">5</b> were recoded, in <b>both</b> directions.""",
     """All <b class="num">69</b> rows with a documented response were re-verified against the source
    document; <b class="num">9</b> were recoded, in <b>both</b> directions."""),
    # footer
    ("""Headline population = Tier A ∩ severity C1 (n=147) · gap 92/147 = 62.6% · falls short 116/147 = 78.9%""",
     """Headline population = Tier A ∩ severity C1 (n=147) · falls short 118/147 = 80.3% · no response at all 91/147 = 61.9%"""),
]
for a, b in SUBS:
    if a not in t:
        print("!! NOT MATCHED:", " ".join(a.split())[:78])
        continue
    t = t.replace(a, b)
    print("ok:", " ".join(b.split())[:74])
open(p, "w", encoding="utf-8").write(t)
stale = [x for x in ("62.6", "78.9", "92</b>", ">37<", ">54<", "116/147") if x in t]
print("\nstale figures still present:", stale or "none")
