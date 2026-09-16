#!/usr/bin/env python3
"""Record the specificity rule in the rulebook and guard it in the validator."""
import os, re

RB = os.path.expanduser("~/evaluating-the-evaluators/v10_RULEBOOK.md")
VA = os.path.expanduser("~/Documents/AISIEVAL_validate.py")

RULE = """
### §9 col 17 — the specificity test (worked example, added 2026-08-17)

Col 17 requires a mitigation that **directly addressed the identified problem** (Substantive) or that
**addressed only part of the identified problem** (Partial). Applying that sentence needs one
clarification, because 11 rows had been coded positive on company actions that fail it.

**The test is response specificity, not attribution.** Ask: would this company action read identically
had the finding never been published? If yes, it is not a response to *this* finding, and Action Level
is `None` however impressive the action is.

* **Specific → keep the positive coding, with or without credit.** Type case `METR-2025-04-ALI1`: the
  Claude 3.7 Sonnet card documents the exact reward-hacking pattern, says automated classifiers caught
  it in training transcripts, and records partial pre-launch mitigations — while crediting Anthropic's
  own monitoring rather than METR. `Partial` + `No explicit attribution`. This is precisely the cell
  the Attribution revision exists to hold, and nothing about the specificity test disturbs it.
* **Domain-level → keep.** A Preparedness/RSP capability designation counts where the source document
  reports this finding among the designation's inputs *and* safeguards activated as a result.
* **General-purpose → `None`.** A company-wide method, a product-scope decision or a commercial
  deprecation. Example: OpenAI's self-serve fine-tuning wind-down, whose own notice states a
  *capability* rationale — newer models make much of fine-tuning unnecessary — and references neither
  the finding nor the evaluator. It removes the attack surface, but it is not a response to the
  finding.

Specificity and attribution are **independent axes**. Of the 12 Tier A rows that had
`No explicit attribution`, 11 were general-purpose and 1 (`METR-2025-04-ALI1`) was specific. Do not
use a missing attribution as grounds to downgrade Action Level; that would import col 18 into col 17
and break the separation the 2026-08-15 revision established. Proportionality inputs are unchanged:
Severity × Action Level only.

**Effect on the headline.** Primary specification (specificity enforced): accountability gap
102/147 = 69.4%, falls short of the standard 121/147 = 82.3%. Reported robustness check (general-purpose
unattributed actions admitted): 91/147 = 61.9%. The 11 affected rows are preserved losslessly in
`~/Documents/AISIEVAL_sensitivity_general_response.csv` and restated in each row's Notes, so the
alternative figure is reproducible without recoding anything.
"""

t = open(RB, encoding="utf-8").read()
if "the specificity test (worked example" not in t:
    m = re.search(r'(?m)^### Channel A — company response', t)
    t = (t[:m.start()] + RULE.strip() + "\n\n" + t[m.start():]) if m else t + "\n" + RULE
    open(RB, "w", encoding="utf-8").write(t)
    print(f"rulebook: specificity rule inserted ({len(RULE)} chars)")
else:
    print("rulebook: rule already present")

GUARD = '''
# --- specificity rule (2026-08-17): these 11 rows are None under the primary specification.
# Their prior coding lives in ~/Documents/AISIEVAL_sensitivity_general_response.csv for the
# paper's robustness check. If one drifts back to a positive level, either the rule was
# reversed deliberately (update this list) or a coding was lost.
GENERAL_RESPONSE = {"CAIS-2023-07-JAI1","CAIS-2023-07-JAI3","APOLLO-2023-11-ALI1",
 "SCALEAI-2024-10-JAI1","SCALEAI-2025-02b-JAI3","CISCO-2024-07-JAI1","CIP-2025-08-ALI1",
 "FARAI-2024-08-JAI1","FARAI-2024-10-ALI1","FARAI-2024-10-JAI1","FARAI-2025-02a-JAI2"}
check("general-purpose-response rows drifted off None (specificity rule)",
      [r["Finding ID"] for r in R if r["Finding ID"] in GENERAL_RESPONSE
       and r.get("Action Level") not in ("", "None")])
check("specificity-rule rows missing their audit note",
      [r["Finding ID"] for r in R if r["Finding ID"] in GENERAL_RESPONSE
       and "SPECIFICITY RULE APPLIED" not in str(r.get("Notes") or "")])
'''
v = open(VA, encoding="utf-8").read()
if "GENERAL_RESPONSE" not in v:
    anchor = v.index('print(f"AISIEVAL validator')
    v = v[:anchor] + GUARD.strip() + "\n\n" + v[anchor:]
    open(VA, "w", encoding="utf-8").write(v)
    print("validator: 2 guards added")
else:
    print("validator: guards already present")
