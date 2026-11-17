import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
S=D+'stems_raw/htdemucs/song/'
dr,_=librosa.load(S+'drums.wav',sr=sr,mono=True)
vo,_=librosa.load(S+'vocals.wav',sr=sr,mono=True)
ba,_=librosa.load(S+'bass.wav',sr=sr,mono=True)
mix,_=librosa.load(D+'audio/song.wav',sr=sr,mono=True)
def env(x,ms=10):
    h=int(sr*ms/1000); n=len(x)//h
    return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
# kick onsets: low band
sos=ss.butter(4,[35,130],'bandpass',fs=sr,output='sos')
k=ss.sosfiltfilt(sos,dr)
ke=np.abs(ss.hilbert(k)); ke=ss.sosfiltfilt(ss.butter(2,40,'low',fs=sr,output='sos'),ke)
oe=np.maximum(np.diff(ke,prepend=0),0)
pk,_=ss.find_peaks(oe,height=np.percentile(oe,97),distance=int(0.06*sr))
t=pk/sr
# merge doubles <0.14 s
m=[t[0]]
for x in t[1:]:
    if x-m[-1]>0.14: m.append(x)
t=np.array(m); t=t[(t>30)&(t<215)]
print('kicks',len(t))
# global fit: grid step g, phase via circular mean at 94.0
for bpm in (93.9,94.0,94.1):
    g=60/bpm/4
    ph=np.angle(np.mean(np.exp(2j*np.pi*(t%g)/g)))/(2*np.pi)*g
    res=((t-ph+g/2)%g)-g/2
    print(bpm,'phase ms',round(ph*1000,1),'resid std ms',round(res.std()*1000,1))
g=60/94.0/4
# running phase per 20 s block (local phase of kicks wrt fixed 94.0 grid)
print('local phase per 15 s block (ms, mod g=%.1f)'%(g*1000))
ph0=None
for a in range(30,215,15):
    tt=t[(t>=a)&(t<a+15)]
    p=np.angle(np.mean(np.exp(2j*np.pi*(tt%g)/g)))/(2*np.pi)*g
    R=abs(np.mean(np.exp(2j*np.pi*(tt%g)/g)))
    print(a,round(p*1000,1),'R',round(R,2),len(tt))
# slips around stutters
for c in (132.0,145.7,193.8,73.0):
    for lab,(a,b) in (('before',(c-12,c-0.3)),('after',(c+1.5,c+13))):
        tt=t[(t>=a)&(t<b)]
        p=np.angle(np.mean(np.exp(2j*np.pi*(tt%g)/g)))/(2*np.pi)*g
        R=abs(np.mean(np.exp(2j*np.pi*(tt%g)/g)))
        print('stutter',c,lab,'phase ms',round(p*1000,1),'R',round(R,2),len(tt))
# vocal dropout edges
ve=env(vo); 
for c,w in ((72.15,1),(133.3,1),(145.7,1),(149.3,1),(193.8,1),(204.6,1),(214.2,1)):
    a=int((c-1)*100); b=int((c+2.5)*100)
    seg=ve[a:b]
    # edges: where level crosses -40 dB
    up=seg>-40
    ed=np.where(np.diff(up.astype(int))!=0)[0]
    print('vocal edges near',c,[round((a+e)/100,2) for e in ed])
# vocal dropout edges all over: list falls below -40 for >0.4s
up=ve>-40
ed=np.where(np.diff(up.astype(int))!=0)[0]/100
print('all vocal on/off edges count',len(ed))
# phase of vocal edges vs kick-fitted grid (use phase from global fit at 94.0 bpm)
ph=np.angle(np.mean(np.exp(2j*np.pi*(t%g)/g)))/(2*np.pi)*g
bar=4*g*4/4*1  # bar = 16 steps? bar=4 beats
bar=16*g
def pos(x): return (((x-ph)%bar)/g)
offs=[]
for e in ed:
    if 30<e<215: offs.append(pos(e))
offs=np.array(offs); print('vocal edge positions in 16th steps (0-16):',np.round(offs,1)[:60])
fr=offs-np.round(offs); print('frac dev std (steps)',round(fr.std(),2),'random 0.29')
# bass run starts vs grid
be=env(ba)
on=be>-40
st=np.where(np.diff(on.astype(int))==1)[0]/100
st=st[(st>5)&(st<225)]
# keep starts after >1 s off
print('bass starts n',len(st))
sel=[x for x in st if not on[max(0,int(x*100)-120):int(x*100)-2].any()]
print('bass run starts after >1.2s gap:',[(round(x,2),round(pos(x),1)) for x in sel])
# Gm run starts: drum change +/-0.5 around
de=env(dr)
for c in (16.7,77.6,137.4,199.6):
    a=int((c-2)*100);b=int((c+2)*100)
    print('Gm start',c,'drum mean -2..0',round(de[a:int(c*100)].mean(),1),'0..+2',round(de[int(c*100):b].mean(),1),'bass',round(be[a:int(c*100)].mean(),1),round(be[int(c*100):b].mean(),1),'bar pos',round(pos(c),1))
# rolls: hat band IOIs <0.1 s per 20s block; 2:55-3:00
sosh=ss.butter(4,[6000,9500],'bandpass',fs=sr,output='sos')
h=ss.sosfiltfilt(sosh,dr); he=np.abs(ss.hilbert(h)); he=ss.sosfiltfilt(ss.butter(2,100,'low',fs=sr,output='sos'),he)
ho=np.maximum(np.diff(he,prepend=0),0)
hp,_=ss.find_peaks(ho,height=np.percentile(ho,90),distance=int(0.03*sr)); ht=hp/sr
ioi=np.diff(ht)
for a,b in ((30,60),(60,120),(120,170),(170,175),(175,180),(180,215)):
    mm=(ht[:-1]>=a)&(ht[:-1]<b); x=ioi[mm]
    print('hat IOI',a,b,'n',len(x),'<0.1s %',round(100*np.mean(x<0.1),1),'0.1-0.2 %',round(100*np.mean((x>=0.1)&(x<0.2)),1),'median',round(np.median(x),3))
# triplet test: IOIs near 0.106 (triplet 16th at 94bpm = g*2/3)
tr=g*2/3
x=ioi[(ht[:-1]>30)&(ht[:-1]<215)]
print('IOI near triplet',tr,'frac within 12ms',round(np.mean(abs(x-tr)<0.012),3),' near 16th',round(np.mean(abs(x-g)<0.012),3),' near 8th',round(np.mean(abs(x-2*g)<0.012),3))
# clipped run 2:57.4
for a in (177.3,):
    seg=mix[int(a*sr):int((a+0.3)*sr)]
    print('mix peak 177.3-177.6',round(20*np.log10(abs(seg).max()),2))
    for nm,x in (('drums',dr),('bass',ba),('vox',vo)):
        s=x[int(a*sr):int((a+0.3)*sr)]; print(nm,round(20*np.log10(np.sqrt((s**2).mean())+1e-9),1), 'peak',round(20*np.log10(abs(s).max()+1e-9),1))
    print('drum kick onsets near',[round(x,2) for x in t if 176<x<179], 'pos',[round(pos(x),1) for x in t if 176<x<179])
