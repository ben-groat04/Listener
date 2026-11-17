import sys,librosa,numpy as np
t0,t1=float(sys.argv[1]),float(sys.argv[2]); base='stems_raw/htdemucs/song/'
for s in ['drums','bass','other']:
    y,sr=librosa.load(base+s+'.wav',sr=22050,offset=t0,duration=t1-t0,mono=True)
    o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+t0
    print(s,len(o),np.round(o,2).tolist())
    if s=='drums':
        S=np.abs(librosa.stft(y)); f=librosa.fft_frequencies(sr=sr)
        for lo,hi in [(20,150),(150,1000),(1000,5000),(5000,11000)]:
            print(' band',lo,hi,round(10*np.log10((S[(f>=lo)&(f<hi)]**2).mean()+1e-12),1))
        env=librosa.onset.onset_strength(y=y,sr=sr); print(' tempo',librosa.feature.tempo(onset_envelope=env,sr=sr))
    if s=='other':
        c=librosa.feature.spectral_centroid(y=y,sr=sr); print(' centroid',c.mean())
        h,p=librosa.effects.hpss(y); print(' harm/perc rms',np.sqrt((h**2).mean()),np.sqrt((p**2).mean()))
