import numpy as np, librosa, scipy.signal as ss
y,sr=librosa.load('v1/data/video2/stems_raw/htdemucs/song/drums.wav',sr=22050,mono=True,offset=120,duration=30)
k=ss.sosfilt(ss.butter(4,120,'low',fs=sr,output='sos'),y)
e=np.abs(ss.hilbert(k)); e=ss.savgol_filter(e,101,2)
p,_=ss.find_peaks(e,distance=int(0.35*sr),height=np.percentile(e,60))
print('n kicks',len(p),'IOI mean/std ms',np.diff(p).mean()/sr*1000,np.diff(p).std()/sr*1000)
W=[]
for i in p:
    s=i-int(0.01*sr)
    if s>0 and s+int(0.2*sr)<len(k): W.append(k[s:s+int(0.2*sr)])
W=np.array(W); 
pkdb=20*np.log10(np.abs(W).max(1)); print('peak dB mean/std',pkdb.mean(),pkdb.std())
c=np.corrcoef(W); print('waveform corr mean',(c.sum()-len(c))/(len(c)**2-len(c)))
E=np.array([np.abs(ss.hilbert(w)) for w in W]); 
d=[20*np.log10(x[int(.11*sr)]/x[int(.02*sr)]) for x in E]; print('decay 20->110ms dB mean/std',np.mean(d),np.std(d))
