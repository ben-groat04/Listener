import numpy as np, librosa, json
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
sr=22050
dr,_=librosa.load(D+'drums.wav',sr=sr,mono=True)
bs,_=librosa.load(D+'bass.wav',sr=sr,mono=True)
hop=128
def band(y,lo,hi):
    S=np.abs(librosa.stft(y,n_fft=1024,hop_length=hop))
    f=librosa.fft_frequencies(sr=sr,n_fft=1024)
    m=(f>=lo)&(f<hi)
    e=S[m].sum(0)
    o=np.maximum(0,np.diff(np.log1p(e*5)))
    return np.r_[0,o]
fr=sr/hop
ok=band(dr,40,120); om=band(dr,150,2500); oh=band(dr,6000,11000)
t=np.arange(len(ok))/fr
# fit grid: period P, phase p from broadband onsets 3..165 s
ob=ok+om+oh
sel=(t>3)&(t<165)
best=None
for P in np.arange(0.185,0.200,0.0001):
    for ph in np.arange(0,P,0.004):
        k=np.arange(ph,165,P)
        idx=(k*fr).astype(int)
        idx=idx[idx<len(ob)]
        # smoothed local max within +-1 frame
        sc=sum(ob[max(i-1,0):i+2].max() for i in idx if i>3*fr)
        if best is None or sc>best[0]: best=(sc,P,ph)
print('grid',best)
sc,P,ph=best
json.dump({'P':P,'ph':ph},open('/tmp/grid.json','w'))
