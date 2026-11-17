import librosa,numpy as np
D='/home/user/Listener/v1/data/video2/stems_raw/htdemucs/song/'
sr=22050;hop=64;fr=sr/hop;ph=0.1333;P=0.49995
y=librosa.load(D+'other.wav',sr=sr,mono=True)[0]
e=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
def fold(t0,t1):
    o=np.zeros(16);per=4*P
    # downbeat = chord lattice = beat idx 1 mod 4 -> origin shift one beat
    for i in range(int(t0*fr),int(t1*fr)):
        t=i/fr;o[int((((t-ph-P)%per)/per)*16)%16]+=e[i]
    return o/o.sum()
for r in [(104,200),(200,277)]:
    print(r,np.round(fold(*r),3))
# voice burst times from voice specialist
for t in [280.6,282.5,284.5,286.5,288.5,290.5,292.5,294.5,296.6,298.7]:
    b=(t-ph)/P;print(t,'beat idx %.2f ; rel to chord-lattice downbeat (mod4) %.2f beats'%(b,(b-1)%4))
