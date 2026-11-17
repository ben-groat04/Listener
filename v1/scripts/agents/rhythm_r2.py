import numpy as np, librosa, scipy.signal as ss
D='/home/user/Listener/v1/data/t_cshells_cshore/stems_raw/htdemucs/song/'
sr=22050
def load(n): return librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
dr=load('drums'); ba=load('bass')
def band(x,lo,hi):
    sos=ss.butter(4,[lo,hi],btype='band',fs=sr,output='sos'); return ss.sosfilt(sos,x)
hop=110
def ons(x,lo,hi,delta=0.15):
    y=band(x,lo,hi); e=librosa.feature.rms(y=y,frame_length=441,hop_length=hop)[0]
    env=np.diff(np.log(e+1e-6),prepend=0); env=np.maximum(env,0)
    pk=librosa.util.peak_pick(env,pre_max=5,post_max=5,pre_avg=10,post_avg=10,delta=delta,wait=8)
    return pk*hop/sr
# bass-defined beat grid: bass onsets, IOI histogram by segment
for a,b in [(120,160),(160,200),(200,230),(230,260),(260,300),(300,317),(100,120)]:
    sl=slice(a*sr,b*sr)
    bo=ons(ba[sl],30,200,0.3)+a
    io=np.diff(bo)
    k=ons(dr[sl],35,110,0.3)+a
    ki=np.diff(k)
    # fit tempo from bass quarter IOIs
    q=io[(io>0.42)&(io<0.56)]
    # kick IOI hist
    h,_=np.histogram(ki,bins=[0,.1,.2,.3,.4,.45,.53,.7,.95,1.05,1.5,2.1,4])
    print(a,b,'bass n',len(bo),'qIOI med %.3f'%(np.median(q) if len(q) else 0),'n',len(q),'| kick n',len(k),'hist',h.tolist())
    # kick phase relative to bass-onset grid: for each kick, offset to nearest bass onset
    d=[ (kk-bo[np.argmin(abs(bo-kk))]) for kk in k]
    d=np.array(d); print('   kick-minus-nearest-bass ms: med %.0f, within30ms %.2f, within 60 %.2f'%(np.median(d)*1000,np.mean(abs(d)<.03),np.mean(abs(d)<.06)))
    # bar pattern: fold kicks at 4-beat period using local tempo
    T=np.median(q) if len(q) else .488
    ph=((k-bo[0])/T)%4
    h8,_=np.histogram(ph,bins=np.arange(0,4.01,.25)); print('   16th-bin kick hist over 4 beats',h8.tolist())
