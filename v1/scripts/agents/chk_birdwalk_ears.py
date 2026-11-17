import librosa,numpy as np,soundfile as sf
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
def load(n,a,b):
    y,sr=sf.read(D+n+'.wav',start=int(a*44100),frames=int((b-a)*44100));return y,sr
for (a,b) in [(2,10),(13,23),(26,40),(72,90),(150,160)]:
    y,sr=load('vocals',a,b); m=y.mean(1)
    m=librosa.resample(m,orig_sr=sr,target_sr=16000)
    f0,v,p=librosa.pyin(m,fmin=65,fmax=700,sr=16000,frame_length=2048)
    f=f0[v&~np.isnan(f0)]
    print(a,b,'voiced',len(f)/len(f0), 'median Hz',np.median(f) if len(f) else None, np.percentile(f,[10,90]) if len(f) else None)
# bass / drums correlation and sub share
for n in ['bass','drums','other','vocals']:
    y,sr=load(n,30,40)
    print(n,'LR corr',np.corrcoef(y[:,0],y[:,1])[0,1])
y,sr=load('bass',30,40);m=y.mean(1)
S=np.abs(np.fft.rfft(m));fr=np.fft.rfftfreq(len(m),1/sr)
print('bass peak Hz',fr[S.argmax()],'2nd harm dB',20*np.log10(S[(abs(fr-2*fr[S.argmax()])<3)].max()/S.max()),'share<60',(S[fr<60]**2).sum()/(S**2).sum())
y,sr=load('other',40,47);m=y.mean(1)
S=np.abs(np.fft.rfft(m));fr=np.fft.rfftfreq(len(m),1/sr)
i=np.argsort(S[(fr>150)&(fr<2000)])[-5:];print('other peaks',fr[(fr>150)&(fr<2000)][i])
y,sr=load('drums',0,12);m=y.mean(1)
on=librosa.onset.onset_detect(y=m,sr=sr,units='time',backtrack=False);print('drum onsets 0-12',np.round(on,2))
y,sr=sf.read('/home/user/Listener/v1/data/t_birdwalk/audio/song.wav');m=y.mean(1) if y.ndim>1 else y
S=np.abs(librosa.stft(m,n_fft=4096)).mean(1)**2;fr=librosa.fft_frequencies(sr=sr,n_fft=4096)
for hz in [6000,8000,10000,12000,16000]:print(hz,10*np.log10(S[fr>hz].sum()/S.sum()))
