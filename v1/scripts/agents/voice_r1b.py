import numpy as np, librosa
y,sr=librosa.load('/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/vocals.wav',sr=16000)
S=np.abs(librosa.stft(y,n_fft=1024,hop_length=800))**2
f=librosa.fft_frequencies(sr=sr,n_fft=1024)
def band(a,b,t0,t1):
    i=slice(int(t0*20),int(t1*20)); return S[(f>=a)&(f<b),i].sum()
for t0,t1 in [(10,12.3),(19,24),(27.9,31.8),(50.8,53.2),(1*60+19,1*60+27),(2*60+24,2*60+36),(2*60+44,2*60+48)]:
    tot=band(0,8000,t0,t1)
    print(t0,t1,'<300 %.2f 300-3k %.2f 3k+ %.2f'%(band(0,300,t0,t1)/tot,band(300,3000,t0,t1)/tot,band(3000,8000,t0,t1)/tot))
    # centroid, pitch
    seg=y[int(t0*sr):int(t1*sr)]
    f0,vf,_=librosa.pyin(seg,fmin=70,fmax=400,sr=sr)
    print('  f0 median %.0f Hz voiced %.2f'%(np.nanmedian(f0) if vf.any() else 0,vf.mean()))
# quiet vocal-stem activity between -55 and -42
r=librosa.feature.rms(y=y,frame_length=16000,hop_length=16000)[0]
print([ (i,round(20*np.log10(x+1e-9))) for i,x in enumerate(r) if -58<20*np.log10(x+1e-9)<-40][:80])
