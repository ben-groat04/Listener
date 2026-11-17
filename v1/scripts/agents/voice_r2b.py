import numpy as np, librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050
v,_=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=sr,mono=True)
f=librosa.fft_frequencies(sr=sr,n_fft=8192)
for a,b in [(141.5,143),(143,144.5),(144.5,146),(224,225.5),(312.2,312.9),(336,340)]:
    S=np.abs(librosa.stft(v[int(a*sr):int(b*sr)],n_fft=8192,hop_length=2048)).mean(1)
    idx=np.argsort(S)[::-1]; pk=[]
    for i in idx:
        if all(abs(f[i]-q)>40 for q in pk): pk.append(f[i])
        if len(pk)==6:break
    print(a,b,[round(x) for x in pk], round(20*np.log10(np.sqrt((v[int(a*sr):int(b*sr)]**2).mean())),1))
# 2:22 onset: 10ms envelope
e=librosa.feature.rms(y=v[int(141*sr):int(147*sr)],frame_length=220,hop_length=220)[0]
d=20*np.log10(e+1e-9)
print([round(x) for x in d[::25]])
