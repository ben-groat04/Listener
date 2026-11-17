# Sound specialist round 2, t_dl_mirror: kick double rise, 8 kHz edge, bed floor, 2:57.4 clip, vocal crest hook vs verse
import numpy as np, soundfile as sf, scipy.signal as ss, sys
D='/home/user/Listener/v1/data/t_dl_mirror/'
S=D+'stems_raw/htdemucs/song/'
def ld(p):
    x,sr=sf.read(p,dtype='float32'); return (x.mean(1) if x.ndim>1 else x),sr
def env(x,sr,ms=10):
    n=int(sr*ms/1000); m=len(x)//n
    return np.sqrt((x[:m*n].reshape(m,n)**2).mean(1)+1e-20)
db=lambda v:20*np.log10(v+1e-12)
mix,sr=ld(D+'audio/song.wav'); dr,_=ld(S+'drums.wav'); ba,_=ld(S+'bass.wav'); ot,_=ld(S+'other.wav'); vo,_=ld(S+'vocals.wav')
# 1 kick double rise: low band 30-150 Hz envelope (2 ms) around kick onsets in drums stem
sos=ss.butter(4,[35,130],'band',fs=sr,output='sos'); k=ss.sosfilt(sos,dr)
e=env(k,sr,2); t=np.arange(len(e))*0.002
from scipy.signal import find_peaks
sm=np.convolve(e,np.ones(3)/3,'same')
pk,_=find_peaks(db(sm),height=-35,distance=40,prominence=6)
pk=pk[(t[pk]>30)&(t[pk]<215)]
print('kick-band main peaks',len(pk))
# for each, look 40-220 ms later for a second local max and the dip between
gaps=[];dips=[];ratios=[]
for p in pk:
    seg=sm[p:p+120]  # 240 ms
    if len(seg)<120: continue
    q,_=find_peaks(seg,prominence=seg[0]*0.15)
    q=q[q>20]
    if len(q):
        j=q[0]; gaps.append(j*2); dips.append(db(seg[10:j].min()/seg[0])); ratios.append(db(seg[j]/seg[0]))
print('with second rise (>=40ms later):',len(gaps),'of',len(pk))
if gaps:
    g=np.array(gaps);print('gap ms median %.0f p10 %.0f p90 %.0f'%(np.median(g),*np.percentile(g,[10,90])))
    print('dip depth dB median %.1f ; second/first dB median %.1f'%(np.median(dips),np.median(ratios)))
# decay of single kicks: time for kick band to fall 20 dB from peak (smoothed)
dec=[]
for p in pk:
    seg=db(sm[p:p+150]/sm[p]); i=np.where(seg<-20)[0]
    dec.append(i[0]*2 if len(i) else 300)
print('kick-band fall-20dB ms median %.0f p10 %.0f p90 %.0f'%(np.median(dec),*np.percentile(dec,[10,90])))
# the same in full mix low band (is double rise present in mix?)
km=ss.sosfilt(sos,mix); em=np.convolve(env(km,sr,2),np.ones(3)/3,'same')
c=0;n=0
for p in pk[:200]:
    seg=em[p:p+120]; q,_=find_peaks(seg,prominence=seg[0]*0.15); n+=1; c+= (len(q[q>20])>0)
print('mix low band second rise fraction',c,'/',n)
# 2 the 8 kHz edge: Welch fine, in quiet-vs-loud segments; slope
f,P=ss.welch(mix,sr,nperseg=8192,noverlap=4096)
for fq in [7000,7500,7800,7900,8000,8050,8100,8200,8300,8500,9000,10000,15000,20000]:
    i=np.argmin(abs(f-fq)); print('welch %5d Hz %.1f dB'%(fq,10*np.log10(P[i]+1e-20)))
# floor above 9 kHz: noise-like? level of rms of highpassed 9-20k
hp=ss.sosfilt(ss.butter(8,9000,'high',fs=sr,output='sos'),mix)
print('9k+ rms dBFS: whole %.1f'%db(np.sqrt((hp**2).mean())))
eh=env(hp,sr,1000); print('9k+ per-second dB min %.1f max %.1f'%(db(eh.min()),db(eh.max())))
# correlation of 9k+ envelope with broadband env (images/leak -> correlated; dither -> not)
eb=env(mix,sr,1000); m=min(len(eb),len(eh)); print('corr 9k+ env vs mix env %.2f'%np.corrcoef(db(eh[:m]),db(eb[:m]))[0,1])
# last 4 s: digital zero region 3:57-3:59 noise? 
print('3:57-3:59 abs max',np.abs(mix[int(237*sr):int(239*sr)]).max())
# 3 quantisation: LSB use. count distinct sample values in a quiet segment (3:56-3:56.6)
x16,_=sf.read(D+'audio/song.wav',dtype='int16',start=int(236.0*sr),frames=int(0.7*sr))
print('int16 distinct values in 3:56.0-3:56.7 L:',len(np.unique(x16[:,0])),'max abs',np.abs(x16).max())
# bed floor in fade: other stem spectrum 3:53-3:56 tonal peakiness
seg=ot[int(233*sr):int(235.5*sr)]
f2,P2=ss.welch(seg,sr,nperseg=16384)
pk2,_=find_peaks(10*np.log10(P2+1e-20),prominence=10)
print('fade bed peaks Hz',[int(f2[i]) for i in pk2[:10]],'| level around 5-8k vs 100-1k dB',10*np.log10(P2[(f2>5000)&(f2<7500)].mean()+1e-20),10*np.log10(P2[(f2>100)&(f2<1000)].mean()+1e-20))
# bed fundamental fine
seg=ot[int(220*sr):int(228*sr)]
f3,P3=ss.welch(seg,sr,nperseg=1<<17)
band=(f3>140)&(f3<156); i=np.argmax(P3*band); 
# parabolic
y=np.log(P3[i-1:i+2]);d=0.5*(y[0]-y[2])/(y[0]-2*y[1]+y[2]); fb=f3[i]+d*(f3[1]-f3[0])
print('bed fund Hz %.2f -> cents vs D3(146.832): %.1f'%(fb,1200*np.log2(fb/146.832)))
for h in [2,4,8]:
    b=(f3>fb*h-4)&(f3<fb*h+4); j=np.argmax(P3*b); print(' partial',h,'at %.2f Hz -> f0 %.2f'%(f3[j],f3[j]/h))
