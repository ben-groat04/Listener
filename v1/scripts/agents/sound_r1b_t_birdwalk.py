import numpy as np, soundfile as sf, scipy.signal as ss
D='data/t_birdwalk/'
x,sr=sf.read(D+'audio/song.wav'); m=x.mean(1)
fr,P=ss.welch(m,sr,nperseg=8192); Pd=10*np.log10(P+1e-20)
for a in [3000,4000,4500,5000,5250,5500,5750,6000,6250,6500,7000,8000,10000,12000,16000,20000]:
    i=np.searchsorted(fr,a); print(a, round(Pd[i-2:i+3].mean(),1))
# ending
env=lambda s: np.sqrt(np.convolve(s**2,np.ones(int(.01*sr))/int(.01*sr),'same'))
N=len(m); seg=slice(N-int(3*sr),N)
e=env(m)[seg]; t=np.arange(len(e))/sr+(N-int(3*sr))/sr
print('end level last 3s per 0.25s dBFS:',[round(20*np.log10(e[int(k*.25*sr):int((k+1)*.25*sr)].mean()+1e-9),1) for k in range(12)])
print('last sample abs>1e-4 at', (np.where(np.abs(m)>1e-4)[0].max())/sr, 'dur',N/sr)
print('last 0.5s dBFS 10ms:',[round(20*np.log10(v+1e-9),0) for v in e[-50::5]])
S='data/t_birdwalk/stems_raw/htdemucs/song/'
for n in ['vocals','drums','bass','other']:
    s,_=sf.read(S+n+'.wav'); s=s.mean(1); ee=env(s)[seg]
    print(n,'last 3s 0.5s means',[round(20*np.log10(ee[int(k*.5*sr):int((k+1)*.5*sr)].mean()+1e-9),1) for k in range(6)])
    pk=ss.find_peaks(ee,height=ee.max()*0.5,distance=int(.1*sr))[0]; print('  peaks>half-max',[(round(t[p],2),round(20*np.log10(ee[p]),1)) for p in pk][:12])
# fade last-sound times mix at various thresholds
E=env(m); 
for th in [-40,-50,-60,-70,-80,-90]:
    idx=np.where(20*np.log10(E+1e-12)>th)[0].max(); print(th,'dBFS last above at',round(idx/sr,2))
# dither/noise floor in first 0.3s
print('first 0.1s rms dB',20*np.log10(np.sqrt((m[:4410]**2).mean())+1e-12))
# stem bandwidth
for n in ['vocals','drums','bass','other']:
    s,_=sf.read(S+n+'.wav'); s=s.mean(1)
    f2,P2=ss.welch(s,sr,nperseg=4096); c=np.cumsum(P2)/P2.sum(); P2d=10*np.log10(P2+1e-20)
    print(n,'r99.9',f2[np.searchsorted(c,.999)],'psd 3k %.0f 5k %.0f 6k %.0f 8k %.0f 12k %.0f'%tuple(P2d[np.searchsorted(f2,a)] for a in [3000,5000,6000,8000,12000]))
