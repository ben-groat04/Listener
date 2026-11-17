import numpy as np, soundfile as sf, librosa, json
D='/home/user/Listener/v1/data/video1/'
x,sr=sf.read(D+'audio/song.wav'); print(x.shape,sr)
L,R=x[:,0],x[:,1]; M=(L+R)/2; S=(L-R)/2
def db(v): return 20*np.log10(v+1e-9)
print('peak',db(np.abs(x).max()),'rms',db(np.sqrt((x**2).mean())))
# crest per section
secs=[(0,15),(15,66),(66,76),(76,88),(88,109),(109,119),(119,134),(134,159),(159,188)]
for a,b in secs:
    s=x[int(a*sr):int(b*sr)]; 
    r=np.sqrt((s**2).mean()); pk=np.abs(s).max()
    m=M[int(a*sr):int(b*sr)]; sd=S[int(a*sr):int(b*sr)]
    c=np.corrcoef(L[int(a*sr):int(b*sr)],R[int(a*sr):int(b*sr)])[0,1]
    # short-term loudness range: 400ms rms percentiles
    fr=librosa.feature.rms(y=M[int(a*sr):int(b*sr)],frame_length=int(.4*sr),hop_length=int(.1*sr))[0]
    p=np.percentile(db(fr),[10,90])
    # band energy
    Sp=np.abs(librosa.stft(M[int(a*sr):int(b*sr)],n_fft=4096))**2; f=librosa.fft_frequencies(sr=sr,n_fft=4096)
    bands=[(20,60),(60,250),(250,1000),(1000,4000),(4000,8000),(8000,16000),(16000,22000)]
    be=[Sp[(f>=lo)&(f<hi)].sum() for lo,hi in bands]; be=np.array(be)/sum(be)
    print(f'{a}-{b}s crest {db(pk/r):.1f}dB rms {db(r):.1f} LR corr {c:.2f} S/M {db(np.sqrt((sd**2).mean())/np.sqrt((m**2).mean())):.1f}dB P10/P90 {p[0]:.1f}/{p[1]:.1f} bands%',np.round(be*100,1))
# per stem stats
for n in ['vocals','drums','bass','other']:
    y,_=sf.read(D+f'stems_raw/htdemucs/song/{n}.wav'); l,r=y[:,0],y[:,1]
    c=np.corrcoef(l,r)[0,1]; m=(l+r)/2;s=(l-r)/2
    sp=np.abs(librosa.stft(m,n_fft=4096)).mean(1); f=librosa.fft_frequencies(sr=sr,n_fft=4096)
    cs=np.cumsum(sp**2)/np.sum(sp**2); r95=f[np.searchsorted(cs,.95)]; r99=f[np.searchsorted(cs,.99)]
    cen=librosa.feature.spectral_centroid(y=m,sr=sr).mean()
    print(n,'rms',db(np.sqrt((y**2).mean())),'corr',round(c,2),'S/M',round(db(np.sqrt((s**2).mean())/np.sqrt((m**2).mean())),1),'95%',r95,'99%',r99,'cent',round(cen))
