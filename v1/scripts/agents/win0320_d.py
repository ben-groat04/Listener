import numpy as np, librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/';sr=22050
L=lambda n:librosa.load(D+'stems_raw/htdemucs/song/'+n+'.wav',sr=sr,mono=True)[0]
y=librosa.load(D+'audio/song.wav',sr=sr,mono=True)[0]
S={'mix':y,'other':L('other'),'bass':L('bass'),'vocals':L('vocals')}
def cen(x,a,b):
    s=x[int(a*sr):int(b*sr)];P=np.abs(np.fft.rfft(s))**2;f=np.fft.rfftfreq(len(s),1/sr);return round((P*f).sum()/P.sum()),round(100*P[f>2000].sum()/P.sum(),1)
def rms(x,a,b): return round(20*np.log10(np.sqrt(np.mean(x[int(a*sr):int(b*sr)]**2))+1e-9),1)
for n,x in S.items():
    print(n,'320-324',rms(x,320,324),'328-330',rms(x,328,330),'330.7-332.7',rms(x,330.7,332.7),'| cen/%>2k 328-330',cen(x,328,330),'331-333',cen(x,331,333))
# bass fade 322-325 at 0.25s
b=S['bass'];print('bass',[ (t,rms(b,t,t+.25)) for t in np.arange(322,325.5,.5)])
# other stem: tonal lines 320-329 vs 334-342 (spectral flatness)
for a,b2 in [(320,328),(334,338),(339,342.8)]:
    s=S['other'][int(a*sr):int(b2*sr)];print('other flatness',a,b2,round(float(np.mean(librosa.feature.spectral_flatness(y=s))),4))
