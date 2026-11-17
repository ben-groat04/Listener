import librosa,numpy as np,scipy.signal as s
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050;hop=64;fr=sr/hop
def L(n):return librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
dr=L('drums');ot=L('other');ba=L('bass');vo=L('vocals')
def band(y,lo,hi):return s.sosfilt(s.butter(4,[lo,hi],'band',fs=sr,output='sos'),y)
def env(y):return librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
ek=env(band(dr,30,150))
# global grid: fit period/phase 1:44-5:00
a,b=int(104*fr),int(300*fr);t=np.arange(a,b)/fr
best=max(((abs((ek[a:b]*np.exp(2j*np.pi*t/P)).sum()),P) for P in np.arange(0.499,0.501,0.00005)))
P=best[1];z=(ek[a:b]*np.exp(2j*np.pi*t/P)).sum();ph=(np.angle(z)/(2*np.pi)*P)%P
print('period',P,'phase',ph)
# bar phase 2.0s: find which of 4 beats is downbeat by bass ostinato: bass onset env folded at 2s
eb=env(band(ba,30,200))
def fold(e,t0,t1,N=16,per=2.0*P/0.5):
    out=np.zeros(N);tt=np.arange(int(t0*fr),int(t1*fr))/fr
    for i,x in zip(tt,e[int(t0*fr):int(t1*fr)]):
        out[int(((i-ph)%per)/per*N)%N]+=x
    return out/out.sum()
print('kick fold 2s bar (16)',np.round(fold(ek,104,300),3))
print('bass fold',np.round(fold(eb,104,300),3))
# backbeat: snare 1.5-5k env value at beat positions, mean prominence by beat index mod 4
es=env(band(dr,1500,5000))
for (t0,t1) in [(104,200),(200,277),(280,288)]:
    tt=np.arange(t0,t1,0.5)+ (ph%0.5)
    # beat times
    bt=np.arange(ph+ (int((t0-ph)/P)+1)*P, t1, P)
    v=[es[int((x+0.02)*fr):int((x+0.12)*fr)].max() for x in bt]
    v=np.array(v)
    print('snare-band peak by beat idx mod4',t0,t1,[round(v[i::4].mean(),2) for i in range(4)])
# beat offset: downbeat index = beat where bass step0 lands. report phase of absolute times
def barpos(t):  # in beats since phase, mod 4
    return (((t-ph)/P)%4)
for t in [28.0,41.7,88.5,101.0,157.0,216.0,288.5,300.8,302.3,302.56,0,4,8,12,20]:
    print('t',t,'beatpos mod4 %.2f'%barpos(t))
# 'other' & drums & bass autocorr 0.375 vs 0.5 by region
for nm,y in [('other',ot),('drums',dr),('bass',ba),('vocals',vo)]:
    e=env(y)
    for (t0,t1) in [(28,40),(104,128),(160,200),(220,276),(290,300)]:
        x=e[int(t0*fr):int(t1*fr)];x=x-x.mean();ac=np.correlate(x,x,'full')[len(x)-1:];ac/=ac[0]
        lag=lambda sec:ac[int(round(sec*fr))-2:int(round(sec*fr))+3].max()
        print(nm,t0,t1,'ac .375=%.2f .5=%.2f .25=%.2f .125=%.2f 2.0=%.2f 1.5=%.2f'%(lag(.375),lag(.5),lag(.25),lag(.125),lag(2.0),lag(1.5)))
# voice bursts 4:38-5:00 against beat grid
ev=env(vo);pk=librosa.util.peak_pick(ev,pre_max=20,post_max=20,pre_avg=40,post_avg=40,delta=0.5*ev.max()*0.1,wait=30)
for p in pk:
    tt=p/fr
    if 270<tt<302: print('voice onset %.2f beatpos %.2f'%(tt,barpos(tt)))
