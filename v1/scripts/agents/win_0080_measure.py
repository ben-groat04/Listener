import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_birdwalk/'
sr=22050
def load(p): 
    y,s=librosa.load(p,sr=sr,mono=False,offset=76,duration=34); return y
mix=load(D+'audio/song.wav')
st={k:load(D+f'stems_raw/htdemucs/song/{k}.wav') for k in ['drums','bass','vocals','other']}
def env(y,hop=221):
    m=y if y.ndim==1 else y
    m=np.atleast_2d(m); r=librosa.feature.rms(y=m.mean(0),frame_length=441,hop_length=hop)[0]; return 20*np.log10(r+1e-9)
print('mix peak dBFS 76-110', 20*np.log10(np.abs(mix).max()))
# per-2s dB of each stem 78-104
for k,y in {'mix':mix,**st}.items():
    e=env(y)
    t=np.arange(len(e))*0.01+76
    print(k,[round(float(np.mean(e[(t>=a)&(t<a+2)])),1) for a in range(80,102,2)])
# mid/side
L,R=mix; print('S/M dB',[round(float(10*np.log10(np.mean(((L-R)/2)[int((a-76)*sr):int((a+2-76)*sr)]**2)/np.mean(((L+R)/2)[int((a-76)*sr):int((a+2-76)*sr)]**2))),1) for a in range(80,102,2)])
# onsets
for k in ['drums','bass']:
    y=st[k].mean(0)
    if k=='bass': y=librosa.effects.preemphasis(y,coef=0) 
    o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+76
    o=o[(o>=80)&(o<100)]; print(k,'onsets',np.round(o,2).tolist())
# kick = drums low band
from scipy.signal import butter,sosfilt
k=sosfilt(butter(4,[40,120],'band',fs=sr,output='sos'),st['drums'].mean(0))
oe=librosa.onset.onset_strength(y=k,sr=sr,hop_length=221)
pk=librosa.util.peak_pick(oe,pre_max=8,post_max=8,pre_avg=20,post_avg=20,delta=np.percentile(oe,85)*0.5,wait=12)
kt=pk*0.01+76; kt=kt[(kt>=80)&(kt<100)]
print('kick',np.round(kt,2).tolist()); ioi=np.diff(kt); print('kick IOI median',np.median(ioi),'bpm',60/np.median(ioi))
bt=np.array(json.load(open(D+'audio_features/beat_times.json'))); bt=bt[(bt>=80)&(bt<100)]
print('beat period',np.median(np.diff(bt)),'bpm',60/np.median(np.diff(bt)))
# kick spread vs beat grid
dev=[min(abs(x-bt)) for x in kt]; print('kick-to-tracker-beat dev ms mean/median/max',np.mean(dev)*1000,np.median(dev)*1000,np.max(dev)*1000)
# band energy
S=np.abs(librosa.stft(mix.mean(0),n_fft=2048))**2; f=librosa.fft_frequencies(sr=sr,n_fft=2048)
for a,b in [(0,150),(150,500),(500,2000),(2000,5000),(5000,11025)]:
    print('band',a,b,round(10*np.log10(S[(f>=a)&(f<b)].sum()/S.sum()),1))
# spectral centroid of other in 93-100, bass
c=librosa.feature.spectral_centroid(y=mix.mean(0),sr=sr,hop_length=2205)[0]
t=np.arange(len(c))*0.1+76
print('centroid Hz per 5s',[int(c[(t>=a)&(t<a+5)].mean()) for a in range(80,105,5)])
