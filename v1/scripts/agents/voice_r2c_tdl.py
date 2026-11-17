import numpy as np, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
v,_=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=sr,mono=True)
f0,vf,_=librosa.pyin(v,fmin=80,fmax=700,sr=sr,hop_length=441)
st=np.where(vf,12*np.log2(f0/440),np.nan); tt=np.arange(len(f0))*0.02
def contour(s,l=18):
    i=int(s/0.02); return st[i:i+int(l/0.02)]
# hook starts (corrected): 
S={'h1':10.4,'h2':71.3,'h3':132.0,'h4':193.1}
def cc(a,b):
    m=~np.isnan(a)&~np.isnan(b); 
    return (np.corrcoef(a[m],b[m])[0,1], m.sum(), np.sqrt(np.mean((a[m]-b[m])**2)))
for p,q,lag in [('h1','h2',0.14),('h2','h3',0),('h3','h4',0),('h2','h4',0),('h1','h4',0)]:
    best=None
    for L in np.arange(-3,3.01,0.02):
        a=contour(S[p]); b=contour(S[q]+L)
        n=min(len(a),len(b)); r=cc(a[:n],b[:n])
        if r[1]>200 and (best is None or r[0]>best[0][0]): best=(r,L)
    print(p,q,'f0 contour r %.2f n=%d rms diff %.2f semitones at lag %.2f s'%(best[0][0],best[0][1],best[0][2],best[1]))
# waveform similarity: 1 s snippets from h2 vs h4 at env-lag, search +-80 ms
import scipy.signal as ss
def wf(p,q,L0):
    out=[]
    for off in [3,5,8,15]:
        a=v[int((S[p]+off)*sr):int((S[p]+off+1.0)*sr)]
        best=0
        for L in np.arange(L0-0.5,L0+0.5,0.002):
            i=int((S[q]+off+L)*sr); b=v[i:i+len(a)]
            if len(b)==len(a):
                r=np.corrcoef(a,b)[0,1]
                if abs(r)>abs(best): best=r
        out.append(round(best,2))
    return out
print('waveform r h1-h2',wf('h1','h2',0.14)); print('waveform r h2-h4',wf('h2','h4',0.0))
