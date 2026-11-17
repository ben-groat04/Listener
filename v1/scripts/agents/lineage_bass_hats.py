import librosa,numpy as np
d='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
b,sr=librosa.load(d+'bass.wav',sr=22050,mono=True,offset=62,duration=18)
f0,v,p=librosa.pyin(b,fmin=30,fmax=120,sr=sr,frame_length=4096)
f=f0[~np.isnan(f0)];print('bass f0 pct',np.percentile(f,[5,25,50,75,95]))
# glide: fraction of frames not within 1 semitone of 55
print('share within 1st of 55Hz',np.mean(abs(12*np.log2(f/55))<1))
x,sr=librosa.load(d+'drums.wav',sr=22050,mono=True,offset=62,duration=18)
S=np.abs(librosa.stft(x,n_fft=1024))
fr=librosa.fft_frequencies(sr=sr,n_fft=1024)
hi=S[fr>6000].sum(0);lo=S[fr<150].sum(0)
print('hi/lo ratio',hi.sum()/lo.sum())
on=librosa.onset.onset_detect(y=x,sr=sr,units='time');print('onsets/s',len(on)/18, 'IOI med',np.median(np.diff(on)), 'min',np.min(np.diff(on)))
