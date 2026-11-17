import numpy as np, soundfile as sf, librosa, json
D='/home/user/Listener/v1/data/t_birdwalk/'
S={}
for n in ['vocals','drums','bass','other']:
    y,sr=sf.read(D+f'stems_raw/htdemucs/song/{n}.wav'); S[n]=y.mean(1) if y.ndim>1 else y
mix,sr=sf.read(D+'audio/song.wav'); L=len(mix)/sr; print('dur',L,sr)
mm=mix.mean(1) if mix.ndim>1 else mix
def db(x): return 20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
def lv(a,b): return {k:round(db(v[int(a*sr):int(b*sr)]),1) for k,v in list(S.items())+[('mix',mm)]}
for a in range(160,180,1):
    print(a//60,a%60,lv(a,a+1))
print('peak 160-180',20*np.log10(np.abs(mix[160*sr:180*sr]).max()), 'file',20*np.log10(np.abs(mix).max()))
# drum onsets
for n in ['drums','vocals']:
    x=S[n][160*sr:180*sr]
    if n=='drums':
        import scipy.signal as ss
        lo=ss.sosfilt(ss.butter(4,150,'low',fs=sr,output='sos'),x)
        o=librosa.onset.onset_detect(y=lo,sr=sr,units='time',backtrack=False)
    else: o=librosa.onset.onset_detect(y=x,sr=sr,units='time')
    print(n,[round(t+160,2) for t in o]); print('ioi',np.round(np.diff(o),2))
# centroid by segment
for a,b in [(160,167),(167,170),(170,176.5),(176.5,180)]:
    seg=mm[int(a*sr):int(b*sr)]
    print(a,b,'cent',librosa.feature.spectral_centroid(y=seg,sr=sr).mean(),'roll',librosa.feature.spectral_rolloff(y=seg,sr=sr,roll_percent=.95).mean(), 'side/mid', db((mix[int(a*sr):int(b*sr),0]-mix[int(a*sr):int(b*sr),1])/2)-db(mm[int(a*sr):int(b*sr)]) if mix.ndim>1 else None)
# bass f0
b=S['bass'][int(170*sr):int(176*sr)]
f0,v,_=librosa.pyin(b,fmin=30,fmax=200,sr=sr); print('bass f0 med',np.nanmedian(f0))
b=S['vocals'][int(160*sr):int(166*sr)]
f0,v,_=librosa.pyin(b,fmin=60,fmax=500,sr=sr); print('voc f0 160-166',np.nanmedian(f0),np.nanpercentile(f0,[5,95]),np.mean(v))
b=S['vocals'][int(176*sr):int(180*sr)]
f0,v,_=librosa.pyin(b,fmin=60,fmax=1500,sr=sr); print('voc f0 176-180',np.nanmedian(f0),np.nanpercentile(f0,[5,95]))
# 10ms env, boundaries
def env(x): 
    h=int(.01*sr); n=len(x)//h; return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
for t in [160+7,160+7.2,160+10,160+16.5,160+16.6]:
    print('bound',t,{k:(round(db(v[int((t-.5)*sr):int(t*sr)]),1),round(db(v[int(t*sr):int((t+.5)*sr)]),1)) for k,v in list(S.items())+[('mix',mm)]})
