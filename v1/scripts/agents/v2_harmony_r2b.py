import librosa,numpy as np
from scipy.ndimage import median_filter
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050;hop=512
bass=librosa.load(D+'bass.wav',sr=sr)[0]
C=librosa.feature.chroma_cqt(y=bass,sr=sr,hop_length=hop,fmin=32.7,n_octaves=4)
t=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=hop)
r=median_filter(C.argmax(0),size=43)
ch=[t[i] for i in range(1,len(r)) if r[i]!=r[i-1] and 28<t[i]<285]
oe=librosa.onset.onset_strength(y=bass,sr=sr,hop_length=256);ot=librosa.frames_to_time(np.arange(len(oe)),sr=sr,hop_length=256)
sn=[]
for T in ch:
    m=(ot>T-0.6)&(ot<T+0.6);sn.append(ot[m][oe[m].argmax()])
sn=np.unique(np.round(sn,2))
def circ(x,P):
    z=np.exp(2j*np.pi*(x-0.14)/P).mean();return (np.angle(z)%(2*np.pi))/(2*np.pi)*P,abs(z)
for a,b in [(28,88),(88.6,157),(157,285)]:
    x=sn[(sn>=a)&(sn<b)]
    print(a,b,len(x),'beat(0.5) phase %.3f R=%.2f | bar(2.0) phase %.3f R=%.2f'%(*circ(x,0.5),*circ(x,2.0)))
