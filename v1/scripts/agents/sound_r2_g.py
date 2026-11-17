# bed harmonic-series amplitudes (other stem): partial n at n*147.9 Hz, dB relative to partial 1; chroma classes they imply
import numpy as np, soundfile as sf, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'; S=D+'stems_raw/htdemucs/song/'
x,sr=sf.read(S+'other.wav',dtype='float32'); o=x.mean(1)
names=['D','D#','E','F','F#','G','G#','A','A#','B','C','C#']
for lab,(a,b) in {'1:40-2:00':(100,120),'3:40-3:48':(220,228),'0:36-0:46':(36,46)}.items():
    f,P=ss.welch(o[int(a*sr):int(b*sr)],sr,nperseg=1<<16)
    f0=147.9; out=[]
    ref=None
    for n in range(1,13):
        m=(f>n*f0-5)&(f<n*f0+5); j=np.argmax(P*m); amp=10*np.log10(P[j]+1e-20)
        if ref is None: ref=amp
        pc=names[int(round(12*np.log2(f[j]/(146.832*1.0081))))%12]
        out.append('%d:%s %.0f'%(n,pc,amp-ref))
    print(lab,' | '.join(out))
