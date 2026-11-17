import json,numpy as np,librosa
D='/home/user/Listener/v1/data/t_birdwalk/'
S=D+'stems_raw/htdemucs/song/'
t0,t1=56,82
def ld(f):
    y,sr=librosa.load(f,sr=22050,mono=True,offset=t0,duration=t1-t0);return y,sr
out={}
for n in ['drums','bass','vocals','other']:
    y,sr=ld(S+n+'.wav')
    # 1s rms at 0.5 s hop
    h=sr//2
    r=[20*np.log10(np.sqrt(np.mean(y[i:i+sr]**2))+1e-9) for i in range(0,len(y)-sr+1,h)]
    print(n,'rms/0.5s from',t0);print(' '.join(f'{t0+i*0.5:.1f}:{v:.0f}' for i,v in enumerate(r)))
    if n in('drums','bass'):
        on=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False,delta=0.15 if n=='bass' else 0.1)+t0
        print(n,'onsets',np.round(on,2).tolist())
        out[n]=on
for n in ['drums','bass']:
    on=out[n];on=on[(on>=60)&(on<80)];d=np.diff(on);print(n,'IOI 60-80 median',np.median(d),np.round(d,2).tolist())
# band shares + width
import soundfile as sf
y,sr=sf.read(D+'audio/song.wav');print(sr,y.shape)
for a,b in [(52,59),(60,70),(70,77),(77,81),(81,88)]:
    seg=y[int(a*sr):int(b*sr)]
    m=seg.mean(1) if seg.ndim>1 else seg
    sd=(seg[:,0]-seg[:,1])/2 if seg.ndim>1 else 0*m
    F=np.abs(np.fft.rfft(m))**2;f=np.fft.rfftfreq(len(m),1/sr)
    bs=[F[(f>=lo)&(f<hi)].sum() for lo,hi in [(0,60),(60,200),(200,800),(800,3000),(3000,8000),(8000,22050)]]
    bs=np.array(bs)/sum(bs)*100
    print(a,b,'bands',np.round(bs,1),'side/mid rms',np.sqrt(np.mean(sd**2))/np.sqrt(np.mean(((seg[:,0]+seg[:,1])/2)**2)),'peak',20*np.log10(np.abs(seg).max()),'rms',20*np.log10(np.sqrt(np.mean(seg**2))))
