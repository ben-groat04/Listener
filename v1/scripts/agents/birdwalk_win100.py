import numpy as np, librosa, sys
D='/home/user/Listener/v1/data/t_birdwalk/'
S={}
for n in ['vocals','drums','bass','other']:
    y,sr=librosa.load(D+f'stems_raw/htdemucs/song/{n}.wav',sr=22050,mono=True); S[n]=y
mix,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=True)
hop=int(sr*0.01)
def env(y): return librosa.feature.rms(y=y,frame_length=hop*2,hop_length=hop)[0]
def db(x): return 20*np.log10(x+1e-9)
# per-stem dB per 1s in 112..124 plus 10ms around 118-120.5
for t0 in [98,100,101,103,105,112,114,117,118,119,120]:
    print(t0,{k:round(float(db(np.sqrt(np.mean(v[int(t0*sr):int((t0+1)*sr)]**2)))),1) for k,v in dict(mix=mix,**S).items()})
# bass dropout finer, 0.25s
for k in ['bass','drums','vocals','other']:
    e=db(env(S[k])); print(k,[round(float(e[int(t*100):int((t+.25)*100)].mean()),0) for t in np.arange(100,106,.5)])
# kick onsets in window from drums stem low band
d=librosa.effects.preemphasis(S['drums'])
import scipy.signal as ss
b,a=ss.butter(4,[40/ (sr/2),150/(sr/2)],'band'); lo=ss.filtfilt(b,a,S['drums'])
oe=librosa.onset.onset_strength(y=lo,sr=sr,hop_length=hop)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=hop,units='time',backtrack=False)
k=on[(on>=100)&(on<120)]; print('kicks',len(k),np.round(k,2)); ioi=np.diff(k); print('ioi med',np.median(ioi),np.round(ioi,2))
bt=np.array(__import__('json').load(open(D+'audio_features/beat_times.json')) if True else [])
print(type(bt),bt.shape if hasattr(bt,'shape') else '')
