import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/';S=D+'stems_raw/htdemucs/song/';sr=44100
b=sf.read(S+'bass.wav')[0].mean(1); h=int(.25*sr)
e=np.array([20*np.log10(np.sqrt(np.mean(b[i*h:(i+1)*h]**2))+1e-9) for i in range(len(b)//h)])
for n,a in [('v1',30.4),('v2',91.4),('v3',154.2)]:
    seg=e[int(a/.25):int((a+40.8)/.25)]<-40; out=[];s=None
    for i,x in enumerate(seg):
        if x and s is None:s=i
        if not x and s is not None:
            if (i-s)*.25>=1.5: out.append((round(s*.25,1),round(i*.25,1)))
            s=None
    if s is not None: out.append((round(s*.25,1),round(len(seg)*.25,1)))
    print(n,'bass-out spans (s after verse start):',out,'bass-on fraction',round(1-seg.mean(),2))
