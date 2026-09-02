#!/usr/bin/env python3
"""AISIEVAL integrity validator. Exits non-zero on any violation.
   usage:  python3 AISIEVAL_validate.py [path-to-xlsx]"""
import sys, os, re, collections, datetime, openpyxl

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import dataset_source
# AISIEVAL_V12 is the single source of dataset truth; read in place, never rewritten.
PATH = sys.argv[1] if len(sys.argv) > 1 else dataset_source.WORKBOOK
GOV = ("parliament.uk","hansard","gov.uk","congress.gov","govinfo","federalregister","nist.gov",
       "nvlpubs.nist.gov","europa.eu","commerce.gov","ncsc.gov.uk","fca.org.uk","legislation.gov.uk",
       "whitehouse.gov","aisi.gov.uk","arcep.fr","bis.doc.gov",
       "bankofengland.co.uk","nvlpubs.nist.gov","assets.publishing.service.gov.uk")
VOCAB = {
 "Severity (C1/C2) majority": {"C1","C2"},
 "Action Level": {"None","Acknowledged","Partial","Substantive"},
 "Attribution": {"Explicit attribution","No explicit attribution","No response located"},
 "Policy Level": {"No policy uptake identified","Non-binding policy-related uptake","Binding policy action"},
 "Proportionality": {"Proportionate","Under-response (gap)","Accountability gap (no action)"},
 "Eval? (trackable)": {"yes","no"}, "Action Trackable?": {"yes","no",""},
 "Scope": {"government-AISI","third-party-evaluator"},
 "Access Type": {"Pre-deployment","Post-deployment","Mixed","Aggregate","N/A"},
}
MATRIX = {("C1","Substantive"):"Proportionate",("C1","Partial"):"Under-response (gap)",
 ("C1","Acknowledged"):"Under-response (gap)",("C1","None"):"Accountability gap (no action)",
 ("C2","Substantive"):"Proportionate",("C2","Partial"):"Proportionate",
 ("C2","Acknowledged"):"Under-response (gap)",("C2","None"):"Accountability gap (no action)"}
POSITIVE_PL = {"Binding policy action","Non-binding policy-related uptake"}

def norm(v):
    if v is None: return ""
    if isinstance(v,(datetime.datetime,datetime.date)): return v.strftime("%Y-%m-%d")
    return str(v).strip()

ws = openpyxl.load_workbook(PATH, data_only=True)[openpyxl.load_workbook(PATH).sheetnames[0]]
hdr = [norm(c.value) for c in ws[1]]
R = [{h: norm(ws.cell(r,i).value) for i,h in enumerate(hdr,1) if h} for r in range(2, ws.max_row+1)]
R = [r for r in R if r.get("Finding ID")]
tier = lambda r: ("A" if r.get("Action Trackable?")=="yes" else "B" if r.get("Eval? (trackable)")=="yes" else "C")
A = [r for r in R if tier(r)=="A"]
fail = collections.OrderedDict()
def check(name, rows):
    if rows: fail[name] = rows

# --- vocabulary & identity -------------------------------------------------
check("out-of-vocabulary value",
      [f"{r['Finding ID']} {c}={r[c]!r}" for r in R for c,ok in VOCAB.items() if r.get(c) and r[c] not in ok])
check("duplicate Finding ID",
      [k for k,v in collections.Counter(r["Finding ID"] for r in R).items() if v>1])
rf=re.compile(r"^[A-Z0-9]+-\d{4}-\d{2}[a-z]{0,2}(-[A-Za-z0-9]+)*$")
ff=re.compile(r"^[A-Z0-9]+-\d{4}-\d{2}[a-z]{0,2}(-[A-Za-z0-9]+)*-[A-Z]{2,4}\d+(-s\d+)?$")
check("Report ID off §6 format", sorted({r["Report ID"] for r in R if r.get("Report ID") and not rf.match(r["Report ID"])}))
check("Finding ID off §6 format", [r["Finding ID"] for r in R if not ff.match(r["Finding ID"])])
m=collections.defaultdict(set)
for r in R:
    if r.get("Report ID"): m[r["Report ID"]].add((r.get("Report Title",""), r.get("Publication Date","")))
check("Report ID with inconsistent title/date", [k for k,v in m.items() if len(v)>1])
check("publication date not ISO", [r["Finding ID"] for r in R if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r.get("Publication Date",""))])

