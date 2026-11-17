import numpy as np, soundfile as sf, librosa
from scipy.signal import correlate
D='/home/user/Listener/v1/data/t_birdwalk/stems_raw/htdemucs/song/'
v,sr=sf.read(D+'vocals.wav'); o,_=sf.read(D+'other.wav'); mix,_=sf.read('/home/user/Listener/v1/data/t_birdwalk/audio/song.wav')
print(sr,v.shape,o.shape,mix.shape)
def seg(x,a,b): return x[int(a*sr):int(b*sr)]
def side(x): return (x[:,0]-x[:,1])/2
def mid(x): return (x[:,0]+x[:,1])/2
def env(x,hop=512):
    n=len(x)//hop; return np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))
print('Q1: vocal side vs other side envelope corr; vocal side vs vocal mid')
for a,b in [(0.5,10),(12,24),(50,58),(62,70),(125,133),(150,158),(165,170),(14,24),(75,100),(185,195) ]:
    vs=env(seg(side(v),a,b)); os_=env(seg(side(o),a,b)); vm=env(seg(mid(v),a,b)); om=env(seg(mid(o),a,b))
    c=lambda x,y: np.corrcoef(x,y)[0,1]
    # rough waveform corr of sides
    ws=np.corrcoef(seg(side(v),a,b),seg(side(o),a,b))[0,1]
    print(f'{a}-{b}: sideV/sideO env r={c(vs,os_):.2f} wave r={ws:.2f}; sideV/midV env r={c(vs,vm):.2f}; midV/midO={c(vm,om):.2f}; rms side/mid vocal={vs.mean()/vm.mean():.2f}; side vocal dB={20*np.log10(vs.mean()+1e-9):.0f} side other dB={20*np.log10(os_.mean()+1e-9):.0f}')
# Q2: glide near 2:56-3:02
vm=mid(v); y=librosa.resample(vm,orig_sr=sr,target_sr=22050)
for a,b in [(176,181),(9,13),(164,168)]:
    f0,vf,vp=librosa.pyin(y[int(a*22050):int(b*22050)],fmin=70,fmax=1500,sr=22050,frame_length=2048,hop_length=256)
    t=a+np.arange(len(f0))*256/22050
    print('pitch',a,b)
    for ti,fi,p in zip(t[::6],f0[::6],vp[::6]):
        if not np.isnan(fi): print(f'  {int(ti//60)}:{ti%60:05.2f} {fi:.0f}Hz {librosa.hz_to_note(fi)} p={p:.2f}')
    rms=librosa.feature.rms(y=y[int(a*22050):int(b*22050)],hop_length=2048)[0]
    print('  rms dB',np.round(20*np.log10(rms+1e-9)[::2]).astype(int))
