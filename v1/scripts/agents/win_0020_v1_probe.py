import librosa,numpy as np,sys,json
d='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
t0,t1=20,40
for s in ['drums','bass','other']:
    y,sr=librosa.load(d+s+'.wav',sr=22050,offset=t0,duration=t1-t0)
    o=librosa.onset.onset_strength(y=y,sr=sr)
    on=librosa.onset.onset_detect(onset_envelope=o,sr=sr,units='time')
    print(s,'onsets',len(on),'per s',len(on)/20)
    for a,b in [(0,12),(12,20)]:
        print(' ',a+t0,b+t0,'onsets',((on>=a)&(on<b)).sum())
    S=np.abs(librosa.stft(y))
    f=librosa.fft_frequencies(sr=sr)
    for a,b in [(20,30),(32,40)]:
        pass
    cen=librosa.feature.spectral_centroid(S=S,sr=sr)[0]
    fr=librosa.frames_to_time(np.arange(len(cen)),sr=sr)
    print(' centroid 20-32',cen[fr<12].mean(),'32-40',cen[fr>=12].mean())
y,sr=librosa.load(d+'drums.wav',sr=22050,offset=t0,duration=20)
o=librosa.onset.onset_strength(y=y,sr=sr)
tg=librosa.feature.tempo(onset_envelope=o,sr=sr);print('drum tempo',tg)
on=librosa.onset.onset_detect(onset_envelope=o,sr=sr,units='time');print(np.round(on[:40],2))
y,sr=librosa.load(d+'bass.wav',sr=22050,offset=t0,duration=20)
S=np.abs(librosa.stft(y));f=librosa.fft_frequencies(sr=sr)
for a,b in [(0,12),(12,20)]:
    m=S[:, (librosa.frames_to_time(np.arange(S.shape[1]),sr=sr)>=a)&(librosa.frames_to_time(np.arange(S.shape[1]),sr=sr)<b)].mean(1)
    print('bass energy share >300Hz',a+t0,m[f>300].sum()/m.sum(), 'peak hz',f[m.argmax()])
