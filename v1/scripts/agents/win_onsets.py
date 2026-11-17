import sys,librosa,numpy as np
t0,t1=float(sys.argv[1]),float(sys.argv[2])
d='data/video2/stems_raw/htdemucs/song/'
for s in ['drums','bass']:
    y,sr=librosa.load(d+s+'.wav',sr=22050,offset=t0,duration=t1-t0)
    o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)
    print(s,len(o),np.round(o+t0,2).tolist())
    if s=='drums':
        S=np.abs(librosa.stft(y))**2;f=librosa.fft_frequencies(sr=sr)
        oe=librosa.onset.onset_strength(y=y,sr=sr)
        print('tempo',librosa.feature.tempo(onset_envelope=oe,sr=sr))
        for a,b in [(0,150),(150,500),(500,4000),(4000,11000)]:
            m=(f>=a)&(f<b);e=S[m].sum(0);n=len(e)//4
            print(a,b,[round(float(10*np.log10(e[i*n:(i+1)*n].mean()+1e-12)),1) for i in range(4)])
