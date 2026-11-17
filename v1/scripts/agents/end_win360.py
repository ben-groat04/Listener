import soundfile as sf, numpy as np, json
from scipy.signal import find_peaks
base='.'
files={'mix':'audio/song.wav','vocals':'stems_raw/htdemucs/song/vocals.wav','drums':'stems_raw/htdemucs/song/drums.wav','bass':'stems_raw/htdemucs/song/bass.wav','other':'stems_raw/htdemucs/song/other.wav'}
for k,f in files.items():
    x,sr=sf.read(f); d=len(x)/sr
    m=x.mean(1) if x.ndim>1 else x
    h=int(sr*0.01); n=len(m)//h
    env=np.sqrt((m[:n*h].reshape(n,h)**2).mean(1))+1e-12
    db=20*np.log10(env)
    t0=int((d-3)/0.01) if False else max(0,n-300)
    seg=db[t0:]
    print(k,'dur',round(d,3),'sr',sr,'samplepeak dBFS',round(20*np.log10(np.abs(x).max()),2))
    if k=='mix':
        # 10ms env, print every 100ms last 3s
        for i in range(t0,n,10): print(' t=%.2f %.1f'%(i*0.01,db[i]))
        pk,_=find_peaks(db[t0:],prominence=6); print(' peaks(prom6dB) at',[round((t0+p)*0.01,2) for p in pk],[round(db[t0+p],1) for p in pk])
        aud=np.where(db>-60)[0]; print(' last >-60dB',(aud[-1]+1)*0.01, 'last >-80',(np.where(db>-80)[0][-1]+1)*0.01)
        print(' last 50ms level',db[-5:])
    else:
        pk,_=find_peaks(db[t0:],prominence=6); print(' peaks',[round((t0+p)*0.01,2) for p in pk],' last>-60',(np.where(db>-60)[0][-1]+1)*0.01 if (db>-60).any() else None,'max',round(seg.max(),1),'level last 50ms',round(db[-5:].mean(),1),'level 357-358',round(db[int(357/0.01):int(358/0.01)].mean(),1))
