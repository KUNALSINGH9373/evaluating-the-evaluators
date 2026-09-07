#!/usr/bin/env python3
"""Fetch every cited source and test each verbatim as an exact substring.

Heuristics guess; this measures. A quote is EXACT if it appears in the fetched source after
whitespace normalisation only. Anything else is reported with its closest anchor so a human can
see whether it is a fabrication, a paraphrase, or an extraction artefact.
"""
import sys, os, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds
import fetch

norm = lambda s: re.sub(r'\s+', ' ', (s or '')).strip()
# quotes are stored with surrounding quotation marks in some cells
strip_q = lambda s: norm(s).strip('"“”\'')

def loose(s):
    """alphanumeric-only comparator — tolerates hyphenation and punctuation drift ONLY."""
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())

R = list(ds.rows())
PAIRS = [("Finding Quote", "Source URL"),
         ("Channel A Verbatim", "Channel A Evidence"),
         ("Channel B Verbatim", "Channel B Evidence")]

jobs = []
for r in R:
    for qcol, ucol in PAIRS:
        q = strip_q(r[qcol]); u = (r[ucol] or "").strip()
        if not q or len(q) < 25: continue
        m = re.search(r'https?://[^\s,;)\]]+', u)
        if not m: continue
        url = m.group(0)
        # An arXiv /abs/ page is the ABSTRACT landing page — it never contains the paper body, so a
        # body quote can never match it. Resolve to the PDF, which is what the coder actually read.
        url = re.sub(r'arxiv\.org/abs/', 'arxiv.org/pdf/', url)
        jobs.append((r["Finding ID"], qcol, q, url))

print(f"{len(jobs)} verbatim/source pairs to check across {len({j[3] for j in jobs})} distinct URLs\n")

cache = {}
res = collections.Counter(); out = []
for i, (fid, qcol, q, url) in enumerate(jobs, 1):
    if url not in cache:
        try:
            g = fetch.get(url)
            cache[url] = norm(g.get("text") or "") if g.get("ok") else None
        except Exception:
            cache[url] = None
    t = cache[url]
    if t is None:
        res["source unreachable"] += 1; out.append((fid, qcol, "UNREACHABLE", url, q, 0)); continue
    if q in t:
        res["EXACT"] += 1; continue
    if loose(q) in loose(t):
        res["exact after punctuation/hyphen normalisation"] += 1
        out.append((fid, qcol, "LOOSE", url, q, len(t))); continue
    # find the longest leading fragment that IS present, to localise the divergence
    lo, hi, best = 0, len(q), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if q[:mid] and q[:mid] in t: best = mid; lo = mid + 1
        else: hi = mid - 1
    # A short fetch is a stub (nav/boilerplate/JS shell), not evidence the quote is wrong.
    res["NOT FOUND (thin fetch <8k, inconclusive)" if len(t) < 8000 else "NOT FOUND (full doc fetched)"] += 1
    out.append((fid, qcol, f"DIVERGES@{best}", url, q, len(t)))
    if i % 100 == 0: print(f"  {i}/{len(jobs)}", file=sys.stderr)

print("RESULT")
for k, v in res.most_common(): print(f"  {v:>5}  {k}")
json.dump([{"finding_id": a, "column": b, "verdict": c, "url": d, "quote": e, "doc_chars": f}
           for a, b, c, d, e, f in out],
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "logs/verbatim_audit.json"), "w"), indent=1)
print(f"\ndetail -> logs/verbatim_audit.json ({len(out)} non-exact)")
