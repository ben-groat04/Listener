import librosa,numpy as np,json,scipy.signal as s
D='/home/user/Listener/v1/data/video2/'
sr=22050
dr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)[0]
sos=s.butter(4,[30,150],'band',fs=sr,output='sos'); k=s.sosfilt(sos,dr)
hop=64
env=librosa.onset.onset_strength(y=k,sr=sr,hop_length=hop)
fr=sr/hop
# phase of 0.5s grid per 20s window
for t0 in range(100,300,20):
    e=env[int(t0*fr):int((t0+20)*fr)]; t=np.arange(len(e))/fr
    best=None
    for P in np.arange(0.495,0.505,0.0005):
        z=(e*np.exp(2j*np.pi*t/P)).sum()
        if best is None or abs(z)>best[0]: best=(abs(z),P,np.angle(z)/(2*np.pi)*P)
    print(t0,'best period %.4f phase %.3f s (offset from window start)'%(best[1],best[2]%best[1]), 'abs',round(best[0]/e.sum(),2))
# stem rms drops
r=json.load(open(D+'stems/stem_rms_per_second.json'))
print(type(r), list(r)[:5] if isinstance(r,dict) else r[:2])
