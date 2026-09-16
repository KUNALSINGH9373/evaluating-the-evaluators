#!/usr/bin/env python3
"""Forward-in-time Channel A pass 2: search the company's later documents for the FINDING,
not for the evaluator's name.

Pass 1 matched evaluator names and returned 20 candidates, nearly all spurious -- "UK AISI"
appears in every OpenAI card because testing is ongoing. A response has to engage the
specific result, so this pass searches for each finding's distinctive terms: the benchmark
name, the attack name, the measured behaviour.
"""
import json, os, re, collections

D = os.path.dirname(os.path.abspath(__file__))
rows = {r["Finding ID"]: r for r in json.load(open(os.path.join(D, "sweep53.json")))}

DOCS = {
    "opus5.txt": "Anthropic", "mythos5.txt": "Anthropic", "sonnet5.txt": "Anthropic",
    "claude37_card.txt": "Anthropic", "c35_addendum.txt": "Anthropic", "opus4_card.txt": "Anthropic",
    "anthropic_nist_rfi.txt": "Anthropic", "anth_caisi.txt": "Anthropic", "redeploy_fable5.txt": "Anthropic",
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

# Distinctive terms per row: the thing a genuine response would have to name.
# accountable developer is stated explicitly here rather than inferred by regex.
PROBE = {
    "METR-2023-03-ALI1":        ("OpenAI",    [r'TaskRabbit', r'CAPTCHA']),
    "CAIS-2023-07-JAI2":        ("Google",    [r'adversarial suffix', r'GCG\b']),
    "SHANGHAIAILAB-2024-02-JAI1": ("OpenAI",  [r'Shanghai', r'psychological']),
    "CISCO-2024-08-JAI1":       ("OpenAI",    [r'Structured Output', r'response_format']),
    "UKAISI-2024-10-JAI1":      ("Mistral",   [r'AgentHarm']),
    "UKAISI-2024-10-JAI2":      ("Anthropic", [r'AgentHarm']),
    "UKAISI-2024-10-JAI3":      ("OpenAI",    [r'AgentHarm']),
    "UKAISI-2024-10-JAI5":      ("Google",    [r'AgentHarm']),
    "UKAISI-2024-10-JAI6":      ("OpenAI",    [r'AgentHarm']),
    "UKAISI-2024-10-JAI7":      ("OpenAI",    [r'AgentHarm']),
    "TRANSLUCE-2024-10-JAI1":   ("Meta",      [r'investigator agent', r'Transluce']),
    "PALISADE-2024-12-JAI1":    ("OpenAI",    [r'Palisade', r'BadLlama|fine.?tun\w+ attack']),
    "ROBUSTINT-2025-01-JAI1":   ("DeepSeek",  [r'Robust Intelligence', r'HarmBench']),
    "FARAI-2025-02a-JAI1":      ("DeepSeek",  [r'jailbreak.?tun', r'StrongREJECT']),
    "FARAI-2025-02a-JAI3":      ("Anthropic", [r'jailbreak.?tun', r'StrongREJECT']),
    "FARAI-2025-02a-JAI4":      ("Google",    [r'jailbreak.?tun', r'StrongREJECT']),
    "HOLISTIC-2025-02-JAI1":    ("DeepSeek",  [r'Holistic AI']),
    "SCALEAI-2025-02b-JAI1":    ("Anthropic", [r'\bJ2\b', r'jailbreak.?to.?jailbreak']),
    "SCALEAI-2025-02b-JAI2":    ("Google",    [r'\bJ2\b', r'jailbreak.?to.?jailbreak']),
    "UKAISI-2025-02-JAI1":      ("OpenAI",    [r'pointwise', r'finetuning API|fine.?tuning API']),
    "HOLISTIC-2025-02-JAI2":    ("xAI",       [r'Holistic AI']),
    "APOLLO-2025-03-ALI1":      ("Anthropic", [r'evaluation awareness', r'verbalis\w+ awareness']),
    "UKAISI-2025-04-ALI1":      ("Anthropic", [r'RepliBench', r'self.?replicat']),
    "UKAISI-2025-04-ALI7":      ("Anthropic", [r'RepliBench', r'self.?replicat']),
    "METR-2025-06-ALI1":        ("OpenAI",    [r'RE-Bench', r'reward hack']),
    "METR-2025-06-ALI2":        ("OpenAI",    [r'Optimize LLM Foundry', r'reward hack']),
    "METR-2025-06-ALI3":        ("OpenAI",    [r'reward hack']),
    "TRANSLUCE-2025-06-SOC1":   ("Alibaba",   [r'Transluce']),
    "SHANGHAIAILAB-2025-07-JAI1": ("OpenAI",  [r'Shanghai']),
    "SHANGHAIAILAB-2025-07-JAI2": ("Google",  [r'Shanghai']),
    "PALISADE-2025-07-ALI1":    ("OpenAI",    [r'shutdown resist|resist\w* shutdown', r'Palisade']),
    "UKAISI-2025-07-JAI3":      ("Anthropic", [r'STACK\b', r'component.?wise']),
    "UKAISI-2025-07-JAI4":      ("OpenAI",    [r'STACK\b', r'component.?wise']),
    "FARAI-2025-07b-BIO2":      ("Meta",      [r'FAR\.?AI', r'tamper.?resist']),
    "DREADNODE-2025-08-CYB1":   ("Anthropic", [r'Dreadnode', r'AIRTBench']),
    "DREADNODE-2025-08-CYB2":   ("Google",    [r'Dreadnode', r'AIRTBench']),
    "DREADNODE-2025-08-CYB3":   ("OpenAI",    [r'Dreadnode', r'AIRTBench']),
    "DREADNODE-2025-08-CYB4":   ("Moonshot",  [r'Dreadnode', r'AIRTBench']),
    "PALISADE-2025-08-CYB1":    ("OpenAI",    [r'Palisade']),
    "UKAISI-2025-08-JAI2":      ("OpenAI",    [r'tamper.?resist', r'fine.?tun\w+ defence|fine.?tun\w+ defense']),
    "TRANSLUCE-2025-09-JAI1":   ("Anthropic", [r'Transluce', r'investigator agent']),
    "TRANSLUCE-2025-09-JAI1-s2": ("Google",   [r'Transluce', r'investigator agent']),
    "TRANSLUCE-2025-09-JAI1-s3": ("xAI",      [r'Transluce', r'investigator agent']),
    "TRANSLUCE-2025-09-JAI1-s4": ("OpenAI",   [r'Transluce', r'investigator agent']),
    "PALISADE-2025-09-CYB1":    ("OpenAI",    [r'Palisade']),
    "USCAISI-2025-09-ALI1":     ("DeepSeek",  [r'CAISI']),
    "USCAISI-2025-09-JAI1":     ("DeepSeek",  [r'CAISI']),
    "REDWOOD-2025-10-ALI1":     ("Anthropic", [r'Redwood', r'evaluation awareness']),
    "UKAISI-2025-11-ALI1":      ("Anthropic", [r'sabotage', r'code backdoor']),
    "PALISADE-2025-11-CYB1":    ("OpenAI",    [r'Palisade']),
    "DREADNODE-2025-12-JAI1":   ("Meta",      [r'Dreadnode']),
    "DREADNODE-2025-12-JAI2":   ("Meta",      [r'Dreadnode']),
    "GRAYSWAN-2025-12-CYB1":    ("Anthropic", [r'Gray ?Swan', r'ARTEMIS']),
}
missing = set(rows) - set(PROBE)
if missing:
    print("!! rows with no probe defined:", missing)

strong, weak, nocache = [], [], []
for fid, (dev, pats) in sorted(PROBE.items(), key=lambda kv: rows[kv[0]]["Publication Date"]):
    r = rows[fid]
    docs = {f: t for f, (co, t) in text.items() if co == dev}
    if not docs:
        nocache.append((fid, dev))
        continue
    found = collections.defaultdict(list)
    for f, t in docs.items():
        for p in pats:
            for m in re.finditer(p, t, re.I):
                found[f].append((p, max(0, m.start() - 260), m.end() + 420))
                break
    if found:
        strong.append((fid, dev, found))
    else:
        weak.append((fid, dev))

print(f"\n=== PASS 2 over cached docs ===")
print(f"  finding-specific hit : {len(strong)}")
print(f"  no hit (None stands on the cached set) : {len(weak)}")
print(f"  no cached doc for developer : {len(nocache)}\n")

print("--- FINDING-SPECIFIC HITS — these need reading ---")
for fid, dev, found in strong:
    r = rows[fid]
    print(f"\n{'='*96}\n{fid}  ({dev}, pub {r['Publication Date']}, {r['Institution']})")
    print(f"  finding: {r['Finding'][:230]}")
    for f, spans in found.items():
        co, t = text[f]
        for p, a, b in spans[:1]:
            print(f"  [{f} · /{p}/] …{t[a:b]}…")

print(f"\n\n--- NO FINDING-SPECIFIC HIT ({len(weak)}): None stands over the cached documents ---")
for fid, dev in weak:
    print(f"  {rows[fid]['Publication Date']}  {fid:<28} {dev}")
print(f"\n--- NO CACHED DOC ({len(nocache)}): need open-web battery ---")
for fid, dev in nocache:
    print(f"  {rows[fid]['Publication Date']}  {fid:<28} {dev}")
