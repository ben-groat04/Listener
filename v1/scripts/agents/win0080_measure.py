import librosa,numpy as np,sys
d='/home/user/Listener/v1/data/t_cshells_cshore/'
t0,t1=80,100
y,sr=librosa.load(d+'audio/song.wav',sr=22050,offset=t0-1,duration=t1-t0+2,mono=True)
print('mix sample peak dBFS',20*np.log10(np.abs(y).max()))
dr,_=librosa.load(d+'stems_raw/htdemucs/song/drums.wav',sr=22050,offset=t0-1,duration=t1-t0+2)
on=librosa.onset.onset_detect(y=dr,sr=sr,units='time',backtrack=False)+t0-1
lo=librosa.effects.preemphasis(dr)
# kick: lowpass band onset
import scipy.signal as s
b,a=s.butter(4,150/(sr/2));k=s.filtfilt(b,a,dr)
ke=librosa.onset.onset_strength(y=k,sr=sr)
kt=librosa.onset.onset_detect(onset_envelope=ke,sr=sr,units='time')+t0-1
print('kick',np.round(kt,2));print('IOI',np.round(np.diff(kt),2))
print('drum onsets',np.round(on,2))
for n in['bass','other','vocals','drums']:
    z,_=librosa.load(d+f'stems_raw/htdemucs/song/{n}.wav',sr=22050,offset=t0,duration=20)
    r=librosa.feature.rms(y=z,frame_length=2205,hop_length=1102)[0]
    db=20*np.log10(r+1e-9)
    print(n,'rms per 0.5s',np.round(db[::1][:40:1],0)[:40].tolist())
