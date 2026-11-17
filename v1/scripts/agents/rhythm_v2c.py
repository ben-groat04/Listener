import numpy as np, librosa, json
D='/home/user/Listener/v1/data/video2/'
y,sr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050)
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=128); fps=sr/128
# phase of grid mod 2s per 20s window: circular mean at 2s period weighted by oe
for a in range(30,300,10):
    seg=oe[int(a*fps):int((a+10)*fps)]; t=np.arange(len(seg))/fps+a
    z=(seg*np.exp(2j*np.pi*t/0.5)).sum(); z2=(seg*np.exp(2j*np.pi*t/2)).sum()
    print(a,'phase@0.5s',round((np.angle(z)/(2*np.pi)*0.5)%0.5,3),'str',round(abs(z)/seg.sum(),2),'phase@2s',round((np.angle(z2)/(2*np.pi)*2)%2,3))
# drum rms per 0.5s around stops
dr=np.sqrt(np.convolve(y**2,np.ones(2205)/2205,'same'))
for a,b in [(68,80),(83,90),(298,306)]:
    print(a,b,[ (round(x,1),round(20*np.log10(dr[int(x*sr)]+1e-9))) for x in np.arange(a,b,0.5)])
bt=np.load if 0 else json.load(open(D+'audio_features/beat_times.json'))
bt=np.array(bt); d=np.diff(bt)
print('beat ioi median',np.median(d), 'frac near .375',np.mean(abs(d-0.375)<0.02))
ons=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=128,units='time')
for a in [28,28.2,88.5,88.6,76,77,104]: pass
for lo,hi in [(24,30),(86,90),(100,104),(72,80)]:
    print(lo,hi,[round(float(o),2) for o in ons if lo<=o<hi])
