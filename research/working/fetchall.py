import json,subprocess,hashlib,os,re,html as H,collections
from concurrent.futures import ThreadPoolExecutor
urls=json.load(open('hold_urls.json'))
os.makedirs('h',exist_ok=True)
def key(u): return hashlib.md5(u.encode()).hexdigest()[:10]
def fetch(u):
    k=key(u); b=f'h/{k}.bin'; t=f'h/{k}.txt'
    if os.path.exists(t) and os.path.getsize(t)>800: return u,'CACHED'
    tgt=u.replace('/abs/','/pdf/') if u.startswith('https://arxiv.org/abs/') else u
    subprocess.run(['curl','-sL','--max-time','55','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36','-o',b,tgt],capture_output=True)
    if not os.path.exists(b) or os.path.getsize(b)<400: return u,'FETCH-FAIL'
    if open(b,'rb').read(4)==b'%PDF':
        subprocess.run(['pdftotext','-q',b,t])
    else:
        d=open(b,encoding='utf-8',errors='ignore').read()
        d=re.sub(r'<(script|style|nav|footer)[^>]*>.*?</\1>','',d,flags=re.S|re.I)
        open(t,'w').write(H.unescape(re.sub(r'<[^>]+>',' ',d)))
    if not os.path.exists(t) or os.path.getsize(t)<300: return u,'THIN'
    return u,'OK'
res={}
with ThreadPoolExecutor(12) as ex:
    for u,s in ex.map(fetch,urls): res[u]=s
json.dump(res,open('fetch_status.json','w'),indent=1)
print(collections.Counter(res.values()))
for u,s in res.items():
    if s not in ('OK','CACHED'): print('  ',s,u)
