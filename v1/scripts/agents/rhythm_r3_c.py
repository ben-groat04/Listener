import numpy as np, librosa
D='/home/user/Listener/v1/data/t_dl_mirror/stems_raw/htdemucs/song/'
d,_=librosa.load(D+'drums.wav',sr=22050,mono=True)
db=librosa.amplitude_to_db(librosa.feature.rms(y=d,frame_length=441,hop_length=221)[0]+1e-6)
def seg(a,n):
    x=db[int(round(a*100)):int(round((a+n)*100))];return x-x.mean()
def best(a,n,ref,rng=0.8):
    x=seg(a,n);b=(-2,0)
    for s in range(-int(rng*100),int(rng*100)+1):
        y=seg(ref+s/100,n)
        if len(y)!=len(x):continue
        c=np.corrcoef(x,y)[0,1]
        if c>b[0]:b=(c,s/100)
    return b
L=10.137
for T,sign in ((177.54,-1),(10.62,+1)):
    print('mute at',T,'reference one loop',('earlier' if sign<0 else 'later'))
    for lo,n in ((T-3.2,3.0),(T+0.3,3.0),(T+3.5,3.0)):
        c,s=best(lo,n,lo+sign*L); print('  seg',round(lo,2),'offset vs loop-ref',s,'r',round(c,2))
    # also two loops
    for lo,n in ((T-3.2,3.0),(T+0.3,3.0)):
        c,s=best(lo,n,lo+sign*2*L,1.0); print('  2loops seg',round(lo,2),'offset',s,'r',round(c,2))
# mix level across mutes
m,_=librosa.load('/home/user/Listener/v1/data/t_dl_mirror/audio/song.wav',sr=22050,mono=True)
mdb=librosa.amplitude_to_db(librosa.feature.rms(y=m,frame_length=221,hop_length=110)[0]+1e-6)
for T in (10.62,177.54):
    i=int(T*200); print(T,'mix 5ms dB',np.round(mdb[i-8:i+10],0))
