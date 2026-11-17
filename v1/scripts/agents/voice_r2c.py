import numpy as np, librosa
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
v=librosa.load(D+'vocals.wav',sr=16000)[0]
def seg(a,n=3.0): i=int(round(a*16000)); return v[i:i+int(n*16000)]
def S(x): return np.log(librosa.feature.melspectrogram(y=x,sr=16000,n_fft=512,hop_length=160,n_mels=40)+1e-6)
for a,b in [(49,145.4),(49,121.2),(54.6,150.6),(49,73.4),(49,61.1)]:
    x=seg(a); best=(-1,0)
    for lag in np.arange(-0.3,0.3,0.005):
        y=seg(b+lag)
        if len(y)!=len(x): continue
        r=np.corrcoef(x,y)[0,1]
        if r>best[0]: best=(r,lag)
    sx=S(x); sy=S(seg(b+best[1])); n=min(sx.shape[1],sy.shape[1])
    print(a,b,'waveform best r',round(best[0],2),'lag',round(best[1],3),'=> true offset',round(b+best[1]-a,3),'| mel-corr',round(np.corrcoef(sx[:,:n].ravel(),sy[:,:n].ravel())[0,1],2))
print('--control: mel-corr of 3 s block at 49 vs shifted candidates (hook region 120-165 and verse 75-110)')
x=seg(49); sx=S(x); rs=[]
for b in np.arange(120,162,0.25):
    sy=S(seg(b)); n=min(sx.shape[1],sy.shape[1]); rs.append((np.corrcoef(sx[:,:n].ravel(),sy[:,:n].ravel())[0,1],b))
rs.sort(reverse=True); print('top',[(round(r,2),b) for r,b in rs[:5]],'median',round(np.median([r for r,_ in rs]),2))
rv=[]
for b in np.arange(75,108,0.25):
    sy=S(seg(b)); n=min(sx.shape[1],sy.shape[1]); rv.append(np.corrcoef(sx[:,:n].ravel(),sy[:,:n].ravel())[0,1])
print('verse2 median',round(np.median(rv),2),'max',round(max(rv),2))
