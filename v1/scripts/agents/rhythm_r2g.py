import numpy as np, librosa
exec(open('rhythm_r2.py').read().split('# fit grid')[0])
ob=ok+om+oh
def fit(a,b):
    best=None
    for P in np.arange(0.180,0.200,0.0002):
        for ph in np.arange(0,P,0.004):
            k=np.arange(ph,b,P); k=k[k>=a]; idx=(k*fr).astype(int)
            sc=sum(ob[max(i-1,0):i+2].max() for i in idx if i<len(ob))/len(idx)
            if best is None or sc>best[0]: best=(sc,P,ph,len(idx))
    return best
for a,b in [(5,35),(100,130),(135,165),(170,186)]:
    s,P,ph,n=fit(a,b); print(a,b,'P=%.4f beat=%.4f BPM(slot=8th)=%.1f phase=%.3f'%(P,4*P,60/(2*P),ph))
# onset rate per second in 170-186 vs 140-165
th=0.5*np.percentile(ob,95)
for a,b in [(140,165),(170,186)]:
    sel=(t>=a)&(t<b); pk=librosa.util.peak_pick(ob[sel],pre_max=3,post_max=3,pre_avg=5,post_avg=5,delta=0.05*ob.max(),wait=3)
    print(a,b,'onsets/s',len(pk)/(b-a))
