import numpy as np, soundfile as sf, json, scipy.signal as ss, librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/'
x,sr=sf.read(D+'audio/song.wav'); print('shape',x.shape,sr)
if x.ndim==1: x=np.stack([x,x],1)
m=x.mean(1); L,R=x[:,0],x[:,1]
print('peak',np.abs(x).max(), 20*np.log10(np.abs(x).max()+1e-12))
# true peak 4x oversample
tp=0
for s in range(0,len(m),sr*30):
    seg=x[s:s+sr*30]; o=ss.resample_poly(seg,4,1,axis=0); tp=max(tp,np.abs(o).max())
print('true peak',tp,20*np.log10(tp))
print('samples >=0.999',(np.abs(x)>=0.999).sum(), ' >=0.99',(np.abs(x)>=0.99).sum())
# first/last nonzero
nz=np.nonzero(np.abs(x).max(1)>0)[0]; print('first nz',nz[0]/sr,'last nz',nz[-1]/sr, 'dur',len(m)/sr)
# loudness by 10s: RMS, peak, crest, S/M, corr
print('t  rms  peak crest S/M(dB) corr')
for t in range(0,360,10):
    s=x[t*sr:(t+10)*sr]
    if len(s)==0: break
    r=np.sqrt((s**2).mean()); p=np.abs(s).max()
    M=(s[:,0]+s[:,1])/2;S=(s[:,0]-s[:,1])/2
    sm=10*np.log10((S**2).mean()/((M**2).mean()+1e-20)+1e-20)
    c=np.corrcoef(s[:,0],s[:,1])[0,1] if r>0 else 0
    print(t,round(20*np.log10(r+1e-12),1),round(20*np.log10(p+1e-12),1),round(20*np.log10(p/(r+1e-12)),1),round(sm,1),round(c,3))
# loudness percentile of 1s rms in 60-340
rm=[20*np.log10(np.sqrt((m[i*sr:(i+1)*sr]**2).mean())+1e-12) for i in range(60,340)]
print('1s RMS 60-340 p5,p50,p95',np.percentile(rm,[5,50,95]))
# bands full-mix by section
def bands(seg):
    f,P=ss.welch(seg,sr,nperseg=8192); tot=P.sum()
    ed=[0,60,200,800,3000,8000,12000,16000,22050]
    return [round(100*P[(f>=a)&(f<b)].sum()/tot,1) for a,b in zip(ed[:-1],ed[1:])]
print('bands % [0-60,60-200,200-800,0.8-3k,3-8k,8-12k,12-16k,16-22k]')
for a,b in [(12,20),(25,30),(40,43),(65,100),(120,160),(200,220),(240,260),(300,318),(330,338),(338,342.8)]:
    print(a,b,bands(m[a*sr:b*sr]))
# 16k lowpass check: full song HF
f,P=ss.welch(m[60*sr:340*sr],sr,nperseg=8192)
for k in [10000,14000,16000,18000,20000,21000]:
    i=np.argmin(abs(f-k)); print(k,round(10*np.log10(P[i]+1e-30),1))
