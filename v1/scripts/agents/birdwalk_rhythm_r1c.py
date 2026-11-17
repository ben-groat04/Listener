import numpy as np, librosa, soundfile as sf
D='/home/user/Listener/v1/data/t_birdwalk/'
y,sr=sf.read(D+'audio/song.wav'); y=y.mean(1) if y.ndim>1 else y
hop=256
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop); fr=sr/hop
secs=[(12.5,24),(25,47),(60,70),(71,83),(83.5,93.5),(94,119),(132,143),(157,170),(171,176),(177,188),(1,11),(48,59),(121,131)]
for a,b in secs:
    x=oe[int(a*fr):int(b*fr)]; x=x-x.mean()
    ac=np.correlate(x,x,'full')[len(x)-1:]; ac/=ac[0]
    lags=np.arange(len(ac))/fr
    m=(lags>0.3)&(lags<2.0)
    # top peaks
    from scipy.signal import find_peaks
    p,_=find_peaks(ac*m,height=0.1)
    top=sorted(p,key=lambda i:-ac[i])[:4]
    print(a,b,[(round(lags[i],3),round(60/lags[i],1),round(ac[i],2)) for i in top])
