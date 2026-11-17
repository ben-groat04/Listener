import librosa, numpy as np
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'other.wav',sr=22050)
S=np.abs(librosa.stft(y,n_fft=4096,hop_length=512)); fr=librosa.fft_frequencies(sr=sr,n_fft=4096)
for a,b in [(40,47),(60,80),(120,130),(165,170)]:
    i=slice(int(a*sr/512),int(b*sr/512)); band=(fr>150)&(fr<2000)
    X=S[band][:,i]; e=X.sum(0); sel=e>np.percentile(e,60)
    pk=fr[band][X[:,sel].argmax(0)]; m=np.round(librosa.hz_to_midi(pk)).astype(int)
    a_=pk[m%12==9]; 
    h=np.histogram(a_,bins=[150,300,600,1200,2000])[0]
    print(a,b,'A-peaks per octave band 150-300/300-600/600-1.2k/1.2-2k',h, 'median Hz of A peaks',np.median(a_))
