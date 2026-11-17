import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
def load(n,a,b):
    y,sr=librosa.load(D+n+'.wav',sr=22050,mono=True,offset=a,duration=b-a); return y,sr
def db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
# 1. kick shape consistency: sub-150Hz drums, onsets at 0.5 s grid, 2:00-2:30 (grid phase 88.61)
y,sr=load('drums',120,150)
sos=ss.butter(4,150,'low',fs=sr,output='sos'); k=ss.sosfilt(sos,y)
env=np.abs(ss.hilbert(k))
ons=[]
t0=(120-88.61)%0.5
shapes=[]
for i in range(int((30-0.5)/0.5)):
    s=int((t0+i*0.5)*sr); seg=k[s:s+int(0.25*sr)]
    if len(seg)==int(0.25*sr): shapes.append(seg)
S=np.array(shapes)
pk=np.abs(S[:,:int(0.05*sr)]).max(1)
E=np.array([np.abs(ss.hilbert(x)) for x in S])
m=np.corrcoef(E)
print('kick beats',len(S),'peak mean/std dB',20*np.log10(pk.mean()),np.std(20*np.log10(pk)))
print('envelope corr mean offdiag',(m.sum()-len(m))/(len(m)**2-len(m)))
# waveform corr after aligning
W=S[:,:int(0.1*sr)]
c=np.corrcoef(W); print('waveform corr mean',(c.sum()-len(c))/(len(c)**2-len(c)))
# 2. delay repeats: autocorrelation of 'other' envelope and of drums hat band, 3:00-3:40, lag 0.375 and 0.75 vs 0.25/0.5
for n,lo in [('other',4000),('drums',6000)]:
    y,sr=load(n,180,220)
    sos=ss.butter(4,lo,'high',fs=sr,output='sos'); h=ss.sosfilt(sos,y)
    e=librosa.feature.rms(y=h,frame_length=512,hop_length=128)[0]; e=e-e.mean()
    ac=np.correlate(e,e,'full')[len(e)-1:]; ac/=ac[0]
    hop=128/sr
    print(n,'hi-band env autocorr',{l:round(float(ac[int(l/hop)]),2) for l in [0.125,0.25,0.375,0.5,0.75,1.0,2.0]})
# 3. voice reverb/tail and bass accent 4:44-5:00
y,sr=load('vocals',284,300)
e=librosa.feature.rms(y=y,frame_length=1024,hop_length=256)[0]; hop=256/sr
edb=20*np.log10(e+1e-9)
print('vocal floor dB p10',np.percentile(edb,10),'p90',np.percentile(edb,90))
# decay after each call peak
pk=ss.find_peaks(edb,height=np.percentile(edb,85),distance=int(1.5/hop))[0]
for p in pk[:8]:
    t=284+p*hop; seg=edb[p:p+int(1.0/hop)]
    drop=[round(float(seg[min(int(d/hop),len(seg)-1)]-seg[0]),1) for d in (0.1,0.2,0.4,0.8)]
    print('call at %d:%05.2f peak %.1f dB; change after 0.1/0.2/0.4/0.8 s'%(int(t//60),t%60,edb[p]),drop, 'phase in bar',round(((t-88.61)%2),2))
yb,sr=load('bass',284,300)
e=librosa.feature.rms(y=yb,frame_length=1024,hop_length=256)[0]; edbb=20*np.log10(e+1e-9)
d=np.diff(edbb); pb=ss.find_peaks(d,height=4,distance=int(1.0/hop))[0]
print('bass onsets (rise>4dB) phase in bar:',[round(((284+p*hop-88.61)%2),2) for p in pb])
# 4. 4:29-4:36 voice: vibrato (f0 modulation 4-8 Hz) and spectral flatness
y,sr=load('vocals',269,276)
f0,vf,vp=librosa.pyin(y,fmin=200,fmax=1000,sr=sr,frame_length=2048)
h=512/sr; ok=~np.isnan(f0); print('voiced frac',ok.mean())
cents=1200*np.log2(f0/np.nanmedian(f0))
# modulation in longest voiced run
runs=[];i=0
while i<len(ok):
    if ok[i]:
        j=i
        while j<len(ok) and ok[j]: j+=1
        runs.append((i,j)); i=j
    else: i+=1
runs=sorted(runs,key=lambda r:r[1]-r[0],reverse=True)[:3]
for a,b in runs:
    c=cents[a:b]; c=c-np.polyval(np.polyfit(np.arange(len(c)),c,2),np.arange(len(c)))
    fr=np.fft.rfftfreq(len(c),h); sp=np.abs(np.fft.rfft(c*np.hanning(len(c))))
    band=(fr>3)&(fr<9)
    print('run %.2fs at %.2f: detrended cents std %.1f, peak mod %.1f Hz'%((b-a)*h,269+a*h,c.std(),fr[band][sp[band].argmax()] if band.any() and len(c)>12 else -1))
# 5. 'other' top band ramp: harmonic-vs-noise and spectral rolloff 2:44-2:52 and 3:20-3:52, hpss
for a,b in [(150,160),(164,172),(200,208),(210,218),(225,233)]:
    y,sr=load('other',a,b)
    H,P=librosa.effects.hpss(y)
    S=np.abs(librosa.stft(y,n_fft=2048)); fr=librosa.fft_frequencies(sr=sr,n_fft=2048)
    cen=librosa.feature.spectral_centroid(S=S,sr=sr).mean(); ro=librosa.feature.spectral_rolloff(S=S,sr=sr,roll_percent=0.95).mean()
    hi=S[fr>4000]; 
    print('%d:%02d other: perc/harm %.1f dB, centroid %.0f Hz, rolloff95 %.0f Hz, 4k+ share %.4f'%(a//60,a%60,db(P)-db(H),cen,ro,(hi**2).sum()/(S**2).sum()))
