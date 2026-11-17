import numpy as np, soundfile as sf, librosa
D='/home/user/Listener/v1/data/video1/'
def load(p):
    x,sr=sf.read(p); return (x.mean(1) if x.ndim>1 else x).astype(np.float32),sr
dr,sr=load(D+'stems_raw/htdemucs/song/drums.wav')
on=librosa.onset.onset_detect(y=dr,sr=sr,units='time',backtrack=False,delta=0.1)
print('n onsets',len(on),'rate',len(on)/188.66)
d=np.diff(on);print('median gap',np.median(d))
# onset rate by section
for a,b in [(5,30),(33,75),(90,100),(150,165),(170,185)]:
    m=(on>=a)&(on<b);print(a,b,m.sum()/(b-a))
# roll
for a,b in [(183,184),(184,185),(185,186),(186,187),(187,188.3)]:
    m=(on>=a)&(on<b);print('roll check',a,b,m.sum(), np.round(np.diff(on[m]),3)[:30])
# tempo curve via onset envelope tempogram autocorr: global
env=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=512)
for a,b in [(5,60),(60,120),(120,167),(170,188)]:
    e=env[int(a*sr/512):int(b*sr/512)];e=e-e.mean()
    ac=np.correlate(e,e,'full')[len(e)-1:];lags=np.arange(len(ac))*512/sr
    m=(lags>0.5)&(lags<1.6);i=np.argmax(ac*m);print('acf peak',a,b,lags[i],60/lags[i])
    # also at quarter beat
    m=(lags>0.1)&(lags<0.3);i=np.argmax(ac*m);print('  short peak',lags[i], 'beat=',lags[i]*4,60/(lags[i]*4))
# click gap 2:37-2:42 : high-band energy
import scipy.signal as ss
hp=ss.butter(4,2000,'hp',fs=sr,output='sos');h=ss.sosfilt(hp,dr)
for t in np.arange(154,165,0.385):
    s=h[int(t*sr):int((t+0.385)*sr)];print(round(t,2),round(20*np.log10(np.sqrt(np.mean(s**2))+1e-9),1),end=' | ')
print()
