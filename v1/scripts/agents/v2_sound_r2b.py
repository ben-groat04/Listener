import numpy as np,librosa,warnings;warnings.filterwarnings('ignore')
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050
o=librosa.load(D+'other.wav',sr=sr,mono=True)[0]
b=librosa.load(D+'bass.wav',sr=sr,mono=True)[0]
bands=[(60,250),(250,1000),(1000,2000),(2000,4000),(4000,8000)]
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
print('other-stem band dB per 20s (60-250,250-1k,1-2k,2-4k,4-8k) and H/P')
for a in range(0,300,20):
    x=o[a*sr:(a+20)*sr];S=np.abs(librosa.stft(x,n_fft=2048,hop_length=512))**2;P=S.mean(1)
    print('%d:%02d'%(a//60,a%60),' '.join('%.1f'%(10*np.log10(P[(f>=l)&(f<h)].sum()+1e-12)) for l,h in bands))
print('1:50-2:02 other rms per 1s');
print(' '.join('%.1f'%(20*np.log10(np.sqrt((o[t*sr:(t+1)*sr]**2).mean())+1e-9)) for t in range(110,122)))
print('bass gaps (<-40 dB, 0.125s frames) 4:20-4:50')
e=20*np.log10(librosa.feature.rms(y=b[260*sr:290*sr],frame_length=2756,hop_length=2756)[0]+1e-9)
print([('%d:%05.2f'%((260+i*0.125)//60,(260+i*0.125)%60),round(v)) for i,v in enumerate(e) if v<-40])
