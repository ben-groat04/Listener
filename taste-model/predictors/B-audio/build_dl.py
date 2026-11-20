import json,hashlib,subprocess,os,sys,urllib.request,numpy as np
from concurrent.futures import ThreadPoolExecutor
urls=json.load(open("order.json"))
def key(u): return hashlib.md5(u.encode()).hexdigest()
def work(u):
    out=f"audio/{key(u)}.npy"
    if os.path.exists(out) or os.path.exists(out+".bad"): return
    try:
        raw=subprocess.run(["curl","-s","-m","30","--fail","-x","","$u"],capture_output=True) if False else None
        import requests
        r=requests.get(u,timeout=30); r.raise_for_status()
        p=subprocess.run(["ffmpeg","-v","quiet","-i","pipe:0","-t","30","-ac","1","-ar","32000","-f","s16le","pipe:1"],input=r.content,capture_output=True,timeout=60)
        a=np.frombuffer(p.stdout,dtype=np.int16)
        if len(a)<32000*5: raise Exception("short")
        np.save(out,a)
    except Exception as e:
        open(out+".bad","w").write(str(e)[:100])
with ThreadPoolExecutor(6) as ex: list(ex.map(work,urls))
print("done")
