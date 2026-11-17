# kick double-rise redone with Hilbert envelope (the 2 ms RMS version in sound_r2_tdl.py ripples at 2x the 70 Hz period)
import numpy as np, soundfile as sf, scipy.signal as ss
from scipy.signal import find_peaks, hilbert
D='/home/user/Listener/v1/data/t_dl_mirror/'; S=D+'stems_raw/htdemucs/song/'
def ld(p):
    x,sr=sf.read(p,dtype='float32'); return (x.mean(1) if x.ndim>1 else x),sr
db=lambda v:20*np.log10(v+1e-12)
dr,sr=ld(S+'drums.wav'); mix,_=ld(D+'audio/song.wav')
def lowenv(x,lo,hi,cut=40):
    k=ss.sosfiltfilt(ss.butter(4,[lo,hi],'band',fs=sr,output='sos'),x)
    e=np.abs(hilbert(k)); e=np.maximum(ss.sosfiltfilt(ss.butter(2,cut,"low",fs=sr,output="sos"),e),1e-9)
    return e[::44]  # ~1 ms
for name,x in [('drums stem',dr),('mix',mix)]:
    e=lowenv(x,35,130); t=np.arange(len(e))*0.001
    sel=(t>30)&(t<215)
    pk,_=find_peaks(db(e),height=db(e[sel]).max()-30,distance=80,prominence=6)
    pk=pk[(t[pk]>30)&(t[pk]<215)]
    sec=0;gaps=[];dec=[];dipd=[]
    for p in pk:
        seg=e[p:p+250]
        if len(seg)<250: continue
        q,_=find_peaks(seg,prominence=seg[0]*0.2)
        q=q[q>30]
        if len(q): sec+=1;gaps.append(q[0]);dipd.append(db(seg[5:q[0]].min()/seg[0]))
        i=np.where(db(seg/seg[0])<-20)[0]; dec.append(i[0] if len(i) else 250)
    print(name,'kicks',len(pk),'second rise >=30ms, prominence 20%%:',sec)
    if gaps: print('  gap ms median %.0f p10 %.0f p90 %.0f ; dip dB median %.1f'%(np.median(gaps),*np.percentile(gaps,[10,90]),np.median(dipd)))
    print('  fall -20dB ms median %.0f p10 %.0f p90 %.0f'%(np.median(dec),*np.percentile(dec,[10,90])))
# dominant freq of kick body: spectrum of 100 ms after peak, median across kicks, 
e=lowenv(dr,35,130);t=np.arange(len(e))*0.001
pk,_=find_peaks(db(e),height=db(e[(t>30)&(t<215)]).max()-30,distance=80,prominence=6)
pk=pk[(t[pk]>30)&(t[pk]<215)]
fr=[]
for p in pk[:400]:
    a=int(t[p]*sr); s=dr[a:a+int(0.08*sr)]*np.hanning(int(0.08*sr)); F=np.abs(np.fft.rfft(s,16384)); f=np.fft.rfftfreq(16384,1/sr)
    m=(f>25)&(f<200); fr.append(f[m][np.argmax(F[m])])
print('kick body dominant Hz median %.0f p10 %.0f p90 %.0f'%(np.median(fr),*np.percentile(fr,[10,90])))
# 8k edge step centre, fine, median over time frames (Welch median)
f,P=ss.welch(mix,sr,nperseg=16384,noverlap=8192,average='median')
for fq in range(7900,8301,25):
    i=np.argmin(abs(f-fq)); print(fq,'%.1f'%(10*np.log10(P[i]+1e-20)),end=' | ')
print()
# 9k+ band per-second: relation to clipping
hp=ss.sosfilt(ss.butter(8,9000,'high',fs=sr,output='sos'),mix)
n=sr; m=len(hp)//n
h=db(np.sqrt((hp[:m*n].reshape(m,n)**2).mean(1)))
print('9k+ per-second dB: median %.1f p10 %.1f p90 %.1f max %.1f at %d s'%(np.median(h[:236]),*np.percentile(h[:236],[10,90]),h[:236].max(),h[:236].argmax()))
cl=np.array([(np.abs(mix[i*n:(i+1)*n])>=0.999).sum() for i in range(m)])
print('corr(9k+ dB, clipped count) %.2f; median 9k+ in seconds with 0 clipped %.1f ; with >50 clipped %.1f'%(np.corrcoef(h[:236],cl[:236])[0,1],np.median(h[:236][cl[:236]==0]),np.median(h[:236][cl[:236]>50])))
