#!/usr/bin/env python3
"""Fix the two derived figures the headline change left behind, and correct slide 7's claim.

Both were computed on the NO-ACTION rate. With falls-short as the headline they must be
restated on that metric -- and on falls-short the time trend declines monotonically, which
contradicts what slide 7 currently says.
"""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck.html")
t = open(p, encoding="utf-8").read()

SUBS = [
    # slide 3 -- gov-only subset, restated on the headline metric
    ("""Flag here that the headline
    holds on the government-only subset too &mdash; <span class="num">32/54 = 59.3%</span> &mdash; so it is not an artifact
    of pooling AISIs with independent labs.""",
     """Flag here that the headline
    holds on the government-only subset too &mdash; <span class="num">41/54 = 75.9%</span> fall short &mdash; so it is
    not an artifact of pooling AISIs with independent labs."""),
    # slide 7 -- the claim itself has to change on the headline metric
    ("""<h3>Unevenly distributed, and not closing</h3>
    <p class="land">Gap rate varies sharply by developer and by how much access the evaluator had. Over time:
    2023 <span class="num">40%</span> &rarr; 2024 <span class="num">50%</span> &rarr; 2025 <span class="num">72%</span>
    &rarr; 2026 <span class="num">60%</span>.</p>""",
     """<h3>Unevenly distributed, and improving slowly</h3>
    <p class="land">Shortfall varies sharply by developer and by how much access the evaluator had. Over time it
    declines: 2023 <span class="num">100%</span> &rarr; 2024 <span class="num">90%</span> &rarr;
    2025 <span class="num">82%</span> &rarr; 2026 <span class="num">74%</span> &mdash; but it is still roughly three
    in four.</p>"""),
    ("""<p class="say"><b>Say:</b> name the caveats before anyone else does &mdash; fig 19 covers developers with n&ge;5 and
    the smallest bars are fragile; 2026 is partial (cutoff 31 July) and 2023 is n=5. The defensible claim is
    <b>&quot;no evidence of closing&quot;</b>, not &quot;actively worsening&quot;.</p>""",
     """<p class="say"><b>Say:</b> be straight about the direction &mdash; on the headline metric the trend is
    <b>downward</b>, so do not claim it is getting worse. The honest line is that the shortfall is narrowing but
    remains the norm. Caveats to state first: 2023 is n=5, 2024 n=20, and 2026 is partial (cutoff 31 July); fig 19
    covers developers with n&ge;5 and the smallest bars are fragile. Part of the decline is likely composition &mdash;
    later years hold more pre-deployment evaluations, which are answered in the launch card by construction.</p>"""),
    # slide 7 figure list: fig 15 plots the no-action rate, so name the mismatch
    ("""<div class="figs"><span class="fig">19_gap_rate_by_developer.png</span><span class="fig">16_gap_rate_by_access_type.png</span><span class="fig">15_gap_rate_by_year.png</span></div>""",
     """<div class="figs"><span class="fig">19_gap_rate_by_developer.png</span><span class="fig">16_gap_rate_by_access_type.png</span><span class="fig">15_gap_rate_by_year.png</span><span class="fig solo">figs 15/16/19 plot the no-action rate, not falls-short</span></div>"""),
]
for a, b in SUBS:
    if a not in t:
        print("!! NOT MATCHED:", " ".join(a.split())[:80])
        continue
    t = t.replace(a, b)
    print("ok:", " ".join(b.split())[:78])
open(p, "w", encoding="utf-8").write(t)
print("\nstale:", [x for x in ("59.3", "40%", "50%", "72%", "60%", "not closing") if x in t] or "none")
