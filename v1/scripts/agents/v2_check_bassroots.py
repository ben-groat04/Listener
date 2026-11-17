import librosa,numpy as np
y,sr=librosa.load('/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/bass.wav',sr=22050,mono=True)
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def root(a,b):
    seg=y[int(a*sr):int(b*sr)]
    if len(seg)<sr or np.sqrt((seg**2).mean())<1e-3: return '-'
    f=librosa.yin(seg,fmin=30,fmax=200,sr=sr)
    m=librosa.hz_to_midi(f[np.isfinite(f)])
    import collections
    c=collections.Counter([names[int(round(x))%12] for x in m])
    return ' '.join(f"{k}{v*100//len(m)}" for k,v in c.most_common(2))
import sys
t0=float(sys.argv[1]);t1=float(sys.argv[2]);step=float(sys.argv[3]) if len(sys.argv)>3 else 4
t=t0
while t<t1:
    print(f"{int(t//60)}:{t%60:05.2f}",root(t+0.3,t+step-0.3)); t+=step
