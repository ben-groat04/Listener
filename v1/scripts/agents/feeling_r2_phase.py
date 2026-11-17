import numpy as np, librosa
y,sr=librosa.load('data/video2/stems_raw/htdemucs/song/drums.wav',sr=22050,mono=True)
env=librosa.onset.onset_strength(y=y,sr=sr,hop_length=256)
t=librosa.frames_to_time(np.arange(len(env)),sr=sr,hop_length=256)
def ph(a,b,P=0.5):
    m=(t>=a)&(t<b); e=env[m]-env[m].mean(); tt=t[m]
    z=(e*np.exp(2j*np.pi*tt/P)).sum()
    return (np.angle(z)/(2*np.pi)*P)%P, abs(z)/e.sum()
for a,b in [(29,40),(44,60),(89,100),(104,125),(130,155),(200,240),(260,288)]:
    print(a,b,'phase %.3f s  strength %.2f'%ph(a,b))
