import sys,numpy as np,soundfile as sf
d=sys.argv[1]
names={'mix':d+'/audio/song.wav'}
for s in ['vocals','drums','bass','other']: names[s]=d+f'/stems_raw/htdemucs/song/{s}.wav'
t0=float(sys.argv[2]); t1=float(sys.argv[3])
for n,p in names.items():
    x,sr=sf.read(p); 
    if x.ndim>1: x=x.mean(1)
    print(n,'dur',len(x)/sr,'peak dBFS',20*np.log10(np.abs(x).max()+1e-12))
    h=int(sr*0.01); a=int(t0*sr); b=min(int(t1*sr),len(x))
    seg=x[a:b]; k=len(seg)//h
    r=np.sqrt((seg[:k*h].reshape(k,h)**2).mean(1)); db=20*np.log10(r+1e-9)
    print(' ',' '.join(f'{t0+i*0.01:.2f}:{v:.0f}' for i,v in enumerate(db) if i%10==0 and True)[:0])
    thr=-60
    idx=np.where(db>thr)[0]
    print('  last >-60dB at',t0+(idx[-1]+1)*0.01 if len(idx) else None, ' >-80:',t0+(np.where(db>-80)[0][-1]+1)*0.01 if (db>-80).any() else None)
    # coarse 100ms table
    print('  100ms dB:',' '.join(f'{t0+i*0.1:.1f}:{db[i*10:i*10+10].mean():.0f}' for i in range(k//10)))
