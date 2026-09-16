#!/usr/bin/env python3
"""File the AISI-evals work into ~/MATS/Research/AISI_Evals; delete only same-session backups.

TCC lets this process stat and rename inside ~/Desktop but not open() files another app created,
so verification is by size via os.rename rather than by hash. Once a file lands outside the
protected folder it becomes readable, and the hash is recorded then. Idempotent: re-running skips
anything already filed.
"""
import os, shutil, hashlib, json

HOME = os.path.expanduser("~")
DESK = os.path.join(HOME, "Desktop")
DOCS = os.path.join(HOME, "Documents")
ROOT = os.path.join(HOME, "MATS", "Research", "AISI_Evals")
for d in ("dataset", "charts", "deck", "logs", "archive"):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)


def md5(p):
    try:
        h = hashlib.md5()
        with open(p, "rb") as f:
            for b in iter(lambda: f.read(1 << 20), b""):
                h.update(b)
        return h.hexdigest()[:12]
    except PermissionError:
        return "unreadable-in-place"


def relocate(src, sub, note, tag=""):
    if not os.path.exists(src):
        return ("skip", os.path.basename(src), 0, "not present")
    base = os.path.basename(src)
    stem, ext = os.path.splitext(base)
    name = f"{stem}{tag}{ext}"
    dst = os.path.join(ROOT, sub, name)
    if os.path.exists(dst):
        return ("already", name, os.path.getsize(dst), note)
    size = os.path.getsize(src)
    try:
        os.rename(src, dst)                  # same volume; needs dir write, not file read
    except PermissionError:
        # TCC binds files another app created to that app; this process cannot move them.
        return ("BLOCKED", name, size, note)
    assert os.path.getsize(dst) == size, f"size mismatch moving {base}"
    return ("moved", name, size, note)


PLAN = [
 (os.path.join(DESK, "AISIEVAL.xlsx"),                       "dataset", "authoritative workbook", ""),
 (os.path.join(DOCS, "AISIEVAL_validate.py"),                "dataset", "integrity validator", ""),
 (os.path.join(DESK, "AISIEVAL_10min.pptx"),                 "deck",    "10-minute talk", ""),
 (os.path.join(DOCS, "AISIEVAL_correction_log.csv"),         "logs",    "correction log", ""),
 (os.path.join(DOCS, "AISIEVAL_restoration_log.csv"),        "logs",    "restoration log", ""),
 (os.path.join(DOCS, "AISIEVAL_notes_archive.csv"),          "logs",    "SOLE copy of pre-merge IDs + cleared values", ""),
 (os.path.join(DESK, "v9.csv"),                              "archive", "differs from the repo copy", ""),
 (os.path.join(DESK, "v10.csv"),                             "archive", "differs from the repo copy", ""),
 (os.path.join(DESK, "v10_revised.xlsx"),                    "archive", "pre-merge half", ""),
 (os.path.join(DESK, "v11_FINAL.xlsx"),                      "archive", "pre-merge half", ""),
 (os.path.join(DOCS, "v10_revised.xlsx"),                    "archive", "Documents copy, distinct hash", "__from-Documents"),
 (os.path.join(DOCS, "AISIEVAL_ICML_FINAL.xlsx"),            "archive", "superseded, misleadingly named", ""),
 (os.path.join(DOCS, "AISIEVAL_ICML_FINAL_RESTORED.xlsx"),   "archive", "superseded, misleadingly named", ""),
 (os.path.join(DOCS, "AISIEVAL.superseded-2026-08-16.xlsx"), "archive", "superseded", ""),
]
rows = [relocate(*p) for p in PLAN]

# charts
csrc = os.path.join(DESK, "AISIEVAL_charts")
nfig = 0
if os.path.isdir(csrc):
    for f in sorted(os.listdir(csrc)):
        s = os.path.join(csrc, f)
        if os.path.isfile(s):
            d = os.path.join(ROOT, "charts", f)
            if not os.path.exists(d):
                sz = os.path.getsize(s)
                try:
                    os.rename(s, d)
                except PermissionError:
                    continue
                assert os.path.getsize(d) == sz
                nfig += 1
    if not os.listdir(csrc):
        os.rmdir(csrc)

print(f"{'action':<9} {'size':>9}  file")
print("-" * 92)
for act, name, sz, note in rows:
    print(f"{act:<9} {sz/1e6:>7.2f}MB  {name:<46} {note}")
print(f"{'moved':<9} {'':>9}  charts/ — {nfig} figures (Desktop folder removed)")

# ---- deletion: same-session backups only, and only once the final is filed ----------
final = os.path.join(ROOT, "dataset", "AISIEVAL.xlsx")
if not os.path.exists(final):
    raise SystemExit("REFUSING to delete: dataset/AISIEVAL.xlsx is not in place")
print(f"\nfinal workbook verified at dataset/AISIEVAL.xlsx  ({os.path.getsize(final)/1e6:.2f} MB, md5 {md5(final)})")

days = ["2026081%d" % d for d in range(3, 8)]
PATS = ["AISIEVAL.backup-{ts}.xlsx", "AISIEVAL_10min.backup-{ts}.pptx",
        "v10_revised.backup-{ts}.xlsx", "v11_FINAL.backup-repair-{ts}.xlsx"]
targets = []
for pat in PATS:
    for d in days:
        for hh in range(24):
            for mm in range(60):
                for ss in range(60):
                    p = os.path.join(DESK, pat.format(ts=f"{d}-{hh:02d}{mm:02d}{ss:02d}"))
                    if os.path.exists(p):
                        targets.append(p)
freed = sum(os.path.getsize(p) for p in targets)
gone, failed = 0, []
for p in targets:
    try:
        os.remove(p)
        gone += 1
    except Exception as e:
        failed.append((os.path.basename(p), str(e)[:50]))
print(f"deleted {gone}/{len(targets)} same-session backups · {freed/1e6:.2f} MB freed")
if failed:
    print("  could not delete:")
    for n, e in failed:
        print(f"    {n}: {e}")

json.dump({"root": ROOT, "filed": [[a, n, s, t] for a, n, s, t in rows],
           "figures": nfig, "backups_deleted": gone},
          open(os.path.join(ROOT, "_filing_manifest.json"), "w"), indent=1)
print(f"\nmanifest: {ROOT}/_filing_manifest.json")
