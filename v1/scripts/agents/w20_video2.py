import librosa,numpy as np
d='stems_raw/htdemucs/song/'
y,sr=librosa.load(d+'drums.wav',sr=22050,offset=18,duration=24)
o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+18
print('drum onsets',np.round(o,2))
if len(o)>8:
    m=o[(o>28)&(o<40)]; print('IOI median',np.median(np.diff(m)))
b,sr=librosa.load(d+'bass.wav',sr=22050,offset=26,duration=14)
f=librosa.yin(b,fmin=30,fmax=250,sr=sr);t=librosa.times_like(f,sr=sr)+26
for a in range(26,40,1):
    s=(t>=a)&(t<a+1); print(a,round(float(np.median(f[s])),1),'Hz')
x,sr=librosa.load('audio/song.wav',sr=22050,offset=18,duration=24)
S=np.abs(librosa.stft(x));fr=librosa.fft_frequencies(sr=sr)
for a,bb in[(0,150),(150,500),(500,2000),(2000,6000),(6000,11000)]:
    e=S[(fr>=a)&(fr<bb)].sum(0);tt=librosa.times_like(e,sr=sr)+18
    print(a,bb,[round(float(20*np.log10(e[(tt>=u)&(tt<u+4)].mean()+1e-9)),1) for u in (18,22,26,30,34,38)])
