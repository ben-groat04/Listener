import json,numpy as np,librosa
D='/home/user/Listener/v1/data/t_birdwalk/'
y,sr=librosa.load(D+'audio/song.wav',sr=None,mono=False,offset=38,duration=24)
m=y.mean(0); s=(y[0]-y[1])/2; mid=(y[0]+y[1])/2
h=int(sr*0.01)
def env(x): 
    n=len(x)//h; return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
e=env(mid); t=np.arange(len(e))*0.01+38
for a,b in [(46.4,46.6),(46.6,46.8),(46.8,47.0),(47.0,47.2),(47.2,47.4),(58.6,58.8),(58.8,59.0),(59.0,59.2),(59.2,59.4),(59.4,59.6)]:
    k=(t>=a)&(t<b); print('mix',a,b,round(e[k].mean(),1),round(e[k].max(),1))
# band shares
def shares(a,b):
    i=int(a*sr-38*sr); j=int(b*sr-38*sr); x=mid[i:j]
    F=np.abs(np.fft.rfft(x*np.hanning(len(x))))**2; f=np.fft.rfftfreq(len(x),1/sr)
    bs=[(0,60),(60,200),(200,800),(800,3000),(3000,8000),(8000,30000)]
    tot=F.sum(); return [round(100*F[(f>=lo)&(f<hi)].sum()/tot,1) for lo,hi in bs], round(float(np.sqrt((s[i:j]**2).sum()/(mid[i:j]**2).sum())),2)
for a,b in [(40,46.5),(47.2,58.8),(59.5,60)]: print('bands/sidemid',a,b,shares(a,b))
# stem width
for st in ['vocals','other','drums']:
    z,_=librosa.load(D+f'stems_raw/htdemucs/song/{st}.wav',sr=None,mono=False,offset=38,duration=24)
    for a,b in [(40,46.5),(47.2,58.8),(59.5,60)]:
        i=int((a-38)*sr);j=int((b-38)*sr)
        M=(z[0]+z[1])[i:j]/2;S=(z[0]-z[1])[i:j]/2
        print(st,a,b,'side/mid',round(float(np.sqrt((S**2).sum()/(M**2).sum())),2))
# kick (drums low band) onsets 
d,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050,mono=True,offset=38,duration=24)
import scipy.signal as ss
lo=ss.sosfilt(ss.butter(4,150,'low',fs=22050,output='sos'),d)
hi=ss.sosfilt(ss.butter(4,3000,'high',fs=22050,output='sos'),d)
for nm,x in [('low<150',lo),('high>3k',hi)]:
    oe=librosa.onset.onset_strength(y=x,sr=22050,hop_length=128)
    on=librosa.onset.onset_detect(onset_envelope=oe,sr=22050,hop_length=128,units='time')+38
    on=on[(on>=47.3)&(on<59.3)]; print(nm,np.round(on,2).tolist())
    if len(on)>2: print(' IOI',np.round(np.diff(on),3).tolist())
# 47.8.. hits: fit grid
on=np.array([47.8,49.3,50.84,52.44,53.95,55.52,57.11,58.68])
# refine via peak of drum env
dn=np.abs(d); eh=env(d); 
ref=[]
for o in on:
    k=(t>=o-0.1)&(t<=o+0.15); ref.append(t[k][np.argmax(eh[k])])
ref=np.array(ref); p=np.polyfit(np.arange(len(ref)),ref,1); print('refined',np.round(ref,3).tolist(),'period',p[0],'resid ms',np.round((ref-np.polyval(p,np.arange(len(ref))))*1000,0).tolist())
# lower sec 40-46.7 kick grid
b,_=librosa.load(D+'stems_raw/htdemucs/song/bass.wav',sr=22050,mono=True,offset=38,duration=24)
eb=env(b)
# other stem periodicity 47.2-58.8
o,_=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=22050,mono=True,offset=38,duration=24)
x=o[int(9.2*22050):int(20.8*22050)]
oe=librosa.onset.onset_strength(y=x,sr=22050,hop_length=256)
ac=librosa.autocorrelate(oe-oe.mean()); ac/=ac[0]; lag=np.arange(len(ac))*256/22050
k=(lag>0.1)&(lag<4); top=np.argsort(ac[k])[::-1][:6]; print('other onset env AC peaks',[(round(lag[k][i],2),round(ac[k][i],2)) for i in top])
oc=librosa.feature.chroma_cqt(y=x,sr=22050); print('other chroma mean (C..B)',np.round(oc.mean(1),2).tolist())
vv,_=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=22050,mono=True,offset=38,duration=24)
for a,b in [(40,46.5),(47.2,58.8)]:
    x=vv[int((a-38)*22050):int((b-38)*22050)]; sc=librosa.feature.spectral_centroid(y=x,sr=22050).mean(); print('vocal centroid',a,b,round(sc))
