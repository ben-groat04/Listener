import numpy as np,soundfile as sf,librosa,sys
x,sr=sf.read('audio/song.wav'); print(sr,x.shape)
m=x.mean(1) if x.ndim>1 else x
nz=np.where(np.abs(x if x.ndim==1 else x).max(axis=-1)>0)[0] if x.ndim>1 else np.where(x!=0)[0]
print('last nonzero sample t=',nz[-1]/sr,'abs val',np.abs(x[nz[-1]]).max())
print('exact zeros after:',(np.abs(x[nz[-1]+1:])==0).all(), 'len s',(len(x)-nz[-1]-1)/sr)
print('last 3s max abs',np.abs(x[-3*sr:]).max())
print('global peak',np.abs(x).max(), 'at',np.abs(x).max(axis=-1).argmax()/sr if x.ndim>1 else np.abs(x).argmax()/sr)
# 10ms envelope 340-343 peak picking
h=int(.01*sr); a=int(339*sr); seg=m[a:int(343*sr)]; k=len(seg)//h
env=np.sqrt((seg[:k*h].reshape(k,h)**2).mean(1)); db=20*np.log10(env+1e-9)
from scipy.signal import find_peaks
pk,_=find_peaks(db,prominence=4); print('10ms peaks (prom>4dB):',[(round(339+i*.01,2),round(db[i],1)) for i in pk][:40])
for lo,hi in [(338,339),(339,340),(340,341),(341,342),(342,342.8)]:
    s=m[int(lo*sr):int(hi*sr)]
    S=np.abs(librosa.stft(s,n_fft=2048))
    f=librosa.fft_frequencies(sr=sr,n_fft=2048)
    cen=(S.mean(1)*f).sum()/S.mean(1).sum()
    P=S.mean(1)**2; tot=P.sum()
    bands=[(0,200),(200,1000),(1000,4000),(4000,10000),(10000,sr/2)]
    print(lo,hi,'centroid',round(cen),'rolloff95',round(f[np.searchsorted(np.cumsum(P)/tot,.95)]),'band share %',[round(100*P[(f>=a_)&(f<b_)].sum()/tot,1) for a_,b_ in bands])
# stereo width / L-R
if x.ndim>1:
    for lo,hi in [(330,335),(338,342.8)]:
        s=x[int(lo*sr):int(hi*sr)]; M=s.sum(1)/2;S_=(s[:,0]-s[:,1])/2
        print(lo,hi,'rmsM',20*np.log10(np.sqrt((M**2).mean())+1e-9),'rmsS',20*np.log10(np.sqrt((S_**2).mean())+1e-9))
# last audible 50ms fade check
print('last 30ms samples',x[nz[-1]-5:nz[-1]+3])
# per-second dB 320-343 from mix in 0.5 s
for t in np.arange(328,343,1.0):
    s=m[int(t*sr):int((t+1)*sr)]; print(t,round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1),end=' | ')
