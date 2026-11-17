import librosa,numpy as np
d,sr=librosa.load('stems_raw/htdemucs/song/drums.wav',sr=22050,offset=140,duration=20)
on=librosa.onset.onset_detect(y=d,sr=sr,units='time',backtrack=False)
print(len(on),np.round(on,2))
print('ioi median',np.median(np.diff(on)))
env=librosa.onset.onset_strength(y=d,sr=sr)
m,sr=librosa.load('audio/song.wav',sr=22050,offset=120,duration=60)
c=librosa.feature.spectral_centroid(y=m,sr=sr)[0]
t=librosa.times_like(c,sr=sr)+120
for a in range(120,180,10):print(a,round(c[(t>=a)&(t<a+10)].mean()))
b,sr=librosa.load('stems_raw/htdemucs/song/bass.wav',sr=22050,offset=140,duration=20)
f0=librosa.yin(b,fmin=30,fmax=200,sr=sr);print(np.round(librosa.hz_to_note(np.median(f0[:200])),0))
