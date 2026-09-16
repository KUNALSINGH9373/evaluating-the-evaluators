#!/usr/bin/env python3
"""Recompute every number quoted in the deck and diff it against the file."""
import openpyxl, os, re, collections, datetime

P = os.path.expanduser("~/Desktop/AISIEVAL.xlsx")
DECK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck.html")
ws = openpyxl.load_workbook(P, data_only=True)[openpyxl.load_workbook(P).sheetnames[0]]
hdr = [c.value for c in ws[1]]
ix = {h: i + 1 for i, h in enumerate(hdr) if h}


def norm(v):
    if v is None:
        return ""
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime("%Y-%m-%d")
    return str(v).strip()


R = [{h: norm(ws.cell(r, ix[h]).value) for h in ix} for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value]
tier = lambda r: ("A" if r["Action Trackable?"] == "yes" else "B" if r["Eval? (trackable)"] == "yes" else "C")
A = [r for r in R if tier(r) == "A"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]
n = len(H)
GAPV = "Accountability gap (no action)"

facts = {}
facts["corpus"] = len(R)
facts["reports"] = len({r["Report ID"] for r in R if r["Report ID"]})
facts["evaluators"] = len({r["Institution"] for r in R})
facts["tierA"] = len(A)
facts["C1"] = n
c = collections.Counter(r["Proportionality"] for r in H)
facts["no action"] = c[GAPV]
facts["under"] = c["Under-response (gap)"]
facts["proportionate"] = c["Proportionate"]
facts["falls short"] = c[GAPV] + c["Under-response (gap)"]
al = collections.Counter(r["Action Level"] for r in A)
facts.update({f"AL {k}": v for k, v in al.items()})
at = collections.Counter(r["Attribution"] for r in A)
facts.update({f"attr {k}": v for k, v in at.items()})
pl = collections.Counter(r["Policy Level"] for r in A)
facts.update({f"PL {k}": v for k, v in pl.items()})
sc = collections.Counter(r.get("Scope", "") for r in R)
facts["scope gov (all rows)"] = sc["government-AISI"]
facts["scope 3p (all rows)"] = sc["third-party-evaluator"]

print("=== headline ===")
print(f"  falls short {facts['falls short']}/{n} = {facts['falls short']/n:.1%}")
print(f"  no action   {facts['no action']}/{n} = {facts['no action']/n:.1%}")
print(f"  outcomes    no action {facts['no action']} · under {facts['under']} · proportionate {facts['proportionate']}")
print(f"  action lvl  {dict(al.most_common())}")
print(f"  attribution {dict(at.most_common())}")
print(f"  policy      {dict(pl.most_common())}")

print("\n=== slide 3: government-AISI subset (deck says 32/54 = 59.3%) ===")
g = [r for r in H if r.get("Scope") == "government-AISI"]
gg = sum(1 for r in g if r["Proportionality"] == GAPV)
gs = sum(1 for r in g if r["Proportionality"] != "Proportionate")
print(f"  gov C1 n={len(g)} · no action {gg} = {gg/len(g):.1%} · falls short {gs} = {gs/len(g):.1%}")

print("\n=== slide 7: gap rate by year (deck says 40/50/72/60) ===")
for y in sorted({r["Publication Date"][:4] for r in H if r["Publication Date"]}):
    yr = [r for r in H if r["Publication Date"][:4] == y]
    ygap = sum(1 for r in yr if r["Proportionality"] == GAPV)
    yshort = sum(1 for r in yr if r["Proportionality"] != "Proportionate")
    print(f"  {y}  n={len(yr):>3}  no-action {ygap:>3} = {ygap/len(yr):>4.0%}   falls-short {yshort:>3} = {yshort/len(yr):>4.0%}")

print("\n=== slide 4 domain counts (deck slide 4 dropped; kept for reserve fig 11) ===")
d = collections.Counter()
for r in H:
    for x in r.get("Domain", "").split(";"):
        if x.strip():
            d[x.strip()] += 1
print("  ", d.most_common(6))

print("\n=== numbers appearing in the deck file, for eyeballing ===")
t = open(DECK, encoding="utf-8").read()
body = re.sub(r'<style.*?</style>', '', t, flags=re.S)
nums = sorted(set(re.findall(r'(?<![\w.])(\d[\d,]*(?:\.\d+)?%?)(?![\w])', re.sub(r'<[^>]+>', ' ', body))))
print("  ", " ".join(nums))
