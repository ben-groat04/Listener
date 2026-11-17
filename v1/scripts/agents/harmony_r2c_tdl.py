import numpy as np, librosa
sr=16000
v=librosa.load('stems_raw/htdemucs/song/vocals.wav',sr=sr,mono=True)[0]
N=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
for name,(a,b) in {'v1':(31,70),'v2':(92,131),'v3':(152,190),'hook4':(194,214)}.items():
    s=v[int(a*sr):int(b*sr)]
    f,vf,p=librosa.pyin(s,fmin=70,fmax=700,sr=sr,frame_length=1024,hop_length=320)
    f=f[vf&(p>0.5)] if p is not None else f[vf]
    f=f[~np.isnan(f)]
    midi=69+12*np.log2(f/440)-0.13
    med=np.median(midi); pc=np.round(midi).astype(int)%12
    share={N[i]:round(float((pc==i).mean()),2) for i in range(12) if (pc==i).mean()>.07}
    print(name,len(f),'median Hz',round(float(np.median(f)),1),'median midi',round(float(med),2),'IQR semis',np.round(np.percentile(midi,[25,75]),2),share)
