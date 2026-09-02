#!/usr/bin/env python3
"""Every reported quantity, recomputed from the current sheet. Read-only."""
import sys, os, collections, statistics, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds

R = list(ds.rows())
tier = lambda r: ("A" if r["Eval? (trackable)"] == "yes" and r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")
A = [r for r in R if tier(r) == "A"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]        # headline population
isgap   = lambda r: r["Action Level"] == "None"
isshort = lambda r: r["Proportionality"] != "Proportionate"
pc = lambda n, d: f"{n}/{d} = {n/d*100:.1f}%" if d else "n/a"

print("="*78); print("CORPUS"); print("="*78)
t = collections.Counter(tier(r) for r in R)
print(f"  findings              {len(R)}")
print(f"  reports               {len({r['Report ID'] for r in R})}")
print(f"  source URLs           {len({r['Source URL'].lower() for r in R if r['Source URL']})}")
print(f"  institutions          {len({r['Institution'] for r in R})}")
d = sorted(r["Publication Date"][:10] for r in R if r["Publication Date"])
print(f"  window                {d[0]} .. {d[-1]}")
print(f"  Tier A {t['A']} · B {t['B']} · C {t['C']}")

print("\n"+"="*78); print("HEADLINE"); print("="*78)
print(f"  Tier A                          {len(A)}")
print(f"  of which C1 (headline pop)      {len(H)}")
print(f"  NO DOCUMENTED RESPONSE          {pc(sum(1 for r in H if isgap(r)), len(H))}")
print(f"  FALLS SHORT (not proportionate) {pc(sum(1 for r in H if isshort(r)), len(H))}")

print("\n"+"="*78); print("CHANNEL A — company response (Tier A)"); print("="*78)
for k, v in collections.Counter(r["Action Level"] for r in A).most_common():
    print(f"  {k or '(blank)':<16} {v:>4}   {v/len(A)*100:>5.1f}%")
print("\n  on the C1 headline population:")
for k, v in collections.Counter(r["Action Level"] for r in H).most_common():
    print(f"  {k or '(blank)':<16} {v:>4}   {v/len(H)*100:>5.1f}%")

print("\n"+"="*78); print("PROPORTIONALITY"); print("="*78)
for k, v in collections.Counter(r["Proportionality"] for r in A).most_common():
    print(f"  {k or '(blank)':<34} {v:>4}   {v/len(A)*100:>5.1f}%")

print("\n"+"="*78); print("CHANNEL B — policy uptake (Tier A)"); print("="*78)
for k, v in collections.Counter(r["Policy Level"] for r in A).most_common():
    print(f"  {k or '(blank)':<38} {v:>4}   {v/len(A)*100:>5.1f}%")

print("\n"+"="*78); print("SEVERITY"); print("="*78)
for k, v in collections.Counter(r["Severity (C1/C2) majority"] for r in R).most_common():
    print(f"  {k or '(blank)':<8} {v:>5}   {v/len(R)*100:>5.1f}%   (corpus)")
print(f"  C1 share within Tier A: {pc(len(H), len(A))}")
una = sum(1 for r in R if len({r['Sonnet5 vote'], r['GPT-5.5 vote'], r['Gemini3.1 vote']}) == 1)
print(f"  unanimous across the 3 models: {pc(una, len(R))}")

print("\n"+"="*78); print("ROBUSTNESS — is the headline an artefact of unit choice?"); print("="*78)
print(f"  finding-weighted        {pc(sum(1 for r in H if isshort(r)), len(H))}")
byrep = collections.defaultdict(list)
for r in H: byrep[r["Report ID"]].append(r)
rs = [any(isshort(x) for x in v) for v in byrep.values()]
print(f"  report-weighted         {pc(sum(rs), len(rs))}   (a report counts once)")
byinst = collections.defaultdict(list)
for r in H: byinst[r["Institution"]].append(r)
iw = statistics.mean(sum(1 for x in v if isshort(x))/len(v) for v in byinst.values())
print(f"  institution-weighted    {iw*100:.1f}%   (mean of per-institution rates, n={len(byinst)})")
allA = [r for r in A if r["Action Level"]]
print(f"  all Tier A (ignore sev) {pc(sum(1 for r in allA if isshort(r)), len(allA))}")
C2 = [r for r in A if r["Severity (C1/C2) majority"] == "C2" and r["Action Level"]]
print(f"  C2 only                 {pc(sum(1 for r in C2 if isshort(r)), len(C2))}")

def z2(a_n, a_d, b_n, b_d):
    if not a_d or not b_d: return None
    p = (a_n + b_n) / (a_d + b_d)
    se = math.sqrt(p*(1-p)*(1/a_d + 1/b_d))
    if se == 0: return None
    z = (a_n/a_d - b_n/b_d)/se
    return z, math.erfc(abs(z)/math.sqrt(2))

print("\n"+"="*78); print("SUBGROUP TESTS (two-proportion z)"); print("="*78)
g = [r for r in H if r["Scope"] == "government-AISI"]; tp = [r for r in H if r["Scope"] == "third-party-evaluator"]
print(f"  government-AISI      {pc(sum(1 for r in g if isshort(r)), len(g))}")
print(f"  third-party          {pc(sum(1 for r in tp if isshort(r)), len(tp))}")
r_ = z2(sum(1 for r in g if isshort(r)), len(g), sum(1 for r in tp if isshort(r)), len(tp))
print(f"  -> z={r_[0]:+.2f}  p={r_[1]:.3f}   {'no difference' if r_[1]>0.05 else 'DIFFERENT'}")
c1 = [r for r in A if r["Severity (C1/C2) majority"]=="C1" and r["Action Level"]]
c2 = [r for r in A if r["Severity (C1/C2) majority"]=="C2" and r["Action Level"]]
print(f"\n  does severity predict a response?")
print(f"  C1 no-response       {pc(sum(1 for r in c1 if isgap(r)), len(c1))}")
print(f"  C2 no-response       {pc(sum(1 for r in c2 if isgap(r)), len(c2))}")
r_ = z2(sum(1 for r in c1 if isgap(r)), len(c1), sum(1 for r in c2 if isgap(r)), len(c2))
print(f"  -> z={r_[0]:+.2f}  p={r_[1]:.3f}   {'severity does NOT predict response' if r_[1]>0.05 else 'severity PREDICTS response'}")
pre = [r for r in H if r["Access Type"]=="Pre-deployment"]; post=[r for r in H if r["Access Type"]=="Post-deployment"]
print(f"\n  pre-deployment       {pc(sum(1 for r in pre if isgap(r)), len(pre))}")
print(f"  post-deployment      {pc(sum(1 for r in post if isgap(r)), len(post))}")
r_ = z2(sum(1 for r in pre if isgap(r)), len(pre), sum(1 for r in post if isgap(r)), len(post))
if r_: print(f"  -> z={r_[0]:+.2f}  p={r_[1]:.3f}")

print("\n"+"="*78); print("LAG (days), rows with a response"); print("="*78)
lags=[]
for r in A:
    v=(r["Lag (days)"] or "").strip()
    if v:
        try: lags.append(int(float(v)))
        except ValueError: pass
if lags:
    lags.sort()
    print(f"  n={len(lags)}  median={statistics.median(lags):.0f}  mean={statistics.mean(lags):.0f}")
    print(f"  min={lags[0]}  max={lags[-1]}  negative (pre-deployment)={sum(1 for x in lags if x<0)}  zero={sum(1 for x in lags if x==0)}")

print("\n"+"="*78); print("BY COMPANY (headline population, n>=4)"); print("="*78)
import re
DEV=[("Anthropic",r"claude|opus|sonnet|haiku|mythos|fable"),("OpenAI",r"gpt|o1|o3|o4|chatgpt|codex"),
     ("Google",r"gemini|gemma"),("Meta",r"llama|muse"),("xAI",r"grok"),("DeepSeek",r"deepseek"),
     ("Alibaba",r"qwen"),("Mistral",r"mistral"),("Zhipu",r"glm")]
for name,pat in DEV:
    S=[r for r in H if re.search(pat,(r["Models / Systems"] or ""),re.I)]
    if len(S)>=4: print(f"  {name:<12} n={len(S):>3}  no action {pc(sum(1 for r in S if isgap(r)), len(S))}")

print("\n"+"="*78); print("BY YEAR (headline population)"); print("="*78)
for y in sorted({r["Publication Date"][:4] for r in H}):
    S=[r for r in H if r["Publication Date"].startswith(y)]
    print(f"  {y}  n={len(S):>3}  no action {pc(sum(1 for r in S if isgap(r)), len(S))}   falls short {pc(sum(1 for r in S if isshort(r)), len(S))}")

print("\n"+"="*78); print("BY DOMAIN (headline population)"); print("="*78)
dc=collections.Counter(x.strip() for r in H for x in (r["Domain"] or "").split(";") if x.strip())
for dom,_ in dc.most_common(9):
    S=[r for r in H if dom in [x.strip() for x in (r["Domain"] or "").split(";")]]
    print(f"  {dom:<20} n={len(S):>3}  no action {pc(sum(1 for r in S if isgap(r)), len(S))}")
