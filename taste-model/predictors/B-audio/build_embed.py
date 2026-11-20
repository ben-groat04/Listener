import numpy as np, os, json, hashlib, time, torch, librosa, pickle
torch.set_num_threads(1)
from transformers import ClapModel, ClapProcessor
m=ClapModel.from_pretrained("laion/clap-htsat-unfused").eval(); p=ClapProcessor.from_pretrained("laion/clap-htsat-unfused")
urls=json.load(open("order.json")); key=lambda u: hashlib.md5(u.encode()).hexdigest()
out={}; 
if os.path.exists("emb.pkl"): out=pickle.load(open("emb.pkl","rb"))
def save(): pickle.dump(out,open("emb.tmp","wb")); os.replace("emb.tmp","emb.pkl")
pending=[u for u in urls if u not in out]; n=0
while pending:
    nxt=[]
    for u in pending:
        f=f"audio/{key(u)}.npy"
        if os.path.exists(f+".bad"): out[u]=None; continue
        if not os.path.exists(f): nxt.append(u); continue
        a=np.load(f).astype(np.float32)/32768
        s=len(a)//2; a=a[max(0,s-160000):s+160000]
        a=librosa.resample(a,orig_sr=32000,target_sr=48000)
        x=p(audio=[a],sampling_rate=48000,return_tensors="pt")
        with torch.no_grad(): e=m.audio_model(**x).pooler_output[0].numpy()
        out[u]=e.astype(np.float32); n+=1
        if n%200==0: save(); print(n,flush=True)
    pending=nxt
    if pending: time.sleep(10)
save(); print("done")
