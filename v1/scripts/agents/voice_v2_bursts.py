import numpy as np, librosa, sys
y,sr=librosa.load('/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/vocals.wav',sr=16000,mono=True)
hop=800
rms=librosa.feature.rms(y=y,frame_length=1600,hop_length=hop)[0]
db=20*np.log10(rms+1e-9)
cen=librosa.feature.spectral_centroid(y=y,sr=sr,hop_length=hop)[0]
thr=-52
act=db>thr
segs=[];s=None
for i,a in enumerate(act):
    if a and s is None:s=i
    if not a and s is not None:
        if i-s>=3:segs.append((s*0.05,i*0.05,db[s:i].max(),np.median(cen[s:i])))
        s=None
# merge gaps<0.3
m=[]
for g in segs:
    if m and g[0]-m[-1][1]<0.3:m[-1]=(m[-1][0],g[1],max(m[-1][2],g[2]),m[-1][3])
    else:m.append(g)
f=lambda t:f"{int(t//60)}:{t%60:04.1f}"
for a,b,p,c in m:print(f(a),f(b),f"{b-a:.1f}s peak{p:.0f}dB cen{c:.0f}")
