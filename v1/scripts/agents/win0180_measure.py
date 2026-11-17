import numpy as np, librosa, soundfile as sf, json
d='/home/user/Listener/v1/data/t_birdwalk/'
def env(p,t0,t1):
    y,sr=sf.read(p);
    if y.ndim>1: y=y.mean(1)
    a=y[int(t0*sr):int(t1*sr)];h=int(.01*sr)
    n=len(a)//h; e=np.array([np.sqrt((a[i*h:(i+1)*h]**2).mean()) for i in range(n)])
    return 20*np.log10(e+1e-9),sr,y
mix,sr,y=env(d+'audio/song.wav',0,200)
print('dur',len(y)/sr,'samplepeak dBFS',20*np.log10(np.abs(sf.read(d+'audio/song.wav')[0]).max()))
yy=sf.read(d+'audio/song.wav')[0]
for a,b in [(0,60),(60,120),(120,188.2),(180,188.2)]:
    print('peak',a,b,20*np.log10(np.abs(yy[int(a*sr):int(b*sr)]).max()))
base='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
for nm in ['song','drums','bass','other','vocals']:
    p=d+'audio/song.wav' if nm=='song' else base+nm+'.wav'
    e,sr,y=env(p,185,188.15)
    print(nm,'last3s 10ms env dB, per 0.25s max:',[round(e[i:i+25].max(),0) for i in range(0,len(e),25)])
    idx=[i for i in range(1,len(e)-1) if e[i]>e[i-1] and e[i]>=e[i+1] and e[i]>e.max()-25]
    print(' peaks',[(round(185+i*.01,2),round(e[i],1)) for i in idx])
    # last time above -60
    for thr in (-50,-60,-70):
        ii=np.where(e>thr)[0]; print(' last>',thr, round(185+ii[-1]*.01,2) if len(ii) else None)
