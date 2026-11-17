# kick shape: pitch trajectory and band-limited envelope; is the 'double rise' a second hit, a pitch sweep or beating
import numpy as np, soundfile as sf, scipy.signal as ss
from scipy.signal import hilbert, find_peaks
D='/home/user/Listener/v1/data/t_dl_mirror/'; S=D+'stems_raw/htdemucs/song/'
x,sr=sf.read(S+'drums.wav',dtype='float32'); dr=x.mean(1)
def band_env(lo,hi):
    k=ss.sosfiltfilt(ss.butter(4,[lo,hi],'band',fs=sr,output='sos'),dr); e=np.abs(hilbert(k))
    return np.maximum(ss.sosfiltfilt(ss.butter(2,50,'low',fs=sr,output='sos'),e),1e-9)
db=lambda v:20*np.log10(v+1e-12)
e=band_env(35,130); step=44; ed=e[::step]; t=np.arange(len(ed))*step/sr
pk,_=find_peaks(db(ed),height=db(ed[(t>30)&(t<215)]).max()-30,distance=80,prominence=6); pk=pk[(t[pk]>30)&(t[pk]<215)]
# use only kicks isolated (no other kick within 150 ms before the peak) 
iso=[p for p in pk if all(abs(t[p]-t[q])>0.3 or q==p for q in pk)]
print('isolated kicks (no other kick peak within 300 ms):',len(iso),'of',len(pk))
# time-resolved dominant frequency (25 ms hann, 5 ms hop, zero-padded)
offs=np.arange(-10,141,10)/1000
tr=[];lv=[]
for o in offs:
    fr=[];l=[]
    for p in iso[:300]:
        a=int((t[p]+o)*sr)-int(0.0125*sr); 
        if a<0: continue
        s=dr[a:a+int(0.025*sr)]*np.hanning(int(0.025*sr)); F=np.abs(np.fft.rfft(s,8192)); f=np.fft.rfftfreq(8192,1/sr); m=(f>30)&(f<250)
        fr.append(f[m][np.argmax(F[m])]); l.append(F[m].max())
    tr.append(np.median(fr)); lv.append(np.median(l))
print('offset ms :',' '.join('%4d'%(o*1000) for o in offs))
print('dom Hz    :',' '.join('%4.0f'%v for v in tr))
print('level dB  :',' '.join('%4.0f'%v for v in db(np.array(lv)/max(lv))))
# second rise in narrow bands for isolated kicks
for lo,hi in [(35,60),(60,90),(90,130)]:
    e2=band_env(lo,hi)[::step]; c=0;gp=[]
    for p in iso:
        seg=e2[p:p+160]; 
        if len(seg)<160: continue
        q,_=find_peaks(seg,prominence=seg[0]*0.2); q=q[q>25]
        if len(q): c+=1;gp.append(q[0]*step/sr*1000)
    print('band %d-%d Hz isolated kicks with second rise: %d/%d, gap median %.0f ms'%(lo,hi,c,len(iso),np.median(gp) if gp else 0))
