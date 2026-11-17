import numpy as np,librosa
D='/home/user/Listener/v1/data/t_birdwalk/audio/song.wav'
y,sr=librosa.load(D,sr=22050,mono=True)
H=128
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=H)
t=librosa.times_like(oe,sr=sr,hop_length=H)
for a,b in [(12.5,47),(60,83),(94,119),(132,143),(157,188),(165,183),(62,80),(0,12),(47.5,59.5),(2*60+36,2*60+60)]:
    m=(t>=a)&(t<b); x=oe[m]-oe[m].mean()
    best=[]
    for p in np.arange(0.34,0.43,0.001):
        # eighth-note comb
        ph=(t[m]%(p/2))/(p/2); sc=np.abs((x*np.exp(2j*np.pi*ph)).sum())
        ph2=(t[m]%p)/p; sc2=np.abs((x*np.exp(2j*np.pi*ph2)).sum())
        best.append((sc+sc2,p))
    best.sort(reverse=True)
    print(a,b,'best period',[round(p,4) for _,p in best[:3]],'bpm',round(60/best[0][1],1))
