import numpy as np, soundfile as sf, scipy.signal as ss
d='/home/user/Listener/v1/data/t_dl_mirror/'
sr=44100;h=441
def ld(n):
  y,_=sf.read(d+n); return y.mean(1) if y.ndim>1 else y
S={'mix':ld('audio/song.wav')}
for s in ['vocals','drums','bass','other']: S[s]=ld(f'stems_raw/htdemucs/song/{s}.wav')
def env(a): n=len(a)//h; return 10*np.log10((a[:n*h].reshape(n,h)**2).mean(1)+1e-12)
E={k:env(v) for k,v in S.items()}
def pm(k,a,b): return round(10*np.log10((10**(E[k][int(a*100):int(b*100)]/10)).mean()),1)
for nm,b in [('0:10.4',10.4),('0:30.4',30.4),('1:11.3',71.3),('2:12',132),('3:13.1',193.1),('3:34',214),('3:35.3',215.3),('3:49',229),('3:54.5',234.5)]:
  print(nm,{k:(pm(k,b-1.5,b),pm(k,b,b+1.5)) for k in E})
# band wall
for k in ['mix','vocals','drums']:
  f,P=ss.welch(S[k],sr,nperseg=16384); P=10*np.log10(P+1e-20)
  print(k,[ (fr,round(P[np.argmin(abs(f-fr))],1)) for fr in [3000,6000,7500,7900,8000,8050,8200,8600,12000,16000]])
# mix 10s rms
m=E['mix']; print('mix 10s rms range',min(10*np.log10((10**(m[i:i+1000]/10)).mean()) for i in range(0,len(m)-1000,500)))
# bass on-time first 10 s
b=E['bass']; print('bass>-35 0-10.4',[round(i*.01,2) for i in np.where(np.diff((b[:1040]>-40).astype(int))!=0)[0]])
# tempo: autocorr of drums envelope
dr=ss.butter(4,[2000,8000],'bp',fs=sr,output='sos'); y=ss.sosfilt(dr,S['drums']); o=np.sqrt(np.convolve(y**2,np.ones(220)/220,'same'))[::220]
o=o-o.mean(); fs=sr/220
ac=np.correlate(o,o,'full')[len(o)-1:]
for lag in [60.8,121.6,182.4]:
  c=int(lag*fs); w=ac[c-200:c+200]; print(lag, (c-200+np.argmax(w))/fs)
import librosa
y2,_=librosa.load(d+'audio/song.wav',sr=22050)
oe=librosa.onset.onset_strength(y=y2,sr=22050); print('tempo',librosa.beat.tempo(onset_envelope=oe,sr=22050))
