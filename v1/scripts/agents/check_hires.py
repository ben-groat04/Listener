import numpy as np, soundfile as sf, sys
D='/home/user/Listener/v1/data/video1/'
def load(p):
    x,sr=sf.read(p); 
    return (x.mean(1) if x.ndim>1 else x),sr
def rms_db(x,sr,t0,t1,hop=0.05,win=0.1):
    out=[]
    t=t0
    while t<t1:
        s=x[int(t*sr):int((t+win)*sr)]
        out.append((round(t,2),round(20*np.log10(np.sqrt(np.mean(s**2))+1e-9),1)))
        t+=hop
    return out
mix,sr=load(D+'audio/song.wav')
dr,_=load(D+'stems_raw/htdemucs/song/drums.wav')
print('sr',sr,len(mix)/sr)
print('MIX 2:46.5-2:49 ');print(rms_db(mix,sr,166.5,169,0.1))
print('DRUMS');print(rms_db(dr,sr,167.0,169,0.1))
print('END mix');print(rms_db(mix,sr,187.5,188.66,0.1))
print('END drums');print(rms_db(dr,sr,187.5,188.66,0.1))
