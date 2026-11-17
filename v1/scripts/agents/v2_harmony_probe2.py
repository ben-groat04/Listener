import librosa,numpy as np
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
N=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
sr=22050
bass,_=librosa.load(D+'bass.wav',sr=sr);oth,_=librosa.load(D+'other.wav',sr=sr);dr,_=librosa.load(D+'drums.wav',sr=sr);mix,_=librosa.load('/home/user/Listener/v1/data/video2/audio/song.wav',sr=sr)
print('tuning offset (semitones, mix):',librosa.estimate_tuning(y=mix,sr=sr))
# exact bass-root change times 0:28-4:40 via 0.5s frames, dominant bass pitch class (low band)
hop=512
C=librosa.feature.chroma_cqt(y=bass,sr=sr,hop_length=hop,fmin=32.7,n_octaves=4)
t=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=hop)
roots=C.argmax(0)
# median filter
from scipy.ndimage import median_filter
r=median_filter(roots,size=43)
ch=[0]+[i for i in range(1,len(r)) if r[i]!=r[i-1]]
segs=[(t[a],N[r[a]]) for a in ch if 28<t[a]<290]
print(' '.join('%.1f:%s'%(x,n) for x,n in segs))
# tempo via drums onset autocorr 3:00-3:40
oe=librosa.onset.onset_strength(y=dr[int(180*sr):int(220*sr)],sr=sr,hop_length=hop)
ac=librosa.autocorrelate(oe-oe.mean());ac/=ac[0]
lag=np.arange(len(ac))*hop/sr
for lo,hi in [(0.3,0.45),(0.45,0.6),(0.9,1.1),(1.9,2.1)]:
    m=(lag>=lo)&(lag<hi);print('ac peak',lo,hi,lag[m][ac[m].argmax()],ac[m].max())
pass
# D vs D# (third of B), thirds in specific spans on other+mix
def ch(y,a,b):
    c=librosa.feature.chroma_cqt(y=y[int(a*sr):int(b*sr)],sr=sr).mean(1);return c/c.max()
for name,a,b in [('0:53-0:56 B',53,56),('1:20-1:24 B',80,84),('2:20-2:24 B',140,144),('2:36-2:40 B',156,160),('final 5:01-5:02',301.1,302.2),('final hit 5:02.3-5:02.9',302.34,302.9),('3:00-3:04',180,184),('4:49-4:55',289,295)]:
    c=ch(mix,a,b);print(name,'mix D %.2f D# %.2f F# %.2f B %.2f'%(c[2],c[3],c[6],c[11]))
# lead in other 4:28-4:38 : top pitches
y=oth[int(268*sr):int(278*sr)]
f0,v,p=librosa.pyin(y,fmin=200,fmax=1500,sr=sr,hop_length=1024)
mid=librosa.hz_to_midi(f0[v]);print('other 4:28-4:38 voiced frac',v.mean(),'pitch classes',np.bincount((np.round(mid)%12).astype(int),minlength=12))
vo,_=librosa.load(D+'vocals.wav',sr=sr);y=vo[int(268*sr):int(278*sr)]
f0,v,p=librosa.pyin(y,fmin=200,fmax=1500,sr=sr,hop_length=1024);print('vocals voiced frac',v.mean())
