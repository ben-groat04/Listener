import numpy as np, librosa, json, sys
D='/home/user/Listener/v1/data/video1/'
v,sr=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=22050,mono=True)
beats=np.array(json.load(open(D+'audio_features/beat_times.json')))
# voiced segments by RMS
hop=512
rms=librosa.feature.rms(y=v,hop_length=hop)[0];db=20*np.log10(rms+1e-9)
t=np.arange(len(rms))*hop/sr
act=db>-45
segs=[];s=None
for i,a in enumerate(act):
    if a and s is None:s=i
    if not a and s is not None:
        if t[i]-t[s]>0.15:segs.append((t[s],t[i]))
        s=None
# merge gaps<0.3
m=[]
for a,b in segs:
    if m and a-m[-1][1]<0.35:m[-1]=(m[-1][0],b)
    else:m.append((a,b))
bt=np.median(np.diff(beats));print('beat',bt, 'bpm',60/bt)
print('n segs',len(m))
for a,b in m:
    nb=np.argmin(abs(beats-a));ph=((a-beats[nb])/bt)
    nbe=np.argmin(abs(beats-b));phe=((b-beats[nbe])/bt)
    print(f"{int(a//60)}:{a%60:05.2f}-{int(b//60)}:{b%60:05.2f} dur {b-a:.2f} on-beat offset {ph:+.2f} beats (beat idx {nb}, mod8 {nb%8}) end-offset {phe:+.2f}")
# pitch of speech
f0,vf,vp=librosa.pyin(v,fmin=70,fmax=400,sr=sr,hop_length=hop)
for a,b in [(10,16),(20,31),(41,42.5),(51,56),(1*60+19,1*60+27),(2*60+24,2*60+36),(2*60+44,2*60+48)]:
    i=(t>=a)&(t<=b);x=f0[i&vf] if True else 0
    x=f0[i][~np.isnan(f0[i])]
    print(a,b,'median f0 %.0f'%np.median(x) if len(x) else 'none', 'p10-90',np.percentile(x,[10,90]).round() if len(x) else '')
# bandwidth: spectral rolloff 95% during speech
S=np.abs(librosa.stft(v,n_fft=2048,hop_length=hop))
ro=librosa.feature.spectral_rolloff(S=S,sr=sr,roll_percent=0.95)[0]
cen=librosa.feature.spectral_centroid(S=S,sr=sr)[0]
for a,b in [(10,16),(20,31),(1*60+19,1*60+27),(2*60+24,2*60+36),(2*60+44,2*60+48)]:
    i=(t>=a)&(t<=b)&(db>-35);print(a,'rolloff95 med %.0f cent %.0f'%(np.median(ro[i]),np.median(cen[i])))
# low-end: energy below 150Hz share
fr=librosa.fft_frequencies(sr=sr,n_fft=2048)
for a,b in [(20,31),(2*60+44,2*60+48)]:
    i=(t>=a)&(t<=b)&(db>-35);e=(S[:,i]**2).sum(1);print('share<200Hz',e[fr<200].sum()/e.sum(),'>4k',e[fr>4000].sum()/e.sum())
# repetition: compare 0:27-0:32 and 2:43.5-2:48.5 mfcc DTW
def mf(a,b):
    y=v[int(a*sr):int(b*sr)];return librosa.feature.mfcc(y=y,sr=sr,n_mfcc=20,hop_length=hop)
A=mf(27,32);B=mf(2*60+43.5,2*60+48.5)
Dm,wp=librosa.sequence.dtw(A[1:],B[1:],metric='cosine');print('dtw cost per step',Dm[-1,-1]/len(wp))
# baseline: compare vs different phrase
C=mf(53,56);Dm2,wp2=librosa.sequence.dtw(A[1:],C[1:],metric='cosine');print('baseline cost',Dm2[-1,-1]/len(wp2))
# duration of "Waar iedereen" phrase: 
