import numpy as np, librosa, soundfile as sf
P='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
v,sr=sf.read(P+'vocals.wav'); m=v.mean(1)
def ridge(a,b,fmin=1500):
    s=m[int(a*sr):int(b*sr)]
    S=np.abs(librosa.stft(s,n_fft=4096,hop_length=1024)); f=librosa.fft_frequencies(sr=sr,n_fft=4096)
    k=f>fmin; idx=np.argmax(S[k],0); return [(round(a+i*1024/sr,2),int(f[k][j])) for i,j in enumerate(idx)][::3]
for a,b in [(9.2,12.2),(152.3,155.8),(164,167.2),(176.4,179.5)]:
    print(a,b,ridge(a,b))
# L/R correlation of vocal stem per section
for a,b in [(1,12),(12,24),(25,47),(48,59),(60,70),(71,83),(84,100),(101,119),(121,131),(132,143),(144,155),(157,167)]:
    L=v[int(a*sr):int(b*sr),0];R=v[int(a*sr):int(b*sr),1]
    print(a,b,'LR corr %.2f'%np.corrcoef(L,R)[0,1])
# syllable rate at hook vs verse using envelope peaks
import scipy.signal as ss
env=librosa.feature.rms(y=m,frame_length=1024,hop_length=256)[0]
env=ss.savgol_filter(env,5,2)
pk,_=ss.find_peaks(env,prominence=0.15*env.max()/5,distance=int(0.09*sr/256))
t=pk*256/sr
for a,b in [(25,47),(48,59),(71,83),(84,100),(101,119),(121,131),(132,143),(144,155),(157,167)]:
    x=t[(t>=a)&(t<b)]; d=np.diff(x)
    print(a,b,'peaks/s %.1f'%(len(x)/(b-a)),'median IOI %.3f'%np.median(d))
