import numpy as np, soundfile as sf, librosa
d='v1/data/video2/stems_raw/htdemucs/song/'
x,sr=sf.read(d+'vocals.wav'); x=x.mean(1) if x.ndim>1 else x
hop=256
e=librosa.feature.rms(y=x.astype(np.float32),frame_length=1024,hop_length=hop)[0]
db=20*np.log10(e+1e-9); t=np.arange(len(e))*hop/sr
# onsets: rise >8 dB over 50ms vs prior 100ms, level > -55
on=[]
for i in range(20,len(e)-5):
    if db[i+3]-db[i-8:i].min()>10 and db[i+3]>-55 and (not on or t[i]-on[-1]>0.25): on.append(t[i])
on=np.array(on)
L=88.61
for a,b in [(208,216),(216,276),(276,288),(288,300)]:
    o=on[(on>=a)&(on<b)]
    ph=((o-L)%2.0)
    cyc=((o-216.6)%12.0)
    print(a,b,'n',len(o),'bar-phase (s) median',np.round(np.median(ph),2) if len(o) else None,'frac within .15 of beat',np.round(np.mean(np.abs(((o-L)%0.5)-0.0)<0.12 )if len(o) else 0,2))
    print('  first 14 onsets',np.round(o[:14],2))
    print('  cycle-pos hist (12 s in 2 s bins)',np.histogram(cyc,bins=6,range=(0,12))[0])
    print('  bars after drop (int) hist mod 6',np.bincount(np.floor((o-L)/2).astype(int)%6,minlength=6))
