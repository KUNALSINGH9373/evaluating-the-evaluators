import json,subprocess,urllib.parse,re,time,collections,openpyxl
wb=openpyxl.load_workbook('/Users/kunalsingh/Desktop/v11_FINAL.xlsx'); ws=wb[wb.sheetnames[0]]
hdr=[c.value for c in ws[1]]; ix={h:i+1 for i,h in enumerate(hdr) if h}
G=lambda r,k: ws.cell(r,ix[k]).value
A=[dict(row=r,fid=G(r,'Finding ID'),inst=str(G(r,'Institution') or ''),date=str(G(r,'Publication Date') or ''),
        title=str(G(r,'Report Title ') or ''))
   for r in range(2,ws.max_row+1) if G(r,'Action Trackable?')=='yes']
# search terms: evaluator names (exact phrases) + distinctive report titles
EV=sorted({x['inst'] for x in A})
TERMS=set()
for e in EV:
    base=re.sub(r'\s*\(.*?\)','',e).strip()
    TERMS.add(base)
    if 'UK AI' in base or 'UK AISI' in base: TERMS.add('AI Security Institute')
    if 'CAIS' in e: TERMS.add('Center for AI Safety')
TITLES={x['title'] for x in A if len(x['title'])>24 and not x['title'].startswith('[')}
def q(u):
    for i in range(3):
        o=subprocess.run(['curl','-sL','--max-time','30',u],capture_output=True,text=True).stdout
        try: return json.loads(o)
        except Exception: time.sleep(2)
    return None
res={'federal_register':{},'hansard':{}}
print('=== Federal Register (exact phrase) ===')
for t in sorted(TERMS):
    d=q('https://www.federalregister.gov/api/v1/documents.json?per_page=5&conditions%%5Bterm%%5D=%s'%urllib.parse.quote('"%s"'%t))
    n=(d or {}).get('count',0)
    res['federal_register'][t]={'count':n,'hits':[{'title':r['title'],'date':r['publication_date'],'url':r['html_url'],'type':r.get('type')} for r in (d or {}).get('results',[])[:5]]}
    print('  %-42s %s'%(t[:42],n))
    time.sleep(0.7)
print()
print('=== Hansard (exact-phrase verified) ===')
for t in sorted(TERMS):
    d=q('https://hansard-api.parliament.uk/search.json?queryParameters.searchTerm=%s&queryParameters.take=10'%urllib.parse.quote('"%s"'%t))
    if not d: print('  %-42s ERR'%t[:42]); continue
    hits=[]
    for c in (d.get('Contributions') or []):
        txt=' '.join(str(c.get(k) or '') for k in ('ContributionText','DebateSection','Title'))
        if t.lower() in txt.lower():
            hits.append({'member':c.get('MemberName'),'house':c.get('House'),'date':c.get('SittingDate'),'section':c.get('DebateSection'),'text':txt[:300]})
    res['hansard'][t]={'raw':d.get('TotalContributions',0),'verified':len(hits),'hits':hits[:4]}
    print('  %-42s raw=%-5s exact=%s'%(t[:42],d.get('TotalContributions',0),len(hits)))
    time.sleep(0.7)
json.dump(res,open('chB_sweep.json','w'),indent=1)
