import csv, os

HEADER = "Finding ID,Report ID,Institution,Institution Type,Report Title ,Publication Date,Domain,Models / Systems,Access Type,Source URL,Finding,Finding Quote,Severity (C1/C2) majority,Sonnet5 vote,GPT-5.5 vote,Gemini3.1 vote,Attribution,Company Response,Channel A Verbatim,Response Date,Lag (days),Channel A Evidence,Action Level,Sources Checked (channel A),Policy Level,Policy Response,Channel B Verbatim,Channel B Evidence,Media Outlets,Academic Citations,Social Highlights,Channel C Verbatim,Proportionality,,Eval? (trackable),Action Trackable?,Finding Type,Tags,Scope,Notes".split(",")
assert len(HEADER) == 40, len(HEADER)

OUT = "/Users/kunalsingh/evaluating-the-evaluators/sweep_state/extract_jobs"
TODO = "TODO severity ensemble + Channel A/B/C."


def row(fid, rid, inst, itype, title, date, domain, models, access, url, finding, quote,
        evaltrack, actiontrack, ftype, tags, scope, notes=""):
    n = (notes + " " if notes else "") + TODO
    d = {h: "" for h in HEADER}
    d.update({
        "Finding ID": fid, "Report ID": rid, "Institution": inst, "Institution Type": itype,
        "Report Title ": title, "Publication Date": date, "Domain": domain,
        "Models / Systems": models, "Access Type": access, "Source URL": url,
        "Finding": finding, "Finding Quote": quote, "Eval? (trackable)": evaltrack,
        "Action Trackable?": actiontrack, "Finding Type": ftype, "Tags": tags,
        "Scope": scope, "Notes": n,
    })
    return d


def write(key, rows):
    key = key[:-4] if key.endswith(".csv") else key
    p = os.path.join(OUT, "out_%s.csv" % key)
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(p, len(rows))


def write_dups(key, dups):
    key = key[:-4] if key.endswith(".csv") else key
    p = os.path.join(OUT, "dup_%s.csv" % key)
    with open(p, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["candidate_title", "candidate_url", "matched_finding_id", "why_duplicate"])
        for d in dups:
            w.writerow(d)
    print(p, len(dups))
