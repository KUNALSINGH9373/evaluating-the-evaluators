import os,re,json,glob,collections,datetime
rem=json.load(open('remaining.json'))
# --- corpus with company + doc date ---
DOC=[]
seen=set()
for d in ('src','h','q','ta','ch'):
    for p in sorted(glob.glob(d+'/*.txt')):
        t=open(p,encoding='utf-8',errors='ignore').read()
        if len(t)<3000: continue
        t=re.sub(r'\s+',' ',t)
        head=t[:300]
        if not re.search(r'system card|preparedness|risk report|deployment safety|responsible scaling|safety & preparedness',head,re.I): continue
        sig=head[:90]
        if sig in seen: continue
        seen.add(sig)
        co=('Anthropic' if re.search(r'anthropic',head,re.I) else 'Meta' if re.search(r'Muse Spark|Meta',head,re.I) else 'OpenAI')
        m=re.search(r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{0,2},?\s*20\d\d)|(\d{4}-\d{2}-\d{2})',head)
        DOC.append(dict(path=p,co=co,title=head[:70].strip(),date=(m.group(0) if m else ''),text=t))
print('corpus:',len(DOC),'unique company documents')
print(' ',collections.Counter(d['co'] for d in DOC))
# --- scan: does any company doc mention this evaluator AND the finding topic? ---
EVAL={'Center for AI Safety (CAIS)':['Center for AI Safety','CAIS','Zou et al','GCG'],
 'FAR.AI':['FAR.AI','FAR AI'],'Scale AI':['Scale AI','SEAL','Scale'],'METR':['METR'],
 'Apollo Research':['Apollo Research','Apollo'],'Redwood Research':['Redwood Research','Redwood'],
 'SecureBio':['SecureBio'],'Transluce':['Transluce'],'Dreadnode':['Dreadnode'],
 'RAND Europe':['RAND Europe','RAND'],'Cisco (Robust Intelligence / Foundation AI)':['Robust Intelligence','Cisco'],
 'Shanghai AI Laboratory (AI45 Lab)':['Shanghai AI Lab','AI45'],
 'UK AISI + Anthropic + Theorem + MATS':['UK AISI','UK AI Security Institute']}
out=[]
for x in rem:
    names=None
    for k,v in EVAL.items():
        if x['inst'].startswith(k[:14]): names=v; break
    names=names or [x['inst'].split('(')[0].strip()]
    hits=[]
    for d in DOC:
        if d['co'] not in x['dev'].split('+') and x['dev']!='none': continue
        for nm in names:
            for m in re.finditer(r'\b'+re.escape(nm)+r'\b',d['text']):
                hits.append(dict(doc=d['title'],date=d['date'],path=d['path'],name=nm,
                                 ctx=d['text'][max(0,m.start()-200):m.start()+260]))
                break
    out.append({**x,'hits':hits[:4],'nhits':len(hits)})
json.dump(out,open('corpus_scan.json','w'),indent=1)
print()
print('rows with >=1 evaluator mention in a company doc:',sum(1 for o in out if o['nhits']))
print('rows with none                                 :',sum(1 for o in out if not o['nhits']))
c=collections.Counter(o['inst'] for o in out if o['nhits'])
for k,v in c.most_common(): print('   %2d  %s'%(v,k))
