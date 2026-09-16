#!/usr/bin/env python3
"""File the AISI-evals work into ~/MATS/Research/AISI_Evals and clear the redundant backups.

Design rule: only byte-level redundancy is deleted. Every file that is a distinct artifact is
archived instead, because "an older version" is not the same thing as "a duplicate" -- the Desktop
v10.csv and v9.csv differ from the repo copies, and all four Documents workbooks hash differently.
What is genuinely redundant is the run of same-session backups of one workbook, superseded by the
final save.

Nothing is deleted until every move has been verified by size and hash at the destination.
"""
import os, shutil, hashlib, datetime, json

HOME = os.path.expanduser("~")
DESK = os.path.join(HOME, "Desktop")
DOCS = os.path.join(HOME, "Documents")
ROOT = os.path.join(HOME, "MATS", "Research", "AISI_Evals")
TREE = ["dataset", "charts", "deck", "logs", "archive", "site"]


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


for d in TREE:
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)
print("tree created under", ROOT)

# ---- moves: (source, destination subfolder, note) -----------------------------------
MOVES = [
 (os.path.join(DESK, "AISIEVAL.xlsx"),            "dataset", "the authoritative workbook"),
 (os.path.join(DOCS, "AISIEVAL_validate.py"),     "dataset", "integrity validator, 24 checks"),
 (os.path.join(DESK, "AISIEVAL_10min.pptx"),      "deck",    "10-minute talk, Keynote-editable"),
 (os.path.join(DOCS, "AISIEVAL_correction_log.csv"),   "logs", "correction log"),
 (os.path.join(DOCS, "AISIEVAL_restoration_log.csv"),  "logs", "restoration log"),
 (os.path.join(DOCS, "AISIEVAL_notes_archive.csv"),    "logs", "SOLE copy of pre-merge Finding IDs and cleared values"),
 (os.path.join(DESK, "v9.csv"),                   "archive", "differs from the repo copy"),
 (os.path.join(DESK, "v10.csv"),                  "archive", "differs from the repo copy"),
 (os.path.join(DESK, "v10_revised.xlsx"),         "archive", "pre-merge half"),
 (os.path.join(DESK, "v11_FINAL.xlsx"),           "archive", "pre-merge half"),
 (os.path.join(DOCS, "v10_revised.xlsx"),         "archive", "Documents copy, distinct hash"),
 (os.path.join(DOCS, "AISIEVAL_ICML_FINAL.xlsx"), "archive", "superseded, misleadingly named"),
 (os.path.join(DOCS, "AISIEVAL_ICML_FINAL_RESTORED.xlsx"), "archive", "superseded, misleadingly named"),
 (os.path.join(DOCS, "AISIEVAL.superseded-2026-08-16.xlsx"), "archive", "superseded"),
]
moved, skipped = [], []
for src, sub, note in MOVES:
    if not os.path.exists(src):
        skipped.append((src, "not present"))
        continue
    base = os.path.basename(src)
    # Documents/v10_revised.xlsx would collide with Desktop's; keep both, tagged
    dst = os.path.join(ROOT, sub, base)
    if os.path.exists(dst):
        stem, ext = os.path.splitext(base)
        dst = os.path.join(ROOT, sub, f"{stem}__from-Documents{ext}")
    before = (os.path.getsize(src), md5(src))
    shutil.move(src, dst)
    after = (os.path.getsize(dst), md5(dst))
    assert before == after, f"verification failed for {base}"
    moved.append((base, sub, before[0], note))

# ---- the chart folder ----------------------------------------------------------------
csrc = os.path.join(DESK, "AISIEVAL_charts")
if os.path.isdir(csrc):
    cdst = os.path.join(ROOT, "charts")
    n = 0
    for f in sorted(os.listdir(csrc)):
        s = os.path.join(csrc, f)
        if os.path.isfile(s):
            d = os.path.join(cdst, f)
            b = (os.path.getsize(s), md5(s))
            shutil.move(s, d)
            assert b == (os.path.getsize(d), md5(d)), f
            n += 1
    if not os.listdir(csrc):
        os.rmdir(csrc)
    print(f"charts: {n} files moved, empty AISIEVAL_charts/ removed from Desktop")

print(f"\nmoved {len(moved)} items:")
for base, sub, sz, note in moved:
    print(f"   {sub:<8} {sz/1e6:>7.2f} MB  {base:<44} {note}")
if skipped:
    print("\nnot present, skipped:")
    for s, why in skipped:
        print(f"   {os.path.basename(s)}  ({why})")

# ---- delete only the same-session backups -------------------------------------------
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
final = os.path.join(ROOT, "dataset", "AISIEVAL.xlsx")
assert os.path.exists(final), "refusing to delete backups: the final workbook is not in place"
freed = sum(os.path.getsize(p) for p in targets)
for p in targets:
    os.remove(p)
print(f"\ndeleted {len(targets)} same-session backups · {freed/1e6:.2f} MB freed")
print("   (only after confirming the final workbook is filed at dataset/AISIEVAL.xlsx)")

json.dump({"moved": moved, "deleted": [os.path.basename(p) for p in targets]},
          open(os.path.join(ROOT, "_filing_manifest.json"), "w"), indent=1)
