import numpy as np,librosa
D='stems_raw/htdemucs/song/'
R=np.load('/tmp/claude-0/r.npy',allow_pickle=True).item()
h=0.1
v=R['vocals']
# vocal activity segments above -45 dB, gap merge 1.0s
act=v>-50
segs=[];s=None
for i,a in enumerate(act):
    t=i*h
    if a and s is None: s=t
    if not a and s is not None:
        if segs and s-segs[-1][1]<1.0: segs[-1][1]=t
        else: segs.append([s,t])
        s=None
print('vocal segs',[(round(a,1),round(b,1)) for a,b in segs if b-a>0.3][:80])
# call onset times 284-300
y,sr=librosa.load(D+'vocals.wav',sr=22050)
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=128)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=128,units='time')
print('onsets 283-301',[round(o,2) for o in on if 283<o<301])
print('mod 2 rel 88.61',[round((o-88.61)%2,2) for o in on if 283<o<301])
# mix band 4-10k
m,sr=librosa.load('audio/song.wav',sr=22050,mono=True)
S=np.abs(librosa.stft(m,n_fft=2048,hop_length=512))**2
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
b=10*np.log10(S[(f>4000)&(f<10000)].sum(0)+1e-12)
fr=sr/512
for a in range(150,260,10):
    print(a,round(b[int(a*fr):int((a+10)*fr)].mean(),1),end=' | ')
print()
for a in [160,165,170,175,180,185,190]:pass
# other-stem
o,sr=librosa.load(D+'other.wav',sr=22050)
So=np.abs(librosa.stft(o,n_fft=2048,hop_length=512))**2
bo=10*np.log10(So[(f>4000)&(f<10000)].sum(0)+1e-12)
for a in range(150,260,10):
    print(a,round(bo[int(a*fr):int((a+10)*fr)].mean(),1),end=' | ')
print()
ot=10*np.log10(So.sum(0)+1e-12)
print('other total 2:40-2:56 per s',[round(ot[int(t*fr):int((t+1)*fr)].mean(),1) for t in range(160,175)])
