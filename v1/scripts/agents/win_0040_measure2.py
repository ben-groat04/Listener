import librosa,numpy as np,scipy.signal as sg
R='/home/user/Listener/v1/data/t_dl_mirror/';S=R+'stems_raw/htdemucs/song/'
sr=44100
d,_=librosa.load(S+'drums.wav',sr=sr,mono=True)
b,a=sg.butter(4,[40/(sr/2),150/(sr/2)],'band');k=sg.filtfilt(b,a,d)
env=np.abs(sg.hilbert(np.nan_to_num(k)));env=np.convolve(env,np.ones(441)/441,"same")
pk,_=sg.find_peaks(env[40*sr:60*sr],height=env[40*sr:60*sr].max()*0.35,distance=int(0.1*sr))
t=pk/sr+40
print('n low-band hits',len(t),np.round(t,2).tolist())
# fit grid to 0.32 s
for P in [0.3135,0.32,0.3175]:
    ph=np.arange(len(t));best=None
    r=(t-t[0])/P;dev=(r-np.round(r))*P*1000
    print('P',P,'dev ms std',round(dev.std(),1),'abs mean',round(np.abs(dev-np.median(dev)).mean(),1))
# bass pitch
bs,_=librosa.load(S+'bass.wav',sr=sr,mono=True)
f0,vf,_=librosa.pyin(bs[40*sr:60*sr],fmin=30,fmax=200,sr=sr,frame_length=4096)
tt=librosa.times_like(f0,sr=sr)+40
m=~np.isnan(f0)
import collections
nn=librosa.hz_to_note(f0[m]);print(collections.Counter(nn).most_common(6))
# cutoff of mix
y,_=librosa.load(R+'audio/song.wav',sr=None,mono=True)
Sx=np.abs(librosa.stft(y[40*sr:60*sr],n_fft=4096)).mean(1);f=librosa.fft_frequencies(sr=sr,n_fft=4096)
db=20*np.log10(Sx+1e-9)
for fr in [4000,6000,7000,7500,8000,8500,9000,10000,12000,16000]:
    print(fr,round(db[np.argmin(abs(f-fr))],1))
# end-of-bass levels before/after dropout windows: mix level in bass-out vs bass-in (sec resolution from json done) 
import json
p=json.load(open(R+'music_views/per_second_levels.json'))
bin_=[x['dbfs'] for x in p[40:60] if x['bass']>-30];bout=[x['dbfs'] for x in p[40:60] if x['bass']<-45]
print('mix bass-in',np.mean(bin_),len(bin_),'bass-out',np.mean(bout),len(bout))
print('drums', np.mean([x['drums'] for x in p[40:60]]),'voc',np.mean([x['vocals'] for x in p[40:60]]),'oth',np.mean([x['other'] for x in p[40:60]]))
