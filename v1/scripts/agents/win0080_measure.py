import json,numpy as np,librosa,sys
D='/home/user/Listener/v1/data/t_dl_mirror/'
p=json.load(open(D+'music_views/per_second_levels.json'))
print('t dbfs width voc drums bass other')
for r in p[76:106]: print(r['t'],r['dbfs'],r['width'],r['vocals'],r['drums'],r['bass'],r['other'])
S='/home/user/Listener/v1/data/t_dl_mirror/stems_raw/htdemucs/song/'
t0,t1=78,102
y,sr=librosa.load(D+'audio/song.wav',sr=22050,offset=t0,duration=t1-t0)
print('mix peak dBFS (win)',20*np.log10(np.abs(y).max()))
dr,_=librosa.load(S+'drums.wav',sr=22050,offset=t0,duration=t1-t0)
# kick: lowpass band onsets
import scipy.signal as ss
b,a=ss.butter(4,150/(sr/2),'low'); k=ss.filtfilt(b,a,dr)
env=librosa.onset.onset_strength(y=k,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=env,sr=sr,hop_length=256,units='time',backtrack=False)+t0
print('kick onsets',np.round(on,2).tolist())
ioi=np.diff(on);print('kick IOI median',np.median(ioi), 'tempo from beats file')
bt=json.load(open(D+'audio_features/beat_times.json'));bt=np.array(bt if isinstance(bt,list) else bt.get('beats',bt))
bw=bt[(bt>=78)&(bt<=102)];print('beats',np.round(bw,2).tolist()); print('beat IOI med',np.median(np.diff(bw)))
# snare/hat band onsets
b2,a2=ss.butter(4,[2000/(sr/2),8000/(sr/2)],'band'); h=ss.filtfilt(b2,a2,dr)
env2=librosa.onset.onset_strength(y=h,sr=sr,hop_length=256)
on2=librosa.onset.onset_detect(onset_envelope=env2,sr=sr,hop_length=256,units='time')+t0
print('hi-band onsets count',len(on2), np.round(on2,2).tolist())
