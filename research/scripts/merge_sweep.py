#!/usr/bin/env python3
"""Merge the gap-closure sweep into V13, following the v10 rulebook.

Three rules do the work here:
  * reports already in V13 INHERIT their canonical Institution / Type / Scope from the existing
    rows. The sweep agents wrote prose in those fields and in several cases put the *evaluated
    company* where the evaluator belongs, so their metadata is not trusted where V13 already
    knows the answer.
  * tier is DERIVED from Eval? + Action Trackable?, never read from the agent's "tier" label.
  * anything failing the S1 scope test or the S2 finding test is QUARANTINED with a reason, not
    silently dropped and not silently merged.
"""
import sys, os, json, re, collections, datetime, shutil, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds
import openpyxl

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
STAGED = os.path.join(ROOT, "logs/window_extension/merge/staged.json")

def urlkey(u):
    u = (u or '').lower().strip()
    u = re.sub(r'^https?://(www\.)?', '', u).rstrip('/')
    u = re.sub(r'[?#].*$', '', u)
    u = re.sub(r'arxiv\.org/(abs|pdf)/', 'arxiv.org/', u)
    return re.sub(r'v\d+$', '', u)

# ---- canonical institutions. Type/Scope taken from what V13 already uses for that name. -------
INST = {
    r'weval|collective intelligence':      ("Collective Intelligence Project (Weval)", "Non-Profit (AIEF)", "third-party-evaluator", "CIP"),
    r'shanghai':                           ("Shanghai AI Laboratory (AI45 Lab)", "Non-Profit (Independent)", "third-party-evaluator", "SHANGHAIAILAB"),
    r'^scale ai':                          ("Scale AI", "For-Profit", "third-party-evaluator", "SCALEAI"),
    r'securebio':                          ("SecureBio", "Non-Profit (AIEF)", "third-party-evaluator", "SECUREBIO"),
    r'holistic ai':                        ("Holistic AI", "For-Profit", "third-party-evaluator", "HOLISTIC"),
    r'far\.ai':                            ("FAR.AI", "Non-Profit (Independent)", "third-party-evaluator", "FARAI"),
    r'international network':              ("International Network of AI Safety Institutes", "Government", "government-AISI", "NETWORK"),
    r'rand europe':                        ("RAND Europe", "Non-Profit (AIEF)", "third-party-evaluator", "RANDEU"),
    r'rand corporation':                   ("RAND", "Non-Profit (AIEF)", "third-party-evaluator", "RAND"),
    r'crux|princeton':                     ("Princeton CRUX", "Non-Profit (AIEF)", "third-party-evaluator", "CRUX"),
    r'uk ai security institute|uk aisi':   ("UK AISI", "Government", "government-AISI", "UKAISI"),
    r'gray ?swan':                         ("Gray Swan AI", "For-Profit", "third-party-evaluator", "GRAYSWAN"),
    r'latticeflow':                        ("LatticeFlow AI", "For-Profit", "third-party-evaluator", "LATTICEFLOW"),
    r'ul research|dsri':                   ("UL Research Institutes (DSRI)", "For-Profit", "third-party-evaluator", "UL"),
    r'caisi|standards and innovation':     ("US CAISI", "Government", "government-AISI", "USCAISI"),
    r'^metr':                              ("METR", "Non-Profit (AIEF)", "third-party-evaluator", "METR"),
    r'palisade':                           ("Palisade Research", "Non-Profit (Independent)", "third-party-evaluator", "PALISADE"),
}
# S1 hard drop: a developer reporting on its own model with no external evaluator named.
SELF_REPORT = r'^(openai|anthropic|google deepmind|google|meta|alibaba|mistral ai|deepseek|xai|zhipu|microsoft)\b'
UNI_ONLY    = r'^(bocconi|tsinghua)'

def canon(inst):
    for pat, v in INST.items():
        if re.search(pat, inst or '', re.I):
            return v
    return None

