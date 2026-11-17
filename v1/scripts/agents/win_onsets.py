import sys,json,numpy as np,librosa
d='stems_raw/htdemucs/song/'
t0,t1=float(sys.argv[1]),float(sys.argv[2])
for n in ['drums','bass','vocals','other']:
    y,sr=librosa.load(d+n+'.wav',sr=22050,offset=t0,duration=t1-t0)
    on=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+t0
    print(n,'onsets',np.round(on,2).tolist())
    if n=='drums':
        e=librosa.onset.onset_strength(y=y,sr=sr);o=librosa.onset.onset_detect(onset_envelope=e,sr=sr,units='time')+t0
        print('IOI',np.round(np.diff(o),2).tolist())
        c=librosa.feature.spectral_centroid(y=y,sr=sr)[0];print('drum centroid mean',c.mean())
y,sr=librosa.load('audio/song.wav',sr=None,mono=False)
print(sr,y.shape,'peak dBFS 0-20',20*np.log10(np.abs(y[:,:int(20*sr)]).max()),'full',20*np.log10(np.abs(y).max()))
m=y.mean(0)
from scipy.signal import welch
f,P=welch(m[:int(20*sr)],sr,nperseg=8192)
tot=P.sum()
for lo,hi in [(0,200),(200,2000),(2000,8000),(8000,12000),(12000,16000),(16000,22000)]:
    print(lo,hi,round(10*np.log10(P[(f>=lo)&(f<hi)].sum()/tot),1))
