import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/'
P,a=0.7693,0.973
y,sr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050,mono=True)
oe=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
on=librosa.onset.onset_detect(onset_envelope=oe,sr=sr,hop_length=256,units='time',backtrack=False)
def ph(lo,hi):
    o=on[(on>=lo)&(on<hi)]; f=((o-a)/P*4)%1  # in sixteenth units
    # circular mean phase of 16th grid
    z=np.exp(2j*np.pi*f); m=z.mean(); return len(o),(np.angle(m)/(2*np.pi))%1,abs(m)
for lo,hi in [(100,120),(140,167),(120,135),(168.4,188),(168.4,178),(178,188)]:
    n,p,r=ph(lo,hi); print('%.0f-%.0f n=%d circ-mean sixteenth phase %.2f (x %.3f s) R=%.2f'%(lo,hi,n,p,p*P/4,r))