DOMAIN = [
    (r'jailbreak|misuse resist|refusal|adversarial|red.?team|prompt.?inject|guardrail', 'Jailbreaks'),
    (r'cyber|security|vulnerab|exploit|malware|penetration',                            'Cyber'),
    (r'bio|chem|weapon|pathogen|drug|clinical|medical|health',                          'Bio-Chem'),
    (r'agent|autonom|r&d|self-improv|software engineer|coding|browser|tool.?use',       'Autonomy'),
    (r'persuas|influence|manipulat|deception|sycophan',                                 'Human Influence'),
    (r'bias|fairness|discriminat|toxic|societ|privacy|equity|education|economic',       'Societal'),
    (r'methodolog|benchmark|eval|measurement|reproduc',                                 'Eval-methodology'),
    (r'align|value|honest|truthful|personality|causal|reasoning|robust|capabilit',      'Alignment'),
    (r'governance|policy|process|assurance|standard|labelling',                         'Governance'),
]
def domain(s):
    for pat, v in DOMAIN:
        if re.search(pat, s or '', re.I): return v
    return 'Alignment'

def ftype(s, tier):
    s = (s or '').lower()
    mods = [m for m in ('company-published', 'anonymised-model', 'reassuring-null', 'non-frontier') if m in s]
    if 'governance' in s or 'process' in s: base = 'governance'
    elif 'methodolog' in s:                 base = 'methodology'
    elif 'trend' in s:                      base = 'capability-trend'
    else:                                   base = 'capability-finding'
    if tier == 'C' and base == 'capability-finding': base = 'methodology'
    return ';'.join([base] + mods)

def access(s):
    s = (s or '').lower()
    if re.search(r'pre-?deploy|pre-?release|deep access|early access', s): return 'Pre-deployment'
    # A standing scorecard, leaderboard or model card describes the report's FORMAT, not how the
    # evaluator reached the model. That is why `Aggregate` was retired on 2026-08-31 and all 85
    # rows recoded; this rule was still minting the value it had been retired for.
    if re.search(r'aggregate|leaderboard|model card', s):                  return 'Post-deployment'
    if re.search(r'mix', s):                                               return 'Mixed'
    if re.search(r'api|open weight|public product|deployed|web page|black.?box', s): return 'Post-deployment'
    return 'N/A'

DCODE = {'Jailbreaks': 'JAI', 'Cyber': 'CYB', 'Bio-Chem': 'BIO', 'Alignment': 'ALI', 'Autonomy': 'AUT',
         'Societal': 'SOC', 'Human Influence': 'HUM', 'Governance': 'GOV', 'Eval-methodology': 'GOV'}

# ---- load -------------------------------------------------------------------------------------
staged = json.load(open(STAGED))
R = list(ds.rows())
by_url = collections.defaultdict(list)
for r in R: by_url[urlkey(r["Source URL"])].append(r)
existing_ids = {r["Finding ID"] for r in R}

merged, quarantine = [], []
for it in staged:
    u = urlkey(it.get("url", ""))
    prior = by_url.get(u, [])
    for fd in it["findings"]:
        inst_raw = fd.get("institution", "") or it.get("venue", "")
        e = str(fd.get("eval_trackable", "")).strip().lower()
        a = str(fd.get("action_trackable", "")).strip().lower()
        tier = "A" if e == "yes" and a == "yes" else "B" if e == "yes" else "C"

        # A row with no resolvable publication date cannot get a compliant S6.1 ID and fails the
        # validator's ISO-date check. Park it rather than invent a date.
        if not prior and not (it.get("resolved_date") or "").strip():
            quarantine.append((it, fd, tier, "undatable: no resolvable publication date")); continue

        if prior:                                   # inherit — V13 already knows this report
            p = prior[0]
            inst, itype, scope = p["Institution"], p["Institution Type"], p["Scope"]
            prefix = re.match(r'[A-Z\-]+', p["Finding ID"]).group(0).rstrip('-')
            src = "inherited from V13"
            # S6.2: all rows sharing a Report ID must share Report Title, Source URL AND
            # Publication Date. These findings belong to a report V13 already holds, so they take
            # its Report ID and its canonical title/date/URL — minting a fresh Report ID here
            # would file one report under two IDs with two different titles.
            inherit_report = (p["Report ID"], p["Report Title"], p["Publication Date"], p["Source URL"])
        else:
            c = canon(inst_raw)
            # The sweep agents repeatedly wrote the EVALUATED COMPANY into `institution` (the
            # Mousetrap / Gemini-1.5-Flash class of error). Where the field names a developer but
            # the item's venue names a registered evaluator, the venue is the evaluator.
            if (not c or re.search(SELF_REPORT, inst_raw.strip(), re.I)) and canon(it.get("venue", "")):
                c = canon(it.get("venue", ""))
                fd["_inst_corrected"] = f'{inst_raw[:40]} -> venue {c[0]}'
            if re.search(SELF_REPORT, inst_raw.strip(), re.I) and not c:
                quarantine.append((it, fd, tier, "S1 hard drop: company self-report, no external evaluator named")); continue
            if re.search(UNI_ONLY, inst_raw.strip(), re.I) and not c:
                quarantine.append((it, fd, tier, "university-only author, no registered evaluator")); continue
            if not c:
                quarantine.append((it, fd, tier, f"unmapped institution: {inst_raw[:60]}")); continue
            inst, itype, scope, prefix = c
            src = "mapped"
            inherit_report = None

        dom = domain((fd.get("domain") or '') + ' ' + (fd.get("finding") or ''))
        merged.append({
            "it": it, "fd": fd, "tier": tier, "Institution": inst, "Institution Type": itype,
            "Scope": scope, "prefix": prefix, "Domain": dom, "src": src,
            "inherit_report": inherit_report,
            "Access Type": access((fd.get("access_type") or '') + ' ' + (it.get("venue") or '')),
            "Finding Type": ftype(fd.get("finding_type"), tier),
        })

