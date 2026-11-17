import numpy as np, librosa, json
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
sr=22050; y,_=librosa.load(D+'drums.wav',sr=sr,mono=True)
bt=np.array(json.load(open('/home/user/Listener/v1/data/video1/audio_features/beat_times.json')))
o=librosa.onset.onset_detect(y=y,sr=sr,hop_length=256,units='time')
P=0.7664
def phase(ts,ref): return ((ts-ref)/P)%1
ref=bt[-1]
for a,b in [(150,167.5),(168.5,178),(178,188)]:
    ts=o[(o>a)&(o<b)]; ph=phase(ts,ref)
    h,_=np.histogram(ph,bins=8,range=(0,1)); print(a,b,'phase hist',h.tolist(),'peak',np.round(np.argmax(h)/8,2))
# fit period after stop
ts=o[(o>168.5)&(o<188)]; ac=np.histogram(np.diff(ts),bins=np.arange(0.1,0.9,0.02))[0]
print('post-stop IOI mode',0.1+0.02*np.argmax(ac))
# tempo drift: beat IBI by section
ib=np.diff(bt); mid=(bt[1:]+bt[:-1])/2
for a in range(0,180,30):
    m=(mid>=a)&(mid<a+30); print(a,'mean beat period',round(ib[m].mean(),4),'->',round(60/ib[m].mean(),2),'bpm')
