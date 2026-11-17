import librosa,numpy as np
from scipy.ndimage import median_filter
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
N=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
sr=22050;hop=512
ld=lambda n:librosa.load(D+n+'.wav',sr=sr)[0]
bass,oth,vo=ld('bass'),ld('other'),ld('vocals')
C=librosa.feature.chroma_cqt(y=bass,sr=sr,hop_length=hop,fmin=32.7,n_octaves=4)
t=librosa.frames_to_time(np.arange(C.shape[1]),sr=sr,hop_length=hop)
r=median_filter(C.argmax(0),size=43)
ch=[i for i in range(1,len(r)) if r[i]!=r[i-1]]
oe=librosa.onset.onset_strength(y=bass,sr=sr,hop_length=256);ot=librosa.frames_to_time(np.arange(len(oe)),sr=sr,hop_length=256)
print('A. bass root changes: time, root, snapped onset, phase in 2s bar from 0.14, phase in beats(0.5)')
rows=[]
for i in ch:
    T=t[i]
    if not 28<T<285: continue
    m=(ot>T-0.6)&(ot<T+0.6)
    s=ot[m][oe[m].argmax()]
    rows.append((T,N[r[i]],s,((s-0.14)%2.0)))
for a in []: print('%.2f %s snap %.2f ph %.2f'%a)
def reg(a,b):
    p=np.array([x[3] for x in rows if a<=x[0]<b]);
    if len(p): print('region %d-%d n=%d phase median %.2f mean-circ %.2f'%(a,b,len(p),np.median(p),(np.angle(np.exp(2j*np.pi*p/2.0).mean())%(2*np.pi))/(2*np.pi)*2.0))
for a,b in [(28,88),(89,157),(157,285)]: reg(a,b)
# B. other-stem octave distribution 2:40-3:00
Cq=np.abs(librosa.cqt(oth,sr=sr,hop_length=hop,fmin=65.4,n_bins=72,bins_per_octave=12))
for a,b in [(2*60+38,2*60+46),(2*60+51,2*60+59),(3*60+30,3*60+38),(4*60+10,4*60+18)]:
    f0=int(a*sr/hop);f1=int(b*sr/hop);e=Cq[:,f0:f1].mean(1)
    oc=np.array([e[k*12:(k+1)*12].sum() for k in range(6)]);oc=oc/oc.sum()
    pc=np.zeros(12)
    for k in range(72):pc[(k+0)%12]+=e[k]  # fmin C2
    pc/=pc.max()
    print('B other %d-%d octave share C2..C7:'%(a,b),np.round(oc,2),'top pcs',[N[i] for i in pc.argsort()[::-1][:4]],np.round(np.sort(pc)[::-1][:4],2))
# C. voice pitch vs bass root
for a,b in [(250,256),(284,289)]:
    y=vo[int(a*sr):int(b*sr)];f0,v,p=librosa.pyin(y,fmin=150,fmax=800,sr=sr,hop_length=512)
    tt=librosa.times_like(f0,sr=sr,hop_length=512)+a
    print('C voice %d-%d voiced %.2f'%(a,b,v.mean()))
    for k in range(a,b):
        m=(tt>=k)&(tt<k+1)&v
        rt=N[r[int((k+.5)*sr/hop)]]
        if m.sum()>3: print('  %d:%02d voice med %s (%.0fHz) n=%d | bass root %s'%(k//60,k%60,N[int(np.round(librosa.hz_to_midi(np.median(f0[m]))))%12],np.median(f0[m]),m.sum(),rt))
        else: print('  %d:%02d voice none | bass %s'%(k//60,k%60,rt))
# D. bass root histogram by region incl C#/F#; and 1:57-2:25 roots
for a,b in [(117,145),(28,150),(156,285)]:
    s=r[int(a*sr/hop):int(b*sr/hop)];h=np.bincount(s,minlength=12)/len(s)
    print('D bass root share %d-%d:'%(a,b),{N[i]:round(h[i],2) for i in range(12) if h[i]>0.01})
# E. third D vs D# in other stem and in bass-free sense
Cc=librosa.feature.chroma_cqt(y=oth,sr=sr,hop_length=hop)
for name,a,b in [('0:53-0:56',53,56),('0:36-0:40 D bar',36,40),('2:20-2:24 B bar',140,144),('3:12-3:16 B bar',192,196),('4:17-4:20',257,260),('4:05-4:09',245,249),('4:52-4:58',292,298)]:
    c=Cc[:,int(a*sr/hop):int(b*sr/hop)].mean(1);c/=c.max()
    print('E other %s: B %.2f D %.2f D# %.2f F# %.2f A %.2f E %.2f G %.2f C# %.2f'%(name,c[11],c[2],c[3],c[6],c[9],c[4],c[7],c[1]))