# --- tier scoping ----------------------------------------------------------
check("invalid tier encoding",
      [r["Finding ID"] for r in R if (r.get("Eval? (trackable)"), r.get("Action Trackable?")) not in
       (("yes","yes"),("yes","no"),("no",""),("no","no"))])
check("Tier-A-only field on non-Tier-A row",
      [r["Finding ID"] for r in R if tier(r)!="A" and any(r.get(c) for c in
       ("Action Level","Attribution","Policy Level","Proportionality"))])
check("Tier A not fully classified",
      [r["Finding ID"] for r in A if not all(r.get(c) for c in
       ("Action Level","Attribution","Policy Level","Proportionality"))])

# --- derived fields --------------------------------------------------------
check("Proportionality != Severity x Action Level",
      [r["Finding ID"] for r in A if r.get("Action Level") and
       MATRIX.get((r.get("Severity (C1/C2) majority"), r["Action Level"])) != r.get("Proportionality")])
check("Attribution invariant (No response located <-> Action Level None)",
      [r["Finding ID"] for r in A if r.get("Action Level") and
       (r["Action Level"]=="None") != (r.get("Attribution")=="No response located")])
# D8 — acute individual harm. Deterministic override at the coding layer, so the frozen ensemble
# prompt stays comparable. A model actively urging a user toward suicide or self-harm is C1
# regardless of scale; D4 requires harm "at scale" and D6 requires a deployed safeguard to be
# bypassed, so the written taxonomy has no home for it. Registered rows are exempt from the
# vote-majority check and must carry the audit note.
# §4b ordinary accuracy/reliability: excluded from the dataset entirely, preserved in
# logs/AISIEVAL_excluded_ordinary_accuracy.csv. They must not reappear in the workbook.
SCOPE_EXCLUDED = {"CAIS-2026-07-ALI1","UKAISI-2026-03-CYB11","UKAISI-2025-07-HUM2",
                  "TRANSLUCE-2025-04-ALI1","HAL-2025-10-AUT3","HAL-2025-10-AUT3-s2",
                  "OPENAI-2025-07-SELF-ALI1"}
check("row excluded under §4b has reappeared in the workbook",
      [r["Finding ID"] for r in R if r["Finding ID"] in SCOPE_EXCLUDED])

D8_OVERRIDE = {"TRANSLUCE-2026-07-SOC2"}
# D5 deliberateness rule: a fabricated artefact alone does not show deliberate deception, and
# Critical Rule 2 requires the capability to be SHOWN. Rows here were lexical false positives
# where every classifier quoted a characterisation word rather than evidence of intent.
D5_DOWNGRADE = {"CAIS-2026-07-ALI1", "OPENAI-2025-07-SELF-ALI1"}
# Defective-input corrections: the Finding text omitted a severity-bearing fact that was present
# in the row's own Finding Quote, so the ensemble voted on an incomplete sentence. The Finding has
# been corrected, so a future re-run should agree; until then the stored votes disagree.
INPUT_FIX = {"SECUREBIO-2026-04-BIO5"}
check("Human severity label missing",
      [r["Finding ID"] for r in R if r.get("Human") not in ("C1", "C2")])
check("Human label disagrees with the recorded majority",
      [r["Finding ID"] for r in R if r.get("Human") != r.get("Severity (C1/C2) majority")])
check("severity != 3-vote majority (excluding registered D8 overrides)",
      [r["Finding ID"] for r in R if r["Finding ID"] not in (D8_OVERRIDE | D5_DOWNGRADE | INPUT_FIX)
       and r.get("Severity (C1/C2) majority") !=
       ("C1" if sum(1 for c in ("Sonnet5 vote","GPT-5.5 vote","Gemini3.1 vote") if r.get(c)=="C1")>=2 else "C2")])
# AISIEVAL_V12 carries no Notes column, so the in-row audit note can no longer be asserted; the
# registers below plus rulebook §7c are the audit trail. What is still checked is the outcome:
# every registered override must actually be coded the way the register says.
check("input-fix row not coded C1",
      [r["Finding ID"] for r in R if r["Finding ID"] in INPUT_FIX
       and r.get("Severity (C1/C2) majority") != "C1"])
check("D5 downgrade not actually coded C2",
      [r["Finding ID"] for r in R if r["Finding ID"] in D5_DOWNGRADE
       and r.get("Severity (C1/C2) majority") != "C2"])
check("D8 override not actually coded C1",
      [r["Finding ID"] for r in R if r["Finding ID"] in D8_OVERRIDE
       and r.get("Severity (C1/C2) majority") != "C1"])
