#!/usr/bin/env python3
"""Resize every figure for the web and report the base64 budget.

The artifact CSP blocks external hosts, so each PNG must be inlined as a data URI. At 200 dpi
the originals are far larger than any browser needs; downscaling to a sane web width keeps the
page well inside the 16 MB limit.
"""
import os, io, base64, json
from PIL import Image

SRC = os.path.expanduser("~/Desktop/AISIEVAL_charts")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_figs")
os.makedirs(OUT, exist_ok=True)
TARGET_W = 1500          # plenty for a 1280px-max content column on a retina screen

rows = []
tot_src = tot_web = 0
for f in sorted(os.listdir(SRC)):
    if not f.endswith(".png"):
        continue
    p = os.path.join(SRC, f)
    src_b = os.path.getsize(p)
    im = Image.open(p).convert("RGB")
    w, h = im.size
    if w > TARGET_W:
        im = im.resize((TARGET_W, round(h * TARGET_W / w)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    data = buf.getvalue()
    # PNG of a chart is usually smaller than JPEG at equal quality; check anyway
    jbuf = io.BytesIO()
    im.save(jbuf, "JPEG", quality=88, optimize=True, progressive=True)
    if len(jbuf.getvalue()) < len(data) * 0.75:
        data, ext = jbuf.getvalue(), "jpg"
    else:
        ext = "png"
    open(os.path.join(OUT, f.rsplit(".", 1)[0] + "." + ext), "wb").write(data)
    tot_src += src_b
    tot_web += len(data)
    rows.append((f, w, h, src_b, len(data), ext))

print(f"{'figure':<44} {'src px':>11} {'src KB':>8} {'web KB':>8}  fmt")
print("-" * 88)
for f, w, h, s, n, e in rows:
    print(f"{f:<44} {w}x{h:<6} {s/1024:>8.0f} {n/1024:>8.0f}  {e}")
b64 = tot_web * 4 / 3
print("-" * 88)
print(f"{len(rows)} figures · source {tot_src/1e6:.2f} MB → web {tot_web/1e6:.2f} MB "
      f"→ base64 ≈ {b64/1e6:.2f} MB")
print(f"artifact limit 16 MB · headroom {(16e6 - b64)/1e6:.1f} MB")
json.dump({f: e for f, _, _, _, _, e in rows}, open(os.path.join(OUT, "_fmt.json"), "w"))
