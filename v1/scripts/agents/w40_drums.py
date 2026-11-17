import librosa,numpy as np,json
d='stems_raw/htdemucs/song/'
y,sr=librosa.load(d+'drums.wav',sr=22050,offset=40,duration=20,mono=True)
o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)
print('drum onsets',len(o),np.round(o,2).tolist())
S=np.abs(librosa.stft(y))**2;f=librosa.fft_frequencies(sr=sr)
for lo,hi in[(30,150),(150,500),(500,3000),(3000,11000)]:
    print(lo,hi,[round(10*np.log10(S[(f>=lo)&(f<hi)][:,i*43:(i+1)*43*5].sum()+1e-12),1) for i in range(0,4)])
y2,sr=librosa.load('audio/song.wav',sr=22050,offset=40,duration=20)
print('centroid per5s',[round(float(librosa.feature.spectral_centroid(y=y2[i*5*sr:(i+1)*5*sr],sr=sr).mean())) for i in range(4)])
b,_=librosa.load(d+'bass.wav',sr=22050,offset=40,duration=20)
print('bass rms 2s',[round(float(np.sqrt((b[i*2*sr:(i+1)*2*sr]**2).mean())),3) for i in range(10)])
