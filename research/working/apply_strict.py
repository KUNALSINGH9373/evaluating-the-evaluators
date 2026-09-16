#!/usr/bin/env python3
"""Primary specification: apply col 17's 'directly addressed the identified problem' strictly.

The 11 rows below have a positive Action Level resting on a company action that is
general-purpose -- a company-wide method, a product-scope decision, or a commercial
deprecation -- that would read identically had the finding never been published, and that
the company never linked to the finding. Under col 17 that is not a response to THIS
finding, so Action Level becomes None.

This is reversible by design. Every cleared value is written to
AISIEVAL_sensitivity_general_response.csv (lossless) and restated in the row's Notes, so the
permissive figure stays reproducible for the paper's robustness check.

NOT affected, and deliberately so: rows where the action is specific to the finding even
though the company gave no credit (METR-2025-04-ALI1 is the type case -- Anthropic documents
the exact reward-hacking pattern and partial pre-launch mitigations while crediting its own
monitoring). Response specificity and attribution are separate axes; only specificity is
col 17's test.
"""
import openpyxl, os, shutil, time, csv, collections, datetime

P = os.path.expanduser("~/Desktop/AISIEVAL.xlsx")
CSV = os.path.expanduser("~/Documents/AISIEVAL_sensitivity_general_response.csv")
D = "2026-08-17"

WHY = {
 "CAIS-2023-07-JAI1":   "deliberative alignment is a general safety-training method applied to the o-series; it improves jailbreak robustness broadly and does not address GCG adversarial-suffix transfer in particular. OpenAI never cites CAIS.",
 "CAIS-2023-07-JAI3":   "Constitutional Classifiers was a prototype for possible future deployment, not a measure addressing the GCG transfer result, and Anthropic never links it to this finding.",
 "APOLLO-2023-11-ALI1": "barring stock trading is an Operator product-scope decision covering a class of regulated activity; it is not a measure addressing the insider-trading-and-concealment behaviour Apollo elicited in GPT-4, and OpenAI never links the two.",
 "SCALEAI-2024-10-JAI1":"Operator launched with generic agentic refusals and confirmation prompts; nothing ties them to BrowserART's specific result that browser agents pursue harmful behaviours their backbone models refuse in chat.",
 "SCALEAI-2025-02b-JAI3":"Safety Reasoner is a company-wide safeguard deployed across successor systems; it is not a measure addressing the J2 attacker result on GPT-4o, and OpenAI never references Scale AI or J2.",
 "CISCO-2024-07-JAI1":  "Prompt Guard 2 is the successor classifier in the same family, released with broadly improved detection; Meta does not present it as a fix for the specific single-character-embedding flaw Cisco identified, nor cite Cisco.",
 "CIP-2025-08-ALI1":    "the October 2025 mental-health update was built with 170+ clinicians and addresses the domain broadly; the addendum makes no reference to CIP or Weval and is not presented as a response to their worst-in-class crisis-response result.",
 "FARAI-2024-08-JAI1":  "the self-serve fine-tuning wind-down is a commercial deprecation whose own notice states a capability rationale -- newer models make much of fine-tuning unnecessary -- not a safety rationale, and does not reference this finding or FAR.AI.",
 "FARAI-2024-10-ALI1":  "same wind-down, same commercial rationale, no reference to the finding or FAR.AI.",
 "FARAI-2024-10-JAI1":  "same wind-down, same commercial rationale, no reference to the finding or FAR.AI.",
 "FARAI-2025-02a-JAI2": "same wind-down, same commercial rationale, no reference to the finding or FAR.AI.",
}
PRESERVE = ["Action Level", "Attribution", "Proportionality", "Company Response",
            "Response Date", "Lag (days)", "Channel A Evidence"]

shutil.copy2(P, P.replace(".xlsx", f".backup-{time.strftime('%Y%m%d-%H%M%S')}.xlsx"))
wb = openpyxl.load_workbook(P)
ws = wb[wb.sheetnames[0]]
hdr = [c.value for c in ws[1]]
ix = {h: i + 1 for i, h in enumerate(hdr) if h}


