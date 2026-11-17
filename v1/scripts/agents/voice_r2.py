import numpy as np, librosa, json
D='/home/user/Listener/v1/data/video1/'
y,sr=librosa.load(D+'stems_raw/htdemucs/song/vocals.wav',sr=16000)
o,_=librosa.load(D+'stems_raw/htdemucs/song/other.wav',sr=16000)
dr,_=librosa.load(D+'stems_raw/htdemucs/song/drums.wav',sr=16000)
bt=np.array(json.load(open(D+'audio_features/beat_times.json')))
hop=160
r=librosa.feature.rms(y=y,frame_length=640,hop_length=hop)[0]; db=20*np.log10(r+1e-9)
on=db>-42
seg=[];s=None
for i,v in enumerate(on):
    if v and s is None:s=i
    if not v and s is not None:seg.append([s,i]);s=None
mg=[]
for a,b in seg:
    if mg and a-mg[-1][1]<=30: mg[-1][1]=b
    else: mg.append([a,b])
mg=[(a/100,b/100) for a,b in mg if b-a>=40]
bar=4*0.7665
def pos(t):
    i=np.searchsorted(bt,t)-1
    if i<0: return (0,0.0)
    if i+1>=len(bt): return (i,min(1.0,(t-bt[i])/0.766))
    ph=(t-bt[i])/(bt[i+1]-bt[i]); return i,ph
print('burst start/end beat-index (mod4) and phase')
for a,b in mg:
    pa,pb=pos(a),pos(b)
    print('%d:%05.2f-%d:%05.2f  start beat%%4=%d ph=%.2f | end beat%%4=%d ph=%.2f | dur %.1f bars %.2f'%(a//60,a%60,b//60,b%60,pa[0]%4,pa[1],pb[0]%4,pb[1],b-a,(b-a)/bar))
# repeat test: 0:24.4-0:32 vs 2:44.0-2:48.2 mel envelope xcorr
def mel(t0,t1):
    seg=y[int(t0*sr):int(t1*sr)]
    return librosa.power_to_db(librosa.feature.melspectrogram(y=seg,sr=sr,n_fft=512,hop_length=160,n_mels=40,fmax=6000))
A=mel(24.0,32.5);B=mel(43.5,49.0)
B2=mel(163.5,169.0)
def best(A,B):
    A=A-A.mean(1,keepdims=True);B=B-B.mean(1,keepdims=True)
    n=B.shape[1];res=[]
    for k in range(0,A.shape[1]-n+1):
        a=A[:,k:k+n];res.append((a*B).sum()/np.sqrt((a**2).sum()*(B**2).sum()))
    return max(res),np.argmax(res)/100
for nm,(t0,t1) in {'2:44-2:49':(164,169),'0:41-0:43 (De 12e)':(41,43)}.items():
    Bm=mel(t0,t1)
    A2=mel(24.0,32.5)
    print(nm,'vs 0:24-0:32.5: best corr %.2f at +%.2f s'%best(A2,Bm))
# sanity: control, random segment of speech vs same
Bc=mel(51,53.5); print('control 0:51-0:53.5 vs 0:24-0:32.5: %.2f at %.2f'%best(mel(24.0,32.5),Bc))
Bc=mel(2*60+24,2*60+27); print('control 2:24-2:27 vs 0:24-0:32.5: %.2f at %.2f'%best(mel(24.0,32.5),Bc))
# leakage: corr of vocal-stem 2-8k envelope with other-stem and drum-stem 2-8k envelopes within bursts vs voiced fraction
def band(x,lo,hi):
    S=np.abs(librosa.stft(x,n_fft=512,hop_length=160))
    f=librosa.fft_frequencies(sr=sr,n_fft=512);return S[(f>=lo)&(f<hi)].sum(0)
vb=band(y,3000,8000);ob=band(o,3000,8000);dbn=band(dr,3000,8000);vm=band(y,300,3000)
for a,b in mg:
    i,j=int(a*100),int(b*100)
    print('%d:%05.1f  corr(voc HF, drums HF)=%.2f  corr(voc HF,other HF)=%.2f  voc HF/mid=%.2f'%(a//60,a%60,np.corrcoef(vb[i:j],dbn[i:j])[0,1],np.corrcoef(vb[i:j],ob[i:j])[0,1],vb[i:j].sum()/vm[i:j].sum()))
# end of last voice vs cut at 167.8
print('vocal dB around 2:46-2:49 per 0.1s:')
print(' '.join('%.0f'%db[int(t*100)] for t in np.arange(166.0,169.0,0.1)))
