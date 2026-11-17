import librosa,numpy as np,json
y,sr=librosa.load('stems_raw/htdemucs/song/drums.wav',sr=22050,offset=78,duration=24)
o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+78
print(np.round(o,2))
d=np.diff(o[o>88.5]);print(np.round(d,2),np.median(d))
for n in ['bass','other']:
    y,sr=librosa.load(f'stems_raw/htdemucs/song/{n}.wav',sr=22050,offset=88,duration=14)
    c=librosa.feature.spectral_centroid(y=y,sr=sr).mean();print(n,'centroid',c)
b=json.load(open('audio_features/beat_times.json'));b=b if isinstance(b,list) else b.get('beats',b)
b=np.array(b);b=b[(b>80)&(b<100)];print(np.round(b,2),np.median(np.diff(b)))
c=json.load(open('music_views/clap_tags.json'))
for w in c['windows']:
    if 80<=w['t']<=100: print(w['t'],w['genre'][:2],w['instrument'][:2],w['mood'][:2],w['voice'][:2],w['sound'][:2])
