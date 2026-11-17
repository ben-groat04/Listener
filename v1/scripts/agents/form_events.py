import numpy as np, librosa, json
S='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
bt=np.array(json.load(open('/home/user/Listener/v1/data/video1/audio_features/beat_times.json')))
bt=bt if bt.ndim==1 else np.array(bt)
print('beats',len(bt),bt[:5],'median ibi %.3f'%np.median(np.diff(bt)))
def env(n):
    y,sr=librosa.load(S+n+'.wav',sr=22050,mono=True); h=1102  # 0.05s
    r=librosa.feature.rms(y=y,hop_length=h)[0]; return 20*np.log10(r+1e-9),np.arange(len(r))*h/sr
b,t=env('bass'); o,_=env('other')
def edges(x,thr,name,lo,hi):
    on=x>thr
    for i in range(1,len(x)):
        if on[i]!=on[i-1] and lo<=t[i]<=hi: print(name,'%s at %.2f'%('ON' if on[i] else 'OFF',t[i]), 'nearest beat idx %d (%.2f) off %.2f'%(np.argmin(abs(bt-t[i])),bt[np.argmin(abs(bt-t[i]))],t[i]-bt[np.argmin(abs(bt-t[i]))]))
edges(b,-45,'bass',60,160)
# other step at 1:27 and 1:58
for name,a,bb in [('other',85,90),('other',115,121)]:
    seg=o[(t>=a)&(t<bb)]; print(name,[ '%.2f:%.0f'%(tt,v) for tt,v in zip(t[(t>=a)&(t<bb)][::4],seg[::4])])
