import numpy as np, librosa, json, sys
D='/home/user/Listener/v1/data/video2/'
y,sr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050)
hop=256
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
fps=sr/hop
def ac_period(seg):
    a=librosa.autocorrelate(seg-seg.mean()); a/=a[0]
    lo,hi=int(0.2*fps),int(4.5*fps)
    return a,lo,hi
for st in range(30,306,20):
    seg=oe[int(st*fps):int((st+20)*fps)]
    if len(seg)<fps*10: continue
    a,lo,hi=ac_period(seg)
    pk=[i for i in range(lo,hi) if a[i]>a[i-1] and a[i]>=a[i+1] and a[i]>0.15]
    top=sorted(pk,key=lambda i:-a[i])[:5]
    print(st,[(round(i/fps,3),round(a[i],2)) for i in sorted(top)])
    # tempogram-ish
    tg=librosa.feature.tempo(onset_envelope=seg,sr=sr,hop_length=hop,aggregate=None)
    print('   tempo',round(float(np.median(tg)),1))
# kick vs snare band onset timeline in a steady section 150-170
b=np.array(json.load(open(D+'audio_features/beat_times.json')) if True else [])
print(type(b), b[:3] if b.ndim else b)
