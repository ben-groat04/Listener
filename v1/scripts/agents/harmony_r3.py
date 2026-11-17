import numpy as np, librosa, json
d='data/video1/stems_raw/htdemucs/song/'
def cls(f,t0,t1):
    y,sr=librosa.load(d+f+'.wav',sr=22050,offset=t0,duration=t1-t0,mono=True)
    C=np.abs(librosa.cqt(y,sr=sr,fmin=librosa.note_to_hz('C1'),n_bins=84*3,bins_per_octave=36))**2
    p=C.mean(1); n=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    pc=np.zeros(12)
    for i,v in enumerate(p): pc[(round(i/3))%12]+=v
    pc/=pc.max(); fr=np.fft.rfftfreq(len(y)*4,1/sr); S=np.abs(np.fft.rfft(y*np.hanning(len(y)),len(y)*4))
    m=(fr>30)&(fr<400); pk=fr[m][np.argmax(S[m])]
    return {n[i]:round(float(pc[i]),2) for i in np.argsort(-pc)[:6]}, round(float(pk),1)
for f in ['other','bass','vocals']:
    for a,b in [(1*60+57,1*60+58.2),(1*60+46.6,1*60+48.4),(1*60+43,1*60+46),(1*60+49,1*60+53)]:
        print(f,a,b,cls(f,a,b))
