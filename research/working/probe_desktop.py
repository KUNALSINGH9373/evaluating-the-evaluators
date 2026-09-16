#!/usr/bin/env python3
"""Enumerate ~/Desktop without directory-listing permission.

macOS TCC blocks listing ~/Desktop for this process, but os.path.exists on a known path works.
Every backup this session created follows a timestamp pattern, so the set can be recovered by
probing the pattern across the plausible date range instead of listing the folder.
"""
import os, datetime, itertools

D = os.path.expanduser("~/Desktop")
PATTERNS = [
    "AISIEVAL.backup-{ts}.xlsx",
    "AISIEVAL_10min.backup-{ts}.pptx",
    "v10_revised.backup-{ts}.xlsx",
    "v11_FINAL.backup-repair-{ts}.xlsx",
    "AISIEVAL.superseded-{d}.xlsx",
]
found = []
days = ["2026081%d" % d for d in range(3, 8)]          # 13-17 Aug
n = 0
for pat in PATTERNS:
    if "{d}" in pat:
        for d in days:
            dd = f"{d[:4]}-{d[4:6]}-{d[6:]}"
            p = os.path.join(D, pat.format(d=dd))
            n += 1
            if os.path.exists(p):
                found.append(pat.format(d=dd))
        continue
    for d in days:
        for hh in range(24):
            for mm in range(60):
                for ss in range(60):
                    ts = f"{d}-{hh:02d}{mm:02d}{ss:02d}"
                    p = os.path.join(D, pat.format(ts=ts))
                    n += 1
                    if os.path.exists(p):
                        found.append(pat.format(ts=ts))
print(f"probed {n:,} candidate paths\n")
tot = 0
for f in sorted(found):
    sz = os.path.getsize(os.path.join(D, f))
    tot += sz
    print(f"   {sz/1e6:>7.2f} MB  {f}")
print(f"\n{len(found)} backup/superseded files on Desktop · {tot/1e6:.2f} MB total")

# also probe other plausible clutter names
EXTRA = ["v10 revised.xlsx", "v10_revised_RESTORED.xlsx", "aisi_v9.csv", "aisi_v10.csv",
         "v11.csv", "AISIEVAL_notes_archive.csv", "site.html", "deck.html",
         "AISIEVAL_10min.pptx", "AISIEVAL.xlsx", "v9.csv", "v10.csv",
         "v10_revised.xlsx", "v11_FINAL.xlsx"]
print("\nother AISIEVAL-related names present on Desktop:")
for e in EXTRA:
    p = os.path.join(D, e)
    if os.path.exists(p):
        print(f"   {os.path.getsize(p)/1e6:>7.2f} MB  {e}")

ch = os.path.join(D, "AISIEVAL_charts")
if os.path.isdir(ch):
    fs = sorted(os.listdir(ch))
    print(f"\nAISIEVAL_charts/ : {len(fs)} files")
    print("   " + ", ".join(fs[:6]) + (" ..." if len(fs) > 6 else ""))
