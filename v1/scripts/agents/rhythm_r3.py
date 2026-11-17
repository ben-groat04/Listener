import numpy as np, librosa
exec(open('rhythm_r2.py').read().split('# fit grid')[0])
P=0.1923; ph=0.16
np.set_printoptions(precision=2,suppress=True,linewidth=220)
# absolute per-slot peak onset strength, normalised by the band's own 95th percentile of peaks
def prof(o,t0,t1,mod=16):
    pr=np.zeros(mod);n=np.zeros(mod)
    for j in range(int(np.ceil((t0-ph)/P)),int((t1-ph)/P)):
        i=int((ph+j*P)*fr); pr[j%mod]+=o[max(i-1,0):i+2].max(); n[j%mod]+=1
    return pr/np.maximum(n,1)
for nm,o in [('kick',ok),('mid',om),('hat',oh)]:
    ref=np.percentile(o[(t>3)&(t<165)],99.5)
    print(nm,'abs/ref per slot, 3-33',prof(o,3,33)/ref); print(nm,'abs/ref 100-115',prof(o,100,115)/ref); print(nm,'abs/ref 121-158',prof(o,121,158)/ref)
# drums stem around sub drops
env=lambda y,w=0.02: 20*np.log10(np.sqrt(np.convolve(y**2,np.ones(int(w*sr))/int(w*sr),'same'))+1e-9)
ed=env(dr)
drops=[121.086+6.1538*k for k in range(6)]
lowd=librosa.effects.preemphasis(dr)
S=np.abs(librosa.stft(dr,n_fft=1024,hop_length=hop)); f=librosa.fft_frequencies(sr=sr,n_fft=1024)
klow=S[(f>=40)&(f<120)].sum(0)
for d in drops:
    i=int(d*fr); w=klow[i-3:i+10]
    print('drop %.2f kick-band peak at +%.0f ms (rel %.1fx median) ; drums stem dB at drop %.1f, at +2.2s %.1f, mean %.1f'%(d,(np.argmax(w)-3)/fr*1000,w.max()/np.median(klow[(t>121)&(t<158)]),ed[int(d*sr)],ed[int((d+2.2)*sr)],ed[int(121*sr):int(158*sr)].mean()))
# hat onset density in cycle: onsets per slot in drop+2.2 +-0.2 vs elsewhere (hat band)
for d in drops[:5]:
    a=d+2.0;b=d+2.5
    print('drop+2.0..2.5 onsets (kick,mid,hat) per s', [round(float(((o[int(a*fr):int(b*fr)])>0.5*np.percentile(o,99)).sum())/0.5,1) for o in (ok,om,oh)])
