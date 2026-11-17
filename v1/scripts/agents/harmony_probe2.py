import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'bass.wav',sr=22050,mono=True)
def peak(a,b):
    seg=y[int(a*sr):int(b*sr)]
    S=np.abs(np.fft.rfft(seg*np.hanning(len(seg)),n=2**18)); f=np.fft.rfftfreq(2**18,1/sr)
    m=(f>25)&(f<300); i=np.argsort(-S[m])[:3]; fs=f[m][i]
    return [(round(x,1),librosa.hz_to_note(x)) for x in fs]
for a,b in [(4,7),(10,13),(20,28),(30,38),(50,56),(62,70),(100,108),(122,124),(128,130),(134,136),(145,147),(152,154),(159,161),(165,175),(180,188)]:
    print(f'{a//60}:{a%60:02d}-{b//60}:{b%60:02d}',peak(a,b))
# 2:00-2:40 the Dm hold vs bass: other chroma at bass bursts
o,_=librosa.load(D+'other.wav',sr=22050,mono=True)
ch=librosa.feature.chroma_cqt(y=o,sr=sr,hop_length=2048); t=librosa.frames_to_time(np.arange(ch.shape[1]),sr=sr,hop_length=2048)
names='C C# D D# E F F# G G# A A# B'.split()
for a,b in [(121.2,122.9),(127.2,129),(133.4,135),(140,141.3),(125,127)]:
    m=(t>=a)&(t<b); v=ch[:,m].mean(1); print(a,[names[i] for i in np.argsort(-v)[:4]], np.round(np.sort(v)[::-1][:4]/v.max(),2))
