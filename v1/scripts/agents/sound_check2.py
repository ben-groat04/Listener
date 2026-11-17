import numpy as np, soundfile as sf, scipy.signal as ss, librosa, json
D='/home/user/Listener/v1/data/t_cshells_cshore/'
x,sr=sf.read(D+'audio/song.wav'); m=x.mean(1)
f,P=ss.welch(m[60*sr:320*sr],sr,nperseg=8192)
print('HF PSD dB (60-320s):',{k:round(10*np.log10(P[np.argmin(abs(f-k))]+1e-30),1) for k in [100,1000,5000,8000,10000,12000,14000,16000,18000,20000,21500]})
f2,P2=ss.welch(m[12*sr:20*sr],sr,nperseg=8192)
print('HF PSD dB (12-20s):',{k:round(10*np.log10(P2[np.argmin(abs(f2-k))]+1e-30),1) for k in [100,1000,5000,8000,10000,12000,14000,16000,18000,20000]})
# first 100ms at 11.3
a=int(11.2*sr); seg=m[a:a+int(0.3*sr)]
env=np.array([np.abs(seg[i:i+441]).max() for i in range(0,len(seg)-441,441)])
print('11.2-11.5 10ms peak dB',np.round(20*np.log10(env+1e-12),0))
# end: last 3 s of audible: 339.8-342.9 and 10ms env of mix and stems
def env10(y): 
    n=len(y)//441; return np.sqrt((y[:n*441].reshape(n,441)**2).mean(1))
S={}
for nm in ['vocals','drums','bass','other']:
    s,_=sf.read(D+f'stems_raw/htdemucs/song/{nm}.wav'); S[nm]=s.mean(1) if s.ndim>1 else s
e=env10(m); t0=int(339.9*100); 
print('mix 10ms RMS dB last audible 339.9-342.95 step 0.25s:')
for i in range(t0,t0+310,25): print(round(i/100,2),round(20*np.log10(e[i]+1e-12),1), {k:round(20*np.log10(env10(v)[i]+1e-12),0) for k,v in S.items()})
last=np.nonzero(e>1e-6)[0][-1]; print('last env>-120dB at',last/100, 'level',20*np.log10(e[last-3:last+1]+1e-12))
print('final 20 frames dB',np.round(20*np.log10(e[last-19:last+3]+1e-12),1))
# peaks in last 3s env (count local maxima, prominence 3dB)
seg=20*np.log10(env10(m[int(339.9*sr):int(343.1*sr)])+1e-12)
pk,_=ss.find_peaks(seg,prominence=3); print('env peaks (prom 3dB) in 339.9-343.1:',(pk/100+339.9).round(2),seg[pk].round(1))
# fade slope
for t in range(326,344,2): print(t, round(20*np.log10(e[t*100:(t+1)*100].mean()+1e-12),1))
