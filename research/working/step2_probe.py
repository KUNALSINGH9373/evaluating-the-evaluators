#!/usr/bin/env python3
"""Probe the cached source documents for the three undated-battery rows."""
import re, os
D = os.path.dirname(os.path.abspath(__file__))


def load(f):
    t = open(os.path.join(D, f), encoding='utf-8', errors='ignore').read()
    return re.sub(r'\s+', ' ', t)


def show(t, pat, label, before=420, after=900, limit=2):
    print(f"\n>>> [{label}]")
    hits = 0
    for m in re.finditer(pat, t, re.I):
        print("   …" + t[max(0, m.start() - before):m.end() + after] + "…\n")
        hits += 1
        if hits >= limit:
            break
    if not hits:
        print("   NOT FOUND")


print("=" * 100)
print("JOINT-2026-07-CYB1 — GPT-5.6 card: is UK AISI's cyber-range result an input to the High cyber designation?")
t = load('gpt56.txt')
show(t, r'External Evaluations for Cyber Capabilities\s*[–-]\s*UK AISI', 'UK AISI cyber section', 200, 1600, 1)
show(t, r'we are treating Sol, Terra and Luna as High capability', 'High capability designation', 300, 700, 1)
show(t, r'The Last Ones', 'the named cyber range', 400, 700, 1)

print("\n" + "=" * 100)
print("UKAISI-2026-06-ALI6 — Fable5/Mythos5 card: any response to the 14% sabotage-continuation rate?")
m = load('mythos5.txt')
show(m, r'14%', 'the 14% figure', 500, 1100, 3)
show(m, r'continues compromising|continue to compromis|sabotage', 'sabotage-continuation language', 400, 900, 2)
