import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
tk=np.load('/tmp/kicks.npy')
# collapse pairs <0.15 s
g=[tk[0]]
for x in tk[1:]:
    if x-g[-1]>0.15: g.append(x)
g=np.array(g); ioi=np.diff(g)
print('collapsed kick groups',len(g),'per bar',len(g)/(185/2.554))
st=0.6385/4
u=ioi/st; 
h=np.round(u).astype(int); 
from collections import Counter
c=Counter(h); print('IOI in 16th steps (94.0 BPM) counts:',sorted(c.items()))
dev=(u-np.round(u))*st*1000
print('dev from integer 16th multiples: std %.1f ms, mean abs %.1f ms (random %.1f ms std)'%(dev.std(),abs(dev).mean(),st*1000/np.sqrt(12)))
# cumulated-grid test: assign each kick to grid positions via cumulative sum of rounded steps; compute residual drift
pos=np.concatenate([[0],np.cumsum(h)])*st
res=g-g[0]-pos
print('cumulative residual std ms (allowing drift)',res.std()*1000)
# same for 95.7 tracker 16th
st2=0.627/4; u2=ioi/st2; dev2=(u2-np.round(u2))*st2*1000
print('on tracker 95.7 16th: std %.1f ms (random %.1f)'%(dev2.std(),st2*1000/np.sqrt(12)))
# a cleaner test of tempo: fit best step s minimizing circular spread of IOIs
best=[]
for bpm in np.arange(90,98,0.1):
    s=60/bpm/4; u=ioi/s; d=np.exp(2j*np.pi*u); best.append((abs(d.mean()),bpm))
print('IOI-coherence best bpm:',max(best), 'at 95.7:',[b for b in best if abs(b[1]-95.7)<0.06][0],'at 94.0:',[b for b in best if abs(b[1]-94.0)<0.06][0])
# snare/crack
dr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)[0]
b,a=ss.butter(4,[1500/(sr/2),5000/(sr/2)],'band'); hi=ss.filtfilt(b,a,dr)
hop=110; env=np.sqrt(np.convolve(hi**2,np.ones(2*hop)/(2*hop),'same'))[::hop]; fr=sr/hop; t=np.arange(len(env))/fr
d=ss.savgol_filter(np.diff(env,prepend=env[0]),5,2)
pk,_=ss.find_peaks(d,height=np.percentile(d[(t>30)&(t<215)],85),distance=int(0.08*fr)); pk=pk[(t[pk]>30)&(t[pk]<215)]
ts=t[pk]; io=np.diff(ts); u=io/st; dv=(u-np.round(u))*st*1000
print('crack-band onsets',len(ts),'per s',len(ts)/185,'dev std %.1f ms'%dv.std())
c=Counter(np.round(u).astype(int)); print('crack IOI steps',sorted(c.items())[:14])
