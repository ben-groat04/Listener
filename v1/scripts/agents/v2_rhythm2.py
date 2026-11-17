import librosa,numpy as np
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050
def load(n): return librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
dr=load('drums'); ba=load('bass')
def filt(y,lo,hi):
    import scipy.signal as s
    sos=s.butter(4,[lo,hi],'band',fs=sr,output='sos'); return s.sosfilt(sos,y)
def onsets(y):
    o=librosa.onset.onset_strength(y=y,sr=sr,hop_length=128)
    t=librosa.onset.onset_detect(onset_envelope=o,sr=sr,hop_length=128,units='time',backtrack=False)
    return t
# global tempo drift: refine period by fit on drums 100-300
for name,y,bands in [('drums',dr,{'kick<150':(30,150),'snare/clap1.5-5k':(1500,5000),'hat>6k':(6000,10500)}),('bass',ba,{'bass':(30,400)})]:
    for lab,(t0,t1) in {'A 0:28-0:40':(28,40),'B 1:44-2:36':(104,156),'C 2:40-3:20':(160,200),'D 3:40-4:40':(220,280)}.items():
        seg=y[int(t0*sr):int(t1*sr)]
        for bn,(lo,hi) in bands.items():
            t=onsets(filt(seg,lo,hi))+t0
            ph=((t-t0)%2.0)/0.125
            # fit phase offset: use circular mean of ph mod 16 with 16 steps
            h=np.histogram(((ph+0.5)%16),bins=16,range=(0,16))[0]
            print(name,lab,bn,'n=',len(t),'steps(offset0 at',t0,')',' '.join(f'{x:2d}' for x in h))
