import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
y,sr=librosa.load(D+'vocals.wav',sr=16000)
def mf(t0,t1):
    s=y[int(t0*sr):int(t1*sr)]
    m=librosa.feature.mfcc(y=s,sr=sr,n_mfcc=13,n_fft=512,hop_length=160,n_mels=40,fmax=6000)[1:]
    return m-m.mean(1,keepdims=True)
def dtw(a,b):
    D_,wp=librosa.sequence.dtw(a,b,metric='cosine',subseq=True)
    return D_[-1,:].min()/len(b[0])
tgt=[('2:44.3-2:46.0',164.3,166.0),('2:46.5-2:48.2',166.5,168.2),('2:44.3-2:48.2',164.3,168.2)]
refs=[('0:19.0-0:23.9',19,23.9),('0:24.4-0:26.7',24.4,26.8),('0:27.9-0:31.7',27.9,31.8),('0:41.0-0:42.4',41,42.5),('0:50.8-0:56.2',50.8,56.2),('1:18.9-1:27',78.9,87),('2:24.1-2:26.5',144.1,146.5),('2:31.4-2:32.8',151.4,152.8)]
for tn,a,b in tgt:
    T=mf(a,b)
    print(tn,' '.join('%s:%.3f'%(rn,dtw(mf(c,d),T)) for rn,c,d in refs))
# 1:57 burst low-band share
for nm,(a,b) in {'1:57.0-1:58.2':(117.0,118.3),'1:46.6-1:48.4':(106.6,108.4),'1:03.5-1:05.7':(63.5,65.7),'2:24-2:26.5 (speech)':(144,146.5)}.items():
    s=y[int(a*sr):int(b*sr)];S=np.abs(np.fft.rfft(s*np.hanning(len(s))))**2;f=np.fft.rfftfreq(len(s),1/sr)
    t=S.sum();print(nm,'<150Hz %.0f%%  150-3k %.0f%%  >3k %.0f%%'%(100*S[f<150].sum()/t,100*S[(f>=150)&(f<3000)].sum()/t,100*S[f>=3000].sum()/t), 'pyin voiced',end=' ')
    f0,vf,_=librosa.pyin(s,fmin=70,fmax=400,sr=sr,frame_length=1024);print('%.2f'%np.mean(vf), 'median f0 %.0f'%np.nanmedian(f0) if np.any(~np.isnan(f0)) else '')
