import numpy as np, librosa, json, sys
D='/home/user/Listener/v1/data/t_cshells_cshore/'
a,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False)
m=a.mean(0) if a.ndim>1 else a
print('sr',sr,'peak 4:00-4:20 L/R',[20*np.log10(np.abs(x[240*sr:260*sr]).max()) for x in (a if a.ndim>1 else [a])],'song peak',20*np.log10(np.abs(a).max()))
def seg(f):
    y,s=librosa.load(f,sr=22050,offset=235,duration=30);return y,s
dr,s=seg(D+'stems_raw/htdemucs/song/drums.wav')
bs,_=seg(D+'stems_raw/htdemucs/song/bass.wav')
ot,_=seg(D+'stems_raw/htdemucs/song/other.wav')
mx,_=seg(D+'audio/song.wav')
# kick: low band of drums
import scipy.signal as sg
sos=sg.butter(4,[40,110],'band',fs=s,output='sos');k=sg.sosfilt(sos,dr)
on=librosa.onset.onset_detect(y=k,sr=s,units='time',backtrack=False,hop_length=128)
on=on+235
w=on[(on>=240)&(on<260)]
print('kick onsets',len(w),np.round(w,2))
ioi=np.diff(w);print('IOI',np.round(ioi,3),'median',np.median(ioi))
bt=60/np.median(ioi) if len(ioi) else 0
print('bpm from median ioi',bt)
# kick grid deviation
base=np.median(ioi);grid=w[0]+np.round((w-w[0])/base)*base
print('dev ms std',np.std((w-grid)*1000))
# tracker beats
b=json.load(open(D+'audio_features/beat_times.json'));b=np.array(b if isinstance(b,list) else b.get('beats',[]));bb=b[(b>=240)&(b<260)];print('tracker beats',len(bb),np.round(np.diff(bb).mean(),3) if len(bb)>1 else None)
# snare/hat all-onset
oa=librosa.onset.onset_detect(y=dr,sr=s,units='time',hop_length=128)+235;oa=oa[(oa>=240)&(oa<260)];print('drum onsets',len(oa),'per s',len(oa)/20)
# spectral centroid and bands per 4s
for t in range(240,260,4):
    i=(t-235)*s;j=i+4*s
    S=np.abs(librosa.stft(mx[i:j]))**2;f=librosa.fft_frequencies(sr=s)
    c=(S.sum(1)*f).sum()/S.sum()
    hf=S[f>8000].sum()/S.sum()
    print(t,'centroid',round(c),'hf>8k share',round(hf,4),'other rms dB',round(20*np.log10(np.sqrt((ot[i:j]**2).mean())),1),'bass',round(20*np.log10(np.sqrt((bs[i:j]**2).mean())+1e-9),1))
# stem levels 1s resolution of bass dropout times; 10ms-ish envelope of bass
e=np.sqrt(np.convolve(bs**2,np.ones(2205)/2205,'same'));
tt=np.arange(len(bs))/s+235
for t0 in np.arange(240,260,0.5):
    i=int((t0-235)*s);print(t0,round(20*np.log10(e[i]+1e-9),1),end=' | ')
print()
# self-similarity: repeat of 2-bar/4-bar in mix
hop=512;C=librosa.feature.chroma_cqt(y=mx,sr=s,hop_length=hop)
fr=s/hop
for lag in [1.95,3.9,7.8,15.6]:
    L=int(lag*fr);i0=int(5*fr);i1=int(25*fr)
    x=C[:,i0:i1].ravel();y=C[:,i0+L:i1+L].ravel() if i1+L<C.shape[1] else None
    if y is not None: print('chroma corr lag',lag,round(np.corrcoef(x,y)[0,1],3))
