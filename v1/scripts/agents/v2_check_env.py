import librosa,numpy as np,sys
P='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
hop=512
def env(n):
    y,sr=librosa.load(P+n+'.wav',sr=22050,mono=True)
    r=librosa.feature.rms(y=y,frame_length=2048,hop_length=hop)[0]
    return 20*np.log10(r+1e-9), sr/hop
import json
res={}
for n in ['bass','drums','vocals','other']:
    res[n]=env(n)
def show(n,a,b,step=0.1):
    e,fr=res[n]
    print(n,' '.join(f"{t:.2f}:{e[int(t*fr)]:.0f}" for t in np.arange(a,b,step)))
if __name__=='__main__':
    for arg in sys.argv[1:]:
        n,a,b,s=arg.split(','); show(n,float(a),float(b),float(s))
