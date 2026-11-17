import sys,librosa,numpy as np
a,b=float(sys.argv[1]),float(sys.argv[2]);d='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
for s in ['drums','other']:
    y,sr=librosa.load(d+s+'.wav',sr=22050,offset=a,duration=b-a)
    o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+a
    print(s,len(o),'onsets; median IOI',np.round(np.median(np.diff(o)),3))
    if s=='drums':
        S=np.abs(librosa.stft(y))**2;f=librosa.fft_frequencies(sr=sr)
        t=librosa.frames_to_time(range(S.shape[1]),sr=sr)+a
        for lo,hi,n in[(30,150,'kick'),(150,400,'snare-body'),(5000,10000,'hat')]:
            e=S[(f>=lo)&(f<hi)].sum(0);print(n,'per-5s dB',[round(10*np.log10(e[(t>=x)&(t<x+5)].mean()+1e-9),1) for x in range(int(a),int(b),5)])
            if n=='kick':
                oo=librosa.onset.onset_detect(onset_envelope=np.log1p(e),sr=sr,units='time')+a;print('kick onsets',np.round(oo,2)[:40])
    else:
        c=librosa.feature.spectral_centroid(y=y,sr=sr)[0];t=librosa.frames_to_time(range(len(c)),sr=sr)+a
        print('other centroid per 2.5s',[int(c[(t>=x)&(t<x+2.5)].mean()) for x in np.arange(a,b,2.5)])
