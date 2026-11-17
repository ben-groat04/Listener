import numpy as np, librosa
D='/home/user/Listener/v1/data/video2/'
y,sr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050)
def bands(lo,hi):
    S=np.abs(librosa.stft(y,n_fft=1024,hop_length=128))
    f=librosa.fft_frequencies(sr=sr,n_fft=1024)
    b=S[(f>=lo)&(f<hi)].sum(0)
    return librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[(f>=lo)&(f<hi)]+1e-6),sr=sr,hop_length=128), 
fps=sr/128
for name,(lo,hi) in dict(kick=(30,150),mid=(150,2000),hat=(5000,10000)).items():
    S=np.abs(librosa.stft(y,n_fft=1024,hop_length=128)); f=librosa.fft_frequencies(sr=sr,n_fft=1024)
    e=librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[(f>=lo)&(f<hi)]**2+1e-9),sr=sr,hop_length=128)
    for (a,b) in [(100,160),(200,260)]:
        seg=e[int(a*fps):int(b*fps)]
        t=np.arange(len(seg))/fps+a
        ph=(t%2.0)
        h,_=np.histogram(ph,bins=32,range=(0,2),weights=seg)  # 1/16 of 2s = 0.0625
        h=h/h.max()
        print(name,a,' '.join(f'{v:.1f}' for v in h))
