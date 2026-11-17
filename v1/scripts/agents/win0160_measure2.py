import numpy as np, soundfile as sf, librosa, scipy.signal as ss, json
D='/home/user/Listener/v1/data/t_birdwalk/'
sr=44100
dr,_=sf.read(D+'stems_raw/htdemucs/song/drums.wav'); dr=dr.mean(1)
bs,_=sf.read(D+'stems_raw/htdemucs/song/bass.wav'); bs=bs.mean(1)
mix,_=sf.read(D+'audio/song.wav'); mm=mix.mean(1)
bt=json.load(open(D+'audio_features/beat_times.json'));print(str(bt)[:100])
lo=ss.sosfilt(ss.butter(4,120,'low',fs=sr,output='sos'),dr)
for a,b in [(160,167),(170,176.5),(167,170)]:
    x=lo[int(a*sr):int(b*sr)]
    o=librosa.onset.onset_detect(y=x,sr=sr,units='time',delta=0.2)+a
    print(a,b,'kick',np.round(o,2),'ioi',np.round(np.diff(o),2))
# bass note onsets / hold
for a,b in [(170,176)]:
    x=bs[int(a*sr):int(b*sr)]
    o=librosa.onset.onset_detect(y=x,sr=sr,units='time')+a; print('bass on',np.round(o,2))
# band energy of mix above 8k vs total, vocal vs full
S=np.abs(librosa.stft(mm[160*sr:180*sr],n_fft=4096))**2; f=librosa.fft_frequencies(sr=sr,n_fft=4096)
tot=S.sum(); 
for lo_,hi in [(0,150),(150,1000),(1000,4000),(4000,8000),(8000,22050),(16000,22050)]:
    print(lo_,hi,round(10*np.log10(S[(f>=lo_)&(f<hi)].sum()/tot),1))
# periodicity: autocorr of mix onset envelope for loop regularity
oe=librosa.onset.onset_strength(y=mm[160*sr:180*sr],sr=sr); ac=librosa.autocorrelate(oe-oe.mean()); ac/=ac[0]
hop=512/sr; lags=np.arange(len(ac))*hop
m=(lags>0.3)&(lags<6); i=np.argsort(ac*m)[-5:]; print('ac peaks',[(round(lags[j],2),round(ac[j],2)) for j in i])
# 10ms envelope: sweep 2:56.5-2:59 vocals band
# mix peak per sub-window
for a in range(160,180,5): print(a,20*np.log10(np.abs(mix[a*sr:(a+5)*sr]).max()))
# clipping count
print('samples >=0.999', int((np.abs(mix[160*sr:180*sr])>=0.999).sum()))
