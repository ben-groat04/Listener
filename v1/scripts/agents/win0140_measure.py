import librosa, numpy as np, json
D='/home/user/Listener/v1/data/t_birdwalk/'
S='stems_raw/htdemucs/song/'
sr=22050
t0,t1=120,170
def load(p): return librosa.load(D+p,sr=sr,offset=t0,duration=t1-t0)[0]
y=load('audio/song.wav'); st={k:load(S+k+'.wav') for k in ['vocals','drums','bass','other']}
def env(x,w=0.1):
    h=int(sr*w); n=len(x)//h; return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
mix=env(y)
print('peak mix 140-160 dBFS',20*np.log10(np.abs(y[20*sr:40*sr]).max()), 'whole file peak')
yf=librosa.load(D+'audio/song.wav',sr=None)[0]; print('file peak',20*np.log10(np.abs(yf).max()))
for k,x in st.items():
    e=env(x); print(k,[round(np.mean(e[int((a-t0)*10):int((b-t0)*10)]),1) for a,b in [(140,143.4),(144,155),(156,160)]])
print('mix',[round(np.mean(mix[int((a-t0)*10):int((b-t0)*10)]),1) for a,b in [(140,143.4),(144,155),(156,160)]])
# kick onsets from drum stem low band
d=st['drums']; 
import scipy.signal as sg
b,a=sg.butter(4,150,'low',fs=sr); lo=sg.filtfilt(b,a,d)
oenv=librosa.onset.onset_strength(y=lo,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oenv,sr=sr,hop_length=256,units='time',backtrack=False)+t0
on=on[(on>=138)&(on<=162)]
print('kick onsets',np.round(on,2)); print('IOI',np.round(np.diff(on),2))
# bass onsets
bo=librosa.onset.onset_detect(y=st['bass'],sr=sr,hop_length=256,units='time')+t0
bo=bo[(bo>=138)&(bo<=162)];print('bass on',np.round(bo,2))
# full-mix tempo
tp=librosa.beat.beat_track(y=y[20*sr:50*sr],sr=sr);print(tp[0])
# centroid and HF
for nm,(a,b2) in {'drumbass':(140,143.4),'voxonly':(144,155),'full':(156,160)}.items():
    seg=y[int((a-t0)*sr):int((b2-t0)*sr)]
    print(nm,'centroid',round(float(librosa.feature.spectral_centroid(y=seg,sr=sr).mean())), 'rolloff95',round(float(librosa.feature.spectral_rolloff(y=seg,sr=sr,roll_percent=.95).mean())))
# vocal pitch in dropout
f0,vf,_=librosa.pyin(st['vocals'][int(24*sr):int(36*sr)],fmin=60,fmax=800,sr=sr)
f=f0[~np.isnan(f0)];print('vocal f0 pct',np.percentile(f,[5,50,95]) if len(f) else None, 'voiced frac',vf.mean())
# 10ms env for 2:20-2:40 boundaries
for name,x in [('mix',y)]+list(st.items()):
    e=env(x,0.01)
    for tt in (143.0,143.5,144.0,155.0,155.5,156.0):
        i=int((tt-t0)*100); print(name,tt,round(e[i],1),end=' | ')
    print()
