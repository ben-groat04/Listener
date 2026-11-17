import librosa,numpy as np,json
R='data/t_cshells_cshore/stems_raw/htdemucs/song/'
t0,t1=198,222
y,sr=librosa.load('data/t_cshells_cshore/audio/song.wav',sr=None,mono=False)
print('sr',sr,y.shape)
m=y.mean(0) if y.ndim>1 else y
seg=y[...,int(200*sr):int(220*sr)]
print('window sample peak dBFS',20*np.log10(np.abs(seg).max()),'file peak',20*np.log10(np.abs(y).max()))
d,_=librosa.load(R+'drums.wav',sr=sr,mono=True)
# kick band
import scipy.signal as ss
sos=ss.butter(4,[40,120],'bp',fs=sr,output='sos');k=ss.sosfilt(sos,d)
env=librosa.feature.rms(y=k,frame_length=1024,hop_length=256)[0];tt=librosa.frames_to_time(np.arange(len(env)),sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=np.diff(env,prepend=0),sr=sr,hop_length=256,units='time',backtrack=False,delta=0.01*env.max())
on=on[(on>=200)&(on<220)];print('kick onsets',np.round(on,2));ioi=np.diff(on);print('IOI med',np.median(ioi),'bpm',60/np.median(ioi))
g=np.arange(len(on))
per=np.median(ioi);ph=np.round((on-on[0])/per);res=(on-on[0])-ph*per;print('resid std ms',res.std()*1000)
# overall onset tempo
oe=librosa.onset.onset_strength(y=d,sr=sr);tp=librosa.feature.tempo(onset_envelope=oe,sr=sr);print('drum tempo',tp)
bt=np.array(json.load(open('data/t_cshells_cshore/audio_features/beat_times.json')) if isinstance(json.load(open('data/t_cshells_cshore/audio_features/beat_times.json')),list) else json.load(open('data/t_cshells_cshore/audio_features/beat_times.json'))['beats'])
b=bt[(bt>=200)&(bt<220)];print('beat ioi median',np.median(np.diff(b)),len(b))
# stem band levels per second for bass 
for name in ['bass','other','drums','vocals']:
    s,_=librosa.load(R+name+'.wav',sr=sr,mono=True)
    e=librosa.feature.rms(y=s,frame_length=2048,hop_length=sr//10)[0]
    print(name,'0.5s dB',np.round(20*np.log10(e[2000:2200:5]+1e-9),0))
# spectral centroid mix per 4s
for a in range(200,220,4):
    x=m[a*sr:(a+4)*sr];print(a,'centroid',librosa.feature.spectral_centroid(y=x,sr=sr).mean().round(0),'rolloff',librosa.feature.spectral_rolloff(y=x,sr=sr,roll_percent=.95).mean().round(0))
# loop regularity: correlation of 1 bar (4 beats) segments of drum stem
bar=4*np.median(np.diff(b));print('bar s',bar)
def seg(t):
    x=d[int(t*sr):int((t+bar)*sr)];return librosa.feature.rms(y=x,frame_length=1024,hop_length=512)[0][:60]
for t in [200.5,200.5+bar,200.5+2*bar,200.5+3*bar]:
    print(t,np.corrcoef(seg(200.5),seg(t))[0,1])
# sweep: lead-ish in other 207-209
o,_=librosa.load(R+'other.wav',sr=sr,mono=True)
S=np.abs(librosa.stft(o[int(207*sr):int(209.5*sr)],n_fft=4096,hop_length=1024));f=librosa.fft_frequencies(sr=sr,n_fft=4096)
for i in range(0,S.shape[1],4):print(round(207+i*1024/sr,2),round(f[100:600][S[100:600,i].argmax()]+0,0)+ (f[100]-f[0]) *0)
