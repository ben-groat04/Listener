import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_cshells_cshore/'; sr=22050
y,_=librosa.load(D+'audio/song.wav',sr=sr)
import scipy.signal as sg
d,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr)
bt=np.array(json.load(open(D+'audio_features/beat_times.json')))
bt=bt[(bt>=220)&(bt<240)]; print('beats',len(bt),'median spacing',np.median(np.diff(bt)),60/np.median(np.diff(bt)))
# kick grid distance: low band onset env
b,a=sg.butter(4,120/(sr/2),'low'); k=sg.filtfilt(b,a,d)
ko=librosa.onset.onset_detect(y=k,sr=sr,hop_length=128,units='time',delta=0.3)
ko=ko[(ko>=220)&(ko<240)]
ioi=np.diff(ko);print('strong kick n',len(ko),np.round(ko,2));print('IOI median',np.median(ioi))
beat=0.488
off=[(t-bt[0])%beat for t in ko]; off=[o if o<beat/2 else o-beat for o in off]
print('offset from beat grid (ms) std',np.std(off)*1000, 'mean',np.mean(off)*1000)
# loop regularity: autocorr of mix chroma over 224-240 at lag of 1 bar (4 beats=1.95s)
ch=librosa.feature.chroma_cqt(y=y[int(224*sr):int(240*sr)],sr=sr,hop_length=512)
for bars in [1,2,4]:
    lag=int(round(bars*1.952*sr/512)); c=np.mean([np.corrcoef(ch[:,i],ch[:,i+lag])[0,1] for i in range(ch.shape[1]-lag)]); print('bar lag',bars,c)
# last 3 s end of track
dur=len(y)/sr;print('dur',dur)
