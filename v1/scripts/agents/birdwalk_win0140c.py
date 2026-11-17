import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_birdwalk/';S=D+'stems_raw/htdemucs/song/'
sr=22050
bt=np.array(json.load(open(D+'audio_features/beat_times.json')))if isinstance(json.load(open(D+'audio_features/beat_times.json')),list) else np.array(json.load(open(D+'audio_features/beat_times.json'))['beats'])
for k in [139.62,140.75,141.86]:
    print('kick',k,'dev ms',round(1000*(k-bt[np.argmin(abs(bt-k))])))
print('beat IOI median',np.median(np.diff(bt[(bt>138)&(bt<162)])))
for name in['other','vocals']:
    y,_=librosa.load(S+name+'.wav',sr=sr,mono=True)
    for a,b in[(145,155)]:
        x=y[int(a*sr):int(b*sr)]
        oe=librosa.onset.onset_strength(y=x,sr=sr,hop_length=220)
        ac=librosa.autocorrelate(oe-oe.mean()); ac/=ac[0]
        lag=np.arange(len(ac))*220/sr
        for L0 in[0.395,0.79,1.58,3.16]:
            i=np.argmin(abs(lag-L0)); w=ac[i-4:i+5]; print(name,a,b,'autocorr near',L0,round(w.max(),2),'at',round(lag[i-4+np.argmax(w)],2))
        on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=220,units='time')+a
        print(name,'n onsets',len(on),'median IOI',np.round(np.median(np.diff(on)),3))
# bar similarity of other-stem mel, bars from 144.2 in 1.58 steps within gap
y,_=librosa.load(S+'other.wav',sr=sr,mono=True)
bars=[]
for t in np.arange(144.6,155.0-1.58,1.58):
    m=librosa.feature.melspectrogram(y=y[int(t*sr):int((t+1.58)*sr)],sr=sr,n_mels=64); m=np.log(m+1e-6)[:, :60]; bars.append(m.flatten())
c=[np.corrcoef(bars[i],bars[i+1])[0,1] for i in range(len(bars)-1)];print('other bar-to-bar corr',np.round(c,2))
y,_=librosa.load(S+'vocals.wav',sr=sr,mono=True)
bars=[]
for t in np.arange(144.6,155.0-1.58,1.58):
    m=librosa.feature.melspectrogram(y=y[int(t*sr):int((t+1.58)*sr)],sr=sr,n_mels=64); m=np.log(m+1e-6)[:, :60]; bars.append(m.flatten())
c=[np.corrcoef(bars[i],bars[i+1])[0,1] for i in range(len(bars)-1)];print('vocal bar-to-bar corr',np.round(c,2))
