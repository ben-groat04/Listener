import numpy as np, soundfile as sf, scipy.signal as ss, json
D='data/t_birdwalk/'
x,sr=sf.read(D+'audio/song.wav'); print(x.shape,sr,len(x)/sr)
m=x.mean(1) if x.ndim>1 else x
print('peak',np.abs(x).max(), 'argmax s',np.abs(x).argmax()/sr/ (1 if x.ndim==1 else 1) if x.ndim==1 else np.abs(x).max(1).argmax()/sr)
up=ss.resample_poly(x,4,1,axis=0); print('true peak 4x',np.abs(up).max(), 20*np.log10(np.abs(up).max()))
print('rms dB',20*np.log10(np.sqrt((m**2).mean())), 'crest',20*np.log10(np.abs(x).max()/np.sqrt((m**2).mean())))
# fraction samples >0.99
print('frac>0.99',(np.abs(x)>0.99).mean(), 'count',(np.abs(x)>0.999).sum())
# L/R corr, mono
L,R=x[:,0],x[:,1]; print('corr LR',np.corrcoef(L,R)[0,1],'S/M dB',10*np.log10(((L-R)**2).sum()/((L+R)**2).sum()))
# bandwidth per 10s: rolloff 99% and 99.9%, level in bands
f,_=None,None
for t in range(0,188,10):
    s=m[int(t*sr):int((t+10)*sr)]
    fr,P=ss.welch(s,sr,nperseg=4096)
    c=np.cumsum(P)/P.sum()
    r95=fr[np.searchsorted(c,.95)]; r999=fr[np.searchsorted(c,.999)]
    def b(a,bb): return 10*np.log10(P[(fr>=a)&(fr<bb)].sum()/P.sum()+1e-20)
    # cutoff: highest freq with level > -90dB rel peak psd
    Pd=10*np.log10(P+1e-20); cut=fr[np.where(Pd>Pd.max()-80)[0].max()]
    print(t,'r95 %.0f r99.9 %.0f cut80 %.0f sub60 %.1f 60-250 %.1f 250-2k %.1f 2-6k %.1f 6-10k %.1f >10k %.1f'%(r95,r999,cut,b(0,60),b(60,250),b(250,2000),b(2000,6000),b(6000,10000),b(10000,22050)))
