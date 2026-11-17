import numpy as np, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050; hop=32; fr=sr/hop
dr,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)
oe=librosa.onset.onset_strength(y=dr,sr=sr,hop_length=hop,n_fft=1024)
def acf(x):
    x=x-x.mean(); n=len(x); F=np.fft.rfft(x,2*n); a=np.fft.irfft(F*np.conj(F))[:n]; return a/a[0]
for (s,e) in [(0,10),(0,20),(10,20),(20,30),(15,35),(25,45),(215,230),(228,236)]:
    a=acf(oe[int(s*fr):int(e*fr)]); lags=np.arange(len(a))/fr
    w=(lags>2.3)&(lags<2.75); i=np.argmax(np.where(w,a,-9))
    w1=(lags>0.58)&(lags<0.70); j=np.argmax(np.where(w1,a,-9))
    print(s,e,'bar lag',round(lags[i],3),'r',round(a[i],2),'bpm',round(240/lags[i],2),'| beat lag',round(lags[j],3),round(a[j],2))
