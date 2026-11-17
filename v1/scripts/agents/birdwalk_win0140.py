import numpy as np, librosa, json
D='/home/user/Listener/v1/data/t_birdwalk/'
S='stems_raw/htdemucs/song/'
sr=22050
def load(p):
    y,_=librosa.load(D+p,sr=sr,mono=False); return y
mix=load('audio/song.wav'); st={k:load(S+k+'.wav') for k in['drums','bass','vocals','other']}
def mono(y): return y if y.ndim==1 else y.mean(0)
def db(x): return 20*np.log10(max(x,1e-9))
def seg(y,a,b):
    return y[...,int(a*sr):int(b*sr)]
def rms(y,a,b): return db(np.sqrt(np.mean(mono(seg(y,a,b))**2)))
hop=int(.01*sr)
def env(y,a,b):
    x=mono(seg(y,a,b)); n=len(x)//hop
    return np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))
print('peak 140-160 mix sample', db(np.abs(seg(mix,140,160)).max()))
# boundary table
for b in [143.0,143.4,144.0,155.0,155.6,155.8,156.4]:
    row=[]
    for k in['drums','bass','vocals','other']:
        row.append('%s %.1f->%.1f'%(k,rms(st[k],b-1.35,b),rms(st[k],b,b+1.35)))
    print(b,row,'mix %.1f->%.1f'%(rms(mix,b-1.35,b),rms(mix,b,b+1.35)))
# bass onsets/ drums onsets
for k in ['bass','drums']:
    y=mono(st[k]); 
    on=librosa.onset.onset_detect(y=y,sr=sr,units='time',backtrack=False,delta=0.1)
    print(k,[round(t,2) for t in on if 139<=t<=161])
# kick band peaks
import scipy.signal as sg
d=mono(st['drums']); b,a=sg.butter(4,[40/(sr/2),120/(sr/2)],'band'); kb=sg.filtfilt(b,a,d)
e=np.abs(sg.hilbert(kb)); e=np.convolve(e,np.ones(441)/441,'same')
pk,_=sg.find_peaks(e,height=0.25*e[int(139*sr):int(161*sr)].max(),distance=int(.1*sr))
print('kicks',[round(p/sr,2) for p in pk if 139<=p/sr<=161])
bt=np.array(json.load(open(D+'audio_features/beat_times.json')) if not isinstance(json.load(open(D+'audio_features/beat_times.json')),dict) else json.load(open(D+'audio_features/beat_times.json'))['beats'])
ks=np.array([p/sr for p in pk if 139<=p/sr<=161])
print('kick dev from beat grid ms',[round(1000*(k-bt[np.argmin(abs(bt-k))])) for k in ks])
print('kick IOI',np.round(np.diff(ks),2))
# bass pitch
y=mono(st['bass'])
for t in [140.5,141.5,142.3,155.9,157,158,159,160]:
    x=y[int((t)*sr):int((t+.3)*sr)]
    f=np.abs(np.fft.rfft(x*np.hanning(len(x)),n=2**16)); fr=np.fft.rfftfreq(2**16,1/sr)
    m=(fr>30)&(fr<300); print('bass',t,round(fr[m][np.argmax(f[m])],1))
# mix band shares & centroid
for a,b2 in [(140,143.3),(144.5,155.5),(156,160)]:
    x=mono(seg(mix,a,b2)); S_=np.abs(np.fft.rfft(x))**2; fr=np.fft.rfftfreq(len(x),1/sr)
    tot=S_.sum(); sh=lambda lo,hi:10*np.log10(S_[(fr>=lo)&(fr<hi)].sum()/tot+1e-12)
    cen=(fr*S_).sum()/tot
    m=seg(mix,a,b2); mid=(m[0]+m[1])/2; side=(m[0]-m[1])/2
    print(a,b2,'centroid %.0f'%cen,'<150 %.1f 150-500 %.1f 500-2k %.1f 2-5k %.1f >5k %.1f'%(sh(0,150),sh(150,500),sh(500,2000),sh(2000,5000),sh(5000,1e5)),'side/mid dB %.1f'%(db(np.sqrt((side**2).mean()))-db(np.sqrt((mid**2).mean()))),'rms %.1f'%rms(mix,a,b2))
# vocal onset rate
for a,b2 in [(140,144),(144,155.5),(156,160)]:
    on=librosa.onset.onset_detect(y=mono(st['vocals'])[int(a*sr):int(b2*sr)],sr=sr,units='time')
    print('vocal onsets/s',a,b2,round(len(on)/(b2-a),2))
# drum onsets in 156-160 and stab (other) onsets
# drops: drum hit in 144-155.5
e=env(st['drums'],144,155.5); print('drums max env dB in gap',db(e.max()),'median',db(np.median(e)))
e=env(st['bass'],144.3,155.5); print('bass max env dB in gap',db(e.max()))
# lead pitch range
l=json.load(open(D+'music_views/lead_notes.json'))
print([ (n['note']) for n in l][:3], len(l))
# mix level dB drop
print('mix 141-143 rms',rms(mix,141,143),'145-155',rms(mix,145,155),'157-160',rms(mix,157,160))
# 1:08 bar similarity of vocal mel
