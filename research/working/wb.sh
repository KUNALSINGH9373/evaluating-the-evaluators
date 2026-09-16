#!/bin/bash
# fetch a URL via Wayback, print resolved snapshot + extracted text path
u="$1"; n=$(echo "$u" | md5 | cut -c1-8)
loc=$(curl -sIL --max-time 45 -A "Mozilla/5.0" "https://web.archive.org/web/2026/$u" 2>/dev/null | grep -i '^location:' | tail -1 | sed 's/^[Ll]ocation: //;s/\r//')
[ -z "$loc" ] && loc="https://web.archive.org/web/2026/$u"
curl -sL --max-time 60 -A "Mozilla/5.0" -o "ch/$n.bin" "$loc"
python3 - "$n" "$u" "$loc" <<'PY'
import re,html,sys
n,u,loc=sys.argv[1:4]
d=open('ch/%s.bin'%n,encoding='utf-8',errors='ignore').read()
d=re.sub(r'<(script|style)[^>]*>.*?</\1>','',d,flags=re.S|re.I)
t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',d)))
open('ch/%s.txt'%n,'w').write(t)
MON='January|February|March|April|May|June|July|August|September|October|November|December'
print('  snapshot:',loc[:96])
print('  len %d | dates %s'%(len(t),re.findall(r'(?:%s)\s+\d{1,2},?\s+20\d\d'%MON,t)[:4]))
print('  file: ch/%s.txt'%n)
PY
