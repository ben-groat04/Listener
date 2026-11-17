import numpy as np,librosa
D='/home/user/Listener/v1/data/video2/'
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False)
m=y.mean(0)
# when does 4k+ content switch on, 0:36-0:44 in 1s
import scipy.signal as ss
sos=ss.butter(4,4000,'hp',fs=sr,output='sos');h=ss.sosfilt(sos,m)
for a in range(34,46):
    print(a,'HF rms dB %.1f'%(20*np.log10(np.sqrt((h[a*sr:(a+1)*sr]**2).mean())+1e-9)))
# vocals stem band limits when speech present
v,_=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=22050,mono=True)
S=np.abs(librosa.stft(v,n_fft=2048,hop_length=512))**2;f=librosa.fft_frequencies(sr=22050,n_fft=2048)
fr=librosa.frames_to_time(np.arange(S.shape[1]),sr=22050,hop_length=512)
for a,b in [(65,80),(225,240),(250,265)]:
    mm=(fr>=a)&(fr<b);P=S[:,mm].mean(1);c=np.cumsum(P)/P.sum()
    print('vocal',a,b,'roll95 %.0f roll99 %.0f cent %.0f'%(f[np.searchsorted(c,.95)],f[np.searchsorted(c,.99)],(P*f).sum()/P.sum()))
# ending tail: width and level per 0.25s 5:00-5:05
for a in np.arange(300.5,305.9,0.5):
    z=y[:,int(a*sr):int((a+.5)*sr)]
    M=(z[0]+z[1])/2;Sd=(z[0]-z[1])/2
    print('%.1f'%a,'%.1f dB'%(20*np.log10(np.sqrt((z**2).mean())+1e-9)),'S/M %.1f'%(10*np.log10(((Sd**2).sum()+1e-12)/((M**2).sum()+1e-12))))
# DC / low-end content under 40Hz, intro noise floor
print('sub40 rms dB 5-25: %.1f'%(20*np.log10(np.sqrt((ss.sosfilt(ss.butter(4,40,'lp',fs=sr,output='sos'),m[5*sr:25*sr])**2).mean()))))
print('sub40 rms dB 120-140: %.1f'%(20*np.log10(np.sqrt((ss.sosfilt(ss.butter(4,40,'lp',fs=sr,output='sos'),m[120*sr:140*sr])**2).mean()))))
# clipping: fraction samples >0.99
print('clip frac',(np.abs(y)>0.99).mean(), 'count',(np.abs(y)>0.99).sum())
# short-term LUFS-ish: 3s rms percentile
r=[20*np.log10(np.sqrt((m[i*sr:(i+3)*sr]**2).mean())) for i in range(0,300,3)]
print('3s rms p10/50/90',np.percentile(r,[10,50,90]))
