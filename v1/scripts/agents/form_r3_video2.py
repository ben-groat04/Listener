import numpy as np, soundfile as sf
d='data/video2/stems_raw/htdemucs/song/'
def rms(n,t0,t1,w=0.5):
    x,sr=sf.read(d+n+'.wav'); x=x.mean(1) if x.ndim>1 else x
    return [(round(t,1),round(20*np.log10(np.sqrt(np.mean(x[int(t*sr):int((t+w)*sr)]**2))+1e-9),1)) for t in np.arange(t0,t1,w)]
print('bass 4:30-5:04',[v for _,v in rms('bass',270,304)])
print('drums 1:22-1:30',rms('drums',82,90))
print('bass 1:22-1:30',rms('bass',82,90))
x,sr=sf.read('data/video2/audio/song.wav'); x=x.mean(1) if x.ndim>1 else x
print('dur',len(x)/sr)
for a,b in [(150,156),(156,162),(264,270),(270,276),(276,282),(294,300)]:
    print(a,round(20*np.log10(np.sqrt(np.mean(x[a*sr:b*sr]**2))),1))
