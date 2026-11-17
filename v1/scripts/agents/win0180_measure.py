import numpy as np, soundfile as sf, librosa, json
D='/home/user/Listener/v1/data/t_birdwalk/'
def load(p):
    y,sr=sf.read(p); 
    return y,sr
names={'mix':D+'audio/song.wav'}
for s in ['vocals','drums','bass','other']: names[s]=D+f'stems_raw/htdemucs/song/{s}.wav'
sig={}
for k,p in names.items():
    y,sr=load(p); sig[k]=y
print('sr',sr,'dur',len(sig['mix'])/sr)
def env(y,sr,hop=0.01):
    m=y.mean(1) if y.ndim>1 else y
    n=int(sr*hop); k=len(m)//n
    r=np.sqrt((m[:k*n].reshape(k,n)**2).mean(1)); return 20*np.log10(r+1e-9)
mix=sig['mix']; print('peak abs',np.abs(mix).max(),20*np.log10(np.abs(mix).max()), 'peak 180-188:',20*np.log10(np.abs(mix[180*sr:]).max()))
E={k:env(v,sr) for k,v in sig.items()}
# 100ms mean per stem over 176..188.2 in 0.5 s steps
print('t   '+'  '.join(f'{k:>7}' for k in E))
for t in np.arange(176,188.2,0.5):
    a=int(t*100); b=a+50
    print(f'{t:6.1f} '+'  '.join(f'{10*np.log10(np.mean(10**(E[k][a:b]/10))):7.1f}' for k in E))
# end: last 3 s
print('END')
n=len(E['mix']); 
for k in E:
    e=E[k][-300:]
    last=np.where(e>-60)[0]
    print(k,'last >-60dB at', (n-300+last[-1])/100 if len(last) else None,'level final 100ms',e[-10:].mean(), 'min', e.min())
e=E['mix'][-300:]
print('mix last 3s every 100ms',np.round(e.reshape(30,10).mean(1),1))
# peaks in 10ms envelope last 3 s
from scipy.signal import find_peaks
for k in ['mix','drums','bass','other']:
    e=E[k][-300:]; pk,_=find_peaks(e,prominence=3)
    print(k,'peaks t',[(round((n-300+i)/100,2),round(e[i],1)) for i in pk])
# onsets in drums stem 180-188
d=sig['drums'].mean(1)
oenv=librosa.onset.onset_strength(y=d,sr=sr,hop_length=441)
on=librosa.onset.onset_detect(onset_envelope=oenv,sr=sr,hop_length=441,units='time',backtrack=False)
on=on[(on>=179)]
print('drum onsets',np.round(on,2))
lo=librosa.effects.preemphasis(d)  
from scipy.signal import butter,sosfilt
sos=butter(4,150,'low',fs=sr,output='sos'); dl=sosfilt(sos,d)
oe=librosa.onset.onset_strength(y=dl,sr=sr,hop_length=441)
ko=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=441,units='time'); ko=ko[ko>=176]
print('kick onsets',np.round(ko,2)); print('IOI',np.round(np.diff(ko),2))
# stereo width & centroid
def width(a,b):
    s=mix[int(a*sr):int(b*sr)]; M=(s[:,0]+s[:,1])/2; S=(s[:,0]-s[:,1])/2
    return 10*np.log10((S**2).mean()/(M**2).mean()+1e-12)
def cen(a,b):
    s=mix[int(a*sr):int(b*sr)].mean(1); return librosa.feature.spectral_centroid(y=s,sr=sr).mean(), librosa.feature.spectral_rolloff(y=s,sr=sr,roll_percent=.95).mean()
for a,b in [(176,180),(180,182),(182,184),(184,186),(186,188.15)]:
    print(a,b,'width dB',round(width(a,b),1),'centroid/rolloff',[round(x) for x in cen(a,b)])
# band energy: share above 8k / 4k per segment
for a,b in [(170,176),(176,180),(180,182),(182,185),(185,188.15)]:
    s=mix[int(a*sr):int(b*sr)].mean(1); S=np.abs(np.fft.rfft(s))**2; f=np.fft.rfftfreq(len(s),1/sr)
    print(a,b,'frac<150',round(S[f<150].sum()/S.sum(),3),'>4k',round(S[f>4000].sum()/S.sum(),4),'>8k',round(S[f>8000].sum()/S.sum(),5))
# pitch of vocals 176-181
v=sig['vocals'].mean(1)[int(176*sr):int(181*sr)]
f0,vf,vp=librosa.pyin(v,fmin=60,fmax=900,sr=sr,frame_length=2048)
t=librosa.times_like(f0,sr=sr,hop_length=512)+176
for tt,ff in zip(t[::6],f0[::6]):
    if not np.isnan(ff): print(round(tt,2),round(ff))
# bass f0
b=sig['bass'].mean(1)[int(176*sr):int(186*sr)]
f0,vf,vp=librosa.pyin(b,fmin=30,fmax=200,sr=sr,frame_length=4096)
print('bass f0 median',np.nanmedian(f0), np.nanpercentile(f0,[10,90]))
