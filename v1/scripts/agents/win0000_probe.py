import numpy as np, librosa, json
d='/home/user/Listener/v1/data/t_cshells_cshore/'
y,sr=librosa.load(d+'audio/song.wav',sr=None,mono=False)
print(y.shape,sr)
m=y.mean(0) if y.ndim>1 else y
hop=int(sr*0.01)
def env(x): 
    n=len(x)//hop; return np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-12
e=20*np.log10(env(m[:20*sr]))
for a,b in [(0,2),(2,4),(4,6),(6,8),(8,10),(10,11.2),(11.4,13),(13,16),(16,20)]:
    print('mix',a,b,round(e[int(a*100):int(b*100)].mean(),1),round(e[int(a*100):int(b*100)].max(),1))
print('peak sample 0-20',20*np.log10(np.abs(y[:, :20*sr]).max()))
print('peak whole',20*np.log10(np.abs(y).max()))
# first sound
for th in (-80,-60,-50,-40,-30):
    i=np.argmax(e>th); print('first >',th,i/100)
st={}
for s in ['vocals','drums','bass','other']:
    x,_=librosa.load(d+f'stems_raw/htdemucs/song/{s}.wav',sr=sr,mono=True); st[s]=x
    ee=20*np.log10(env(x[:20*sr]))
    print(s,[ (a,b,round(ee[int(a*100):int(b*100)].mean(),1)) for a,b in [(0,2.5),(2.5,6),(6,7.5),(7.5,11.2),(11.4,14),(14,20)]])
# drums onsets after 11.3
x=st['drums'][:20*sr]
on=librosa.onset.onset_detect(y=x,sr=sr,units='time',backtrack=False)
print('drum onsets',np.round(on,2))
# kick: low band
import scipy.signal as ss
b,a=ss.butter(4,150/(sr/2)); k=ss.filtfilt(b,a,x)
ko=librosa.onset.onset_detect(y=k,sr=sr,units='time',delta=0.1)
print('kick onsets',np.round(ko,2)); print('kick IOI',np.round(np.diff(ko),2))
bt=json.load(open(d+'audio_features/beat_times.json')); bt=[t for t in bt if t<20]; print('beats',bt[:40])
# stereo width/band-limit
M=np.abs(librosa.stft(m[int(12*sr):int(20*sr)])); f=librosa.fft_frequencies(sr=sr)
tot=M.sum(); 
for lo,hi in [(0,200),(200,2000),(2000,8000),(8000,16000),(16000,sr/2)]:
    print('band',lo,hi,round(M[(f>=lo)&(f<hi)].sum()/tot,3))
print('rolloff95',np.median(librosa.feature.spectral_rolloff(y=m[int(12*sr):int(20*sr)],sr=sr,roll_percent=.95)))
print('centroid',np.median(librosa.feature.spectral_centroid(y=m[int(12*sr):int(20*sr)],sr=sr)))
