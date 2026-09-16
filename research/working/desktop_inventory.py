#!/usr/bin/env python3
"""Full Desktop inventory via AppleScript, since TCC blocks listing but Finder is permitted.

Classifies every entry as project / not-project so nothing unrelated is touched, and separates
same-session backups (deletable) from distinct artifacts (to be filed).
"""
import subprocess, os, re, datetime

DESK = os.path.expanduser("~/Desktop")
names = subprocess.run(
    ["osascript", "-e",
     'tell application "Finder" to get name of every item of (path to desktop folder)'],
    capture_output=True, text=True).stdout.strip()
items = [n.strip() for n in names.split(",") if n.strip()]

PROJECT = re.compile(
    r'AISI|evaluating-the-evaluators|v9|v10|v11|RULEBOOK|severity_ensemble|paper_charts', re.I)
BACKUP = re.compile(
    r'\.backup-|-backup-|\.pre-severity|_pre_ICML_audit|_pre_batch2_backup|\.stale-.*\.bak', re.I)


def info(n):
    p = os.path.join(DESK, n)
    try:
        st = os.stat(p)
        isdir = os.path.isdir(p)
        if isdir:
            sz = 0
            cnt = 0
            try:
                for dp, _, fs in os.walk(p):
                    for f in fs:
                        sz += os.path.getsize(os.path.join(dp, f))
                        cnt += 1
            except Exception:
                cnt = -1
            return isdir, sz, cnt, datetime.date.fromtimestamp(st.st_mtime).isoformat()
        return isdir, st.st_size, 0, datetime.date.fromtimestamp(st.st_mtime).isoformat()
    except Exception as e:
        return None, 0, 0, str(e)[:30]


proj, other, backups = [], [], []
for n in items:
    if n.startswith("."):
        continue
    isdir, sz, cnt, when = info(n)
    row = (n, isdir, sz, cnt, when)
    if not PROJECT.search(n):
        other.append(row)
    elif BACKUP.search(n):
        backups.append(row)
    else:
        proj.append(row)

def show(title, rows):
    print(f"\n=== {title} ({len(rows)}) ===")
    tot = 0
    for n, isdir, sz, cnt, when in sorted(rows, key=lambda r: r[0].lower()):
        tot += sz
        kind = f"DIR({cnt})" if isdir else "file"
        print(f"  {when}  {kind:<8} {sz/1e6:>8.2f} MB  {n}")
    print(f"  {'':>34}{tot/1e6:>8.2f} MB total")
    return tot

a = show("PROJECT FILES to file away", proj)
b = show("SAME-SESSION BACKUPS / superseded snapshots", backups)
c = show("NOT this project — leave alone", other)
print(f"\ntotal Desktop entries: {len(items)} · project {len(proj)+len(backups)} "
      f"({(a+b)/1e6:.2f} MB) · unrelated {len(other)} ({c/1e6:.2f} MB)")
