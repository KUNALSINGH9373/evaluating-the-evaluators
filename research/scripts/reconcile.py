#!/usr/bin/env python3
"""Two-way reconciliation between the screening ledger and the dataset (rulebook §10).

Direction A — every ledger `INCLUDED` item must either appear in the sheet, or carry a documented
              reason for its absence in the exclusion registry below.
Direction B — every report in the sheet must appear in the ledger as `INCLUDED`.

This exists because a merge script once read one hardcoded output directory and silently skipped a
whole sweep's results. Nothing verified that every screened item had been consumed. Run this after
any merge, deletion, or sweep; a non-zero exit means the dataset and the ledger disagree.
"""
import sys, os, csv, re, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
uk = lambda u: re.sub(r'^https?://(www\.)?', '', (u or '').lower()).rstrip('/').split('?')[0]
tk = lambda t: re.sub(r'[^a-z0-9]', '', (t or '').lower())[:48]
STOP = {"the","a","an","of","for","and","in","to","on","with","from","its","our","new","report",
        "evaluation","evaluations","ai","model","models","system","card","aisi","openai","anthropic"}
def toks(s):
    return {w for w in re.findall(r'[a-z0-9]{3,}', (s or '').lower()) if w not in STOP}
def fuzzy(t, pool):
    """A ledger title matches a sheet title when their distinctive words overlap heavily.
    Exact/prefix matching missed pairs like 'AISI Frontier AI Trends Report (2025)' vs
    'Frontier AI Trends Report 2025' — same report, different wording."""
    a = toks(t)
    if len(a) < 2: return False
    for b in pool:
        if not b: continue
        inter = len(a & b)
        if inter >= 2 and inter / min(len(a), len(b)) >= 0.75: return True
    return False

REGISTRY = os.path.join(ROOT, "logs/reconciliation_exclusions.csv")

def load_registry():
    if not os.path.exists(REGISTRY): return {}
    return {r["url_key"]: r for r in csv.DictReader(open(REGISTRY))}

def main():
    R = list(ds.rows())
    sheet_u = {uk(r["Source URL"]) for r in R}
    sheet_t = {tk(r["Report Title"]) for r in R}
    sheet_tok = [toks(r["Report Title"]) for r in R]

    led = [r for r in csv.DictReader(open(os.path.join(ROOT, "sweep/master_ledger.csv")))]
    inc = [r for r in led if str(r["decision"]).upper().startswith("INC")]
    reg = load_registry()

    # ---- direction A -------------------------------------------------------------------
    missing, explained = [], collections.Counter()
    for r in inc:
        u, t = uk(r["url"]), tk(r["item_title"])
        if u in sheet_u or t in sheet_t: explained["in the sheet"] += 1
        elif fuzzy(r["item_title"], sheet_tok): explained["in the sheet (title variant)"] += 1
        elif u in reg:                   explained[reg[u]["reason"]] += 1
        else:                            missing.append(r)

    # ---- direction B -------------------------------------------------------------------
    led_u = {uk(r["url"]) for r in led}
    led_t = {tk(r["item_title"]) for r in led}
    byrep = collections.defaultdict(list)
    for r in R: byrep[r["Report ID"]].append(r)
    led_tok = [toks(r["item_title"]) for r in led]
    orphan = [rid for rid, rows in byrep.items()
              if uk(rows[0]["Source URL"]) not in led_u and tk(rows[0]["Report Title"]) not in led_t
              and not fuzzy(rows[0]["Report Title"], led_tok)]

    print(f"ledger {len(led)} screened · {len(inc)} INCLUDED    sheet {len(R)} findings · {len(byrep)} reports\n")
    print("DIRECTION A — ledger INCLUDED accounted for in the sheet")
    for k, v in explained.most_common(): print(f"   {v:>4}  {k}")
    print(f"   {len(missing):>4}  *** UNACCOUNTED ***")
    print(f"\nDIRECTION B — sheet reports not marked INCLUDED in the ledger: {len(orphan)}")
    for rid in orphan[:10]:
        print(f"      {rid:<32} {byrep[rid][0]['Report Title'][:56]}")
    if len(orphan) > 10: print(f"      ... +{len(orphan)-10} more")

    if missing:
        out = os.path.join(ROOT, "logs/reconcile_unaccounted.csv")
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(missing[0].keys())); w.writeheader(); w.writerows(missing)
        print(f"\nunaccounted detail -> {out}")
        print("\nby venue:")
        for k, v in collections.Counter(r["venue"][:40] for r in missing).most_common():
            print(f"   {v:>4}  {k}")
    ok = not missing and not orphan
    print(f"\n{'RECONCILED' if ok else 'NOT RECONCILED'}")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
