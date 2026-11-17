import librosa,numpy as np
d='stems_raw/htdemucs/song/'
for n in ['song','bass','drums','other']:
    f='audio/song.wav' if n=='song' else d+n+'.wav'
    y,sr=librosa.load(f,sr=22050,offset=299,duration=7)
    r=librosa.feature.rms(y=y,hop_length=512)[0]; t=librosa.times_like(r,sr=sr,hop_length=512)+299
    print(n,' '.join(f'{a:.2f}:{20*np.log10(b+1e-6):.0f}' for a,b in zip(t[::5],r[::5]) if a<305.8))
    on=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+299;print(' onsets',np.round(on,2))
    if n=='song':
        S=np.abs(librosa.stft(y));fr=librosa.fft_frequencies(sr=sr)
        for a,b in[(299.8,300.6),(302.4,303.1),(303.5,304.5)]:
            m=S[:,int((a-299)*sr/512):int((b-299)*sr/512)].mean(1);print(' cent',a,librosa.feature.spectral_centroid(S=S[:,int((a-299)*sr/512):int((b-299)*sr/512)],sr=sr).mean().round())
    if n=='bass':
        f0,_,_=librosa.pyin(y,fmin=30,fmax=200,sr=sr);tt=librosa.times_like(f0,sr=sr)+299
        print(' f0',[(round(a,2),round(b,1)) for a,b in zip(tt,f0) if not np.isnan(b) and a>302][::6])
