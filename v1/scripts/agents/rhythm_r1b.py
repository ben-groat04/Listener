import numpy as np, librosa, json, soundfile as sf
D='/home/user/Listener/v1/data/t_cshells_cshore/'
beats=np.array(json.load(open(D+'audio_features/beat_times.json')))
if beats.ndim>1: beats=beats[:,0]
for s in range(40,320,10):
    m=(beats>=s)&(beats<s+10)
    if m.sum()>3: print(s, round(60/np.median(np.diff(beats[m])),1), end=' | ')
print()
on=np.load('/tmp/on.npy')
# 120 vs 123: block hit times
sr=22050
y,s=sf.read(D+'audio/song.wav'); y=y.mean(1) if y.ndim>1 else y
y=librosa.resample(y,orig_sr=s,target_sr=sr)
env=librosa.feature.rms(y=y,frame_length=441,hop_length=220)[0]; te=220/sr
de=np.diff(20*np.log10(env+1e-7))
pk=np.where(de>9)[0]*te
# merge
hits=[]
for p in pk:
    if not hits or p-hits[-1]>1.5: hits.append(p)
print('big mix jumps (>9 dB in 10ms):',[round(h,2) for h in hits if 40<h<260])
h=np.array([x for x in hits if 56<x<150]); print('IOI',np.diff(h).round(2))
# phase-corrected 16th grid
for a,b in [(80,120),(120,200),(200,320)]:
    o=on[(on>=a)&(on<b)]
    bt=beats; idx=np.searchsorted(bt,o).clip(1,len(bt)-1); ph=((o-bt[idx-1])/(bt[idx]-bt[idx-1]))
    # circular mean on 8th grid
    ang=2*np.pi*ph*2; mu=np.angle(np.exp(1j*ang).mean())/(2*np.pi)/2*1  # offset in beats mod 0.5
    off=(ph-mu)%1
    h8,_=np.histogram(off,bins=16,range=(0,1))
    R=np.abs(np.exp(1j*ang).mean())
    print(a,b,'8th-grid offset(s)',round(mu*0.488,3),'R8th',round(R,2),'16-bin hist',h8.tolist())
    q=(off*4)%1; dev=np.minimum(q,1-q)*0.488/4*1000
    print('  deviation from nearest 16th (ms) median',np.median(dev).round(0),'p90',np.percentile(dev,90).round(0))
