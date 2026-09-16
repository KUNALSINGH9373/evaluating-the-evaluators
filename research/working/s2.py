import json,re,subprocess,time,collections
A=json.load(open('tierA_v11.json'))
def ident(u,title):
    m=re.search(r'arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})',u)
    if m: return 'ARXIV:'+m.group(1)
    m=re.search(r'aclanthology\.org/([0-9]{4}\.[a-z-]+\.[0-9]+)',u)
    if m: return 'ACL:'+m.group(1)
    m=re.search(r'doi\.org/(10\.[^\s?#]+)',u)
    if m: return 'DOI:'+m.group(1)
    return None
F='paperId,title,year,citationCount,influentialCitationCount,externalIds,publicationDate'
out={}
ids=[(x['fid'],ident(x['url'],x['title'])) for x in A]
have=[(f,i) for f,i in ids if i]
print(len(have),'of',len(A),'Tier A rows have a resolvable paper identifier')
uniq=sorted({i for _,i in have})
# batch endpoint
r=subprocess.run(['curl','-sL','--max-time','60','-X','POST','-H','Content-Type: application/json',
 '-d',json.dumps({'ids':uniq}),
 'https://api.semanticscholar.org/graph/v1/paper/batch?fields='+F],capture_output=True,text=True).stdout
try: data=json.loads(r)
except Exception as e: print('ERR',r[:300]); raise SystemExit
for i,rec in zip(uniq,data if isinstance(data,list) else []):
    if rec: out[i]=rec
print('resolved',len(out),'of',len(uniq))
json.dump(out,open('s2.json','w'),indent=1)
for i in uniq:
    rec=out.get(i)
    if rec: print('  %-22s cites=%-5s infl=%-4s %s'%(i,rec.get('citationCount'),rec.get('influentialCitationCount'),(rec.get('title') or '')[:52]))
    else:   print('  %-22s NOT FOUND'%i)
