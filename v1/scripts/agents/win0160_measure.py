import librosa, numpy as np, scipy.signal as sg
D='/home/user/Listener/v1/data/t_birdwalk/'; S='stems_raw/htdemucs/song/'; sr=22050
t0,t1=150,185
L=lambda p: librosa.load(D+p,sr=sr,offset=t0,duration=t1-t0)[0]
y=L('audio/song.wav'); st={k:L(S+k+'.wav') for k in ['vocals','drums','bass','other']}
def env(x,w):
    h=int(sr*w); n=len(x)//h; return 20*np.log10(np.sqrt((x[:n*h].reshape(n,h)**2).mean(1))+1e-9)
al=dict(mix=y,**st)
print('sample peak 160-180', 20*np.log10(np.abs(y[10*sr:30*sr]).max()))
segs=[(160,167),(167,170),(170,176.5),(176.5,180)]
for k,x in al.items():
    e=env(x,0.1); print(k,[round(float(e[int((a-t0)*10):int((b-t0)*10)].mean()),1) for a,b in segs])
for k,x in al.items():
    e=env(x,0.01)
    print(k,'10ms',{tt:round(float(e[int((tt-t0)*100)]),1) for tt in (166.8,167.0,167.3,169.8,170.0,170.3,170.5,176.0,176.4,176.6,176.8)})
# kicks
b,a=sg.butter(4,150,'low',fs=sr); lo=sg.filtfilt(b,a,st['drums'])
oe=librosa.onset.onset_strength(y=lo,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time')+t0
on=on[(on>=158)&(on<=182)]; print('kick',np.round(on,2)); print('IOI',np.round(np.diff(on),2))
# full drum onsets
do=librosa.onset.onset_detect(y=st['drums'],sr=sr,hop_length=256,units='time')+t0
do=do[(do>=158)&(do<=182)]; print('drum all',np.round(do,2)); print('IOI',np.round(np.diff(do),2))
bo=librosa.onset.onset_detect(y=st['bass'],sr=sr,hop_length=256,units='time')+t0
print('bass on',np.round(bo[(bo>=158)&(bo<=182)],2))
# bass pitch
for a_,b_ in [(160,166),(170,176),(177,180)]:
    seg=st['bass'][int((a_-t0)*sr):int((b_-t0)*sr)]
    f0,vf,_=librosa.pyin(seg,fmin=30,fmax=200,sr=sr); f=f0[~np.isnan(f0)]
    print('bass f0',a_,b_,np.percentile(f,[10,50,90]) if len(f) else None)
for a_,b_ in [(160,167),(177,180)]:
    seg=st['vocals'][int((a_-t0)*sr):int((b_-t0)*sr)]
    f0,vf,_=librosa.pyin(seg,fmin=60,fmax=800,sr=sr); f=f0[~np.isnan(f0)]
    print('vox f0',a_,b_,np.percentile(f,[5,50,95]) if len(f) else None,vf.mean())
vo=librosa.onset.onset_detect(y=st['vocals'][:int(17*sr)],sr=sr,hop_length=256,units='time')+t0
v=vo[(vo>=160)&(vo<=167)];print('vox onsets',len(v),np.median(np.diff(v)))
for nm,(a_,b_) in {'vox':(160,167),'nonvox':(168,176),'return':(177,180)}.items():
    seg=y[int((a_-t0)*sr):int((b_-t0)*sr)]
    print(nm,'centroid',round(float(librosa.feature.spectral_centroid(y=seg,sr=sr).mean())),'roll95',round(float(librosa.feature.spectral_rolloff(y=seg,sr=sr,roll_percent=.95).mean())))
# stereo
yy,_=librosa.load(D+'audio/song.wav',sr=sr,mono=False,offset=160,duration=20)
m=(yy[0]+yy[1])/2;s=(yy[0]-yy[1])/2
for a_,b_ in [(0,7),(8,16),(17,20)]:
    sl=slice(int(a_*sr),int(b_*sr));print('S/M dB',a_+160,20*np.log10(np.sqrt((s[sl]**2).mean())/np.sqrt((m[sl]**2).mean())))
print('tempo', librosa.beat.beat_track(y=y[10*sr:30*sr],sr=sr)[0])
# end
yf,sr0=librosa.load(D+'audio/song.wav',sr=None); print('dur',len(yf)/sr0)
