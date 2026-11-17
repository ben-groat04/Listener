import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_birdwalk/'
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False); print(sr,y.shape)
m=y.mean(0) if y.ndim>1 else y
w=y[:, int(100*sr):int(120*sr)] if y.ndim>1 else y[int(100*sr):int(120*sr)]
print('sample peak window dBFS',20*np.log10(np.abs(w).max()),'whole',20*np.log10(np.abs(y).max()))
hop=int(sr*.01); e=librosa.feature.rms(y=m,frame_length=hop*2,hop_length=hop)[0]; db=20*np.log10(e+1e-9)
for t in np.arange(117.5,121,0.25): print(round(t,2),round(float(db[int(t*100):int(t*100+25)].mean()),1),end=' | ')
print()
i=np.argmax(db[11700:11950])+11700; print('peak env t',i/100,db[i])
# drop time: biggest fall
d=db[11800:12000]; print('min',(np.argmin(d)+11800)/100)
for k in range(11860,11925,5): print(k/100,round(float(db[k]),1),end=' ')
print()
# band split in window
S=np.abs(librosa.stft(m[int(100*sr):int(120*sr)],n_fft=4096))**2
f=librosa.fft_frequencies(sr=sr,n_fft=4096); tot=S.sum()
for lo,hi in [(0,150),(150,300),(300,3400),(3400,8000),(8000,sr/2)]: print(lo,hi,round(float(S[(f>=lo)&(f<hi)].sum()/tot),3))
# spectral rolloff 
print('rolloff95',np.median(librosa.feature.spectral_rolloff(y=m[int(100*sr):int(120*sr)],sr=sr,roll_percent=.95)))
bt=np.array(json.load(open(D+'audio_features/beat_times.json')));b=bt[(bt>=100)&(bt<120)];print('beats',len(b),np.round(np.diff(b).mean(),3))
# 1-s pitch/loop: chroma bar correlation in window using beats groups of 4
c=librosa.feature.chroma_cqt(y=m[int(100*sr):int(120*sr)],sr=sr,hop_length=512)
print('chroma ok',c.shape)
# end of mix: from 1:59 how long does lowpass track; check stems 10ms around 118.9
