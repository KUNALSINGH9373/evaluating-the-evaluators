#!/usr/bin/env python3
"""Convert v10.csv into data.js consumed by the dashboard.

Run: python3 build_data.py
Reads v10.csv in this directory, writes data.js.
"""
import csv
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
# Dataset CSV, derived from AISIEVAL.xlsx. Pass a path to override; v11 is the current
# merged corpus and v10 is kept so older builds stay reproducible.
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    HERE / "v11.csv" if (HERE / "v11.csv").exists() else HERE / "v10.csv")
SWEEP = HERE / "sweep_state"
OUT = HERE / "data.js"


UK_AISI_ALIASES = {"UK AISI", "UK AI Security Institute (UK AISI)", "UK AI Security Institute"}
US_CAISI_ALIASES = {"US CAISI", "US Center for AI Standards and Innovation (CAISI), NIST", "NIST/US CAISI"}


def canon_institution(inst: str, scope: str) -> str:
    """Broad institution-group bucket for the site's charts/filters.

    Government-AISI and third-party-evaluator rows are kept structurally separate
    (per `Scope`) rather than collapsed into one "Other national AISI" catch-all —
    an evaluator like METR or SecureBio is not a national institute.
    """
    if not inst:
        return "Not recorded"
    if inst in UK_AISI_ALIASES:
        return "UK AISI"
    if inst in US_CAISI_ALIASES:
        return "US CAISI"
    if "+" in inst or "Joint" in inst or "Network" in inst or ";" in inst:
        return "Joint / multi-party"
    if scope == "third-party-evaluator":
        return "Third-party evaluator"
    return "Other national AISI"


def quarter(date: str):
    if not date or len(date) < 7:
        return None
    y, m = date[:4], int(date[5:7])
    return f"{y}-Q{(m - 1) // 3 + 1}"


def sweep_coverage():
    """Pull the discovery-sweep census numbers from sweep_state/, if present.

    These describe the search process (how many publications were found and
    screened for evaluation-relevance), not the final dataset — kept separate
    from `meta` findings-level stats and always reported with an honest
    in-progress caveat rather than a false precision.
    """
    ledger = SWEEP / "master_ledger.csv"
    if not ledger.exists():
        return None
    rows = list(csv.DictReader(ledger.open()))
    decisions = {}
    for r in rows:
        decisions[r["decision"]] = decisions.get(r["decision"], 0) + 1
    venues = set()
    enum_path = SWEEP / "cached_enumerations.json"
    if enum_path.exists():
        venues = set(json.loads(enum_path.read_text()).keys())
    return {
        "enumerated": sum(len(v) for v in json.loads(enum_path.read_text()).values()) if enum_path.exists() else None,
        "screened": len(rows),
        "venues": len(venues),
        "included": decisions.get("INCLUDED", 0),
        "pendingFetch": decisions.get("PENDING-FETCH", 0),
    }


def main():
    with SRC.open() as f:
        raw_rows = list(csv.DictReader(f))

    rows = [r for r in raw_rows if r["Finding ID"].strip()]
    dropped_blank = len(raw_rows) - len(rows)

    findings = []
    for r in rows:
        sev = r["Severity (C1/C2) majority"].strip() or None
        lag_raw = r["Lag (days)"].strip()
        try:
            lag = float(lag_raw)
            lag = int(lag) if lag == int(lag) else lag
        except ValueError:
            lag = None
        findings.append({
            "id": r["Finding ID"].strip(),
            "rid": r["Report ID"].strip(),
            "inst": r["Institution"].strip(),
            "instGroup": canon_institution(r["Institution"].strip(), r["Scope"].strip()),
            "instType": r["Institution Type"].strip(),
            "title": r["Report Title"].strip(),
            "date": r["Publication Date"].strip(),
            "q": quarter(r["Publication Date"].strip()),
            "dom": [d.strip() for d in r["Domain"].split(";") if d.strip()],
            "tags": [t.strip().lower() for t in r["Tags"].split(";") if t.strip()],
            "models": r["Models / Systems"].strip(),
            "access": r["Access Type"].strip(),
            "url": r["Source URL"].strip(),
            "finding": r["Finding"].strip(),
            "sev": sev,
            "sevProv": False,
            "action": r["Action Level"].strip(),
            "resp": r["Company Response"].strip(),
            "respDate": r["Response Date"].strip(),
            "lag": lag,
            "attr": r["Attribution"].strip(),
            "pol": r["Policy Level"].strip(),
            "prop": r["Proportionality"].strip(),
            "quote": "",
            "ftype": [t.strip() for t in r["Finding Type"].split(";") if t.strip()],
            "scope": r["Scope"].strip(),
            "track": r["Action Trackable?"].strip(),
            "evalT": r["Eval? (trackable)"].strip(),
        })

    track = [f for f in findings if f["track"] == "yes"]
    trackC1 = [f for f in track if f["sev"] == "C1"]
    lags = [f["lag"] for f in track if f["lag"] is not None]
    action_counts = {}
    for f in track:
        action_counts[f["action"]] = action_counts.get(f["action"], 0) + 1
    action_counts_c1 = {}
    for f in trackC1:
        action_counts_c1[f["action"]] = action_counts_c1.get(f["action"], 0) + 1

    meta = {
        "totalFindings": len(findings),
        "droppedBlankRows": dropped_blank,
        "reports": len({f["rid"] for f in findings if f["rid"]}),
        "trackable": len(track),
        "trackableC1": len(trackC1),
        "noResponse": action_counts.get("None", 0),
        "substantive": action_counts.get("Substantive", 0),
        "anyResponse": len(track) - action_counts.get("None", 0),
        "c1NoResponse": action_counts_c1.get("None", 0),
        "c1Substantive": action_counts_c1.get("Substantive", 0),
        "c1Gap": action_counts_c1.get("None", 0) + action_counts_c1.get("Partial", 0) + action_counts_c1.get("Acknowledged", 0),
        "empirical": sum(1 for f in findings if f["evalT"] == "yes"),
        "medianLag": statistics.median(lags) if lags else None,
        "lagN": len(lags),
        "dateMin": min(f["date"] for f in findings if f["date"]),
        "dateMax": max(f["date"] for f in findings if f["date"]),
        "sweep": sweep_coverage(),
    }

    payload = "window.AISI = " + json.dumps(
        {"meta": meta, "findings": findings}, ensure_ascii=False, separators=(",", ":")
    ) + ";\n"
    OUT.write_text(payload)
    print(f"wrote {OUT.name}: {len(findings)} findings, {meta['trackable']} trackable, "
          f"{len(payload) // 1024} KB")


if __name__ == "__main__":
    main()
