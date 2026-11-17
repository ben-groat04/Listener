import librosa, numpy as np, json, sys
D='/home/user/Listener/v1/data/video2/'
y,sr=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=22050)
beats=np.array(json.load(open(D+'audio_features/beat_times.json')) if True else [])
if isinstance(beats[0],dict): beats=np.array([b['t'] for b in beats])
rms=librosa.feature.rms(y=y,frame_length=1024,hop_length=256)[0]
t=librosa.frames_to_time(np.arange(len(rms)),sr=sr,hop_length=256)
db=20*np.log10(rms+1e-9)
def segs(a,b,thr):
    m=(t>=a)&(t<b); on=None; out=[]
    for ti,v in zip(t[m],db[m]>thr):
        if v and on is None: on=ti
        if not v and on is not None:
            if ti-on>0.15: out.append((round(on,2),round(ti,2)))
            on=None
    return out
for a,b,thr in [(208,262,-48),(262,300,-50)]:
    s=segs(a,b,thr); print(a,b,len(s)); print(s[:40])
    st=np.array([x[0] for x in s]); 
    if len(st)>2:
        print('IOI',np.round(np.diff(st),2)[:30])
        # phase vs beat
        ph=[(x-beats[np.argmin(abs(beats-x))]) for x in st]; print('offset to nearest beat',np.round(ph,2)[:30])
print('beat period',np.median(np.diff(beats)))
# pitch in speech vs chops
for a,b in [(65,70),(85,88),(110,116),(150,155),(215,222),(236,243)]:
    seg=y[int(a*sr):int(b*sr)]
    f0,vf,vp=librosa.pyin(seg,fmin=70,fmax=900,sr=sr)
    f=f0[~np.isnan(f0)]
    print(a,b,'voiced frac',round(vf.mean(),2),'median f0',round(np.median(f),1) if len(f) else None, 'p10-p90',np.round(np.percentile(f,[10,90]),0) if len(f) else None)
