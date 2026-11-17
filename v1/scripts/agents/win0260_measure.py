import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_cshells_cshore/'
def ld(p,s,e):
    y,sr=librosa.load(p,sr=22050,mono=False,offset=s,duration=e-s); return y,sr
mix,sr=ld(D+'audio/song.wav',260,280)
m=mix.mean(0) if mix.ndim>1 else mix
print('sample peak dBFS',20*np.log10(np.abs(mix).max()), 'rms',20*np.log10(np.sqrt((m**2).mean())))
dr,_=ld(D+'stems_raw/htdemucs/song/drums.wav',260,280); dr=dr.mean(0) if dr.ndim>1 else dr
lo=librosa.effects.preemphasis(dr)
import scipy.signal as ss
b,a=ss.butter(4,150/(sr/2),'low'); k=ss.filtfilt(b,a,dr)
oe=librosa.onset.onset_strength(y=k,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time',backtrack=False)
print('kick onsets',len(on)); ioi=np.diff(on); print('IOI median',np.median(ioi),'bpm',60/np.median(ioi) if np.median(ioi) else 0)
print(np.round(on+260,2))
# grid deviation relative to best-fit grid at median beat
for per in [np.median(ioi),np.median(ioi)*2]:
    best=None
    for ph in np.linspace(0,per,100):
        d=((on-ph+per/2)%per)-per/2; s=np.std(d)
        if best is None or s<best[0]: best=(s,ph)
    print('grid period',per,'bpm',60/per,'resid std ms',best[0]*1000)
full,_=ld(D+'audio/song.wav',0,361)
t,beats=librosa.beat.beat_track(y=full.mean(0) if full.ndim>1 else full,sr=sr); print('tempo',t)
# bass levels
for nm in ['bass','other','vocals']:
    y,_=ld(D+f'stems_raw/htdemucs/song/{nm}.wav',255,285); y=y.mean(0) if y.ndim>1 else y
    r=[20*np.log10(np.sqrt((y[i*sr:(i+1)*sr]**2).mean())+1e-9) for i in range(30)]
    print(nm,np.round(r,1))
# bass dropout times at 100ms
y,_=ld(D+'stems_raw/htdemucs/song/bass.wav',255,285); y=y.mean(0) if y.ndim>1 else y
h=sr//10; r=np.array([20*np.log10(np.sqrt((y[i*h:(i+1)*h]**2).mean())+1e-9) for i in range(len(y)//h)])
lowm=r<-40; ch=np.diff(lowm.astype(int)); print('bass<-40 transitions',(np.where(ch!=0)[0]+1)/10+255,ch[ch!=0])
# spectral band: 400-1000Hz line, centroid, rolloff
S=np.abs(librosa.stft(m,n_fft=2048)); f=librosa.fftfreq if 0 else None
fr=librosa.fft_frequencies(sr=sr,n_fft=2048)
tot=S.sum(); 
for lo_,hi in [(0,200),(200,1000),(1000,4000),(4000,10000)]: print(lo_,hi,S[(fr>=lo_)&(fr<hi)].sum()/tot)
print('centroid',librosa.feature.spectral_centroid(y=m,sr=sr).mean(),'rolloff95',librosa.feature.spectral_rolloff(y=m,sr=sr,roll_percent=0.95).mean())
# loop regularity: bar-length (4 beats @~123) self-similarity of drums
bar=int(sr*4*60/123.05)
rms=librosa.feature.chroma_stft(y=m,sr=sr)
