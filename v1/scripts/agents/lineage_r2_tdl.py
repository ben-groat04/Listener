import numpy as np, librosa, soundfile as sf, scipy.signal as sg
D='/home/user/Listener/v1/data/t_dl_mirror/'; S=D+'stems_raw/htdemucs/song/'; sr=44100
st={k:sf.read(S+k+'.wav')[0].mean(1) for k in ['drums','bass']}
# (a) bass pitch in hook 4 step vs verse
b=st['bass']
for name,(a,c) in {'hook4 walk 3:17-3:24':(197,204),'hook1 walk 0:14-0:21':(14,21),'verse 2:45-2:52':(165,172)}.items():
    seg=b[int(a*sr):int(c*sr)]
    f0,vf,vp=librosa.pyin(seg,fmin=30,fmax=200,sr=sr,frame_length=8192,hop_length=2205)
    t=np.arange(len(f0))*0.05+a
    # median per 0.5 s
    out=[]
    for k in range(0,int((c-a)/0.5)):
        m=(t>=a+k*0.5)&(t<a+k*0.5+0.5)&vf
        out.append(round(float(np.median(f0[m])),1) if m.sum()>3 else None)
    print(name,out)
# (b) hat IOI: refractory sensitivity
d=st['drums']
for lo,hi in [(5000,7800),(6000,9500)]:
    sos=sg.butter(4,[lo,hi],'bandpass',fs=sr,output='sos'); x=sg.sosfilt(sos,d[30*sr:215*sr])
    env=librosa.onset.onset_strength(y=x,sr=sr,hop_length=110,aggregate=np.median)
    for refr in (0.03,0.06,0.10):
        on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=110,units='time',wait=int(refr/0.0025),delta=0.15)
        ioi=np.diff(on); n=len(ioi)
        print('hat',lo,hi,'refr',refr,'n',n,'rate/s %.2f'%(len(on)/185),'<0.1 %.0f%%'%(100*(ioi<0.1).mean()),'~0.16(0.13-0.2) %.0f%%'%(100*((ioi>0.13)&(ioi<0.2)).mean()),'~0.08(0.07-0.1) %.0f%%'%(100*((ioi>0.07)&(ioi<0.1)).mean()))
# (c) kick 32-step (2-bar) fold, hook vs verse, and snare-band backbeat
beat=60/94.0
def fold(lo,hi,a,c,off=None):
    sos=sg.butter(4,[lo,hi],'bandpass',fs=sr,output='sos'); x=sg.sosfilt(sos,d[int(a*sr):int(c*sr)])
    env=librosa.onset.onset_strength(y=x,sr=sr,hop_length=220); t=np.arange(len(env))*220/sr+a
    return env,t
env,t=fold(30,150,30.4,71.3)
best=None
for o in np.arange(0,beat*8,0.01):
    ph=((t-o)/beat*4)%32; bins=np.floor(ph).astype(int)%32
    prof=np.array([env[bins==k].mean() for k in range(32)])
    sc=prof[0]-prof.mean()
    if best is None or sc>best[0]: best=(sc,o,prof)
print('verse1 kick 32-step profile (anchored max step0):',np.round(best[2]/best[2].max(),2))
off=best[1]
for nm,(a,c) in {'verse1 30.4-71.3':(30.4,71.3),'hook 1:11.3-1:31.4':(71.3,91.4),'verse2 1:31.4-2:12':(91.4,132),'verse3 2:34-3:15':(154,195)}.items():
    env,t=fold(30,150,a,c); ph=((t-off)/beat*4)%32; bins=np.floor(ph).astype(int)%32
    prof=np.array([env[bins==k].mean() for k in range(32)]); prof/=prof.max()
    top=np.argsort(prof)[::-1][:8]
    print(nm,'top steps',sorted(top.tolist()),'corr with verse1',round(np.corrcoef(prof,best[2])[0,1],2))
