import numpy as np, soundfile as sf, scipy.signal as ss, json, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=44100
x,_=sf.read(D+'audio/song.wav'); m=x.mean(1)
# clip runs
c=(np.abs(x[:,0])>=0.9999).astype(int); d=np.diff(np.r_[0,c,0]); st=np.nonzero(d==1)[0]; en=np.nonzero(d==-1)[0]; rl=en-st
print('clip runs',len(rl),'len>=2',(rl>=2).sum(),'max run',rl.max(),'hist',np.bincount(rl)[:8])
# clip density per 30s
for t in range(0,240,30):
    print(t,'clipped samples',int(c[t*sr:(t+30)*sr].sum()),end=' | ')
print()
# LR diff location
L,R=x[:,0],x[:,1]; di=np.nonzero(L!=R)[0]
print('LR diff clusters (s):',np.unique(np.round(di/sr,0))[:30], 'max |L-R|',np.abs(L-R).max(), 'dB vs mix', 20*np.log10(np.abs(L-R).max()+1e-12))
# stems
S={}
for s in ['vocals','drums','bass','other']:
    y,_=sf.read(D+f'stems_raw/htdemucs/song/{s}.wav'); S[s]=y.mean(1)
    f,P=ss.welch(S[s],sr,nperseg=8192); Pd=10*np.log10(P+1e-20)
    r=np.cumsum(P)/P.sum(); ro95=f[np.searchsorted(r,.95)]; ro99=f[np.searchsorted(r,.99)]
    cent=(f*P).sum()/P.sum()
    pk=20*np.log10(abs(S[s]).max()); rms=20*np.log10(np.sqrt((S[s]**2).mean()))
    print(s,'peak',round(pk,1),'rms',round(rms,1),'rolloff95',round(ro95),'99',round(ro99),'centroid',round(cent),'psd@7k',round(Pd[np.argmin(abs(f-7000))],1),'@9k',round(Pd[np.argmin(abs(f-9000))],1))
# other: noise floor / clicks (vinyl crackle test): highpass 3k, count impulsive events
o=S['other']; 
for name,y in [('mix',m),('other',o)]:
    h=ss.sosfilt(ss.butter(4,3000,'hp',fs=sr,output='sos'),y)
    e=np.abs(h); med=ss.medfilt(e[::441][:],21)
    print(name,'hp3k rms dB',round(20*np.log10(np.sqrt((h**2).mean())),1))
# spectral flatness of other in steady region 3:40-3:48
seg=o[int(220*sr):int(228*sr)]
f,P=ss.welch(seg,sr,nperseg=16384); 
pk,_=ss.find_peaks(10*np.log10(P+1e-20),prominence=15)
print('other 3:40-3:48 strongest partials Hz',np.round(f[pk][np.argsort(P[pk])[::-1][:12]],1))
# drum kick: low band onsets
dr=S['drums']; lo=ss.sosfilt(ss.butter(4,150,'lp',fs=sr,output='sos'),dr)
oe=librosa.onset.onset_strength(y=lo,sr=sr,hop_length=220)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=220,units='time',backtrack=False)
ioi=np.diff(on); print('kick n',len(on),'median ioi',np.median(ioi))
h,b=np.histogram(ioi,bins=np.arange(0.1,1.3,0.02)); print([ (round(b[i],2),h[i]) for i in np.argsort(h)[::-1][:8]])
# grid dev: fit 16th grid at kick period
for per in [0.157,0.1595,0.1566]:
    ph=np.mod(on,per); ang=np.exp(2j*np.pi*ph/per).mean(); dev=np.angle(ang)/(2*np.pi)*per
    res=((ph-dev+per/2)%per)-per/2
    print('grid',per,'BPM16th',round(60/per/4,2),'R',round(abs(ang),3),'rms dev ms',round(1000*np.sqrt((res**2).mean()),1),'uniform rms ms',round(1000*per/np.sqrt(12),1))
# loop regularity: bar-lag correlation of mel of other and bass, drums over track
bar=2.508
for s in ['other','bass','drums']:
    M=librosa.power_to_db(librosa.feature.melspectrogram(y=S[s][::2],sr=sr//2,n_mels=64,hop_length=441),ref=1)
    fr=int(round(bar/0.02)); 
    cs=[]
    for k in range(0,M.shape[1]-2*fr,fr):
        a=M[:,k:k+fr].ravel(); bb=M[:,k+fr:k+2*fr].ravel(); cs.append(np.corrcoef(a,bb)[0,1])
    print(s,'bar-to-next-bar mel corr median',round(np.median(cs),3))
# 10 ms envelope corr drums bar-to-bar with beat-synchronised sample for exact repeat check
# dynamic: stem share per 30s
for t in range(0,240,30):
    print(t,{k:round(20*np.log10(np.sqrt((v[t*sr:(t+30)*sr]**2).mean())+1e-9),1) for k,v in S.items()})
