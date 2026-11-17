import numpy as np,librosa
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=44100
y,_=librosa.load(D+'audio/song.wav',sr=sr,offset=18,duration=24,mono=False)
print(y.shape)
m=y.mean(0) if y.ndim>1 else y
def seg(a,b):
    return m[int((a-18)*sr):int((b-18)*sr)]
for a,b in [(20,22),(22,24),(24.5,29),(32,34.5),(36,38),(38,40)]:
    x=seg(a,b);S=np.abs(np.fft.rfft(x*np.hanning(len(x))))**2;f=np.fft.rfftfreq(len(x),1/sr)
    c=np.cumsum(S)/S.sum()
    print(a,b,'roll95 %.0f roll99 %.0f'%(f[np.searchsorted(c,.95)],f[np.searchsorted(c,.99)]),'peak %.3f'%np.abs(x).max(),'crest %.1f'%(20*np.log10(np.abs(x).max()/x.std())),
      'low<200 share %.2f'%(S[f<200].sum()/S.sum()), 'top peaks',[round(f[i]) for i in np.argsort(S[(f>40)&(f<1500)])[-0:][::-1][:0]])
# partials 24.5-29
x=seg(25,29);S=np.abs(np.fft.rfft(x*np.hanning(len(x))));f=np.fft.rfftfreq(len(x),1/sr)
import scipy.signal as ss
pk,_=ss.find_peaks(S,height=S.max()*0.08,distance=int(8*len(x)/sr))
print('peaks',[(round(f[i],1),round(S[i]/S.max(),2)) for i in pk if f[i]<1500][:25])
# 10ms envelope events 29-41
hop=441;e=librosa.feature.rms(y=m,frame_length=882,hop_length=hop)[0];t=np.arange(len(e))*0.01+18
for a in (22,30,31,32,35,38):
    s=(t>=a-.5)&(t<a+1.0);print(a,'min %.1f at %.2f'%(20*np.log10(e[s].min()),t[s][e[s].argmin()]),'max %.1f at %.2f'%(20*np.log10(e[s].max()),t[s][e[s].argmax()]))
# loop regularity: autocorr of 24.9-40 chroma/envelope
ch=librosa.feature.chroma_cqt(y=m[int(6.9*sr):],sr=sr,hop_length=2048)  # from 24.9
print('chroma frames',ch.shape)
# bar-level self similarity of env 24.4 - 40
oe=librosa.onset.onset_strength(y=m[int(6.4*sr):],sr=sr,hop_length=512)
ac=librosa.autocorrelate(oe-oe.mean());ac/=ac[0];lag=np.arange(len(ac))*512/sr
r=(lag>0.3)&(lag<8);i=np.argsort(ac[r])[-5:];print('ac peaks',[(round(lag[r][j],2),round(ac[r][j],2)) for j in i])
