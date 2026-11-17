import numpy as np, librosa, soundfile as sf
from scipy.signal import fftconvolve
P='/home/user/Listener/v1/data/t_birdwalk/'
v,sr=sf.read(P+'stems_raw/htdemucs/song/vocals.wav'); m=v.mean(1)
m16=librosa.resample(m,orig_sr=sr,target_sr=16000); sr=16000
# envelope-based+waveform: normalised xcorr of a segment against whole track
def xc(t0,d=2.5):
    a=m16[int(t0*sr):int((t0+d)*sr)]; a=a-a.mean()
    num=fftconvolve(m16,a[::-1],'valid')
    e=np.sqrt(fftconvolve(m16**2,np.ones(len(a)),'valid')*np.sum(a**2))+1e-9
    c=num/e; out=[]
    for _ in range(3):
        i=np.argmax(np.abs(c)); out.append((round(float(c[i]),2),round(i/sr,2)))
        c[max(0,i-sr):i+sr]=0
    return out
for t in [1.2,24.0,26.0,30.0,41,47.5,50,53,62,65,125,137,142,150,160,163]:
    print(t,xc(t))
# self-match including near: lag test of 0:24-0:47 chant
for t in [25,30,36]:
    a=m16[int(t*sr):int((t+2)*sr)]
