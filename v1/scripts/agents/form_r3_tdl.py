import numpy as np, soundfile as sf
from scipy.signal import correlate
D='/home/user/Listener/v1/data/t_dl_mirror/'
def ld(p):
    x,sr=sf.read(p); x=x.mean(1) if x.ndim>1 else x; return x,sr
mix,sr=ld(D+'audio/song.wav'); dr,_=ld(D+'stems_raw/htdemucs/song/drums.wav')
# end: 10 ms envelope last 3 s
def env(x,s0,s1,w=0.01):
    n=int(w*sr); seg=x[int(s0*sr):int(s1*sr)]; k=len(seg)//n
    return 20*np.log10(np.sqrt((seg[:k*n].reshape(k,n)**2).mean(1))+1e-12)
e=env(mix,len(mix)/sr-3,len(mix)/sr); t=len(mix)/sr-3+np.arange(len(e))*.01
a=np.where(e>-60)[0]; print('dur',len(mix)/sr,'last >-60',t[a[-1]],e[a[-1]],'last>-90',t[np.where(e>-90)[0][-1]])
# drum-stem envelope similarity hook1 vs hook4 (183 s gap), flux envelope, lag search for kick pattern
from scipy.signal import butter,sosfilt
sos=butter(4,[40,150],'bp',fs=sr,output='sos'); k=sosfilt(sos,dr)
hop=0.005; n=int(hop*sr); ke=np.abs(k[:len(k)//n*n]).reshape(-1,n).mean(1)
def seg(s,d): return ke[int(s/hop):int((s+d)/hop)]
A=seg(15,15)
for name,s0 in [('hook2',76),('hook3',137),('hook4',198)]:
    B=seg(s0-6,27)  # search window
    A0=A-A.mean(); best=None
    c=[]
    for i in range(len(B)-len(A)):
        b=B[i:i+len(A)]; c.append(np.corrcoef(A,b)[0,1])
    c=np.array(c); i=c.argmax(); print(name,'best offset s',(i*hop-6),'r',c[i], 'expected hook-start delta bars', )
