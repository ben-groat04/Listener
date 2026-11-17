import numpy as np, librosa, soundfile as sf, json
d='/home/user/Listener/v1/data/t_cshells_cshore/'
names=['mix','drums','bass','vocals','other']
env={}
sr=None
for n in names:
    p=d+('audio/song.wav' if n=='mix' else f'stems_raw/htdemucs/song/{n}.wav')
    y,sr=sf.read(p,start=int(95*44100) if False else 0,frames=0) if False else (None,None)
    info=sf.info(p); sr=info.samplerate
    y,_=sf.read(p,start=int(96*sr),frames=int(28*sr)); y=y.mean(1) if y.ndim>1 else y
    env[n]=(y,sr)
def rms(y,sr,a,b): 
    s=y[int((a-96)*sr):int((b-96)*sr)]; return 20*np.log10(np.sqrt(np.mean(s**2))+1e-9)
segs=[(100,102),(102,105),(105,109),(109,113),(113,114),(114,118),(118,121),(121,124),(100,109.3),(109.3,113.2),(113.2,120)]
print('seg',*names)
for a,b in segs: print(a,b,*[round(rms(*env[n],a,b),1) for n in names])
for a in [100,105,108,109,112,113,114,115,118,119,120]:
    pass
# 1s rms around boundaries
for t in np.arange(106,116,0.5):
    print(round(t,1),*[round(rms(*env[n],t,t+0.5),1) for n in names])
# kick onsets
y,sr=env['drums']
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time')+96
print('drum onsets 100-120',[round(x,2) for x in on if 100<=x<=120])
y,sr=env['bass']
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time')+96
b=[x for x in on if 113<=x<=121]
print('bass onsets 113-121',[round(x,3) for x in b]); print('IOI',np.round(np.diff(b),3))
# peak
y,sr=sf.read(d+'audio/song.wav',start=int(100*44100),frames=20*44100)
print('sr',sr,'peak 100-120',20*np.log10(np.abs(y).max()))
print('peak 106-113',20*np.log10(np.abs(y[6*sr:13*sr]).max()))
# low-band kick: 40-120Hz on drums
from scipy.signal import butter,sosfilt
y,sr=env['drums']; sos=butter(4,[40,120],'bandpass',fs=sr,output='sos'); k=sosfilt(sos,y)
e=np.abs(k); 
oe=librosa.onset.onset_strength(y=k,sr=sr,hop_length=128)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=128,units='time',backtrack=False)+96
on=[x for x in on if 100<=x<=120]; print('kick-band onsets',np.round(on,2)); print('IOI',np.round(np.diff(on),2))
bt=json.load(open(d+'audio_features/beat_times.json')); bt=bt if isinstance(bt,list) else bt.get('beats',bt)
print('beats',[round(x,2) for x in bt if 100<=x<=120][:12])
# spectral centroid / stereo
y,sr=sf.read(d+'audio/song.wav',start=int(100*44100),frames=20*44100)
for a,b2 in [(0,9.3),(9.3,13.3),(13.3,20)]:
    s=y[int(a*sr):int(b2*sr)]; m=s.mean(1); 
    c=librosa.feature.spectral_centroid(y=m,sr=sr).mean(); hf=np.mean(np.abs(np.fft.rfft(m))[int(len(m)*8000/ (sr/2)):])
    S=np.abs(np.fft.rfft(m))**2;f=np.fft.rfftfreq(len(m),1/sr)
    print(a+100,b2+100,'centroid',round(c),'>8k share dB',round(10*np.log10(S[f>8000].sum()/S.sum()),1))
