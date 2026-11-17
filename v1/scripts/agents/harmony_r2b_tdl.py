import numpy as np, librosa
d='stems_raw/htdemucs/song/'; sr=22050
N=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def load(n): return librosa.load(d+n+'.wav',sr=sr,mono=True)[0]
oth=load('other'); bas=load('bass')
def tl(y,t0,t1,step=0.63,fmin='C2',oct=5):
    out=[]
    t=t0
    while t<t1:
        s=y[int(t*sr):int((t+step)*sr)]
        c=librosa.feature.chroma_cqt(y=s,sr=sr,tuning=0.13,n_octaves=oct,fmin=librosa.note_to_hz(fmin)).mean(1)
        top=np.argsort(-c)[:3]
        out.append(f'{int(t//60)}:{t%60:05.2f} '+' '.join(f'{N[i]}{c[i]/c.max():.2f}' for i in top))
        t+=step
    return out
import sys
for a,b in [(16,23),(24.8,31),(198.5,204),(207.5,213)]:
    print('--- other',a,b); print('\n'.join(tl(oth,a,b)))
    print('--- bass'); print('\n'.join(tl(bas,a,b,fmin='C1',oct=4)))
