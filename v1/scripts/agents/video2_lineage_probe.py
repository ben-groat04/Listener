import librosa, numpy as np
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
d,sr=librosa.load(D+'drums.wav',sr=22050,mono=True)
b,_=librosa.load(D+'bass.wav',sr=22050,mono=True)
o,_=librosa.load(D+'other.wav',sr=22050,mono=True)
# tempo autocorr 2:00-4:40
seg=d[120*sr:280*sr]
env=librosa.onset.onset_strength(y=seg,sr=sr,hop_length=256)
fps=sr/256
ac=np.correlate(env-env.mean(),env-env.mean(),'full')[len(env)-1:]
ac/=ac[0]
for lag in [0.375,0.5,0.75,1.0,2.0]:
    i=int(round(lag*fps)); print('ac',lag,round(ac[i-2:i+3].max(),3))
# kick band onset fold on 0.5 s
S=np.abs(librosa.stft(seg,n_fft=2048,hop_length=256))
fr=librosa.fft_frequencies(sr=sr,n_fft=2048)
for name,(lo,hi) in {'kick':(30,120),'snare':(150,2000),'hat':(5000,10000)}.items():
    e=S[(fr>=lo)&(fr<hi)].sum(0); e=np.diff(e,prepend=0); e[e<0]=0
    ph=(np.arange(len(e))/fps)%2.0
    h,_=np.histogram(ph,bins=16,weights=e,range=(0,2)); print(name,np.round(h/h.sum(),2))
# bass pitch distribution
f0,v,p=librosa.pyin(b[120*sr:200*sr],fmin=30,fmax=200,sr=sr)
n=librosa.hz_to_note(f0[v]); import collections
print(collections.Counter(n).most_common(6))
# harmonic vs percussive share of other
H,P=librosa.decompose.hpss(np.abs(librosa.stft(o[200*sr:240*sr])))
print('other H share',H.sum()/(H.sum()+P.sum()))
y,_=librosa.load('/home/user/Listener/v1/data/video2/audio/song.wav',sr=22050)
for a,bb in [(0,28),(60,88),(120,180),(200,280)]:
    s=y[a*sr:bb*sr]; print(a,bb,'centroid',round(librosa.feature.spectral_centroid(y=s,sr=sr).mean()),'flat',round(librosa.feature.spectral_flatness(y=s).mean(),4))
