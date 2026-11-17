import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/'
y,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=True)
S=np.abs(librosa.stft(y,n_fft=8192,hop_length=1024)); f=librosa.fft_frequencies(sr=sr,n_fft=8192); t=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr,hop_length=1024)
for a,b in [(121.2,123),(127.3,129),(133.6,135)]:
    s=(t>=a)&(t<b); m=S[:,s].mean(1); k=(f>25)&(f<120); i=np.argmax(m*k); print(a,'sub peak Hz',round(f[i],1))
# find dips
r=librosa.feature.rms(y=y,frame_length=2048,hop_length=512)[0]; rt=librosa.frames_to_time(np.arange(len(r)),sr=sr,hop_length=512)
db=20*np.log10(r+1e-6)
low=rt[(db<-30)]
import itertools
g=[]
for x in low:
    if g and x-g[-1][1]<0.1: g[-1][1]=x
    else: g.append([x,x])
print('dips<-30dB',[(round(a,2),round(b,2)) for a,b in g])
# first-30s onset times of kick-like (low band) for groove
lo=librosa.onset.onset_strength(y=librosa.effects.preemphasis(y)*0+y,sr=sr,hop_length=256,fmax=200)
pk=librosa.onset.onset_detect(onset_envelope=lo,sr=sr,hop_length=256,units='time')
print('kick-ish onsets 20-28s',np.round(pk[(pk>20)&(pk<28)],2))
hi=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256,lag=1)
