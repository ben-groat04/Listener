import librosa,numpy as np,sys
y,sr=librosa.load('/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/vocals.wav',sr=16000)
for a,b in [(10,19),(20,31),(41,43),(51,56),(63,66),(79,86),(135,150),(155,159),(164,168)]:
    seg=y[int(a*sr):int(b*sr)]
    f0,v,p=librosa.pyin(seg,fmin=70,fmax=400,sr=sr,frame_length=1024)
    f=f0[v&~np.isnan(f0)]
    print(a,b,len(f),np.percentile(f,[10,50,90]).round() if len(f) else None)
