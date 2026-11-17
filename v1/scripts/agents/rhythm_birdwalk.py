import sys, json, numpy as np, librosa
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
sr=22050
out={}
for s in ['drums','bass','other','vocals']:
    y,_=librosa.load(D+s+'.wav',sr=sr,mono=True)
    oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
    t=librosa.times_like(oe,sr=sr,hop_length=256)
    on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time',backtrack=False)
    np.save(f'/tmp/on_{s}.npy',on); np.save(f'/tmp/oe_{s}.npy',oe)
    print(s,len(on))
    # tempogram windows
    for a in range(0,180,20):
        seg=oe[(t>=a)&(t<a+20)]
        ac=librosa.autocorrelate(seg-seg.mean(),max_size=int(2.5*sr/256))
        lags=np.arange(len(ac))*256/sr
        m=(lags>0.25)
        k=np.argsort(ac[m])[::-1]
        # top peaks local
        pk=[i for i in range(1,len(ac)-1) if m[i] and ac[i]>ac[i-1] and ac[i]>ac[i+1]]
        pk=sorted(pk,key=lambda i:-ac[i])[:4]
        print(' ',s,a,[round(lags[i],3) for i in pk])
