import numpy as np, librosa, sys
D='/home/user/Listener/v1/data/video1/'
y,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=True)
hop=512
rms=librosa.feature.rms(y=y,hop_length=hop)[0]
db=20*np.log10(rms+1e-9); t=librosa.times_like(rms,sr=sr,hop_length=hop)
def show(a,b,step=0.1):
    print('--',a,b)
    for x in np.arange(a,b,step):
        i=np.searchsorted(t,x); print('%.2f %.1f'%(x,db[i]),end=' | ')
    print()
show(167.4,168.8,0.1); show(187.0,188.7,0.15); show(0,1.6,0.1)
# 1-s RMS envelope smoothed; list biggest 1s jumps
e=np.array([db[(t>=s)&(t<s+1)].mean() for s in range(int(t[-1]))])
d=np.diff(e); idx=np.argsort(-abs(d))[:12]
for i in sorted(idx): print('jump at %d:%02d %.1f -> %.1f'%((i+1)//60,(i+1)%60,e[i],e[i+1]))
# spectral centroid per 10s
c=librosa.feature.spectral_centroid(y=y,sr=sr,hop_length=hop)[0]
for s in range(0,188,10): print('%d:%02d cent %.0f rms %.1f'%(s//60,s%60,c[(t>=s)&(t<s+10)].mean(),db[(t>=s)&(t<s+10)].mean()))
