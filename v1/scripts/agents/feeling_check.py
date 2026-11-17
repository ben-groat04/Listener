import librosa,numpy as np,sys
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'drums.wav',sr=22050,mono=True)
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time')
ioi=np.diff(on);print('onsets',len(on),'median ioi',np.median(ioi))
h,_=np.histogram(ioi,bins=np.arange(0.05,1.0,0.05));print(dict(zip(np.round(np.arange(0.05,0.95,0.05),2),h)))
ac=librosa.autocorrelate(oe-oe.mean());ac/=ac[0];fps=sr/256
lags=np.arange(len(ac))/fps
for lo,hi in[(0.15,0.25),(0.35,0.45),(0.7,0.85),(1.4,1.6),(3,3.2),(6,6.3)]:
    m=(lags>=lo)&(lags<=hi);i=np.argmax(ac[m]);print(lo,hi,'peak lag',round(lags[m][i],3),'ac',round(ac[m][i],2))
# band energy per 10s for low bass vs total, and ending
x,sr2=librosa.load('/home/user/Listener/v1/data/video1/audio/song.wav',sr=22050,mono=True)
r=librosa.feature.rms(y=x,frame_length=2048,hop_length=512)[0];t=librosa.times_like(r,sr=sr2,hop_length=512)
for a in (186,187,188,188.3,188.5):
    m=(t>=a)&(t<a+0.2);print(a,round(20*np.log10(r[m].mean()+1e-9),1))
# kick/low-band drum rhythm: bass-drum onsets
import scipy.signal as s
sos=s.butter(4,150,'low',fs=sr,output='sos');k=s.sosfilt(sos,y)
ke=librosa.onset.onset_strength(S=np.abs(librosa.stft(k,hop_length=256))[:8],sr=sr,hop_length=256)
kon=librosa.onset.onset_detect(onset_envelope=ke,sr=sr,hop_length=256,units='time');print('kick-ish onsets',len(kon),'median ioi',np.median(np.diff(kon)))
