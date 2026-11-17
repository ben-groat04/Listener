import librosa,numpy as np
for s in ['drums','other','bass']:
    y,sr=librosa.load(f'stems_raw/htdemucs/song/{s}.wav',sr=22050,offset=0,duration=20)
    o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)
    print(s,len(o),np.round(o[:40],2))
y,sr=librosa.load('stems_raw/htdemucs/song/drums.wav',sr=22050,duration=20)
S=np.abs(librosa.stft(y));f=librosa.fft_frequencies(sr=sr)
for a,b in [(0,150),(150,2000),(2000,11000)]:
    e=S[(f>=a)&(f<b)].mean(0);print(a,b,[round(float(20*np.log10(e[i*43:(i+1)*43].mean()+1e-9)),1) for i in range(0,20,5)])
