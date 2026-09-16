#!/usr/bin/env python3
"""Phase 0 of the window extension — deterministic triage. No agents, no network.

The venues were already paginated to the end, so the back-catalogue is enumerated: the ledger
holds items to 1962. What was never done is READING the pre-2023 items that title-triage excluded.
This ranks those by whether the title looks like an evaluation, so agents only ever see plausible
candidates and every drop is a reproducible rule rather than an opinion.

    python3 sweep_triage.py [--start 2018-01-01]
"""
import argparse, csv, collections, os, re, json, datetime

LED = os.path.expanduser("~/MATS/Research/AISI_Evals/sweep/master_ledger.csv")
OUT = os.path.expanduser("~/MATS/Research/AISI_Evals/logs/window_extension")

RETIRE = ("not a roster org", "venue retired", "out-of-scope org")

# An evaluation report names a thing tested, or a way of testing. Governance and methodology
# findings qualify too (rulebook §2), so the vocabulary deliberately reaches past capability work.
POS = r"""evaluat|benchmark|red.?team|jailbreak|capabilit|assess|audit|adversarial|robust|
    attack|vulnerab|exploit|uplift|elicit|safety.case|measur|probe|stress.test|
    scorecard|leaderboard|test(ing|ed|s)?\b|risk|threat|misuse|harm|bio|cyber|
    autonom|deceiv|deception|sandbag|scheming|persuas|agent|
    gpt|claude|llama|gemini|mistral|qwen|deepseek|grok|o1|o3|frontier|
    system.card|model.card"""
# Titles that are almost never a finding — announcements, hiring, events, opinion.
NEG = r"""we.?re hiring|join us|careers|newsletter|podcast|webinar|event|conference|
    workshop|call for|register|announc|partner(ship|ing)|welcome|introducing our team|
    appoint|obituar|in memoriam|press release|media advisory|save the date"""
POS_RE = re.compile(POS, re.I | re.X)
NEG_RE = re.compile(NEG, re.I | re.X)


def year(row):
    m = re.match(r"(\d{4})", (row.get("publication_date") or "").strip())
    return int(m.group(1)) if m else None


ap = argparse.ArgumentParser()
ap.add_argument("--start", default="2018-01-01")
a = ap.parse_args()
START = int(a.start[:4])
os.makedirs(OUT, exist_ok=True)

led = list(csv.DictReader(open(LED, newline="")))
retired = {r["venue"] for r in led if any(k in (r.get("decision") or "") for k in RETIRE)}
active = [r for r in led if r["venue"] not in retired]

dated = [r for r in active if year(r)]
undated = [r for r in active if not year(r)]
window = [r for r in dated if START <= year(r) < 2023]
tri = [r for r in window if "not an evaluation" in (r.get("decision") or "")]

scored = []
for r in tri:
    t = (r.get("item_title") or "") + " " + (r.get("url") or "")
    pos = len(set(m.group(0).lower() for m in POS_RE.finditer(t)))
    neg = bool(NEG_RE.search(t))
    scored.append({"venue": r["venue"], "title": r.get("item_title"), "url": r.get("url"),
                   "date": r.get("publication_date"), "signals": pos, "negative": neg,
                   "shortlist": pos >= 1 and not neg})

short = [s for s in scored if s["shortlist"]]
json.dump(short, open(f"{OUT}/shortlist_backcatalogue.json", "w"), indent=1)
json.dump(scored, open(f"{OUT}/triage_all.json", "w"), indent=1)

print(f"WINDOW {a.start} -> 2022-12-31   (retired venues excluded: {len(retired)})\n")
print(f"  active-venue items dated in window            {len(window):>5}")
print(f"  of those, title-triaged and never read        {len(tri):>5}   <- the candidate pool")
print(f"  shortlisted by the signal rule                {len(short):>5}   <- agents see only these")
print(f"  dropped: no evaluation signal in the title    {sum(1 for s in scored if not s['negative'] and s['signals']==0):>5}")
print(f"  dropped: negative signal (event/hiring/etc)   {sum(1 for s in scored if s['negative']):>5}")
print(f"\n  shortlist by venue:")
for v, n in collections.Counter(s["venue"] for s in short).most_common():
    print(f"     {v[:46]:<46} {n}")
print(f"\n  shortlist by year:")
for y, n in sorted(collections.Counter(s["date"][:4] for s in short if s["date"]).items()):
    print(f"     {y}  {n}")
print(f"\n  undated active-venue rows (need a date before they can be placed): {len(undated)}")
print(f"\nwritten: {OUT}/shortlist_backcatalogue.json")
