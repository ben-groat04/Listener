import numpy as np, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050; hop=32; fr=sr/hop
dr,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)
S=np.abs(librosa.stft(dr,n_fft=1024,hop_length=hop)); f=librosa.fft_frequencies(sr=sr,n_fft=1024)
def band(lo,hi):
    m=(f>=lo)&(f<hi); e=np.log1p(30*S[m].sum(0)); return np.maximum(np.diff(e,prepend=e[0]),0)
env={'kick':band(35,110),'snare':band(150,400),'crack':band(1500,5000),'hat':band(6000,10000)}
tot=sum(v/v.std() for v in env.values())
t=np.arange(len(tot))/fr
bar=2.554
print('bar-period phase per 12 s block (ms), strength')
for a in range(24,228,12):
    m=(t>=a)&(t<a+12); z=np.sum(tot[m]*np.exp(-2j*np.pi*t[m]/bar)); print(a,round(np.angle(z)/(2*np.pi)*bar*1000,1),round(abs(z)/tot[m].sum(),3))
# fine-scan bar period to maximise fold concentration over 24-230
m=(t>=24)&(t<230)
best=None
for B in np.arange(2.53,2.58,0.0005):
    z=np.sum(tot[m]*np.exp(-2j*np.pi*t[m]/B)); 
    # use 4 harmonics
    s=sum(abs(np.sum(tot[m]*np.exp(-2j*np.pi*h*t[m]/B))) for h in (1,2,3,4,6,8))
    if best is None or s>best[0]: best=(s,B)
print('best bar period',best[1],'bpm',240/best[1])
B=best[1]
z=np.sum(tot[m]*np.exp(-2j*np.pi*t[m]/B)); p0=np.angle(z)/(2*np.pi)*B
for k,v in list(env.items())+[('all',tot)]:
    x=v/v.std(); ph=((t[m]-p0)%B)/B
    h,_=np.histogram(ph,bins=128,weights=x[m]); h=h/h.mean()
    pk=[(i,round(h[i],2)) for i in range(128) if h[i]>1.6*np.median(h) and h[i]==h[max(0,i-3):i+4].max()]
    print(k,'peaks (bin of 128 per bar, height/mean):',pk)
np.save('/tmp/fold_params.npy',np.array([B,p0]))
