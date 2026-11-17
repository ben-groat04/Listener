import numpy as np, librosa, soundfile as sf
D='/home/user/Listener/v1/data/t_cshells_cshore/'
y,sr=sf.read(D+'audio/song.wav'); print('shape',y.shape,sr,'peak',20*np.log10(np.abs(y).max()))
m=y.mean(1) if y.ndim>1 else y
d,_=sf.read(D+'stems_raw/htdemucs/song/drums.wav'); d=d.mean(1)
b,_=sf.read(D+'stems_raw/htdemucs/song/bass.wav'); b=b.mean(1)
def kick(t0,t1):
    s=librosa.resample(d[int(t0*sr):int(t1*sr)],orig_sr=sr,target_sr=4000)
    import scipy.signal as ss
    f=ss.butter(4,150,fs=4000,output='sos'); s=ss.sosfilt(f,s)
    o=librosa.onset.onset_detect(y=s,sr=4000,hop_length=40,units='time',backtrack=False)+t0
    i=np.diff(o); return o,i
for a,c in [(120,140),(160,180),(200,215),(260,280),(300,317)]:
    o,i=kick(a,c); g=0.488
    ph=((o-o[0])/g)%1; dev=np.minimum(ph,1-ph)*g
    print(a,c,'n',len(o),'medIOI %.3f'%np.median(i),'mean dev from 123bpm grid (ms) %.0f'%(dev.mean()*1000))
# bar self-similarity: chroma-free, use onset env autocorr at 4 beats (1.95s) & 8 beats
for a,c in [(125,145),(165,185),(265,285)]:
    s=m[int(a*sr):int(c*sr)]
    oe=librosa.onset.onset_strength(y=s,sr=sr,hop_length=512)
    ac=librosa.autocorrelate(oe-oe.mean()); ac/=ac[0]
    lag=lambda t:int(round(t*sr/512))
    print(a,'ac beat %.2f bar %.2f 2bar %.2f'%(ac[lag(.488)],ac[lag(1.952)],ac[lag(3.904)]))
# band share whole song / sections
S=np.abs(librosa.stft(m[int(120*sr):int(300*sr)],n_fft=4096))**2
f=librosa.fft_frequencies(sr=sr,n_fft=4096); t=S.sum()
for lo,hi in [(0,200),(200,2000),(2000,8000),(8000,16000),(16000,24000)]: print(lo,hi,'%.3f'%(S[(f>=lo)&(f<hi)].sum()/t))
# bass pitch
yb=b[int(160*sr):int(180*sr)]
p=librosa.yin(yb,fmin=30,fmax=300,sr=sr,frame_length=4096)
print('bass pitch median Hz',np.median(p),'hist',np.round(librosa.hz_to_midi(p[::10]))[:0])
mid=np.round(librosa.hz_to_midi(p)).astype(int)%12
print(np.bincount(mid,minlength=12))
import json
bt=np.array(json.load(open(D+'audio_features/beat_times.json')))
for a,c in [(120,140),(160,180),(200,215),(260,280),(300,317)]:
    o,i=kick(a,c)
    dev=np.array([np.abs(bt-x).min() for x in o]); print('trackergrid',a,'median dev ms %.0f'%(np.median(dev)*1000),'frac<40ms %.2f'%(dev<.04).mean())
