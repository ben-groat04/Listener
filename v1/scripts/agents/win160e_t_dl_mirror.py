import numpy as np, soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/'
fs=44100;T0,T1=158,183
S={k:sf.read(D+f'stems_raw/htdemucs/song/{k}.wav')[0].mean(1)[T0*fs:T1*fs] for k in ['drums','bass','vocals','other']}
mix=sf.read(D+'audio/song.wav')[0].mean(1)[T0*fs:T1*fs]
def db(x): return 20*np.log10(np.sqrt((x**2).mean())+1e-9)
env=np.sqrt(np.convolve(S['bass']**2,np.ones(2205)/2205,'same'));e=20*np.log10(env+1e-9)
on=e>-48
# smooth: close gaps <0.3s
idx=np.flatnonzero(np.diff(on.astype(int)));t=idx/fs+T0
st=[];cur=None
for i,s in zip(idx,np.sign(np.diff(on.astype(int)))[idx]):pass
ons=[x/fs+T0 for x in np.flatnonzero(np.diff(on.astype(int))==1)];offs=[x/fs+T0 for x in np.flatnonzero(np.diff(on.astype(int))==-1)]
runs=[]
for a in ons:
    b=[o for o in offs if o>a];b=b[0] if b else T1
    if runs and a-runs[-1][1]<0.6: runs[-1][1]=b
    else: runs.append([a,b])
print('bass runs',[(round(a,2),round(b,2)) for a,b in runs])
def seg(a,b):
    return {k:round(db(v[int((a-T0)*fs):int((b-T0)*fs)]),1) for k,v in {**S,'mix':mix}.items()}
bounds=[]
for a,b in runs:
    if 160.5<a<181: bounds.append(('in',a))
    if 160<b<181: bounds.append(('out',b))
for kind,t in bounds:
    print(kind,round(t,2),'pre1s',seg(t-1,t),'post1s',seg(t,t+1))
