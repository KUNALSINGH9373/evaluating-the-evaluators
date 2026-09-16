#!/usr/bin/env python3
"""Sort the whole sheet: Publication Date DESC, then Report ID, then Finding ID (natural order).

The 167 sweep rows were appended in a block at the end rather than interleaved. Sorting only those
would not fix the sheet — the V12 block itself had 3 date-order violations and 162 reports split
across non-contiguous blocks. So the sort is applied to every row, which makes each report a
single contiguous group and puts the whole corpus in one date order.

Row position carries no meaning (Finding ID is the key), and the script asserts that every row's
cell contents are preserved exactly before it saves.
"""
import sys, os, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds
import openpyxl

def natkey(s):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s or "")]

wb = openpyxl.load_workbook(ds.WORKBOOK)
ws = wb[ds.SHEET]
hdr = [ds.norm(c.value) for c in ws[1]]
ncol = len(hdr)

body = []
for r in range(2, ws.max_row + 1):
    if not ws.cell(r, 1).value: continue
    body.append([ws.cell(r, c).value for c in range(1, ncol + 1)])

i_id, i_rep, i_date = hdr.index("Finding ID"), hdr.index("Report ID"), hdr.index("Publication Date")
before = {ds.norm(row[i_id]): tuple(ds.norm(v) for v in row) for row in body}
assert len(before) == len(body), "duplicate Finding ID — refusing to sort"

# date DESC (blank dates last), then report, then finding id
body.sort(key=lambda row: (
    "0000-00-00" if not ds.norm(row[i_date]) else "",         # blanks to the end
    [-ord(ch) for ch in ds.norm(row[i_date])[:10]],            # descending date
    natkey(ds.norm(row[i_rep])),
    natkey(ds.norm(row[i_id])),
))

after = {ds.norm(row[i_id]): tuple(ds.norm(v) for v in row) for row in body}
assert before == after, "cell contents changed during sort — aborting"

for i, row in enumerate(body):
    for c, v in enumerate(row, start=1):
        ws.cell(i + 2, c).value = v
wb.save(ds.WORKBOOK)
print(f"sorted {len(body)} rows · contents verified identical")
