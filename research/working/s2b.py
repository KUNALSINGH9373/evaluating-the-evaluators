import json,re,subprocess,time,urllib.parse,collections
A=json.load(open('tierA_v11.json'))
F='paperId,title,year,citationCount,influentialCitationCount,externalIds,publicationDate,authors'
def norm(s): return re.sub(r'[^a-z0-9 ]',' ',s.lower()).split()
SKIP=re.compile(r'system card|addendum|update to|preparedness|safety & preparedness|deployment',re.I)
res={}
titles=sorted({x['title'] for x in A if x['title'] and not SKIP.search(x['title'])})
print(len(titles),'candidate titles (system cards excluded — they are not papers)')
for t in titles:
    q=urllib.parse.quote(re.sub(r'\[.*?\]','',t)[:120])
    r=subprocess.run(['curl','-sL','--max-time','30',
      f'https://api.semanticscholar.org/graph/v1/paper/search?query={q}&limit=3&fields={F}'],capture_output=True,text=True).stdout
    try: d=json.loads(r).get('data',[])
    except Exception: d=[]
    best=None
    tw=set(norm(t))
    for c in d:
        cw=set(norm(c.get('title') or ''))
        if not tw or not cw: continue
        j=len(tw&cw)/len(tw|cw)
        if j>=0.6 and (best is None or j>best[0]): best=(j,c)
    if best: res[t]={'match':best[1],'jaccard':round(best[0],2)}
    time.sleep(1.1)
json.dump(res,open('s2_titles.json','w'),indent=1)
print('matched',len(res),'of',len(titles))
for t,v in sorted(res.items(), key=lambda kv:-(kv[1]['match'].get('citationCount') or 0)):
    m=v['match']
    print('  cites=%-5s j=%.2f  %s'%(m.get('citationCount'),v['jaccard'],(m.get('title') or '')[:66]))
