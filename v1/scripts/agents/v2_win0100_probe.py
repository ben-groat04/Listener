import librosa,numpy as np,json
D='data/video2/'
y,sr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050,offset=98,duration=26)
o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)+98
print('drum onsets',np.round(o[(o>=100)&(o<120)],2).tolist())
S=np.abs(librosa.stft(y,n_fft=2048))**2;f=librosa.fft_frequencies(sr=sr,n_fft=2048)
for t in o[(o>=100)&(o<=106)]:
    i=int((t-98)*sr/512);s=S[:,i:i+3].mean(1)
    print(round(t,2),'low%.0f%% mid%.0f%% hi%.0f%%'%tuple(100*np.array([s[f<200].sum(),s[(f>=200)&(f<2000)].sum(),s[f>=2000].sum()])/s.sum()))
b=json.load(open(D+'audio_features/beat_times.json'));b=b if isinstance(b,list) else b.get('beats',b)
b=np.array(b);bb=b[(b>=100)&(b<120)];print('beats',np.round(bb,2).tolist());print('median ibi',np.median(np.diff(bb)))
for nm in ['bass','other']:
    y2,_=librosa.load(D+f'stems_raw/htdemucs/song/{nm}.wav',sr=22050,offset=100,duration=20)
    c=librosa.feature.spectral_centroid(y=y2,sr=sr)[0];print(nm,'centroid per 5s',[round(float(c[i:i+216].mean())) for i in range(0,len(c),216)])
