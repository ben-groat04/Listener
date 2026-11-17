import numpy as np, soundfile as sf, librosa, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
def ld(p):
    y,sr=sf.read(p); 
    return (y.mean(1) if y.ndim>1 else y), sr, y
mix,sr,raw=ld(D+'audio/song.wav')
st={k:ld(D+f'stems_raw/htdemucs/song/{k}.wav')[0] for k in ['vocals','drums','bass','other']}
hop=int(sr*0.01)
def env(x):
    n=len(x)//hop; return 20*np.log10(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-9)
E={'mix':env(mix),**{k:env(v) for k,v in st.items()}}
def m(k,a,b): return E[k][int(a*100):int(b*100)].mean()
print('sr',sr,'dur',len(mix)/sr)
print('peak 200-220', np.abs(raw[200*sr:220*sr]).max(), 'n>=.999',(np.abs(raw[200*sr:220*sr])>=0.999).sum(),'rms',20*np.log10(np.sqrt((mix[200*sr:220*sr]**2).mean())))
if raw.ndim>1: print('LR corr',np.corrcoef(raw[200*sr:220*sr,0],raw[200*sr:220*sr,1])[0,1])
# 1s means each stem
for t in range(200,240,1):
    print(t, ' '.join(f'{k}:{m(k,t,t+1):6.1f}' for k in E))
import sys
# boundaries
bs=[203.0,204.6,208.4,214.0,215.0,216.0,218.9,222.9,229.0]
for b in [200.0,202.1,204.6,208.4,210.4,214.2,215.5,216.0,218.9]:
    print('B',b,' | '.join(f'{k} {m(k,b-.5,b):.1f}->{m(k,b,b+.5):.1f}' for k in E))
# bass off segments in 200-240 (below -45)
for k in ['bass','vocals']:
    on=E[k]<-45; segs=[];s=None
    for i in range(20000,len(on)):
        if on[i] and s is None: s=i
        if not on[i] and s is not None:
            if i-s>=15: segs.append((s/100,i/100))
            s=None
    print(k,'off segs',segs)
# drums onsets
d=st['drums'][200*sr:220*sr]
oe=librosa.onset.onset_strength(y=d,sr=sr,hop_length=512)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=512,units='time')
ioi=np.diff(on);print('drum onsets',len(on),np.percentile(ioi,[10,50,90]))
# kick: low band
import scipy.signal as ss
sos=ss.butter(4,[35,110],'band',fs=sr,output='sos');z=ss.sosfiltfilt(sos,np.nan_to_num(st['drums'][200*sr:220*sr].astype(float)))
e=np.convolve(np.abs(z),np.ones(441)/441,'same');pk,_=ss.find_peaks(e,height=e.max()*0.3,distance=int(sr*0.08));t=pk/sr
print('kick-band n',len(t),'IOI pct',np.percentile(np.diff(t),[10,50,90]))
for per,nm in [(0.627,'beat'),(0.3135,'8th'),(0.1568,'16th')]:
    best=min(np.sqrt((((t-ph+per/2)%per-per/2)**2).mean()) for ph in np.arange(0,per,0.005));print(nm,best*1000,per/np.sqrt(12)*1000)
# bands
S=np.abs(librosa.stft(mix[200*sr:220*sr],n_fft=4096))**2; f=librosa.fft_frequencies(sr=sr,n_fft=4096)
tot=S.sum()
for lo,hi in [(0,150),(150,2000),(2000,8000),(8000,24000)]:
    print(lo,hi,10*np.log10(S[(f>=lo)&(f<hi)].sum()/tot))
print('centroid',librosa.feature.spectral_centroid(S=np.sqrt(S),sr=sr).mean())
for k in ['other','drums','vocals']:
    for a in range(200,220,4):
        x=st[k][a*sr:(a+4)*sr];S2=np.abs(librosa.stft(x,n_fft=2048))**2;f2=librosa.fft_frequencies(sr=sr,n_fft=2048)
        print(k,a,'4-10k dB',round(10*np.log10(S2[(f2>=4000)&(f2<10000)].sum(1).mean()+1e-12),1),end='; ')
    print()
# loop regularity
def corr(x,lag):
    return np.corrcoef(x[:-lag],x[lag:])[0,1]
for k in E:
    seg=E[k][19000:24000]
    seg=np.convolve(seg,np.ones(10)/10,'same')
    print(k,'lag4/8/16 beats',[round(corr(seg,int(100*0.627*n)),2) for n in (4,8,16)])
# end of track
for k in E:
    x=E[k][-300:]; print('END',k,'last 3s min/max',x.min().round(1),x.max().round(1))
e=E['mix'];idx=np.where(e>-60)[0];print('last >-60dB',idx[-1]/100, 'last >-40',np.where(e>-40)[0][-1]/100)
