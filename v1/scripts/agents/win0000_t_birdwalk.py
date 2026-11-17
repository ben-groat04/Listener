import numpy as np,librosa,soundfile as sf
d='stems_raw/htdemucs/song/'
def ld(n,s=0,e=22):
    y,sr=sf.read(d+n+'.wav',start=int(s*44100),stop=int(e*44100));return y,sr
mix,sr=sf.read('audio/song.wav',stop=22*44100);print('sr',sr,mix.shape)
m=mix if mix.ndim==1 else mix.mean(1)
print('sample peak dBFS 0-20 L/R',[20*np.log10(np.abs(mix[:20*sr,i]).max()) for i in range(mix.shape[1])] if mix.ndim>1 else '')
print('peak 0-12',20*np.log10(np.abs(mix[:12*sr]).max()),'12-20',20*np.log10(np.abs(mix[12*sr:20*sr]).max()))
dr,_=ld('drums');dm=dr.mean(1)
for lab,(lo,hi) in {'0-12':(0,12),'12-20':(12,20)}.items():
    seg=dm[int(lo*sr):int(hi*sr)]
    # low-band for kick
    import scipy.signal as ss
    b,a=ss.butter(4,150/(sr/2));lowb=ss.filtfilt(b,a,seg)
    for nm,x in [('full',seg),('lowband',lowb)]:
        on=librosa.onset.onset_detect(y=x,sr=sr,units='time',backtrack=False,delta=0.15)
        print(lab,nm,np.round(on+lo,2).tolist())
        if len(on)>2: print(' IOI',np.round(np.diff(on),2).tolist())
# band energy of mix: rolloff
S=np.abs(librosa.stft(m[:20*sr],n_fft=4096))**2
f=librosa.fft_frequencies(sr=sr,n_fft=4096)
for lo,hi in [(0,12),(12,20)]:
    fr=S[:,int(lo*sr/1024):int(hi*sr/1024)].mean(1);c=np.cumsum(fr)/fr.sum()
    print(lo,hi,'rolloff95',f[np.searchsorted(c,.95)],'99',f[np.searchsorted(c,.99)],'above 10k dB rel',10*np.log10(fr[f>10000].sum()/fr.sum()),'above 16k',10*np.log10(fr[f>16000].sum()/fr.sum()))
for n in ['vocals','other','bass']:
    y,_=ld(n,0,20);ym=y.mean(1)
    print(n,'peak dB',20*np.log10(np.abs(y).max()),'rms 0-12',20*np.log10(np.sqrt((ym[:12*sr]**2).mean())),'12-20',20*np.log10(np.sqrt((ym[12*sr:]**2).mean())))
# bass entry
b,_=ld('bass',10,16);e=np.sqrt(np.convolve(b.mean(1)**2,np.ones(441)/441,'same'))[::441]
t=np.arange(len(e))*.01+10;i=np.argmax(e>0.02);print('bass entry',t[i]);
# bass pitch
by,_=ld('bass',12,20);f0=librosa.pyin(by.mean(1),fmin=30,fmax=200,sr=sr)[0];ff=f0[~np.isnan(f0)];print('bass f0 median',np.median(ff),np.percentile(ff,[10,90]))
# bar-repeat check on mix: chroma/mel correlation of beat-spaced segments in 0-12
tempo=librosa.beat.beat_track(y=m[:20*sr],sr=sr)[0];print('tempo',tempo)
