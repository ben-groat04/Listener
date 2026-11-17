import numpy as np,librosa
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
sr=22050;H=128
y,_=librosa.load(D+'drums.wav',sr=sr,mono=True)
S=np.abs(librosa.stft(y,n_fft=2048,hop_length=H)); f=librosa.fft_frequencies(sr=sr,n_fft=2048)
t=librosa.times_like(S[0],sr=sr,hop_length=H)
bands={'kick':(30,150),'snare':(150,2500),'hat':(5000,10000)}
E={}
for k,(a,b) in bands.items():
    x=S[(f>=a)&(f<b)].sum(0); d=np.maximum(np.diff(np.log1p(x*5),prepend=0),0)
    E[k]=d
tot=sum(E.values())
def best_period(a,b,lo=0.385,hi=0.405):
    m=(t>=a)&(t<b);best=None
    for p in np.arange(lo,hi,0.0005):
        # comb at p/2 (eighths), fold
        ph=(t[m]%p)/p
        sc=np.abs((tot[m]*np.exp(2j*np.pi*ph*2)).sum())
        if best is None or sc>best[0]: best=(sc,p)
    return best[1]
def fold(a,b,p,nb=4,sub=4):
    m=(t>=a)&(t<b); bar=p*nb
    ph=(t[m]%bar)/bar
    out={}
    for k in E:
        h,_=np.histogram(ph,bins=nb*sub,weights=E[k][m]); out[k]=h
    return out
secs=[(12.9,47),(60,83),(94,119),(132,143),(157,188),(50,59.5)]
for a,b in secs:
    p=best_period(a,b)
    o=fold(a,b,p)
    print(f'--- {a}-{b} period {p:.4f}s = {60/p:.1f} bpm')
    for k,h in o.items():
        h=h/h.max()
        # rotate so kick max at 0
        print(k,' '.join(f'{int(v*9)}' for v in h))
