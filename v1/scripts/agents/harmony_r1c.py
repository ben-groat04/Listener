import librosa, numpy as np
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
for nm,(a,b) in {'drums 3:00-3:40':(180,220),'drums 1:00-1:40':(60,100),'drums 4:00-4:40':(240,280)}.items():
    y,sr=librosa.load(D+'drums.wav',sr=22050,offset=a,duration=b-a)
    oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
    ac=librosa.autocorrelate(oe-oe.mean()); ac/=ac[0]
    lags=np.arange(len(ac))*256/sr
    m=(lags>0.15)&(lags<4.5)
    idx=[i for i in np.argsort(ac*m)[::-1][:40]]
    # local maxima
    pk=[i for i in range(1,len(ac)-1) if m[i] and ac[i]>ac[i-1] and ac[i]>ac[i+1]]
    pk=sorted(pk,key=lambda i:-ac[i])[:6]
    print(nm,[(round(lags[i],3),round(ac[i],2)) for i in pk], 'bpm of top', [round(60/lags[i],1) for i in pk[:3]])
