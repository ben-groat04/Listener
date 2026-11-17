import numpy as np, soundfile as sf, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/'
T0,T1=180.,200.
mix,sr=sf.read(D+'audio/song.wav',always_2d=True)
seg=mix[int(T0*sr):int(T1*sr)]
print('sr',sr,'ch',mix.shape[1])
print('peak dB',20*np.log10(np.abs(seg).max()),'rms',20*np.log10(np.sqrt((seg**2).mean())),'n>=.999',(np.abs(seg)>=.999).sum())
if seg.shape[1]>1: print('LRcorr',np.corrcoef(seg[:,0],seg[:,1])[0,1])
m=seg.mean(1)
S=np.abs(librosa.stft(m,n_fft=2048))**2;f=librosa.fft_frequencies(sr=sr,n_fft=2048);tot=S.sum()
for a,b in [(0,150),(150,2000),(2000,8000),(8000,24000)]:
    print('band',a,b,round(10*np.log10(S[(f>=a)&(f<b)].sum()/tot),1))
print('centroid',librosa.feature.spectral_centroid(S=np.sqrt(S),sr=sr).mean())
st={}
for n in ['vocals','drums','bass','other']:
    x,s=sf.read(D+f'stems_raw/htdemucs/song/{n}.wav',always_2d=True);st[n]=x.mean(1)
def env(x,hop=0.01):
    h=int(sr*hop);n=len(x)//h
    return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
E={n:env(st[n]) for n in st};E['mix']=env(mix.mean(1))
def runs(e,thr,a,b,above=True):
    v=(e[int(a*100):int(b*100)]>thr);
    if not above:v=~v
    out=[];s=None
    for i,k in enumerate(v):
        if k and s is None:s=i
        if not k and s is not None:out.append((round(a+s/100,2),round(a+i/100,2)));s=None
    if s is not None:out.append((round(a+s/100,2),b))
    return out
for n in ['bass','vocals']:
    print(n,'below -45 runs>=0.15s:',[r for r in runs(E[n],-45,T0-3,T1+3,False) if r[1]-r[0]>=0.15])
def mean(n,a,b):return round(float(np.mean(E[n][int(a*100):int(b*100)])),1)
print('0.5s means every 1s: t mix voc drums bass other')
for t in np.arange(T0-1,T1+1.5,1.0):
    print(round(t,1),[mean(n,t,t+0.5) for n in ['mix','vocals','drums','bass','other']])
# bass pitch/lowest
# drum onsets
d=st['drums'];
on=librosa.onset.onset_detect(y=d[int((T0)*sr):int(T1*sr)],sr=sr,units='time',backtrack=False)
print('n drum onsets',len(on),'IOI pct',np.percentile(np.diff(on),[10,50,90]))
# kick low band
import scipy.signal as ss
sos=ss.butter(4,[35/(sr/2),110/(sr/2)],'band',output='sos');lo=ss.sosfiltfilt(sos,d[int(T0*sr):int(T1*sr)])
eo=np.abs(ss.hilbert(lo));eo=ss.savgol_filter(eo,201,2) if False else eo
env2=librosa.feature.rms(y=lo,frame_length=1024,hop_length=256)[0]
pk,_=ss.find_peaks(env2,height=env2.max()*0.35,distance=int(0.09*sr/256))
kt=pk*256/sr;ioi=np.diff(kt)
print('kicks',len(kt),'IOI pct',np.percentile(ioi,[10,50,90]).round(3))
beat=0.627
for per,name in [(0.627,'tracker beat'),(0.627/2,'half-beat 8th'),(0.627/4,'16th')]:
    ph=np.arange(0,per,0.005);best=None
    for p in ph:
        dev=((kt-p+per/2)%per)-per/2
        r=np.sqrt((dev**2).mean())
        if best is None or r<best[0]:best=(r,p)
    print(name,per,'rms dev ms',round(best[0]*1000,1),'random',round(per/np.sqrt(12)*1000,1))
# loop regularity: envelope correlation at 4 bars? bar=2.508s
for n in ['drums','bass','other','vocals']:
    e=E[n][int(T0*100):int(T1*100)];
    out=[]
    for lagb in [4,8,16]:
        L=int(lagb*0.627*100);out.append(round(float(np.corrcoef(e[:-L],e[L:])[0,1]),2))
    print('loop corr',n,out)
# end of window not needed
# bass band: spectral peak of bass stem in on segments
for a,b in [(183,185.5),(186,188.5),(192,194),(195,197)]:
    x=st['bass'][int(a*sr):int(b*sr)];F=np.abs(np.fft.rfft(x*np.hanning(len(x))));fr=np.fft.rfftfreq(len(x),1/sr)
    msk=(fr>25)&(fr<400);print('bass peak',a,b,round(fr[msk][F[msk].argmax()],1))
# 4-10k band of stems per 4s
for n in ['drums','other','vocals']:
    x=st[n][int(T0*sr):int(T1*sr)]
    S2=np.abs(librosa.stft(x,n_fft=2048))**2;ff=librosa.fft_frequencies(sr=sr,n_fft=2048)
    print(n,'4-10k dB per 4s',[round(10*np.log10(S2[(ff>4000)&(ff<10000)][:,i:i+int(4*sr/512)].sum()+1e-12),1) for i in range(0,S2.shape[1],int(4*sr/512))])
print('--- boundaries (0.5s before / after) ---')
for t in [183.05,188.73,189.62,191.9,193.2,193.81,195.09,197.5,199.58]:
    print(t,{n:(mean(n,t-0.5,t),mean(n,t,t+0.5)) for n in ['mix','drums','bass','vocals','other']})
print('min mix 0.25s means',min((mean('mix',t,t+0.25),t) for t in np.arange(180,200,0.25)))
for a,b in [(193.5,195.2)]:
    print('vocal 10ms min',E['vocals'][int(a*100):int(b*100)].min(), 'mix',E['mix'][int(a*100):int(b*100)].min())
print('other 1s means 190-198',[mean('other',t,t+1) for t in range(190,199)])
