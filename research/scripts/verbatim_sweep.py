#!/usr/bin/env python3
"""Check every stored verbatim against the document it cites.

Motivated by APOLLO-2025-08-ALI2, whose Channel A quote reads "We constructed 13 environments"
while the GPT-5 system card reads "We constructed environments" — the 13 is a page-number footer
that a PDF text layer inserted mid-sentence and a copy-paste swallowed. Any quote spanning a page
break can pick up the footer the same way, so this is a class of defect, not one row.

For each Tier A row with a verbatim and an evidence URL: fetch the source through the ladder,
normalise whitespace, and look for the quote. Report NOT FOUND, and separately flag quotes
containing a bare digit-run mid-sentence, which is the footer signature.

    python3 verbatim_sweep.py [--channel a|b] [--limit N]

Writes logs/verbatim_sweep_<date>.json. Reads only; changes nothing.
"""
import sys, os, re, json, argparse, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds
from fetch import get

norm = lambda s: re.sub(r"\s+", " ", str(s or "")).strip()

# Typographic noise is not a defect. A PDF or HTML text layer routinely differs from a pasted
# quote in curly quotes, dash width, ellipsis glyph, and words broken across a line. Level 1
# normalises those away; level 2 strips to alphanumerics only, so anything still failing level 2
# is a genuine content mismatch rather than a rendering artifact.
_SUB = {"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-", "\u2212": "-", "\u2026": "...", "\u00a0": " ", "|": " "}


def soft(s):
    s = norm(s)
    for k, v in _SUB.items():
        s = s.replace(k, v)
    return re.sub(r"\s+", " ", s).strip().lower()


def hard(s):
    return re.sub(r"[^a-z0-9]+", "", soft(s))
FOOTER = re.compile(r"[a-z,;]\s+\d{1,3}\s+[a-z]")     # "...constructed 13 environments..."


def url_of(cell):
    m = re.match(r"\s*(https?://\S+)", str(cell or ""))
    return m.group(1).rstrip(").,;|") if m else ""


def check(quote, page_text):
    q, p = norm(quote).lower(), norm(page_text).lower()
    if not q or not p:
        return "no-data", None
    if q in p:
        return "exact", None
    if soft(quote) in soft(page_text):
        return "exact-modulo-typography", None
    if hard(quote) and hard(quote) in hard(page_text):
        return "exact-modulo-linebreaks", None
    # try the longest leading fragment that does match, to locate where it diverges
    lo, hi = 0, len(q)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if q[:mid] in p: lo = mid
        else: hi = mid - 1
    if lo >= 40:
        return "diverges", {"matched_chars": lo, "quote_continues": norm(quote)[lo:lo + 90]}
    return "not-found", {"matched_chars": lo}


ap = argparse.ArgumentParser()
ap.add_argument("--channel", default="a", choices=["a", "b"])
ap.add_argument("--limit", type=int, default=0)
a = ap.parse_args()
VB = "Channel A Verbatim" if a.channel == "a" else "Channel B Verbatim"
EV = "Channel A Evidence" if a.channel == "a" else "Channel B Evidence"

rows = [r for r in ds.rows()
        if r["Eval? (trackable)"] == "yes" and r["Action Trackable?"] == "yes"
        and norm(r.get(VB)) and url_of(r.get(EV))]
if a.limit: rows = rows[:a.limit]
print(f"Channel {a.channel.upper()}: {len(rows)} Tier A rows carry both a verbatim and an evidence URL\n")

cache, out, counts = {}, [], {}
for i, r in enumerate(rows, 1):
    u = url_of(r[EV])
    if u not in cache: cache[u] = get(u)
    f = cache[u]
    if not f["ok"]:
        verdict, detail = "unfetchable", {"status": f["status"], "attempts": f["attempts"]}
    else:
        verdict, detail = check(r[VB], f["text"])
    footer = bool(FOOTER.search(norm(r[VB])))
    counts[verdict] = counts.get(verdict, 0) + 1
    out.append({"finding_id": r["Finding ID"], "verdict": verdict, "footer_signature": footer,
                "url": u, "via": f.get("via"), "detail": detail,
                "quote_head": norm(r[VB])[:120]})
    if verdict in ("not-found", "diverges") or (footer and verdict != "exact"):
        print(f"  [{verdict:<11}] {r['Finding ID']:<28} {'FOOTER?' if footer else '':<8} {u[:60]}")
        if detail and detail.get("quote_continues"):
            print(f"                  matched {detail['matched_chars']} chars, then quote says: "
                  f"{detail['quote_continues'][:70]!r}")
    if i % 25 == 0: print(f"  ... {i}/{len(rows)}")

p = os.path.expanduser(f"~/MATS/Research/AISI_Evals/logs/verbatim_sweep_{a.channel}_"
                       f"{datetime.date.today()}.json")
json.dump(out, open(p, "w"), indent=1)
print("\nSUMMARY:", counts)
print("quotes carrying a mid-sentence digit-run (footer signature):",
      sum(1 for x in out if x["footer_signature"]))
print("written:", p)
