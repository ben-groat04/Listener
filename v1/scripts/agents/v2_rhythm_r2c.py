import librosa,numpy as np,collections
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050;hop=512;ph=0.1333;P=0.49995
y=librosa.load(D+'other.wav',sr=sr,mono=True)[0]+librosa.load(D+'bass.wav',sr=sr,mono=True)[0]
ch=librosa.feature.chroma_cqt(y=y,sr=sr,hop_length=hop)
f=sr/hop
# novelty over 1.0s smoothing: compare mean chroma of 1s before vs 1s after each frame
w=int(1.0*f);nov=np.zeros(ch.shape[1])
for i in range(w,ch.shape[1]-w):
    a=ch[:,i-w:i].mean(1);b=ch[:,i:i+w].mean(1)
    nov[i]=1-np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-9)
for (t0,t1) in [(30,64),(64,88),(277,300)]:
    seg=nov[int(t0*f):int(t1*f)];thr=np.percentile(seg,90)
    pk=[i for i in range(1,len(seg)-1) if seg[i]>thr and seg[i]==seg[max(0,i-15):i+15].max()]
    out=[]
    for i in pk:
        t=t0+i/f;b=(t-ph)/P;out.append((round(t,2),round(b%8,2)))
    print(t0,t1,out)
