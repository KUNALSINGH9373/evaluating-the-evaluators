import subprocess,hashlib,os,re,html as H
ALT={'https://www.wmdp.ai/':'https://arxiv.org/pdf/2403.03218',
     'https://llm-attacks.org/':'https://arxiv.org/pdf/2307.15043',
     'https://openai.com/index/gpt-4-5-system-card':'https://cdn.openai.com/gpt-4-5-system-card-2272025.pdf'}
import json; json.dump(ALT,open('alt_urls.json','w'),indent=1)
for orig,new in ALT.items():
    k=hashlib.md5(orig.encode()).hexdigest()[:10]; b=f'h/{k}.bin'; t=f'h/{k}.txt'
    subprocess.run(['curl','-sL','--max-time','55','-A','Mozilla/5.0','-o',b,new],capture_output=True)
    if open(b,'rb').read(4)==b'%PDF': subprocess.run(['pdftotext','-q',b,t])
    else:
        d=open(b,encoding='utf-8',errors='ignore').read()
        d=re.sub(r'<(script|style)[^>]*>.*?</\1>','',d,flags=re.S|re.I)
        open(t,'w').write(H.unescape(re.sub(r'<[^>]+>',' ',d)))
    print(orig,'->',new,os.path.getsize(t))