# catch future cases: a model actively urging individual harm, still sitting at C2 and unregistered
_ACT = re.compile(r"\b(encourag|instruct|told|urg|advis|suggest|coach|provided)\w*\b", re.I)
_HARM = re.compile(r"suicid|self.?harm|kill (?:them|him|her)self|cut(?:ting)? (?:them|him|her)self", re.I)
check("possible unregistered D8 case (model urging individual harm, coded C2)",
      [r["Finding ID"] for r in R if r.get("Severity (C1/C2) majority") == "C2"
       and r["Finding ID"] not in D8_OVERRIDE
       and _ACT.search(r.get("Finding","")) and _HARM.search(r.get("Finding","") + " " + r.get("Finding Quote",""))])

# --- Channel A -------------------------------------------------------------
check("Action Level None but Channel A response fields filled",
      [r["Finding ID"] for r in A if r.get("Action Level")=="None" and
       (r.get("Company Response") or r.get("Channel A Verbatim") or r.get("Channel A Evidence"))])
check("response coded but no Channel A evidence",
      [r["Finding ID"] for r in A if r.get("Action Level") not in ("","None") and
       not (r.get("Company Response") or r.get("Channel A Evidence"))])
check("'None' without a dated Channel A search log",
      [r["Finding ID"] for r in A if r.get("Action Level")=="None" and not r.get("Sources Checked (channel A)")])
check("Response Date / Lag not paired",
      [r["Finding ID"] for r in R if bool(r.get("Response Date")) != bool(r.get("Lag (days)"))])
bad=[]
for r in R:
    if r.get("Response Date") and re.fullmatch(r"-?\d+", r.get("Lag (days)","")):
        try:
            d=(datetime.date.fromisoformat(r["Response Date"][:10])-datetime.date.fromisoformat(r["Publication Date"][:10])).days
            if d!=int(r["Lag (days)"]): bad.append(r["Finding ID"])
        except ValueError: bad.append(r["Finding ID"])
check("Lag != ResponseDate - PublicationDate", bad)
check("negative lag on a non-pre-deployment row",
      [r["Finding ID"] for r in R if r.get("Lag (days)","").startswith("-") and
       r.get("Access Type") not in ("Pre-deployment","Mixed")])

# --- Channel B (item 4: positive PL needs the full trio + a government source)
check("positive Policy Level without Policy Response + Verbatim + Evidence",
      [f"{r['Finding ID']} missing {[c for c in ('Policy Response','Channel B Verbatim','Channel B Evidence') if not r.get(c)]}"
       for r in R if r.get("Policy Level") in POSITIVE_PL and
       not all(r.get(c) for c in ("Policy Response","Channel B Verbatim","Channel B Evidence"))])
noGov=[]
for r in R:
    if r.get("Policy Level") not in POSITIVE_PL: continue
    ev=r.get("Channel B Evidence","").lower()
    # match government domains whether or not the citation carries an http prefix
    if not any(gd in ev for gd in GOV) and "evidence note" not in ev:
        noGov.append(r["Finding ID"])
check("positive Policy Level with no government-source URL and no documented exception", noGov)
check("'No policy uptake identified' without a search log",
      [r["Finding ID"] for r in A if r.get("Policy Level")=="No policy uptake identified" and not r.get("Channel B Evidence")])
check("Policy Level says no uptake but Policy Response asserts uptake",
      [r["Finding ID"] for r in R if r.get("Policy Level")=="No policy uptake identified"
       and r.get("Policy Response") and not r["Policy Response"].startswith("Not found")])

# --- report ----------------------------------------------------------------
H=[r for r in A if r.get("Severity (C1/C2) majority")=="C1"]
gap=sum(1 for r in H if r.get("Proportionality")=="Accountability gap (no action)")

print(f"AISIEVAL validator · {os.path.basename(PATH)}")
print(f"  {len(R)} records · Tier A {len(A)} · headline population {len(H)} · gap {gap}/{len(H)} = {gap/len(H):.1%}\n")
if not fail:
    print("  PASS — 0 violations across all checks"); sys.exit(0)
print(f"  FAIL — {len(fail)} check(s) with violations:")
for k,v in fail.items():
    print(f"    [{len(v)}] {k}")
    for x in v[:5]: print(f"          {x}")
    if len(v)>5: print(f"          ... +{len(v)-5} more")
sys.exit(1)
