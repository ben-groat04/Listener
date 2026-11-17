import numpy as np, librosa, json
from scipy.signal import butter,sosfilt
D='/home/user/Listener/v1/data/t_dl_mirror/stems_raw/htdemucs/song/'
sr=44100
S={n:librosa.load(D+n+'.wav',sr=sr,mono=True)[0] for n in ['vocals','drums','bass','other']}
m=librosa.load('/home/user/Listener/v1/data/t_dl_mirror/audio/song.wav',sr=sr,mono=True)[0]
def db(y,a,b):
    x=y[int(a*sr):int(b*sr)];return round(float(20*np.log10(np.sqrt((x**2).mean())+1e-9)),1)
print('132-135 in 0.25s: t, mix, vocals, drums, bass, other')
for t in np.arange(131.75,135,0.25): print(round(t,2),db(m,t,t+.25),[db(S[n],t,t+.25) for n in S])
# kick: strong low-band onsets near tracker beats
beats=np.array(json.load(open('/home/user/Listener/v1/data/t_dl_mirror/audio_features/beat_times.json')))
beats=beats[(beats>=114)&(beats<=146)]
sos=butter(4,120,'low',fs=sr,output='sos');k=sosfilt(sos,S['drums'])
env=np.abs(k);hop=128
e=np.array([env[i:i+hop].max() for i in range(0,len(env)-hop,hop)]);tt=np.arange(len(e))*hop/sr
lag=[]
for b in beats:
    w=(tt>b-.1)&(tt<b+.1)
    if e[w].max()>0.5*np.percentile(e[(tt>114)&(tt<146)],98): lag.append((tt[w][e[w].argmax()]-b)*1000)
lag=np.array(lag);print('kick peaks near tracker beats n=',len(lag),'mean ms',lag.mean().round(1),'std ms',lag.std().round(1))
ib=np.diff(beats);print('tracker beat IOI mean',ib.mean().round(3),'=> BPM',(60/ib.mean()).round(1))
# loop regularity on drum stem: correlate 1 bar chunk envelope at hop=10ms across bars (bar=4 beats)
bar=4*ib.mean();e2=librosa.feature.rms(y=S['drums'],frame_length=882,hop_length=441)[0]
def ch(t):return e2[int(t*100):int((t+bar)*100)]
b0=114.451
cs=[round(np.corrcoef(ch(b0),ch(b0+bar*i))[0,1],2) for i in range(1,12) if len(ch(b0+bar*i))==len(ch(b0))]
print('bar-to-bar drum env corr vs 114.45:',cs)
# drum hi-hat / snare crude: brightness centroid
for a,b in [(120,125),(125,131),(134,138),(138,142)]:
    x=m[int(a*sr):int(b*sr)];print(a,b,'centroid',round(float(librosa.feature.spectral_centroid(y=x,sr=sr).mean())),'Hz','crest dB',round(float(20*np.log10(np.abs(x).max()/np.sqrt((x**2).mean()))),1))
