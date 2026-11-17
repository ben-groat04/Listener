# above-wall energy by STFT (sharp), vs clipped samples; 2:57.4 event stems; vocal crest hook vs verse
import numpy as np, soundfile as sf, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'; S=D+'stems_raw/htdemucs/song/'
def ld(p):
    x,sr=sf.read(p,dtype='float32'); return (x.mean(1) if x.ndim>1 else x),sr
db=lambda v:20*np.log10(v+1e-12)
mix,sr=ld(D+'audio/song.wav')
f,t,Z=ss.stft(mix,sr,nperseg=2048,noverlap=1024)
P=np.abs(Z)**2
hi=P[f>9500].sum(0); lo=P[(f>100)&(f<8000)].sum(0); band=P[(f>8100)&(f<9500)].sum(0)
ratio=10*np.log10(hi/lo+1e-20)
sec=np.floor(t).astype(int)
cl=np.array([(np.abs(mix[i*sr:(i+1)*sr])>=0.999).sum() for i in range(239)])
r=np.array([ratio[sec==i].mean() for i in range(239)])
print('9.5k+/(0.1-8k) power ratio dB per second: median %.1f p10 %.1f p90 %.1f'%(np.median(r[:236]),*np.percentile(r[:236],[10,90])))
print('seconds with 0 clipped samples: median %.1f ; >50 clipped: median %.1f ; >1000 clipped: %.1f'%(np.median(r[:236][cl[:236]==0]),np.median(r[:236][cl[:236]>50]),np.median(r[:236][cl[:236]>1000])))
print('frame-level 9.5k+ vs 100-8k: absolute dB of hi (re 1) median %.1f'%(10*np.log10(np.median(hi))))
# if the floor is an independent noise, ratio should be larger in quiet frames
q=np.argsort(lo)[:200]; print('quietest 200 frames (excl digital zero) ratio:',np.median(ratio[[i for i in q if lo[i]>1e-12]]))
# 2:57.4 event
for name,fn in [('mix',None),('drums','drums'),('bass','bass'),('vocals','vocals'),('other','other')]:
    x=mix if fn is None else ld(S+fn+'.wav')[0]
    a=int(177.2*sr);b=int(177.7*sr); seg=x[a:b]
    n=int(0.01*sr); e=np.sqrt((seg[:len(seg)//n*n].reshape(-1,n)**2).mean(1))
    print(name,'10ms env dB 177.2-177.7:',' '.join('%.0f'%v for v in db(e)),'| peak %.2f'%np.abs(seg).max())
# clipped run: spectrum of the stems in the 73 ms run vs 100 ms before
a=int(177.38*sr)
idx=np.where(np.abs(mix[a-2000:a+8000])>=0.999)[0]
print('clipped idx range in 177.34-177.6:', (idx.min()+a-2000)/sr if len(idx) else None, (idx.max()+a-2000)/sr if len(idx) else None, len(idx))
for fn in ['drums','bass','vocals','other']:
    x=ld(S+fn+'.wav')[0]; s=x[a-4000:a+6000]
    print(fn,'peak in event %.2f  band rms dB: <150Hz %.1f, 150-1k %.1f, 1k-8k %.1f'%(np.abs(s).max(),*[db(np.sqrt((ss.sosfilt(ss.butter(4,bd,'band',fs=sr,output='sos'),s)**2).mean())) for bd in [[30,150],[150,1000],[1000,7800]]]))
# vocal crest factor and band tilt hook vs verse
vo,_=ld(S+'vocals.wav')
def crest(a,b):
    s=vo[int(a*sr):int(b*sr)]; n=int(0.05*sr); e=np.sqrt((s[:len(s)//n*n].reshape(-1,n)**2).mean(1)); act=e>10**(-35/20)
    rms=np.sqrt((s**2).mean()); return db(np.abs(s).max()/rms), np.percentile(db(e[act]),[10,90]), act.mean()
for nm,(a,b) in {'verse1 0:34-1:10':(34,70),'hook1 0:12-0:30':(12,30),'verse2 1:35-2:10':(95,130),'hook2 2:15-2:32':(135,152),'hook3 3:16-3:34':(196,214)}.items():
    c,p,ac=crest(a,b); print(nm,'crest %.1f dB, 50ms-active level p10 %.1f p90 %.1f (spread %.1f dB), active frac %.2f'%(c,p[0],p[1],p[1]-p[0],ac))
