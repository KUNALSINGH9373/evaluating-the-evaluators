import json,hashlib,os,re,openpyxl
A=json.load(open('tierA_v11.json'))
wb=openpyxl.load_workbook('/Users/kunalsingh/Desktop/v11_FINAL.xlsx'); ws=wb[wb.sheetnames[0]]
hdr=[c.value for c in ws[1]]; ix={h:i+1 for i,h in enumerate(hdr) if h}
Q={x['fid']:(ws.cell(x['row'],ix['Finding Quote']).value or '') for x in A}
def path(u):
    k=hashlib.md5(u.encode()).hexdigest()[:10]
    for d in ('h','src','q','ta'):
        p='%s/%s.txt'%(d,k)
        if os.path.exists(p) and os.path.getsize(p)>800: return p
def norm(s): return re.sub(r'\s+',' ',s.replace('​','')).strip()
RESP=re.compile(r"\b(we (?:have |had |had already )?(?:patched|fixed|mitigat\w+|remediat\w+|address\w+|updated|added|deployed|implemented|introduced|strengthen\w+|retrained|revised|removed|blocked|resolved)|were (?:all )?patched|has been patched|have been patched|in response to (?:this|these|their|the)|as a result(?:,| of)|we will (?:share|continue|deploy|add)|prior to (?:launch|release|deployment) we|before (?:launch|release) we|we made (?:the following )?changes|remediation)",re.I)
pre=[x for x in A if x['access'] in ('Pre-deployment','Mixed')]
out=[]
for x in pre:
    p=path(x['url'])
    if not p: out.append({**x,'cands':[],'err':'no text'}); continue
    t=norm(open(p,encoding='utf-8',errors='ignore').read())
    q=norm(Q[x['fid']])[:70]
    anchor=t.find(q) if q else -1
    if anchor<0:
        w=norm(Q[x['fid']]).split()
        for i in range(0,max(1,len(w)-7),5):
            j=t.find(' '.join(w[i:i+8]))
            if j>=0: anchor=j; break
    win=t[max(0,anchor-1500):anchor+4000] if anchor>=0 else t
    cands=[]
    for m in RESP.finditer(win):
        s=win.rfind('.',0,m.start()); e=win.find('.',m.end())
        sent=win[(s+1 if s>=0 else 0):(e+1 if e>0 else m.end()+200)].strip()
        if 60<len(sent)<600: cands.append(sent)
    seen=set(); ded=[]
    for c in cands:
        if c[:60] not in seen: seen.add(c[:60]); ded.append(c)
    out.append({**x,'anchored':anchor>=0,'cands':ded[:3]})
json.dump(out,open('chA_pre.json','w'),indent=1)
print('pre-deployment Tier A rows:',len(out))
print('anchored to the quote     :',sum(1 for o in out if o.get('anchored')))
print('with >=1 response candidate:',sum(1 for o in out if o['cands']))
