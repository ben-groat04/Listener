import json,numpy as np,librosa
D='/home/user/Listener/v1/data/video2/'
L=json.load(open(D+'music_views/per_second_levels.json'))
import numpy as np
t=np.array([r['t'] for r in L]);db=np.array([r['dbfs'] for r in L]);w=np.array([r['width'] for r in L])
S={k:np.array([r[k] for r in L]) for k in['vocals','drums','bass','other']}
secs=[(0,28),(28,60),(60,88),(88,104),(104,150),(150,200),(200,216),(216,270),(270,288),(288,300)]
for a,b in secs:
    m=(t>=a)&(t<b)
    print(a,b,'dB mean %.1f max %.1f'%(db[m].mean(),db[m].max()),'width %.2f'%w[m].mean(),' '.join('%s %.1f'%(k,np.median(v[m])) for k,v in S.items()))
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False)
print(sr,y.shape)
m=y.mean(0)
print('peak',np.abs(y).max(),'rms dB',20*np.log10(np.sqrt((m**2).mean())))
import scipy.signal as ss
for a,b in [(5,25),(30,60),(100,140),(160,200),(220,260),(270,298)]:
    x=m[int(a*sr):int(b*sr)]
    f,P=ss.welch(x,sr,nperseg=8192)
    bands=[(20,60),(60,150),(150,500),(500,2000),(2000,6000),(6000,12000),(12000,20000)]
    e=[10*np.log10(P[(f>=lo)&(f<hi)].sum()+1e-20) for lo,hi in bands]
    c=librosa.feature.spectral_centroid(y=x,sr=sr).mean()
    crest=20*np.log10(np.abs(x).max()/np.sqrt((x**2).mean()))
    print(a,b,'bands',' '.join('%.0f'%(v-max(e)) for v in e),'cent %.0f crest %.1f'%(c,crest),'rolloff %.0f'%librosa.feature.spectral_rolloff(y=x,sr=sr,roll_percent=.99).mean())
# L/R correlation and mid/side
for a,b in [(5,25),(30,60),(100,140),(220,260),(270,298)]:
    l=y[0,int(a*sr):int(b*sr)];r=y[1,int(a*sr):int(b*sr)]
    M=(l+r)/2;Sd=(l-r)/2
    print(a,b,'corr %.2f'%np.corrcoef(l,r)[0,1],'S/M dB %.1f'%(10*np.log10((Sd**2).sum()/(M**2).sum())))
# stems width
for s in['vocals','drums','bass','other']:
    z,sr2=librosa.load(D+'stems_raw/htdemucs/song/%s.wav'%s,sr=None,mono=False)
    for a,b in [(100,140),(220,260)]:
        l=z[0,int(a*sr2):int(b*sr2)];r=z[1,int(a*sr2):int(b*sr2)]
        M=(l+r)/2;Sd=(l-r)/2
        print(s,a,b,'S/M %.1f'%(10*np.log10((Sd**2).sum()/((M**2).sum()+1e-12)+1e-12)),'rms %.1f'%(10*np.log10((z[:,int(a*sr2):int(b*sr2)]**2).mean()+1e-12)))
