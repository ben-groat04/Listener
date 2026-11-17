import numpy as np,librosa,scipy.signal as ss,warnings;warnings.filterwarnings('ignore')
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050
st={k:librosa.load(D+k+'.wav',sr=sr,mono=False) for k in ['vocals','drums','bass','other']}
mono={k:v[0].mean(0) for k,v in st.items()}
hop=256
def env(x,lo=None,hi=None):
    if lo or hi:
        sos=ss.butter(4,[lo or 20,hi or 10000],'bp',fs=sr,output='sos');x=ss.sosfilt(sos,x)
    return librosa.feature.rms(y=x,frame_length=512,hop_length=hop)[0]
def ac(e,lags):
    e=e-e.mean();a=np.correlate(e,e,'full')[len(e)-1:];a/=a[0]+1e-12
    return {l:a[int(round(l*sr/hop))] for l in lags}
print('== A. onset-envelope autocorr of other/bass/drums at lags (s)')
lags=[0.125,0.25,0.375,0.5,0.75,1.0,2.0]
for a,b in [(104,200),(220,270),(285,330)]:
    for k in ['other','bass','drums']:
        o=librosa.onset.onset_strength(y=mono[k][a*sr:b*sr],sr=sr,hop_length=hop)
        r=ac(o,lags);print(a,b,k,' '.join('%.3f:%.2f'%(l,v) for l,v in r.items()))
print('== B. other stem: harmonic/percussive energy, flatness, onset rate by section')
for a,b in [(5,25),(30,60),(60,85),(100,140),(160,200),(200,216),(240,280),(280,288),(290,298)]:
    x=mono['other'][a*sr:b*sr];H,P=librosa.effects.hpss(x)
    S=np.abs(librosa.stft(x,n_fft=2048,hop_length=512))
    fl=librosa.feature.spectral_flatness(S=S).mean()
    on=len(librosa.onset.onset_detect(y=x,sr=sr,hop_length=hop))/(b-a)
    print(a,b,'H/P dB %.1f'%(10*np.log10((H**2).sum()/(P**2).sum())),'flat %.4f'%fl,'on/s %.1f'%on)
print('== C. hat leakage: corr of other-stem 6-10k env with drums-stem 6-10k env (0.125 s smoothing)')
for a,b in [(100,200),(220,270),(285,330)]:
    eo=env(mono['other'][a*sr:b*sr],6000,10000);ed=env(mono['drums'][a*sr:b*sr],6000,10000)
    k=int(0.1*sr/hop);eo=np.convolve(eo,np.ones(k)/k,'same');ed=np.convolve(ed,np.ones(k)/k,'same')
    print(a,b,'corr %.2f'%np.corrcoef(eo,ed)[0,1],'other HF dB %.1f drums HF dB %.1f'%(20*np.log10(eo.mean()),20*np.log10(ed.mean())))
print('== D. bass stem: fundamental vs harmonics, gate shape')
for a,b in [(110,140),(220,250),(270,285)]:
    x=mono['bass'][a*sr:b*sr];S=np.abs(librosa.stft(x,n_fft=8192,hop_length=2048))**2;f=librosa.fft_frequencies(sr=sr,n_fft=8192)
    P=S.mean(1)
    def band(l,h):return 10*np.log10(P[(f>=l)&(f<h)].sum()+1e-12)
    print(a,b,'20-60 %.1f 60-120 %.1f 120-250 %.1f 250-500 %.1f 500-1k %.1f 1k+ %.1f'%(band(20,60),band(60,120),band(120,250),band(250,500),band(500,1000),band(1000,11000)))
print('stab shapes 4:49-5:00 (bass env 10 ms) and kick relation')
eb=env(mono['bass'],None,None);ek=env(mono['drums'],30,150)
t=np.arange(len(eb))*hop/sr
sel=(t>=289)&(t<300)
db=20*np.log10(eb[sel]+1e-6);
# stab starts
thr=-45;on=np.where((db[1:]>thr)&(db[:-1]<=thr))[0]
for i in on:
    tt=t[sel][i+1];seg=db[i+1:i+1+int(0.7*sr/hop)]
    pk=seg.argmax();dec=np.where(seg[pk:]<seg[pk]-20)[0]
    print('stab %.2f peak %.1f dB rise %.0f ms decay-20dB %s ms'%(tt,seg.max(),pk*hop/sr*1000,('%.0f'%(dec[0]*hop/sr*1000)) if len(dec) else '>700'))
