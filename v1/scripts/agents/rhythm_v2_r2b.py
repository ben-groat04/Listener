import numpy as np, librosa
from scipy.signal import butter, sosfiltfilt
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050; hop=64; fps=sr/hop
def load(n): return librosa.load(D+n+'.wav',sr=sr)[0]
dr=load('drums'); vo=load('vocals')
def band(y,lo,hi): return sosfiltfilt(butter(4,[lo,hi],'band',fs=sr,output='sos'),y)
oe=lambda y: librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
K=oe(band(dr,30,150)); S=oe(band(dr,150,2000)); H=oe(band(dr,5000,10000)); V=oe(vo)
t=np.arange(len(K))/fps
def coh(o,a,b,P):
    m=(t>=a)&(t<b); z=(o[m]*np.exp(2j*np.pi*t[m]/P)).sum(); return abs(z)/o[m].sum(), (np.angle(z)/(2*np.pi)*P)%P
print('fine period scan (kick+snare) coherence at P in 0.495..0.505')
for a,b in [(30,60),(90,150),(150,290)]:
    best=max(((coh(K+S,a,b,P)[0],P) for P in np.arange(0.490,0.510,0.0005)))
    print(a,b,'best P',round(best[1],4),'coh',round(best[0],3),'-> BPM',round(60/best[1],2))
print('phase of 0.5s grid (absolute t, kick/snare/hat) per 10 s')
for a in range(28,110,10):
    print(a,[ (round(coh(o,a,a+10,0.5)[1],3),round(coh(o,a,a+10,0.5)[0],2)) for o in (K,S,H)])
# hat delay-copy test, 100-200s
th=np.percentile(H[(t>100)&(t<200)],97)
ix=[i for i in range(2,len(H)-2) if t[i]>100 and t[i]<200 and H[i]>th and H[i]==H[i-2:i+3].max()]
def at(i,lag): j=i+int(round(lag*fps)); return H[j-1:j+2].max()
print('strong hat events',len(ix))
for lag in [0.125,0.25,0.375,0.5,0.75,1.125]:
    print('lag',lag,'mean hat env / event env',round(np.mean([at(i,lag)/H[i] for i in ix]),2))
# vocal onsets 3:28-5:05
ons=librosa.onset.onset_detect(onset_envelope=V,sr=sr,hop_length=hop,units='time',delta=0.15)
for a,b in [(208,230),(286,300)]:
    s=[round(float(o),2) for o in ons if a<=o<b]; print(a,b,s)
    print(' mod 0.5 phase',[round(((o)%0.5),2) for o in s])
