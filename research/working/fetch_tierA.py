import json,subprocess,hashlib,os,re,html as H,collections
from concurrent.futures import ThreadPoolExecutor
A=json.load(open('tierA_v11.json'))
os.makedirs('ta',exist_ok=True)
urls=sorted({x['url'] for x in A})
def key(u): return hashlib.md5(u.encode()).hexdigest()[:10]
def existing(u):
    k=key(u)
    for d in ('h','src','q','ta'):
        p='%s/%s.txt'%(d,k)
        if os.path.exists(p) and os.path.getsize(p)>800: return p
    return None
def fetch(u):
    if existing(u): return u,'CACHED'
    k=key(u); b='ta/%s.bin'%k; t='ta/%s.txt'%k
    tgt=u.replace('/abs/','/pdf/') if 'arxiv.org/abs/' in u else u
    subprocess.run(['curl','-sL','--max-time','55','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36','-o',b,tgt],capture_output=True)
    if not os.path.exists(b) or os.path.getsize(b)<400: return u,'FAIL'
    if open(b,'rb').read(4)==b'%PDF': subprocess.run(['pdftotext','-q',b,t])
    else:
        d=open(b,encoding='utf-8',errors='ignore').read()
        d=re.sub(r'<(script|style)[^>]*>.*?</\1>','',d,flags=re.S|re.I)
        open(t,'w').write(H.unescape(re.sub(r'<[^>]+>',' ',d)))
    if not os.path.exists(t) or os.path.getsize(t)<400: return u,'THIN'
    return u,'OK'
st={}
with ThreadPoolExecutor(10) as ex:
    for u,s in ex.map(fetch,urls): st[u]=s
json.dump(st,open('ta_fetch.json','w'),indent=1)
print(collections.Counter(st.values()))
for u,s in st.items():
    if s in ('FAIL','THIN'): print('  ',s,u[:95])
