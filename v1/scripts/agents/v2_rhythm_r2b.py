import librosa,numpy as np
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050;ph=0.1333;P=0.49995
def L(n):return librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
def rms(y,h=256):return librosa.amplitude_to_db(librosa.feature.rms(y=y,frame_length=1024,hop_length=h)[0]+1e-9,ref=1.0),sr/h
def bp(t):return ((t-ph)/P)
for nm in ['drums','bass','other']:
    y=L(nm);db,f=rms(y)
    def first_rise(t0,t1,thr):
        a,b=int(t0*f),int(t1*f);d=db[a:b]
        base=np.median(db[a:a+int(0.3*f)])
        for i in range(len(d)):
            if d[i]>base+thr: return (a+i)/f
    print(nm)
    for lab,(t0,t1,thr) in {'1:28.5 re-entry':(86,90,20),'1:41 swell':(99,103,6),'0:28 entry':(26.5,30,15),'1:04':(62,66,15)}.items():
        t=first_rise(t0,t1,thr)
        if t: print('  ',lab,'t=%.3f'%t,'beat index from grid %.2f'%bp(t),'(frac beat => offset %.0f ms)'%(((bp(t)+0.5)%1-0.5)*P*1000))
y=L('drums');db,f=rms(y)
# last hits at end
a=int(298*f);seg=db[a:int(305*f)]
for i in range(1,len(seg)):
    if seg[i]-seg[i-1]>8: print('hit at %.3f beat %.2f dB %.0f'%((a+i)/f,bp((a+i)/f),seg[i]))
# drum level fall
for i in range(len(seg)-1):
    pass
tt=(a+np.arange(len(seg)))/f
for lo in (-30,-45,-60,-75):
    idx=np.where((seg<lo)&(tt>300))[0]
    print('first below',lo,'at %.2f'%tt[idx[0]] if len(idx) else None)
