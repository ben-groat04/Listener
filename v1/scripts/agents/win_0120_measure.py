import librosa,numpy as np,sys
d='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
for s in ['drums','bass','other']:
    y,sr=librosa.load(d+s+'.wav',sr=22050,offset=110,duration=40)
    oe=librosa.onset.onset_strength(y=y,sr=sr)
    on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,units='time')+110
    c=librosa.feature.spectral_centroid(y=y,sr=sr)[0]
    t=librosa.times_like(c,sr=sr)+110
    print(s,'onsets 120-140:',len(on[(on>=120)&(on<140)]),'centroid 110-120/120-140/140-150:',[round(float(c[(t>=a)&(t<b)].mean())) for a,b in[(110,120),(120,140),(140,150)]])
    if s=='drums': print(np.round(on[(on>=120)&(on<124)],2)); 
    if s=='bass':
        f0,_,_=librosa.pyin(y[:sr*40],fmin=30,fmax=200,sr=sr); tt=librosa.times_like(f0,sr=sr)+110
        for a in range(120,140,4):
            m=(tt>=a)&(tt<a+4)&~np.isnan(f0); print('bass f0',a,round(float(np.median(f0[m])),1) if m.any() else None)
