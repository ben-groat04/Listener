import numpy as np, soundfile as sf, json
d='/home/user/Listener/v1/data/t_dl_mirror/'
x,sr=sf.read(d+'audio/song.wav'); print(x.shape,sr,len(x)/sr)
m=x if x.ndim==1 else x.mean(1)
if x.ndim>1: print('mono diff max',np.abs(x[:,0]-x[:,1]).max())
print('peak',np.abs(x).max(),'>=.999',(np.abs(x)>=.999).sum(),'==1',(np.abs(x)>=1.0).sum())
print('rms',20*np.log10(np.sqrt((m**2).mean())))
h=int(.01*sr)
def env(a): n=len(a)//h; return 20*np.log10(np.sqrt((a[:n*h].reshape(n,h)**2).mean(1))+1e-10)
e=env(m); t=np.arange(len(e))*.01
for tt in [236.4,236.5,236.55,236.6,236.7,236.8,237]:
  print(tt,e[int(tt*100)])
nz=np.where(np.abs(m)>0)[0]; print('last nonzero',nz[-1]/sr)
last=np.where(e>-90)[0][-1]*.01; print('last>-90',last)
from scipy.signal import find_peaks
s=e[-300:]; p,_=find_peaks(s,prominence=3); print('peaks last3s',p, )
# stems
for st in ['vocals','drums','bass','other']:
  y,_=sf.read(d+f'stems_raw/htdemucs/song/{st}.wav'); y=y.mean(1) if y.ndim>1 else y
  ee=env(y); 
  def lv(a,b): return ee[int(a*100):int(b*100)].mean()
  print(st,'end max',ee[-300:].max(), 'last>-70',np.where(ee>-70)[0][-1]*.01)
  for name,b in [('0:10.4',10.4),('1:11.3',71.3),('2:12',132),('3:13.1',193.1),('3:35.3',215.3),('3:49',229),('3:54.5',234.5),('3:34',214)]:
    print(' ',name,round(lv(b-1.5,b),1),round(lv(b,b+1.5),1))
# mix
for name,b in [('0:10.4',10.4),('1:11.3',71.3),('2:12',132),('3:13.1',193.1),('3:34',214),('3:49',229),('3:54.5',234.5)]:
  print('mix',name,round(e[int((b-1.5)*100):int(b*100)].mean(),1),round(e[int(b*100):int((b+1.5)*100)].mean(),1))
# spectrum 8k
import scipy.signal as ss
f,P=ss.welch(m,sr,nperseg=8192); P=10*np.log10(P+1e-20)
for fr in [7000,7900,8000,8100,8500,10000]: print(fr,P[np.argmin(abs(f-fr))])
