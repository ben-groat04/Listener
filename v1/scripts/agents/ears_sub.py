import librosa,numpy as np
y,sr=librosa.load('/home/user/Listener/v1/data/video1/audio/song.wav',sr=4000)
for a in (121.2,127.2,133.4,139.5,145.7,151.9,158.3):
    s=y[int(a*sr):int((a+1.5)*sr)]
    F=np.abs(np.fft.rfft(s*np.hanning(len(s)),n=sr*8));f=np.fft.rfftfreq(sr*8,1/sr)
    m=(f>30)&(f<120);i=np.argmax(F[m]);print(a,round(f[m][i],2))
