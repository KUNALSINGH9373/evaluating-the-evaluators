#!/usr/bin/env python3
"""Read the nine candidate hits that are not obviously coincidental."""
import os, re

D = os.path.dirname(os.path.abspath(__file__))
T = {}
for f in ("gpt5_card.txt", "gpt56.txt", "opus4_card.txt", "opus5.txt", "mythos5.txt",
          "sonnet5.txt", "claude37_card.txt", "anth_caisi.txt", "caisi_aisi_update.txt",
          "cga.txt", "gpt5_bio.txt"):
    p = os.path.join(D, f)
    if os.path.exists(p):
        T[f] = re.sub(r'\s+', ' ', open(p, encoding='utf-8', errors='ignore').read())

Q = [
    ("METR-2025-06-ALI1/2/3 — o3 reward hacking on RE-Bench. Does the GPT-5 card mitigate REWARD HACKING "
     "(not just deception)?", "gpt5_card.txt",
     [r'propensity to deceive, cheat, or hack', r'reward hack\w*', r'cheat\w*']),
    ("UKAISI-2025-07-JAI4 — STACK attack on OpenAI's production GPT-5 safeguard pipeline", "gpt5_card.txt",
     [r'STACK\b', r'component.?wise']),
    ("UKAISI-2025-07-JAI3 — STACK attack on Anthropic's production Claude Opus 4 safeguard pipeline", "opus5.txt",
     [r'STACK\b', r'component.?wise']),
    ("UKAISI-2025-04-ALI1/ALI7 — RepliBench autonomous self-replication", "opus4_card.txt",
     [r'RepliBench', r'self.?replicat\w*']),
    ("APOLLO-2025-03-ALI1 — evaluation awareness in Claude Sonnet 3.7 (thinking)", "opus4_card.txt",
     [r'evaluation awareness', r'verbalis\w+ .{0,20}awareness']),
    ("FARAI-2025-02a-JAI3 — jailbreak-tuning of Claude 3 Haiku via the fine-tuning API", "opus5.txt",
     [r'jailbreak.?tun\w*', r'StrongREJECT']),
]
for label, f, pats in Q:
    print("=" * 100)
    print(label)
    print(f"  doc: {f}")
    t = T.get(f, "")
    if not t:
        print("  (document not cached)")
        continue
    for p in pats:
        ms = list(re.finditer(p, t, re.I))
        if not ms:
            print(f"  /{p}/ : NOT FOUND")
            continue
        print(f"  /{p}/ : {len(ms)} hit(s)")
        for m in ms[:2]:
            print(f"      …{t[max(0,m.start()-420):m.end()+620]}…\n")
