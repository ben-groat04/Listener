import numpy as np, librosa, soundfile as sf
P='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
v,sr=sf.read(P+'vocals.wav'); v=v.mean(1)
d,_=sf.read(P+'drums.wav'); d=d.mean(1)
hop=256
ev=librosa.onset.onset_strength(y=v,sr=sr,hop_length=hop); 
vo=librosa.onset.onset_detect(onset_envelope=ev,sr=sr,hop_length=hop,units='time')
do=librosa.onset.onset_detect(y=d,sr=sr,hop_length=hop,units='time',delta=0.3)
for a,b in [(1,12),(48,59),(121,131),(144,155),(25,47),(71,100)]:
    dd=do[(do>=a)&(do<b)]
    # keep only isolated hits (gap>1s) for sparse sections
    dd=[t for i,t in enumerate(dd) if (i==0 or t-dd[i-1]>0.6)]
    off=[]
    for t in dd:
        j=vo[np.argmin(abs(vo-t))]; off.append(j-t)
    off=np.array(off)
    print(a,b,'n=%d'%len(dd),'median voc-onset offset %.3f s'%np.median(off),'frac within 50ms %.2f'%np.mean(abs(off)<0.05),'frac within 100ms %.2f'%np.mean(abs(off)<0.1))
# chance level: random times
rng=np.random.default_rng(0); r=rng.uniform(48,59,500); off=[abs(vo[np.argmin(abs(vo-t))]-t) for t in r]; print('chance <50ms %.2f <100ms %.2f'%(np.mean(np.array(off)<0.05),np.mean(np.array(off)<0.1)))
