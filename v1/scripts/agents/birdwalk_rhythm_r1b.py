import numpy as np, json, librosa, soundfile as sf
D='/home/user/Listener/v1/data/t_birdwalk/'
on=np.load('/tmp/claude-0/drum_on.npy'); bon=np.load('/tmp/claude-0/bass_on.npy'); kon=np.load('/tmp/claude-0/kick_on.npy')
bt=np.array(json.load(open(D+'audio_features/beat_times.json')))
if bt.ndim>1: bt=bt[:,0]
ib=np.diff(bt)
print('tracker beat IOI median per 20s:')
for a in range(0,188,20):
    m=(bt[:-1]>=a)&(bt[:-1]<a+20); print(a, round(60/np.median(ib[m]),1) if m.any() else None, 'sd',round(ib[m].std(),3))
# snap hit period in sparse sections (drums-only hits ~1.5s)
def hits(a,b,minioi=1.0):
    o=on[(on>=a)&(on<b)]; return o
for a,b in[(0,12),(47,59.4),(120,131.4),(24.5,47)]:
    o=hits(a,b); i=np.diff(o); 
    print(a,b,'hits',o.round(2)[:30]); print(' IOI',i.round(2)[:30])
# fit linear period
for a,b in[(0.5,11),(47.5,59),(120.5,131)]:
    o=hits(a,b); o=o[np.r_[True,np.diff(o)>1.0]]
    k=np.arange(len(o)); p=np.polyfit(k,o,1); res=o-np.polyval(p,k)
    print('fit',a,b,'period',p[0].round(4),'BPM(bar=4 beats)',round(4*60/p[0],2),'resid sd ms',round(res.std()*1000,1),'n',len(o))
# grid fit of kick/bass onsets: best period and phase over groove sections, circular stat
def circ(o,P):
    ph=(o%P)/P*2*np.pi; R=abs(np.exp(1j*ph).mean()); return R
for name,x in[('bass',bon),('kick-band',kon),('drums all',on)]:
    for a,b in[(12.1,47),(59.4,120),(131.4,143),(156.4,188)]:
        o=x[(x>=a)&(x<b)]
        Ps=np.arange(0.18,0.45,0.0005); R=[circ(o,P) for P in Ps]
        j=int(np.argmax(R)); 
        print(name,a,b,'n',len(o),'best P',Ps[j].round(4),'R',round(R[j],2),'R@0.395',round(circ(o,0.3947),2),'R@0.1974',round(circ(o,0.1974),2))
# IOI histogram for bass in groove in units of 0.1974 (16th at 152)
for a,b in[(12.1,47),(59.4,120),(131.4,143),(156.4,188)]:
    o=bon[(bon>=a)&(bon<b)]; i=np.diff(o)/0.1974
    h=np.histogram(i,bins=np.arange(0.5,10.5,1))[0]; print('bass IOI in 16ths',a,b,h)
    o=kon[(kon>=a)&(kon<b)]; i=np.diff(o)/0.1974
    h=np.histogram(i,bins=np.arange(0.5,10.5,1))[0]; print('kickband IOI in 16ths',a,b,h)
# beat-tracker vs kick offset
for a,b in[(12.1,47),(59.4,120),(156.4,188)]:
    o=kon[(kon>=a)&(kon<b)]; off=[ (x-bt[np.argmin(abs(bt-x))]) for x in o]; off=np.array(off)
    print('kick-band offset vs tracker beats',a,b,'median ms',round(np.median(off)*1000),'MAD ms',round(np.median(abs(off-np.median(off)))*1000),'sd',round(off.std()*1000))
