import librosa,numpy as np,scipy.signal as ss
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050;ph=0.1333;P=0.49995;h=128
def L(n):return librosa.load(D+n+'.wav',sr=sr,mono=True)[0]
def bp(t):return (t-ph)/P
dr=L('drums');ba=L('bass')
# kick-band onsets (30-150Hz) and hat band (6k+) per step, step 0 = chord downbeat (beat idx 1 mod 8 after 1:28.6; idx 0 before)
def band(y,lo,hi):
    S=np.abs(librosa.stft(y,n_fft=1024,hop_length=h));f=librosa.fft_frequencies(sr=sr,n_fft=1024)
    b=S[(f>=lo)&(f<hi)].sum(0);o=np.maximum(0,np.diff(np.log1p(b*10)));return np.r_[0,o]
fr=sr/h
ko=band(dr,30,150);so=band(dr,1500,5000)
def fold(o,t0,t1,off):
    a,b=int(t0*fr),int(t1*fr);acc=np.zeros(16);n=np.zeros(16)
    for i in range(a,b):
        t=i/fr-0.02
        s=((bp(t)-off)*4)%16
        acc[int(round(s))%16]+=o[i]
    return acc/acc.sum()
np.set_printoptions(precision=3,suppress=True,linewidth=200)
for lab,t0,t1,off in [('0:30-1:00',30,60,0),('1:05-1:20',65,80,0),('1:30-1:40',90,100,1),('1:44-2:36',104,156,1),('2:40-3:24',160,204,1),('3:24-4:36',204,276,1),('4:40-4:48',280,288,1)]:
    print(lab,'kick',fold(ko,t0,t1,off));
# events in beats from nearest chord-lattice downbeat
def pos(t,off=1): 
    b=bp(t)-off; return b%8
for t in [104.4,115.4,250.4,88.6,98.5]:
    print('t %.1f beat from lattice(8 beat) %.2f'%(t,pos(t)))
# bass holes and noise around 4:38-4:47
bdb=librosa.amplitude_to_db(librosa.feature.rms(y=ba,frame_length=1024,hop_length=h)[0]+1e-9);
for lo,hi in [(277,288),(155,160),(214,219),(84,90)]:
    a,b=int(lo*fr),int(hi*fr);seg=bdb[a:b];med=np.median(seg)
    idx=np.where(seg<med-8)[0]
    if len(idx):
        runs=np.split(idx,np.where(np.diff(idx)>2)[0]+1)
        print('bass holes',lo,hi,'med %.1f'%med,[('%.2f-%.2f'%((a+r[0])/fr,(a+r[-1])/fr),'beat %.2f'%pos((a+r[0])/fr)) for r in runs if len(r)>=3])
# drum hits at 4:38.5 noise
no=band(dr,6000,10000)
for lo,hi in [(276,280)]:
    a,b=int(lo*fr),int(hi*fr);p=ss.find_peaks(no[a:b],height=np.percentile(no[a:b],95))[0]
    print('hat-band peaks',[('%.2f'%((a+x)/fr),'%.2f'%pos((a+x)/fr)) for x in p][:10])
# 3.6 section-change drum/bass level around 156.8, 216.8
for t0 in (156.8,216.8,276.8):
    a=int((t0-3)*fr);b=int((t0+3)*fr)
    sd=librosa.amplitude_to_db(librosa.feature.rms(y=dr,frame_length=1024,hop_length=h)[0]+1e-9)[a:b]
    print(t0,'drum dB range %.1f..%.1f'%(sd.min(),sd.max()),'bass min at %.2f'%((a+np.argmin(bdb[a:b]))/fr))
# 1:24-1:28.6 break and 0:28 offset
print('beat of 1:28.62 on grid %.2f, of 0:28.0 %.2f; diff beats %.2f'%(bp(88.62),bp(28.0),bp(88.62)-bp(28.0)))
