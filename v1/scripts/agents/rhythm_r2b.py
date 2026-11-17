import numpy as np, librosa, scipy.signal as ss
exec(open('rhythm_r2.py').read().split('# bass-defined')[0])
print('bass quarter-note IOI median per 20 s (IOI 0.42-0.58 s)')
for a in range(100,320,20):
    sl=slice(a*sr,(a+20)*sr); bo=ons(ba[sl],30,200,0.3)+a; io=np.diff(bo); q=io[(io>.42)&(io<.58)]
    print(a,len(q),'%.3f s = %.1f BPM'%(np.median(q),60/np.median(q)) if len(q)>4 else 'few')
# drum envelope bar-lag autocorr (full drum stem, broadband onset strength)
for a,b in [(120,200),(200,260),(260,317)]:
    y=dr[a*sr:b*sr]; o=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
    o=o-o.mean(); ac=np.correlate(o,o,'full')[len(o)-1:]; ac/=ac[0]
    f=hop/sr; lags=np.arange(len(ac))*f
    out=[]
    for L in [.25,.49,.98,1.95,3.9,7.8]:
        i=int(round(L/f)); w=ac[i-4:i+5]; out.append('%.2fs:%.2f@%.3f'%(L,w.max(),lags[i-4+w.argmax()]))
    print(a,b,out)
