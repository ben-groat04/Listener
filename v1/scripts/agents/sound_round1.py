import numpy as np, soundfile as sf, librosa, json, sys
D='data/video1/'
def ld(n):
    p=D+'audio/song.wav' if n=='song' else D+f'stems_raw/htdemucs/song/{n}.wav'
    y,sr=sf.read(p,always_2d=True); return y.T,sr
mix,sr=ld('song')
L,R=mix
M=(L+R)/2;S=(L-R)/2
# loudness / crest / stereo per 20 s
def db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
print('t  rmsdB peakdB crest  M/S(dB) corr  cent  rolloff95 flat')
for t0 in range(0,189,10):
    a=int(t0*sr);b=int(min(t0+10,188.6)*sr)
    l,r,m,s=L[a:b],R[a:b],M[a:b],S[a:b]
    pk=20*np.log10(np.max(np.abs(mix[:,a:b]))+1e-9)
    c=np.corrcoef(l,r)[0,1]
    sp=np.abs(librosa.stft(m,n_fft=2048))
    cent=librosa.feature.spectral_centroid(S=sp,sr=sr).mean()
    ro=librosa.feature.spectral_rolloff(S=sp,sr=sr,roll_percent=.95).mean()
    fl=librosa.feature.spectral_flatness(S=sp).mean()
    print(f'{t0//60}:{t0%60:02d} {db(m):6.1f} {pk:6.1f} {pk-db(m):5.1f} {db(s)-db(m):6.1f} {c:5.2f} {cent:6.0f} {ro:6.0f} {fl:.3f}')
# overall band split
sp=np.abs(librosa.stft(M,n_fft=4096))**2
fr=librosa.fft_frequencies(sr=sr,n_fft=4096)
tot=sp.sum()
for lo,hi in [(20,60),(60,150),(150,500),(500,2000),(2000,6000),(6000,12000),(12000,22050)]:
    print('band',lo,hi,round(100*sp[(fr>=lo)&(fr<hi)].sum()/tot,1))
# stems stereo + hf
for n in ['vocals','drums','bass','other']:
    y,_=ld(n);l,r=y
    sp=np.abs(librosa.stft((l+r)/2,n_fft=2048)); 
    print(n,'corr',round(np.corrcoef(l,r)[0,1],2),'S/M dB',round(db((l-r)/2)-db((l+r)/2),1),'rolloff99',round(librosa.feature.spectral_rolloff(S=sp,sr=sr,roll_percent=.99).mean()),'flat',round(librosa.feature.spectral_flatness(S=sp).mean(),3),'cent',round(librosa.feature.spectral_centroid(S=sp,sr=sr).mean()))
# peak spectral content above 16k
sp=np.abs(librosa.stft(M,n_fft=4096))
for f in [8000,10000,12000,16000,18000,20000]:
    print('mean dB >',f, round(20*np.log10(sp[fr>=f].mean()+1e-9),1))
# sub bass pitch 2:01-2:40
y,_=ld('bass');b=(y[0]+y[1])/2
for t0,t1 in [(121.5,122.8),(127.5,128.8),(133.6,134.8),(140,141),(60,70),(30,40),(170,180)]:
    seg=b[int(t0*sr):int(t1*sr)]
    X=np.abs(np.fft.rfft(seg*np.hanning(len(seg)),n=1<<19));f=np.fft.rfftfreq(1<<19,1/sr)
    m=(f>25)&(f<300);k=np.argmax(X[m]);
    pk=f[m][k]; 
    # harmonic levels
    def lv(fq):
        i=np.argmin(abs(f-fq));return 20*np.log10(X[i-20:i+20].max()+1e-9)
    print(f'{t0}-{t1} peak {pk:.1f}Hz  h2-h1 {lv(2*pk)-lv(pk):.1f} h3-h1 {lv(3*pk)-lv(pk):.1f}')
