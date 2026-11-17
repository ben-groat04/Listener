import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_dl_mirror/stems_raw/htdemucs/song/'
t0,t1=118,142
mix,sr=librosa.load('/home/user/Listener/v1/data/t_dl_mirror/audio/song.wav',sr=None,mono=False)
print('sr',sr,'shape',mix.shape)
m=mix if mix.ndim==1 else mix.mean(0)
seg=mix[...,int(120*sr):int(140*sr)]
print('peak 120-140 dBFS',20*np.log10(np.abs(seg).max()))
if mix.ndim>1: print('L-R rms ratio',np.sqrt(((mix[0]-mix[1])**2).mean())/np.sqrt((m**2).mean()+1e-12))
print('global peak',20*np.log10(np.abs(mix).max()))
S={}
for n in ['vocals','drums','bass','other']:
    y,_=librosa.load(D+n+'.wav',sr=sr,mono=True); S[n]=y
def db(y,a,b):
    x=y[int(a*sr):int(b*sr)]; return 20*np.log10(np.sqrt((x**2).mean())+1e-9)
bounds=[(117.5,118.2),(120.5,121.5),(122.8,123.4),(128,128.4),(129,131),(131.5,132.2),(132.4,133.8),(133.8,134.2),(137,138),(138,140),(143,143.6)]
print('stem dB in windows (mix, v,d,b,o)')
for a,b in bounds:
    print(a,b,round(db(m,a,b),1),[round(db(S[n],a,b),1) for n in S])
# bass presence per 0.5s
print('bass 0.5s dB:',[ (round(t,1),round(db(S['bass'],t,t+.5),0)) for t in np.arange(114,146,.5)])
# kick onsets: drum stem low band
from scipy.signal import butter,sosfilt
sos=butter(4,150,'low',fs=sr,output='sos')
k=sosfilt(sos,S['drums'])
env=librosa.onset.onset_strength(y=k,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=256,units='time',backtrack=False)
on=on[(on>=110)&(on<=150)]
ioi=np.diff(on)
print('kick onsets',np.round(on,2).tolist())
print('IOI median',np.median(ioi), 'tempo beat 95.7 => beat',60/95.703)
beat=60/95.703
grid=np.arange(on[0],150,beat)
# deviation from best-fit grid of beat/2 (eighth)
step=beat/2
ph=np.median(((on-on[0])/step)-np.round((on-on[0])/step))
dev=((on-on[0])/step-np.round((on-on[0])/step))*step*1000
print('kick dev from 8th-grid ms: std',dev.std(),'abs max',np.abs(dev).max())
# bass-in decay etc
# loop regularity: correlate 2-bar chunks of drum stem low band env
bar=beat*4
e=librosa.feature.rms(y=S['drums'],frame_length=1024,hop_length=512)[0]
fr=sr/512
def chunk(t): return e[int(t*fr):int((t+bar)*fr)]
base=chunk(112.5+bar*0)
for t in [112.5+bar*i for i in range(1,8)]:
    c=chunk(t);n=min(len(c),len(base)); print('bar corr t=%.1f'%t, round(np.corrcoef(base[:n],c[:n])[0,1],3))
# spectral: mix HF energy
S_=np.abs(librosa.stft(m[int(120*sr):int(140*sr)],n_fft=4096))**2
f=librosa.fft_frequencies(sr=sr,n_fft=4096)
tot=S_.sum()
for lo,hi in [(0,200),(200,2000),(2000,8000),(8000,16000),(16000,24000)]:
    print('band',lo,hi,round(10*np.log10(S_[(f>=lo)&(f<hi)].sum()/tot),1))
# vocal-gap: 10ms envelope
v=S['vocals'];e10=np.array([np.sqrt((v[i:i+int(.01*sr)]**2).mean()) for i in range(int(131*sr),int(136*sr),int(.01*sr))])
d=20*np.log10(e10+1e-9);t=131+np.arange(len(d))*.01
print('vocal 10ms dB, first <-45 after 131:',t[d<-45][:1],'last in range',t[d<-45][-1:], 'mean in gap',d[(t>132.7)&(t<133.8)].mean())
