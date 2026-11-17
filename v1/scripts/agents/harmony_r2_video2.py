import librosa, numpy as np
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
N=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
sr=22050;hop=512
def chroma(n):
    y,_=librosa.load(D+n+'.wav',sr=sr)
    return librosa.feature.chroma_cqt(y=y,sr=sr,hop_length=hop,n_octaves=5,fmin=librosa.note_to_hz('C1'))
cb=chroma('bass');co=chroma('other')
t=np.arange(cb.shape[1])*hop/sr
f=lambda x:'%d:%04.1f'%(x//60,x%60)
# 1 bass root changes at 0.25 s resolution
roots=[]
for t0 in np.arange(28,288,0.25):
    m=(t>=t0)&(t<t0+0.25);roots.append(N[cb[:,m].mean(1).argmax()])
ch=[];prev=None
for i,r in enumerate(roots):
    if r!=prev: ch.append((28+i*0.25,r)); prev=r
# keep runs >=2s
ev=[]
for i,(a,r) in enumerate(ch):
    e=ch[i+1][0] if i+1<len(ch) else 288
    if e-a>=2: ev.append((a,r))
print('changes',' '.join(f'{f(a)}{r}' for a,r in ev))
ph=[(a%4.0) for a,r in ev]
print('phase mod 4 s: median %.2f, spread'%np.median(ph),np.round(np.percentile(ph,[10,25,75,90]),2))
# 2 third of B bars: D vs D# in other stem over B-root bars
def prof(a,b,c=co):
    m=(t>=a)&(t<b);v=c[:,m].mean(1);return v/v.sum()
for lab,(a,b) in {'B bar 0:52.5-0:56':(52.5,56),'B bar 1:53-1:56':(113,116),'B bar 2:21-2:24':(141,144),'B bar 3:00.5-3:04':(180.5,184),'Em bar 0:29-0:32':(29,32),'4:50-4:59 pad':(290,299),'0:00-0:08':(0,8)}.items():
    v=prof(a,b);o=np.argsort(-v)[:5]
    print(lab,' '.join(f'{N[i]}{v[i]:.2f}' for i in o),'| D#%.3f D%.3f F#%.2f F%.3f A#%.3f'%(v[3],v[2],v[6],v[5],v[10]))
# 3 chord (other-stem) at voice bursts 4:40.6..4:58.7 each 2 s
for s in np.arange(280.6,299,2.0):
    v=prof(s,s+1.5);o=np.argsort(-v)[:4];print(f(s),' '.join(f'{N[i]}{v[i]:.2f}' for i in o),end=' ; ')
print()
# 4 A-bar and D-bar in B-A-D loop: other-stem chroma
for lab,(a,b) in {'A 3:00.5+4':(184.5,188),'D 3:05':(189,192),'B 3:12.5':(192.5,196)}.items():
    v=prof(a,b);o=np.argsort(-v)[:4];print(lab,' '.join(f'{N[i]}{v[i]:.2f}' for i in o))
# 5 intro: mono-sum vs L/R chroma
import soundfile as sf
x,s=sf.read('/home/user/Listener/v1/data/video2/audio/song.wav')
print(x.shape,s)
for lab,sig in {'mid':x.mean(1),'L':x[:,0],'R':x[:,1],'side':(x[:,0]-x[:,1])/2}.items():
    y=librosa.resample(sig[:int(8*s)].astype(float),orig_sr=s,target_sr=sr)
    c=librosa.feature.chroma_cqt(y=y,sr=sr,n_octaves=5,fmin=librosa.note_to_hz('C1')).mean(1);c/=c.sum()
    o=np.argsort(-c)[:4];print('intro 0-8',lab,' '.join(f'{N[i]}{c[i]:.2f}' for i in o))
