# mirror-image test about 8 kHz (16 kHz-sampling image) and tuning of bed, drum spectral tilt (vinyl-era vs machine cue)
import numpy as np, soundfile as sf, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'; S=D+'stems_raw/htdemucs/song/'
x,sr=sf.read(D+'audio/song.wav',dtype='float32'); mix=x.mean(1)
f,t,Z=ss.stft(mix,sr,nperseg=4096,noverlap=2048); L=np.log10(np.abs(Z)**2+1e-20)
df=f[1]-f[0]
# bins above the wall 8.3..12 kHz vs mirrored bins 16000-f (7.7..4 kHz)
ii=np.where((f>8300)&(f<12000))[0]; jj=np.array([np.argmin(abs(f-(16000-f[i]))) for i in ii])
cs=[]
for k in range(0,L.shape[1],5):
    a=L[ii,k]; b=L[jj,k]
    if a.std()>0 and b.std()>0 and L[:,k].max()>-6: cs.append(np.corrcoef(a,b)[0,1])
print('mirror corr about 8k (above-wall vs in-band mirror), per-frame median %.2f p90 %.2f  n=%d'%(np.median(cs),np.percentile(cs,90),len(cs)))
# control: mirror about 10 kHz of the same above-wall region vs 12-16k
ii2=np.where((f>10300)&(f<12000))[0]; jj2=np.array([np.argmin(abs(f-(20000-f[i]))) for i in ii2])
c2=[np.corrcoef(L[ii2,k],L[jj2,k])[0,1] for k in range(0,L.shape[1],5) if L[:,k].max()>-6]
print('control mirror about 10k median %.2f'%np.median(c2))
# drum stem spectral tilt: energy in octave bands, 0:30-3:30
dr,_=sf.read(S+'drums.wav',dtype='float32'); dr=dr.mean(1)[int(30*sr):int(210*sr)]
fw,P=ss.welch(dr,sr,nperseg=8192)
for lo,hi in [(30,100),(100,300),(300,1000),(1000,3000),(3000,6000),(6000,8000)]:
    m=(fw>=lo)&(fw<hi); print('drums %5d-%5d Hz  %.1f dB (power sum re total)'%(lo,hi,10*np.log10(P[m].sum()/P.sum())))
