import numpy as np, librosa, json, sys
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050
def ld(p,a=290,b=330): 
    y,_=librosa.load(p,sr=sr,mono=False,offset=a,duration=b-a); return y
mix=ld(D+'audio/song.wav'); 
S={k:ld(D+f'stems_raw/htdemucs/song/{k}.wav') for k in ['drums','bass','vocals','other']}
m=mix.mean(0)
print('sample peak 300-320 dBFS',20*np.log10(np.abs(mix[:,10*sr:30*sr]).max()))
# whole song peak
yf,_=librosa.load(D+'audio/song.wav',sr=None,mono=False); print('song peak',20*np.log10(np.abs(yf).max()), 'sr',_)
# drums onsets / kick
d=S['drums'].mean(0)
from scipy.signal import butter,sosfilt
lo=sosfilt(butter(4,[40,120],'bp',fs=sr,output='sos'),d)
env=librosa.onset.onset_strength(y=lo,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=256,units='time',backtrack=False)+290
on=on[(on>=300)&(on<320)]
print('kick onsets',np.round(on,2)); print('IOI',np.round(np.diff(on),2))
# full onset
env2=librosa.onset.onset_strength(y=d,sr=sr,hop_length=256)
on2=librosa.onset.onset_detect(onset_envelope=env2,sr=sr,hop_length=256,units='time')+290
on2=on2[(on2>=300)&(on2<320)];print('drum onsets',len(on2),np.round(on2,2))
t,b=librosa.beat.beat_track(y=d,sr=sr); print('tempo drums',t)
tempo=librosa.feature.rhythm.tempo(onset_envelope=env2,sr=sr,hop_length=256,aggregate=None)
print('tempo curve',np.round(tempo[::100],1))
bt=json.load(open(D+'audio_features/beat_times.json'));print(str(bt)[:100])
# bands
import scipy.signal as sg
f,tt,Z=sg.stft(m,fs=sr,nperseg=2048)
P=np.abs(Z)**2
def band(lo,hi): i=(f>=lo)&(f<hi); return 10*np.log10(P[i].sum(0)+1e-12)
for a,bb in [(290,300),(300,310),(310,320),(320,330)]:
    sel=(tt+290>=a)&(tt+290<bb)
    print(a,[round(float(band(l,h)[sel].mean()),1) for l,h in [(20,80),(80,250),(250,800),(800,3000),(3000,6000),(6000,11000)]])
# 10ms env of other stem and bass in 300-320 per second
for k in ['drums','bass','other']:
    y=S[k].mean(0); e=np.sqrt(np.convolve(y**2,np.ones(int(.01*sr))/int(.01*sr),'same'))
    print(k,[round(20*np.log10(e[int((s-290)*sr):int((s+1-290)*sr)].mean()+1e-9),1) for s in range(300,320)])
# drum envelope broadband hf >8k present? 
for a in [300,305,310,314,317,318,319]:
    s=int((a-290)*sr);seg=S['drums'].mean(0)[s:s+sr]
    ff,pp=sg.welch(seg,fs=sr,nperseg=2048);print(a,'drums hf>6k dB',round(10*np.log10(pp[ff>6000].sum()+1e-12),1),'lf<150',round(10*np.log10(pp[ff<150].sum()+1e-12),1))
