import librosa, numpy as np, json
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
b,sr=librosa.load(D+'bass.wav',sr=22050)
hop=1024
cb=librosa.feature.chroma_cqt(y=b,sr=sr,hop_length=hop,fmin=librosa.note_to_hz('C1'),n_octaves=4)
t=np.arange(cb.shape[1])*hop/sr
# smoothed argmax at 0.5 s
res=[]
for t0 in np.arange(0,305,0.5):
    m=(t>=t0)&(t<t0+0.5); v=cb[:,m].mean(1); res.append((t0,names[v.argmax()],v.max()/v.sum()))
# run-length of roots
runs=[];
for t0,n,p in res:
    if runs and runs[-1][2]==n: runs[-1][1]=t0+0.5
    else: runs.append([t0,t0+0.5,n])
f=lambda x:'%d:%04.1f'%(x//60,x%60)
print(' '.join(f'{f(a)}{n}' for a,e,n in runs if e-a>=2 and a>=24))
# bass level
r=json.load(open('/home/user/Listener/v1/data/video2/stems/stem_rms_per_second.json'))
print(type(r), list(r.keys())[:6] if isinstance(r,dict) else r[:2])
