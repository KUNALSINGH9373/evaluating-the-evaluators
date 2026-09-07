#!/usr/bin/env python3
"""Full-sheet audit: IDs, dates, titles, links, verbatims, and cross-column coherence.

Deterministic only — no network. Every finding is printed with its row so it can be fixed or
dismissed individually. Nothing is modified.
"""
import sys, os, re, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds

R = list(ds.rows())
NEW = {r["Finding ID"] for r in R if "window-extension sweep" in (r["Sources Checked (channel A)"] or "")}
tier = lambda r: ("A" if r["Eval? (trackable)"] == "yes" and r["Action Trackable?"] == "yes"
                  else "B" if r["Eval? (trackable)"] == "yes" else "C")
A = [r for r in R if tier(r) == "A"]

issues = collections.OrderedDict()
def flag(name, rows, note=""):
    if rows: issues[name] = (rows, note)

WINDOW = (datetime.date(2018, 1, 1), datetime.date(2026, 8, 29))
def d(s):
    s = (s or "")[:10]
    try: return datetime.date.fromisoformat(s)
    except Exception: return None

# ---------- 1. IDENTIFIERS -------------------------------------------------------------------
ids = [r["Finding ID"] for r in R]
flag("duplicate Finding ID", [k for k, v in collections.Counter(ids).items() if v > 1])
flag("Finding ID blank", [f"row {i+2}" for i, r in enumerate(R) if not r["Finding ID"].strip()])
# PREFIX-YYYY-MM[m]-DDDn[-sN]; legacy variants grandfathered
FMT = re.compile(r'^[A-Z][A-Z0-9\-]*-\d{4}-\d{2}[a-zB]?-[A-Z]{3}\d+[a-b]?(-s\d+)?$')
flag("Finding ID not matching §6.1 format", [r["Finding ID"] for r in R if not FMT.match(r["Finding ID"])])
flag("Report ID blank", [r["Finding ID"] for r in R if not (r["Report ID"] or "").strip()])
# §6.2 all rows sharing a Report ID share Title, URL and Publication Date
g = collections.defaultdict(set)
for r in R: g[r["Report ID"]].add((r["Report Title"].strip(), (r["Source URL"] or "").strip(), r["Publication Date"][:10]))
flag("Report ID covering >1 distinct (title,url,date)", [k for k, v in g.items() if len(v) > 1])
# the reverse: one report (same URL) filed under two Report IDs
u = collections.defaultdict(set)
for r in R:
    if r["Source URL"]: u[r["Source URL"].strip().lower()].add(r["Report ID"])
flag("one Source URL filed under >1 Report ID", [f"{k[:70]} -> {sorted(v)}" for k, v in u.items() if len(v) > 1])
# The URL check above only catches a report re-filed under the SAME link. One paper reached the
# sheet under two Report IDs fourteen times with two DIFFERENT links -- an arXiv page and the
# institution's own write-up, or a blog post and a later research page -- so the URL never
# collided and nothing flagged it. Two ingestion passes produced two ID conventions
# (INST-YYYY-MM[letter] and INST-YYYY-MM-<abbreviated title>) and the v12->v13 reconciliation
# preserved both, because it asserted no row was MISSING and never that none was duplicated.
# Match on the title instead, normalised so punctuation, case, and a trailing venue tag
# ("(ACL 2025)", "(NAACL 2024)") cannot hide the collision.
def _norm_title(t):
    t = re.sub(r'\((?:ACL|NAACL|EMNLP|ICML|NeurIPS|ICLR|AAAI|IJCAI|CVPR|ICCV|COLM|TMLR|'
               r'Findings)[^)]*\)', ' ', t or '', flags=re.I)
    t = re.sub(r'\b(llms?|language models?)\b', 'lm', t.lower())
    return ' '.join(re.sub(r'[^a-z0-9 ]', ' ', t).split())
tt = collections.defaultdict(set)
for r in R:
    if r["Report Title"].strip(): tt[_norm_title(r["Report Title"])].add(r["Report ID"])
flag("one report title filed under >1 Report ID",
     [f"{k[:66]} -> {sorted(v)}" for k, v in tt.items() if len(v) > 1])
# ID prefix should match the institution's registered prefix
flag("Finding ID prefix disagrees with Report ID prefix",
     [r["Finding ID"] for r in R
      if r["Report ID"] and r["Finding ID"].split("-")[0] != r["Report ID"].split("-")[0]])

