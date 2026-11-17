import librosa, numpy as np, sys
d='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
t0,t1=160,180
def ld(n): 
    y,sr=librosa.load(d+n+'.wav',sr=22050,offset=t0-1,duration=t1-t0+2); return y,sr
# bass pitch
y,sr=ld('bass')
f0,v,p=librosa.pyin(y,fmin=30,fmax=200,sr=sr,frame_length=4096)
tt=librosa.times_like(f0,sr=sr)+t0-1
for a in range(160,180,2):
    m=(tt>=a)&(tt<a+2)&~np.isnan(f0)
    print('bass',a, round(float(np.median(f0[m])),1) if m.any() else None, m.sum())
# drums onsets per 2 s and centroid
y,sr=ld('drums')
on=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+t0-1
on=on[(on>=t0)&(on<t1)]
print('drum onsets',len(on)); print(np.round(on,2))
for a in range(160,180,4):
    seg=y[int((a-t0+1)*sr):int((a-t0+5)*sr)]
    print('drum centroid',a,round(float(librosa.feature.spectral_centroid(y=seg,sr=sr).mean())), 'low(<150) frac', round(float(np.abs(librosa.stft(seg))[:7].sum()/np.abs(librosa.stft(seg)).sum()),2))
y,sr=ld('vocals')
on=librosa.onset.onset_detect(y=y,sr=sr,units='time')+t0-1
print('vocal onsets',np.round(on[(on>=t0)&(on<t1)],2))
