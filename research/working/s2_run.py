import json,re,subprocess,time,urllib.parse,sys,openpyxl
wb=openpyxl.load_workbook('/Users/kunalsingh/Desktop/v11_FINAL.xlsx'); ws=wb[wb.sheetnames[0]]
hdr=[c.value for c in ws[1]]; ix={h:i+1 for i,h in enumerate(hdr) if h}
G=lambda r,k: ws.cell(r,ix[k]).value
A=[dict(fid=G(r,'Finding ID'),title=str(G(r,'Report Title ') or ''),url=str(G(r,'Source URL') or ''),inst=str(G(r,'Institution') or ''))
   for r in range(2,ws.max_row+1) if G(r,'Action Trackable?')=='yes']
F='paperId,title,year,citationCount,influentialCitationCount,externalIds,publicationDate'
SKIP=re.compile(r'^\[Leaderboard\]|^\[Labs Blog\]|system card|addendum|update to',re.I)
def get(url,tries=8):
    for i in range(tries):
        o=subprocess.run(['curl','-sL','--max-time','40',url],capture_output=True,text=True).stdout
        try: d=json.loads(o)
        except Exception: time.sleep(8); continue
        if isinstance(d,dict) and str(d.get('code'))=='429':
            time.sleep(12*(i+1)); continue
        return d
    return None
def norm(s): return set(re.sub(r'[^a-z0-9 ]',' ',s.lower()).split())
# 1) identifier-resolvable
ids={}
for x in A:
    m=re.search(r'arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})',x['url'])
    if m: ids[x['fid']]='ARXIV:'+m.group(1); continue
    m=re.search(r'aclanthology\.org/([0-9]{4}\.[a-z-]+\.[0-9]+)',x['url'])
    if m: ids[x['fid']]='ACL:'+m.group(1)
res={}
if ids:
    u=sorted(set(ids.values()))
    d=get('https://api.semanticscholar.org/graph/v1/paper/batch?fields='+F)  # warm
    r=subprocess.run(['curl','-sL','--max-time','60','-X','POST','-H','Content-Type: application/json',
        '-d',json.dumps({'ids':u}),'https://api.semanticscholar.org/graph/v1/paper/batch?fields='+F],capture_output=True,text=True).stdout
    try:
        for i,rec in zip(u,json.loads(r)):
            if rec: res[i]=rec
    except Exception as e: print('batch err',e,flush=True)
print('by identifier: %d/%d resolved'%(len(res),len(set(ids.values()))),flush=True)
# 2) title search for the rest
titles=sorted({x['title'] for x in A if x['title'] and not SKIP.search(x['title'])})
tres={}
for n,t in enumerate(titles,1):
    clean=re.sub(r'\s*\(.*?\)\s*$','',re.sub(r'^\[.*?\]\s*','',t))[:140]
    d=get('https://api.semanticscholar.org/graph/v1/paper/search?query=%s&limit=5&fields=%s'%(urllib.parse.quote(clean),F))
    if d is None:
        print('  %2d/%d RATE-LIMITED %s'%(n,len(titles),t[:46]),flush=True); time.sleep(20); continue
    best=None; tw=norm(clean)
    for c in (d.get('data') or []):
        cw=norm(c.get('title') or '')
        if not tw or not cw: continue
        j=len(tw&cw)/len(tw|cw)
        if j>=0.55 and (best is None or j>best[0]): best=(j,c)
    if best: tres[t]={'jaccard':round(best[0],2),**best[1]}
    print('  %2d/%d %-10s %s'%(n,len(titles),('cites=%s'%best[1].get('citationCount')) if best else 'no-match',t[:46]),flush=True)
    time.sleep(4.5)
json.dump({'by_id':res,'by_title':tres,'id_map':ids},open('s2_final.json','w'),indent=1)
print('DONE: by_id %d, by_title %d/%d'%(len(res),len(tres),len(titles)),flush=True)
