#!/usr/bin/env python3
"""For each UNSUPPORTED quote, measure how much of it IS present in the source.

A binary found/not-found verdict cannot separate a genuine paraphrase from a character-exact quote
carrying one transcription slip. Longest-common-substring coverage can:

   >=0.70  near-exact — a small drift (a digit, a hyphen, a dropped word). Repairable.
   0.30-0.70  reassembled from real source material but not a quote. Should be re-extracted.
   <0.30   paraphrase — the cell is the coder's own words in a verbatim column.
"""
import sys, os, re, json, collections
from difflib import SequenceMatcher
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch

norm = lambda s: re.sub(r'\s+', ' ', (s or '')).strip()
T = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs/verbatim_triage.json")))
U = [x for x in T if x["verdict"] == "UNSUPPORTED"]
print(f"measuring coverage for {len(U)} UNSUPPORTED quotes\n")

import dataset_source as ds
QROW = {(r["Finding ID"]): r for r in ds.rows()}

cache, out, band = {}, [], collections.Counter()
for i, x in enumerate(U, 1):
    u = x["url"]
    if u not in cache:
        try:
            g = fetch.get(u); cache[u] = norm(g.get("text") or "") if g.get("ok") else None
        except Exception: cache[u] = None
    t = cache[u]
    if not t: band["unreachable"] += 1; continue
    q = norm(QROW[x["finding_id"]][x["column"]]).strip('"“”')
    q = re.sub(r'^\s*\[[^\]]{3,140}\]\s*:?\s*', '', q)
    if len(q) < 22: continue
    sm = SequenceMatcher(None, q.lower(), t.lower(), autojunk=False)
    m = sm.find_longest_match(0, len(q), 0, len(t))
    cov = m.size / len(q)
    b = "near-exact (>=0.70)" if cov >= .70 else "reassembled (0.30-0.70)" if cov >= .30 else "paraphrase (<0.30)"
    band[b] += 1
    out.append({"finding_id": x["finding_id"], "column": x["column"], "coverage": round(cov, 3),
                "band": b, "url": u, "quote": q[:200],
                "longest_match": q[m.a:m.a + m.size][:160]})
    if i % 25 == 0: print(f"  {i}/{len(U)}", file=sys.stderr)

print("COVERAGE BANDS")
for k, v in band.most_common(): print(f"  {v:>4}  {k}")
out.sort(key=lambda z: z["coverage"])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                 "logs/verbatim_coverage.json"), "w"), indent=1)
print("\nWORST 12 (lowest coverage = most likely the coder's own words):")
for z in out[:12]:
    print(f"  {z['coverage']:.2f}  {z['finding_id']:<24} [{z['column']}]")
    print(f"        quote:   {z['quote'][:104]}")
    print(f"        matched: {z['longest_match'][:104]}")
