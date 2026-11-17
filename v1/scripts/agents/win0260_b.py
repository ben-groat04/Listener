import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050
def L(p,s,d): y,_=librosa.load(p,sr=sr,mono=True,offset=s,duration=d); return y
dr=L(D+'stems_raw/htdemucs/song/drums.wav',255,30)
sos=ss.butter(4,[35,110],'band',fs=sr,output='sos'); k=ss.sosfiltfilt(sos,dr)
env=np.abs(ss.hilbert(k)); env=ss.savgol_filter(env,101,3)
pk,_=ss.find_peaks(env,height=env.max()*0.3,distance=int(0.15*sr))
t=pk/sr+255; w=t[(t>=260)&(t<280)]; print('kick n',len(w),np.round(w,2)); ioi=np.diff(w); print('ioi med',np.median(ioi),'mean',ioi.mean(),'std',ioi.std())
for per in [60/123.05]:
    best=min((np.std(((w-ph+per/2)%per)-per/2),ph) for ph in np.linspace(0,per,200)); print('123.05 grid resid ms',best[0]*1000)
# tone line
o=L(D+'stems_raw/htdemucs/song/other.wav',260,3)
S=np.abs(np.fft.rfft(o*np.hanning(len(o))));f=np.fft.rfftfreq(len(o),1/sr);m=(f>300)&(f<1500)
idx=np.argsort(S[m])[-5:];print('peak freqs 260-263',f[m][idx])
# loop regularity: chroma+rms similarity of consecutive 4-beat bars
x=L(D+'audio/song.wav',256,30); bar=int(sr*4*60/123.05)
def s(a,b):return np.corrcoef(np.abs(librosa.stft(a,n_fft=1024)).mean(1),np.abs(librosa.stft(b,n_fft=1024)).mean(1))[0,1]
dd=dr[:len(dr)]; 
bars=[dr[i*bar:(i+1)*bar] for i in range(len(dr)//bar)]
env_b=[np.abs(librosa.onset.onset_strength(y=b_,sr=sr,hop_length=512))[:40] for b_ in bars]
print('bar drum onset-env corr consecutive',[round(float(np.corrcoef(env_b[i],env_b[i+1])[0,1]),2) for i in range(len(env_b)-1)])
