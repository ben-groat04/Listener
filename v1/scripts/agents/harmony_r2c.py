import librosa, numpy as np
D='/home/user/Listener/v1/data/video1/'
yo,sr=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=22050)
f0,vf,vp=librosa.pyin(yo,fmin=80,fmax=700,sr=sr,hop_length=512)
tt=librosa.times_like(f0,sr=sr,hop_length=512)
def seq(a,b,step=0.5):
    out=[]
    x=a
    while x<b:
        m=(tt>=x)&(tt<x+step)&vf
        out.append(librosa.hz_to_note(np.median(f0[m])) if m.sum()>=4 else '.')
        x+=step
    return ' '.join(out)
print('1:15-1:40 per 0.5 s:',seq(75,100))
print('2:50-3:08 per 0.5 s:',seq(170,188))
# chroma per 2s in 2:00-2:40
nm=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
C=np.abs(librosa.cqt(yo,sr=sr,hop_length=2048,fmin=librosa.note_to_hz('C2'),n_bins=180,bins_per_octave=36))
t=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=2048)
pc=np.zeros((12,C.shape[1]))
for s in range(60): pc[s%12]+=(C[3*s:3*s+3]**2).sum(0)
for a in range(120,160,3):
    m=(t>=a)&(t<a+3); v=pc[:,m].mean(1); v/=v.max()
    print(f'{a//60}:{a%60:02d}',' '.join(f'{nm[i]}={v[i]:.2f}' for i in np.argsort(-v)[:5]))
