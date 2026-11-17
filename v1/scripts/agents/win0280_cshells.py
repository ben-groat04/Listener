import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_cshells_cshore/'
t0,t1=270,305
def load(p):
    y,sr=librosa.load(p,sr=None,mono=False,offset=t0,duration=t1-t0); return y,sr
mix,sr=load(D+'audio/song.wav'); m=mix.mean(0) if mix.ndim>1 else mix
print('sr',sr,'peak in 280-300 (sample):',20*np.log10(np.abs(mix[:,10*sr:30*sr]).max()))
st={}
for n in['vocals','drums','bass','other']:
    y,_=load(D+f'stems_raw/htdemucs/song/{n}.wav'); st[n]=y.mean(0)
def env(x,hop=sr//100):
    r=np.sqrt(np.convolve(x**2,np.ones(hop)/hop,'same'))[::hop]; return 20*np.log10(r+1e-9)
# mean level per 1 s in window per stem, and in 0.5 s around boundaries
for name,x in [('mix',m)]+list(st.items()):
    e=env(x)
    print(name,' '.join(f'{e[int(a*100):int((a+1)*100)].mean():.0f}' for a in range(5,30)))
# drum onsets
d=st['drums']; oenv=librosa.onset.onset_strength(y=d,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oenv,sr=sr,hop_length=256,units='time',backtrack=False)+t0
print('drum onsets 280-300',len(on[(on>=280)&(on<300)]))
# low-band kick onsets
dl=ss.sosfilt(ss.butter(4,150,'low',fs=sr,output='sos'),d)
ol=librosa.onset.onset_strength(y=dl,sr=sr,hop_length=256)
k=librosa.onset.onset_detect(onset_envelope=ol,sr=sr,hop_length=256,units='time',delta=0.3)+t0
k=k[(k>=280)&(k<300)]; ioi=np.diff(k)
print('kicks',len(k),np.round(k,2)); print('IOI median',np.median(ioi),'bpm',60/np.median(ioi))
for lo,hi,nm in [(280,286,'A 280-286'),(288,300,'B 288-300')]:
    kk=k[(k>=lo)&(k<hi)]; i=np.diff(kk)
    if len(i)>2:
        g=np.median(i); res=(kk-kk[0])/g; res=res-np.round(res); print(nm,'n',len(kk),'IOI med',g,'resid std ms',np.std(res)*g*1000)
tempo,b=librosa.beat.beat_track(y=d,sr=sr,start_bpm=123); print('tempo',tempo)
# spectral centroid/brightness per 5 s
for a in range(280,300,5):
    s=m[(a-t0)*sr:(a+5-t0)*sr]; c=librosa.feature.spectral_centroid(y=s,sr=sr).mean()
    S=np.abs(np.fft.rfft(s))**2;f=np.fft.rfftfreq(len(s),1/sr)
    print(a,'centroid',round(c),'>6k share dB',10*np.log10(S[f>6000].sum()/S.sum()),'<150 share',10*np.log10(S[f<150].sum()/S.sum()))
# bass entry, other 1k tone
b=st['bass']; e=env(b); print('bass env 284-289 each 0.5s',[round(e[int((a-t0)*100):int((a-t0+.5)*100)].mean()) for a in np.arange(284,289,.5)])
o=st['other']; S=np.abs(librosa.stft(o[int(10*sr):int(12*sr)],n_fft=8192)).mean(1); f=librosa.fft_frequencies(sr=sr,n_fft=8192)
print('other 280-282 peak freqs',f[np.argsort(S)[-6:]])
S=np.abs(librosa.stft(o[int(15*sr):int(17*sr)],n_fft=8192)).mean(1); print('other 285-287 peak',f[np.argsort(S)[-6:]])
v=st['vocals'];S=np.abs(librosa.stft(v[int(26*sr):int(29*sr)],n_fft=8192)).mean(1);print('vocals 296-299 peaks',f[np.argsort(S)[-6:]])
# loop regularity: autocorr of mono at bar lag
bar=4*60/123
for a,b2 in[(280,286),(288,300)]:
    x=m[int((a-t0)*sr):int((b2-t0)*sr)]; c=librosa.feature.chroma_cqt(y=x,sr=sr); 
    n=c.shape[1]; fps=sr/512; L=int(round(bar*fps)); print(a,'chroma bar-lag corr',np.mean([np.corrcoef(c[:,:n-L].ravel(),c[:,L:].ravel())[0,1]]))
