import numpy as np, librosa
from scipy.signal import butter, sosfiltfilt
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050; hop=64; fps=sr/hop
def load(n): return librosa.load(D+n+'.wav',sr=sr)[0]
dr=load('drums'); ba=load('bass'); vo=load('vocals')
def band(y,lo,hi):
    return sosfiltfilt(butter(4,[lo,hi],'band',fs=sr,output='sos'),y)
def oenv(y): 
    o=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop); return o
O={'kick':oenv(band(dr,30,150)),'snare':oenv(band(dr,150,2000)),'hat':oenv(band(dr,5000,10000)),'bass':oenv(ba),'voc':oenv(vo)}
T0=0.14
def fold(o,a,b,period=2.0,nb=16,ref=T0):
    t=np.arange(len(o))/fps; m=(t>=a)&(t<b)
    ph=((t[m]-ref)%period)/period; h=np.zeros(nb)
    idx=(ph*nb).astype(int)%nb
    np.add.at(h,idx,o[m]); return h/ h.sum()
np.set_printoptions(precision=2,suppress=True,linewidth=200)
for a,b in [(30,60),(88.6,140),(140,200),(200,288)]:
    print('== fold on 2s bar (16 semis) from',a,b)
    for k in ['kick','snare','hat','bass']:
        print(k,fold(O[k],a,b))
# per-beat (0.5s) fold in 8 bins for snare/kick alt beats
for a,b in [(30,60),(88.6,288)]:
    print('beat-level 4 beats/bar, bins=4 beats', a,b)
    for k in ['kick','snare','bass']:
        print(k,fold(O[k],a,b,nb=4))
# bass before/after 4:48
for a,b in [(200,288),(290,300)]:
    print('bass fold 1s',a,b,fold(O['bass'],a,b,period=1.0,nb=8))
# vocal onsets 4:46-4:59 relative to bar grid
ons=librosa.onset.onset_detect(onset_envelope=O['voc'],sr=sr,hop_length=hop,units='time',delta=0.3,backtrack=False)
sel=[o for o in ons if 286<=o<=299]
print('voc onsets',[(round(o,2),round(((o-T0)%2.0),2)) for o in sel])
# phase over time of kick on 0.5 grid & 2s grid
for a in range(30,300,20):
    for k in ['kick','bass']:
        o=O[k]; t=np.arange(len(o))/fps; m=(t>=a)&(t<a+20)
        z=(o[m]*np.exp(2j*np.pi*(t[m]-T0)/0.5)).sum(); z4=(o[m]*np.exp(2j*np.pi*(t[m]-T0)/2.0)).sum()
        print(a,k,'ph0.5',round((np.angle(z)/(2*np.pi)*0.5)%0.5,3),'ph2',round((np.angle(z4)/(2*np.pi)*2)%2,3),end=' | ')
    print()
# hat: mean hat envelope at lags after kick-heavy? lag test: cross-correlation hat vs kick
def xc(a,b,lo,hi):
    ta=np.arange(len(a))/fps; m=(ta>=lo)&(ta<hi); a=a[m]-a[m].mean(); b=b[m]-b[m].mean()
    c=np.correlate(a,b,'full')/ (np.std(a)*np.std(b)*len(a)); lags=(np.arange(-len(a)+1,len(a)))/fps
    return lags,c
l,c=xc(O['hat'],O['kick'],100,200); mm=(l>=0)&(l<=1.0)
pk=[(round(l[mm][i],3),round(c[mm][i],3)) for i in range(1,mm.sum()-1) if c[mm][i]>c[mm][i-1] and c[mm][i]>c[mm][i+1] and c[mm][i]>0.05]
print('hat-vs-kick xcorr peaks lag',pk)
