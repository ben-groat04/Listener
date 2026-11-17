import numpy as np, librosa, soundfile as sf, json
from scipy.signal import butter, sosfilt
D='/home/user/Listener/v1/data/t_cshells_cshore/'
sr=22050;hop=110
def ld(p):
    y,s=sf.read(p); y=y.mean(1) if y.ndim>1 else y
    return librosa.resample(y,orig_sr=s,target_sr=sr)
dr=ld(D+'stems_raw/htdemucs/song/drums.wav')
beats=np.array(json.load(open(D+'audio_features/beat_times.json')))
for nm,(lo,hi) in {'kick40-100':(40,100),'snare150-300+1-3k':None,'hat6k+':(6000,10000)}.items() if False else [('kick',(40,100)),('hat',(6000,10000))]:
    sos=butter(4,[lo,hi],'band',fs=sr,output='sos'); k=sosfilt(sos,dr)
    oe=librosa.onset.onset_strength(S=np.abs(librosa.stft(k,n_fft=1024,hop_length=hop))[None][0][:20] if False else None,sr=sr) if False else None
    e=librosa.feature.rms(y=k,frame_length=441,hop_length=hop)[0]
    x=np.maximum(0,np.diff(np.log10(e+1e-5)))
    on=librosa.onset.onset_detect(onset_envelope=x,sr=sr,hop_length=hop,units='time',delta=0.15,wait=8)
    for a,b in [(80,140),(140,200),(200,260),(260,317)]:
        o=on[(on>=a)&(on<b)]
        if len(o)<10: continue
        idx=np.searchsorted(beats,o).clip(1,len(beats)-1)
        ph=(o-beats[idx-1])/(beats[idx]-beats[idx-1])
        ang=2*np.pi*ph; mu=np.angle(np.exp(1j*ang).mean())/(2*np.pi); R=abs(np.exp(1j*ang).mean())
        d=((ph-mu+0.5)%1-0.5)*0.488*1000
        h,_=np.histogram((ph-mu)%1,bins=8,range=(0,1))
        ioi=np.diff(o)
        print(nm,a,b,'n',len(o),'beat-phase R=%.2f off=%.0f ms'%(R,mu*488),'8-bin hist(beat at bin0)',h.tolist(),'IOI med %.3f'%np.median(ioi),'frac IOI within 25ms of 0.49/0.98: %.2f'%np.mean((abs(ioi-0.488)<.025)|(abs(ioi-0.976)<.04)))
        if nm=='kick':
            on_beat=np.abs(d)<30; print('   kick within 30 ms of (offset-corrected) tracker beat: %.2f (chance %.2f) std of those %.0f ms'%(on_beat.mean(),60/488,d[on_beat].std()))
# end check
y,s=sf.read(D+'audio/song.wav'); y=y.mean(1) if y.ndim>1 else y
print('peak',np.abs(y).max(),'dBFS',20*np.log10(np.abs(y).max()))
n=int(s*0.01); seg=y[int(300*s):]; r=np.sqrt(np.convolve(seg**2,np.ones(n)/n,'valid'))[::n]; t=300+np.arange(len(r))*0.01
nz=np.where(r>1e-4)[0]; print('last >-80dB at',t[nz[-1]].round(2))
for tt in [317,318,319,320,325,330,335,340,342,342.8]:
    i=int((tt-300)/0.01); print(tt,round(20*np.log10(r[i]+1e-9),1),end=' | ')
