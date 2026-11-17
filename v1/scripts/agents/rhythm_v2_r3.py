import numpy as np, librosa
from scipy.signal import butter, sosfiltfilt
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050; hop=64; fps=sr/hop
L=lambda n: librosa.load(D+n+'.wav',sr=sr)[0]
dr,ba,vo=L('drums'),L('bass'),L('vocals')
band=lambda y,lo,hi: sosfiltfilt(butter(4,[lo,hi],'band',fs=sr,output='sos'),y)
oe=lambda y: librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
K=oe(band(dr,30,150)); S=oe(band(dr,150,2000)); B=oe(ba); V=oe(vo)
t=np.arange(len(K))/fps
np.set_printoptions(precision=2,suppress=True,linewidth=200)
def ph(o,a,b,p):
    m=(t>=a)&(t<b); z=(o[m]*np.exp(-2j*np.pi*t[m]/p)).sum(); return (np.angle(z)/(2*np.pi)*p)%p, abs(z)/o[m].sum()
print('phase of kick/snare on 0.5s grid (abs time) per window')
for a,b in [(30,50),(50,70),(88.6,110),(110,140),(140,200),(200,260),(260,288)]:
    print(a,b,'kick',[round(x,3) for x in ph(K,a,b,0.5)],'snare',[round(x,3) for x in ph(S,a,b,0.5)])
# 1:24-1:28.6 hole and 1:10-1:16.5: drum energy per 0.25s
print('kick env per 0.5 s 1:08-1:30'); 
for a in np.arange(68,90,0.5):
    m=(t>=a)&(t<a+.5); print(round(a,1),round(K[m].max(),1),round(S[m].max(),1),end=' | ')
print()
# 1 s fold of kick+snare on 2 s bar, post 1:28.6 relative to 88.61: which beat is snare-strong
for ref in (88.61,):
    for nm,o in (('kick',K),('snare',S)):
        m=(t>=100)&(t<288); p=((t[m]-ref)%2.0)/0.5; h=np.zeros(4); np.add.at(h,(p.astype(int))%4,o[m]); print(nm,'beat-fold from 88.61 (0.5 s bins)',h/h.sum())
# ending: onsets after 296
print('end events (kick, snare, all drums) 298-306')
for a in np.arange(298,306,0.125):
    m=(t>=a)&(t<a+.125); 
    if K[m].max()>3 or S[m].max()>3: print(round(a,3),round(K[m].max(),1),round(S[m].max(),1))
# bass onset times 200-300 using peak-picking on bass env
bo=librosa.onset.onset_detect(onset_envelope=B,sr=sr,hop_length=hop,units='time',delta=0.4)
print('bass onsets',[round(x,2) for x in bo if 100<x<300][:80])
bo=np.array([x for x in bo if 90<x<288])
print('bass onset mod 4 from 88.61',np.round((bo-88.61)%4,2)[:60])
print('bass onset mod 4 from 0.14 ',np.round((bo-0.14)%4,2)[:60])
# voice call phase vs kick/snare beat grid 286-299
vo_on=librosa.onset.onset_detect(onset_envelope=V,sr=sr,hop_length=hop,units='time',delta=0.3)
print('voice on 286-299 rel 88.61 mod2',[ (round(x,2),round((x-88.61)%2,2)) for x in vo_on if 286<x<299])
