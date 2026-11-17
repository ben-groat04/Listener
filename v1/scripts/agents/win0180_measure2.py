import numpy as np, soundfile as sf
from scipy.signal import find_peaks
D='/home/user/Listener/v1/data/t_birdwalk/'
y,sr=sf.read(D+'audio/song.wav'); m=y.mean(1)
print('file peak at',np.argmax(np.abs(y).max(1))/sr, 'n samples >=0.999:',(np.abs(y)>=0.999).sum())
for a,b in [(170,180),(180,188.15)]:
    print(a,b,'peak dBFS',20*np.log10(np.abs(y[int(a*sr):int(b*sr)]).max()))
n=int(sr*0.01); k=len(m)//n
e=20*np.log10(np.sqrt((m[:k*n].reshape(k,n)**2).mean(1))+1e-9)
# dips: 10ms mix below local (±0.3s median) -12 dB
from scipy.ndimage import median_filter
med=median_filter(e,size=61)
dips=np.where((e<med-12)&(e<-28))[0]
# group
g=[];
for i in dips:
    if g and i-g[-1][-1]<=3: g[-1].append(i)
    else: g.append([i])
for gg in g:
    t=gg[0]/100
    if t>=176: print('dip %.2f-%.2f min %.1f dB (local median %.1f)'%(t,gg[-1]/100+.01,e[gg].min(),med[gg[0]]))
# mix hit peaks 180-188
pk,_=find_peaks(e,prominence=6)
print('mix env peaks 180+',[(round(i/100,2),round(e[i],1)) for i in pk if i>=17900])
# kick grid fit on onsets from earlier; test bar repetition: correlate 10ms env of 1.58s (4 beats at 0.395)
beat=0.3947
lags=np.arange(0.3,4.5,0.005)
a=e[17600:18100]-e[17600:18100].mean()
# autocorrelation of onset-ish env diff
d=np.maximum(np.diff(e[17000:18400]),0)
ac=np.correlate(d-d.mean(),d-d.mean(),'full')[len(d)-1:]; ac/=ac[0]
for L in [0.395,0.79,1.185,1.58,3.16,6.32]:
    i=int(round(L*100)); print('onset-env autocorr at',L,round(ac[i-2:i+3].max(),2))
