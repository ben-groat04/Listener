import numpy as np, soundfile as sf, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
def env(p,hop=0.01):
    x,sr=sf.read(p); x=x.mean(1) if x.ndim>1 else x; n=int(sr*hop); k=len(x)//n
    return 20*np.log10(np.sqrt((x[:k*n].reshape(k,n)**2).mean(1))+1e-12)
b=env(D+'stems_raw/htdemucs/song/bass.wav'); dr=env(D+'stems_raw/htdemucs/song/drums.wav')
t=np.arange(len(b))*0.01
on=b>-40
# runs
runs=[];i=0
while i<len(on):
    if on[i]:
        j=i
        while j<len(on) and (on[j] or (on[j:j+15].any())): j+=1
        runs.append((t[i],t[min(j,len(t)-1)])); i=j
    else: i+=1
runs=[r for r in runs if r[1]-r[0]>0.25]
print('bass-on runs >0.25 s:',len(runs))
# summarise: bass-on seconds per 10 s block and fraction
for s in range(0,240,20):
    m=(t>=s)&(t<s+20); print('%d:%02d bass on %.0f%%  drums med %.1f dB'%(s//60,s%60,100*on[m].mean(),np.median(dr[m])),end=' | ')
print()
# bass onsets vs kick groups
tk=np.load('/tmp/kicks.npy'); g=[tk[0]]
for x in tk[1:]:
    if x-g[-1]>0.15: g.append(x)
g=np.array(g)
d=np.diff(b,prepend=b[0]); pk,_=ss.find_peaks(d,height=12,distance=8); bo=t[pk]; bo=bo[(bo>30)&(bo<215)]
dist=np.array([np.min(abs(g-x)) for x in bo])
print('bass onsets',len(bo),'within 40 ms of kick onset %.2f ; within 80 ms %.2f'%(np.mean(dist<0.04),np.mean(dist<0.08)))
# chance: random times
rng=np.random.default_rng(0); r=rng.uniform(30,215,2000); dd=np.array([np.min(abs(g-x)) for x in r]); print('chance within 40 ms %.2f, within 80 ms %.2f'%(np.mean(dd<0.04),np.mean(dd<0.08)))
# gating on bar grid: bass on-off transition times vs 4-bar loop 10.2 s
tr=[]
for a,c in runs: tr.append(a)
tr=np.array(tr); print('run starts (s):',np.round(tr,1).tolist()[:70])
# drums last 3 s
seg=dr[int(233.4*100):int(236.5*100)]; pk,_=ss.find_peaks(seg,prominence=5); print('drum 10ms peaks 3:53.4-3:56.5:',len(pk),[round(233.4+i*0.01,2) for i in pk])
print('drum stem env at 233.4..236.5 every 0.5 s',[round(dr[int(x*100)],1) for x in np.arange(233.4,236.6,0.5)])
