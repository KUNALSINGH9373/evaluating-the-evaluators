#!/usr/bin/env python3
"""Exhaustive duplicate scan over the whole sheet.

The merge-time dedup only compared NEW rows against existing ones, so duplicates *within* the
pre-existing corpus were never tested. This scans all 1,168 rows pairwise.

§5 split-and-club makes some near-identical text legitimate: one finding split by evaluated company
produces sibling rows with the same wording and different Models / Systems. Those are reported
separately from true duplicates.
"""
import sys, os, re, collections, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds

R = list(ds.rows())
tier = lambda r: ("A" if r["Eval? (trackable)"] == "yes" and r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")

norm  = lambda s: re.sub(r'\s+', ' ', (s or '')).strip().lower()
alnum = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower())
toks  = lambda s: set(re.findall(r'[a-z0-9]{4,}', (s or '').lower()))
def jac(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0

def url(u):
    u = (u or '').lower().strip()
    u = re.sub(r'^https?://(www\.)?', '', u).rstrip('/')
    u = re.sub(r'[?#].*$', '', u)
    u = re.sub(r'arxiv\.org/(abs|pdf)/', 'arxiv.org/', u)
    return re.sub(r'v\d+$', '', u)

print(f"scanning {len(R)} rows\n")

# ---- 1. identical primary key -------------------------------------------------------------
d = [k for k, v in collections.Counter(r["Finding ID"] for r in R).items() if v > 1]
print(f"[1] duplicate Finding ID                          : {len(d)}  {d[:5]}")

# ---- 2. byte-identical Finding text ------------------------------------------------------
g = collections.defaultdict(list)
for r in R: g[alnum(r["Finding"])].append(r)
exact = {k: v for k, v in g.items() if len(v) > 1 and k}
print(f"[2] byte-identical Finding text (groups)          : {len(exact)}")
for k, v in list(exact.items()):
    models = {norm(x["Models / Systems"]) for x in v}
    kind = "LEGIT §5 split (different models)" if len(models) == len(v) else "*** SAME MODELS — TRUE DUPLICATE ***"
    print(f"      {kind}")
    for x in v:
        print(f"        [{tier(x)}] {x['Finding ID']:<28} models={(x['Models / Systems'] or '')[:44]}")

# ---- 3. identical Finding Quote ----------------------------------------------------------
gq = collections.defaultdict(list)
for r in R:
    q = alnum(r["Finding Quote"])
    if len(q) > 40: gq[q].append(r)
dupq = {k: v for k, v in gq.items() if len(v) > 1}
print(f"\n[3] identical Finding Quote (groups)              : {len(dupq)}")
susp = 0
for k, v in dupq.items():
    reps = {x["Report ID"] for x in v}
    if len(reps) > 1:      # same quote across DIFFERENT reports is the suspicious case
        susp += 1
        if susp <= 6:
            print(f"      quote shared across {len(reps)} reports:")
            for x in v: print(f"        [{tier(x)}] {x['Finding ID']:<28} {x['Report ID']}")
print(f"      of which span >1 report (suspicious)        : {susp}")

# ---- 4. same report + same models + near-identical finding --------------------------------
print(f"\n[4] near-duplicates WITHIN a report, same models:")
byrep = collections.defaultdict(list)
for r in R: byrep[r["Report ID"]].append(r)
n4 = 0
for rid, rows in byrep.items():
    for a, b in itertools.combinations(rows, 2):
        if norm(a["Models / Systems"]) != norm(b["Models / Systems"]): continue
        s = jac(toks(a["Finding"]), toks(b["Finding"]))
        if s >= 0.75:
            n4 += 1
            if n4 <= 12:
                print(f"      sim={s:.2f}  {a['Finding ID']:<26} <-> {b['Finding ID']:<26} [{rid}]")
                print(f"                 {a['Finding'][:88]}")
                print(f"                 {b['Finding'][:88]}")
print(f"      total: {n4}")

# ---- 5. cross-report near-duplicates on the SAME source URL ------------------------------
print(f"\n[5] near-duplicates sharing a Source URL but different Report ID:")
byurl = collections.defaultdict(list)
for r in R: byurl[url(r["Source URL"])].append(r)
n5 = 0
for u, rows in byurl.items():
    if len({x["Report ID"] for x in rows}) < 2: continue
    for a, b in itertools.combinations(rows, 2):
        if a["Report ID"] == b["Report ID"]: continue
        if jac(toks(a["Finding"]), toks(b["Finding"])) >= 0.70:
            n5 += 1
            if n5 <= 10:
                print(f"      {a['Finding ID']:<26} <-> {b['Finding ID']:<26}  {u[:56]}")
print(f"      total: {n5}")

# ---- 6. global near-duplicate sweep, blocked on model+domain -----------------------------
print(f"\n[6] global near-duplicates (>=0.85), blocked on models+domain:")
blk = collections.defaultdict(list)
for r in R: blk[(norm(r["Models / Systems"])[:60], norm(r["Domain"]))].append(r)
n6 = 0; seen = set()
for key, rows in blk.items():
    if len(rows) < 2: continue
    for a, b in itertools.combinations(rows, 2):
        if a["Report ID"] == b["Report ID"]: continue
        s = jac(toks(a["Finding"]), toks(b["Finding"]))
        if s >= 0.85:
            pair = tuple(sorted((a["Finding ID"], b["Finding ID"])))
            if pair in seen: continue
            seen.add(pair); n6 += 1
            if n6 <= 12:
                print(f"      sim={s:.2f}  [{tier(a)}]{a['Finding ID']:<26} <-> [{tier(b)}]{b['Finding ID']}")
                print(f"                 {a['Finding'][:86]}")
                print(f"                 {b['Finding'][:86]}")
print(f"      total: {n6}")