# ---- IDs --------------------------------------------------------------------------------------
seq = collections.Counter()
report_owner = {r["Report ID"]: (r["Source URL"] or "").strip() for r in R}
for m in merged:
    d = (m["it"].get("resolved_date") or "")[:7].replace("-", "-") or "0000-00"
    code = DCODE[m["Domain"]]
    base = f'{m["prefix"]}-{d}-{code}'
    n = 1
    while f"{base}{n}" in existing_ids: n += 1
    seq[base] += 1
    while f"{base}{seq[base]}" in existing_ids: seq[base] += 1
    m["Finding ID"] = f"{base}{seq[base]}"
    existing_ids.add(m["Finding ID"])
    if m["inherit_report"]:
        rid, rtitle, rdate, rurl = m["inherit_report"]
        m["Report ID"] = rid
        m["title"], m["date"], m["url"] = rtitle, rdate, rurl
    else:
        want = f'{m["prefix"]}-{d}'
        key = (m["it"].get("url") or "").strip()
        if want in report_owner and report_owner[want] != key:
            for suf in "bcdefghij":
                if f"{want}{suf}" not in report_owner or report_owner[f"{want}{suf}"] == key:
                    want = f"{want}{suf}"; break
        report_owner[want] = key
        m["Report ID"] = want

t = collections.Counter(m["tier"] for m in merged)
print(f"MERGE-READY {len(merged)}   Tier A {t['A']} · B {t['B']} · C {t['C']}")
print(f"QUARANTINED {len(quarantine)}")
for reason, g in itertools.groupby(sorted(quarantine, key=lambda x: x[3]), key=lambda x: x[3]):
    g = list(g); print(f"   {len(g):>3}  {reason}")
json.dump([{k: v for k, v in m.items() if k not in ("it", "fd")} |
           {"finding": m["fd"].get("finding"), "url": m.get("url") or m["it"].get("url"),
            "title": m.get("title") or m["it"].get("title"), "date": m.get("date") or m["it"].get("resolved_date"),
            "quote": m["fd"].get("finding_quote"), "models": m["fd"].get("models_systems"),
            "eval": str(m["fd"].get("eval_trackable", "")).lower(),
            "action": str(m["fd"].get("action_trackable", "")).lower(),
            "reasoning": m["fd"].get("tier_reasoning")}
          for m in merged], open(os.path.join(ROOT, "logs/window_extension/merge/merge_ready.json"), "w"), indent=1)
json.dump([{"reason": r, "title": i.get("title"), "url": i.get("url"), "tier": tr,
            "institution": f.get("institution"), "finding": f.get("finding")}
           for i, f, tr, r in quarantine],
          open(os.path.join(ROOT, "logs/window_extension/merge/quarantine.json"), "w"), indent=1)
print("\nwrote merge_ready.json + quarantine.json")
