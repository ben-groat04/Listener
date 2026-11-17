import numpy as np, librosa
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
m,sr=librosa.load(D+'vocals.wav',sr=22050,mono=True)
hop=220
M=librosa.power_to_db(librosa.feature.melspectrogram(y=m,sr=sr,n_fft=1024,hop_length=hop,n_mels=48,fmax=6000))
fps=sr/hop
db=M.max(0)
def seg(a,b): return M[:,int(a*fps):int(b*fps)]
def ncc(A,B):
    n=min(A.shape[1],B.shape[1]);A=A[:,:n]-A[:,:n].mean();B=B[:,:n]-B[:,:n].mean()
    return float((A*B).sum()/np.sqrt((A**2).sum()*(B**2).sum()))
# exact repeat test: for a reference 3.2 s segment, best ncc against shifts over whole track (step 0.01)
def best(a,L=3.2,rng=(1,166)):
    R=seg(a,a+L);res=[]
    for s in np.arange(rng[0],rng[1]-L,0.02):
        if abs(s-a)<0.3: continue
        res.append((ncc(R,seg(s,s+L)),s))
    res.sort(reverse=True);return res[:3]
for a in [60.3,63.5,70.5,76.8,100,130,142.0,152.0,25.0,30.0,35.0]:
    print(a,[(round(x,2),round(s,2)) for x,s in best(a)])
# control: ncc of random pairs
rs=np.random.RandomState(0);c=[ncc(seg(a,a+3.2),seg(b,b+3.2)) for a,b in rs.uniform(1,160,(300,2))]
print('random pair ncc mean/95pct',np.mean(c),np.percentile(c,95))
