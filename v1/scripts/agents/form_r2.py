import numpy as np, librosa, json
S='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
bt=np.array(json.load(open('/home/user/Listener/v1/data/video1/audio_features/beat_times.json')))
# linear fit of the beat grid (exclude the two tracker slips by robust fit)
n=np.arange(len(bt)); P,a=np.polyfit(n,bt,1)
res=bt-(a+P*n); print('fit P=%.4f a=%.3f  resid std %.3f max %.3f'%(P,a,res.std(),abs(res).max()))
ev={'0:32 voice off':31.8,'0:41 voice B':41.0,'1:15.3 bass off':75.3,'1:27.4 wall':87.4,'1:40.0 bass in':100.0,'1:55.5 bass off':115.5,
'2:01.1 stab1':121.1,'2:07.2 stab2':127.2,'2:13.3 stab3':133.3,'2:14 reignite':134.0,'2:38.4 bass on':158.4,'2:47.8 stop':167.8,'2:48.2 return':168.2,'3:08.06 end':188.06}
print('event, beats since fitted beat0, mod4, mod8, mod16 (0 = tracker beat)')
for k,t in ev.items():
    b=(t-a)/P; print('%-18s %7.2f  m4 %5.2f  m8 %5.2f m16 %5.2f'%(k,b,b%4,b%8,b%16))
# refine edges with 20 ms envelopes
def env(nm,h=441):
    y,sr=librosa.load(S+nm+'.wav',sr=22050,mono=True); h=int(0.02*sr)
    r=librosa.feature.rms(y=y,hop_length=h,frame_length=2*h)[0]; return 20*np.log10(r+1e-9),np.arange(len(r))*h/sr
b,t=env('bass'); o,_=env('other'); d,_=env('drums')
def first_cross(x,lo,hi,thr,up):
    m=(t>=lo)&(t<=hi); tt=t[m]; xx=x[m]
    for i in range(1,len(xx)):
        if up and xx[i-1]<thr<=xx[i]: return tt[i]
        if (not up) and xx[i-1]>=thr>xx[i]: return tt[i]
for nm,x,lo,hi,thr,up in [('bass off ~1:15',b,74,77,-45,False),('bass on ~1:40',b,98,102,-40,True),('bass off ~1:55',b,114,117,-45,False),('bass on ~2:38',b,156,160,-40,True),('other up ~1:27',o,85,90,-30,True),('other up ~2:14',o,132,136,-23,True)]:
    c=first_cross(x,lo,hi,thr,up)
    print(nm,'%.2f'%c, 'beats %.2f m4 %.2f'%((c-a)/P,((c-a)/P)%4))
# beats between successive events using the fitted grid
