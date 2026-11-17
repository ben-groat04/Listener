import json,numpy as np,librosa
D='/home/user/Listener/v1/data/video2/'
L=json.load(open(D+'music_views/per_second_levels.json'))
import collections
print('per 20s: mix, width, vox, drum, bass, other')
for s in range(0,300,20):
    r=[x for x in L if s<=x['t']<s+20]
    f=lambda k:np.mean([x[k] for x in r])
    print(s//60,s%60,*[round(f(k),1) for k in ['dbfs','width','vocals','drums','bass','other']])
y,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=False)
m=y.mean(0) if y.ndim>1 else y
print('dur',m.size/sr, 'channels', y.shape)
S=np.abs(librosa.stft(m,n_fft=4096))**2
fr=librosa.fft_frequencies(sr=sr,n_fft=4096)
bands=[(20,60),(60,150),(150,500),(500,2000),(2000,6000),(6000,11000)]
def seg(a,b):
    i,j=int(a*sr/1024),int(b*sr/1024)
    P=S[:,i:j].sum(1);t=P.sum()
    return [round(100*P[(fr>=lo)&(fr<hi)].sum()/t,1) for lo,hi in bands]
for a,b in [(0,28),(28,42),(60,76),(100,120),(120,140),(180,200),(240,270),(280,295)]:
    print('bands%',a,b,seg(a,b), 'centroid',round(float(librosa.feature.spectral_centroid(S=np.sqrt(S[:,int(a*sr/1024):int(b*sr/1024)]),sr=sr).mean())))
# crest factor / dynamics per 20 s
for a in range(0,300,40):
    x=m[a*sr:(a+20)*sr];print('crest dB',a,round(20*np.log10(np.abs(x).max()/np.sqrt((x**2).mean())),1),'rms',round(20*np.log10(np.sqrt((x**2).mean())),1))
# L/R correlation
if y.ndim>1:
    for a,b in [(5,10),(30,38),(110,118),(200,210)]:
        l,r=y[0,a*sr:b*sr],y[1,a*sr:b*sr];print('LR corr',a,round(float(np.corrcoef(l,r)[0,1]),2))
# stem sub-bass and bass spectral
for n in ['bass','drums','other']:
    z,_=librosa.load(D+f'stems_raw/htdemucs/song/{n}.wav',sr=22050)
    Z=np.abs(librosa.stft(z,n_fft=4096))**2
    for a,b in [(40,60),(110,130),(200,220)]:
        P=Z[:,int(a*sr/1024):int(b*sr/1024)].sum(1);t=P.sum()+1e-12
        print(n,a,[round(100*P[(fr>=lo)&(fr<hi)].sum()/t,1) for lo,hi in bands])
# final hit
x=m[int(298*sr):]; print('tail rms per 0.25s',[round(20*np.log10(np.sqrt((x[i:i+sr//4]**2).mean())+1e-9),0) for i in range(0,len(x),sr//4)][:25])
