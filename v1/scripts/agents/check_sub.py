import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/video1/'
for name,p in [('bass','stems_raw/htdemucs/song/bass.wav'),('mix','audio/song.wav')]:
    b,sr=sf.read(D+p);b=b.mean(1)
    for a,c in [(121.2,122.6),(127.2,128.6),(133.4,134.6),(139.5,140.8),(145.7,147),(151.9,153.2)]:
        s=b[int(a*sr):int(c*sr)]*np.hanning(int((c-a)*sr)) if False else b[int(a*sr):int(c*sr)]
        s=s*np.hanning(len(s));N=1<<19
        F=np.abs(np.fft.rfft(s,N));f=np.fft.rfftfreq(N,1/sr);m=(f>30)&(f<70)
        i=np.argmax(F*m);print(name,a,round(f[i],2),end=' ; ')
    print()
# bass at 2:38.3 pitch
b,sr=sf.read(D+'stems_raw/htdemucs/song/bass.wav');b=b.mean(1)
for a,c in [(159,162),(170,174),(100.5,103),(33,36),(15,18)]:
    s=b[int(a*sr):int(c*sr)]*np.hanning(int((c-a)*sr));N=1<<19
    F=np.abs(np.fft.rfft(s,N));f=np.fft.rfftfreq(N,1/sr);m=(f>30)&(f<200);print(a,f[np.argmax(F*m)])
