import numpy as np, soundfile as sf, scipy.signal as ss
D='/home/user/Listener/v1/data/t_dl_mirror/'
def ld(p):
    x,sr=sf.read(p); x=x.mean(1) if x.ndim>1 else x; return x,sr
S={k:ld(D+f'stems_raw/htdemucs/song/{k}.wav') for k in['vocals','drums','bass','other']}
mix,sr=ld(D+'audio/song.wav')
def env(x,w):
    n=int(sr*w); m=len(x)//n; return 20*np.log10(np.sqrt((x[:m*n].reshape(m,n)**2).mean(1))+1e-9)
# 1 ducking: 100ms frames
w=0.1
E={k:env(S[k][0],w) for k in S}; M=env(mix,w)
v=E['vocals']; act=v>-35; 
t0,t1=int(10/w),int(220/w)
for k in['other','bass','drums']:
    print(k,'voice-active mean',E[k][t0:t1][act[t0:t1]].mean().round(2),'inactive',E[k][t0:t1][~act[t0:t1]].mean().round(2))
print('mix active',M[t0:t1][act[t0:t1]].mean().round(2),'inactive',M[t0:t1][~act[t0:t1]].mean().round(2))
# per hook/verse: onset-aligned average of other, mix around vocal onsets (inactive>=1s then active)
on=[i for i in range(t0+10,t1-20) if act[i] and not act[i-10:i].any()]
print('n onsets',len(on))
for k,a in [('other',E['other']),('bass',E['bass']),('drums',E['drums']),('mix',M)]:
    seg=np.array([a[i-5:i+10]-a[i-5:i-1].mean() for i in on]); print(k,'re pre-onset mean, frames -0.5..+1.0s',np.round(np.median(seg,0),1))
# 2 vocal decay 3:33.0-3:36.5 at 50ms
x=S['vocals'][0]; e=env(x,0.05); i0=int(213/0.05)
print('vocal 50ms dB 3:33-3:36.5',np.round(e[i0:i0+70],0))
eo=env(S['other'][0],0.05);print('other',np.round(eo[i0:i0+70:2],0))
# decay slope
for a,b in[(213.5,214.5),(214.5,215.1)]:
    ia,ib=int(a/0.05),int(b/0.05); print(a,b,'slope dB/s',np.polyfit(np.arange(ia,ib)*0.05,e[ia:ib],1)[0].round(1))
# autocorr of vocal env residual for repeats at 0.635
ee=env(x,0.01)[21350:21550]; print('vocal 10ms 3:33.5-3:35.5 min',ee.min().round(0))
# 3 bass spectrum
b=S['bass'][0]; seg=b[int(60*sr):int(120*sr)]
f,P=ss.welch(seg,sr,nperseg=65536); P=10*np.log10(P+1e-20)
def band(a,c): m=(f>=a)&(f<c); return 10*np.log10((10**(P[m]/10)).sum())
tot=band(20,2000)
for a,c in[(20,30),(30,45),(45,60),(60,90),(90,130),(130,200),(200,400),(400,2000)]: print('bass',a,c,round(band(a,c)-tot,1))
# hook window bass peak
for (a,c) in[(20,30),(30,45),(45,60),(60,90),(90,130)]:
    m=(f>=a)&(f<c); print('peak',a,c,f[m][P[m].argmax()].round(1),P[m].max().round(1))
# bass vs ducking: whole-file correlation between voice env and other env over 1s
e1=env(S['vocals'][0],1.0);o1=env(S['other'][0],1.0);b1=env(S['bass'][0],1.0);m1=env(mix,1.0)
print('corr 1s vocal vs other',np.corrcoef(e1[10:215],o1[10:215])[0,1].round(2),'vs mix',np.corrcoef(e1[10:215],m1[10:215])[0,1].round(2))
# hook vocal rms
