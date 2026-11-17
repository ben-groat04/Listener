import librosa,numpy as np,json
y,sr=librosa.load('stems_raw/htdemucs/song/drums.wav',sr=22050,offset=60,duration=20)
o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)
print(len(o)); 
for a,b in [(0,5),(5,10),(10,15),(15,20)]: print(a+60,sum(1 for t in o if a<=t<b))
d=np.diff(o);print(np.round(np.median(d),3))
S=np.abs(librosa.stft(y));f=librosa.fft_frequencies(sr=sr)
for a,b in [(0,5),(5,15),(15,20)]:
    s=S[:,int(a*sr/512):int(b*sr/512)].mean(1);print(a+60,'hi-hat band >6k share',round(s[f>6000].sum()/s.sum(),3))
y2,sr=librosa.load('stems_raw/htdemucs/song/other.wav',sr=22050,offset=60,duration=20)
for a,b in [(0,15),(15,18),(18,20)]:
    seg=y2[int(a*sr):int(b*sr)];c=librosa.feature.spectral_centroid(y=seg,sr=sr).mean();print('other centroid',a+60,round(c))
