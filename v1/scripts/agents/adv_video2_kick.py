import numpy as np,librosa,json,scipy.signal as ss
D='stems_raw/htdemucs/song/'
d,sr=librosa.load(D+'drums.wav',sr=22050)
hop=128
S=np.abs(librosa.stft(d,n_fft=2048,hop_length=hop))
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
k=S[(f>30)&(f<120)].sum(0)
ke=np.maximum(np.diff(k,prepend=0),0)
pk,_=ss.find_peaks(ke,height=np.percentile(ke,90),distance=int(0.15*sr/hop))
on=pk*hop/sr
def ph(a,b,P=0.5):
    o=on[(on>a)&(on<b)]
    if len(o)<3: return len(o)
    return len(o),np.round(np.median(np.diff(o)),3),np.round(np.percentile(np.mod(o-88.61,P)/P,[10,50,90]),2)
for a,b in [(30,70),(88.7,100),(100,156),(160,210),(220,276)]: print(a,b,ph(a,b))
o=librosa.onset.onset_strength(y=d,sr=sr,hop_length=hop)
for a,b in [(30,85),(90,150),(160,210),(220,290)]:
    seg=o[int(a*sr/hop):int(b*sr/hop)]
    ac=librosa.autocorrelate(seg-seg.mean());lags=np.arange(len(ac))*hop/sr
    m=(lags>0.2)&(lags<1.6);i=np.argmax(ac*m);print(a,b,'ac lag',round(lags[i],3), round(60/lags[i],1))
