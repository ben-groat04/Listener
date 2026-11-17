import numpy as np, soundfile as sf, librosa
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
x,sr=sf.read(D+'other.wav');x=x.mean(1).astype(np.float32)
names='C C# D D# E F F# G G# A A# B'.split()
def ch(t0,t1):
    s=x[int(t0*sr):int(t1*sr)]
    c=librosa.feature.chroma_cqt(y=s,sr=sr,hop_length=2048,fmin=librosa.note_to_hz('C2')).mean(1)
    c=c/c[2];return ' '.join(f'{n}:{v:.2f}' for n,v in zip(names,c) if v>0.45)
for a,b in [(70,74),(75.6,77),(77.2,78.6),(78.7,80.5),(80.5,84),(84,87),(88,92),(2*60+13,2*60+16.1),(136.2,139.3),(139.3,142.4),(142.4,145.5),(145.5,148.6),(148.6,151.7),(151.7,154.8),(190-30,166),(170,180)]:
    print(a,b,ch(a,b))
# onset of other at start
y=np.abs(x[:int(3*sr)])
for t in np.arange(0,2.0,0.1):
    s=x[int(t*sr):int((t+0.1)*sr)];print(round(t,1),round(20*np.log10(np.sqrt(np.mean(s**2))+1e-9),1),end=' | ')
print()
# sub 42.6Hz
b,sr2=sf.read(D+'bass.wav');b=b.mean(1)
import scipy.signal as ss
for a,c in [(119,122),(125,128),(131,134),(137,140)]:
    s=b[int(a*sr2):int(c*sr2)]; f,P=ss.welch(s,sr2,nperseg=sr2*2);m=(f>25)&(f<120);print(a,c,f[m][np.argmax(P[m])])
