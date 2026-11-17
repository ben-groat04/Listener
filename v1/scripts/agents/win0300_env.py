import numpy as np, soundfile as sf, librosa, sys
d='stems_raw/htdemucs/song/'
for n in ['song','vocals','drums','bass','other']:
    p='audio/song.wav' if n=='song' else d+n+'.wav'
    y,sr=sf.read(p,start=int(298*44100) if False else 0,frames=0) if False else (None,None)
    info=sf.info(p); sr=info.samplerate
    y,_=sf.read(p,start=int(298*sr),frames=int(8.5*sr),always_2d=True)
    m=y.mean(1); h=int(0.25*sr)
    r=[20*np.log10(np.sqrt(np.mean(m[i:i+h]**2))+1e-9) for i in range(0,len(m)-h+1,h)]
    print(n,' '.join(f'{x:.0f}' for x in r))
    if n=='song':
        y2=m[int(1.5*sr):]
        S=np.abs(librosa.stft(y2,n_fft=4096,hop_length=1024)); f=librosa.fft_frequencies(sr=sr,n_fft=4096)
        for t0,t1 in [(298.5,300.0),(300.0,300.8),(301.0,302.3),(302.4,303.0),(303.0,304.0)]:
            a=int((t0-299.5)*sr/1024);b=int((t1-299.5)*sr/1024); 
            if a<0: continue
            sp=S[:,a:b].mean(1); c=(f*sp).sum()/sp.sum(); print(' ',t0,t1,'centroid',round(c))
        on=librosa.onset.onset_detect(y=m[int(296*sr)-int(298*sr)+0:] if False else y2,sr=sr,units='time',hop_length=256)
        print('onsets',[round(o+299.5,2) for o in on if o+299.5<306])
