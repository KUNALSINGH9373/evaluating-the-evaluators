import json,re,subprocess,time,urllib.parse,openpyxl,collections
MAIL='singhkunal9373@gmail.com'
wb=openpyxl.load_workbook('/Users/kunalsingh/Desktop/v11_FINAL.xlsx'); ws=wb[wb.sheetnames[0]]
hdr=[c.value for c in ws[1]]; ix={h:i+1 for i,h in enumerate(hdr) if h}
G=lambda r,k: ws.cell(r,ix[k]).value
A=[dict(row=r,fid=G(r,'Finding ID'),title=str(G(r,'Report Title ') or ''),url=str(G(r,'Source URL') or ''),
        inst=str(G(r,'Institution') or ''),date=str(G(r,'Publication Date') or ''))
   for r in range(2,ws.max_row+1) if G(r,'Action Trackable?')=='yes']
SKIP=re.compile(r'^\[Leaderboard\]|^\[Labs Blog\]|system card|addendum|update to|pre-release testing report',re.I)
def get(u):
    for i in range(4):
        o=subprocess.run(['curl','-sL','--max-time','35',u],capture_output=True,text=True).stdout
        try: return json.loads(o)
        except Exception: time.sleep(3)
    return None
def norm(s): return set(re.sub(r'[^a-z0-9 ]',' ',s.lower()).split())
# 1) arXiv / ACL identifier -> exact DOI lookup
byid={}
for x in A:
    m=re.search(r'arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})',x['url'])
    if not m: continue
    doi='10.48550/arxiv.'+m.group(1)
    d=get('https://api.openalex.org/works/https://doi.org/%s?mailto=%s'%(doi,MAIL))
    if d and not d.get('error'):
        byid[x['fid']]=dict(title=d.get('title'),date=d.get('publication_date'),cites=d.get('cited_by_count'),
                            doi=d.get('doi'),oa=d.get('id'))
        print('ID  %-30s cites=%-5s %s'%(x['fid'],d.get('cited_by_count'),(d.get('title') or '')[:46]),flush=True)
    time.sleep(0.35)
# 2) title search for the rest
titles=sorted({x['title'] for x in A if x['title'] and not SKIP.search(x['title'])})
bytitle={}
for n,t in enumerate(titles,1):
    clean=re.sub(r'\s*\(.*?\)\s*$','',re.sub(r'^\[.*?\]\s*','',t))
    d=get('https://api.openalex.org/works?search=%s&per-page=5&mailto=%s'%(urllib.parse.quote(clean[:160]),MAIL))
    best=None; tw=norm(clean)
    for w in ((d or {}).get('results') or []):
        cw=norm(w.get('title') or '')
        if not tw or not cw: continue
        j=len(tw&cw)/len(tw|cw)
        if j>=0.6 and (best is None or j>best[0]): best=(j,w)
    if best:
        w=best[1]
        bytitle[t]=dict(jaccard=round(best[0],2),title=w.get('title'),date=w.get('publication_date'),
                        cites=w.get('cited_by_count'),doi=w.get('doi'),oa=w.get('id'))
    print(' %2d/%d %-11s %s'%(n,len(titles),('cites=%s'%best[1].get('cited_by_count')) if best else 'no-match',t[:48]),flush=True)
    time.sleep(0.35)
json.dump({'by_id':byid,'by_title':bytitle},open('openalex.json','w'),indent=1)
print('\nDONE  by_id %d  by_title %d/%d'%(len(byid),len(bytitle),len(titles)),flush=True)
