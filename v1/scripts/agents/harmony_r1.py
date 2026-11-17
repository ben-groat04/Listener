import librosa, numpy as np, json, sys
D='/home/user/Listener/v1/data/video1/'
nm=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
secs=[(1,8),(8,20),(20,40),(40,60),(60,75),(75,100),(100,116),(116,135),(135,160),(160,168),(168,188)]
for stem in ['other','bass']:
    y,sr=librosa.load(D+f'stems_raw/htdemucs/song/{stem}.wav',sr=22050)
    # use CQT chroma w/ tuning
    ch=librosa.feature.chroma_cqt(y=y,sr=sr,hop_length=2048,n_chroma=12,fmin=librosa.note_to_hz('C1') if stem=='bass' else None)
    t=librosa.frames_to_time(np.arange(ch.shape[1]),sr=sr,hop_length=2048)
    print(stem)
    for a,b in secs:
        m=(t>=a)&(t<b); v=ch[:,m].mean(1); v=v/v.max()
        print(f'{a//60}:{a%60:02d}-{b//60}:{b%60:02d}',' '.join(f'{nm[i]}={v[i]:.2f}' for i in np.argsort(-v)[:7]))
# bass pitch
y,sr=librosa.load(D+'stems_raw/htdemucs/song/bass.wav',sr=22050)
f0,vf,vp=librosa.pyin(y,fmin=30,fmax=200,sr=sr,hop_length=1024)
t=librosa.times_like(f0,sr=sr,hop_length=1024)
for a,b in [(3,20),(40,60),(60,75),(100,115),(120,135),(140,160),(170,188)]:
    m=(t>=a)&(t<b)&vf
    if m.sum()>5:
        mid=np.round(librosa.hz_to_midi(f0[m])).astype(int)
        u,c=np.unique(mid,return_counts=True); o=np.argsort(-c)[:5]
        print('bass',a,b,[(librosa.midi_to_note(u[i]),int(c[i])) for i in o])
