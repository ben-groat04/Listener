import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
S=D+'stems_raw/htdemucs/song/'
t0,t1=60,80
def ld(p): return librosa.load(p,sr=22050,mono=False,offset=t0-1,duration=t1-t0+2)
y,sr=ld(D+'audio/song.wav'); m=y.mean(0)
print('mix sample peak dBFS',20*np.log10(np.abs(y).max()), 'L/R corr', np.corrcoef(y[0],y[1])[0,1] if y.ndim>1 else None)
dr,_=ld(S+'drums.wav'); dm=dr.mean(0)
# kick band
import scipy.signal as ss
b,a=ss.butter(4,150,'low',fs=sr); k=ss.filtfilt(b,a,dm)
env=librosa.onset.onset_strength(y=k,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=256,units='time',backtrack=False)+ (t0-1)
on=on[(on>=t0)&(on<t1)]
ioi=np.diff(on); print('kick onsets',np.round(on,2)); print('IOI median',np.median(ioi),'bpm-ish',60/np.median(ioi))
# grid fit: tempo 95.7
bt=json.load(open(D+'audio_features/beat_times.json')); bt=np.array(bt if isinstance(bt,list) else bt.get('beats',[]))
bt=bt[(bt>=t0)&(bt<t1)]; print('beat IOI med',np.median(np.diff(bt)), 'n',len(bt))
beat=np.median(np.diff(bt)); 
for div,name in [(1,'beat'),(0.5,'8th'),(0.25,'16th')]:
    g=beat*div; ph=((on-bt[0])/g); dev=(ph-np.round(ph))*g*1000
    print(name,'grid dev ms mean abs',np.abs(dev).mean(),'std',dev.std())
# 10ms env per stem per second window of 1s for dropouts
for n in ['vocals','drums','bass','other']:
    x,_=librosa.load(S+n+'.wav',sr=22050,mono=True,offset=t0-5,duration=t1-t0+10)
    h=int(.01*22050); e=np.sqrt(np.convolve(x**2,np.ones(h)/h,'same'))[::h]; T=np.arange(len(e))*.01+t0-5
    out=[]
    for a_,b_ in [(55,60),(60,65),(65,70),(70,71.5),(71.5,73),(73,75),(75,77),(77,80),(80,84)]:
        s=e[(T>=a_)&(T<b_)]; out.append((a_,round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1)))
    print(n,out)
# vocal fine gaps
x,_=librosa.load(S+'vocals.wav',sr=22050,mono=True,offset=t0,duration=20); h=int(.05*22050)
e=20*np.log10(np.sqrt(np.convolve(x**2,np.ones(h)/h,'same'))[::h]+1e-9)
print('vocal 50ms dB', [(round(i*.05+60,2),round(v,0)) for i,v in enumerate(e) if v<-45])
