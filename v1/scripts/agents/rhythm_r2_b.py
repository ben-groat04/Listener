import numpy as np, soundfile as sf, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
x,sr0=sf.read(D+'audio/song.wav'); print('native sr',sr0,x.shape,'peak dBFS',round(20*np.log10(abs(x).max()),2),'n>=0.999',int((abs(x)>=0.999).sum()))
m=x if x.ndim==1 else x.mean(1)
a=int(177.3*sr0); s=m[a:a+int(0.3*sr0)]; print('177.3-177.6 native peak',round(20*np.log10(abs(s).max()),2),'n>=0.999',int((abs(s)>=0.999).sum()))
cl=np.where(abs(m)>=0.999)[0]/sr0; print('clipped-sample times (s) clusters:',np.round(np.unique(np.round(cl,1)),1)[:40])
sr=22050
S=D+'stems_raw/htdemucs/song/'
dr,_=librosa.load(S+'drums.wav',sr=sr); vo,_=librosa.load(S+'vocals.wav',sr=sr)
def env(x,ms=10):
    h=int(sr*ms/1000); n=len(x)//h
    return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
# drum-onset (broadband, spectral flux) times for sync of vocal edges: nearest drum onset
oe=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=64)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=64,units='time',backtrack=False)
print('drum onsets',len(on),'median ioi',np.median(np.diff(on)))
ve=env(vo)
# clean vocal gate edges: falls of >=25 dB within 0.15 s to below -45 dB, and rises back
fall=[];rise=[]
for i in range(15,len(ve)-15):
    if ve[i-10:i-3].mean()>-32 and ve[i+3:i+8].mean()<-45 and ve[i-1]-ve[i+4]>15: fall.append(i/100)
    if ve[i-8:i-3].mean()<-45 and ve[i+3:i+10].mean()>-32 and ve[i+4]-ve[i-1]>15: rise.append(i/100)
def dedupe(l):
    o=[]
    for v in l:
        if not o or v-o[-1]>0.3: o.append(v)
    return o
fall=dedupe(fall); rise=dedupe(rise)
g=60/94/4
def nearest(v):
    j=np.argmin(abs(on-v)); return on[j]-v
print('falls',len(fall),'rises',len(rise))
print('fall -> nearest drum onset (ms)',[round(nearest(v)*1000) for v in fall][:40])
print('rise -> nearest drum onset (ms)',[round(nearest(v)*1000) for v in rise][:40])
# random expectation: median |dev| for random times
rng=np.random.default_rng(0); r=rng.uniform(30,215,500); print('random median |nearest| ms',round(np.median([abs(nearest(v)) for v in r])*1000))
print('median |nearest| falls',round(np.median([abs(nearest(v)) for v in fall])*1000),'rises',round(np.median([abs(nearest(v)) for v in rise])*1000))
# gap durations between a fall and next rise, in bars/16ths
fs=[f for f in fall if 30<f<215]
gaps=[]
for f in fs:
    nx=[r_ for r_ in rise if r_>f]
    if nx and nx[0]-f<3: gaps.append((round(f,2),round(nx[0]-f,2),round((nx[0]-f)/g,1)))
print('gaps (fall, dur s, dur in 16ths):',gaps)
# gap starts relative to each other in beats (0.6383)
print('fall times mod bar 2.553 for the gaps list:',[round(((f-fs[0])%2.553)/g,1) for f,_,_ in gaps])
