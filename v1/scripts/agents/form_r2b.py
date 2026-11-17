import numpy as np, librosa, json
from scipy import signal
D='/home/user/Listener/v1/data/video1/'
bt=np.array(json.load(open(D+'audio_features/beat_times.json'))); P,a=np.polyfit(np.arange(len(bt)),bt,1)
def bar(t): return (t-a)/P/4
# vocals envelope edges
y,sr=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=22050,mono=True); h=int(0.02*sr)
r=20*np.log10(librosa.feature.rms(y=y,hop_length=h,frame_length=2*h)[0]+1e-9); t=np.arange(len(r))*h/sr
for lo,hi in [(24,34),(164,172)]:
    m=(t>=lo)&(t<=hi); tt=t[m]; xx=r[m]; on=xx>-40
    ed=[(round(tt[i],2),'ON' if on[i] else 'OFF') for i in range(1,len(on)) if on[i]!=on[i-1]]
    print(lo,hi,[(e,k,round(bar(e),2)) for e,k in ed])
# K-weighted short-term loudness per second (BS.1770 filters, mono-sum of stereo mix approx)
import soundfile as sf
x,fs=sf.read(D+'audio/song.wav'); 
if x.ndim==1: x=np.stack([x,x],1)
# stage1 high-shelf, stage2 RLB (coefficients for 48k; resample if needed)
if fs!=48000:
    x=np.stack([librosa.resample(x[:,i],orig_sr=fs,target_sr=48000) for i in range(x.shape[1])],1); fs=48000
b1=[1.53512485958697,-2.69169618940638,1.19839281085285]; a1=[1,-1.69065929318241,0.73248077421585]
b2=[1,-2,1]; a2=[1,-1.99004745483398,0.99007225036621]
k=signal.lfilter(b2,a2,signal.lfilter(b1,a1,x,axis=0),axis=0)
ms=(k**2).sum(1)
win=int(3*fs); out=[]
for s in range(0,int(len(ms)/fs)-2):
    seg=ms[s*fs:s*fs+win]; out.append(-0.691+10*np.log10(seg.mean()+1e-12))
out=np.array(out); json.dump(out.tolist(),open('/tmp/form_stlufs.json','w'))
print('ST-LUFS (3 s window start s): min %.1f max %.1f'%(out.min(),out.max()))
for lo,hi,name in [(5,31,'0:05-0:31'),(35,75,'0:35-1:15'),(78,100,'1:18-1:40'),(100,114,'1:40-1:54'),(122,133,'2:02-2:13'),(136,157,'2:16-2:37'),(170,186,'2:50-3:06')]:
    print(name,'mean %.1f  range %.1f..%.1f'%(out[lo:hi].mean(),out[lo:hi].min(),out[lo:hi].max()))
