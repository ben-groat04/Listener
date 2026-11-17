import librosa,numpy as np,json
R='/home/user/Listener/v1/data/t_dl_mirror/'
S=R+'stems_raw/htdemucs/song/'
t0,t1=40,60
out={}
y,sr=librosa.load(R+'audio/song.wav',sr=None,mono=False)
print('sr',sr,y.shape)
m=y if y.ndim==1 else y.mean(0)
if y.ndim>1: print('L-R rms ratio',np.sqrt(np.mean((y[0]-y[1])**2))/np.sqrt(np.mean(m**2)))
seg=m[int(t0*sr):int(t1*sr)]
print('peak win dBFS',20*np.log10(np.abs(seg).max()),'whole peak',20*np.log10(np.abs(m).max()))
print('rms win',20*np.log10(np.sqrt(np.mean(seg**2))))
# band energy
S_=np.abs(librosa.stft(seg,n_fft=2048))**2
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
tot=S_.sum()
for lo,hi in [(0,60),(60,200),(200,1000),(1000,4000),(4000,8000),(8000,16000),(16000,30000)]:
    print(lo,hi,round(10*np.log10(S_[(f>=lo)&(f<hi)].sum()/tot+1e-12),1))
# drums
d,_=librosa.load(S+'drums.wav',sr=sr,mono=True)
dd=d[int(t0*sr):int(t1*sr)]
# kick: lowpass band onset
import scipy.signal as sg
b,a=sg.butter(4,150/(sr/2));k=sg.filtfilt(b,a,dd)
env=librosa.onset.onset_strength(y=k,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=256,units='time',delta=0.3)
on=on+t0
print('kick onsets',np.round(on,2).tolist())
ioi=np.diff(on);print('kick IOI',np.round(ioi,2).tolist())
bt=np.array(json.load(open(R+'audio_features/beat_times.json')))
bt=bt[(bt>=t0)&(bt<t1)];print('beat IOI median',np.median(np.diff(bt)),'n',len(bt))
# snare band
b2,a2=sg.butter(4,[1500/(sr/2),6000/(sr/2)],'band');sn=sg.filtfilt(b2,a2,dd)
env2=librosa.onset.onset_strength(y=sn,sr=sr,hop_length=256)
on2=librosa.onset.onset_detect(onset_envelope=env2,sr=sr,hop_length=256,units='time',delta=0.3)+t0
print('mid-band onsets',np.round(on2,2).tolist())
# bass stem activity at 0.1s
bs,_=librosa.load(S+'bass.wav',sr=sr,mono=True)
bb=bs[int(t0*sr):int(t1*sr)]
h=int(0.1*sr);e=[20*np.log10(np.sqrt(np.mean(bb[i:i+h]**2))+1e-9) for i in range(0,len(bb)-h,h)]
e=np.array(e);on_=e>-40
runs=[];st=None
for i,v in enumerate(on_):
    if v and st is None: st=i
    if not v and st is not None: runs.append((round(t0+st*.1,1),round(t0+i*.1,1)));st=None
if st is not None: runs.append((round(t0+st*.1,1),t1))
print('bass runs (>-40dB)',runs)
# loop regularity: chroma/mel similarity of 2-bar segments at lag
bar=60/95.7*4
print('bar s',bar)
o,_=librosa.load(S+'other.wav',sr=sr,mono=True)
mel=librosa.power_to_db(librosa.feature.melspectrogram(y=o[int(t0*sr):int(t1*sr)],sr=sr,hop_length=512))
fr=sr/512
for lag in [bar,2*bar,4*bar]:
    L=int(lag*fr);A=mel[:,:-L].ravel();B=mel[:,L:].ravel();print('other mel corr lag %.2fs'%lag,round(np.corrcoef(A,B)[0,1],3))
# vocals stem band: 
v,_=librosa.load(S+'vocals.wav',sr=sr,mono=True);vv=v[int(t0*sr):int(t1*sr)]
Sv=np.abs(librosa.stft(vv,n_fft=2048))**2;print('vocal centroid Hz',librosa.feature.spectral_centroid(S=np.sqrt(Sv),sr=sr).mean())
So=np.abs(librosa.stft(o[int(t0*sr):int(t1*sr)],n_fft=2048))**2
fo=so=None
print('other energy >8k share',round(So[f>8000].sum()/So.sum(),4),'other centroid',librosa.feature.spectral_centroid(S=np.sqrt(So),sr=sr).mean())
