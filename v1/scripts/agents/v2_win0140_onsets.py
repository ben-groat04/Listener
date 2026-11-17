import librosa,numpy as np,sys
D='stems_raw/htdemucs/song/'
for n in ['drums','bass','other']:
    y,sr=librosa.load(D+n+'.wav',sr=22050,offset=138,duration=24)
    o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+138
    print(n,len(o),np.round(o[:60],2).tolist() if n=='drums' else '')
y,sr=librosa.load('audio/song.wav',sr=22050,offset=140,duration=20)
S=np.abs(librosa.stft(y))**2;f=librosa.fft_frequencies(sr=sr)
for lo,hi in [(0,150),(150,500),(500,2000),(2000,6000),(6000,11000)]:
    e=S[(f>=lo)&(f<hi)].sum(0);print(lo,hi,[round(10*np.log10(e[i*43:(i+1)*43*5].mean()+1e-9),1) for i in range(0,4)])
print('centroid',[round(float(librosa.feature.spectral_centroid(y=y[i*sr*5:(i+1)*sr*5],sr=sr).mean())) for i in range(4)])
d,_=librosa.load(D+'drums.wav',sr=22050,offset=140,duration=20)
oe=librosa.onset.onset_strength(y=d,sr=sr);print('tempo',librosa.beat.tempo(onset_envelope=oe,sr=sr))
