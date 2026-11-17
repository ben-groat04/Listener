import numpy as np, soundfile as sf, librosa
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
v,sr=sf.read(D+'vocals.wav'); y=librosa.resample(v.mean(1),orig_sr=sr,target_sr=16000)
M=librosa.power_to_db(librosa.feature.melspectrogram(y=y,sr=16000,n_fft=512,hop_length=160,n_mels=48)) # 10ms
M=M-M.mean(); fr=100
def best(a,b0,span=0.6,L=6.0):
    A=M[:,int(a*fr):int((a+L)*fr)].ravel()
    res=[]
    for t in np.arange(b0-span,b0+span,0.01):
        B=M[:,int(t*fr):int(t*fr)+int(L*fr)].ravel()
        res.append((np.corrcoef(A,B)[0,1],t))
    return max(res)
print('hook chain (6 s blocks)')
for a,b in [(2*60+12,2*60+24),(2*60+24,2*60+36),(2*60+36,2*60+48),(2*60+12,2*60+36),(2*60+12,2*60+48),(12.5,2*60+12),(12.5,2*60+24),(48.5,2*60+0.5),(48.5,2*60+12),(48.5,12.5+24),(12.5,48.5)]:
    r,t=best(a,b); print(f'{a:.1f} vs ~{b:.1f}: best r={r:.2f} at {t:.2f} lag={t-a:.2f}')
