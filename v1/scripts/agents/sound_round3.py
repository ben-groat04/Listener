import numpy as np, soundfile as sf, scipy.signal as ss
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
S={n:sf.read(D+n+'.wav')[0] for n in ['other','bass','drums','vocals']}
sr=44100
def seg(n,a,b): return S[n][int(a*sr):int(b*sr)]
def spec(x):
    m=x.mean(1); w=np.hanning(len(m)); N=1<<18
    f,P=ss.welch(m,sr,nperseg=16384); return f,P
def db(x): return 10*np.log10(x+1e-20)
# 1 side/mid
print('MID/SIDE dB (side relative to mid) per stem')
for n in ['bass','other']:
  for a,b in [(90,99),(100+1,110),(170,180),(2*60+19,2*60+37)]:
    x=seg(n,a,b);M=(x[:,0]+x[:,1])/2;Sd=(x[:,0]-x[:,1])/2
    print(n,a,b,'mid %.1f side %.1f diff %.1f'%(db(np.mean(M**2)),db(np.mean(Sd**2)),db(np.mean(Sd**2))-db(np.mean(M**2))))
# 2 drums click/centroid
def cent(x,lo,hi):
    f,P=spec(x);k=(f>=lo)&(f<hi);return (f[k]*P[k]).sum()/P[k].sum(), db(P[k].sum())
print('drum bands (centroid 2-12k, level 2-12k, level<150)')
for a,b in [(5,30),(34,60),(100,115),(125,140),(150,167),(170,186)]:
    x=seg('drums',a,b);print(a,b,'%.0f Hz %.1f dB | low %.1f'%(*cent(x,2000,12000),cent(x,30,150)[1]))
# 3 vocals/other at 2:44-2:48 vs 0:20-0:26
print('voice bands & other masking')
bands=[(100,500),(500,2000),(2000,5000),(5000,8000)]
for lab,a,b in [('0:20-26',20,26),('2:15-21',135,141),('2:44-47.5',164,167.5)]:
    for n in ['vocals','other']:
        f,P=spec(seg(n,a,b));print(lab,n,[round(db(P[(f>=l)&(f<h)].sum()),1) for l,h in bands])
# 4 C played vs intermod: peak frequencies in other stem
def peak(n,a,b,lo,hi):
    f,P=spec(seg(n,a,b));k=(f>=lo)&(f<hi);i=np.argmax(P[k]);return f[k][i],db(P[k][i])
print('peaks other (Hz,dB) region C4(261.6)/7th partial(256.9), C3(130.8)/(128.4), D3 146.8, A3 220')
for lab,a,b in [('thin 2:00-2:13',120,133),('dense 1:30-1:40',90,100),('final 2:50-3:05',170,185),('0:40-0:55',40,55)]:
    r=[peak('other',a,b,lo,hi) for lo,hi in [(120,138),(140,153),(215,230),(245,275)]]
    print(lab,[('%.1f'%p,'%.0f'%l) for p,l in r])
