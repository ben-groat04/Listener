import numpy as np, soundfile as sf, scipy.signal as ss, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
x,sr=sf.read(D+'audio/song.wav'); print('sr',sr,x.shape, x.shape[1] if x.ndim>1 else 1)
L,R=(x[:,0],x[:,1]) if x.ndim>1 else (x,x)
m=(L+R)/2
print('peak dBFS',20*np.log10(np.abs(x).max()),'n>=0.999',(np.abs(x)>=0.999).sum(), 'n==max',(np.abs(x)==np.abs(x).max()).sum())
d=np.nonzero(L!=R)[0]; print('LR differ',len(d), d.min()/sr if len(d) else None, d.max()/sr if len(d) else None)
print('whole RMS dBFS',20*np.log10(np.sqrt((m**2).mean())))
# long-term spectrum
f,P=ss.welch(m,sr,nperseg=8192)
Pd=10*np.log10(P+1e-20)
for fr in [1000,2000,4000,6000,7000,7500,8000,8500,9000,9500,10000,12000,16000,20000]:
    i=np.argmin(abs(f-fr)); print(fr,round(Pd[i],1))
# per-30s band-limit
# cliff location
band=np.array([Pd[(f>=a)&(f<a+250)].mean() for a in range(6000,12000,250)])
for a,b in zip(range(6000,12000,250),band): print(a,round(b,1),end=' | ')
print()
# loudness curve per 10 s: RMS, peak
for t in range(0,240,10):
    s=m[t*sr:(t+10)*sr]
    if len(s)==0: continue
    print(t,'rms',round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1),'peak',round(20*np.log10(abs(s).max()+1e-9),1),'crest',round(20*np.log10(abs(s).max()/np.sqrt((s**2).mean()+1e-12)),1))
# ending
env=lambda y: np.sqrt(np.convolve(y**2,np.ones(int(.01*sr))/int(.01*sr),'same'))
tail=m[-int(4*sr):]; e=env(tail); db=20*np.log10(e+1e-9)
t0=len(m)/sr-4
nz=np.nonzero(np.abs(tail)>0)[0]; print('last nonzero sample t',t0+nz.max()/sr, 'dur',len(m)/sr)
above=np.nonzero(db>-60)[0]; print('last >-60 dB env',t0+above.max()/sr, db[above.max()])
for T in [-3,-2.5,-2,-1,0]: pass
# stems ending
for s in ['vocals','drums','bass','other']:
    y,_=sf.read(D+f'stems_raw/htdemucs/song/{s}.wav'); y=y.mean(1) if y.ndim>1 else y
    tl=y[-int(4*sr):]; dbs=20*np.log10(env(tl)+1e-9); a=np.nonzero(dbs>-60)[0]
    print(s,'last>-60',t0+a.max()/sr if len(a) else None)
# DC/ end peaks in last 3.5s
seg=m[int(236*sr):int(240*sr)]; ee=20*np.log10(env(seg)+1e-9)
pk,_=ss.find_peaks(ee,height=-70,distance=10,prominence=3)
print('peaks 236-240',[(round(236+p/sr,2),round(ee[p],1)) for p in pk][:20])
