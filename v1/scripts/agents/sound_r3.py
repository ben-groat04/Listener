import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_cshells_cshore/'
def ld(p):
    x,sr=sf.read(p); 
    return (x.mean(1) if x.ndim>1 else x),sr
mix,sr=ld(D+'audio/song.wav')
S={k:ld(D+f'stems_raw/htdemucs/song/{k}.wav')[0] for k in['vocals','drums','bass','other']}
def spec(x,a,b,n=1<<19):
    s=x[int(a*sr):int(b*sr)]*np.hanning(int((b-a)*sr)); F=np.abs(np.fft.rfft(s,n)); f=np.fft.rfftfreq(n,1/sr); return f,F
def peaks(x,a,b,lo,hi,k=5):
    f,F=spec(x,a,b); m=(f>lo)&(f<hi); idx=np.where(m)[0]; Fm=20*np.log10(F[idx]+1e-12)
    out=[]; 
    for i in np.argsort(-Fm):
        if all(abs(f[idx[i]]-o[0])>15 for o in out): out.append((round(f[idx[i]],1),round(Fm[i],1)))
        if len(out)>=k: break
    return out
print('DRONE 0:25-0:32 other stem partials of A (110/55?)')
f,F=spec(S['other'],25,32); ref=None
for f0 in [55,110,220]:
    r=[]
    for n in range(1,9):
        m=(abs(f-f0*n)<f0*n*0.02); r.append(round(20*np.log10(F[m].max()+1e-12),1))
    print(f0,r)
print('mix peaks 25-32 (40-1500):',peaks(mix,25,32,40,1500,8))
print('TONE 1-1.7k mix:')
for a,b in[(3:=210,215),(215,225),(240,250),(256,266),(276,286),(312,314),(332,342)]:
    print(a,b,peaks(mix,a,b,900,1800,3))
print('4:36-4:46 mix 300-1800',peaks(mix,276,286,300,1800,5))
print('2:22-2:24 other 150-400',peaks(S['other'],142,144,150,400,4),'vocals',peaks(S['vocals'],142,144,150,1000,4),'mix',peaks(mix,142,144,150,400,4))
# 5:32-5:37 vocals vs other spectrum correlation (log bands)
ed=np.geomspace(100,8000,25)
def band(x,a,b):
    f,F=spec(x,a,b,1<<18); return np.array([10*np.log10((F[(f>=ed[i])&(f<ed[i+1])]**2).sum()+1e-20) for i in range(24)])
v=band(S['vocals'],332,337);o=band(S['other'],332,337);m=band(mix,332,337)
print('corr vocals-other',np.corrcoef(v,o)[0,1],'vocals-mix',np.corrcoef(v,m)[0,1])
# residual: vocals minus scaled other
print('vocals-minus-other dB per band',np.round(v-o,0))
# low drum: 50-80Hz mix 20ms RMS during 2:00-2:30 vs drum stem
from scipy.signal import butter,sosfilt
def lo(x,a,b,l,h):
    s=sosfilt(butter(4,[l,h],'band',fs=sr,output='sos'),x[int(a*sr):int(b*sr)]); return 20*np.log10(np.sqrt((s**2).mean())+1e-12)
for nm in['drums','bass','other']:
    print(nm,'50-80Hz 2:00-2:30',round(lo(S[nm],120,150,50,80),1),'80-150',round(lo(S[nm],120,150,80,150),1))
print('mix 50-80',round(lo(mix,120,150,50,80),1))
# drum stem 2:22 pulse?
from scipy.signal import hilbert
e=np.abs(hilbert(S['drums'][int(142*sr):int(144.5*sr)])); 
print('drums stem 142-144.5 env 50ms dB',[round(20*np.log10(e[i:i+2205].mean()+1e-9),0) for i in range(0,len(e)-2205,int(0.2*sr))])
