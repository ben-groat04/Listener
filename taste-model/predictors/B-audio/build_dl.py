"""usage: python3 build_dl.py WORKDIR   (WORKDIR/urls.json comes from `python3 ../B-audio2/build_features.py urls WORKDIR`)"""
import json,hashlib,subprocess,os,sys,numpy as np
W=sys.argv[1]; os.makedirs(W+"/audio",exist_ok=True)
from concurrent.futures import ThreadPoolExecutor
urls=json.load(open(W+"/urls.json"))
def key(u): return hashlib.md5(u.encode()).hexdigest()
def work(u):
    out=f"{W}/audio/{key(u)}.npy"
    if os.path.exists(out) or os.path.exists(out+".bad"): return
    try:
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
