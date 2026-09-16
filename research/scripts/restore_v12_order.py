#!/usr/bin/env python3
"""Restore V12's original row order.

I re-sorted the whole sheet, which moved the 1,001 V12 rows. That order was the author's and was
not mine to change. This puts the V12 rows back in exactly the sequence they hold in the V12
source workbook, with the 167 sweep rows after them — the state before the sort.

Cell contents are untouched; only row position changes. Verified identical before saving.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds
import openpyxl

V12P = "/Users/kunalsingh/evaluating-the-evaluators/AISI  Eval Findings.xlsx"
src = openpyxl.load_workbook(V12P, data_only=True, read_only=True)["AISIEVAL_V12"]
srows = list(src.iter_rows(values_only=True))
shdr = [str(c).strip() if c is not None else "" for c in srows[0]]
si = shdr.index("Finding ID")
V12_ORDER = [str(r[si]).strip() for r in srows[1:] if r[si]]
RANK = {fid: i for i, fid in enumerate(V12_ORDER)}

wb = openpyxl.load_workbook(ds.WORKBOOK)
ws = wb[ds.SHEET]
hdr = [ds.norm(c.value) for c in ws[1]]
ncol = len(hdr)
i_id = hdr.index("Finding ID")

body = [[ws.cell(r, c).value for c in range(1, ncol + 1)]
        for r in range(2, ws.max_row + 1) if ws.cell(r, 1).value]
before = {ds.norm(row[i_id]): tuple(ds.norm(v) for v in row) for row in body}
assert len(before) == len(body)
assert all(f in before for f in V12_ORDER), "a V12 row is missing — refusing to reorder"

# V12 rows first, in their original sequence; then the sweep rows, newest first.
body.sort(key=lambda row: (
    0 if ds.norm(row[i_id]) in RANK else 1,
    RANK.get(ds.norm(row[i_id]), 0),
    "" if ds.norm(row[i_id]) in RANK
       else "".join(chr(255 - ord(ch)) for ch in ds.norm(row[hdr.index("Publication Date")])[:10]),
    ds.norm(row[i_id]),
))

after = {ds.norm(row[i_id]): tuple(ds.norm(v) for v in row) for row in body}
assert before == after, "cell contents changed — aborting"

for i, row in enumerate(body):
    for c, v in enumerate(row, start=1):
        ws.cell(i + 2, c).value = v
wb.save(ds.WORKBOOK)

check = [ds.norm(row[i_id]) for row in body[:len(V12_ORDER)]]
print(f"restored {len(body)} rows")
print(f"V12 order byte-identical to source: {check == V12_ORDER}")
