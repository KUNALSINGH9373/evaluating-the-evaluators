#!/usr/bin/env python3
"""Fragment-level triage of the quotes that failed whole-string matching.

A quote may legitimately be a composite: fragments joined by an ellipsis, or a table/figure
transcription behind a [locator] prefix. Whole-string matching calls all of those failures. This
splits each quote into its fragments and checks each one, which separates:

  COMPOSITE-OK   every fragment appears verbatim -> the cell is faithful, just not contiguous
  PARTIAL        some fragments appear, others do not -> needs a human look
  UNSUPPORTED    no fragment appears -> the cell is not backed by the cited source
"""
import sys, os, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch

norm = lambda s: re.sub(r'\s+', ' ', (s or '')).strip()
loose = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower())
LEAD = re.compile(r'^\s*\[[^\]]{3,140}\]\s*:?\s*')

def fragments(q):
    q = LEAD.sub('', q)                      # drop the table/figure locator
    parts = re.split(r'\s*(?:\.\.\.|…)\s*', q)          # ellipsis joins
    out = []
    for p in parts:
        p = p.strip().strip('"“”\'')
        # a long fragment is still often several sentences welded together
        out += [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z"])', p)] if len(p) > 180 else [p]
    return [f for f in out if len(f) >= 22]

D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs/verbatim_audit.json")))
hard = [d for d in D if d["verdict"].startswith("DIVERGES") and d["doc_chars"] >= 8000]
print(f"triaging {len(hard)} hard failures\n")

cache, res, rows = {}, collections.Counter(), []
for i, d in enumerate(hard, 1):
    u = d["url"]
    if u not in cache:
        try:
            g = fetch.get(u); cache[u] = norm(g.get("text") or "") if g.get("ok") else None
        except Exception: cache[u] = None
    t = cache[u]
    if not t: res["unreachable on recheck"] += 1; continue
    tl = loose(t)
    frags = fragments(d["quote"])
    if not frags: res["no testable fragment"] += 1; continue
    hits = [f for f in frags if f in t or loose(f) in tl]
    v = ("COMPOSITE-OK" if len(hits) == len(frags) else
         "UNSUPPORTED" if not hits else "PARTIAL")
    res[v] += 1
    if v != "COMPOSITE-OK":
        rows.append({"finding_id": d["finding_id"], "column": d["column"], "verdict": v,
                     "frags_total": len(frags), "frags_found": len(hits), "url": u,
                     "missing": [f[:160] for f in frags if f not in hits][:3]})
    if i % 50 == 0: print(f"  {i}/{len(hard)}", file=sys.stderr)

print("RESULT")
for k, v in res.most_common(): print(f"  {v:>4}  {k}")
json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                                  "logs/verbatim_triage.json"), "w"), indent=1)
print(f"\n{len(rows)} rows need a human look -> logs/verbatim_triage.json")
