import numpy as np, librosa
D='/home/user/Listener/v1/data/video1/stems_raw/htdemucs/song/'
ph,P=0.164,0.7692
b,sr=librosa.load(D+'bass.wav',sr=11025)
hop=110
r=librosa.feature.rms(y=b,frame_length=1024,hop_length=hop)[0];db=20*np.log10(r+1e-6);t=np.arange(len(r))*hop/sr
for c in [139.5,145.7,151.9,158.3]:
    m=(t>c-1.5)&(t<c+1.5);tt=t[m];d=db[m]
    # first time exceed midpoint
    thr=(d.min()+d.max())/2;i=np.argmax(d>thr);x=(tt[i]-ph)/P
    print(c,'rise at %.2f beat-pos %.2f (mod4), range %.0f..%.0f dB'%(tt[i],x%4,d.min(),d.max()))
# 2-bar fold of drum low band across 120-168
y,_=librosa.load(D+'drums.wav',sr=22050)
S=np.abs(librosa.stft(y,n_fft=1024,hop_length=64));f=librosa.fft_frequencies(sr=22050,n_fft=1024)
e=np.diff(S[(f>=30)&(f<150)].sum(0),prepend=0);e[e<0]=0
g=P/4
def fold(a,b,n):
    out=np.zeros(n);cnt=0
    for i in range(int(a/g)//n*n,int(b/g)//n*n):
        c=int(round((ph+i*g)*22050/64));out[i%n]+=e[c-1:c+2].max()
    return out/out.max()
np.set_printoptions(precision=2,suppress=True,linewidth=220)
print(fold(33,108,32));print(fold(120,168,32))
# drum-stem events at 27.9 and 31.7 and 2:47.8
for c in [27.9,31.7,32.0]:
    rr=librosa.feature.rms(y=y,frame_length=1024,hop_length=220)[0];tt=np.arange(len(rr))*220/22050
    m=(tt>c-0.8)&(tt<c+0.8);print(c,np.round(20*np.log10(rr[m]+1e-6)[::4],0))
