import librosa, numpy as np, sys
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
names='C C# D D# E F F# G G# A A# B'.split()
def pyin_bass(a,b):
    y,sr=librosa.load(D+'bass.wav',sr=22050,offset=a,duration=b-a)
    f,v,p=librosa.pyin(y,fmin=30,fmax=200,sr=sr,frame_length=4096)
    m=librosa.hz_to_midi(f[v&~np.isnan(f)]); 
    if len(m)==0: return 'none'
    pc=np.bincount(np.round(m).astype(int)%12,minlength=12)/len(m)
    return f"n={len(m)} "+' '.join(f"{names[i]}{pc[i]:.2f}" for i in np.argsort(-pc)[:4])+f" medMIDI {np.median(m):.1f}"
for a,b in [(100,107),(107,112),(150,170),(170,176),(176,180),(184,187)]:
    print('bass',a,b,pyin_bass(a,b))
# other stem: stab pitch, peak frequency in 500-1500 Hz per frame, 0:40-0:47 and 1:00-1:20
y,sr=librosa.load(D+'other.wav',sr=22050)
S=np.abs(librosa.stft(y,n_fft=4096,hop_length=512)); fr=librosa.fft_frequencies(sr=sr,n_fft=4096)
def peaks(a,b,lo=150,hi=2000):
    i=slice(int(a*sr/512),int(b*sr/512)); band=(fr>lo)&(fr<hi)
    X=S[band][:,i]; e=X.sum(0); sel=e>np.percentile(e,60)
    pk=fr[band][X[:,sel].argmax(0)]
    m=np.round(librosa.hz_to_midi(pk)).astype(int)
    pc=np.bincount(m%12,minlength=12)/len(m)
    return ' '.join(f"{names[i]}{pc[i]:.2f}" for i in np.argsort(-pc)[:5])
for a,b in [(40,47),(60,80),(120,130),(165,170),(155,165)]:
    print('other peak pc',a,b,peaks(a,b))
# chroma of other, low-energy-weighted: C vs C#, E, in breaks vs grooves
c=librosa.feature.chroma_cqt(y=y,sr=sr)
for a,b in [(0,12),(48,59),(120,131),(144,155),(167,170),(176,180)]:
    i=slice(int(a*sr/512),int(b*sr/512)); v=c[:,i].mean(1); v/=v.max()
    print('other chroma',a,b,' '.join(f"{names[k]}{v[k]:.2f}" for k in range(12)))
