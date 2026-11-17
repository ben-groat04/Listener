import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_dl_mirror/'
v,sr=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=22050,mono=True)
d,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050,mono=True)
hop=221 # 10ms
def env(x):
    n=len(x)//hop
    return 20*np.log10(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-9)
ev=env(v); t=np.arange(len(ev))*0.01
# gap edges: frames where env crosses -40 with 30dB drop within 0.1 s
act=ev>-40
edges=[]
for i in range(1,len(act)):
    if act[i]!=act[i-1]: edges.append((round(t[i],2),'on' if act[i] else 'off'))
# keep gaps 0.4-2 s inside vocal region (10-215)
gaps=[]
last_off=None
for tt,k in edges:
    if tt<10 or tt>216: continue
    if k=='off': last_off=tt
    elif last_off is not None:
        g=tt-last_off
        if 0.3<g<3: gaps.append((last_off,tt,round(g,2)))
        last_off=None
print('gaps',len(gaps))
# kick grid: fit 16th grid phase from drum low-band onsets at 94.0 BPM using drums stem
step=60/94.0/4
dl=librosa.effects.preemphasis(d,coef=0)  
import scipy.signal as ss
b,a=ss.butter(4,[35/11025,130/11025],'band'); k=ss.filtfilt(b,a,d)
on=librosa.onset.onset_detect(y=k,sr=sr,hop_length=64,units='time',backtrack=False)
on=on[(on>30)&(on<215)]
# phase fit via circular mean on 16th grid
ph=2*np.pi*(on%step)/step
R=np.abs(np.exp(1j*ph).mean()); phi=np.angle(np.exp(1j*ph).mean())*step/(2*np.pi)
print('kick 16th phase',round(phi,4),'R',round(R,3),'n',len(on))
# vocal onsets in verses
vo=librosa.onset.onset_detect(y=v,sr=sr,hop_length=64,units='time')
def dev(times,ph0,st):
    r=((np.array(times)-ph0+st/2)%st)-st/2
    return r
for name,(a0,a1) in {'v1':(31,70),'v2':(92,130),'v3':(155,192),'h2':(73,90),'h3':(135,152),'h4':(197,214)}.items():
    s=vo[(vo>a0)&(vo<a1)]
    r=dev(s,phi,step); Rv=np.abs(np.exp(2j*np.pi*r/step).mean())
    print(name,'onsets',len(s),'rate',round(len(s)/(a1-a0),2),'phase conc R',round(Rv,3),'mean|dev| ms',round(1000*np.abs(r).mean(),1),'(random 40)')
# gap edges vs kick grid
for lo,hi,g in gaps:
    r=dev([lo,hi],phi,step)*1000
    bar=((lo-phi)%(step*16))/step
    print('gap',lo,hi,g,'off dev ms %.0f on dev ms %.0f'%(r[0],r[1]),'step in bar (off) %.1f (on) %.1f'%(bar,((hi-phi)%(step*16))/step))
# hook comparisons: level & pitch
f0,vf,vp=librosa.pyin(v,fmin=80,fmax=700,sr=sr,hop_length=441)
tt=np.arange(len(f0))*0.02
for name,(a0,a1) in {'h1':(12,30),'h2':(74,91),'h3':(135,152),'h4':(197,214)}.items():
    m=(tt>a0)&(tt<a1)&vf
    e=ev[(t>a0)&(t<a1)]; e=e[e>-40]
    fs=f0[m]; semis=12*np.log2(fs/440)
    print(name,'rms-active dB',round(10*np.log10((10**(e/10)).mean()),1),'f0 median',round(np.median(fs)),'p90',round(np.percentile(fs,90)),'max',round(fs.max()),'frac>480Hz',round((fs>480).mean(),3),'frac F(~350)',round(((fs>335)&(fs<365)).mean(),3),'F#(370)',round(((fs>365)&(fs<385)).mean(),3))
