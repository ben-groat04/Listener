import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
sr=22050;P=0.1923;ph=0.16
S={k:librosa.load(D+k+'.wav',sr=sr,mono=True)[0] for k in ['bass','other','drums','vocals']}
def env(y,w=0.02):
    n=int(w*sr); r=np.sqrt(np.convolve(y**2,np.ones(n)/n,'same')); return 20*np.log10(r+1e-9)
E={k:env(v) for k,v in S.items()}
def first(k,t0,t1,thr,up=True):
    e=E[k]; i0,i1=int(t0*sr),int(t1*sr)
    seg=e[i0:i1]; idx=np.where(seg>thr if up else seg<thr)[0]
    return None if len(idx)==0 else (i0+idx[0])/sr
def rep(name,t):
    if t is None: print(name,None);return
    x=(t-ph)/P; print(f'{name:28s} t={t:8.3f}  slot={x:8.2f}  slot mod16={x%16:5.2f}  bars(16slot={16*P:.3f}s) from t0.16={x/16:6.2f}')
rep('bass in ~1:40 (>-35)',first('bass',97,104,-35))
rep('bass out ~1:15 (<-45)',first('bass',72,80,-45,False))
rep('bass out ~1:55 (<-45)',first('bass',112,120,-45,False))
rep('bass cont ~2:38 (>-30)',first('bass',155,162,-30))
rep('stop start (mix drop)',None)
# stop: drums stem drop
for k in ['drums','other','bass']:
    rep('stop '+k+' <-45',first(k,166.5,169,-45,False))
    rep('after stop '+k+' >-35',first(k,168.0,170,-35))
rep('other jump ~1:27 (>-30)',first('other',85,90,-30))
rep('other up 2:14 (>-24)',first('other',132,136,-24))
rep('drums first hit',first('drums',0,2,-45))
rep('other first',first('other',0.8,3,-50))
rep('end drums <-45',first('drums',186,189,-45,False))
