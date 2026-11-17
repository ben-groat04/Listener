import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'bass.wav',sr=22050,mono=True)
def pk(a,b):
    seg=y[int(a*sr):int(b*sr)]
    if np.sqrt(np.mean(seg**2))<2e-3: return '-'
    S=np.abs(np.fft.rfft(seg*np.hanning(len(seg)),n=2**17)); f=np.fft.rfftfreq(2**17,1/sr)
    m=(f>30)&(f<200); x=f[m][np.argmax(S[m])]; return librosa.hz_to_note(x)
for rng in [(0,16),(36,50),(72,88),(96,112),(150,170)]:
    print(rng,' '.join(f'{int(t//60)}:{int(t%60):02d}={pk(t,t+1.5)}' for t in np.arange(rng[0],rng[1],1.5)))
