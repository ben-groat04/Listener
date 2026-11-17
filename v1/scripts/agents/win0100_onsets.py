import librosa,numpy as np
y,sr=librosa.load('stems_raw/htdemucs/song/drums.wav',sr=22050,offset=100,duration=22)
o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)
print(len(o)); 
for a in range(0,22,2): print(a+100, ((o>=a)&(o<a+2)).sum())
print(np.round(np.diff(o[(o>2)&(o<8)]),2))
