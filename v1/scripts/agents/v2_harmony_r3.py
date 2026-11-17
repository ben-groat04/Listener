import numpy as np, librosa
D='data/video2/stems_raw/htdemucs/song/'
b,sr=librosa.load(D+'bass.wav',sr=22050,mono=True)
o,_=librosa.load(D+'other.wav',sr=22050,mono=True)
d,_=librosa.load(D+'drums.wav',sr=22050,mono=True)
def rms(x,t0,t1):
    s=x[int(t0*sr):int(t1*sr)]; return 20*np.log10(np.sqrt((s**2).mean())+1e-9)
# 1 pickup character: bass level 0.1s frames around pickups
for name,ts in [('A->D',[75.4,95.7,108.1,124.1,136.1,152.1]),('E->B',[168.1,180.1,192.1,204.1,216.1,276.1])]:
    print(name)
    for t in ts:
        env=[rms(b,t+k*0.1,t+k*0.1+0.1) for k in range(-3,12)]
        f0=librosa.pyin(b[int((t-0.3)*sr):int((t+1.4)*sr)],fmin=30,fmax=120,sr=sr,frame_length=4096)[0]
        f=np.round(f0[~np.isnan(f0)][::4],0)
        print(f"{t:6.1f}",np.round(env,0).astype(int).tolist(),f.tolist()[:14])
# 2 G# in bass/other 4:29-4:49 chroma
for nm,x in [('bass',b),('other',o)]:
    for t0,t1 in [(250,258),(269,276),(276,284),(284,289)]:
        c=librosa.feature.chroma_cqt(y=x[int(t0*sr):int(t1*sr)],sr=sr).mean(1); c/=c.max()
        pc='C C# D D# E F F# G G# A A# B'.split()
        print(nm,t0,t1,{pc[i]:round(float(c[i]),2) for i in np.argsort(-c)[:6]},'G#',round(float(c[8]),2),'G',round(float(c[7]),2))
