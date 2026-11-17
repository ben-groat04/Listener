import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/stems_raw/htdemucs/song/'
sr=22050
d,_=librosa.load(D+'drums.wav',sr=sr,mono=True)
b,_=librosa.load(D+'bass.wav',sr=sr,mono=True)
# kick-band onset envelope
sos=ss.butter(4,[35,130],'bandpass',fs=sr,output='sos')
k=ss.sosfilt(sos,d); hop=221 # 10ms
env=np.sqrt(np.convolve(k**2,np.ones(hop)/hop,'same'))[::hop]
t=np.arange(len(env))*0.01
on=np.maximum(np.diff(librosa.amplitude_to_db(env+1e-6)),0)
pk,_=ss.find_peaks(on,height=np.percentile(on,92),distance=8)
kt=t[pk+1]; kt=kt[(kt>30)&(kt<215)]
print('kicks',len(kt))
def R(per,x):
    ph=2*np.pi*(x%per)/per; return abs(np.exp(1j*ph).mean())
for name,div in [('bar',1),('4bar',4)]:
    ps=np.arange(2.48,2.62,0.0005)*div
    r=np.array([R(p,kt) for p in ps])
    i=r.argmax(); print(name,'best period',ps[i]/div,'BPM',240/(ps[i]/div),'R',r[i],'R@2.554',R(2.554*div,kt),'R@2.540',R(2.540*div,kt),'R@2.510',R(2.51*div,kt))
    top=ps[np.argsort(-r)[:5]]/div; print(' top',top)
# 16th-grid scan (beat/4) with kick onset
ps=np.arange(0.155,0.165,0.00005); r=np.array([R(p,kt) for p in ps]); print('16th best',ps[r.argmax()],60/(ps[r.argmax()]*4),r.max())
# hook-to-hook drum-env cross-correlation: hook1 vs hook4 (183 s gap) with stretch
de=librosa.feature.rms(y=d,frame_length=441,hop_length=221)[0]
def seg(a,s,n): return de[int(a*100):int((a+n)*100)]
def xc(a,b_,n=19.5):
    x=seg(a,0,n);y=seg(b_,0,n)
    x=x-x.mean();y=y-y.mean();return x,y
x,y=xc(10.4,193.1)
# search time-scale alpha and shift: y(t)=x(alpha t + s)
best=None
from scipy.interpolate import interp1d
f=interp1d(np.arange(len(de))*0.01,de,fill_value=0,bounds_error=False)
tt=np.arange(0,19.0,0.01)
for al in np.arange(0.9990,1.0010,0.00005):
  for s in np.arange(-0.4,0.4,0.01):
    # hook4 times 193.1+tt  vs hook1 times 10.4+ (tt*al)... 
    a=f(193.1+s+tt); c=f(10.4+tt*al)
    if True:
      cc=np.corrcoef(a,c)[0,1]
      if best is None or cc>best[0]: best=(cc,al,s)
print('hook1 vs hook4 env best',best)
# BPM implied: ratio of periods
# kick IOI across mutes
for T in (10.62,177.54):
    w=kt[(kt>T-3)&(kt<T+3)]; print('kicks near',T,np.round(w,3),np.round(np.diff(w),3))
# phase continuity: fit 0.1596 grid using kicks 4s before and 4s after, compare
for T in (10.62,177.54):
    for P in (60/94.0/4,60/94.5/4):
        for lo,hi in ((T-5,T-0.1),(T+0.3,T+5)):
            w=kt[(kt>lo)&(kt<hi)]
            z=np.exp(2j*np.pi*(w%P)/P).mean(); print(T,round(P,4),lo,'phase ms',round(np.angle(z)/(2*np.pi)*P*1000,1),'R',round(abs(z),2),len(w))
# hook starts: kick phase over first 8 bars of each hook vs bar period
hs=[10.4,71.3,132.0,193.1]
print('per-hook kick phase (bar 2.554 and 2.540), first 18 s:')
for P in (2.554,2.540):
    out=[]
    for h in hs:
        w=kt[(kt>=h)&(kt<h+18)] if h>30 else None
        if w is None or len(w)<5:
            w=np.array([x for x in on]) if False else np.array([])
        if len(w)>5:
            z=np.exp(2j*np.pi*(w%P)/P).mean(); out.append((h,round(np.angle(z)/(2*np.pi)*P,3),round(abs(z),2)))
    print(P,out)
