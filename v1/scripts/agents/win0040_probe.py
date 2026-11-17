import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_cshells_cshore/'
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False)
m=y.mean(0) if y.ndim>1 else y
a,b=int(40*sr),int(60*sr)
seg=m[a:b]
print('sr',sr,'peak 40-60 dBFS',20*np.log10(np.abs(y[...,a:b]).max()),'whole',20*np.log10(np.abs(y).max()))
h=int(sr*0.01)
env=np.sqrt(np.convolve(seg**2,np.ones(h)/h,'same'))[::h]
db=20*np.log10(env+1e-9)
for t in range(0,200,5):
    print(f'{40+t/10:.1f}:{db[t:t+5].max():.0f}',end=' ')
print()
# onsets
o=librosa.onset.onset_detect(y=seg,sr=sr,units='time',backtrack=False)
print('onsets',[round(40+x,2) for x in o])
# bands, centroid per 2s
for s in range(40,60,2):
    x=m[int(s*sr):int((s+2)*sr)];S=np.abs(np.fft.rfft(x))**2;f=np.fft.rfftfreq(len(x),1/sr)
    print(s,'cent',int((S*f).sum()/S.sum()),'<200',round(S[f<200].sum()/S.sum(),3),'>4k',round(S[f>4000].sum()/S.sum(),3))
# drums stem onsets
for n in ['drums','other']:
    z,_=librosa.load(D+f'stems_raw/htdemucs/song/{n}.wav',sr=sr,mono=True)
    zz=z[a:b];oo=librosa.onset.onset_detect(y=zz,sr=sr,units='time')
    print(n,[round(40+x,2) for x in oo])
