import librosa,numpy as np
from scipy.signal import butter,sosfilt
P='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
y,sr=librosa.load(P+'drums.wav',sr=22050,mono=True)
lo=sosfilt(butter(4,[40,120],'bp',fs=sr,output='sos'),y)
on=librosa.onset.onset_detect(y=lo,sr=sr,hop_length=128,units='time',backtrack=False,delta=0.2)
on=np.array(on)
sel=on[(on>90)&(on<296)]
print(len(sel))
# fit period/phase: test periods
best=None
for T in np.arange(0.495,0.505,0.00005):
    ph=np.angle(np.mean(np.exp(2j*np.pi*sel/T)))
    R=abs(np.mean(np.exp(2j*np.pi*sel/T)))
    if best is None or R>best[0]: best=(R,T,ph/(2*np.pi)*T)
print('period fit',best)
R,T,p=best
# per-section phase drift
for a in range(90,296,30):
    s=sel[(sel>=a)&(sel<a+30)]
    z=np.mean(np.exp(2j*np.pi*(s-p)/T)); print(a,round(abs(z),2),round(np.angle(z)/(2*np.pi)*T*1000),'ms')
# 1:28.62 drop position
d=on[(on>88)&(on<90)];print(d)
print('beat idx of drop rel 28.13 beat grid',(88.62-28.13)/0.5)
