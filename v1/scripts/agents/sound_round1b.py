import numpy as np, soundfile as sf, librosa
D='data/video1/stems_raw/htdemucs/song/'
sr=44100
b,_=sf.read(D+'bass.wav',always_2d=True);b=b.mean(1)
# sub glide: f0 in bursts via fine FFT of 0.25s frames
for t0 in [121.3,127.3,133.5,139.7,158.5,159.5]:
    out=[]
    for k in range(7):
        seg=b[int((t0+k*.25)*sr):int((t0+k*.25+.5)*sr)]
        X=np.abs(np.fft.rfft(seg*np.hanning(len(seg)),n=1<<18));f=np.fft.rfftfreq(1<<18,1/sr);m=(f>30)&(f<120)
        out.append(round(f[m][np.argmax(X[m])],1))
    print(t0,out)
# sub burst envelope shape
seg=np.abs(b[int(121*sr):int(124*sr)]);env=librosa.feature.rms(y=b[int(121*sr):int(124*sr)],frame_length=2048,hop_length=2205)[0]
print('env dB 0.05s steps',np.round(20*np.log10(env+1e-6),0))
# drums: low vs high ratio, onset strength variation; kick vs hats
d,_=sf.read(D+'drums.wav',always_2d=True);d=d.mean(1)
for t0,t1 in [(10,30),(35,40),(70,75),(100,110),(125,135),(150,158),(170,180)]:
    x=d[int(t0*sr):int(t1*sr)];X=np.abs(librosa.stft(x,n_fft=2048))**2;f=librosa.fft_frequencies(sr=sr,n_fft=2048);T=X.sum()
    print(t0,t1,'drum <150 %.0f%% 150-1k %.0f%% 1-5k %.0f%% >5k %.0f%%'%tuple(100*X[(f>=a)&(f<c)].sum()/T for a,c in [(0,150),(150,1000),(1000,5000),(5000,30000)]))
# pumping: other stem rms modulation at beat rate? correlation of other env with drums
o,_=sf.read(D+'other.wav',always_2d=True);o=o.mean(1)
# other stem 1:27-1:39 pitch peaks
for t0,t1 in [(80,87),(90,98),(100,106)]:
    x=o[int(t0*sr):int(t1*sr)];X=np.abs(np.fft.rfft(x*np.hanning(len(x)),n=1<<20));f=np.fft.rfftfreq(1<<20,1/sr)
    m=(f>60)&(f<1500);idx=np.argsort(X[m])[::-1];pk=[]
    for i in idx:
        fq=f[m][i]
        if all(abs(fq-p)>8 for p in pk): pk.append(fq)
        if len(pk)==6:break
    print(t0,t1,[round(p) for p in pk],[librosa.hz_to_note(p) for p in pk])
# end tail: reverb decay of last hits
mixs,_=sf.read('data/video1/audio/song.wav',always_2d=True);m=mixs.mean(1)
seg=m[int(187.5*sr):];r=librosa.feature.rms(y=seg,frame_length=441,hop_length=441)[0];print('end rms dB 10ms',np.round(20*np.log10(r+1e-7)).astype(int)[:70])
# voice spectrum band-limit
v,_=sf.read(D+'vocals.wav',always_2d=True);v=v.mean(1)
for t0,t1 in [(10,20),(20,30),(100,108),(135,150),(164,168)]:
    x=v[int(t0*sr):int(t1*sr)];X=np.abs(librosa.stft(x,n_fft=2048))**2;f=librosa.fft_frequencies(sr=sr,n_fft=2048);T=X.sum()
    print('voice',t0,t1,'<300 %.0f 300-3k %.0f 3-8k %.0f >8k %.0f'%tuple(100*X[(f>=a)&(f<c)].sum()/T for a,c in [(0,300),(300,3000),(3000,8000),(8000,30000)]))
