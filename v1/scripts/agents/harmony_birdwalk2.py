import librosa, numpy as np
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
names=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
t,m=np.load('/tmp/bass_midi.npy')
ok=np.isfinite(m)
print('bass midi hist (octave-specific):')
h=np.bincount(np.round(m[ok]).astype(int)); 
for k in np.nonzero(h)[0]:
    if h[k]>40: print(k,names[k%12],h[k])
# bass median pitch in 1s bins of A-ish; fractional
print('bass median cents vs A1(33):',np.median(m[ok&(np.abs(m-33)<1.5)])-33)
# other stem chroma (CQT, no bass), per section
y,sr=librosa.load(D+'other.wav',sr=22050,mono=True)
C=np.abs(librosa.cqt(y,sr=sr,hop_length=512,fmin=librosa.note_to_hz('C2'),n_bins=72,bins_per_octave=12))
ch=librosa.feature.chroma_cqt(C=C,sr=sr) if False else None
chroma=librosa.feature.chroma_cqt(y=y,sr=sr,hop_length=512)
tt=librosa.times_like(chroma,sr=sr,hop_length=512)
rms=librosa.feature.rms(y=y,hop_length=512)[0]
for a,b in [(0,12),(12,47),(47,60),(60,83),(83,92),(92,100),(100,131),(131,144),(144,155),(155,168),(168,188)]:
    s=(tt>=a)&(tt<b); w=rms[s]**2
    v=(chroma[:,s]*w).sum(1)/w.sum(); v/=v.max()
    print(a,b,' '.join(f'{names[i]}:{v[i]:.2f}' for i in np.argsort(-v)[:6]))
# vocal pitch histogram whole song
y,sr=librosa.load(D+'vocals.wav',sr=22050,mono=True)
f0,vf,vp=librosa.pyin(y,fmin=70,fmax=700,sr=sr,frame_length=2048,hop_length=512)
tv=librosa.times_like(f0,sr=sr,hop_length=512)
mv=12*np.log2(f0/440)+69
np.save('/tmp/voc_midi.npy',np.vstack([tv,mv]))
for a,b in [(0,12),(12,24),(24,40),(40,47),(47,83),(83,100),(100,131),(131,144),(144,155),(155,168)]:
    s=(tv>=a)&(tv<b)&np.isfinite(mv)
    hh=np.bincount(np.round(mv[s]).astype(int)%12,minlength=12);hh=hh/max(hh.sum(),1)
    print('voc',a,b,s.sum(),'median',np.median(mv[s]) if s.sum() else None,' '.join(f'{names[i]}:{hh[i]:.2f}' for i in np.argsort(-hh)[:5]))
