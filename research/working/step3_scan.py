#!/usr/bin/env python3
"""Forward-in-time Channel A pass 1: does any cached company document mention the evaluator?

Cheap first filter over the 53 pre-2026 C1 rows coded None. A hit is a CANDIDATE only --
it still has to be a response to *this* finding, dated after it, in the *named company's*
own document. A miss over the cached set is not a battery; it just means pass 2 must search
the open web for that row.
"""
import json, os, re, collections

D = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(D, "sweep53.json")))

# cached primary documents, mapped to the company that published them
DOCS = {
    "opus5.txt": "Anthropic", "mythos5.txt": "Anthropic", "sonnet5.txt": "Anthropic",
    "claude37_card.txt": "Anthropic", "c35_addendum.txt": "Anthropic", "opus4_card.txt": "Anthropic",
    "anthropic_nist_rfi.txt": "Anthropic", "anth_caisi.txt": "Anthropic",
    "redeploy_fable5.txt": "Anthropic",
    "gpt5_card.txt": "OpenAI", "gpt54t.txt": "OpenAI", "gpt56.txt": "OpenAI",
    "gpt-5-6-preview.txt": "OpenAI", "gpt-5-5_biological-and-chemical.txt": "OpenAI",
    "gpt-5-5_cybersecurity.txt": "OpenAI", "cga.txt": "OpenAI", "gpt5_bio.txt": "OpenAI",
    "caisi_aisi_update.txt": "OpenAI", "addendum.txt": "OpenAI", "codex.txt": "OpenAI",
}
text = {}
for f, co in DOCS.items():
    p = os.path.join(D, f)
    if os.path.exists(p):
        text[f] = (co, re.sub(r'\s+', ' ', open(p, encoding='utf-8', errors='ignore').read()))
print(f"cached documents loaded: {len(text)}  "
      f"({collections.Counter(c for c, _ in text.values())})\n")

# evaluator -> the search aliases that would appear in a company document
ALIAS = {
    "UK AISI": [r'UK AISI', r'UK AI S(?:ecurity|afety) Institute'],
    "US CAISI": [r'\bCAISI\b', r'Center for AI Standards'],
    "METR": [r'\bMETR\b'],
    "Apollo Research": [r'Apollo Research'],
    "Redwood Research": [r'Redwood'],
    "FAR.AI": [r'FAR\.?AI', r'\bFAR AI\b'],
    "Palisade Research": [r'Palisade'],
    "Transluce": [r'Transluce'],
    "Dreadnode": [r'Dreadnode'],
    "Gray Swan AI": [r'Gray ?Swan'],
    "Scale AI": [r'Scale AI', r'\bSEAL\b'],
    "Center for AI Safety (CAIS)": [r'Center for AI Safety', r'\bCAIS\b(?!I)'],
    "Cisco (Robust Intelligence / Foundation AI)": [r'Robust Intelligence', r'\bCisco\b'],
    "Holistic AI": [r'Holistic AI'],
    "Shanghai AI Laboratory (AI Lab)": [r'Shanghai AI Lab'],
}


def developer(r):
    s = r["Models / Systems"] + " " + r["Finding"]
    if re.search(r'gpt|\bo[134]\b|chatgpt|codex|operator|sora|text-embedding', s, re.I): return "OpenAI"
    if re.search(r'claude|opus|sonnet|haiku|fable|mythos', s, re.I): return "Anthropic"
    if re.search(r'gemini|gemma|palm|bard', s, re.I): return "Google"
    if re.search(r'llama|prompt.?guard|maverick', s, re.I): return "Meta"
    if re.search(r'grok', s, re.I): return "xAI"
    if re.search(r'deepseek', s, re.I): return "DeepSeek"
    if re.search(r'mistral|magistral', s, re.I): return "Mistral"
    if re.search(r'qwen', s, re.I): return "Alibaba"
    if re.search(r'kimi|moonshot', s, re.I): return "Moonshot"
    if re.search(r'\bGLM\b|zhipu', s, re.I): return "Zhipu"
    return "?"


hits, misses, nodoc = [], [], []
for r in rows:
    dev = developer(r)
    inst = r["Institution"]
    pats = None
    for k, v in ALIAS.items():
        if inst.startswith(k[:12]):
            pats = v
            break
    if pats is None:
        pats = [re.escape(inst.split("(")[0].strip())]
    cand = []
    have_doc = False
    for f, (co, t) in text.items():
        if co != dev:
            continue
        have_doc = True
        for p in pats:
            if re.search(p, t, re.I):
                cand.append(f)
                break
    if not have_doc:
        nodoc.append((r, dev))
    elif cand:
        hits.append((r, dev, sorted(set(cand))))
    else:
        misses.append((r, dev))

print(f"=== PASS 1: {len(hits)} candidate(s) · {len(misses)} clean miss over cached docs · "
      f"{len(nodoc)} no cached doc for that developer\n")
print("--- CANDIDATES (evaluator named in one of the developer's own later documents) ---")
for r, dev, cand in sorted(hits, key=lambda x: x[0]["Publication Date"]):
    print(f"\n{r['Publication Date']}  {r['Finding ID']:<28} {dev}")
    print(f"   evaluator: {r['Institution']}")
    print(f"   models   : {r['Models / Systems'][:70]}")
    print(f"   finding  : {r['Finding'][:200]}")
    print(f"   named in : {', '.join(cand)}")

print("\n\n--- CLEAN MISS over cached docs (needs pass 2 web search) ---")
for r, dev in sorted(misses, key=lambda x: x[0]["Publication Date"]):
    print(f"  {r['Publication Date']}  {r['Finding ID']:<28} {dev:<10} {r['Institution'][:34]}")

print("\n--- NO CACHED DOCUMENT for that developer (all need pass 2) ---")
for r, dev in sorted(nodoc, key=lambda x: x[0]["Publication Date"]):
    print(f"  {r['Publication Date']}  {r['Finding ID']:<28} {dev:<10} {r['Institution'][:34]}")
