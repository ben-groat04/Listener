import numpy as np, librosa, soundfile as sf
from scipy.signal import fftconvolve
P='/home/user/Listener/v1/data/t_birdwalk/'
v,sr=sf.read(P+'stems_raw/htdemucs/song/vocals.wav'); m=v.mean(1)
x=librosa.resample(m,orig_sr=sr,target_sr=16000); sr=16000
def corr(t0,lag,d=3.0):
    a=x[int(t0*sr):int((t0+d)*sr)]; b=x[int((t0+lag)*sr):int((t0+lag+d)*sr)]
    if len(b)<len(a): return float('nan')
    return float(np.corrcoef(a,b)[0,1])
def fine(t0,d,lag0,w=0.3):
    best=(-2,0)
    for l in np.arange(lag0-w,lag0+w,1/sr*16):
        c=corr(t0,l,d)
        if c>best[0]: best=(c,l)
    return best
# for each 3 s block of the track find best-matching earlier/later block (|lag|>5 s), report
res=[]
for t0 in np.arange(1,185,3.0):
    a=x[int(t0*sr):int((t0+3)*sr)]
    if np.sqrt(np.mean(a**2))<0.003: continue
    a=a-a.mean(); num=fftconvolve(x,a[::-1],'valid'); e=np.sqrt(fftconvolve(x**2,np.ones(len(a)),'valid')*np.sum(a**2))+1e-9
    c=num/e; idx=np.arange(len(c))/sr
    c[np.abs(idx-t0)<5]=-1
    i=np.argmax(c); res.append((t0,idx[i],c[i]))
for t0,t1,c in res: print(f'{int(t0)//60}:{t0%60:04.1f} <-> {int(t1)//60}:{t1%60:04.1f}  r={c:.2f} lag={t1-t0:+.2f}')
