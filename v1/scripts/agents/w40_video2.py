import librosa,numpy as np,json
d='data/video2/stems_raw/htdemucs/song/'
t0,t1=40,60
y,sr=librosa.load(d+'drums.wav',sr=22050,offset=t0,duration=20)
o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)
print('drum onsets',np.round(o+t0,2).tolist())
env=librosa.onset.onset_strength(y=y,sr=sr)
b,sr=librosa.load(d+'bass.wav',sr=22050,offset=t0,duration=20)
f=librosa.yin(b,fmin=30,fmax=200,sr=sr,frame_length=4096,hop_length=1024)
for s in range(0,20,2):
    seg=f[int(s*sr/1024):int((s+2)*sr/1024)]
    print('bass',t0+s,round(float(np.median(seg)),1))
m,sr=librosa.load('data/video2/audio/song.wav',sr=22050,offset=t0,duration=20)
S=np.abs(librosa.stft(m))**2;fr=librosa.fft_frequencies(sr=sr)
for a,bb in[(0,150),(150,500),(500,2000),(2000,6000),(6000,11000)]:
    e=10*np.log10(S[(fr>=a)&(fr<bb)].sum(0)+1e-12)
    n=len(e)//4
    print(a,bb,[round(float(e[i*n:(i+1)*n].mean()),1) for i in range(4)])
