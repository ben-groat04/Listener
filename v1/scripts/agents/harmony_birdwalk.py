import librosa, numpy as np, json, sys
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def load(n): return librosa.load(D+n+'.wav',sr=22050,mono=True)
# bass pitch via pyin
y,sr=load('bass')
f0,vf,vp=librosa.pyin(y,fmin=28,fmax=200,sr=sr,frame_length=4096,hop_length=512)
t=librosa.times_like(f0,sr=sr,hop_length=512)
m=np.where(np.isfinite(f0),12*np.log2(f0/440)+69,np.nan)
np.save('/tmp/bass_midi.npy',np.vstack([t,m]))
def pcs(a,b):
    s=(t>=a)&(t<b)&np.isfinite(m)
    h=np.bincount(np.round(m[s]).astype(int)%12,minlength=12)
    return h/max(h.sum(),1), s.sum()
for a in range(0,188,10):
    h,n=pcs(a,a+10)
    top=np.argsort(-h)[:3]
    print(a,n,[(names[i],round(h[i],2)) for i in top])
