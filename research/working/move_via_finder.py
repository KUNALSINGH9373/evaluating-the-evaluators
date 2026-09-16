#!/usr/bin/env python3
"""Clear every project file off ~/Desktop using Finder, which TCC permits.

This process can neither read nor rename Excel-created files in ~/Desktop, but Finder can, so the
moves are delegated to it via osascript. Redundant backups go to the Trash rather than being
unlinked, so a mistake stays recoverable.
"""
import os, subprocess, collections

HOME = os.path.expanduser("~")
DESK = os.path.join(HOME, "Desktop")
ROOT = os.path.join(HOME, "MATS", "Research", "AISI_Evals")

# destination subfolder -> files
PLAN = {
 "paper": ["evaluating-the-evaluators-paper.docx",
           "evaluating-the-evaluators-paper-v3.docx",
           "evaluating-the-evaluators-paper-v3.html",
           "evaluating-the-evaluators-findings-calculations.docx"],
 "rulebook": ["v10_RULEBOOK.md", "v11_RULEBOOK.md"],
 "scripts": ["run_severity_ensemble.py"],
 "logs": ["v11_applied_changes.csv", "v11_legend.csv", "v11_removed_rows.csv",
          "v11_revision_summary.csv", "v11_worklist.csv"],
 "archive": ["AISI  Eval Findings.xlsx", "v10_revised.xlsx",
             "v11_FINAL.pre-severity.xlsx", "v11_FINAL_pre_ICML_audit.xlsx",
             "v10_pre_batch2_backup.csv", "v10_RULEBOOK.md.stale-2026-08-01.bak",
             "v10_RULEBOOK.txt"],
 # earlier figure sets keep their own names so provenance survives
 "charts/previous": ["v10_charts", "AISI_paper_charts", "evaluating-the-evaluators-figures"],
}
# blind same-session snapshots of one workbook; the named milestones above are NOT here
TRASH = ["v11_FINAL-backup-20260816-011115.xlsx",
         "v11_FINAL-backup-20260816-011207.xlsx",
         "v11_FINAL-backup-20260816-011556.xlsx",
         "v11_FINAL.backup-20260815-133716.xlsx",
         "v11_FINAL.backup-20260815-133726.xlsx",
         "v11_FINAL.backup-20260815-154551.xlsx",
         "v11_FINAL.backup-20260815-171141.xlsx",
         "v11_FINAL.backup-20260815-192033.xlsx",
         "v11_FINAL.backup-20260815-192741.xlsx",
         "v11_FINAL.backup-20260815-193609.xlsx",
         "v11_FINAL.backup-20260815-194558.xlsx",
         "v11_FINAL.backup-20260815-221352.xlsx",
         "v11_FINAL.backup-newrules-20260816-011555.xlsx",
         "v11_FINAL.backup-policyfix-20260816-143144.xlsx",
         "v11_FINAL.backup-preFix-20260816-011207.xlsx"]


def finder(script):
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return r.returncode == 0, (r.stderr or r.stdout).strip()


# the current 26 figures move under charts/current so "current" stays unambiguous
cur = os.path.join(ROOT, "charts")
newcur = os.path.join(cur, "current")
if not os.path.isdir(newcur):
    os.makedirs(newcur)
    for f in sorted(os.listdir(cur)):
        p = os.path.join(cur, f)
        if os.path.isfile(p):
            os.rename(p, os.path.join(newcur, f))
    print(f"charts/: existing figures moved into charts/current ({len(os.listdir(newcur))} files)")

results = collections.Counter()
detail = []
for sub, files in PLAN.items():
    dst = os.path.join(ROOT, sub)
    os.makedirs(dst, exist_ok=True)
    for name in files:
        src = os.path.join(DESK, name)
        if not os.path.exists(src):
            results["absent"] += 1
            detail.append(("absent", sub, name, ""))
            continue
        if os.path.exists(os.path.join(dst, name)):
            results["already"] += 1
            detail.append(("already", sub, name, ""))
            continue
        ok, err = finder(f'tell application "Finder" to move (POSIX file "{src}") '
                         f'to (POSIX file "{dst}")')
        landed = os.path.exists(os.path.join(dst, name))
        results["moved" if landed else "FAILED"] += 1
        detail.append(("moved" if landed else "FAILED", sub, name, "" if landed else err[:60]))

for name in TRASH:
    src = os.path.join(DESK, name)
    if not os.path.exists(src):
        results["absent"] += 1
        continue
    ok, err = finder(f'tell application "Finder" to delete (POSIX file "{src}")')
    gone = not os.path.exists(src)
    results["trashed" if gone else "FAILED"] += 1
    if not gone:
        detail.append(("FAILED", "TRASH", name, err[:60]))

print(f"\n{'result':<9} {'destination':<17} file")
print("-" * 84)
for act, sub, name, err in detail:
    print(f"{act:<9} {sub:<17} {name}" + (f"   [{err}]" if err else ""))
print(f"\n{dict(results)}")
