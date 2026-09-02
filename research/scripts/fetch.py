#!/usr/bin/env python3
"""One fetch ladder, used by every agent, so a blocked source is never mistaken for an absence.

The last re-verification pass recorded "congress.gov 403" against 172 findings and concluded the
US jurisdiction was unsearchable. It wasn't: congress.gov *search* pages 403, but its *documents*
return 200. Similarly openai.com 403s direct but is fully available through the Wayback Machine.
Both were treated as dead ends. This module removes that class of error by trying, in order:

    1. direct GET with complete browser headers on a keep-alive session
    2. PDF -> pypdf, falling back to pdfminer when extraction comes back thin
    3. HTML -> BeautifulSoup/lxml with chrome stripped
    4. on 403/429/5xx -> the nearest Wayback snapshot, fetched with the id_ flag so the
       archive toolbar is not injected into the text

Every attempt is recorded. A caller can always distinguish "fetched and the response is not there"
from "could not fetch", which is the distinction the whole dataset rests on.

    from fetch import get
    r = get(url)
    r["ok"], r["via"], r["status"], r["text"], r["attempts"]

CLI:  python3 fetch.py <url> [chars]
"""
import hashlib
import io
import json
import os
import re
import sys
import time
import warnings

warnings.filterwarnings("ignore")
import requests
from bs4 import BeautifulSoup

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
}
_S = requests.Session()
_S.headers.update(HEADERS)

TIMEOUT = 60
RETRY_STATUS = {403, 408, 429, 500, 502, 503, 504}

# ---- disk cache ---------------------------------------------------------------------------
# The Tier A universe is 9 companies, ~40 response documents and a handful of safety hubs, but
# the row count is 184 and every verifier re-checks what a searcher already read. Without a cache
# the same 186-page PDF is downloaded dozens of times. Extracted text is cached, not raw bytes,
# so the expensive part (PDF extraction) is paid once too.
CACHE = os.path.expanduser("~/MATS/Research/AISI_Evals/logs/fetch_cache")
TTL = 14 * 24 * 3600


def _key(url):
    return os.path.join(CACHE, hashlib.sha256(url.encode()).hexdigest()[:24] + ".json")


def _cache_read(url):
    p = _key(url)
    try:
        if os.path.exists(p) and (time.time() - os.path.getmtime(p)) < TTL:
            d = json.load(open(p, encoding="utf-8"))
            d["cached"] = True
            return d
    except Exception:
        pass
    return None


def _cache_write(rec):
    try:
        os.makedirs(CACHE, exist_ok=True)
        json.dump({k: rec[k] for k in ("url", "ok", "via", "status", "final_url", "text", "meta")},
                  open(_key(rec["url"]), "w", encoding="utf-8"))
    except Exception:
        pass


def _clean(html):
    s = BeautifulSoup(html, "lxml")
    for t in s(["script", "style", "nav", "footer", "noscript", "svg"]):
        t.decompose()
    return re.sub(r"[ \t\xa0]+", " ", re.sub(r"\n{3,}", "\n\n", s.get_text("\n"))).strip()


def _pdf(data):
    """pypdf first; pdfminer when pypdf yields suspiciously little for the page count."""
    text, pages = "", 0
    try:
        from pypdf import PdfReader
        rd = PdfReader(io.BytesIO(data))
        pages = len(rd.pages)
        text = "\n".join((p.extract_text() or "") for p in rd.pages)
    except Exception:
        pass
    if len(text) < max(400, pages * 40):
        try:
            from pdfminer.high_level import extract_text
            alt = extract_text(io.BytesIO(data)) or ""
            if len(alt) > len(text):
                text = alt
        except Exception:
            pass
    return text, pages


def _extract(resp):
    ct = (resp.headers.get("content-type") or "").lower()
    if "pdf" in ct or resp.content[:5] == b"%PDF-":
        t, pages = _pdf(resp.content)
        return t, {"kind": "pdf", "pages": pages}
    return _clean(resp.text), {"kind": "html", "pages": None}


def _wayback(url, attempts):
    """Nearest snapshot, raw original (id_) so the archive banner is not part of the text."""
    try:
        j = _S.get("https://archive.org/wayback/available",
                   params={"url": url}, timeout=30).json()
        snap = (j.get("archived_snapshots") or {}).get("closest") or {}
        if not snap.get("available"):
            attempts.append({"via": "wayback", "status": "no snapshot"})
            return None
        ts = snap["timestamp"]
        raw = f"https://web.archive.org/web/{ts}id_/{url}"
        for wait in (0, 4):
            if wait:
                time.sleep(wait)
            try:
                r = _S.get(raw, timeout=90)
                attempts.append({"via": "wayback", "status": r.status_code,
                                 "snapshot": ts, "url": raw})
                if r.status_code == 200:
                    return r
            except Exception as e:
                attempts.append({"via": "wayback", "status": f"{type(e).__name__}"})
    except Exception as e:
        attempts.append({"via": "wayback", "status": f"lookup {type(e).__name__}"})
    return None


def get(url, allow_wayback=True, refresh=False):
    if not refresh:
        hit = _cache_read(url)
        if hit is not None:
            hit.setdefault("attempts", [{"via": "cache", "status": 200}])
            hit.setdefault("error", None)
            return hit
    out = {"url": url, "ok": False, "via": None, "status": None, "final_url": None,
           "text": "", "meta": {}, "attempts": [], "error": None, "cached": False}
    resp = None
    try:
        resp = _S.get(url, timeout=TIMEOUT, allow_redirects=True)
        out["attempts"].append({"via": "direct", "status": resp.status_code})
        if resp.status_code == 200:
            out.update(ok=True, via="direct", status=200, final_url=resp.url)
    except Exception as e:
        out["attempts"].append({"via": "direct", "status": f"{type(e).__name__}"})
        out["error"] = f"{type(e).__name__}: {e}"[:200]

    if not out["ok"] and allow_wayback and (
            resp is None or resp.status_code in RETRY_STATUS):
        w = _wayback(url, out["attempts"])
        if w is not None:
            resp, _ = w, out.update(ok=True, via="wayback", status=200, final_url=w.url)

    if out["ok"] and resp is not None:
        try:
            out["text"], out["meta"] = _extract(resp)
        except Exception as e:
            out["ok"] = False
            out["error"] = f"extract {type(e).__name__}: {e}"[:200]
    elif not out["ok"]:
        out["status"] = resp.status_code if resp is not None else None
    if out["ok"]:
        _cache_write(out)
    return out


def find(url, *terms, window=260):
    """Fetch and return a snippet around each term. Empty hits list with ok=True means the
    document was read and the term genuinely is not in it — that is admissible negative evidence."""
    r = get(url)
    hits = []
    low = r["text"].lower()
    for t in terms:
        i = low.find(t.lower())
        if i >= 0:
            hits.append({"term": t, "snippet": r["text"][max(0, i - window // 2): i + window]})
    r["hits"] = hits
    r["text"] = ""          # callers want the snippets, not the whole document
    return r


if __name__ == "__main__":
    u = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    r = get(u)
    print(f"ok={r['ok']} via={r['via']} status={r['status']} kind={r['meta'].get('kind')} "
          f"pages={r['meta'].get('pages')} chars={len(r['text'])}")
    print("attempts:", r["attempts"])
    print("-" * 70)
    print(r["text"][:n])