# ---------- 2. DATES -------------------------------------------------------------------------
flag("Publication Date not ISO", [r["Finding ID"] for r in R if not d(r["Publication Date"])])
flag("Publication Date outside the corpus window 2018-01-01..2026-08-29",
     [f'{r["Finding ID"]} {r["Publication Date"][:10]}' for r in R
      if d(r["Publication Date"]) and not (WINDOW[0] <= d(r["Publication Date"]) <= WINDOW[1])])
flag("Response Date not ISO",
     [r["Finding ID"] for r in R if (r["Response Date"] or "").strip() and not d(r["Response Date"])])
flag("Response Date in the future", [r["Finding ID"] for r in R
     if d(r["Response Date"]) and d(r["Response Date"]) > WINDOW[1]])
# Lag exists <=> Response Date exists, and Lag == Response - Publication
bad = []
for r in R:
    rd, pd, lag = d(r["Response Date"]), d(r["Publication Date"]), (r["Lag (days)"] or "").strip()
    if rd and not lag: bad.append(f'{r["Finding ID"]} has Response Date, no Lag')
    elif lag and not rd: bad.append(f'{r["Finding ID"]} has Lag, no Response Date')
    elif rd and pd and lag:
        try:
            if int(float(lag)) != (rd - pd).days:
                bad.append(f'{r["Finding ID"]} Lag {lag} != {(rd-pd).days}')
        except ValueError: bad.append(f'{r["Finding ID"]} Lag not numeric: {lag!r}')
flag("Lag (days) incoherent", bad)

# ---------- 3. TITLES / LINKS ----------------------------------------------------------------
flag("Report Title blank", [r["Finding ID"] for r in R if not r["Report Title"].strip()])
flag("Report Title suspiciously short (<12 chars)",
     [f'{r["Finding ID"]}: {r["Report Title"]!r}' for r in R if 0 < len(r["Report Title"].strip()) < 12])
flag("Source URL blank", [r["Finding ID"] for r in R if not (r["Source URL"] or "").strip()])
flag("Source URL malformed",
     [f'{r["Finding ID"]}: {r["Source URL"][:60]}' for r in R
      if r["Source URL"].strip() and not re.match(r'^https?://[^\s]+$', r["Source URL"].strip())])
for col in ("Channel A Evidence", "Channel B Evidence"):
    flag(f"{col} looks like a URL field but holds no URL and no 'Not found' log",
         [r["Finding ID"] for r in R if (r[col] or "").strip()
          and "http" not in r[col].lower() and not r[col].strip().lower().startswith("not found")])

# ---------- 4. VERBATIMS ---------------------------------------------------------------------
def suspicious(q):
    """Heuristics for a quote that was reconstructed rather than copied."""
    out = []
    if not q: return out
    if re.search(r'\b\d{1,3}\s+[a-z]', q) and re.search(r'\.\s*\d{1,3}\s+[a-z]', q):
        out.append("page-number glued mid-sentence")
    if "..." in q or "…" in q: out.append("ellipsis (not character-exact)")
    if re.search(r'\[\w+\]', q): out.append("bracketed editorial insertion")
    if re.search(r'-\s+[a-z]', q): out.append("possible repaired hyphenation")
    return out
for col in ("Finding Quote", "Channel A Verbatim", "Channel B Verbatim", "Channel C Verbatim"):
    rows = []
    for r in R:
        s = suspicious(r[col] or "")
        if s: rows.append(f'{r["Finding ID"]} [{col}] {"; ".join(s)} :: {(r[col] or "")[:70]}')
    flag(f"{col} shows reconstruction markers", rows)
flag("Finding Quote blank on a Tier A row", [r["Finding ID"] for r in A if not (r["Finding Quote"] or "").strip()])

# ---------- 5. CONTROLLED VOCABULARIES --------------------------------------------------------
VOCAB = {
 "Institution Type": {"Government","Non-Profit (AIEF)","For-Profit","Non-Profit (Independent)",
                      "Non-Profit (Independent);Lab","Government;Lab","For-Profit;Lab","Government;For-Profit"},
 "Access Type": {"Pre-deployment","Post-deployment","Mixed","Aggregate","N/A"},
 "Scope": {"government-AISI","third-party-evaluator"},
 "Severity (C1/C2) majority": {"C1","C2"},
 "Human": {"C1","C2"},
 "Action Level": {"Substantive","Partial","Acknowledged","None",""},
 "Attribution": {"Explicit attribution","No explicit attribution","No response located",""},
 "Policy Level": {"Binding policy action","Non-binding policy-related uptake","No policy uptake identified",""},
 "Proportionality": {"Proportionate","Under-response (gap)","Accountability gap (no action)",""},
 "Eval? (trackable)": {"yes","no"},
 "Action Trackable?": {"yes","no",""},
}
for col, ok in VOCAB.items():
    bad = [f'{r["Finding ID"]}: {r[col]!r}' for r in R if r[col] not in ok]
    flag(f"{col} outside its controlled vocabulary", bad)

