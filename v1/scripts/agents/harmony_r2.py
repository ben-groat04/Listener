import librosa, numpy as np
D='/home/user/Listener/v1/data/video1/'
y,sr=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=22050,mono=True)
C=librosa.feature.chroma_cqt(y=y,sr=sr,hop_length=2048,n_chroma=12,tuning=0)
t=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=2048)
N='C C# D D# E F F# G G# A A# B'.split()
def seg(a,b):
    m=C[:,(t>=a)&(t<b)].mean(1); m=m/m[2]; return ' '.join(f'{N[i]}{m[i]:.2f}' for i in [2,3,4,5,6,7,9,10,11,0,1] )
for a,b in [(87,100),(168,188),(168,180),(180,188),(75,78),(127,131),(139,143),(145,150),(152,158),(62,75),(186,188.7),(0,8),(120,160)]:
    print(a,b,seg(a,b))
# tuning
print('tuning',librosa.estimate_tuning(y=y,sr=sr))
# chroma at sub hits
for s in [121.3,127.3,133.5,139.7]:
    print('subhit',s,seg(s,s+1.5))
# E vs F at hits: per-frame
# bar-periodicity of chroma: self-similarity at lag in 1:00-1:15
Cs=C[:,(t>=60)&(t<75)]; 
for lag in [0.77*4,0.77*8,0.77*16]:
    k=int(round(lag/(2048/sr)))
    a=Cs[:,:-k];b=Cs[:,k:]
    print('lag',lag,np.mean([np.corrcoef(a[:,i],b[:,i])[0,1] for i in range(a.shape[1])]))
