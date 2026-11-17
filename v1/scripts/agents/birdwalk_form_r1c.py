import numpy as np, soundfile as sf
from scipy.signal import welch
D='/home/user/Listener/v1/data/t_birdwalk/'
m,sr=sf.read(D+'audio/song.wav'); x=m.mean(1)
h=int(.01*sr); k=len(x)//h
e=20*np.log10(np.sqrt((x[:k*h].reshape(k,h)**2).mean(1))+1e-9)
# gaps: 10ms frames > 20 dB below the median of the surrounding 200 ms, excluding the final fade
cuts=[]
for i in range(20,k-20):
    ctx=np.median(np.r_[e[i-20:i-3],e[i+3:i+20]])
    if e[i]<ctx-20 and ctx>-30 and i*0.01<175: cuts.append(round(i*.01,2))
# merge
mg=[]
for c in cuts:
    if not mg or c-mg[-1][-1]>0.15: mg.append([c])
    else: mg[-1].append(c)
print('mix gaps (start,len s):',[(f'{int(a[0]//60)}:{a[0]%60:05.2f}',round(a[-1]-a[0]+.01,2)) for a in mg])
f,P=welch(x,sr,nperseg=8192)
tot=P.sum()
for lo,hi in [(0,60),(60,200),(200,800),(800,3000),(3000,6000),(6000,10000),(10000,16000),(16000,22050)]:
    print(lo,hi,round(10*np.log10(P[(f>=lo)&(f<hi)].sum()/tot+1e-12),1),'dB rel total')
# true-ish peak via 4x oversample
from scipy.signal import resample_poly
tp=np.abs(resample_poly(m[:,0],4,1)).max(); print('true peak L approx dBFS',20*np.log10(tp))
print('frames at >=-0.1 dBFS sample',int((np.abs(m)>0.99).any(1).sum()))
# crest
print('crest dB',20*np.log10(np.abs(m).max()/np.sqrt((m**2).mean())))
# loop regularity: other stem, similarity of bar (1.556s) to bars 1,2,4,8 later in the 0:47-0:59 passage
o,_=sf.read(D+'stems_raw/htdemucs/song/other.wav'); o=o.mean(1)
import librosa
for a,b in [(47.8,58.6),(121,131),(2*60+36,2*60+46),(60,70)]:
    seg=o[int(a*sr):int(b*sr)]
    S=np.abs(librosa.feature.melspectrogram(y=seg,sr=sr,n_mels=64,hop_length=441))
    S=np.log1p(S); 
    bar=int(1.556/0.01)
    cs=[]
    for lag in [bar,2*bar,4*bar]:
        if lag<S.shape[1]-50:
            A=S[:,:S.shape[1]-lag].flatten(); B=S[:,lag:].flatten(); cs.append((lag*.01,round(np.corrcoef(A,B)[0,1],3)))
    print(a,b,'other mel self-corr at bar multiples',cs)
