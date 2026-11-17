import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
sr=22050
v,_=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=sr,mono=True)
d,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=sr,mono=True)
step=60/94.0/4
b,a=ss.butter(4,[35/11025,130/11025],'band'); k=ss.filtfilt(b,a,d)
kon=librosa.onset.onset_detect(y=k,sr=sr,hop_length=64,units='time')
vo=librosa.onset.onset_detect(y=v,sr=sr,hop_length=64,units='time')
res=[]
for w0 in range(30,210,15):
    kk=kon[(kon>=w0)&(kon<w0+15)]; vv=vo[(vo>=w0)&(vo<w0+15)]
    z=np.exp(2j*np.pi*kk/step).mean(); R=abs(z); ph=np.angle(z)/(2*np.pi)*step
    zv=np.exp(2j*np.pi*(vv-ph)/step).mean()
    res.append((w0,round(R,2),round(abs(zv),2),round(np.angle(zv)/(2*np.pi)*step*1000)))
    print(w0,'kick R',round(R,2),'vocal-vs-local-kick-grid R',round(abs(zv),2),'mean offset ms',round(np.angle(zv)/(2*np.pi)*step*1000),'nvoc',len(vv))
print('mean kick R',np.mean([r[1] for r in res]),'mean vocal R',np.mean([r[2] for r in res]))
# random baseline for vocal R with n~40
rng=np.random.default_rng(0); print('random R n=40 mean',np.mean([abs(np.exp(2j*np.pi*rng.random(40)).mean()) for _ in range(2000)]))
# hook identity: envelope xcorr between hooks, 10 ms env smoothed 50 ms
hop=221
n=len(v)//hop; e=np.sqrt((v[:n*hop].reshape(n,hop)**2).mean(1)); e=20*np.log10(e+1e-6); e=np.maximum(e,-60)
def seg(s,l): return e[int(s*100):int((s+l)*100)]
def xc(a,b,maxlag=150):
    best=(-2,0)
    for L in range(-maxlag,maxlag+1):
        x=a[max(0,L):len(a)+min(0,L)]; y=b[max(0,-L):len(b)+min(0,-L)]
        m=min(len(x),len(y)); c=np.corrcoef(x[:m],y[:m])[0,1]
        if c>best[0]: best=(c,L)
    return best
starts={'h1':10.4,'h2':71.3,'h3':134.0,'h4':195.09}
for pa in ['h1','h2','h3']:
    for pb in ['h2','h3','h4']:
        if pa<pb:
            c,L=xc(seg(starts[pa],20),seg(starts[pb],20)); print(pa,pb,'env r %.2f lag %.2f s'%(c,L/100))
# first pass vs second pass inside hook 4 and hook 2
for h in ['h1','h2','h3','h4']:
    s=starts[h]; c,L=xc(seg(s,10),seg(s+10.2,10),100); print(h,'pass1 vs pass2 env r %.2f lag %.2f'%(c,L/100))
# verse vs hook dynamics: frame-level crest of active vocal
for name,(a0,a1) in {'verse1':(31,70),'verse2':(93,130),'verse3':(156,192),'hook2':(73,90),'hook4':(197,214)}.items():
    x=v[int(a0*sr):int(a1*sr)]; ee=e[int(a0*100):int(a1*100)]; act=ee[ee>-40]
    print(name,'peak dB %.1f rms dB %.1f crest %.1f  env p10-p90 spread %.1f dB'%(20*np.log10(abs(x).max()),10*np.log10((x**2).mean()),20*np.log10(abs(x).max())-10*np.log10((x**2).mean()),np.percentile(act,90)-np.percentile(act,10)))
print('--- wide lag, 10 s passes')
passes={}
for h,s in starts.items():
    passes[h+'a']=s; passes[h+'b']=s+10.2
ks=list(passes)
import itertools
out=[]
for p,q in itertools.combinations(ks,2):
    if p[:2]==q[:2]: continue
    c,L=xc(seg(passes[p],10),seg(passes[q],10),600); out.append((round(c,2),p,q,L/100))
out.sort(reverse=True)
for o in out[:14]: print(o)
