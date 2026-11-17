import librosa,numpy as np,collections
y,sr=librosa.load('/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/other.wav',sr=22050,mono=True)
def run(a,b):
    seg=y[int(a*sr):int(b*sr)]
    S=np.abs(librosa.stft(seg,n_fft=4096,hop_length=512))
    f=librosa.fft_frequencies(sr=sr,n_fft=4096)
    m=(f>150)&(f<2000)
    rms=S[m].sum(0);thr=np.percentile(rms,60)
    seq=[]
    for i in range(S.shape[1]):
        if rms[i]<thr: continue
        fr=f[m][S[m][:,i].argmax()]
        pc=int(round(12*np.log2(fr/440)))%12
        seq.append('A Bb B C Db D Eb E F Gb G Ab'.split()[pc])
    c=collections.Counter(seq);n=len(seq)
    print(a,b,{k:round(v/n,2) for k,v in c.most_common(6)})
    # transitions between successive distinct pitch classes
    t=collections.Counter(zip(seq,seq[1:]));print(' trans',[(k,v) for k,v in t.most_common(6) if k[0]!=k[1]])
for a,b in [(62,80),(100,120),(80,83),(81,84),(40,47),(147,150),(176,180)]: run(a,b)
