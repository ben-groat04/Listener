import numpy as np, librosa, json
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def load(n): return librosa.load(D+n+'.wav',sr=22050,mono=True)[0]
oth=load('other'); bas=load('bass')
sr=22050
for nm,y in [('other',oth)]:
    ch=librosa.feature.chroma_cqt(y=y,sr=sr,hop_length=2048)
    t=librosa.frames_to_time(np.arange(ch.shape[1]),sr=sr,hop_length=2048)
    print(nm,'chroma per 20s (normalised to D=1)')
    print('      '+' '.join(f'{n:>4}' for n in names))
    for s in range(0,189,20):
        m=(t>=s)&(t<s+20)
        if m.sum()==0: continue
        v=ch[:,m].mean(1); v=v/v[2]
        print(f'{s//60}:{s%60:02d}  '+' '.join(f'{x:4.2f}' for x in v))
# bass pitch per 6s-bursts: pyin
f0,vf,vp=librosa.pyin(bas,fmin=30,fmax=200,sr=sr,hop_length=1024)
t=librosa.frames_to_time(np.arange(len(f0)),sr=sr,hop_length=1024)
print('bass median pitch per 10s (voiced only)')
for s in range(0,189,10):
    m=(t>=s)&(t<s+10)&~np.isnan(f0)
    if m.sum()>5:
        h=np.round(librosa.hz_to_midi(f0[m])).astype(int)
        u,c=np.unique(h,return_counts=True); o=np.argsort(-c)[:3]
        print(f'{s//60}:{s%60:02d}',[(librosa.midi_to_note(u[i]),int(c[i])) for i in o])
