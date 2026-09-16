#!/usr/bin/env python3
"""Why won't Keynote open it? Check the package for the things Keynote is strict about."""
import os, zipfile, re
from lxml import etree

P = os.path.expanduser("~/Desktop/AISIEVAL_10min.pptx")
z = zipfile.ZipFile(P)
names = z.namelist()

print("=== parts ===")
for n in sorted(names):
    print("   ", n)

print("\n=== XML well-formedness ===")
bad = []
for n in names:
    if not n.endswith((".xml", ".rels")):
        continue
    try:
        etree.fromstring(z.read(n))
    except Exception as e:
        bad.append((n, str(e)[:90]))
print("   malformed:", bad or "none")

ct = z.read("[Content_Types].xml").decode()
print("\n=== [Content_Types].xml overrides ===")
for m in re.finditer(r'PartName="([^"]+)"\s+ContentType="[^"]*?([^./]+)\+xml"', ct):
    pass
declared = set(re.findall(r'PartName="([^"]+)"', ct))
print(f"   {len(declared)} explicit overrides")
missing_ct = [n for n in names
              if n.endswith(".xml") and not n.startswith("_rels") and "/_rels/" not in n
              and ("/" + n) not in declared]
print("   parts with NO content-type override:", missing_ct or "none")

print("\n=== notes plumbing (Keynote is strict here) ===")
has_nm = any("notesMaster" in n for n in names)
print("   notesMaster part present:", has_nm)
pres = z.read("ppt/presentation.xml").decode()
print("   presentation.xml declares notesMasterIdLst:", "notesMasterIdLst" in pres)
print("   notesSlide parts:", sorted(n for n in names if "notesSlides/notesSlide" in n and n.endswith(".xml")))
if not has_nm:
    print("   >>> LIKELY CAUSE: notes slides exist with no notesMaster to reference.")
    print("       PowerPoint tolerates this; Keynote rejects the file outright.")
# does any notesSlide reference a notesMaster relationship?
for n in sorted(names):
    if re.match(r'ppt/notesSlides/_rels/notesSlide1\.xml\.rels', n):
        print("\n   notesSlide1 rels:")
        for m in re.finditer(r'Type="[^"]*/(\w+)"\s+Target="([^"]+)"', z.read(n).decode()):
            print(f"      {m.group(1):<18} -> {m.group(2)}")

print("\n=== slide masters / layouts ===")
print("   masters :", [n for n in names if re.match(r'ppt/slideMasters/\w+\.xml$', n)])
print("   layouts :", len([n for n in names if re.match(r'ppt/slideLayouts/\w+\.xml$', n)]))
print("   theme   :", [n for n in names if n.startswith("ppt/theme/")])
