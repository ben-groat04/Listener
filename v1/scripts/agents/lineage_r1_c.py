import numpy as np, librosa, soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/'; S=D+'stems_raw/htdemucs/song/'; sr=44100
v=sf.read(S+'vocals.wav')[0].mean(1)
def run(a,b,lo,hi,off):
    f0,_,_=librosa.pyin(v[int(a*sr):int(b*sr)],fmin=lo,fmax=hi,sr=sr,frame_length=4096,hop_length=256)
    ok=~np.isnan(f0); n=12*np.log2(f0[ok]/440)+69-off
    # stable-note frames: steps<0.05 st
    dev=(n-np.round(n))*100
    return len(n),round(dev.std(),1),round((abs(dev)<15).mean(),2),round((abs(dev)<10).mean(),2)
for off in (0,0.14):
    print('offset',off)
    for nm,(a,b,lo,hi) in {'hook1':(10.5,30,150,700),'hook2':(72,91,150,700),'hook4':(194,215,150,700),'v1':(40,70,100,400),'v2':(100,130,100,400),'v3':(160,190,100,400)}.items():
        print(nm,run(a,b,lo,hi,off))
