import numpy as np,soundfile as sf
B='/home/user/Listener/v1/data/t_cshells_cshore/'
names={'mix':B+'audio/song.wav'}
for s in ['vocals','drums','bass','other']: names[s]=B+f'stems_raw/htdemucs/song/{s}.wav'
for k,p in names.items():
    x,sr=sf.read(p);x=x.mean(1) if x.ndim>1 else x
    nz=np.nonzero(np.abs(x)>1e-4)[0]
    last=nz[-1]/sr if len(nz) else None
    h=int(sr*.01);e=x[:len(x)//h*h].reshape(-1,h);e=20*np.log10(np.sqrt((e**2).mean(1))+1e-12)
    t=np.arange(len(e))*.01
    print(k,'dur',round(len(x)/sr,2),'last>1e-4',round(last,2),'peak dB',round(20*np.log10(abs(x).max()),1))
    for a in (338,340,341,342,343,344):
        i=(t>=a)&(t<a+1);print('  ',a,round(e[i].max(),1),round(e[i].mean(),1))
x,sr=sf.read(names['mix']);x=x.mean(1)
nz=np.nonzero(np.abs(x)>0)[0];print('last nonzero sample',nz[-1]/sr, 'first',nz[0]/sr)
