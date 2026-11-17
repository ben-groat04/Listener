import librosa,numpy as np
d='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050
def ld(n): return librosa.load(d+n+'.wav',sr=sr,mono=True)[0]
o=ld('other'); v=ld('vocals')
# 1: band energy of other per 4s-cycle around transitions
S=np.abs(librosa.stft(o,n_fft=2048,hop_length=512))**2
f=librosa.fft_frequencies(sr=sr,n_fft=2048); t=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr,hop_length=512)
def band(a,b,t0,t1):
    m=(f>=a)&(f<b); k=(t>=t0)&(t<t1); return 10*np.log10(S[m][:,k].sum(0).mean()+1e-12)
print('other bands per 6s: 250-1k,1-2k,2-4k,4-8k  (harmonic ratio of upper/lower)')
for t0 in [2*60+24,2*60+30,2*60+36.8,2*60+42,2*60+48.8,2*60+54,3*60+0.8,3*60+12.8,3*60+24.8,3*60+30,3*60+36.8,3*60+48.8,4*60+24,4*60+30,4*60+36.8,4*60+42]:
    print(f'{int(t0//60)}:{t0%60:04.1f}',[round(band(a,b,t0,t0+6),1) for a,b in [(250,1000),(1000,2000),(2000,4000),(4000,8000)]])
# upper partial scaling: ratio 4-8k to 250-1k per 2s from 3:00 to 4:50
print('tilt (4-8k minus 250-1k) per 4s')
for t0 in range(150,300,8):
    print(f'{t0//60}:{t0%60:02d}',round(band(4000,8000,t0,t0+4)-band(250,1000,t0,t0+4),1),end=' | ')
print()
# 2: onset lead: vocals vs other at 4:40-4:59
def ons(x,t0,t1):
    e=librosa.onset.onset_strength(y=x[int(t0*sr):int(t1*sr)],sr=sr,hop_length=256)
    return e
t0,t1=280,299
ev=ons(v,t0,t1); eo=ons(o,t0,t1)
n=min(len(ev),len(eo)); ev=ev[:n]-ev[:n].mean(); eo=eo[:n]-eo[:n].mean()
hop=256/sr
lags=range(-20,21)
cc=[np.dot(ev[max(0,l):n+min(0,l)],eo[max(0,-l):n-max(0,l)])/np.sqrt((ev**2).sum()*(eo**2).sum()) for l in lags]
i=int(np.argmax(cc)); print('xcorr vocal vs other peak lag ms (positive = other earlier than vocal? see sign)',round(list(lags)[i]*hop*1000),round(max(cc),2),'zero-lag',round(cc[20],2))
# 3: 4:37 step: broadband per-second drop for other, mix
for t0 in [4*60+34,4*60+36,4*60+37,4*60+38]:
    print('other bands at',t0,[round(band(a,b,t0,t0+1),1) for a,b in [(60,250),(250,1000),(1000,4000),(4000,8000)]])