# is bass dip on kick beats before 4:48 (sidechain)? mean bass env folded on 0.5s beat
for a,b in [(110,140),(220,280)]:
    m=(t>=a)&(t<b);ph=((t[m]-0.11)%0.5)/0.5
    bins=np.digitize(ph,np.linspace(0,1,11))-1
    prof=[20*np.log10(eb[m][bins==i].mean()+1e-9) for i in range(10)]
    print(a,b,'bass env over beat (10 bins, dB):',' '.join('%.1f'%p for p in prof))
    pk=[20*np.log10(ek[m][bins==i].mean()+1e-9) for i in range(10)]
    print('   kick env:',' '.join('%.1f'%p for p in pk))
print('== E. vocal bursts: band-limit, width, leakage')
def bursts(a,b,thr=-40):
    e=20*np.log10(env(mono['vocals'][a*sr:b*sr])+1e-9);return e
for lab,a,b in [('narr 1:05-1:20',65,80),('narr 2:25-2:36',145,156),('late 3:24-3:40',204,220),('late 4:00-4:20',240,260),('late 4:40-4:59',280,299)]:
    x=mono['vocals'][a*sr:b*sr];e=env(x);act=e>np.percentile(e,70)
    S=np.abs(librosa.stft(x,n_fft=2048,hop_length=hop))**2;f=librosa.fft_frequencies(sr=sr,n_fft=2048)
    n=min(S.shape[1],len(act));P=S[:,:n][:,act[:n]].mean(1);c=np.cumsum(P)/P.sum()
    L,R=st['vocals'][0][0][a*sr:b*sr],st['vocals'][0][1][a*sr:b*sr];M=(L+R)/2;Sd=(L-R)/2
    fl=librosa.feature.spectral_flatness(S=np.sqrt(S[:,:n][:,act[:n]])).mean()
    print(lab,'roll95 %.0f roll99 %.0f cent %.0f flat %.4f S/M %.1f dB'%(f[np.searchsorted(c,.95)],f[np.searchsorted(c,.99)],(P*f).sum()/P.sum(),fl,10*np.log10((Sd**2).sum()/(M**2).sum())))
print('4:38.5 burst: vocals vs drums/other env at 4:37-4:41 (0.1 s steps dB)')
for k in ['vocals','drums','other','bass']:
    e=20*np.log10(env(mono[k][277*sr:281*sr])+1e-9);k2=int(0.25*sr/hop)
    print(k,' '.join('%.0f'%e[i] for i in range(0,len(e)-k2,k2)))
x=mono['vocals'][int(278.2*sr):int(279.4*sr)];S=np.abs(librosa.stft(x,n_fft=1024,hop_length=256))**2;f=librosa.fft_frequencies(sr=sr,n_fft=1024)
P=S.mean(1);print('4:38.2-39.4 vocals roll95 %.0f cent %.0f flat %.3f'%(f[np.searchsorted(np.cumsum(P)/P.sum(),.95)],(P*f).sum()/P.sum(),librosa.feature.spectral_flatness(S=np.sqrt(S)).mean()))
print('== F. other stem at transitions: centroid, width, onset rate in 4 s slices')
for a in [20,24,26,28,29,30,32,80,84,86,88,89,90,92,94]:
    x=mono['other'][a*sr:(a+2)*sr];c=librosa.feature.spectral_centroid(y=x,sr=sr).mean()
    L,R=st['other'][0][0][a*sr:(a+2)*sr],st['other'][0][1][a*sr:(a+2)*sr]
    print(a,'rms %.1f cent %.0f corr %.2f'%(20*np.log10(np.sqrt((x**2).mean())+1e-9),c,np.corrcoef(L,R)[0,1]))
