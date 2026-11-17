# hard mutes in the body of the mix: 10 ms envelope below -40 dBFS between 0:05 and 3:48
import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/'
x,sr=sf.read(D+'audio/song.wav',dtype='float32'); m=x.mean(1)
n=int(sr*0.01); e=20*np.log10(np.sqrt((m[:len(m)//n*n].reshape(-1,n)**2).mean(1))+1e-12)
t=np.arange(len(e))*0.01
sel=(t>5)&(t<228)
idx=np.where(sel&(e<-40))[0]
groups=[]
for i in idx:
    if groups and i-groups[-1][-1]<=3: groups[-1].append(i)
    else: groups.append([i])
print('clusters of 10ms frames < -40 dBFS in 0:05-3:48:',len(groups))
for g in groups: print('%.2f-%.2f s (%d ms) min %.0f dB'%(t[g[0]],t[g[-1]]+0.01,len(g)*10,e[g].min()))
print('frames < -30 dBFS (count):',(sel&(e<-30)).sum())
# 10-s block median 10 ms env, for loudness curve statements
print('10ms-env median 0:10-3:30 %.1f, p5 %.1f, p95 %.1f'%(np.median(e[(t>10)&(t<210)]),*np.percentile(e[(t>10)&(t<210)],[5,95])))
