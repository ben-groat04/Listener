import librosa,numpy as np,sys
D='/home/user/Listener/v1/data/t_birdwalk/'
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False)
print('sr',sr,y.shape)
m=y.mean(0) if y.ndim>1 else y
S=np.abs(librosa.stft(m,n_fft=4096))**2
f=librosa.fft_frequencies(sr=sr,n_fft=4096)
tot=S.sum(0)+1e-12
bands=[(20,60),(60,200),(200,800),(800,3000),(3000,6000),(6000,10000),(10000,16000),(16000,22050)]
fr=sr/1024
print('overall band share %:',[round(100*S[(f>=a)&(f<b)].sum()/S.sum(),2) for a,b in bands])
t=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr,n_fft=4096,hop_length=1024)
for a,b in [(0,12),(14,45),(48,58),(60,100),(121,135),(140,170),(180,188)]:
  i=(t>=a)&(t<b); print(a,b,[round(100*S[(f>=x)&(f<z)][:,i].sum()/S[:,i].sum(),1) for x,z in bands])
# rolloff 99.9%
cs=np.cumsum(S.sum(1))/S.sum(); print('99.9% rolloff Hz',f[np.searchsorted(cs,0.999)], '99.99',f[np.searchsorted(cs,0.9999)])
# energy above 16k relative
for lo in (10000,12000,14000,16000,18000):
  print(lo, 10*np.log10(S[f>=lo].sum()/S.sum()))
# crest, peak
print('peak',np.abs(y).max(),'rms dB',20*np.log10(np.sqrt((y**2).mean())))
r=librosa.feature.rms(y=m,frame_length=2048,hop_length=512)[0]
print('crest dB',20*np.log10(np.abs(m).max()/np.sqrt((m**2).mean())))
print('short-term loudness range (p95-p10 dB of 1s rms):',np.percentile(20*np.log10(r+1e-9),[10,50,95]))
# stereo correlation
if y.ndim>1:
  print('L/R corr',np.corrcoef(y[0],y[1])[0,1])
  M=(y[0]+y[1])/2;Sd=(y[0]-y[1])/2
  for a,b in [(0,12),(14,45),(48,58),(60,100),(121,135),(140,170)]:
    s=slice(int(a*sr),int(b*sr)); print('side/mid',a,b,round(np.sqrt((Sd[s]**2).mean()/(M[s]**2).mean()),3), 'LR corr',round(np.corrcoef(y[0][s],y[1][s])[0,1],3))
# stems: spectral centroid, bandshare, hnr
for st in ['vocals','drums','bass','other']:
  z,_=librosa.load(D+f'stems_raw/htdemucs/song/{st}.wav',sr=22050)
  c=librosa.feature.spectral_centroid(y=z,sr=22050)[0]; fl=librosa.feature.spectral_flatness(y=z)[0]
  rr=librosa.feature.rms(y=z)[0]; w=rr>np.percentile(rr,50)
  print(st,'centroid(active)',round(np.median(c[w])),'flat',round(float(np.median(fl[w])),4),'crest',round(20*np.log10(np.abs(z).max()/np.sqrt((z**2).mean())),1))
