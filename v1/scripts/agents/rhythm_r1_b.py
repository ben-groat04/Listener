import numpy as np, librosa, json, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050; hop=32; fr=sr/hop
dr,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)
S=np.abs(librosa.stft(dr,n_fft=1024,hop_length=hop))
f=librosa.fft_frequencies(sr=sr,n_fft=1024)
def band(lo,hi):
    m=(f>=lo)&(f<hi); e=np.log1p(30*S[m].sum(0)); d=np.maximum(np.diff(e,prepend=e[0]),0); return d
bands={'kick':(35,110),'snaretone':(150,400),'crack':(1500,5000),'hat':(6000,10000)}
env={k:band(*v) for k,v in bands.items()}
np.save('/tmp/dummy.npy',0)
tot=sum(env[k]/env[k].std() for k in env)
def acf(x,maxlag):
    x=x-x.mean(); n=len(x); F=np.fft.rfft(x,2*n); a=np.fft.irfft(F*np.conj(F))[:n]; a/=a[0]; return a[:maxlag]
seg=tot[int(30*fr):int(215*fr)]
a=acf(seg,int(12*fr)); lags=np.arange(len(a))/fr
for k in [1,2,4,8,16]:
    L0=0.637*k; w=(lags>L0*0.985)&(lags<L0*1.015); i=np.argmax(np.where(w,a,-9)); 
    # parabolic
    y0,y1,y2=a[i-1],a[i],a[i+1]; d=0.5*(y0-y2)/(y0-2*y1+y2); lag=(i+d)/fr
    print(k,'beats lag',round(lag,4),'->beat',round(lag/k,4),'bpm',round(60*k/lag,2),'r',round(a[i],3))
np.save('/tmp/tot.npy',tot)
