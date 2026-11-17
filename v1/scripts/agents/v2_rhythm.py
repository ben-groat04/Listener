import librosa,numpy as np,json,sys
D='/home/user/Listener/v1/data/video2/'
y,sr=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=22050,mono=True)
b,_=librosa.load(D+'stems_raw/htdemucs/song/bass.wav',sr=22050,mono=True)
hop=256
def ac(sig,t0,t1,name):
    s=sig[int(t0*sr):int(t1*sr)]
    o=librosa.onset.onset_strength(y=s,sr=sr,hop_length=hop)
    o=o-o.mean(); a=np.correlate(o,o,'full')[len(o)-1:]; a/=a[0]
    fr=sr/hop; lags=np.arange(len(a))/fr
    pk=[(round(lags[i],3),round(a[i],2)) for i in range(5,int(4*fr)) if a[i]>a[i-1] and a[i]>=a[i+1] and a[i]>0.15]
    print(name,t0,t1,pk[:14])
for t0,t1 in [(28,40),(104,128),(128,157),(160,200),(200,217),(217,277),(277,300)]:
    ac(y,t0,t1,'drums')
for t0,t1 in [(104,128),(160,200),(217,277)]:
    ac(b,t0,t1,'bass')
