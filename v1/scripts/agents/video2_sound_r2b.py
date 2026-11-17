import numpy as np, librosa
from scipy.signal import butter, sosfilt
D='/home/user/Listener/v1/data/video2/'; sr=22050
oth,_=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=sr,mono=False)
mix,_=librosa.load(D+'audio/song.wav',sr=sr,mono=False)
def bp(y,lo,hi): return sosfilt(butter(4,[lo,hi],'bp',fs=sr,output='sos'),y,axis=-1)
def db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
for a in [5,40,100,150,200,250]:
    s=oth[:,int(a*sr):int((a+8)*sr)]
    r=[]
    for lo,hi in [(80,300),(300,1000),(1000,4000),(4000,9000)]:
        b=bp(s,lo,hi); r.append(round(float(np.corrcoef(b[0],b[1])[0,1]),2))
    # mono fold loss
    m=(s[0]+s[1])/2; loss=db(s)-db(m)
    print(a,'other corr by band',r,'mono fold dB change',round(db(m)-db(s),1))
for a in [5,100,200]:
    s=mix[:,int(a*sr):int((a+8)*sr)]; m=(s[0]+s[1])/2
    print(a,'mix mono fold dB change',round(db(m)-db(s),1))
