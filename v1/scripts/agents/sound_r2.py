import numpy as np, soundfile as sf, scipy.signal as ss
D='/home/user/Listener/v1/data/t_cshells_cshore/'
def ld(p):
    x,sr=sf.read(p); 
    return (x.mean(1) if x.ndim>1 else x),sr
mix,sr=ld(D+'audio/song.wav')
st={k:ld(D+f'stems_raw/htdemucs/song/{k}.wav')[0] for k in ['vocals','drums','bass','other']}
def seg(x,a,b): return x[int(a*sr):int(b*sr)]
def db(v): return 20*np.log10(max(v,1e-12))
def psd(x):
    f,p=ss.welch(x,sr,nperseg=16384); return f,p
def band(x,lo,hi):
    f,p=psd(x); m=(f>=lo)&(f<hi); return 10*np.log10(p[m].sum()+1e-20)
print('--- A. final pad partials')
for a,b in [(5*60+22,5*60+30),(5*60+30,5*60+38)]:
    x=seg(st['other'],a,b); n=len(x); w=np.hanning(n); X=np.abs(np.fft.rfft(x*w,8*n)); f=np.fft.rfftfreq(8*n,1/sr)
    out=[]
    for h in range(1,7):
        m=(f>215*h*0.97)&(f<222*h*1.03); i=np.argmax(X[m]); out.append((round(f[m][i],2),round(db(X[m][i]/X.max()),1)))
    f1=out[0][0]; print(a,b,out,'cents vs 220: %.1f'%(1200*np.log2(f1/220)))
    env=np.abs(ss.hilbert(ss.sosfilt(ss.butter(4,[150,300],'bp',fs=sr,output='sos'),x)))
    e=ss.sosfilt(ss.butter(2,10,'lp',fs=sr,output='sos'),env)[sr:-sr]; e=e-e.mean()
    F=np.abs(np.fft.rfft(e*np.hanning(len(e)))); ff=np.fft.rfftfreq(len(e),1/sr); m=(ff>0.2)&(ff<8)
    print(' AM depth(std/mean)=%.3f peak mod Hz=%.2f'%(env.std()/env.mean(),ff[m][np.argmax(F[m])]))
print('--- B. 3:44 low band in mix and stems (dB, 30-150Hz / 150-1000 / 1-4k)')
for a,b in [(3*60+30,3*60+43),(3*60+47,4*60+0)]:
    print(a,b,'mix',[round(band(seg(mix,a,b),lo,hi),1) for lo,hi in [(30,150),(150,1000),(1000,4000)]],
     'bass',round(band(seg(st['bass'],a,b),30,150),1),'other',[round(band(seg(st['other'],a,b),lo,hi),1) for lo,hi in [(30,150),(150,1000),(1000,4000)]])
print('--- C. voice events: mix band shares and tilt vs 6 s before')
def sh(x):
    f,p=psd(x); t=p.sum(); return [round(100*p[(f>=lo)&(f<hi)].sum()/t,1) for lo,hi in [(0,200),(200,1000),(1000,4000),(4000,8000),(8000,17000)]]
for name,(a,b) in {'2:21.5-2:26':(141.5,146),'4:28.5-4:31':(268.5,271),'5:12-5:13':(312,313.2),'5:30-5:42':(330.5,342.5)}.items():
    pre=(a-8,a-2)
    print(name,'mix',sh(seg(mix,a,b)),'pre',sh(seg(mix,*pre)),'vocal stem',sh(seg(st['vocals'],a,b)))
    v=seg(st['vocals'],a,b); f,p=psd(v); c=np.cumsum(p)/p.sum(); print('  vocal 85%% roll %.0f Hz 95%% %.0f Hz'%(f[np.searchsorted(c,.85)],f[np.searchsorted(c,.95)]))
# reverb: decay of vocal envelope at 2:22
v=st['vocals']; env=np.sqrt(np.convolve(v**2,np.ones(int(.05*sr))/int(.05*sr),'same'))
for t in np.arange(141.5,147,0.5): print(' voc env %.1f %.1f dB'%(t,db(env[int(t*sr)])),end=';')
print()
print('--- D. stab decay 1:00-1:20 (other stem, 20ms rms) and low band 40-90Hz in mix, drums')
o=st['other']; hop=int(.02*sr)
for t0 in [60.83,64.84,68.85,72.89]:
    r=[db(np.sqrt(np.mean(seg(o,t0+k*.5,t0+k*.5+.02)**2))) for k in range(0,8)]
    print(t0,[round(v,1) for v in r])
print('--- E. low drum: 45-90Hz band onsets in DRUMS stem vs BASS stem 120-160 s; share of 45-90 power')
for a,b in [(120,160),(260,300)]:
    for k in ['drums','bass','other']:
        x=seg(st[k],a,b); print(a,b,k,'45-90Hz dB',round(band(x,45,90),1),'90-300',round(band(x,90,300),1),'300-3k',round(band(x,300,3000),1),'3k-10k',round(band(x,3000,10000),1))
# drum low-band crest
sos=ss.butter(4,[45,90],'bp',fs=sr,output='sos')
for k in ['drums','bass']:
    x=ss.sosfilt(sos,seg(st[k],120,160)); e=np.sqrt(ss.sosfilt(ss.butter(2,30,'lp',fs=sr,output='sos'),x**2)); 
    print(k,'low-band envelope crest (max/median) %.1f dB, peaks/s'%db(e.max()/np.median(e)), len(ss.find_peaks(e,prominence=e.max()*.2,distance=int(.1*sr))[0])/40)
