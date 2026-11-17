import numpy as np, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/'
v,sr=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=22050,mono=True)
d,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050,mono=True)
import scipy.signal as ss
b,a=ss.butter(4,[35/11025,130/11025],'band'); k=ss.filtfilt(b,a,d)
kon=librosa.onset.onset_detect(y=k,sr=sr,hop_length=64,units='time')
starts=[10.4,71.3,132.0,193.1]
hop=221
for h,s in enumerate(starts):
    seg=(kon>s)&(kon<s+20.4)
    ko=kon[seg]
    # hook syllable onsets (onset strength of vocal stem, hop 64 = 2.9ms)
    vo=librosa.onset.onset_detect(y=v,sr=sr,hop_length=64,units='time',backtrack=False)
    vo=vo[(vo>s)&(vo<s+20.4)]
    # beat grids from kick fit within hook
    for name,bpm,div in [('8th@94.0',94.0,2),('16th@94.0',94.0,4),('8th@94.5',94.5,2)]:
        st=60/bpm/div
        ph=2*np.pi*(ko%st)/st; phi=np.angle(np.exp(1j*ph).mean())*st/(2*np.pi); Rk=abs(np.exp(1j*ph).mean())
        r=((vo-phi+st/2)%st)-st/2
        Rv=abs(np.exp(1j*2*np.pi*r/st).mean())
        rng=np.random.default_rng(1)
        Rr=np.mean([abs(np.exp(1j*2*np.pi*rng.uniform(0,st,len(vo))/st).mean()) for _ in range(500)])
        print(f'hook{h+1} {name} nvo={len(vo)} nkick={len(ko)} Rkick={Rk:.2f} Rvoice={Rv:.2f} Rrand={Rr:.2f} off_ms={1000*np.mean(r):.0f} rate/s={len(vo)/20.4:.2f}')
    if h in (1,2,3):
        print(' onsets line1 (first 3.3-5.0 s after start):',[round(x-s,2) for x in vo if 3.3<x-s<5.5])
# first-syllable onsets of hook line starts, across hooks, offset from hook start
for h,s in enumerate(starts):
    vo=librosa.onset.onset_detect(y=v,sr=sr,hop_length=64,units='time')
    for lo,hi in [(0.9,2.5),(3.6,5.2),(13.3,15.0)]:
        x=[round(t-s,2) for t in vo if lo<t-s<hi]
        print('hook',h+1,(lo,hi),x[:8])
# pitch at step starts: median f0 in 1s before/after, hooks 3 and 4 and hook1/2 step starts = hook start +5.7..6.0 and +15.4
f0,vf,_=librosa.pyin(v,fmin=120,fmax=700,sr=sr,hop_length=221,frame_length=2048)
t=np.arange(len(f0))*0.01
for h,s in enumerate(starts):
    for off in (5.7,15.6):
        for lo,hi,l in [(off-1.5,off-0.3,'before'),(off-0.3,off+0.9,'around'),(off+0.9,off+2.1,'after')]:
            m=(t>s+lo)&(t<s+hi)&~np.isnan(f0)
            if m.sum()>5: print(f'hook{h+1} step@+{off} {l}: median F0 {np.median(f0[m]):.0f} Hz n={m.sum()}')
