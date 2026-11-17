import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_cshells_cshore/stems_raw/htdemucs/song/'
sr=22050
def L(n):
    y,_=librosa.load(D+n+'.wav',sr=sr,mono=True);return y
dr,ba,ot=L('drums'),L('bass'),L('other')
hop=110
def env(y):return librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
fps=sr/hop
# 1) tempo per 10 s: drum+bass onset-strength AC, beat lag in 0.44-0.56
oe=env(dr)+env(ba)
print('BPM per 20s window stepping 10s (AC peak lag 0.43-0.56s), drums+bass')
for s in range(100,320,10):
    a=oe[int(s*fps):int((s+20)*fps)];a=a-a.mean()
    ac=np.correlate(a,a,'full')[len(a)-1:];ac/=ac[0]
    lo,hi=int(.43*fps),int(.56*fps);k=lo+np.argmax(ac[lo:hi]);
    # parabolic
    y0,y1,y2=ac[k-1],ac[k],ac[k+1];d=.5*(y0-y2)/(y0-2*y1+y2);lag=(k+d)/fps
    print(s,round(lag,4),round(60/lag,1),round(ac[k],2))
# 2) drum band energy per 10s 2:30-3:20 and hat/snare bands
S=np.abs(librosa.stft(dr,n_fft=2048,hop_length=512))**2;f=librosa.fft_frequencies(sr=sr,n_fft=2048)
tt=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr,hop_length=512)
print('drum band dB per 5s: <150, 150-1k, 1-4k, 4-10k, onset/s')
on=librosa.onset.onset_detect(onset_envelope=env(dr),sr=sr,hop_length=hop,units='time')
for s in range(150,215,5):
    m=(tt>=s)&(tt<s+5);r=[10*np.log10(S[(f>=a)&(f<b)][:,m].sum(0).mean()+1e-12) for a,b in[(30,150),(150,1000),(1000,4000),(4000,10000)]]
    print(s,[round(x,1) for x in r],round(((on>=s)&(on<s+5)).sum()/5,1))
# 3) bass onsets per 5 s and pitch-ish: bass quarter vs eighth at 3:00-3:30
bo=librosa.onset.onset_detect(onset_envelope=env(ba),sr=sr,hop_length=hop,units='time',delta=.1)
for s in range(180,230,5):
    x=bo[(bo>=s)&(bo<s+5)];i=np.diff(x)
    print('bass',s,len(x),np.round(np.median(i),3) if len(i) else None)
# 4) 2:22 pulses in drum/bass/other 10ms env
for nm,y in[('drums',dr),('bass',ba),('other',ot)]:
    a=y[int(141.8*sr):int(144.2*sr)];w=int(.01*sr);e=np.sqrt(np.convolve(a**2,np.ones(w)/w,'same'))
    p,_=ss.find_peaks(20*np.log10(e+1e-9),distance=int(.25*sr),prominence=6)
    print(nm,'2:22 peaks',[round(141.8+q/sr,2) for q in p],[round(20*np.log10(e[q]+1e-9),0) for q in p])
# 5) bass onset sharpness before/after 3:20: onset strength peak-to-median in bass
for s0,s1 in[(120,200),(200,225),(225,260)]:
    e=env(ba)[int(s0*fps):int(s1*fps)];print('bass OS',s0,s1,round(np.percentile(e,95)/np.median(e),1))
