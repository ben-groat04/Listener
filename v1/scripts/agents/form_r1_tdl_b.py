import numpy as np, librosa, soundfile as sf
D='/home/user/Listener/v1/data/t_dl_mirror/'
S=D+'stems_raw/htdemucs/song/'
x,sr=sf.read(D+'audio/song.wav'); print(x.shape,sr,'native sample peak dBFS',20*np.log10(np.abs(x).max()),'frames',len(x),len(x)/sr)
m=x.mean(1) if x.ndim>1 else x
def env10(y,sr):
    h=int(sr*0.01); n=len(y)//h
    return 10*np.log10((y[:n*h].reshape(n,h)**2).mean(1)+1e-14)
t0=len(m)/sr-3
for name,y in [('mix',m)]+[(k,sf.read(S+k+'.wav')[0].mean(1)) for k in ['drums','bass','vocals','other']]:
    e=env10(y[int(t0*sr):],sr); idx=np.where(e>-90)[0]
    # last sound above -80dB, and above -60
    last=lambda th:(t0+ (np.where(e>th)[0].max()+1)*0.01) if (e>th).any() else None
    print(name,'last >-60',last(-60),'last >-80',last(-80),'level at last >-60 env',e[np.where(e>-60)[0].max()] if (e>-60).any() else None)
    if name=='mix':
        # peaks
        from scipy.signal import find_peaks
        p,_=find_peaks(e,height=-70,distance=5,prominence=2)
        print(' peaks (t,dB):',[(round(t0+i*0.01,2),round(e[i],1)) for i in p])
        print(' exact zero from',t0+ (np.where(np.abs(m[int(t0*sr):])>0)[0].max()+1)/sr)
# true-peak-ish: how many samples within 0.1 dB of max, mix RMS
print('mix RMS dBFS',10*np.log10((x**2).mean()))
print('stereo corr', np.corrcoef(x[:,0],x[:,1])[0,1] if x.ndim>1 else None)
# kick from drums low band
d,sr2=sf.read(S+'drums.wav'); d=d.mean(1)
import scipy.signal as ss
b,a=ss.butter(4,[40,120],'bp',fs=sr2); k=ss.filtfilt(b,a,d)
on=librosa.onset.onset_detect(y=k,sr=sr2,units='time',backtrack=False)
ioi=np.diff(on); print('n kick-band onsets',len(on),'median IOI',np.median(ioi), 'bpm eq',60/np.median(ioi))
import json
bt=np.array(json.load(open(D+'audio_features/beat_times.json')) if True else [])
print('beat json type',type(bt),bt[:5] if bt.ndim else bt)
