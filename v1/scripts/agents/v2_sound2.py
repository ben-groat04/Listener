import numpy as np,librosa
D='/home/user/Listener/v1/data/video2/'
y,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=True)
S=np.abs(librosa.stft(y,n_fft=2048,hop_length=512))**2
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
fr=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr,hop_length=512)
for a in range(0,306,10):
    m=(fr>=a)&(fr<a+10)
    if not m.any():continue
    P=S[:,m].mean(1);c=np.cumsum(P)/P.sum()
    hi=10*np.log10(P[f>4000].sum()/P.sum()+1e-12)
    print('%d:%02d'%(a//60,a%60),'roll99 %5.0f'%f[np.searchsorted(c,.99)],'>4k %.1f dB'%hi,'cent %.0f'%(P*f).sum()/P.sum() if False else '')
# other stem centroid & hf
o,_=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=22050,mono=True)
So=np.abs(librosa.stft(o,n_fft=2048,hop_length=512))**2
for a in range(0,300,20):
    m=(fr>=a)&(fr<a+20);P=So[:,m].mean(1)
    print('other',a,'cent %.0f'%((P*f).sum()/P.sum()),'>2k %.1f'%(10*np.log10(P[f>2000].sum()/P.sum()+1e-12)))
