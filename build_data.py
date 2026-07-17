#!/usr/bin/env python3
"""Convert aisi_v6.csv into data.js consumed by the dashboard.

Run: python3 build_data.py
Reads aisi_v6.csv in this directory, writes data.js.
"""
import csv
import json
import statistics
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "aisi_v6.csv"
OUT = HERE / "data.js"

CONF_MAP = {"high": "High", "medium": "Medium", "med": "Medium", "low": "Low"}


def canon_institution(inst: str) -> str:
    if not inst:
        return "Not recorded"
    if inst == "UK AISI":
        return "UK AISI"
    if inst == "US CAISI":
        return "US CAISI"
    if "+" in inst or "Joint" in inst or "Network" in inst:
        return "Joint / multi-party"
    return "Other national AISI"


def norm_sev(raw: str):
    raw = raw.strip()
    if not raw:
        return None, False
    provisional = "PROVISIONAL" in raw
    return raw.split()[0].split("(")[0], provisional


def norm_prop(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("Proportionate: C2"):
        return "Proportionate (Cat2)"
    return raw


def quarter(date: str):
    if not date or len(date) < 7:
        return None
    y, m = date[:4], int(date[5:7])
    return f"{y}-Q{(m - 1) // 3 + 1}"


def main():
    with SRC.open() as f:
        raw_rows = list(csv.DictReader(f))

    rows = [r for r in raw_rows if r["Finding ID"].strip()]
    dropped_blank = len(raw_rows) - len(rows)

    findings = []
    for r in rows:
        sev, prov = norm_sev(r["Severity (C1/C2) majority"])
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
            "instGroup": canon_institution(r["Institution"].strip()),
            "title": r["Report Title"].strip(),
            "date": r["Publication Date"].strip(),
            "q": quarter(r["Publication Date"].strip()),
            "dom": [d.strip() for d in r["Domain"].split(";") if d.strip()],
            "models": r["Models / Systems"].strip(),
            "access": r["Access Type"].strip(),
            "url": r["Source URL"].strip(),
            "finding": r["Finding"].strip(),
            "sev": sev,
            "sevProv": prov,
            "action": r["Action Level"].strip(),
            "resp": r["Company Response"].strip(),
            "respDate": r["Response Date"].strip(),
            "lag": lag,
            "attr": r["Attribution"].strip(),
            "pol": r["Policy Level"].strip(),
            "prop": norm_prop(r["Proportionality"]),
            "conf": CONF_MAP.get(r["Confidence"].strip().lower(), r["Confidence"].strip()),
            "quote": r["Key Quote"].strip(),
            "ftype": [t.strip() for t in r["Finding Type"].split(";") if t.strip()],
            "scope": r["Scope"].strip(),
            "track": r["Action Trackable?"].strip(),
            "evalT": r["Eval? (trackable)"].strip(),
        })

    track = [f for f in findings if f["track"] == "yes"]
    lags = [f["lag"] for f in track if f["lag"] is not None]
    action_counts = {}
    for f in track:
        action_counts[f["action"]] = action_counts.get(f["action"], 0) + 1

    meta = {
        "totalFindings": len(findings),
        "droppedBlankRows": dropped_blank,
        "reports": len({f["rid"] for f in findings if f["rid"]}),
        "trackable": len(track),
        "trackableC1": sum(1 for f in track if f["sev"] == "C1"),
        "noResponse": action_counts.get("None", 0),
        "substantive": action_counts.get("Substantive", 0),
        "anyResponse": len(track) - action_counts.get("None", 0),
        "c1NoResponse": sum(1 for f in track if f["sev"] == "C1" and f["action"] == "None"),
        "empirical": sum(1 for f in findings if f["evalT"] == "yes"),
        "medianLag": statistics.median(lags) if lags else None,
        "lagN": len(lags),
        "dateMin": min(f["date"] for f in findings if f["date"]),
        "dateMax": max(f["date"] for f in findings if f["date"]),
    }

    payload = "window.AISI = " + json.dumps(
        {"meta": meta, "findings": findings}, ensure_ascii=False, separators=(",", ":")
    ) + ";\n"
    OUT.write_text(payload)
    print(f"wrote {OUT.name}: {len(findings)} findings, {meta['trackable']} trackable, "
          f"{len(payload) // 1024} KB")


if __name__ == "__main__":
    main()