def norm(v):
    if v is None:
        return ""
    if isinstance(v, (datetime.datetime, datetime.date)):
        return v.strftime("%Y-%m-%d")
    return str(v).strip()


saved = []
for r in range(2, ws.max_row + 1):
    fid = ws.cell(r, 1).value
    if fid not in WHY:
        continue
    prior = {c: norm(ws.cell(r, ix[c]).value) for c in PRESERVE}
    saved.append({"Finding ID": fid, "Institution": norm(ws.cell(r, ix["Institution"]).value),
                  "Publication Date": norm(ws.cell(r, ix["Publication Date"]).value),
                  "Severity": norm(ws.cell(r, ix["Severity (C1/C2) majority"]).value), **prior})
    # primary spec: no response to THIS finding
    ws.cell(r, ix["Action Level"]).value = "None"
    ws.cell(r, ix["Attribution"]).value = "No response located"
    ws.cell(r, ix["Proportionality"]).value = "Accountability gap (no action)"
    for c in ("Company Response", "Response Date", "Lag (days)", "Channel A Evidence"):
        ws.cell(r, ix[c]).value = None
    note = (f"[SPECIFICITY RULE APPLIED {D} — PRIMARY SPECIFICATION] Action Level "
            f"{prior['Action Level']} -> None; Proportionality {prior['Proportionality']} -> Accountability gap "
            f"(no action); Attribution {prior['Attribution']} -> No response located. Col 17 requires a mitigation "
            f"that \"directly addressed the identified problem\" (Substantive) or \"addressed only part of the "
            f"identified problem\" (Partial). Here, {WHY[fid]} A general-purpose action that would read identically "
            "had this finding never been published does not satisfy that test, so no response to THIS finding is "
            "documented. This is a specificity judgement, NOT an attribution one: rows whose action is specific to "
            "the finding keep their positive coding even with no credit given (type case METR-2025-04-ALI1). "
            "REVERSIBLE — the prior coding is preserved verbatim here and in "
            "~/Documents/AISIEVAL_sensitivity_general_response.csv, and is reported in the paper as a robustness "
            f"check. PRIOR VALUES: Action Level={prior['Action Level']!r}; Attribution={prior['Attribution']!r}; "
            f"Proportionality={prior['Proportionality']!r}; Response Date={prior['Response Date']!r}; "
            f"Lag={prior['Lag (days)']!r}; Channel A Evidence={prior['Channel A Evidence']!r}; "
            f"Company Response={prior['Company Response']!r}")
    nt = ws.cell(r, ix["Notes"]).value or ""
    ws.cell(r, ix["Notes"]).value = (nt + "\n\n" + note).strip()
wb.save(P)

with open(CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["Finding ID", "Institution", "Publication Date", "Severity"] + PRESERVE)
    w.writeheader()
    w.writerows(saved)
print(f"reclassified {len(saved)} rows · sensitivity file: {CSV}")
for s in saved:
    print(f"  {s['Finding ID']:<26} {s['Action Level']:<12} -> None   (was {s['Proportionality']})")

ws2 = openpyxl.load_workbook(P, data_only=True)[wb.sheetnames[0]]
R = [{h: norm(ws2.cell(r, ix[h]).value) for h in ix} for r in range(2, ws2.max_row + 1) if ws2.cell(r, 1).value]
tier = lambda r: ("A" if r["Action Trackable?"] == "yes" else "B" if r["Eval? (trackable)"] == "yes" else "C")
A = [r for r in R if tier(r) == "A"]
H = [r for r in A if r["Severity (C1/C2) majority"] == "C1"]
c = collections.Counter(r["Proportionality"] for r in H)
gap, und, n = c["Accountability gap (no action)"], c["Under-response (gap)"], len(H)
print(f"\nPRIMARY SPEC  gap {gap}/{n} = {gap/n:.1%} · falls short {gap+und}/{n} = {(gap+und)/n:.1%}")
print(f"SENSITIVITY   gap {gap-11}/{n} = {(gap-11)/n:.1%} (admitting general-purpose unattributed actions)")
print("Action Level:", dict(collections.Counter(r["Action Level"] for r in A).most_common()))
print("Attribution :", dict(collections.Counter(r["Attribution"] for r in A).most_common()))
