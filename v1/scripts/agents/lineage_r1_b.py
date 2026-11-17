import numpy as np, librosa, soundfile as sf, scipy.signal as sg
D='/home/user/Listener/v1/data/t_dl_mirror/'; S=D+'stems_raw/htdemucs/song/'; sr=44100
mix,_=sf.read(D+'audio/song.wav'); m=mix.mean(1)
st={k:sf.read(S+k+'.wav')[0].mean(1) for k in ['vocals','drums','bass','other']}
print('L-R corr',np.corrcoef(mix[:,0],mix[:,1])[0,1],'duration',len(m)/sr)
print('tuning offset (semitone frac) other',librosa.estimate_tuning(y=st['other'][20*sr:200*sr],sr=sr), 'mix',librosa.estimate_tuning(y=m[20*sr:200*sr],sr=sr))
F,P=sg.welch(m,sr,nperseg=8192); 
for f in [4000,6000,7000,7800,8000,8200,9000,12000,16000]:
    i=np.argmin(abs(F-f)); print('welch dB at',f,round(10*np.log10(P[i]+1e-20),1))
# bass note decay: onsets (rise) and level at +0.1,+0.3,+0.6 s after envelope peak
b=st['bass']; hop=int(0.01*sr)
e=np.sqrt(np.convolve(b**2,np.ones(hop)/hop,'same'))[::hop]; db=20*np.log10(e+1e-9)
pk,_=sg.find_peaks(db,height=-22,distance=30)
pk=[p for p in pk if 40<p*0.01<215]
res=[]
for p in pk:
    if p+70<len(db): res.append([db[p+k]-db[p] for k in (10,30,60)])
res=np.array(res); print('bass peaks',len(pk),'decay dB at +0.1,+0.3,+0.6 s median',np.median(res,0), 'p25',np.percentile(res,25,0),'p75',np.percentile(res,75,0))
# backbeat: drums 1.5-5k onset energy folded on bar (94.0 BPM, 4 beats) using kick-aligned? use autocorr folding with offset search
d=st['drums']; sos=sg.butter(4,[1500,5000],'bandpass',fs=sr,output='sos'); dm=sg.sosfilt(sos,d)
beat=60/94.0
env=librosa.onset.onset_strength(y=dm,sr=sr,hop_length=220); t=np.arange(len(env))*220/sr
sel=(t>30)&(t<215)
best=None
for off in np.arange(0,4*beat,0.01):
    ph=((t[sel]-off)/beat)%4
    bins=np.floor(ph*4).astype(int)%16
    prof=np.array([env[sel][bins==k].mean() for k in range(16)])
    sc=prof[4]+prof[12]-prof[0]-prof[8]
    if best is None or sc>best[0]: best=(sc,off,prof)
print('16-step profile (best backbeat offset %.2f s):'%best[1],np.round(best[2]/best[2].max(),2))
# swing: ratio of even/odd 16th energies in best profile
p=best[2]; print('8th offbeat(steps 2,6,10,14) vs onbeat(0,4,8,12) means',p[[2,6,10,14]].mean(),p[[0,4,8,12]].mean(),'odd 16ths',p[[1,3,5,7,9,11,13,15]].mean())
# end of track: 10ms env last 3s of audio
for name,x in [('mix',m)]+list(st.items()):
    n=int(0.01*sr); seg=x[-3*sr:]; e=np.sqrt(np.convolve(seg**2,np.ones(n)/n,'same'))[::n]; dbs=20*np.log10(e+1e-9)
    nz=np.where(dbs>-90)[0]
    print(name,'last 3s: last >-90dB at',(len(m)/sr-3)+(nz[-1]*0.01 if len(nz) else -1), 'level max',round(dbs.max(),1),'last 20 frames',np.round(dbs[-5:],1))
# find last audible in mix over whole tail
n=int(0.01*sr); e=np.sqrt(np.convolve(m[-8*sr:]**2,np.ones(n)/n,'same'))[::n]; dbs=20*np.log10(e+1e-9)
t0=len(m)/sr-8
for th in (-60,-70,-80,-90): 
    nz=np.where(dbs>th)[0]; print('last frame above',th,'dB at',round(t0+nz[-1]*0.01,2) if len(nz) else None)
pk,_=sg.find_peaks(dbs,height=-75,prominence=6); print('tail peaks (10ms env, >-75, prom 6 dB):',[(round(t0+p*0.01,2),round(dbs[p],1)) for p in pk])
# boundary table: 0.5 s RMS windows before/after (1.5 s each)
def rms(x,a,b): s=x[int(a*sr):int(b*sr)]; return round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1)
for t in [10.4,30.4,71.3,91.4,132.0,154.5,194.0,215.3,229.0]:
    print('boundary',t, {k:(rms(x,t-1.5,t-0.1),rms(x,t+0.1,t+1.5)) for k,x in [('mix',m)]+list(st.items())})
