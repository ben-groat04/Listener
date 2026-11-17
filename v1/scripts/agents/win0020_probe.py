import librosa,numpy as np
d='/home/user/Listener/v1/data/video2/'
y,sr=librosa.load(d+'audio/song.wav',sr=22050,offset=18,duration=24)
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
ch=librosa.feature.chroma_cqt(y=y,sr=sr)
for a,b in [(18,26),(26,32),(32,36.5),(36.5,42)]:
    i=int((a-18)*sr/512);j=int((b-18)*sr/512);m=ch[:,i:j].mean(1)
    print(a,b,[(names[k],round(float(m[k]),2)) for k in np.argsort(-m)[:4]])
for stem in ['drums','bass']:
    s,_=librosa.load(d+f'stems_raw/htdemucs/song/{stem}.wav',sr=22050,offset=18,duration=24)
    o=librosa.onset.onset_detect(y=s,sr=sr,units='time',backtrack=False)
    print(stem,[round(float(t+18),2) for t in o])
cent=librosa.feature.spectral_centroid(y=y,sr=sr)[0]
for a,b in [(18,28),(28,40)]:
    print('centroid',a,b,cent[int((a-18)*sr/512):int((b-18)*sr/512)].mean())
b=np.array(__import__('json').load(open(d+'audio_features/beat_times.json')));print(np.diff(b).mean(), 60/np.diff(b).mean())
