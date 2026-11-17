import numpy as np, librosa
d='data/video1/stems_raw/htdemucs/song/'
dr,sr=librosa.load(d+'drums.wav',sr=22050)
B=0.7692; ref=134.0  # Rhythm's edge at position 2.0
for t in [135.0,138.2,141.2,144.1,147.5,150.5,27.9,31.7,28.0]:
    print('voice',t,'pos in Rhythm fold',round((2+(t-ref)/B)%4,2))
# drum onset-strength by fold position, drums low (<150) and high (>2k) bands, 2:15-2:47 and 0:33-1:15
S=np.abs(librosa.stft(dr,n_fft=1024,hop_length=256)); f=librosa.fft_frequencies(sr=sr,n_fft=1024); tt=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr,hop_length=256)
for name,m in [('low',f<150),('hi',f>2000)]:
    e=S[m].sum(0); o=np.maximum(0,np.diff(e,prepend=e[0]))
    for a,b in [(135,167),(33,75)]:
        sel=(tt>a)&(tt<b); pos=((2+(tt[sel]-ref)/B)%4)
        bins=np.floor(pos*2)/2; print(name,a,b,[ (k,round(o[sel][bins==k].sum()/max(1,(bins==k).sum())*1e3,2)) for k in np.arange(0,4,0.5)])
