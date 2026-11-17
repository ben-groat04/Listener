import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_birdwalk/'
S=D+'stems_raw/htdemucs/song/'
t0,t1=118,142
def load(p):
    y,sr=librosa.load(p,sr=None,mono=False,offset=t0,duration=t1-t0); return y,sr
mix,sr=load(D+'audio/song.wav')
m=mix.mean(0) if mix.ndim>1 else mix
print('sr',sr,'sample peak 120-140 dBFS',20*np.log10(np.abs(mix[:,int(2*sr):int(22*sr)]).max()))
def env(y,sr,hop=0.01):
    h=int(sr*hop); n=len(y)//h
    return np.sqrt((y[:n*h].reshape(n,h)**2).mean(1)+1e-12)
def db(x): return 20*np.log10(x+1e-9)
e=env(m,sr)
print('mix level per 2s:',[round(db(np.sqrt((e[i:i+200]**2).mean())),1) for i in range(0,2400,200)])
for st in ['drums','bass','vocals','other']:
    y,s=librosa.load(S+st+'.wav',sr=None,offset=t0,duration=t1-t0)
    ev=env(y,s)
    print(st,'1s-RMS dB from 118:',[round(db(np.sqrt((ev[i:i+100]**2).mean())),0) for i in range(0,2400,100)])
    if st in('drums','bass'):
        on=librosa.onset.onset_detect(y=y,sr=s,units='time',backtrack=False,delta=0.15 if st=='drums' else 0.1)
        print(st,'onsets',[round(o+t0,2) for o in on])
        if st=='drums':
            lo=librosa.effects.preemphasis(y)  # placeholder
            from scipy.signal import butter,sosfilt
            k=sosfilt(butter(4,[40,120],'bp',fs=s,output='sos'),y)
            ke=env(k,s); 
            from scipy.signal import find_peaks
            p,_=find_peaks(ke,height=ke.max()*0.25,distance=20)
            kt=p/100+t0; print('kick-band peaks',[round(x,2) for x in kt])
            print('kick IOI',np.round(np.diff(kt),2))
