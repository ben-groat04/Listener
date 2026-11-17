import numpy as np, librosa, json
d='/home/user/Listener/v1/data/t_cshells_cshore/'
L=json.load(open(d+'music_views/per_second_levels.json'))
for r in L[150:185]: print(r['t'],r['dbfs'],r['width'],r['vocals'],r['drums'],r['bass'],r['other'])
sr=22050
def ld(n):
    y,_=librosa.load(d+'stems_raw/htdemucs/song/%s.wav'%n,sr=sr,mono=True,offset=150,duration=40);return y
mix,_=librosa.load(d+'audio/song.wav',sr=sr,mono=False,offset=150,duration=40)
print('mix peak',np.abs(mix).max(), 20*np.log10(np.abs(mix).max()))
hop=int(0.1*sr)
S={n:ld(n) for n in['vocals','drums','bass','other']}
S['mix']=mix.mean(0) if mix.ndim>1 else mix
for n,y in S.items():
    r=librosa.feature.rms(y=y,frame_length=hop*2,hop_length=hop)[0]
    db=20*np.log10(r+1e-9)
    # 1s averages from 155
    print(n,' '.join('%d:%.0f'%(150+i,np.mean(db[i*10:i*10+10])) for i in range(5,35)))
# kick onsets: drums low band
y=S['drums']
import scipy.signal as sg
b,a=sg.butter(4,150/(sr/2),'low');k=sg.filtfilt(b,a,y)
on=librosa.onset.onset_detect(y=k,sr=sr,units='time',hop_length=256,backtrack=False)
on=on+150
seg=on[(on>=160)&(on<180)]
print('kick onsets',np.round(seg,2))
ioi=np.diff(seg);print('ioi median',np.median(ioi),'bpm',60/np.median(ioi))
# bass onsets
bo=librosa.onset.onset_detect(y=S['bass'],sr=sr,units='time',hop_length=256)+150
bo=bo[(bo>=160)&(bo<180)];print('bass onsets',np.round(bo,2));print('bass ioi med',np.median(np.diff(bo)))
bt=np.array(json.load(open(d+'audio_features/beat_times.json')) if True else [])
print(type(bt),bt.shape if hasattr(bt,'shape') else '')
