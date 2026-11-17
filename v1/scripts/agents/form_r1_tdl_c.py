import numpy as np, librosa, soundfile as sf, scipy.signal as ss
from scipy.signal import find_peaks
D='/home/user/Listener/v1/data/t_dl_mirror/'
S=D+'stems_raw/htdemucs/song/'
x,sr=sf.read(D+'audio/song.wav'); m=x.mean(1)
h=int(sr*0.01); a=int(235.5*sr)//h*h; seg=m[a:a+int(1.2*sr)//h*h]; e=10*np.log10((seg.reshape(-1,h)**2).mean(1)+1e-14)
p,_=find_peaks(e,height=-80,prominence=1.5)
print('final peaks',[(round(235.5+i*0.01,2),round(e[i],1)) for i in p if e[i]>-70])
# stem 10ms env near end (3:55-3:57)
for k in ['drums','bass','other','vocals']:
    y=sf.read(S+k+'.wav')[0].mean(1); s=y[int(235.5*sr):int(237*sr)]; ee=10*np.log10((s[:len(s)//h*h].reshape(-1,h)**2).mean(1)+1e-14)
    print(k,'max 235.5-237',round(ee.max(),1),'dB; mean 237.5-239.4', round(10*np.log10((y[int(237.5*sr):]**2).mean()+1e-14),1))
d=sf.read(S+'drums.wav')[0].mean(1); d=np.nan_to_num(d)
sos=ss.butter(4,[40,120],'bp',fs=sr,output='sos'); k=ss.sosfiltfilt(sos,d)
on=librosa.onset.onset_detect(y=k.astype(np.float32),sr=sr,units='time',hop_length=256,delta=0.15)
on=on[(on>5)&(on<215)]; ioi=np.diff(on)
print('kick onsets',len(on),'median IOI',np.median(ioi),'BPM',60/np.median(ioi))
# phase against fitted grid
T=np.median(ioi)*4 # guess bar? try beat period from 60/94
for P in [60/95.7*0.5, 60/95.7, 60/95.7*2]:
    ph=(on%P)/P; ang=np.angle(np.mean(np.exp(2j*np.pi*ph))); res=((ph-ang/(2*np.pi)+0.5)%1-0.5)*P
    print('grid',round(P,4),'rms dev ms',round(1000*np.sqrt(np.mean(res**2)),1),'R',round(abs(np.mean(np.exp(2j*np.pi*ph))),3))
# bar-level loop regularity of "other" stem chroma: self-similarity at lag of 4 beats (bar) vs random
o=sf.read(S+'other.wav')[0].mean(1); o=np.nan_to_num(o)
ch=librosa.feature.chroma_cqt(y=o[::2],sr=sr//2,hop_length=512); fps=(sr//2)/512
bar=int(round(4*60/95.7*fps)); 
for L in [bar,2*bar,4*bar]:
    c=[np.corrcoef(ch[:,i],ch[:,i+L])[0,1] for i in range(0,ch.shape[1]-L,3)]
    print('chroma self-corr at lag',round(L/fps,2),'s mean',round(np.nanmean(c),3))
# drums bar repeat: low-band onset envelope autocorr
env=librosa.onset.onset_strength(y=d.astype(np.float32),sr=sr,hop_length=512); 
bf=sr/512; L=int(round(4*60/95.7*bf)); 
c=[np.corrcoef(env[i:i+L],env[i+L:i+2*L])[0,1] for i in range(int(10*bf),int(200*bf),L)]
print('drum onset-env bar-to-bar corr mean',round(np.mean(c),3),'min',round(min(c),3))
