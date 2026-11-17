import numpy as np,soundfile as sf,librosa
B='/home/user/Listener/v1/data/t_cshells_cshore/'
v,sr=sf.read(B+'stems_raw/htdemucs/song/vocals.wav');v=v.mean(1)
v=librosa.resample(v,orig_sr=sr,target_sr=16000);sr=16000
for a,b in [(141.5,146.5),(224,226),(227.5,229.5),(296,298),(312,313.5),(330.5,336),(336,343)]:
    x=v[int(a*sr):int(b*sr)]
    f0,vf,vp=librosa.pyin(x,fmin=70,fmax=500,sr=sr,frame_length=1024,hop_length=160)
    on=librosa.onset.onset_detect(y=x,sr=sr,hop_length=160,units='time')
    e=librosa.feature.rms(y=x,hop_length=160)[0]
    # syllable-rate: modulation spectrum 2-10 Hz peak
    ee=e-e.mean();F=np.abs(np.fft.rfft(ee));fr=np.fft.rfftfreq(len(ee),.01)
    m=(fr>1)&(fr<12);pk=fr[m][F[m].argmax()]
    print(a,b,'voiced frac',round(float(np.nanmean(vf)),2),'f0 median',None if np.all(np.isnan(f0)) else round(float(np.nanmedian(f0))),'f0 range',None if np.all(np.isnan(f0)) else (round(float(np.nanpercentile(f0,10))),round(float(np.nanpercentile(f0,90)))),'onsets',len(on),'mod peak Hz',round(pk,2))
