import sys,librosa,numpy as np
t0,t1=float(sys.argv[1]),float(sys.argv[2])
sr=22050
for st in ['drums','bass','other','vocals']:
    y,_=librosa.load(f'/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/{st}.wav',sr=sr,offset=t0,duration=t1-t0)
    if st=='drums':
        on=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+t0
        print('drum onsets',len(on),'median IOI',np.median(np.diff(on)).round(3));
        S=np.abs(librosa.stft(y));f=librosa.fft_frequencies(sr=sr)
        t=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr)+t0
        for a,bnd in [(0,200),(200,2000),(2000,11000)]:
            e=S[(f>=a)&(f<bnd)].sum(0)
            print(a,bnd,'energy by 5s',[round(float(e[(t>=x)&(t<x+5)].mean()),1) for x in np.arange(t0,t1,5)])
        print(np.round(on[:40],2))
    if st=='bass':
        f0,v,p=librosa.pyin(y,fmin=30,fmax=200,sr=sr)
        tt=librosa.times_like(f0,sr=sr)+t0
        n=librosa.hz_to_note(f0[~np.isnan(f0)])
        import collections
        print('bass notes',collections.Counter(n).most_common(6))
        for x in range(int(t0),int(t1),4):
            m=(tt>=x)&(tt<x+4)&~np.isnan(f0)
            if m.sum(): print(x,librosa.hz_to_note(np.median(f0[m])))
    if st=='other':
        S=np.abs(librosa.stft(y));f=librosa.fft_frequencies(sr=sr)
        print('other centroid',librosa.feature.spectral_centroid(S=S,sr=sr).mean().round(0))
        ch=librosa.feature.chroma_cqt(y=y,sr=sr).mean(1);print('other chroma',dict(zip('C C# D D# E F F# G G# A A# B'.split(),ch.round(2))))
