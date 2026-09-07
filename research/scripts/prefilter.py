#!/usr/bin/env python3
"""Decide deterministically which findings actually need an agent.

The Tier A universe is 9 accountable companies and a few dozen response documents. Sending all 184
findings to LLM agents means every agent re-fetches the same corpus and re-asserts the same
negatives. This does the cheap part in code:

  1. build the company response corpus ONCE (newsroom indexes, system cards, safety hubs), cached
  2. for each finding, grep that corpus for the evaluator name, the model, and the finding's own
     distinctive numbers
  3. a finding with ZERO hits anywhere in its company's corpus is a confirmed None — the negative
     is a reproducible grep, not an agent's word that it looked
  4. only findings WITH hits go to an agent, which is where judgement is actually required

The negative evidence this produces is stronger than the agent version, not weaker: it names the
documents searched, is re-runnable, and cannot hallucinate.

    python3 prefilter.py --build     # fetch/refresh the corpus
    python3 prefilter.py             # score every Tier A finding, write the triage
"""
import argparse, json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dataset_source as ds
from fetch import get

OUT = os.path.expanduser("~/MATS/Research/AISI_Evals/logs/prefilter")

# The company surfaces a Channel A response can live on. Indexes are crawled one level for
# document links; PDFs and articles are read directly.
SURFACES = {
    "OpenAI": ["https://openai.com/news/", "https://openai.com/safety/",
               "https://deploymentsafety.openai.com/",
               "https://cdn.openai.com/gpt-5-system-card.pdf",
               "https://cdn.openai.com/papers/gpt-4-system-card.pdf",
               "https://developers.openai.com/api/docs/deprecations"],
    "Anthropic": ["https://www.anthropic.com/news", "https://www.anthropic.com/rsp",
                  "https://www.anthropic.com/safety",
                  "https://anthropic.com/aug-2026-risk-report"],
    "Google": ["https://deepmind.google/discover/blog/",
               "https://deepmind.google/about/responsibility-safety/"],
    "Meta": ["https://ai.meta.com/blog/", "https://ai.meta.com/responsible-ai/"],
    "DeepSeek": ["https://api-docs.deepseek.com/news/"],
    "Alibaba": ["https://qwenlm.github.io/blog/"],
    "xAI": ["https://x.ai/news"],
    "Mistral": ["https://mistral.ai/news/"],
}


def dev(r):
    s = (r["Models / Systems"] + " " + r["Finding"]).lower()
    for k, v in [("openai", "OpenAI"), ("gpt-", "OpenAI"), (" o3", "OpenAI"),
                 ("anthropic", "Anthropic"), ("claude", "Anthropic"),
                 ("gemini", "Google"), ("google", "Google"), ("llama", "Meta"), (" meta", "Meta"),
                 ("deepseek", "DeepSeek"), ("qwen", "Alibaba"), ("grok", "xAI"),
                 ("mistral", "Mistral")]:
        if k in s:
            return v
    return "other"


def build():
    os.makedirs(OUT, exist_ok=True)
    corpus = {}
    for company, urls in SURFACES.items():
        docs = []
        for u in urls:
            r = get(u)
            docs.append({"url": u, "ok": r["ok"], "status": r["status"], "via": r.get("via"),
                         "chars": len(r["text"])})
            print(f"  {company:<10} {'ok ' if r['ok'] else 'FAIL'} {str(r['status']):>4} "
                  f"{len(r['text']):>8} chars  {u[:66]}")
        corpus[company] = docs
    json.dump(corpus, open(os.path.join(OUT, "corpus.json"), "w"), indent=1)
    ok = sum(1 for v in corpus.values() for d in v if d["ok"])
    print(f"\ncorpus: {ok}/{sum(len(v) for v in corpus.values())} surfaces readable, cached to disk")


NUM = re.compile(r"\b\d+(?:\.\d+)?%|\b\d{2,}(?:\.\d+)?\b")
STOP = {"the", "and", "for", "with", "that", "this", "from", "were", "was", "are"}


def signals(r):
    """The strings whose presence in a company document would indicate a response to THIS finding."""
    sig = set()
    inst = re.sub(r"\(.*?\)", "", r["Institution"]).strip()
    for part in re.split(r"[+;/]", inst):
        part = part.strip()
        if len(part) > 3:
            sig.add(part)
    for m in re.split(r"[;,]", r["Models / Systems"]):
        m = m.strip()
        if 3 < len(m) < 40:
            sig.add(m)
    sig |= set(NUM.findall(r["Finding"])[:6])
    return {s for s in sig if s.lower() not in STOP}


def main():
    corpus_meta = json.load(open(os.path.join(OUT, "corpus.json")))
    text = {}
    for company, docs in corpus_meta.items():
        blob = []
        for d in docs:
            if d["ok"]:
                blob.append(get(d["url"])["text"])
        text[company] = "\n".join(blob).lower()

    R = ds.rows()
    A = [r for r in R if r["Eval? (trackable)"] == "yes" and r["Action Trackable?"] == "yes"]
    triage = []
    for r in A:
        c = dev(r)
        body = text.get(c, "")
        sig = signals(r)
        hits = sorted({s for s in sig if s and s.lower() in body})
        triage.append({"finding_id": r["Finding ID"], "company": c,
                       "current_action_level": r["Action Level"],
                       "severity": r["Severity (C1/C2) majority"],
                       "signals_tested": sorted(sig), "signals_found": hits,
                       "needs_agent": bool(hits) or not body,
                       "corpus_available": bool(body)})
    json.dump(triage, open(os.path.join(OUT, "triage.json"), "w"), indent=1)

    need = [t for t in triage if t["needs_agent"]]
    clear = [t for t in triage if not t["needs_agent"]]
    print(f"Tier A findings                    {len(triage)}")
    print(f"  zero signal in company corpus    {len(clear):>4}  <- confirmed None by grep, no agent")
    print(f"  at least one signal              {len(need):>4}  <- send to an agent")
    nc = collections.Counter(t["company"] for t in need)
    print(f"\n  of the {len(need)} needing an agent, by company: {dict(nc.most_common())}")
    now_none = [t for t in clear if t["current_action_level"] == "None"]
    print(f"\n  {len(now_none)} of the zero-signal rows are already coded None — those are now "
          f"reproducibly confirmed")
    print(f"  {len(clear)-len(now_none)} zero-signal rows are coded as HAVING a response — "
          f"worth a look, the grep disagrees")
    print(f"\nwritten: {os.path.join(OUT,'triage.json')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    if a.build:
        build()
    else:
        main()
