import librosa,numpy as np,sys
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
def pc(y,sr,a,b):
    c=librosa.feature.chroma_cqt(y=y[int(a*sr):int(b*sr)],sr=sr).mean(1);c/=c.sum()
    return ' '.join(f"{n}:{v:.2f}" for n,v in zip('C C# D D# E F F# G G# A A# B'.split(),c))
y,sr=librosa.load('/home/user/Listener/v1/data/video1/audio/song.wav',sr=22050)
for a,b in [(160,168),(168,180),(180,188)]: print('mix',a,b,pc(y,sr,a,b))
yo,_=librosa.load(D+'other.wav',sr=sr)
for a,b in [(160,168),(168,180),(180,188)]: print('other',a,b,pc(yo,sr,a,b))
yd,_=librosa.load(D+'drums.wav',sr=sr)
for a,b in [(150,158),(160,168),(168,180),(180,188)]:
    s=yd[int(a*sr):int(b*sr)];o=librosa.onset.onset_detect(y=s,sr=sr,units='time');print('drums onsets/s',a,b,len(o)/(b-a), 'median ioi',np.median(np.diff(o)) if len(o)>2 else None)
    S=np.abs(librosa.stft(s));f=librosa.fft_frequencies(sr=sr);print(' centroid',librosa.feature.spectral_centroid(S=S,sr=sr).mean(),' hf(>5k) share',S[f>5000].sum()/S.sum())
yb,_=librosa.load(D+'bass.wav',sr=sr)
for a,b in [(160,168),(168,180)]:
    print('bass f0',a,b,np.nanmedian(librosa.pyin(yb[int(a*sr):int(b*sr)],fmin=30,fmax=200,sr=sr)[0]))
