import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_birdwalk/'
sr=22050
def L(n): return librosa.load(D+f'stems_raw/htdemucs/song/{n}.wav',sr=sr,mono=True)[0]
b=L('bass'); d=L('drums'); v=L('vocals'); o=L('other')
hop=220
# bass onsets
oe=librosa.onset.onset_strength(y=b,sr=sr,hop_length=hop)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=hop,units='time')
on=on[(on>=100)&(on<119.5)]; print('bass onsets',len(on),np.round(on,2)); print('IOI',np.round(np.diff(on),2))
step=0.369
best=None
for ph in np.arange(0,step,0.005):
    r=((on-ph+step/2)%step)-step/2; s=np.sqrt((r**2).mean())
    if best is None or s<best[0]: best=(s,ph)
print('0.369 grid rms ms',best[0]*1000,'of step',best[0]/step)
for st in [0.395,0.3947]:
    bb=min((np.sqrt((((((on-ph+st/2)%st)-st/2))**2).mean()),ph) for ph in np.arange(0,st,0.005)); print(st,bb[0]*1000)
# 10ms stem envelope across 118.4..120.6
for n,y in [('drums',d),('bass',b),('vocals',v),('other',o)]:
    e=20*np.log10(librosa.feature.rms(y=y,frame_length=441,hop_length=221)[0]+1e-9)
    print(n,[round(float(e[int(t*100):int(t*100+20)].mean())) for t in np.arange(118.0,121.0,0.2)])
# drum peaks 118-120.5
e=librosa.feature.rms(y=d,frame_length=441,hop_length=221)[0]
pk,_=ss.find_peaks(e[11800:12100],height=0.02,distance=8); print('drum peaks',(pk+11800)/100)
# ridge of sweep in vocals 1:54..1:59
S=np.abs(librosa.stft(v[int(114*sr):int(119*sr)],n_fft=2048,hop_length=441)); f=librosa.fft_frequencies(sr=sr,n_fft=2048)
m=(f>1500)&(f<8000)
for i in range(0,S.shape[1],25): 
    c=S[:,i]; print(round(114+i*.02,2),int(f[m][np.argmax(c[m])]),end=' | ')
print()
# centroid of other 1:50..1:58 per sec
for t in range(100,120): 
    seg=o[int(t*sr):int((t+1)*sr)]; print(t,int(librosa.feature.spectral_centroid(y=seg,sr=sr).mean()),end=' ')
