import json,numpy as np,librosa,soundfile as sf
d='/home/user/Listener/v1/data/t_dl_mirror/'
S={}
for n in ['drums','bass','vocals','other']:
    x,s=sf.read(d+'stems_raw/htdemucs/song/'+n+'.wav'); S[n]=x.mean(1)
mix,s=sf.read(d+'audio/song.wav'); S['mix']=mix.mean(1)
def db(z,t0,t1): 
    z=z[int(t0*s):int(t1*s)];return round(20*np.log10(np.sqrt((z**2).mean())+1e-9),1)
bt=json.load(open(d+'audio_features/beat_times.json'))
print('segment dB (mix,drums,bass,vocals,other)')
for t0,t1 in [(0,2.8),(2.8,6),(6,10.4),(10.4,12.3),(12.3,15.4),(15.4,16.7),(16.7,18.3),(18.3,20)]:
    print(t0,t1,[db(S[n],t0,t1) for n in ['mix','drums','bass','vocals','other']])
print('0.5s steps bass dB 0-12:',[db(S['bass'],t,t+.5) for t in np.arange(0,12,.5)])
print('1s-around-boundaries 0.25 steps mix:')
for b in [10.4,12.3,15.46,16.7,18.3]:
    print(b,{n:[db(S[n],t,t+.25) for t in np.arange(b-1,b+1,.25)] for n in ['mix','drums','bass','vocals','other']})
# peaks
for n in ['mix']:
    z=S[n][:20*s];print('mix peak 0-10',20*np.log10(abs(z[:10*s]).max()),'10-20',20*np.log10(abs(z[10*s:]).max()))
    print('time of peak',np.abs(z).argmax()/s)
# loop regularity: onset env autocorr on mix and drums 0-10 (pre-vocal)
for n in ['mix','drums','other']:
    oe=librosa.onset.onset_strength(y=S[n][:int(10.3*s)].astype(np.float32),sr=s,hop_length=512)
    oe=oe-oe.mean();ac=np.correlate(oe,oe,'full')[len(oe)-1:];ac/=ac[0]
    fr=512/s;lags=np.arange(len(ac))*fr
    top=[(round(lags[i],2),round(ac[i],2)) for i in range(5,len(ac)-1) if ac[i]>ac[i-1] and ac[i]>ac[i+1] and ac[i]>0.2][:8]
    print(n,'ac peaks',top)
# bar waveform repeat: 4 beats = ~2.53s; cross-correlation of drums best lag 
z=S['drums'][:int(10.3*s)]
from scipy.signal import fftconvolve
seg=z[int(0.28*s):int(2.8*s)]
cc=fftconvolve(z,seg[::-1],'valid');nrm=np.sqrt(np.convolve(z**2,np.ones(len(seg)),'valid'))*np.linalg.norm(seg)+1e-9
r=cc/nrm; ts=np.arange(len(r))/s
print('drum bar template corr peaks (t, r):',[(round(ts[i],2),round(r[i],2)) for i in range(1,len(r)-1) if r[i]>r[i-1] and r[i]>r[i+1] and r[i]>0.3][:8])
# centroid of transients; high-freq cutoff of the mix 0-10 vs 10-20
D=np.abs(librosa.stft(S['mix'][:20*s].astype(np.float32),n_fft=4096));f=librosa.fft_frequencies(sr=s,n_fft=4096)
for a,b in [(0,10),(10,20)]:
    m=D[:,int(a*s/1024):int(b*s/1024)].mean(1);cs=np.cumsum(m**2)/np.sum(m**2)
    print(a,b,'mean-spec 99%/99.9% energy Hz',f[np.searchsorted(cs,.99)],f[np.searchsorted(cs,.999)])
# band above 9k and 16k noise floor
m=D[:,:int(10*s/1024)].mean(1)
for lo,hi in [(5000,8000),(8000,10000),(10000,16000),(16000,20000)]:
    print(lo,hi,round(20*np.log10(m[(f>=lo)&(f<hi)].mean()+1e-9),1))
# stereo L/R
L=mix[:20*s,0];R=mix[:20*s,1];print('LR identical 0-10',np.abs(L[:10*s]-R[:10*s]).max())
# bright bursts
oe=librosa.onset.onset_strength(y=S['mix'][:20*s].astype(np.float32),sr=s)
hf=np.abs(librosa.stft(S['mix'][:20*s].astype(np.float32)))[f[:1025]>9000 if False else librosa.fft_frequencies(sr=s)>9000].sum(0)
t=librosa.times_like(hf,sr=s);i=np.argsort(hf)[::-1][:6];print('HF>9k top frames',sorted(np.round(t[i],2)))
