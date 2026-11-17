import numpy as np, librosa, json
D='data/video2/'
def band(p,lo,hi,t0,t1,step=0.5):
    y,sr=librosa.load(p,sr=22050,mono=True,offset=t0,duration=t1-t0)
    S=np.abs(librosa.stft(y,n_fft=2048,hop_length=512))**2
    f=librosa.fft_frequencies(sr=sr,n_fft=2048); m=(f>=lo)&(f<hi)
    e=S[m].sum(0); fr=int(step*sr/512)
    return [round(10*np.log10(e[i:i+fr].mean()+1e-12),0) for i in range(0,len(e)-fr+1,fr)]
for n in ['vocals','other','bass','drums']:
    print(n,band(D+f'stems_raw/htdemucs/song/{n}.wav',4000,8000,40.5,44))
print('mix',band(D+'audio/song.wav',4000,8000,40.5,44))
def rms(p,t0,t1,h=0.25):
    y,sr=librosa.load(p,sr=22050,mono=True,offset=t0,duration=t1-t0)
    n=int(h*sr);return [round(20*np.log10(np.sqrt((y[i:i+n]**2).mean())+1e-9),0) for i in range(0,len(y)-n+1,n)]
for n in ['bass','drums']: print(n,'hole',rms(D+f'stems_raw/htdemucs/song/{n}.wav',83.5,89))
print('vocals 3:24',rms(D+'stems_raw/htdemucs/song/vocals.wav',203.5,210))
print('end drums',rms(D+'stems_raw/htdemucs/song/drums.wav',299.5,304))
print('end mix',rms(D+'audio/song.wav',299.5,304))
