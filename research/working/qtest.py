import json,subprocess,hashlib,os,re,collections
from concurrent.futures import ThreadPoolExecutor
d=json.load(open('hold.json'))
qrows=[x for x in d if 'QUOTE' in x['defects']]
urls=sorted({x['url'] for x in qrows})
os.makedirs('q',exist_ok=True)
def norm(s):
    s=s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
    s=s.replace('—','-').replace('–','-').replace(' ',' ')
    return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
def fetch(u):
    k=hashlib.md5(u.encode()).hexdigest()[:10]; b=f'q/{k}.bin'; t=f'q/{k}.txt'
    if u.startswith('https://arxiv.org/abs/'): u2=u.replace('/abs/','/pdf/')
    else: u2=u
    subprocess.run(['curl','-sL','--max-time','50','-A','Mozilla/5.0','-o',b,u2],capture_output=True)
    if not os.path.exists(b) or os.path.getsize(b)<400: return u,None,'FETCH-FAIL'
    if open(b,'rb').read(4)==b'%PDF': subprocess.run(['pdftotext','-q',b,t])
    else:
        h=open(b,encoding='utf-8',errors='ignore').read()
        h=re.sub(r'<(script|style)[^>]*>.*?</\1>','',h,flags=re.S|re.I)
        import html as H
        open(t,'w').write(H.unescape(re.sub(r'<[^>]+>',' ',h)))
    if not os.path.exists(t): return u,None,'NOTXT'
    return u,norm(open(t,encoding='utf-8',errors='ignore').read()),'OK'
cache={}
with ThreadPoolExecutor(10) as ex:
    for u,txt,st in ex.map(fetch,urls): cache[u]=(txt,st)
res=collections.Counter(); detail=[]
for x in qrows:
    txt,st=cache[x['url']]
    q=norm(x['quote'])
    if txt is None: v='FETCH-FAIL'
    elif not q: v='EMPTY-QUOTE'
    else:
        if q in txt: v='FOUND-EXACT'
        else:
            w=q.split(); 
            probes=[' '.join(w[i:i+8]) for i in range(0,max(1,len(w)-7),6)]
            hit=sum(1 for p in probes if p in txt)
            v='FOUND-PARTIAL(%d/%d)'%(hit,len(probes)) if hit else 'NOT-FOUND'
            if hit and hit==len(probes): v='FOUND-SPLICED'
    res[v.split('(')[0]]+=1; detail.append((x['row'],x['fid'],x['inst'][:26],v,x['url']))
json.dump(detail,open('qtest.json','w'),indent=1)
print('fetch:',collections.Counter(s for _,s in cache.values()))
print()
for k,v in res.most_common(): print(' %3d %s'%(v,k))
