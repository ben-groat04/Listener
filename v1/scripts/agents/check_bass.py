import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/video1/'
b,sr=sf.read(D+'stems_raw/htdemucs/song/bass.wav');b=b.mean(1)
def pk(a,c):
    s=b[int(a*sr):int(c*sr)]*np.hanning(int((c-a)*sr));N=1<<19
    F=np.abs(np.fft.rfft(s,N));f=np.fft.rfftfreq(N,1/sr);m=(f>35)&(f<150)
    idx=np.argsort(F*m)[::-1];top=[];
    for i in idx:
        if all(abs(f[i]-t)>4 for t in top): top.append(f[i])
        if len(top)==3:break
    return [round(t,1) for t in top]
for a in [158.5,160,162,164,166,168.5,172,176,180,184]: print(a,pk(a,a+2))
print('1:41',pk(101,104),'1:50',pk(108,111))
