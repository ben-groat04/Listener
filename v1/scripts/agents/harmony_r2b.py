import librosa, numpy as np
D='/home/user/Listener/v1/data/video1/'
nm=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
yb,sr=librosa.load(D+'stems_raw/htdemucs/song/bass.wav',sr=22050)
yo,_=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=22050)
def peakf(y,a,b,lo=28,hi=120):
    seg=y[int(a*sr):int(b*sr)]
    S=np.abs(np.fft.rfft(seg*np.hanning(len(seg)),n=len(seg)*16)); f=np.fft.rfftfreq(len(seg)*16,1/sr)
    m=(f>lo)&(f<hi); return f[m][np.argmax(S[m])]
def cents(f,ref): return 1200*np.log2(f/ref)
for d in [121.1,127.27,133.4,139.58,145.72,151.87,158.4]:
    f=peakf(yb,d+0.3,d+1.5); 
    g=peakf(yb,d+3.2,d+5.8)
    print(f'drop {int(d//60)}:{d%60:05.2f} sub {f:.2f} Hz = {cents(f,43.654):+.0f}c vs F1 ; after: {g:.2f} Hz')
for a in [45,60,170,180,105]:
    f=peakf(yb,a,a+6); print('D bass',a,round(f,2),f'{cents(f,73.416):+.0f}c vs D2')
# other stem 1:15-1:27 in 3 s slices, and 1:33-1:38 pitch
hop=2048
C=np.abs(librosa.cqt(yo,sr=sr,hop_length=hop,fmin=librosa.note_to_hz('C2'),n_bins=180,bins_per_octave=36))
t=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=hop)
pc=np.zeros((12,C.shape[1]))
for s in range(60): pc[s%12]+=(C[3*s:3*s+3]**2).sum(0)
for a,b in [(75,78),(78,81),(81,84),(84,87),(93,96),(96,99),(172,176),(176,180),(180,184),(184,188)]:
    m=(t>=a)&(t<b); v=pc[:,m].mean(1); v/=v.max(); print(f'{int(a//60)}:{a%60:02d}',' '.join(f'{nm[i]}={v[i]:.2f}' for i in np.argsort(-v)[:6]))
# strongest peak track in other stem 1:21-1:25 (top 3 CQT bins per frame, median)
for a,b in [(81,85),(93,98)]:
    m=(t>=a)&(t<b); Cm=C[:,m]; mean=Cm.mean(1); idx=np.argsort(-mean)[:6]
    print(a,b,'top partial bins', [(round(librosa.cqt_frequencies(180,fmin=librosa.note_to_hz('C2'),bins_per_octave=36)[i],1), librosa.hz_to_note(librosa.cqt_frequencies(180,fmin=librosa.note_to_hz('C2'),bins_per_octave=36)[i])) for i in idx])
f0,vf,vp=librosa.pyin(yo,fmin=80,fmax=700,sr=sr,hop_length=1024)
tt=librosa.times_like(f0,sr=sr,hop_length=1024)
for a,b in [(81,85),(93,98),(172,186)]:
    m=(tt>=a)&(tt<b)&vf
    mid=np.round(librosa.hz_to_midi(f0[m])).astype(int) if m.sum() else []
    u,c=np.unique(mid,return_counts=True); o=np.argsort(-c)[:5]
    print('pyin other',a,b,m.sum(),[(librosa.midi_to_note(u[i]),int(c[i])) for i in o])
