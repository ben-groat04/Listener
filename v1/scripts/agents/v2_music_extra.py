import librosa, numpy as np, json
D='/home/user/Listener/v1/data/video2/'
y,sr=librosa.load(D+'audio/song.wav',sr=22050,mono=False)
m=y.mean(0); L,R=y[0],y[1]
mid=(L+R)/2; side=(L-R)/2
hop=512
S=np.abs(librosa.stft(m,n_fft=2048,hop_length=hop))**2
f=librosa.fft_frequencies(sr=sr,n_fft=2048)
bands={'sub<80':(20,80),'bass80-250':(80,250),'mid250-2k':(250,2000),'pres2-5k':(2000,5000),'air5k+':(5000,11000)}
H,P=librosa.decompose.hpss(np.abs(librosa.stft(m,hop_length=hop)))
fps=sr/hop
def seg(a,b):
    i,j=int(a*fps),int(b*fps)
    r={}
    tot=S[:,i:j].sum()
    for k,(lo,hi) in bands.items():
        r[k]=round(float(S[(f>=lo)&(f<hi),i:j].sum()/tot),3)
    r['perc_frac']=round(float((P[:,i:j]**2).sum()/((P[:,i:j]**2).sum()+(H[:,i:j]**2).sum())),3)
    ii,jj=int(a*sr),int(b*sr)
    r['side/mid']=round(float(np.sqrt((side[ii:jj]**2).mean()/(mid[ii:jj]**2).mean())),3)
    r['rms_db']=round(float(20*np.log10(np.sqrt((m[ii:jj]**2).mean())+1e-9)),1)
    r['crest']=round(float(np.abs(m[ii:jj]).max()/np.sqrt((m[ii:jj]**2).mean())),2)
    return r
secs=[(0,28),(28,41),(41,58),(58,76),(76,89),(89,101),(101,157),(157,177),(177,217),(217,277),(277,301),(301,306)]
out={f'{a}-{b}':seg(a,b) for a,b in secs}
# tempo
oenv=librosa.onset.onset_strength(y=m,sr=sr,hop_length=hop)
for a,b in [(10,60),(90,150),(180,240),(260,300)]:
    t=librosa.feature.tempo(onset_envelope=oenv[int(a*fps):int(b*fps)],sr=sr,hop_length=hop,aggregate=None)
    out[f'tempo_{a}-{b}']=[round(float(np.median(t)),1)]
    ac=librosa.autocorrelate(oenv[int(a*fps):int(b*fps)]);
    lags=np.arange(len(ac));bp=60*fps/np.maximum(lags,1)
    sel=(bp>50)&(bp<220); idx=np.argsort(ac*sel)[::-1][:1]
    out[f'tempo_{a}-{b}'].append(round(float(bp[idx[0]]),1))
# silences/ per-sec rms
rms=librosa.feature.rms(y=m,hop_length=hop)[0]
ps=[float(rms[int(t*fps):int((t+1)*fps)].mean()) for t in range(int(len(m)/sr))]
out['per_sec_rms']=[round(x,4) for x in ps]
d=np.diff(ps); out['biggest_rises']=[(int(i+1),round(float(d[i]),3)) for i in np.argsort(d)[::-1][:8]]
out['biggest_drops']=[(int(i+1),round(float(d[i]),3)) for i in np.argsort(d)[:8]]
# low-energy gaps
gap=[t for t,x in enumerate(ps) if x<0.02]; out['quiet_secs']=gap
json.dump(out,open(D+'audio_features/extra/v2_extra.json','w'),indent=1)
for k,v in out.items():
    if k!='per_sec_rms': print(k,v)
