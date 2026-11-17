import librosa,numpy as np,sys
d='/home/user/Listener/v1/data/video2/'
def ld(p):
    y,sr=librosa.load(p,sr=22050,offset=110,duration=40);return y,sr
y,sr=ld(d+'audio/song.wav')
dr,_=ld(d+'stems_raw/htdemucs/song/drums.wav')
ba,_=ld(d+'stems_raw/htdemucs/song/bass.wav')
ot,_=ld(d+'stems_raw/htdemucs/song/other.wav')
def on(x,fmin=None):
    o=librosa.onset.onset_strength(y=x,sr=sr,hop_length=256)
    f=librosa.onset.onset_detect(onset_envelope=o,sr=sr,hop_length=256,units='time',backtrack=False)
    return f+110
od=on(dr);print('drum onsets 2:00-2:20',len(od[(od>=120)&(od<140)]))
sel=od[(od>=120)&(od<140)];ioi=np.diff(sel);print('IOI median',np.median(ioi),'->bpm',60/np.median(ioi)*1)
print(np.round(sel,2))
# drum band energy: kick(<150) snare(150-2k) hat(>5k) per 2 s
S=np.abs(librosa.stft(dr,n_fft=2048,hop_length=512));fr=librosa.fft_frequencies(sr=sr,n_fft=2048);tt=librosa.frames_to_time(np.arange(S.shape[1]),sr=sr,hop_length=512)+110
for a in range(112,142,2):
    m=(tt>=a)&(tt<a+2)
    f=lambda lo,hi:10*np.log10((S[(fr>=lo)&(fr<hi)][:,m]**2).sum()+1e-9)
    print(a,'kick %.0f snare %.0f hat %.0f'%(f(30,150),f(150,2000),f(5000,11000)))
# centroid of mix & other per 4 s
for nm,x in(('mix',y),('other',ot)):
    c=librosa.feature.spectral_centroid(y=x,sr=sr,hop_length=512)[0];tc=librosa.frames_to_time(np.arange(len(c)),sr=sr,hop_length=512)+110
    print(nm,[int(c[(tc>=a)&(tc<a+4)].mean()) for a in range(112,142,4)])
# bass note pitch via pyin
f0,vf,_=librosa.pyin(ba,fmin=30,fmax=200,sr=sr,hop_length=512);tf=librosa.frames_to_time(np.arange(len(f0)),sr=sr,hop_length=512)+110
for a in range(120,140,2):
    m=(tf>=a)&(tf<a+2)&~np.isnan(f0)
    print(a,'bass median',librosa.hz_to_note(np.median(f0[m])) if m.sum() else None)
# tempo curve
o=librosa.onset.onset_strength(y=y,sr=sr);print('tempo',librosa.beat.tempo(onset_envelope=o,sr=sr,start_bpm=160)[0])
