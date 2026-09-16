import json,re,subprocess,time,urllib.parse,sys
A=json.load(open('tierA_v11.json'))
F='paperId,title,year,citationCount,influentialCitationCount,externalIds,publicationDate'
SKIP=re.compile(r'^\[Leaderboard\]|^\[Labs Blog\]|system card|addendum|update to|pre-release testing report',re.I)
titles=sorted({x['title'] for x in A if x['title'] and not SKIP.search(x['title'])})
def norm(s): return set(re.sub(r'[^a-z0-9 ]',' ',s.lower()).split())
def get(url,tries=6):
    for i in range(tries):
        out=subprocess.run(['curl','-sL','--max-time','30',url],capture_output=True,text=True).stdout
        try: d=json.loads(out)
        except Exception: d={'message':'unparseable','raw':out[:120]}
        if isinstance(d,dict) and d.get('code')=='429':
            time.sleep(5*(i+1)); continue
        return d,None
    return None,'429 after %d tries'%tries
res={}; fails=[]
for n,t in enumerate(titles,1):
    clean=re.sub(r'\s*\(.*?\)\s*$','',re.sub(r'^\[.*?\]\s*','',t))[:140]
    d,err=get('https://api.semanticscholar.org/graph/v1/paper/search?query=%s&limit=5&fields=%s'%(urllib.parse.quote(clean),F))
    if err: fails.append((t,err)); print('  %2d/%d  RATE-LIMITED  %s'%(n,len(titles),t[:50])); continue
    best=None; tw=norm(clean)
    for c in (d.get('data') or []):
        cw=norm(c.get('title') or '')
        if not tw or not cw: continue
        j=len(tw&cw)/len(tw|cw)
        if j>=0.55 and (best is None or j>best[0]): best=(j,c)
    if best: res[t]={'jaccard':round(best[0],2),**best[1]}
    print('  %2d/%d  %-9s %s'%(n,len(titles),('cites=%s'%best[1].get('citationCount')) if best else 'no-match',t[:52]))
    time.sleep(3.2)
json.dump({'matched':res,'rate_limited':fails},open('s2_titles.json','w'),indent=1)
print()
print('matched %d / %d  |  rate-limited %d'%(len(res),len(titles),len(fails)))
