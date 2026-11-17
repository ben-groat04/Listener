import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'drums.wav',sr=22050,mono=True)
# kick-band onsets (<150 Hz)
sos=ss.butter(4,150,'lp',fs=sr,output='sos'); k=ss.sosfilt(sos,y)
oe=librosa.onset.onset_strength(y=np.abs(k),sr=sr,hop_length=128)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=128,units='time')
P=0.7693;a=0.973
# fit grid: slot period P/4 ; estimate phase of 16-slot cycle (4 beats) using kick onsets 0:30-2:45
o=on[(on>30)&(on<165)]
best=None
for off in np.arange(0,4*P,0.005):
    s=((o-off)/(P/4)); r=np.abs(s-np.round(s)).mean()
    if best is None or r<best[0]: best=(r,off)
off=best[1]; print('slot-grid offset %.3f resid %.3f slots'%(off,best[0]))
slot=np.round((o-off)/(P/4)).astype(int)%16
cnt=np.bincount(slot,minlength=16); print('kick-band slot counts',cnt.tolist())
# bar one = slot with max count among 0,4,8,12 ... print
for B in range(4):
  print('strongest beat-slot',B*4,cnt[B*4])
# downbeat candidate: slot with max count
s0=int(np.argmax(cnt)); print('max slot',s0)
base=off+s0*P/4  # time of that slot in cycle
def bar(t): x=(t-base)/(4*P); return x, ((x%1)*4)
ev={'0:32 voice end':31.70,'1:15.3 bass out':75.3,'1:27.4 wall':87.4,'1:40.0 bass in':100.0,'1:55 bass out':115.0,'2:01.2 sub1':121.2,'2:07.3':127.3,'2:13.4':133.4,'2:38.4 bass in':158.4,'2:47.8 stop':167.8,'2:48.22 return':168.22}
for n,t in ev.items():
    x,b=bar(t); print('%-18s bar %.2f  beat-in-bar %.2f'%(n,x,b))
