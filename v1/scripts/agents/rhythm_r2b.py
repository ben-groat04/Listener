import numpy as np, librosa, json
exec(open('rhythm_r2.py').read().split('# fit grid')[0])
P=0.1923; ph=0.16
# drift: refit phase per 30s block
for a in range(0,180,30):
    sc=[];phs=np.arange(0,P,0.004)
    for p in phs:
        k=np.arange(p+ (a//P+1)*P*0,a+30,P); k=k[k>=a]
        idx=(k*fr).astype(int);idx=idx[idx<len(ob:=ok+om+oh)]
        sc.append(sum(ob[max(i-1,0):i+2].max() for i in idx))
    # phase relative to global grid at block start
    print(a, 'best phase mod P', round(phs[int(np.argmax(sc))],3))
# slot index of every onset
def prof(o,t0,t1,mod):
    pr=np.zeros(mod);n=np.zeros(mod)
    k=np.arange(0,int((t1-t0)/P))
    for j in k:
        tt=ph+ (int(t0/P)+j)*P
        if tt<t0 or tt>=t1: continue
        i=int(tt*fr)
        v=o[max(i-1,0):i+2].max()
        s=(int(round((tt-ph)/P)))%mod
        pr[s]+=v;n[s]+=1
    return pr/np.maximum(n,1)
np.set_printoptions(precision=2,suppress=True,linewidth=200)
for name,o in [('kick',ok),('mid',om),('hat',oh)]:
    for (a,b) in [(3,33),(33,65),(65,100),(100,115),(115,160),(170,186)]:
        p=prof(o,a,b,16); print(name,a,b,(p/p.max()))
