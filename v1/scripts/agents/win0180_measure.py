import json,numpy as np,librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/'
p=json.load(open(D+'music_views/per_second_levels.json'))
for r in p[172:206]: print(r['t'],r['dbfs'],r['width'],r['vocals'],r['drums'],r['bass'],r['other'])
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False)
m=y if y.ndim==1 else y.mean(0)
print('sr',sr,'peak 180-200 dBFS',20*np.log10(np.abs(y[...,180*sr:200*sr]).max()),'whole',20*np.log10(np.abs(y).max()))
d,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050)
o=librosa.onset.onset_detect(y=d,sr=22050,units='time',backtrack=False)
o=o[(o>178)&(o<202)]
print('drum onsets',np.round(o,2))
b,_=librosa.load(D+'stems_raw/htdemucs/song/bass.wav',sr=22050)
ob=librosa.onset.onset_detect(y=b,sr=22050,units='time')
ob=ob[(ob>178)&(ob<202)];print('bass onsets',np.round(ob,2)); print('bass IOI',np.round(np.diff(ob),2))
bt=np.array(json.load(open(D+'audio_features/beat_times.json')) if not isinstance(json.load(open(D+'audio_features/beat_times.json')),dict) else json.load(open(D+'audio_features/beat_times.json'))['beats'])
bt=bt[(bt>178)&(bt<202)];print('beat IOI med',np.median(np.diff(bt)),60/np.median(np.diff(bt)))
# spectral centroid & bands per second
S=np.abs(librosa.stft(m,n_fft=2048))
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
for t in [181,185,190,193,195,196,200]:
    a=S[:,int(t*sr/512):int((t+1)*sr/512)].mean(1)
    print(t,'cent',round((f*a).sum()/a.sum()),'>4k share',round(a[f>4000].sum()/a.sum(),3))
