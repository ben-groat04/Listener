import json,numpy as np,librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/'
p=json.load(open(D+'music_views/per_second_levels.json'))
for r in p[112:142]: print(r['t'],r['dbfs'],r['width'],r['vocals'],r['drums'],r['bass'],r['other'])
for r in json.load(open(D+'music_views/chords.json')):
    if 118<r['end'] and r['start']<142: print('chord',r['start'],r['end'],r['chord'])
for r in json.load(open(D+'music_views/lead_notes.json')):
    if 118<r['end'] and r['start']<142: print('lead',r)
t=json.load(open(D+'music_views/clap_tags.json'));print(t.keys())
bt=json.load(open(D+'audio_features/beat_times.json'));print(type(bt), str(bt)[:100])
S=D+'stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False);print(sr,y.shape)
seg=y[:,int(120*sr):int(140*sr)];print('peak dBFS 120-140',20*np.log10(np.abs(seg).max()),'global',20*np.log10(np.abs(y).max()))
d,sr2=librosa.load(S+'drums.wav',sr=22050,mono=True)
d=d[int(120*sr2):int(140*sr2)]
lo=librosa.effects.preemphasis
# kick: low band onset
import scipy.signal as sg
b,a=sg.butter(4,150/(sr2/2),'low');k=sg.filtfilt(b,a,d)
env=librosa.onset.onset_strength(y=k,sr=sr2,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=env,sr=sr2,hop_length=256,units='time',backtrack=False)
on=on+120;print('kick onsets',np.round(on,2));ioi=np.diff(on);print('ioi',np.round(ioi,3),'median',np.median(ioi))
bs,_=librosa.load(S+'bass.wav',sr=22050,mono=True);bs=bs[int(120*sr2):int(140*sr2)]
env=librosa.onset.onset_strength(y=bs,sr=sr2,hop_length=256);bo=librosa.onset.onset_detect(onset_envelope=env,sr=sr2,hop_length=256,units='time')+120
print('bass onsets',len(bo),np.round(np.diff(bo),3))
# per-stem RMS in 1 s and 0.5s around 127.5 and 133.5
for n in['vocals','drums','bass','other']:
    x,_=librosa.load(S+n+'.wav',sr=22050,mono=True)
    r=librosa.feature.rms(y=x,frame_length=2205,hop_length=1102)[0]
    tt=np.arange(len(r))*1102/22050
    print(n,[ (round(a,1),round(20*np.log10(r[(tt>=a)&(tt<a+1)].mean()+1e-9),1)) for a in range(118,142)])
    sc=librosa.feature.spectral_centroid(y=x[int(120*22050):int(140*22050)],sr=22050)[0];print(n,'centroid 120-140',sc.mean())
