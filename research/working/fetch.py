import subprocess, hashlib, os
from concurrent.futures import ThreadPoolExecutor
urls = """https://www.anthropic.com/claude-opus-5-system-card
https://www.anthropic.com/claude-mythos-preview-system-card
https://www.anthropic.com/claude-sonnet-5-system-card
https://www.anthropic.com/claude-sonnet-4-6-system-card
https://ai.meta.com/static-resource/muse-spark-safety-and-preparedness-report
https://deploymentsafety.openai.com/gpt-5-5
https://deploymentsafety.openai.com/gpt-5-6-preview/
https://cdn.openai.com/gpt-4o-system-card.pdf
https://www.anthropic.com/research/shade-arena-sabotage-monitoring
https://alignment.anthropic.com/2026/sleight-bench
https://www-cdn.anthropic.com/bf10f64990cfda0ba858290be7b8cc6317685f47.pdf
https://www-cdn.anthropic.com/963373e433e489a87a10c823c52a0a013e9172dd.pdf""".split()
def go(u):
    k=hashlib.md5(u.encode()).hexdigest()[:10]
    b=f"src/{k}.bin"; t=f"src/{k}.txt"
    r=subprocess.run(["curl","-sL","--max-time","45","-A","Mozilla/5.0","-o",b,u],capture_output=True)
    if not os.path.exists(b) or os.path.getsize(b)<500: return (u,k,"FAIL")
    head=open(b,'rb').read(5)
    if head[:4]==b'%PDF':
        subprocess.run(["pdftotext","-q",b,t])
    else:
        subprocess.run(f"python3 -c \"import re,sys,html;d=open('{b}',encoding='utf-8',errors='ignore').read();d=re.sub(r'<(script|style)[^>]*>.*?</\\\\1>','',d,flags=re.S|re.I);d=re.sub(r'<[^>]+>',' ',d);open('{t}','w').write(html.unescape(re.sub(r'[ \\t]+',' ',d)))\"",shell=True)
    return (u,k,os.path.getsize(t) if os.path.exists(t) else "NOTXT")
with ThreadPoolExecutor(10) as ex:
    for r in ex.map(go, urls): print(r)
