import subprocess, hashlib, os
from concurrent.futures import ThreadPoolExecutor
urls=["https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf",
"https://www.anthropic.com/research/cyber-evaluations-claude-4",
"https://cdn.openai.com/o1-system-card-20241205.pdf"]
def go(u):
    k=hashlib.md5(u.encode()).hexdigest()[:10]; b=f"src/{k}.bin"; t=f"src/{k}.txt"
    subprocess.run(["curl","-sL","--max-time","45","-A","Mozilla/5.0","-o",b,u],capture_output=True)
    if not os.path.exists(b) or os.path.getsize(b)<500: return (u,k,"FAIL")
    if open(b,'rb').read(4)==b'%PDF': subprocess.run(["pdftotext","-q",b,t])
    else:
        subprocess.run(f"python3 -c \"import re,html;d=open('{b}',encoding='utf-8',errors='ignore').read();d=re.sub(r'<(script|style)[^>]*>.*?</\\\\1>','',d,flags=re.S|re.I);d=re.sub(r'<[^>]+>',' ',d);open('{t}','w').write(html.unescape(re.sub(r'[ \\t]+',' ',d)))\"",shell=True)
    return (u,k,os.path.getsize(t) if os.path.exists(t) else "NOTXT")
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(go,urls): print(r)
