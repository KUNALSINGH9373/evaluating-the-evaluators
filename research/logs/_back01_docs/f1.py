import sys, json, os
sys.path.insert(0, '/Users/kunalsingh/MATS/Research/AISI_Evals/scripts')
from fetch import get
D='/Users/kunalsingh/MATS/Research/AISI_Evals/logs/_back01_docs'
items=json.load(open('/Users/kunalsingh/MATS/Research/AISI_Evals/logs/window_extension/back/back_01.json'))
i=int(sys.argv[1])
it=items[i]
r=get(it['url'])
txt=r.get('text') or ''
open(os.path.join(D,'d%02d.txt'%i),'w').write(txt)
open(os.path.join(D,'m%02d.json'%i),'w').write(json.dumps(dict(url=it['url'],ok=r.get('ok'),via=r.get('via'),status=r.get('status'),chars=len(txt),meta=r.get('meta'),attempts=r.get('attempts')),indent=1))
print(json.dumps(dict(i=i,url=it['url'],ok=r.get('ok'),via=r.get('via'),status=r.get('status'),chars=len(txt),meta=r.get('meta'))))
