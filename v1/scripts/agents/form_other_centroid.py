import numpy as np, librosa
S='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
for n in ['other','drums']:
    y,sr=librosa.load(S+n+'.wav',sr=22050,mono=True)
    c=librosa.feature.spectral_centroid(y=y,sr=sr,hop_length=512)[0]; t=librosa.times_like(c,sr=sr,hop_length=512)
    print(n,' '.join('%d:%02d=%.0f'%(s//60,s%60,c[(t>=s)&(t<s+5)].mean()) for s in list(range(95,125,5))+list(range(160,185,5))))
