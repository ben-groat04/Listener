import sys,librosa,numpy as np
f,lo,hi=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
y,sr=librosa.load(f,sr=22050,offset=lo,duration=hi-lo)
o=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False)
print(f.split('/')[-1],'onsets',len(o),'median IOI',round(float(np.median(np.diff(o))),3))
env=librosa.onset.onset_strength(y=y,sr=sr);t=librosa.feature.tempo(onset_envelope=env,sr=sr);print('tempo',t)
c=np.abs(librosa.stft(y)).mean(1);fr=librosa.fft_frequencies(sr=sr)
print('centroid',librosa.feature.spectral_centroid(y=y,sr=sr).mean())
