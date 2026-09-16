#!/usr/bin/env python3
"""Remove the artefacts of the withdrawn bulk rule, and replace the rulebook section with what
actually survived: the model-tested vs successor-systems distinction inside col 17.
"""
import os, re

RB = os.path.expanduser("~/evaluating-the-evaluators/v10_RULEBOOK.md")
VA = os.path.expanduser("~/Documents/AISIEVAL_validate.py")
CSV = os.path.expanduser("~/Documents/AISIEVAL_sensitivity_general_response.csv")

NEW = """### §9 col 17 — scope of "directly addressed the identified problem" (added 2026-08-17)

Col 17 measures the **content** of the documented company response. It expressly does **not**
establish causation, and it lists *access restriction* among qualifying actions. Two consequences,
both settled by working through the 11 hardest rows in the corpus:

**1. A missing link to the finding is not grounds to downgrade Action Level.** Where a company acts
after a finding without referencing it or the evaluator, the action still counts; the silence is
recorded in col 18 as `No explicit attribution`. Downgrading col 17 as well would count the same
absence twice and would empty the very cell the 2026-08-15 Attribution revision was created to hold.
A bulk reclassification of 11 such rows to `None` was applied on 2026-08-17 and **withdrawn the same
day** for this reason. Motive is likewise outside col 17: OpenAI's fine-tuning wind-down states a
capability rather than a safety rationale, and still counts as an access restriction.

**2. Substantive vs Partial turns on whether the action reaches the model tested.** This is the
distinction that survived, and it is a col 17 question:

* **Substantive** — the action lands on the tested model, the tested surface, or the exact broken
  component. Examples: `CISCO-2024-07-JAI1` (Prompt Guard 2 is the successor to the very classifier
  the finding broke); `CIP-2025-08-ALI1` (same model, same behaviour, 68 days, 65–80% measured
  reduction); `SCALEAI-2024-10-JAI1` (a GPT-4o browser agent shipped with proactive refusals for the
  exact harmful-task class).
* **Partial** — the action addresses the identified problem class but reaches only **successor**
  systems, or removes the venue rather than the behaviour, or is expressly interim. Examples:
  `CAIS-2023-07-JAI1` (deliberative alignment on o-series, not the tested GPT-3.5/GPT-4);
  `SCALEAI-2025-02b-JAI3` (Safety Reasoner across successor systems); `APOLLO-2023-11-ALI1`
  (restricting stock trading removes the scenario, not the deception); `CAIS-2023-07-JAI3`
  (prototype, never deployed); the four `FARAI` fine-tuning rows (phased, and inference on existing
  fine-tuned models continues).

Attribution and response strength are **independent axes**. Of the 12 Tier A rows with
`No explicit attribution`, 11 are the rows above and 1 is `METR-2025-04-ALI1`, where Anthropic
documents the exact reward-hacking pattern and partial pre-launch mitigations while crediting its own
monitoring — `Partial` + `No explicit attribution`, undisturbed. Proportionality inputs are unchanged:
Severity × Action Level only.
"""

t = open(RB, encoding="utf-8").read()
m = re.search(r'(?ms)^### §9 col 17 — the specificity test \(worked example.*?(?=^### Channel A — company response)', t)
if m:
    t = t[:m.start()] + NEW + "\n" + t[m.end():]
    open(RB, "w", encoding="utf-8").write(t)
    print(f"rulebook: withdrawn section replaced ({m.end()-m.start()} chars -> {len(NEW)})")
else:
    print("rulebook: withdrawn section not found — check by hand")

v = open(VA, encoding="utf-8").read()
m = re.search(r'(?ms)^# --- specificity rule \(2026-08-17\).*?and "SPECIFICITY RULE APPLIED" not in str\(r\.get\("Notes"\) or ""\)\]\)\n', v)
if m:
    v = v[:m.start()] + v[m.end():]
    open(VA, "w", encoding="utf-8").write(v)
    print("validator: stale guards removed")
else:
    print("validator: guards not matched — check by hand")
print("GENERAL_RESPONSE still present:", "GENERAL_RESPONSE" in open(VA, encoding="utf-8").read())

if os.path.exists(CSV):
    os.remove(CSV)
    print(f"removed {CSV} — it described the withdrawn rule; the workbook now holds the live values "
          "and every row's Notes records the withdrawal")
