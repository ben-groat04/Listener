import numpy as np, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/stems_raw/htdemucs/song/'
sr=22050
def env(x,ms=10):
    h=int(sr*ms/1000); n=len(x)//h
    return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
ba=env(librosa.load(D+'bass.wav',sr=sr)[0]); dr=env(librosa.load(D+'drums.wav',sr=sr)[0])
secs=[('intro',0,10.4),('hook0',10.4,30.4),('verse1',30.4,71.3),('hook1',71.3,91.4),('verse2',91.4,132),('hook2',134,154),('verse3',154,195),('hook3',195.1,215.3)]
for n,a,b in secs:
    s=ba[int(a*100):int(b*100)]; d=dr[int(a*100):int(b*100)]
    print(n,a,b,'bars',round((b-a)/2.553,1),'bass on %',round(100*np.mean(s>-40),0),'drum median dB',round(np.median(d),1))
