import json,re,hashlib,os,collections
hold=json.load(open('hold_full.json')); ALT=json.load(open('alt_urls.json'))
AX=json.load(open('arxiv_dates.json'))
def norm(s):
    s=s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"').replace('—','-').replace('–','-').replace(' ',' ').replace('​','')
    return re.sub(r'[^a-z0-9]+',' ',s.lower()).strip()
def rawnorm(s):
    s=s.replace(' ',' ').replace('​','').replace('−','-')
    return re.sub(r'\s+',' ',s)
TX={}
def text(u):
    if u in TX: return TX[u]
    k=hashlib.md5(u.encode()).hexdigest()[:10]; p=f'h/{k}.txt'
    t=open(p,encoding='utf-8',errors='ignore').read() if os.path.exists(p) else None
    TX[u]=(norm(t),rawnorm(t)) if t else (None,None)
    return TX[u]
def numvariants(n):
    n=n.strip().rstrip('.')
    v={n}
    v.add(n.replace(',',''))
    if n.endswith('%'):
        b=n[:-1]; v|={b,b.replace(',',''),b+' %'}
    else: v.add(n+'%')
    if re.fullmatch(r'\d+\.0',n): v.add(n[:-2])
    if re.fullmatch(r'\d+',n): v|={n+'.0'}
    return {x for x in v if x}
out=[]
for x in hold:
    nt,rt=text(x['url'])
    res={'row':x['row'],'fid':x['fid'],'defects':x['defects'],'resolved':[],'open':[],'evidence':{}}
    if nt is None:
        res['open']=list(x['defects']); res['evidence']['fetch']='source unfetchable'
        out.append(res); continue
    if 'QUOTE' in x['defects']:
        q=norm(x['quote'])
        ok=False
        if q and q in nt: ok=True; res['evidence']['quote']='exact'
        elif q:
            w=q.split(); probes=[' '.join(w[i:i+8]) for i in range(0,max(1,len(w)-7),6)]
            hit=sum(1 for p in probes if p in nt)
            if probes and hit==len(probes): ok=True; res['evidence']['quote']='all %d segments present (ellipsis/линebreak)'%len(probes)
            elif probes and hit>=max(2,int(0.8*len(probes))): ok=True; res['evidence']['quote']='%d/%d segments present'%(hit,len(probes))
            else: res['evidence']['quote']='not found (%d/%d segments)'%(hit,len(probes) if probes else 0)
        (res['resolved'] if ok else res['open']).append('QUOTE')
    if 'NUMBERS' in x['defects']:
        miss=[n for n in x['nums'] if not any(v in rt for v in numvariants(n))]
        if not miss and x['nums']:
            res['resolved'].append('NUMBERS'); res['evidence']['numbers']='all %d present'%len(x['nums'])
        elif not x['nums']:
            res['open'].append('NUMBERS'); res['evidence']['numbers']='no numbers parsed from note'
        else:
            res['open'].append('NUMBERS'); res['evidence']['numbers']='missing: '+', '.join(miss[:6])
    if 'DATE' in x['defects']:
        m=re.search(r'arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})',x['url'])
        if m and m.group(1) in AX:
            res['resolved'].append('DATE'); res['evidence']['date']=AX[m.group(1)][0]; res['newdate']=AX[m.group(1)][0]
        else:
            res['open'].append('DATE'); res['evidence']['date']='no machine-readable date'
    if 'SOURCE' in x['defects']:
        res['resolved'].append('SOURCE'); res['evidence']['source']='refetched OK'
    out.append(res)
json.dump(out,open('verify.json','w'),indent=1)
full=[r for r in out if not r['open']]
print('HOLD rows:',len(out))
print('FULLY RESOLVED ->flip:',len(full))
print('still open      :',len(out)-len(full))
print()
print('open by remaining defect:',collections.Counter(tuple(r['open']) for r in out if r['open']).most_common())
