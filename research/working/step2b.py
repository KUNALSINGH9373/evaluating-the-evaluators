#!/usr/bin/env python3
import re, os
D = os.path.dirname(os.path.abspath(__file__))
t = re.sub(r'\s+', ' ', open(os.path.join(D, 'mythos5.txt'), encoding='utf-8', errors='ignore').read())
m = re.search(r'Therefore, the increased rate of continuing', t)
print("--- continuation after 'Therefore, the increased rate...' ---")
print(t[m.start() - 700:m.start() + 1800] if m else "NOT FOUND")
print("\n\n--- any mitigation language near the research-sabotage section ---")
for pat in [r'we (?:will|plan to|intend to|are) [^.]{0,180}(?:monitor|mitigat|iterat|address)[^.]{0,120}\.',
            r'research sabotage[^.]{0,300}\.']:
    for mm in list(re.finditer(pat, t, re.I))[:3]:
        print(f"\n[{pat[:34]}] …{t[max(0,mm.start()-300):mm.end()+400]}…")
