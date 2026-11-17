import librosa,numpy as np
from scipy.signal import butter,sosfilt
y,sr=librosa.load('/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/drums.wav',sr=22050)
T=60/78.003/4;ph=0.164
s=butter(4,[30,150],'bandpass',fs=sr,output='sos');e=np.abs(sosfilt(s,y));hop=256
env=librosa.util.normalize(np.convolve(e,np.ones(hop)/hop,'same')[::hop]);t=np.arange(len(env))*hop/sr
for a,b in[(33,60),(60,90),(120,168),(168,178),(178,188),(188,200)]:
    n0=int((a-ph)/T);n1=int((b-ph)/T);acc=np.zeros(16);c=np.zeros(16)
    for n in range(n0,n1):
        i=np.searchsorted(t,ph+n*T);acc[n%16]+=env[max(i-3,0):i+4].max();c[n%16]+=1
    acc/=c;print(a,b,' '.join(f'{v:.2f}' for v in acc/acc.max()))
