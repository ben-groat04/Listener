import librosa,numpy as np
y,sr=librosa.load('/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/vocals.wav',sr=22050)
for a,b in [(212,214),(228,232),(250,256),(264,271),(282,289),(290,298)]:
    f0,vf,_=librosa.pyin(y[int(a*sr):int(b*sr)],fmin=70,fmax=1000,sr=sr)
    f=f0[~np.isnan(f0)]; m=librosa.hz_to_midi(f)
    print(a,b,round(vf.mean(),2),np.round(np.percentile(f,[10,50,90]),0) if len(f) else None, sorted(set(librosa.midi_to_note(np.round(m)))) [:8] if len(f) else '')
