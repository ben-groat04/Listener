import json,numpy as np,librosa
d='/home/user/Listener/v1/data/t_cshells_cshore/'
p=json.load(open(d+'music_views/per_second_levels.json'))
for r in p:
    if 134<=r['t']<=162: print(r['t'],r['dbfs'],r['width'],r['vocals'],r['drums'],r['bass'],r['other'])
y,sr=librosa.load(d+'audio/song.wav',sr=None,mono=False)
m=y.mean(0) if y.ndim>1 else y
print('sr',sr,'peak all dBFS',20*np.log10(abs(y).max()),'peak window',20*np.log10(abs(y[...,int(140*sr):int(160*sr)]).max()))
dr,_=librosa.load(d+'stems_raw/htdemucs/song/drums.wav',sr=22050)
on=librosa.onset.onset_detect(y=dr,sr=22050,units='time',backtrack=False)
on=on[(on>=138)&(on<=162)]
print('drum onsets',np.round(on,2).tolist())
bs,_=librosa.load(d+'stems_raw/htdemucs/song/bass.wav',sr=22050)
bo=librosa.onset.onset_detect(y=bs,sr=22050,units='time')
bo=bo[(bo>=138)&(bo<=162)]
print('bass onsets',np.round(bo,2).tolist());print('bass IOI med',np.median(np.diff(bo)))
# kick: low band of drums
import scipy.signal as ss
sos=ss.butter(4,150,'low',fs=22050,output='sos');k=ss.sosfilt(sos,dr)
ko=librosa.onset.onset_detect(y=k,sr=22050,units='time')
ko=ko[(ko>=140)&(ko<=160)];ioi=np.diff(ko)
print('kick onsets',np.round(ko,2).tolist());print('kick IOI med',np.median(ioi),'bpm',60/np.median(ioi)*1)
g=np.arange(ko[0],160,np.median(ioi));
dev=[min(abs(x-g)) for x in ko];print('kick dev from grid ms mean',np.mean(dev)*1000,'max',max(dev)*1000)
b=json.load(open(d+'audio_features/beat_times.json'));print(str(b)[:100])
