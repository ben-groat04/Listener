import numpy as np, librosa, soundfile as sf
P='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
v,sr=sf.read(P+'vocals.wav'); L,R=v[:,0],v[:,1]; m=(L+R)/2
# stereo: mid/side energy of vocals per section
def db(x): return 10*np.log10(np.mean(x**2)+1e-12)
print('section: vocal rms dB, side-minus-mid dB, onset rate/s, active frac(>-45dB 50ms)')
secs=[(1,12),(12,24),(24,47),(47,59),(60,70),(70,83),(83,100),(100,119),(120,131),(131,143),(143,155),(156,167),(168,176),(176,180),(180,188)]
hop=512
env=librosa.feature.rms(y=m,frame_length=2048,hop_length=hop)[0]
envdb=20*np.log10(env+1e-9)
on=librosa.onset.onset_detect(y=m,sr=sr,hop_length=hop,units='time',backtrack=False)
for a,b in secs:
    s=m[int(a*sr):int(b*sr)]; sd=(L-R)[int(a*sr):int(b*sr)]/2
    e=envdb[int(a*sr/hop):int(b*sr/hop)]
    n=((on>=a)&(on<b)).sum()
    print(f'{a//60}:{a%60:02d}-{b//60}:{b%60:02d}  {db(s):6.1f}  {db(sd)-db(s):6.1f}  {n/(b-a):4.1f}  {np.mean(e>-45):.2f}')
# silences > 0.3s inside vocal-present spans
act=envdb>-48
gaps=[];i=0
while i<len(act):
    if not act[i]:
        j=i
        while j<len(act) and not act[j]: j+=1
        d=(j-i)*hop/sr
        if d>=0.35: gaps.append((i*hop/sr,d))
        i=j
    else:i+=1
print('gaps>=0.35s:',[(round(t,1),round(d,1)) for t,d in gaps])
# repetition: MFCC self-similarity; find strongest lag matches for 3 s segments
mf=librosa.feature.mfcc(y=librosa.resample(m,orig_sr=sr,target_sr=16000),sr=16000,n_mfcc=20,hop_length=160)[1:]
mf=(mf-mf.mean(1,keepdims=True))/mf.std(1,keepdims=True)
fps=100
def best(t0,dur=2.0,lo=None,hi=None):
    a=mf[:,int(t0*fps):int((t0+dur)*fps)]; n=a.shape[1]; res=[]
    for s in range(0,mf.shape[1]-n,5):
        if abs(s/fps-t0)<1.0: continue
        c=np.mean(np.sum(a*mf[:,s:s+n],0)/20)
        res.append((c,s/fps))
    res.sort(reverse=True); return res[:3]
for t in [1.0,13,26,41,62,65,125,135,145,150,161,164]:
    print('seg',t,[(round(c,2),round(s,1)) for c,s in best(t)])
# sweep slope in 2:30-2:37 and 2:56-3:00 via spectral centroid of vocal stem
for a,b in [(152,156),(176,180),(129,132)]:
    s=m[int(a*sr):int(b*sr)]
    S=np.abs(librosa.stft(s,n_fft=2048,hop_length=512))
    f=librosa.fft_frequencies(sr=sr,n_fft=2048)
    cen=(S*f[:,None]).sum(0)/(S.sum(0)+1e-9)
    print(a,b,'centroid Hz every .5s',[int(c) for c in cen[::22]])
