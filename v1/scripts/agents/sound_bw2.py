import librosa,numpy as np
D='/home/user/Listener/v1/data/t_birdwalk/'
b,sr=librosa.load(D+'stems_raw/htdemucs/song/bass.wav',sr=22050)
S=np.abs(librosa.stft(b,n_fft=8192,hop_length=2048))
f=librosa.fft_frequencies(sr=sr,n_fft=8192)
i=f<200
pk=f[i][S[i].argmax(0)]; e=S[i].sum(0)
act=e>np.percentile(e,60)
print('bass peak freq hist (Hz):',np.unique(np.round(pk[act]/2.5)*2.5,return_counts=True))
# 2nd harmonic ratio
# envelope: decay of bass notes
r=librosa.feature.rms(y=b,frame_length=1024,hop_length=256)[0]
t=np.arange(len(r))*256/sr
for a,c in [(14,22)]:
  s=r[(t>=a)&(t<c)]; print(np.round(20*np.log10(s[::8]+1e-9),0))
# clipping count in mix
y,sr2=librosa.load(D+'audio/song.wav',sr=None,mono=False)
print('samples >=0.99:',(np.abs(y)>=0.99).sum(),'>0.95',(np.abs(y)>0.95).sum())
# drum stem onset sharpness, hat band
d,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050)
Sd=np.abs(librosa.stft(d,n_fft=2048))**2;fd=librosa.fft_frequencies(sr=22050,n_fft=2048)
print('drum band share (20-150,150-500,500-2k,2-5k,5-11k):',[round(100*Sd[(fd>=a)&(fd<c)].sum()/Sd.sum(),1) for a,c in [(20,150),(150,500),(500,2000),(2000,5000),(5000,11025)]])
o,_=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=22050)
So=np.abs(librosa.stft(o,n_fft=2048))**2
print('other band share (20-150,150-500,500-2k,2-5k,5-11k):',[round(100*So[(fd>=a)&(fd<c)].sum()/So.sum(),1) for a,c in [(20,150),(150,500),(500,2000),(2000,5000),(5000,11025)]])
v,_=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=22050)
Sv=np.abs(librosa.stft(v,n_fft=2048))**2
print('vocal band share:',[round(100*Sv[(fd>=a)&(fd<c)].sum()/Sv.sum(),1) for a,c in [(20,150),(150,500),(500,2000),(2000,5000),(5000,11025)]])
