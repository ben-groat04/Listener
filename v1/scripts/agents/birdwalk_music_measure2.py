import librosa, numpy as np, json
D='/home/user/Listener/v1/data/t_birdwalk/'
b,sr=librosa.load(D+'stems/bass.mp3',sr=22050)
nm=np.array(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'])
for a,e in [(14,46),(61,98),(120,130),(133,142),(158,166)]:
    seg=b[int(a*sr):int(e*sr)]
    f0,vf,_=librosa.pyin(seg,fmin=30,fmax=120,sr=sr,frame_length=4096)
    f=f0[~np.isnan(f0)]
    mid=librosa.hz_to_midi(f).round().astype(int)
    u,c=np.unique(mid,return_counts=True); o=np.argsort(-c)[:4]
    print(a,e,[(nm[u[i]%12]+str(u[i]//12-1),round(float(librosa.midi_to_hz(u[i])),1),int(c[i])) for i in o])
dr,_=librosa.load(D+'stems/drums.mp3',sr=22050)
oe=librosa.onset.onset_strength(y=dr,sr=22050)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=22050,units='time')
for a,e in [(0,12.86),(12.86,47.46),(47.46,59.79),(59.79,93.79),(93.79,119.47),(119.47,131.96),(131.96,143.08),(143.08,156.41),(156.41,188)]:
    n=((on>=a)&(on<e)).sum(); print('drum onsets/s',a,e,round(n/(e-a),2))
# drum stem: spectral centroid & low/high energy ratio around 98-118
S=np.abs(librosa.stft(dr))**2; fr=librosa.fft_frequencies(sr=22050)
for a,e in [(30,45),(70,90),(98,118),(133,142),(160,175)]:
    i,j=int(a*22050/512),int(e*22050/512); s=S[:,i:j].sum(1)
    print('drums',a,e,'low<200',round(s[fr<200].sum()/s.sum(),2),'hi>5k',round(s[fr>5000].sum()/s.sum(),3))
# tempo drift: local beat intervals
bt=json.load(open(D+'audio_features/beat_times.json'))
bt=np.array(bt if isinstance(bt,list) else list(bt.values())[0])
iv=np.diff(bt); print('beat interval median',np.median(iv),'std',iv.std())
# onset autocorr at beat grid: kick pattern in sec 60-90 using drums stem; ratio of onset strength at 8th offbeats
