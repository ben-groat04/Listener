import librosa,numpy as np,sys
p,s,e=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
y,sr=librosa.load(p,sr=22050,offset=s,duration=e-s)
o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+s
print(p.split('/')[-1],len(o),'onsets; IOI median %.3f'%np.median(np.diff(o)))
print(np.round(o,2))
S=np.abs(librosa.stft(y))**2;f=librosa.fft_frequencies(sr=sr)
tot=S.sum()
for lo,hi in[(0,150),(150,500),(500,2000),(2000,6000),(6000,11025)]:
  print(lo,hi,round(S[(f>=lo)&(f<hi)].sum()/tot,3))
print('centroid',librosa.feature.spectral_centroid(y=y,sr=sr).mean())
