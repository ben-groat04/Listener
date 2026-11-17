import numpy as np, soundfile as sf
from scipy.signal import find_peaks
D='/home/user/Listener/v1/data/t_cshells_cshore/'
def env(p):
    x,sr=sf.read(p);x=x.mean(1) if x.ndim>1 else x
    h=int(.01*sr);n=len(x)//h;e=20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-12);return e,x,sr
for nm,p in [('mix',D+'audio/song.wav')]+[(s,D+f'stems_raw/htdemucs/song/{s}.wav') for s in ['vocals','drums','bass','other']]:
    e,x,sr=env(p);t=np.arange(len(e))*.01
    nz=np.where(np.abs(x)>1e-4)[0];last=nz[-1]/sr
    print(nm,'last sample >-80dBFS at',round(last,2),'peak',round(20*np.log10(np.abs(x[-3*sr:]).max()+1e-12),1),'dB in last 3 s; last-3s env max',round(e[-300:].max(),1),'; env 342.0-342.9 max',round(e[(t>=342)&(t<342.9)].max(),1))
    if nm=='mix':
        m=(t>=341.5)&(t<343);pk,_=find_peaks(e[m],prominence=4);print(' mix env peaks 341.5-343',[(round(t[m][i],2),round(e[m][i],1)) for i in pk]);print(' env 342.5..342.9',np.round(e[(t>=342.5)&(t<=342.95)],0))
