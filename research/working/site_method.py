#!/usr/bin/env python3
"""Correct the two stale methodology rules on the site, and shorten while doing it.

Both currently misdescribe how the published headline was derived:

  1. "A company action counts only if it is explicitly attributable to the finding" -- false.
     Attribution is a SEPARATE axis from response strength; 12 accountability-set rows carry a
     positive Action Level with No explicit attribution. What col 17 requires is that the action
     address the identified problem, not that the company credit anyone.
  2. "Company self-reports are out of scope entirely" -- false. 42 company-published findings are
     in the corpus and 14 are in the accountability set, filed under the named external evaluator
     per the venue rule. What is out of scope is a company evaluating itself with NO external
     evaluator named.
"""
import os, re, csv, collections

REPO = os.path.expanduser("~/evaluating-the-evaluators")
IX = os.path.join(REPO, "index.html")
t = open(IX).read()
before_words = len(re.sub(r"<[^>]+>", " ", t[t.find('<section id="methodology"'):
                                            t.find('</section>', t.find('<section id="methodology"'))]).split())

SUBS = [
 # 1. the response rule
 ("""A company action counts only if it is explicitly attributable to the finding — the company's own primary source (blog, system card, SEC filing, testimony) must draw the connection itself; this establishes an explicit public link, not causation. Pre-existing policy does not count. News coverage quoting a company is never admitted as a company statement. Negative response lags are genuine: pre-deployment evaluators share findings with companies before publication.""",
  """Only the company's own primary document counts — blog, system card, deprecation notice, filing. News coverage quoting a company is never admitted, and pre-existing policy does not count. The action must address the identified problem: a general-purpose measure that would read identically had the finding never been published does not qualify. Whether the company <em>credits</em> the evaluator is recorded separately under Attribution — acting without saying why still counts as acting. Negative lags are genuine: pre-deployment evaluators share findings before publication."""),
 # 2. the self-report rule
 ("""Company self-reports are out of scope entirely — a company evaluating and responding to its own model is not an independent accountability check.""",
  """Company-published reports are included only where an external evaluator is named, and are filed under that evaluator. A company evaluating its own model with no external evaluator named is out of scope."""),
 # 3. narrow opener -> the actual scope
 ("""when a government AI Safety Institute publishes a finding about a specific model or company, does a documented response follow?""",
  """when an AI safety institute or third-party evaluator publishes a finding about a named model, does a documented company response follow?"""),
]
for a, b in SUBS:
    if a in t:
        t = t.replace(a, b)
        print("fixed:", b[:78] + "…")
    else:
        print("!! NOT MATCHED:", a[:70])

# add the one rule the site never stated: what proportionality means
ANCHOR = "<h3>Severity</h3>"
if ANCHOR in t and "severity-relative" not in t:
    add = ("""<h3>Proportionality</h3>
      <p>Outcome = severity × response strength, and the bar is <b>severity-relative</b>: for a
      significant-risk finding only a substantive response is proportionate, whereas for the lower
      severity a partial one is. Action Level scores the <em>content</em> of the public response — not
      whether it was implemented, or whether it reduced risk.</p>
      """)
    t = t.replace(ANCHOR, add + ANCHOR, 1)
    print("added: Proportionality (the rule behind the headline was never stated)")

open(IX, "w").write(t)
i = t.find('<section id="methodology"')
after_words = len(re.sub(r"<[^>]+>", " ", t[i:t.find('</section>', i)]).split())
print(f"\nmethodology section: {before_words} → {after_words} words")
stale = [s for s in ("counts only if it is explicitly attributable",
                     "out of scope entirely") if s in t]
print("stale rules remaining:", stale or "none")
