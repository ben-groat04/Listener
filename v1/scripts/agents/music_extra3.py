import librosa, numpy as np
y,sr=librosa.load('/home/user/Listener/v1/data/video1/audio/song.wav',sr=22050,mono=True)
# sub-bass thumps 118-153
S=np.abs(librosa.stft(y,n_fft=4096,hop_length=512)); f=librosa.fft_frequencies(sr=sr,n_fft=4096)
sub=S[(f>25)&(f<90)].sum(0); t=librosa.times_like(sub,sr=sr,hop_length=512)
m=(t>118)&(t<155); x=sub[m]; tt=t[m]
pk=librosa.util.peak_pick(x,pre_max=20,post_max=20,pre_avg=40,post_avg=40,delta=x.std()*0.8,wait=40)
print('thumps',np.round(tt[pk],1), np.round(np.diff(tt[pk]),2))
# riff: low-band onset times 20-30s and bar length via autocorr of low-band flux
low=S[(f>60)&(f<400)].sum(0); fl=np.maximum(0,np.diff(low,prepend=0))
for a,b in [(20,60),(90,108),(160,185)]:
    seg=fl[int(a*sr/512):int(b*sr/512)]; ac=np.correlate(seg-seg.mean(),seg-seg.mean(),'full')[len(seg)-1:]; lag=np.arange(len(ac))*512/sr
    pk=librosa.util.peak_pick(ac/ac[0],pre_max=5,post_max=5,pre_avg=5,post_avg=5,delta=0.02,wait=5)
    top=sorted(pk,key=lambda i:-ac[i])[:6]; print(a,b,[(round(lag[i],2),round(ac[i]/ac[0],2)) for i in top])
# centroid/lowpass sweep 105-120
cen=librosa.feature.spectral_centroid(y=y,sr=sr,hop_length=512)[0]; ct=librosa.times_like(cen,sr=sr,hop_length=512)
print('centroid 5s',[(a,int(cen[(ct>=a)&(ct<a+2)].mean())) for a in range(104,124,2)])
# stereo
y2,_=librosa.load('/home/user/Listener/v1/data/video1/audio/song.wav',sr=22050,mono=False)
L,R=y2; print('corr',np.corrcoef(L,R)[0,1],'L/R rms',np.sqrt((L**2).mean()),np.sqrt((R**2).mean()))
for a,b in [(0,15),(15,66),(75,88),(118,134),(134,159),(165,185)]:
    l=L[a*sr:b*sr];r=R[a*sr:b*sr];print(a,b,'corr',round(np.corrcoef(l,r)[0,1],2))
# dynamic range, crest, peak
print('peak',np.abs(y).max(),'rms dB',20*np.log10(np.sqrt((y**2).mean())))
r=librosa.feature.rms(y=y,frame_length=sr,hop_length=sr//2)[0]; print('short-term dB p10/p90',np.percentile(20*np.log10(r+1e-6),[10,90]))
# narration presence: 300-3400 Hz band vs time, compare to 2:44-2:48 region
for a,b in [(10,12),(13,16),(19,31),(40,43),(50,56),(79,87),(136,155),(163,168),(185,188)]:
    print('speech win',a,b,'mid rms',round(float(np.sqrt((y[a*sr:b*sr]**2).mean())),3))
r2=librosa.feature.rms(y=y,hop_length=512)[0]; t2=librosa.times_like(r2,sr=sr,hop_length=512)
for a,b in [(160,170),(184,189)]: m=(t2>=a)&(t2<b); print(a,np.round(r2[m][::12],2))
