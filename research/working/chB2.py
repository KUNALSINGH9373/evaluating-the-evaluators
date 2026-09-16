import json,subprocess,urllib.parse,time,re
def q(u):
    for i in range(3):
        o=subprocess.run(['curl','-sL','--max-time','35',u],capture_output=True,text=True).stdout
        try: return json.loads(o)
        except Exception: time.sleep(2)
    return None
TERMS=['AI Security Institute','Apollo Research','Center for AI Safety','Dreadnode','FAR.AI','Gray Swan AI',
       'METR','RAND Europe','Redwood Research','Scale AI','SecureBio','Shanghai AI Laboratory','Transluce']
print('=== Hansard, matching ContributionTextFull, take=20 ===')
out={}
for t in TERMS:
    d=q('https://hansard-api.parliament.uk/search.json?queryParameters.searchTerm=%s&queryParameters.take=20'%urllib.parse.quote('"%s"'%t))
    if not d: print('  %-24s ERR'%t); continue
    hits=[]
    for c in (d.get('Contributions') or []):
        full=str(c.get('ContributionTextFull') or c.get('ContributionText') or '')
        if re.search(re.escape(t),full,re.I):
            hits.append(dict(member=c.get('MemberName'),house=c.get('House'),date=str(c.get('SittingDate'))[:10],
                             sec=c.get('DebateSection'),
                             snip=re.sub(r'\s+',' ',full[max(0,full.lower().find(t.lower())-140):full.lower().find(t.lower())+220])))
    out[t]=dict(total=d.get('TotalContributions'),returned=len(d.get('Contributions') or []),verified=len(hits),hits=hits[:3])
    print('  %-24s total=%-5s returned=%-3s exact=%s'%(t,d.get('TotalContributions'),len(d.get('Contributions') or []),len(hits)))
    time.sleep(0.6)
json.dump(out,open('chB_hansard.json','w'),indent=1)
print()
print('=== Federal Register hits worth inspecting ===')
for t in ['METR','RAND Europe','Scale AI']:
    d=q('https://www.federalregister.gov/api/v1/documents.json?per_page=6&conditions%%5Bterm%%5D=%s'%urllib.parse.quote('"%s"'%t))
    print(' --',t,'count',(d or {}).get('count'))
    for r in (d or {}).get('results',[])[:6]:
        print('     %s  %-14s %s'%(r['publication_date'],(r.get('type') or '')[:14],r['title'][:78]))
    time.sleep(0.6)
