import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
sr=22050
L=lambda n: librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
o,v=L('other'),L('vocals')
sg=lambda x,a,b:x[int(a*sr):int(b*sr)]
def pf(y):
    S=np.abs(librosa.stft(y,n_fft=2048))**2; return np.median(librosa.feature.spectral_flatness(S=S+1e-12)[0])
for a,b in [(30,60),(90,109),(110,119),(121,133),(135,153),(160,168),(77,85)]:
    y=sg(o,a,b); S=np.abs(librosa.stft(y,n_fft=4096)); f=librosa.fft_frequencies(sr=sr,n_fft=4096); p=S.mean(1)
    top=f[np.argsort(p)[-5:]]
    print(a,b,'frame flatness med %.4f'%pf(y),'strongest bins',np.round(np.sort(top)))
# repeat check: vocals 0:27-0:32 vs 2:44-2:48
x=sg(v,27,33); y=sg(v,163.5,169)
x=x/np.abs(x).max(); y=y/np.abs(y).max()
c=np.correlate(y,x,'full'); print('xcorr max (norm) %.3f'%(c.max()/np.sqrt((x**2).sum()*(y**2).sum())))
# envelope correlation
ex=librosa.feature.rms(y=x,hop_length=441)[0]; ey=librosa.feature.rms(y=y,hop_length=441)[0]
n=min(len(ex),len(ey)); 
best=max(np.corrcoef(ex[:n-k],ey[k:n])[0,1] for k in range(0,min(100,n-20)))
print('envelope corr best %.2f'%best)
# vocal-stem spectral tilt in bursts
for a,b in [(19,24),(28,32),(164,168)]:
    S=np.abs(librosa.stft(sg(v,a,b),n_fft=2048))**2; f=librosa.fft_frequencies(sr=sr,n_fft=2048); p=S.mean(1)
    c=np.cumsum(p)/p.sum(); print(a,b,'vocal 95%% below %.0f Hz'%f[np.argmax(c>.95)])
