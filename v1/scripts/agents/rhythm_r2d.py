import numpy as np, librosa
exec(open('rhythm_r2.py').read().split('# fit grid')[0])
P=0.1923; ph=0.16
np.set_printoptions(precision=2,suppress=True,linewidth=220)
def prof(o,t0,t1,mod):
    pr=np.zeros(mod);n=np.zeros(mod)
    j0=int(np.ceil((t0-ph)/P)); j1=int((t1-ph)/P)
    for j in range(j0,j1):
        tt=ph+j*P; i=int(tt*fr)
        pr[j%mod]+=o[max(i-1,0):i+2].max(); n[j%mod]+=1
    return pr/np.maximum(n,1)
for name,o in [('kick',ok),('mid',om),('hat',oh)]:
    p=prof(o,121,158,32); print(name,'32-slot 2:01-2:38\n',(p/p.max()).reshape(2,16))
    p=prof(o,3,165,32); print(name,'32-slot whole\n',(p/p.max()).reshape(2,16))
# sub hit fine onset: bass stem envelope at 5ms
b=np.abs(bs); 
import scipy.signal as ss
env=ss.sosfilt(ss.butter(2,30,'low',fs=sr,output='sos'),b)
for h in [121.086,127.24,133.393]:
    seg=env[int((h-0.4)*sr):int((h+0.3)*sr)]; tt=np.arange(len(seg))/sr+h-0.4
    mx=seg.max(); 
    print('sub',h,'t at 10%/50%/90% of max',[round(tt[np.argmax(seg>=f*mx)],3) for f in (.1,.5,.9)])
