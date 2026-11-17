import librosa,numpy as np,json
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
t0,t1=80,100
for s in ['drums','other','bass','vocals']:
    y,sr=librosa.load(D+s+'.wav',sr=22050,offset=t0,duration=t1-t0)
    if s=='drums':
        on=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)
        for a,b in[(0,7),(7,13),(13,20)]:
            print('drum onsets/s',a+t0,b+t0,round(((on>=a)&(on<b)).sum()/(b-a),2))
        S=np.abs(librosa.stft(y))**2;f=librosa.fft_frequencies(sr=sr)
        for a,b in[(0,7),(7,20)]:
            fr=slice(int(a*sr/512),int(b*sr/512))
            lo=S[f<150,fr].sum();hi=S[f>2000,fr].sum();print('drums hi/lo dB',a+t0,round(10*np.log10(hi/lo),1))
    if s=='other':
        for a,b in[(0,7),(7,20)]:
            fr=slice(int(a*sr/512),int(b*sr/512))
            c=librosa.feature.spectral_centroid(y=y,sr=sr)[0][fr].mean();print('other centroid',a+t0,round(c))
    if s=='bass':
        rms=librosa.feature.rms(y=y)[0];print('bass rms dB per 2s',[round(20*np.log10(rms[int(i*sr/512):int((i+2)*sr/512)].mean()+1e-9),0) for i in range(0,20,2)])
