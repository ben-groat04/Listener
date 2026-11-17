import numpy as np, librosa, scipy.signal as ss
y,sr=librosa.load('data/video1/stems_raw/htdemucs/song/vocals.wav',sr=16000)
hop=160
rms=librosa.feature.rms(y=y,frame_length=400,hop_length=hop)[0]
db=20*np.log10(rms+1e-6)
env=ss.savgol_filter(rms,9,2)
t=np.arange(len(rms))*hop/sr
# syllable-like peaks: 4-8 Hz modulation, peaks >-40dB with prominence
segs={'A 0:09.9-0:18':(9.9,18),'B 0:19-0:31.7':(19,31.7),'C 0:40.6-0:43':(40.6,43),'D 0:51-0:56':(50.9,56.1),'E 1:19.7-1:27':(19.7+60,87),'F town list 2:16-2:26.6':(136.1,146.6),'G towns 2:26.6-2:36':(146.6,156),'H final 2:43.8-2:48':(163.8,168.3),'I 3:06.5-3:08.4 (end)':(186.5,188.4)}
for k,(a,b) in segs.items():
    m=(t>=a)&(t<b); e=env[m]; d=db[m]
    pk,_=ss.find_peaks(ss.savgol_filter(e,5,2),prominence=0.004,distance=8)
    act=(d>-45).mean()
    # pauses >0.2s
    lo=d<-45; runs=np.diff(np.r_[0,lo.astype(int),0]); st=np.where(runs==1)[0]; en=np.where(runs==-1)[0]
    pauses=[(en[i]-st[i])*0.01 for i in range(len(st)) if (en[i]-st[i])>=20]
    print(f"{k}: dur {b-a:.1f}s peaks/s {len(pk)/(b-a):.2f} active {act:.2f} median dB {np.median(d):.1f} max {d.max():.1f} pauses>=.2s n={len(pauses)}")
