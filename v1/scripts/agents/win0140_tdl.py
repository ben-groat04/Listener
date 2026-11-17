import numpy as np, soundfile as sf, json, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
T0,T1=140.,160.
def load(p):
    x,sr=sf.read(p,always_2d=True); return x,sr
mix,sr=load(D+'audio/song.wav')
print('sr',sr,'ch',mix.shape[1],'dur',len(mix)/sr)
seg=mix[int(T0*sr):int(T1*sr)]
print('peak',20*np.log10(np.abs(seg).max()),'rms',20*np.log10(np.sqrt((seg**2).mean())), 'n>=.999',(np.abs(seg)>=.999).sum())
if seg.shape[1]>1: print('LR corr',np.corrcoef(seg[:,0],seg[:,1])[0,1])
m=seg.mean(1)
S=np.abs(librosa.stft(m,n_fft=2048))**2; f=librosa.fft_frequencies(sr=sr,n_fft=2048)
tot=S.sum()
for a,b in [(0,150),(150,2000),(2000,8000),(8000,24000)]:
    print('band',a,b,10*np.log10(S[(f>=a)&(f<b)].sum()/tot))
print('centroid',librosa.feature.spectral_centroid(S=np.sqrt(S),sr=sr).mean())
st={}
for n in ['vocals','drums','bass','other']:
    x,s=load(D+f'stems_raw/htdemucs/song/{n}.wav'); st[n]=x.mean(1); sr2=s
def env(x,hop=0.01):
    h=int(sr2*hop); n=len(x)//h
    return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
E={n:env(st[n]) for n in st}; E['mix']=env(mix.mean(1))
def seg_on(e,thr,a,b,minlen=0.1):
    v=e[int(a*100):int(b*100)]>thr; out=[];s=None
    for i,k in enumerate(v):
        if k and s is None: s=i
        if not k and s is not None:
            out.append((a+s/100,a+i/100)); s=None
    if s is not None: out.append((a+s/100,b))
    return out
for n in ['bass','vocals']:
    thr=-45
    print(n,'on segments',[(round(a,2),round(b,2)) for a,b in seg_on(E[n],thr,T0,T1) if b-a>0.1][:60])
# vocal gaps below -45 > 0.2s
print('vocal gaps',[(round(a,2),round(b,2)) for a,b in seg_on(-E['vocals'],45,T0,T1)])
print('bass gaps',[(round(a,2),round(b,2)) for a,b in seg_on(-E['bass'],45,T0,T1)])
# per-second table
for t in range(138,162):
    print(t,{n:round(float(np.mean(E[n][t*100:(t+1)*100])),1) for n in E})
# 1s-window level in 0.5 s steps for mix around 152-156 and 144-147
for a in [143.5,144,144.5,145,145.5,146,146.5,147,147.5]:
    print(a,{n:round(float(np.mean(E[n][int(a*100):int((a+.5)*100)])),1) for n in E})
# kicks: drum stem low band onsets
dr=st['drums']; lo=ss.sosfilt(ss.butter(4,120,'low',fs=sr2,output='sos'),dr)
oenv=librosa.onset.onset_strength(y=lo,sr=sr2,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oenv,sr=sr2,hop_length=256,units='time',backtrack=False)
on=on[(on>=T0)&(on<T1)]
print('n kicks',len(on)); ioi=np.diff(on)
print('IOI hist',np.round(np.percentile(ioi,[10,25,50,75,90]),3))
bt=json.load(open(D+'audio_features/beat_times.json')); bt=np.array(bt if isinstance(bt,list) else bt.get('beats',bt))
bi=bt[(bt>=T0)&(bt<T1)]; bp=np.median(np.diff(bi)); print('beat period',bp,60/bp)
# fit 16th grid
g=bp/4
best=None
for ph in np.linspace(0,g,200):
    d=((on-ph+g/2)%g)-g/2; r=np.sqrt((d**2).mean())
    if best is None or r<best[0]: best=(r,ph)
print('kick RMS dev from 16th grid ms',best[0]*1000,' vs random expectation',g/np.sqrt(12)*1000)
g4=bp
best=None
for ph in np.linspace(0,g4,200):
    d=((on-ph+g4/2)%g4)-g4/2; r=np.sqrt((d**2).mean())
    if best is None or r<best[0]: best=(r,ph)
print('kick RMS dev from beat grid ms',best[0]*1000)
print('kick onsets',np.round(on,2).tolist())
# bass loop autocorr
for n in ['bass','drums','other']:
    e=E[n][int(T0*100)-1000:int(T1*100)+1000]; e=e-e.mean()
    ac=np.correlate(e,e,'full')[len(e)-1:]; ac/=ac[0]
    print(n,'ac at 1 bar',[round(ac[int(k*100)],2) for k in [2.55,5.1,10.2,20.4]])
# other stem level windows
# stereo width / mid
# spectral rolloff for vocal vs drums in window
E2=None
