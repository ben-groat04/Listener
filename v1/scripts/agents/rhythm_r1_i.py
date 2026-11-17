import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
dr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)[0]
b,a=ss.butter(4,[35/(sr/2),130/(sr/2)],'band'); lo=ss.filtfilt(b,a,dr)
hop=110  # 5 ms
env=np.sqrt(np.convolve(lo**2,np.ones(hop*2)/(hop*2),'same'))[::hop]; fr=sr/hop
db=20*np.log10(env+1e-9)
t=np.arange(len(env))/fr
# onset = rise: peaks in positive derivative of smoothed env
d=np.diff(env,prepend=env[0]); d=ss.savgol_filter(d,5,2)
pk,_=ss.find_peaks(d,height=np.percentile(d[(t>30)&(t<215)],93),distance=int(0.08*fr))
pk=pk[(t[pk]>30)&(t[pk]<215)]
tk=t[pk]
print('n kick-band onsets',len(tk),'per s',len(tk)/185)
ioi=np.diff(tk)
for step,name in ((0.6385/4,'16th@94.0'),(0.627/4,'16th@95.7 (tracker)')):
    u=ioi/step; dev=(u-np.round(u))*step*1000
    m=(ioi>0.12)
    print(name,'IOI dev from integer multiples: std %.1f ms (random uniform expectation %.1f ms)'%(dev[m].std(),step*1000/np.sqrt(12)))
h,_=np.histogram(ioi,bins=np.arange(0.08,1.4,0.04)); print('IOI hist (0.04 s bins from 0.08):',h.tolist())
# strong kicks only: top 40% by height
hh=d[pk]; strong=tk[hh>np.percentile(hh,60)]
io=np.diff(strong); print('strong kicks n',len(strong)); 
h,_=np.histogram(io,bins=np.arange(0.1,2.6,0.1)); print('strong IOI hist 0.1 bins from 0.1:',h.tolist())
# IOI in beats: share within 25 ms of {0.5,1,1.5,2,3,4}*0.6385
for x in (0.25,0.5,0.75,1,1.5,2,2.5,3,4):
    print('IOI share within 20 ms of %.2f beat (%.3f s): %.2f'%(x,x*0.6385,np.mean(abs(io-x*0.6385)<0.02)))
np.save('/tmp/kicks.npy',tk)
