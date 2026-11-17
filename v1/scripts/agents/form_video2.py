import librosa,numpy as np,json
D='/home/user/Listener/v1/data/video2/'
y,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=True)
dr,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050,mono=True)
vo,_=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=22050,mono=True)
on=librosa.onset.onset_detect(y=dr,sr=sr,units='time',backtrack=False)
cen=librosa.feature.spectral_centroid(y=y,sr=sr,hop_length=512)[0]
hf=np.abs(librosa.stft(y,n_fft=2048,hop_length=512))
fr=librosa.fft_frequencies(sr=sr,n_fft=2048)
def band(a,b): return 20*np.log10(np.sqrt((hf[(fr>=a)&(fr<b)]**2).mean(0))+1e-9)
lo,mid,hi=band(30,200),band(200,2000),band(2000,10000)
t=librosa.frames_to_time(np.arange(len(cen)),sr=sr,hop_length=512)
for s in range(0,306,10):
    m=(t>=s)&(t<s+10)
    n=((on>=s)&(on<s+10)).sum()
    vm=vo[int(s*sr):int((s+10)*sr)]
    print('%d:%02d onsets/s %.1f cen %4.0f lo %.0f mid %.0f hi %.0f voiceRMS %.0f'%(s//60,s%60,n/10,cen[m].mean(),lo[m].mean(),mid[m].mean(),hi[m].mean(),20*np.log10(np.sqrt((vm**2).mean())+1e-9)))
