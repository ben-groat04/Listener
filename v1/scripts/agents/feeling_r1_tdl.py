import numpy as np, soundfile as sf, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
def env(p,hop=0.1):
    x,sr=sf.read(p); x=x.mean(1) if x.ndim>1 else x
    n=int(hop*sr); m=len(x)//n
    return 20*np.log10(np.sqrt((x[:m*n].reshape(m,n)**2).mean(1))+1e-9),sr,x
S={k:env(D+f'stems_raw/htdemucs/song/{k}.wav')[0] for k in ['vocals','drums','bass','other']}
mix,sr,x=env(D+'audio/song.wav')
def row(t0,t1):
    a,b=int(t0*10),int(t1*10)
    return ' '.join(f"{k}:{v[a:b].mean():.1f}" for k,v in S.items())+f" mix:{mix[a:b].mean():.1f}"
for t0,t1 in [(0,10),(10.4,30),(30,36),(36.3,43),(43,70),(71.3,91),(91.4,130),(134,154),(155,193),(196,203),(195.1,215),(215.4,218.9),(219,229),(229,236),(236,238)]:
    print(t0,t1,row(t0,t1))
# step at 3:15.09 and 0:10.4 and 3:35.3
for t in [10.4,195.09,215.3,218.9,229.2,229.3]:
    a=int(t*10); print(t,'mix before/after',mix[a-3:a].mean().round(1),mix[a:a+3].mean().round(1))
print('mono diff',np.abs(sf.read(D+'audio/song.wav')[0][:,0]-sf.read(D+'audio/song.wav')[0][:,1]).max() if sf.read(D+'audio/song.wav')[0].ndim>1 else 'mono')
# end 10ms
x2,sr=sf.read(D+'audio/song.wav'); x2=x2.mean(1) if x2.ndim>1 else x2
n=int(sr*0.01); seg=x2[-3*sr:]; m=len(seg)//n
e=20*np.log10(np.sqrt((seg[:m*n].reshape(m,n)**2).mean(1))+1e-9)
idx=np.where(e>-60)[0]; print('sr',sr,'dur',len(x2)/sr,'last >-60 at',len(x2)/sr-3+idx[-1]*0.01, e[idx[-1]])
print('peak',np.abs(x2).max(), 'rms',20*np.log10(np.sqrt((x2**2).mean())))
