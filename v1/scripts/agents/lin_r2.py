import librosa,numpy as np,sys
D='data/video2/stems_raw/htdemucs/song/'
def ac(y,sr,t0,t1,lags=(0.125,0.25,0.375,0.5,0.75,1.0,2.0)):
    y=y[int(t0*sr):int(t1*sr)];h=256
    o=librosa.onset.onset_strength(y=y,sr=sr,hop_length=h);o=o-o.mean()
    a=np.correlate(o,o,'full')[len(o)-1:];a/=a[0]
    return {l:round(float(a[int(round(l*sr/h))]),2) for l in lags}
for st in ['other','bass','drums']:
    y,sr=librosa.load(D+st+'.wav',sr=22050,mono=True)
    for a,b in [(60,100),(160,200),(240,280)]: print(st,a,b,ac(y,sr,a,b))
# drums: kick vs snare band pattern across the bar, 4:00-4:40
y,sr=librosa.load(D+'drums.wav',sr=22050,mono=True)
S=np.abs(librosa.stft(y[int(240*sr):int(280*sr)],n_fft=1024,hop_length=128));f=librosa.fft_frequencies(sr=sr,n_fft=1024)
for nm,(lo,hi) in {'kick':(30,120),'snare':(180,400),'hat':(6000,10000)}.items():
    e=S[(f>=lo)&(f<hi)].sum(0);o=np.maximum(0,np.diff(e));
    pk=librosa.util.peak_pick(o,pre_max=6,post_max=6,pre_avg=20,post_avg=20,delta=o.std()*0.8,wait=8)
    t=pk*128/sr; ph=((t-0.10)%2.0)/0.125  # phase in sixteenths, offset latency 0.10
    h=np.bincount(np.round(ph).astype(int)%16,minlength=16); print(nm,len(pk),h.tolist())
# intro lowpass
y,sr=librosa.load('data/video2/audio/song.wav',sr=22050,mono=True)
for a,b in [(0,28),(28,42),(60,90),(200,230)]:
    s=y[int(a*sr):int(b*sr)];print(a,b,'rolloff95',round(float(np.median(librosa.feature.spectral_rolloff(y=s,sr=sr,roll_percent=0.95))),0))