# ---------- 6. TIER / CHANNEL COHERENCE -------------------------------------------------------
flag("Tier C row with a non-blank Action Trackable?",
     [r["Finding ID"] for r in R if tier(r) == "C" and (r["Action Trackable?"] or "").strip()])
flag("non-Tier-A row carrying an Action Level",
     [r["Finding ID"] for r in R if tier(r) != "A" and (r["Action Level"] or "").strip()])
flag("Tier A row with no Action Level", [r["Finding ID"] for r in A if not (r["Action Level"] or "").strip()])
flag("Action Level None but response fields populated",
     [f'{r["Finding ID"]} [{c}]' for r in A if r["Action Level"] == "None"
      for c in ("Company Response","Channel A Verbatim","Response Date","Channel A Evidence")
      if (r[c] or "").strip()])
flag("Action Level not None but Channel A Evidence empty",
     [r["Finding ID"] for r in A if r["Action Level"] not in ("None","") and not (r["Channel A Evidence"] or "").strip()])
flag("Attribution 'No response located' but Action Level != None",
     [r["Finding ID"] for r in R if r["Attribution"]=="No response located" and r["Action Level"] not in ("None","")])
flag("Action Level None but Attribution != 'No response located'",
     [f'{r["Finding ID"]}: {r["Attribution"]!r}' for r in A if r["Action Level"]=="None" and r["Attribution"]!="No response located"])
MATRIX={("C1","Substantive"):"Proportionate",("C1","Partial"):"Under-response (gap)",
        ("C1","Acknowledged"):"Under-response (gap)",("C1","None"):"Accountability gap (no action)",
        ("C2","Substantive"):"Proportionate",("C2","Partial"):"Proportionate",
        ("C2","Acknowledged"):"Under-response (gap)",("C2","None"):"Accountability gap (no action)"}
flag("Proportionality disagrees with the severity x action formula",
     [f'{r["Finding ID"]}: {r["Severity (C1/C2) majority"]}+{r["Action Level"]} -> {r["Proportionality"]!r}'
      for r in A if r["Action Level"] and MATRIX.get((r["Severity (C1/C2) majority"], r["Action Level"])) != r["Proportionality"]])
flag("severity majority disagrees with its own three votes",
     [r["Finding ID"] for r in R
      if r["Severity (C1/C2) majority"] in ("C1","C2")
      and [r["Sonnet5 vote"],r["GPT-5.5 vote"],r["Gemini3.1 vote"]].count(r["Severity (C1/C2) majority"]) < 2])
flag("positive Policy Level with no government URL",
     [r["Finding ID"] for r in R if r["Policy Level"] in ("Binding policy action","Non-binding policy-related uptake")
      and "http" not in (r["Channel B Evidence"] or "").lower()])

# ---------- 7. WHITESPACE / ENCODING ----------------------------------------------------------
cols=[c.value for c in ds.sheet()[1] if c.value]
ws_bad=[f'{r["Finding ID"]} [{c}]' for r in R for c in cols
        if isinstance(r.get(c),str) and r[c]!=r[c].strip()]
flag("cell has leading/trailing whitespace", ws_bad)
ctrl=[f'{r["Finding ID"]} [{c}]' for r in R for c in cols
      if isinstance(r.get(c),str) and re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', r[c])]
flag("cell contains control characters", ctrl)

# ---------- report -----------------------------------------------------------------------------
print(f"AUDIT · {len(R)} rows · {len(cols)} columns · Tier A {len(A)} · {len(NEW)} from the sweep\n")
if not issues:
    print("CLEAN — no anomalies found.")
else:
    tot=sum(len(v[0]) for v in issues.values())
    print(f"{len(issues)} issue type(s), {tot} affected row(s):\n")
    for name,(rows,note) in issues.items():
        newn=sum(1 for x in rows if any(n in str(x) for n in NEW))
        print(f"  [{len(rows):>4}] {name}" + (f"   ({newn} from the sweep)" if newn else ""))
        for x in rows[:6]: print(f"          {x}")
        if len(rows)>6: print(f"          ... +{len(rows)-6} more")
